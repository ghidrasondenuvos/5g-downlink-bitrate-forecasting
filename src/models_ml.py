"""
Machine Learning Forecasting Module (XGBoost Regressor).
Evaluates multiple Lookback Windows and Prediction Horizons.
Requirement 3 of Topic 11.
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
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import joblib

from src.config import (
    DATA_PROCESSED_DIR,
    MODELS_DIR,
    RESULTS_DIR,
    FIGURES_DIR,
    RANDOM_SEED,
    NUMERIC_FEATURES,
    TARGET_COLUMN,
    DEFAULT_LOOKBACK_WINDOWS,
    DEFAULT_PREDICTION_HORIZONS,
    XGBOOST_PARAMS
)
from src.data_processing import create_sliding_windows

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Computes RMSE, MAE, MAPE (safe division), and R2 metrics.
    """
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    
    # Safe MAPE: epsilon floor of 1.0 kbps for near-zero values
    safe_y_true = np.where(y_true < 1.0, 1.0, y_true)
    mape = float(np.mean(np.abs((y_true - y_pred) / safe_y_true)) * 100.0)
    
    r2 = float(r2_score(y_true, y_pred))

    return {
        "rmse": round(rmse, 2),
        "mae": round(mae, 2),
        "mape": round(mape, 2),
        "r2": round(r2, 4)
    }


def train_and_evaluate_xgboost(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    lookback: int = 10,
    horizon: int = 1,
    feature_cols: list[str] = None,
    save_model: bool = False
) -> tuple[xgb.XGBRegressor, dict, np.ndarray, np.ndarray]:
    """
    Trains XGBoost on sliding windows for given (lookback, horizon) pair.
    """
    if feature_cols is None:
        feature_cols = [f"{col}_scaled" for col in NUMERIC_FEATURES]

    # Create windows
    t0_win = time.time()
    X_train, y_train = create_sliding_windows(train_df, lookback=lookback, horizon=horizon, feature_cols=feature_cols)
    X_test, y_test = create_sliding_windows(test_df, lookback=lookback, horizon=horizon, feature_cols=feature_cols)
    win_time = time.time() - t0_win

    # Downsample train set if very large for rapid grid search while preserving statistical power
    max_train_samples = 40000
    if len(X_train) > max_train_samples:
        indices = np.random.RandomState(RANDOM_SEED).choice(len(X_train), max_train_samples, replace=False)
        X_train_sub = X_train[indices]
        y_train_sub = y_train[indices]
    else:
        X_train_sub = X_train
        y_train_sub = y_train

    # Train model
    model = xgb.XGBRegressor(
        n_estimators=150,
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

    # Predict & benchmark inference time
    t0_infer = time.time()
    y_pred = model.predict(X_test)
    y_pred = np.clip(y_pred, 0.0, None)  # Throughput cannot be negative
    infer_time = time.time() - t0_infer
    infer_time_ms_per_sample = (infer_time / len(X_test)) * 1000.0

    metrics = calculate_metrics(y_test, y_pred)
    metrics["lookback"] = lookback
    metrics["horizon"] = horizon
    metrics["train_time_sec"] = round(train_time, 2)
    metrics["infer_time_ms_per_sample"] = round(infer_time_ms_per_sample, 4)
    metrics["num_features_in"] = int(X_train.shape[1])

    logger.info(
        f"[L={lookback:2d}, H={horizon:2d}] RMSE: {metrics['rmse']:8.1f} kbps | "
        f"MAE: {metrics['mae']:7.1f} kbps | MAPE: {metrics['mape']:5.1f}% | R2: {metrics['r2']:.3f} | "
        f"Train: {train_time:.1f}s | Infer: {infer_time_ms_per_sample:.3f}ms/sample"
    )

    if save_model:
        model_path = MODELS_DIR / f"xgboost_L{lookback}_H{horizon}.joblib"
        joblib.dump(model, model_path)
        logger.info(f"Saved model to {model_path}")

    return model, metrics, y_test, y_pred


def run_lookback_horizon_grid(train_df: pd.DataFrame, test_df: pd.DataFrame) -> list[dict]:
    """
    Sweeps over combinations of lookback windows and prediction horizons.
    """
    logger.info("=== EVALUATING XGBOOST ACROSS LOOKBACKS & PREDICTION HORIZONS ===")
    lookbacks = [5, 10, 20, 30]
    horizons = [1, 3, 5, 10]
    results = []

    best_rmse = float("inf")
    best_model = None
    best_test_data = None

    for L in lookbacks:
        for H in horizons:
            is_best_candidate = (L == 10 and H == 1)
            model, metrics, y_test, y_pred = train_and_evaluate_xgboost(
                train_df, test_df, lookback=L, horizon=H, save_model=is_best_candidate
            )
            results.append(metrics)

            if is_best_candidate:
                best_model = model
                best_test_data = (y_test, y_pred)
                # Save primary model for explainability and downstream tasks
                joblib.dump(best_model, MODELS_DIR / "xgboost_best.joblib")

    # Export grid metrics
    grid_path = RESULTS_DIR / "xgboost_grid_results.json"
    with open(grid_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    logger.info(f"Grid results exported to {grid_path}")

    # Generate multi-panel comparison figure
    generate_grid_figures(results, best_test_data)
    return results


def generate_grid_figures(results: list[dict], best_test_data: tuple[np.ndarray, np.ndarray]):
    """
    Plots the sensitivity of RMSE, MAE, and MAPE across horizons and lookbacks,
    plus actual vs predicted throughput time-series trajectory.
    """
    df_res = pd.DataFrame(results)
    sns.set_theme(style="whitegrid")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("XGBoost Regressor: Lookback Window & Prediction Horizon Sensitivity", fontsize=16, fontweight="bold")

    # 1. RMSE vs Horizon
    sns.lineplot(
        data=df_res,
        x="horizon",
        y="rmse",
        hue="lookback",
        marker="o",
        palette="tab10",
        linewidth=2.5,
        ax=axes[0, 0]
    )
    axes[0, 0].set_title("RMSE (Root Mean Squared Error) vs Prediction Horizon", fontsize=13, fontweight="bold")
    axes[0, 0].set_xlabel("Prediction Horizon H (steps / seconds ahead)")
    axes[0, 0].set_ylabel("RMSE (kbps)")

    # 2. MAE vs Horizon
    sns.lineplot(
        data=df_res,
        x="horizon",
        y="mae",
        hue="lookback",
        marker="s",
        palette="tab10",
        linewidth=2.5,
        ax=axes[0, 1]
    )
    axes[0, 1].set_title("MAE (Mean Absolute Error) vs Prediction Horizon", fontsize=13, fontweight="bold")
    axes[0, 1].set_xlabel("Prediction Horizon H (steps / seconds ahead)")
    axes[0, 1].set_ylabel("MAE (kbps)")

    # 3. MAPE vs Horizon
    sns.lineplot(
        data=df_res,
        x="horizon",
        y="mape",
        hue="lookback",
        marker="^",
        palette="tab10",
        linewidth=2.5,
        ax=axes[1, 0]
    )
    axes[1, 0].set_title("MAPE (%) vs Prediction Horizon", fontsize=13, fontweight="bold")
    axes[1, 0].set_xlabel("Prediction Horizon H (steps / seconds ahead)")
    axes[1, 0].set_ylabel("MAPE (%)")

    # 4. Actual vs Predicted Time-Series Window
    if best_test_data is not None:
        y_test, y_pred = best_test_data
        sample_range = slice(100, 300)
        time_steps = np.arange(200)

        axes[1, 1].plot(time_steps, y_test[sample_range] / 1000.0, label="Actual Throughput", color="#1f77b4", linewidth=2.0)
        axes[1, 1].plot(time_steps, y_pred[sample_range] / 1000.0, label="XGBoost Predicted", color="#d62728", linestyle="--", linewidth=2.0)
        axes[1, 1].fill_between(time_steps, y_test[sample_range] / 1000.0, y_pred[sample_range] / 1000.0, color="#d62728", alpha=0.15)
        axes[1, 1].set_title("Trajectory Tracking: Actual vs Predicted (Test Trace Segment)", fontsize=13, fontweight="bold")
        axes[1, 1].set_xlabel("Time (seconds)")
        axes[1, 1].set_ylabel("Throughput (Mbps)")
        axes[1, 1].legend(loc="upper right")

    plt.tight_layout()
    fig_path = FIGURES_DIR / "03_xgboost_horizons_lookback.png"
    plt.savefig(fig_path, dpi=300)
    plt.close()
    logger.info(f"Saved {fig_path}")


if __name__ == "__main__":
    train_df = pd.read_csv(DATA_PROCESSED_DIR / "train_data.csv")
    test_df = pd.read_csv(DATA_PROCESSED_DIR / "test_data.csv")
    run_lookback_horizon_grid(train_df, test_df)
