"""
Explainable AI (XAI) Module using TreeSHAP.
Computes feature importances, beeswarm plots, dependence plots, waterfall plots, and interactions.
Requirement 4 of Topic 11.
"""

import os
import json
import logging
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import joblib

from src.config import (
    DATA_PROCESSED_DIR,
    MODELS_DIR,
    RESULTS_DIR,
    FIGURES_DIR,
    RANDOM_SEED,
    NUMERIC_FEATURES,
    TARGET_COLUMN
)
from src.data_processing import create_sliding_windows

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def generate_feature_names(lookback: int, base_features: list[str]) -> list[str]:
    """
    Creates interpretable feature names for sliding window representations:
    e.g. CQI_t, CQI_t-1, ..., SNR_t, SNR_t-1, etc.
    """
    names = []
    for t in range(lookback - 1, -1, -1):
        suffix = "_t" if t == 0 else f"_t-{t}"
        for f in base_features:
            clean_name = f.replace("_scaled", "")
            names.append(f"{clean_name}{suffix}")
    return names


def run_explainability_analysis():
    """
    Runs TreeSHAP explanation on the trained XGBoost model.
    """
    logger.info("=== STARTING EXPLAINABLE AI (XAI) ANALYSIS (TreeSHAP) ===")

    # 1. Load trained XGBoost model
    model_path = MODELS_DIR / "xgboost_best.joblib"
    if not model_path.exists():
        model_path = MODELS_DIR / "xgboost_L10_H1.joblib"
    if not model_path.exists():
        raise FileNotFoundError(f"Trained model not found at {model_path}! Run models_ml.py first.")

    model = joblib.load(model_path)
    logger.info(f"Loaded trained model from {model_path}")

    # 2. Load test set and create sliding windows
    test_df = pd.read_csv(DATA_PROCESSED_DIR / "test_data.csv")
    lookback = 10
    horizon = 1
    feature_cols = [f"{col}_scaled" for col in NUMERIC_FEATURES]

    X_test, y_test = create_sliding_windows(
        test_df, lookback=lookback, horizon=horizon, feature_cols=feature_cols
    )

    feature_names = generate_feature_names(lookback, NUMERIC_FEATURES)

    # Subsample test set for SHAP computation
    np.random.seed(RANDOM_SEED)
    sample_size = min(1500, len(X_test))
    sample_indices = np.random.choice(len(X_test), sample_size, replace=False)
    X_sample = X_test[sample_indices]
    y_sample = y_test[sample_indices]

    df_sample = pd.DataFrame(X_sample, columns=feature_names)

    # 3. Compute TreeSHAP values
    logger.info(f"Computing TreeSHAP values for {sample_size} test samples...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(df_sample)

    # 4. Global Feature Importance Calculation
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "mean_abs_shap": mean_abs_shap
    }).sort_values(by="mean_abs_shap", ascending=False).reset_index(drop=True)

    # Aggregate importance by base KPI across time lags
    base_importance = {}
    for base in NUMERIC_FEATURES:
        matching_cols = [col for col in feature_names if col.startswith(base)]
        base_importance[base] = float(importance_df[importance_df["feature"].isin(matching_cols)]["mean_abs_shap"].sum())

    base_importance_sorted = dict(sorted(base_importance.items(), key=lambda item: item[1], reverse=True))

    shap_results = {
        "top_lagged_features": importance_df.head(20).to_dict(orient="records"),
        "base_kpi_importance_aggregate": base_importance_sorted
    }

    out_json = RESULTS_DIR / "shap_importance.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(shap_results, f, indent=4)
    logger.info(f"Saved SHAP importance summary to {out_json}")

    # Print top features
    logger.info("Top 5 Base KPI Importances (Aggregated across time-lags):")
    for kpi, val in list(base_importance_sorted.items())[:5]:
        logger.info(f"  {kpi:20s}: {val:10.2f} kbps impact")

    # 5. Visualization 1: Beeswarm Summary Plot
    logger.info("Generating Beeswarm Summary Plot...")
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values.values, df_sample, max_display=15, show=False)
    plt.title("TreeSHAP Beeswarm Plot: Feature Impact on Downlink Bitrate", fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    fig_beeswarm = FIGURES_DIR / "04_shap_summary_beeswarm.png"
    plt.savefig(fig_beeswarm, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved {fig_beeswarm}")

    # 6. Visualization 2: Aggregated Base Feature Importance Bar Plot
    logger.info("Generating Base Feature Importance Bar Plot...")
    fig, ax = plt.subplots(figsize=(10, 6))
    kpis = list(base_importance_sorted.keys())
    scores = list(base_importance_sorted.values())
    sns.barplot(x=scores, y=kpis, palette="viridis", ax=ax)
    ax.set_title("Aggregated SHAP Feature Importance across Radio Metrics", fontsize=14, fontweight="bold")
    ax.set_xlabel("Cumulative Mean |SHAP value| (kbps)", fontsize=12)
    ax.set_ylabel("Radio KPI", fontsize=12)
    plt.tight_layout()
    fig_bar = FIGURES_DIR / "05_shap_feature_importance.png"
    plt.savefig(fig_bar, dpi=300)
    plt.close()
    logger.info(f"Saved {fig_bar}")

    # 7. Visualization 3: Feature Dependence Plots (e.g. CQI and SNR)
    logger.info("Generating Feature Dependence Plots...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    top_feature_1 = importance_df.iloc[0]["feature"]
    top_feature_2 = importance_df.iloc[1]["feature"]

    idx1 = list(df_sample.columns).index(top_feature_1)
    idx2 = list(df_sample.columns).index(top_feature_2)

    # Dependence 1
    axes[0].scatter(df_sample[top_feature_1], shap_values.values[:, idx1], c=df_sample[top_feature_2], cmap="coolwarm", alpha=0.7)
    axes[0].set_title(f"SHAP Dependence: {top_feature_1} (colored by {top_feature_2})", fontsize=12, fontweight="bold")
    axes[0].set_xlabel(f"{top_feature_1} (scaled)")
    axes[0].set_ylabel("SHAP value (impact on DL bitrate)")
    axes[0].grid(True, linestyle="--", alpha=0.6)

    # Dependence 2
    axes[1].scatter(df_sample[top_feature_2], shap_values.values[:, idx2], c=df_sample[top_feature_1], cmap="plasma", alpha=0.7)
    axes[1].set_title(f"SHAP Dependence: {top_feature_2} (colored by {top_feature_1})", fontsize=12, fontweight="bold")
    axes[1].set_xlabel(f"{top_feature_2} (scaled)")
    axes[1].set_ylabel("SHAP value (impact on DL bitrate)")
    axes[1].grid(True, linestyle="--", alpha=0.6)

    plt.tight_layout()
    fig_dep = FIGURES_DIR / "06_shap_dependence_plots.png"
    plt.savefig(fig_dep, dpi=300)
    plt.close()
    logger.info(f"Saved {fig_dep}")

    # 8. Visualization 4: Local Waterfall Plots (High vs Low Throughput)
    logger.info("Generating Local Explanation Waterfall Plots...")
    high_idx = int(np.argmax(y_sample))
    low_idx = int(np.argmin(y_sample))

    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

    # High throughput instance
    plt.sca(axes[0])
    shap.plots.waterfall(shap_values[high_idx], max_display=10, show=False)
    axes[0].set_title(f"Local Explanation: High Throughput Event ({y_sample[high_idx]:.0f} kbps)", fontsize=12, fontweight="bold")

    # Low throughput instance
    plt.sca(axes[1])
    shap.plots.waterfall(shap_values[low_idx], max_display=10, show=False)
    axes[1].set_title(f"Local Explanation: Low Throughput / Degradation Event ({y_sample[low_idx]:.0f} kbps)", fontsize=12, fontweight="bold")

    plt.tight_layout()
    fig_waterfall = FIGURES_DIR / "07_shap_waterfall_local.png"
    plt.savefig(fig_waterfall, dpi=300, bbox_inches="tight")
    plt.close()
    logger.info(f"Saved {fig_waterfall}")

    logger.info("=== EXPLAINABILITY ANALYSIS COMPLETED SUCCESSFULLY ===")
    return shap_results


if __name__ == "__main__":
    run_explainability_analysis()
