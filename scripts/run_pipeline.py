"""
End-to-End Execution CLI Pipeline for 5G Downlink Bitrate Forecasting Project.
Course: Next Generation Network Architectures, Technologies and Applications (Topic 11)
Supervisor: Panagiotis Marantis (pmaradis@isi.gr)
"""

import sys
import argparse
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("PipelineRunner")


def main():
    parser = argparse.ArgumentParser(
        description="5G Downlink Bitrate Forecasting & Proactive Management Pipeline"
    )
    parser.add_argument("--all", action="store_true", help="Execute complete pipeline end-to-end")
    parser.add_argument("--preprocess", action="store_true", help="Run data cleaning, split & normalization")
    parser.add_argument("--ml", action="store_true", help="Run XGBoost Regressor grid search (lookbacks & horizons)")
    parser.add_argument("--shap", action="store_true", help="Run TreeSHAP Explainable AI analysis")
    parser.add_argument("--dl", action="store_true", help="Run PyTorch LSTM Deep Learning forecaster")
    parser.add_argument("--foundation", action="store_true", help="Run IBM Granite TTM Zero-Shot & Fine-Tuning")
    parser.add_argument("--prune", action="store_true", help="Run SHAP-guided feature pruning & latency analysis")
    parser.add_argument("--proactive", action="store_true", help="Run 5G Proactive QoS Early Warning simulation")
    parser.add_argument("--report", action="store_true", help="Generate Academic Reports (.md, .docx, .pdf)")
    parser.add_argument("--presentation", action="store_true", help="Generate Presentation Deck (.pptx)")

    args = parser.parse_args()

    # Default to --all if no specific flag provided
    run_all = args.all or not any(vars(args).values())

    logger.info("======================================================================")
    logger.info("      5G DOWNLINK BITRATE FORECASTING & PROACTIVE MANAGEMENT          ")
    logger.info("======================================================================")

    if run_all or args.preprocess:
        logger.info("\n>>> STAGE 1: Data Preprocessing & EDA Visualizations")
        from src.data_processing import run_data_pipeline
        run_data_pipeline()

    if run_all or args.ml:
        logger.info("\n>>> STAGE 2: Machine Learning (XGBoost Regressor Grid)")
        import pandas as pd
        from src.config import DATA_PROCESSED_DIR
        from src.models_ml import run_lookback_horizon_grid
        train_df = pd.read_csv(DATA_PROCESSED_DIR / "train_data.csv")
        test_df = pd.read_csv(DATA_PROCESSED_DIR / "test_data.csv")
        run_lookback_horizon_grid(train_df, test_df)

    if run_all or args.shap:
        logger.info("\n>>> STAGE 3: Explainable AI (TreeSHAP Interpretability)")
        from src.explainability import run_explainability_analysis
        run_explainability_analysis()

    if run_all or args.dl:
        logger.info("\n>>> STAGE 4: Deep Learning Time-Series Forecaster (PyTorch LSTM)")
        from src.models_dl import run_deep_learning_pipeline
        run_deep_learning_pipeline()

    if run_all or args.foundation:
        logger.info("\n>>> STAGE 5: Foundation Models (IBM Granite TTM Zero-Shot & Fine-Tuning)")
        from src.models_foundation import run_foundation_model_pipeline
        run_foundation_model_pipeline()

    if run_all or args.prune:
        logger.info("\n>>> STAGE 6: SHAP-Guided Feature Pruning & Edge Efficiency")
        from src.feature_pruning import run_feature_pruning_experiment
        run_feature_pruning_experiment()

    if run_all or args.proactive:
        logger.info("\n>>> STAGE 7: 5G Proactive Network Management (QoS Degradation Early Warning)")
        import pandas as pd
        from src.config import DATA_PROCESSED_DIR
        from src.proactive_5g import analyze_proactive_degradation_detection
        train_df = pd.read_csv(DATA_PROCESSED_DIR / "train_data.csv")
        test_df = pd.read_csv(DATA_PROCESSED_DIR / "test_data.csv")
        analyze_proactive_degradation_detection(train_df, test_df)

    if run_all:
        logger.info("\n>>> STAGE 8: Metrics Compilation")
        from src.summary import compile_summary_metrics
        compile_summary_metrics()

    if run_all or args.report:
        logger.info("\n>>> STAGE 9: Academic Report Generation (.md, .docx, .pdf)")
        from scripts.generate_report import run_all_report_generation
        run_all_report_generation()

    if run_all or args.presentation:
        logger.info("\n>>> STAGE 10: Executive Presentation Generation (.pptx)")
        from scripts.generate_presentation import generate_presentation_deck
        generate_presentation_deck()

    logger.info("======================================================================")
    logger.info("   ALL PIPELINE STAGES COMPLETED SUCCESSFULLY WITH EXIT CODE 0!       ")
    logger.info("======================================================================")


if __name__ == "__main__":
    main()
