"""
Feature Pruning and Edge Latency Benchmarking Module.
Gradually eliminates features according to SHAP importance and measures performance vs inference speed.
Requirement 7 of Topic 11.
"""

import os
import time
import json
import logging
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb

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
from src.models_ml import calculate_metrics

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run_feature_pruning_experiment() -> list[dict]:
    """
    Progressively drops features based on lowest SHAP importance:
    Full (100%), Drop 25%, Drop 50%, Drop 75%.
    Measures RMSE, MAE, R2, Training Time, and Inference Latency.
    """
    logger.info("=== STARTING SHAP-GUIDED FEATURE PRUNING EXPERIMENT ===")

    # 1. Load SHAP ranking
    shap_path = RESULTS_DIR / "shap_importance.json"
    if shap_path.exists():
        with open(shap_path, "r", encoding="utf-8") as f:
            shap_data = json.load(f)
            # base_kpi_importance_aggregate is ordered from highest to lowest
            ranked_kpis = list(shap_data["base_kpi_importance_aggregate"].keys())
    else:
        # Default order if shap not yet run
        ranked_kpis = ["UL_bitrate", "RSSI", "ServingCell_Distance", "Speed", "SNR", "RSRP", "RSRQ", "CQI"]

    logger.info(f"Feature ranking from most to least important: {ranked_kpis}")

    train_df = pd.read_csv(DATA_PROCESSED_DIR / "train_data.csv")
    test_df = pd.read_csv(DATA_PROCESSED_DIR / "test_data.csv")

    lookback = 10
    horizon = 1
    max_train_samples = 30000

    # Pruning Stages:
    # 100% (all 8 features)
    # 75%  (top 6 features)
    # 50%  (top 4 features)
    # 25%  (top 2 features)
    stages = [
        ("100% Features (8 KPIs)", ranked_kpis[:8]),
        ("75% Features (6 KPIs)", ranked_kpis[:6]),
        ("50% Features (4 KPIs)", ranked_kpis[:4]),
        ("25% Features (2 KPIs)", ranked_kpis[:2]),
    ]

    results = []

    for stage_name, kept_kpis in stages:
        logger.info(f"Evaluating stage: {stage_name} -> Features: {kept_kpis}")
        scaled_cols = [f"{col}_scaled" for col in kept_kpis]

        # Create windows
        X_train, y_train = create_sliding_windows(
            train_df, lookback=lookback, horizon=horizon, feature_cols=scaled_cols
        )
        X_test, y_test = create_sliding_windows(
            test_df, lookback=lookback, horizon=horizon, feature_cols=scaled_cols
        )

        # Subsample for consistent timing
        if len(X_train) > max_train_samples:
            indices = np.random.RandomState(RANDOM_SEED).choice(len(X_train), max_train_samples, replace=False)
            X_train_sub = X_train[indices]
            y_train_sub = y_train[indices]
        else:
            X_train_sub = X_train
            y_train_sub = y_train

        # Train model
        model = xgb.XGBRegressor(
            n_estimators=120,
            max_depth=6,
            learning_rate=0.08,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=RANDOM_SEED,
            n_jobs=-1
        )

        t0_train = time.time()
        model.fit(X_train_sub, y_train_sub)
        train_time = time.time() - t0_train

        # Benchmark inference speed (run 3 times for precision)
        t0_infer = time.time()
        y_pred = model.predict(X_test)
        infer_time = time.time() - t0_infer
        infer_time_ms = (infer_time / len(X_test)) * 1000.0

        metrics = calculate_metrics(y_test, np.clip(y_pred, 0.0, None))
        metrics["stage"] = stage_name
        metrics["num_kpis"] = len(kept_kpis)
        metrics["num_input_dims"] = int(X_train.shape[1])
        metrics["kept_kpis"] = kept_kpis
        metrics["train_time_sec"] = round(train_time, 2)
        metrics["infer_time_ms_per_sample"] = round(infer_time_ms, 5)

        logger.info(
            f"  [{stage_name}] RMSE: {metrics['rmse']:7.1f} kbps | MAE: {metrics['mae']:6.1f} kbps | "
            f"Train: {train_time:.2f}s | Infer: {infer_time_ms:.4f} ms/sample"
        )
        results.append(metrics)

    # Export results
    out_json = RESULTS_DIR / "feature_pruning_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    logger.info(f"Saved pruning results to {out_json}")

    # Generate Visualization
    plot_pruning_results(results)
    return results


def plot_pruning_results(results: list[dict]):
    """
    Plots Accuracy (RMSE), Training Time, and Inference Latency trade-offs as features are pruned.
    """
    logger.info("Generating Feature Pruning Visualizations...")
    df = pd.DataFrame(results)

    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    fig.suptitle("Impact of SHAP-Guided Feature Pruning on Accuracy and Edge Efficiency", fontsize=14, fontweight="bold")

    stages = df["stage"]

    # 1. Prediction RMSE
    axes[0].plot(stages, df["rmse"] / 1000.0, marker="o", color="#d62728", linewidth=2.5, markersize=8)
    axes[0].set_title("Forecast Error (RMSE in Mbps)", fontweight="bold")
    axes[0].set_ylabel("RMSE (Mbps)")
    axes[0].grid(True, linestyle="--", alpha=0.6)
    for i, v in enumerate(df["rmse"] / 1000.0):
        axes[0].text(i, v + 0.08, f"{v:.2f}M", ha="center", fontweight="bold")

    # 2. Training Time
    axes[1].bar(stages, df["train_time_sec"], color="#1f77b4", width=0.5, alpha=0.85)
    axes[1].set_title("Model Training Time (Seconds)", fontweight="bold")
    axes[1].set_ylabel("Time (seconds)")
    axes[1].grid(True, linestyle="--", alpha=0.6)
    for i, v in enumerate(df["train_time_sec"]):
        axes[1].text(i, v + 0.04, f"{v:.2f}s", ha="center", fontweight="bold")

    # 3. Inference Latency per Sample
    axes[2].plot(stages, df["infer_time_ms_per_sample"] * 1000.0, marker="s", color="#2ca02c", linewidth=2.5, markersize=8)
    axes[2].set_title("Inference Latency (Microseconds / sample)", fontweight="bold")
    axes[2].set_ylabel("Latency (μs / sample)")
    axes[2].grid(True, linestyle="--", alpha=0.6)
    for i, v in enumerate(df["infer_time_ms_per_sample"] * 1000.0):
        axes[2].text(i, v + 0.05, f"{v:.1f}μs", ha="center", fontweight="bold")

    for ax in axes:
        ax.tick_params(axis="x", rotation=15)

    plt.tight_layout()
    fig_path = FIGURES_DIR / "11_feature_pruning_accuracy_vs_latency.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()
    logger.info(f"Saved {fig_path}")


if __name__ == "__main__":
    run_feature_pruning_experiment()
