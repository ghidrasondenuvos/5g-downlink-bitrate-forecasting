"""
Configuration module for 5G Downlink Bitrate Forecasting Project.
Course: Next Generation Network Architectures, Technologies and Applications (Winter Semester 2026-2027)
Topic 11: Prediction of Downlink Bitrate (Throughput) Based on Quality Metrics
Supervisor: Panagiotis Marantis (pmaradis@isi.gr)
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "Dataset"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
RESULTS_DIR = BASE_DIR / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
DOCS_DIR = BASE_DIR / "docs"
PRESENTATION_DIR = BASE_DIR / "presentation"

# Ensure directories exist
for path in [DATA_PROCESSED_DIR, MODELS_DIR, RESULTS_DIR, FIGURES_DIR, DOCS_DIR, PRESENTATION_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Random Seed for Reproducibility
RANDOM_SEED = 42

# Mobility Scenarios
MOBILITY_SCENARIOS = ["static", "pedestrian", "bus", "car", "train"]

# Core Features for Modeling
NUMERIC_FEATURES = [
    "RSRP",                 # Reference Signal Received Power (dBm)
    "RSRQ",                 # Reference Signal Received Quality (dB)
    "SNR",                  # Signal-to-Noise Ratio (dB)
    "CQI",                  # Channel Quality Indicator (1-15)
    "RSSI",                 # Received Signal Strength Indicator (dBm)
    "Speed",                # Device Velocity (km/h)
    "UL_bitrate",           # Uplink Bitrate (kbps)
    "ServingCell_Distance"  # Distance to Serving Base Station (m)
]

CATEGORICAL_FEATURES = [
    "mobility_mode",        # static, pedestrian, bus, car, train
    "Operatorname"          # Network operator identifier
]

TARGET_COLUMN = "DL_bitrate"  # Downlink Bitrate (kbps)

# Evaluation Lookback Windows and Prediction Horizons
DEFAULT_LOOKBACK_WINDOWS = [5, 10, 20, 30, 64]   # Samples (seconds)
DEFAULT_PREDICTION_HORIZONS = [1, 3, 5, 10, 15]   # Steps ahead (seconds)

# Default Model Parameters
XGBOOST_PARAMS = {
    "n_estimators": 200,
    "max_depth": 6,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": RANDOM_SEED,
    "n_jobs": -1
}

LSTM_PARAMS = {
    "lookback": 64,
    "hidden_dim": 64,
    "num_layers": 2,
    "dropout": 0.2,
    "batch_size": 128,
    "learning_rate": 0.001,
    "epochs": 15
}

FOUNDATION_MODEL_PARAMS = {
    "context_len": 64,
    "pred_len": 1,
    "d_model": 64,
    "num_patches": 8,
    "patch_len": 8,
    "epochs": 5,
    "batch_size": 128,
    "learning_rate": 0.0005
}

# 5G Proactive Network Management SLA Parameters
QOS_DEGRADATION_THRESHOLD_KBPS = 5000.0   # 5 Mbps QoS threshold (critical for 4K video / low latency)
