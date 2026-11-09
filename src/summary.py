"""
Consolidates all experimental metrics into a unified summary JSON.
"""

import json
from pathlib import Path
from src.config import RESULTS_DIR, DATA_PROCESSED_DIR


def compile_summary_metrics():
    summary = {}

    # Metadata
    meta_path = DATA_PROCESSED_DIR / "metadata.json"
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            summary["dataset"] = json.load(f)

    # XGBoost Grid
    xgb_path = RESULTS_DIR / "xgboost_grid_results.json"
    if xgb_path.exists():
        with open(xgb_path, "r", encoding="utf-8") as f:
            summary["xgboost_grid"] = json.load(f)

    # SHAP
    shap_path = RESULTS_DIR / "shap_importance.json"
    if shap_path.exists():
        with open(shap_path, "r", encoding="utf-8") as f:
            summary["shap"] = json.load(f)

    # LSTM
    lstm_path = RESULTS_DIR / "lstm_results.json"
    if lstm_path.exists():
        with open(lstm_path, "r", encoding="utf-8") as f:
            summary["lstm"] = json.load(f)

    # Foundation Model
    ttm_path = RESULTS_DIR / "foundation_model_results.json"
    if ttm_path.exists():
        with open(ttm_path, "r", encoding="utf-8") as f:
            summary["foundation_model"] = json.load(f)

    # Feature Pruning
    prune_path = RESULTS_DIR / "feature_pruning_results.json"
    if prune_path.exists():
        with open(prune_path, "r", encoding="utf-8") as f:
            summary["feature_pruning"] = json.load(f)

    # 5G Proactive Management
    proactive_path = RESULTS_DIR / "proactive_management_results.json"
    if proactive_path.exists():
        with open(proactive_path, "r", encoding="utf-8") as f:
            summary["proactive_management"] = json.load(f)

    out_file = RESULTS_DIR / "metrics_summary.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
    print(f"Compiled summary saved to {out_file}")
    return summary


if __name__ == "__main__":
    compile_summary_metrics()
