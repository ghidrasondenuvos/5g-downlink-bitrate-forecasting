"""
Verification Test Suite.
Validates that all required files, datasets, trained models, metrics JSONs,
figures, academic reports (.md, .docx, .pdf), and presentation decks (.pptx) exist and are valid.
"""

import sys
import json
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import (
    BASE_DIR,
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    MODELS_DIR,
    RESULTS_DIR,
    FIGURES_DIR,
    DOCS_DIR,
    PRESENTATION_DIR
)


def verify_project_integrity() -> bool:
    print("=" * 75)
    print("      5G DOWNLINK FORECASTING PROJECT — VERIFICATION TEST SUITE       ")
    print("=" * 75)

    all_passed = True

    # 1. Check Raw Data
    raw_files = list(DATA_RAW_DIR.glob("*/*.csv"))
    print(f"\n[1] Raw Cellular Traces:")
    if len(raw_files) == 135:
        print(f"  ✓ Found all 135 raw traces across 5 mobility scenarios.")
    else:
        print(f"  ✗ Expected 135 traces, found {len(raw_files)}!")
        all_passed = False

    # 2. Check Processed Data
    print(f"\n[2] Processed Datasets:")
    processed_files = [
        DATA_PROCESSED_DIR / "combined_traces.csv",
        DATA_PROCESSED_DIR / "train_data.csv",
        DATA_PROCESSED_DIR / "test_data.csv",
        DATA_PROCESSED_DIR / "metadata.json",
        DATA_PROCESSED_DIR / "feature_scaler.joblib"
    ]
    for pf in processed_files:
        if pf.exists() and pf.stat().st_size > 0:
            print(f"  ✓ {pf.name} ({pf.stat().st_size:,} bytes)")
        else:
            print(f"  ✗ Missing or empty: {pf.name}")
            all_passed = False

    # 3. Check Trained Models
    print(f"\n[3] Model Checkpoints:")
    model_files = [
        MODELS_DIR / "xgboost_best.joblib",
        MODELS_DIR / "lstm_model.pt",
        MODELS_DIR / "foundation_ttm.pt"
    ]
    for mf in model_files:
        if mf.exists() and mf.stat().st_size > 0:
            print(f"  ✓ {mf.name} ({mf.stat().st_size:,} bytes)")
        else:
            print(f"  ✗ Missing or empty model: {mf.name}")
            all_passed = False

    # 4. Check Results JSONs
    print(f"\n[4] Experimental Metrics JSONs:")
    result_files = [
        RESULTS_DIR / "xgboost_grid_results.json",
        RESULTS_DIR / "shap_importance.json",
        RESULTS_DIR / "lstm_results.json",
        RESULTS_DIR / "foundation_model_results.json",
        RESULTS_DIR / "feature_pruning_results.json",
        RESULTS_DIR / "proactive_management_results.json",
        RESULTS_DIR / "metrics_summary.json"
    ]
    for rf in result_files:
        if rf.exists() and rf.stat().st_size > 0:
            try:
                with open(rf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print(f"  ✓ {rf.name} (Valid JSON, {len(data)} top-level keys/items)")
            except Exception as e:
                print(f"  ✗ Corrupted JSON {rf.name}: {e}")
                all_passed = False
        else:
            print(f"  ✗ Missing result file: {rf.name}")
            all_passed = False

    # 5. Check High-Resolution Figures
    print(f"\n[5] Publication-Quality Visualizations:")
    figures = [
        "01_eda_distributions.png",
        "02_eda_mobility_comparison.png",
        "03_xgboost_horizons_lookback.png",
        "04_shap_summary_beeswarm.png",
        "05_shap_feature_importance.png",
        "06_shap_dependence_plots.png",
        "07_shap_waterfall_local.png",
        "08_lstm_training_loss.png",
        "09_model_comparisons.png",
        "10_foundation_model_performance.png",
        "11_feature_pruning_accuracy_vs_latency.png",
        "12_proactive_5g_early_warning_tradeoff.png"
    ]
    for fig_name in figures:
        fig_path = FIGURES_DIR / fig_name
        if fig_path.exists() and fig_path.stat().st_size > 5000:
            print(f"  ✓ {fig_name} ({fig_path.stat().st_size:,} bytes)")
        else:
            print(f"  ✗ Missing or corrupted figure: {fig_name}")
            all_passed = False

    # 6. Check Academic Reports
    print(f"\n[6] Academic Technical Reports:")
    report_files = [
        DOCS_DIR / "Technical_Report_5G_Forecasting.md",
        DOCS_DIR / "Technical_Report_5G_Forecasting.docx",
        DOCS_DIR / "Technical_Report_5G_Forecasting.pdf"
    ]
    for rep in report_files:
        if rep.exists() and rep.stat().st_size > 10000:
            print(f"  ✓ {rep.name} ({rep.stat().st_size:,} bytes)")
        else:
            print(f"  ✗ Missing or incomplete report: {rep.name}")
            all_passed = False

    # 7. Check Presentation Deck
    print(f"\n[7] Presentation Deck:")
    pres_file = PRESENTATION_DIR / "Downlink_Bitrate_Forecasting_5G.pptx"
    if pres_file.exists() and pres_file.stat().st_size > 50000:
        print(f"  ✓ {pres_file.name} ({pres_file.stat().st_size:,} bytes)")
    else:
        print(f"  ✗ Missing or incomplete presentation: {pres_file.name}")
        all_passed = False

    # 8. Check Top-Level Runners
    print(f"\n[8] Top-Level Run Scripts:")
    runners = [
        BASE_DIR / "run.bat",
        BASE_DIR / "run.ps1",
        BASE_DIR / "README.md"
    ]
    for run_file in runners:
        if run_file.exists() and run_file.stat().st_size > 0:
            print(f"  ✓ {run_file.name}")
        else:
            print(f"  ✗ Missing runner: {run_file.name}")
            all_passed = False

    print("\n" + "=" * 75)
    if all_passed:
        print("    ★ ALL 8 VERIFICATION CATEGORIES PASSED WITH 100% SUCCESS! ★      ")
    else:
        print("    ⚠ SOME VERIFICATION CHECKS FAILED! REVIEW THE LOGS ABOVE.        ")
    print("=" * 75)
    return all_passed


if __name__ == "__main__":
    success = verify_project_integrity()
    sys.exit(0 if success else 1)
