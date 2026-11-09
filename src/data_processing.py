"""
Data Ingestion, Preprocessing, Cleaning, Normalization and Time-Series Windowing.
Requirement 2 of Topic 11.
"""

import os
import glob
import json
import logging
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, RobustScaler
import joblib

from src.config import (
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    FIGURES_DIR,
    RANDOM_SEED,
    MOBILITY_SCENARIOS,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    TARGET_COLUMN
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_raw_traces() -> pd.DataFrame:
    """
    Loads all CSV files from data/Dataset/<mobility_mode>/
    Annotates each trace with mobility_mode and a unique trace_id.
    """
    logger.info(f"Loading raw cellular traces from {DATA_RAW_DIR}...")
    trace_dfs = []
    trace_counter = 0

    for mode in MOBILITY_SCENARIOS:
        mode_dir = DATA_RAW_DIR / mode
        if not mode_dir.exists():
            logger.warning(f"Directory {mode_dir} not found!")
            continue

        csv_files = sorted(list(mode_dir.glob("*.csv")))
        logger.info(f"Scenario '{mode}': Found {len(csv_files)} trace files.")

        for file_path in csv_files:
            try:
                df = pd.read_csv(file_path)
                df["mobility_mode"] = mode
                df["trace_id"] = f"{mode}_{trace_counter}_{file_path.stem}"
                df["source_file"] = file_path.name
                trace_dfs.append(df)
                trace_counter += 1
            except Exception as e:
                logger.error(f"Error reading {file_path}: {e}")

    if not trace_dfs:
        raise RuntimeError("No trace files were loaded! Check data directory.")

    combined_df = pd.concat(trace_dfs, ignore_index=True)
    logger.info(f"Total raw records loaded: {len(combined_df):,} across {trace_counter} traces.")
    return combined_df


def clean_and_impute_traces(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans '-' string placeholders, parses numeric fields, applies domain-aware imputation
    (forward fill per trace sequence, then global median).
    """
    logger.info("Cleaning data and converting datatypes...")
    df_clean = df.copy()

    # Columns that should be numeric
    all_numeric_cols = NUMERIC_FEATURES + [TARGET_COLUMN, "Longitude", "Latitude", "CellID"]

    for col in all_numeric_cols:
        if col in df_clean.columns:
            # Replace '-' with NaN and coerce to float
            df_clean[col] = pd.to_numeric(
                df_clean[col].astype(str).str.strip().replace(["-", "nan", "None", ""], np.nan),
                errors="coerce"
            )

    # Impute missing values within each trace session via ffill and bfill
    logger.info("Applying session-aware forward-fill and backward-fill...")
    numeric_to_impute = [col for col in all_numeric_cols if col in df_clean.columns]
    
    df_clean[numeric_to_impute] = df_clean.groupby("trace_id")[numeric_to_impute].transform(
        lambda group: group.ffill().bfill()
    )

    # Global median fill for any remaining NaNs
    for col in numeric_to_impute:
        if df_clean[col].isna().sum() > 0:
            median_val = df_clean[col].median()
            df_clean[col] = df_clean[col].fillna(median_val if not np.isnan(median_val) else 0.0)

    # Domain range sanity enforcement
    df_clean["DL_bitrate"] = df_clean["DL_bitrate"].clip(lower=0.0)
    df_clean["UL_bitrate"] = df_clean["UL_bitrate"].clip(lower=0.0)
    df_clean["Speed"] = df_clean["Speed"].clip(lower=0.0, upper=250.0)
    if "CQI" in df_clean.columns:
        df_clean["CQI"] = df_clean["CQI"].clip(lower=0.0, upper=15.0)

    # Filter out empty or zero-throughput inactive records if needed
    logger.info(f"Cleaning complete. Non-null shape: {df_clean.shape}")
    return df_clean


def perform_train_test_split(df: pd.DataFrame, test_ratio: float = 0.2) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Performs a session-aware trace split to avoid time-series data leakage.
    Splits complete traces per mobility scenario into 80% train and 20% test.
    """
    logger.info(f"Splitting traces into train ({1-test_ratio:.0%}) and test ({test_ratio:.0%})...")
    np.random.seed(RANDOM_SEED)

    train_traces = []
    test_traces = []

    for mode in MOBILITY_SCENARIOS:
        mode_traces = df[df["mobility_mode"] == mode]["trace_id"].unique()
        np.random.shuffle(mode_traces)
        
        split_idx = int(len(mode_traces) * (1 - test_ratio))
        train_ids = mode_traces[:split_idx]
        test_ids = mode_traces[split_idx:]
        
        train_traces.extend(train_ids)
        test_traces.extend(test_ids)
        logger.info(f"  Mode '{mode}': {len(train_ids)} train traces, {len(test_ids)} test traces.")

    train_df = df[df["trace_id"].isin(train_traces)].copy().reset_index(drop=True)
    test_df = df[df["trace_id"].isin(test_traces)].copy().reset_index(drop=True)

    logger.info(f"Split results: Train = {len(train_df):,} samples ({len(train_traces)} traces), "
                f"Test = {len(test_df):,} samples ({len(test_traces)} traces).")
    return train_df, test_df


def normalize_features(train_df: pd.DataFrame, test_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    """
    Fits StandardScaler on numerical features in the train set ONLY,
    and transforms both train and test sets to prevent data leakage.
    """
    logger.info("Normalizing continuous features with StandardScaler...")
    scaler = StandardScaler()
    
    train_scaled = train_df.copy()
    test_scaled = test_df.copy()

    scaler.fit(train_df[NUMERIC_FEATURES])
    
    scaled_feature_names = [f"{col}_scaled" for col in NUMERIC_FEATURES]
    
    train_scaled[scaled_feature_names] = scaler.transform(train_df[NUMERIC_FEATURES])
    test_scaled[scaled_feature_names] = scaler.transform(test_df[NUMERIC_FEATURES])

    # Save scaler for deployment and inference
    scaler_path = DATA_PROCESSED_DIR / "feature_scaler.joblib"
    joblib.dump(scaler, scaler_path)
    logger.info(f"Scaler saved to {scaler_path}")

    return train_scaled, test_scaled, scaler


def create_sliding_windows(
    df: pd.DataFrame,
    lookback: int = 10,
    horizon: int = 1,
    feature_cols: list[str] = None,
    target_col: str = TARGET_COLUMN,
    flatten_for_tabular: bool = True
) -> tuple[np.ndarray, np.ndarray]:
    """
    Generates time-series sliding windows per continuous trace_id session:
    Input: [x_{t-lookback+1}, ..., x_t]
    Target: y_{t+horizon}
    """
    if feature_cols is None:
        feature_cols = NUMERIC_FEATURES

    X_list = []
    y_list = []

    # Group by trace to ensure we never cross trace boundaries
    for _, trace_group in df.groupby("trace_id"):
        features = trace_group[feature_cols].values
        targets = trace_group[target_col].values
        n_samples = len(features)

        if n_samples < lookback + horizon:
            continue

        for i in range(n_samples - lookback - horizon + 1):
            window = features[i : i + lookback]
            target = targets[i + lookback + horizon - 1]

            if flatten_for_tabular:
                X_list.append(window.flatten())
            else:
                X_list.append(window)
            y_list.append(target)

    if not X_list:
        raise ValueError(f"No windows could be generated for lookback={lookback}, horizon={horizon}!")

    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.float32)
    return X, y


def generate_eda_figures(df: pd.DataFrame):
    """
    Generates publication-quality exploratory data analysis visualizations:
    1. Feature distributions & correlations.
    2. Mobility scenario throughput comparisons.
    """
    logger.info("Generating EDA figures...")
    sns.set_theme(style="whitegrid", font="sans-serif")

    # Figure 1: Throughput and Signal Quality Distributions
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle("5G Cellular Traces: KPI Distributions (UCC Dataset)", fontsize=16, fontweight="bold")

    kpis = ["DL_bitrate", "RSRP", "RSRQ", "SNR", "CQI", "Speed"]
    titles = [
        "Downlink Bitrate (kbps)",
        "RSRP (dBm)",
        "RSRQ (dB)",
        "SNR (dB)",
        "Channel Quality Indicator (CQI)",
        "Velocity / Speed (km/h)"
    ]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

    for idx, (col, title, color) in enumerate(zip(kpis, titles, colors)):
        ax = axes[idx // 3, idx % 3]
        data = df[col].dropna()
        if col == "DL_bitrate":
            data = data[data > 0]  # focus on active transmission
        sns.histplot(data, bins=40, kde=True, ax=ax, color=color, alpha=0.6)
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Value")
        ax.set_ylabel("Count")

    plt.tight_layout()
    fig1_path = FIGURES_DIR / "01_eda_distributions.png"
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    logger.info(f"Saved {fig1_path}")

    # Figure 2: Mobility Scenario Throughput Comparison & Correlation Heatmap
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))

    # Boxplot of Throughput by Mobility Mode
    sns.boxplot(
        data=df[df["DL_bitrate"] > 0],
        x="mobility_mode",
        y="DL_bitrate",
        palette="Set2",
        ax=axes[0],
        showfliers=False
    )
    axes[0].set_title("Downlink Bitrate (kbps) across Mobility Scenarios", fontsize=14, fontweight="bold")
    axes[0].set_xlabel("Mobility Mode", fontsize=12)
    axes[0].set_ylabel("DL Bitrate (kbps)", fontsize=12)

    # Correlation Heatmap
    corr_cols = ["DL_bitrate", "UL_bitrate", "RSRP", "RSRQ", "SNR", "CQI", "RSSI", "Speed"]
    corr_matrix = df[corr_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="vlag", center=0, ax=axes[1], cbar_kws={"label": "Correlation"})
    axes[1].set_title("Radio KPI Cross-Correlation Matrix", fontsize=14, fontweight="bold")

    plt.tight_layout()
    fig2_path = FIGURES_DIR / "02_eda_mobility_comparison.png"
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    logger.info(f"Saved {fig2_path}")


def run_data_pipeline() -> dict:
    """
    Executes full data ingestion, cleaning, split, normalization and metadata export.
    """
    logger.info("=== STARTING DATA PREPROCESSING PIPELINE ===")
    
    # 1. Load raw
    raw_df = load_raw_traces()

    # 2. Clean & Impute
    cleaned_df = clean_and_impute_traces(raw_df)

    # 3. Save combined cleaned dataset
    combined_path = DATA_PROCESSED_DIR / "combined_traces.csv"
    logger.info(f"Saving cleaned dataset to {combined_path}...")
    cleaned_df.to_csv(combined_path, index=False)

    # 4. Generate EDA Visualizations
    generate_eda_figures(cleaned_df)

    # 5. Train/Test Split
    train_df, test_df = perform_train_test_split(cleaned_df, test_ratio=0.2)

    # 6. Normalize Features
    train_df, test_df, _ = normalize_features(train_df, test_df)

    # 7. Save train and test sets
    train_path = DATA_PROCESSED_DIR / "train_data.csv"
    test_path = DATA_PROCESSED_DIR / "test_data.csv"
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    logger.info(f"Saved train set ({len(train_df):,} rows) to {train_path}")
    logger.info(f"Saved test set ({len(test_df):,} rows) to {test_path}")

    # 8. Export Metadata & Summary Stats
    summary = {
        "total_traces": int(cleaned_df["trace_id"].nunique()),
        "total_samples": int(len(cleaned_df)),
        "train_samples": int(len(train_df)),
        "test_samples": int(len(test_df)),
        "train_traces": int(train_df["trace_id"].nunique()),
        "test_traces": int(test_df["trace_id"].nunique()),
        "mobility_counts": cleaned_df["mobility_mode"].value_counts().to_dict(),
        "throughput_stats_kbps": {
            "mean": float(cleaned_df["DL_bitrate"].mean()),
            "std": float(cleaned_df["DL_bitrate"].std()),
            "min": float(cleaned_df["DL_bitrate"].min()),
            "median": float(cleaned_df["DL_bitrate"].median()),
            "max": float(cleaned_df["DL_bitrate"].max()),
            "q25": float(cleaned_df["DL_bitrate"].quantile(0.25)),
            "q75": float(cleaned_df["DL_bitrate"].quantile(0.75))
        },
        "numeric_features": NUMERIC_FEATURES,
        "target_column": TARGET_COLUMN
    }

    summary_path = DATA_PROCESSED_DIR / "metadata.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
    logger.info(f"Metadata exported to {summary_path}")
    logger.info("=== DATA PREPROCESSING COMPLETE ===")
    return summary


if __name__ == "__main__":
    run_data_pipeline()
