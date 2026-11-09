"""
Midterm (40% - 50% Progress) Execution Script for Intermediate Presentation Demo.
Runs ONLY the first half of the assignment requirements:
  - Requirement 2 (15%): Data Preprocessing, cleaning '-', merging 135 traces, train/test split, normalization
  - Requirement 3 (15%): XGBoost Regressor across Lookback Windows & Prediction Horizons (RMSE, MAE, MAPE)
  - Requirement 4 (10%): Explainable AI (SHAP) feature importance
  (Along with Requirement 1 [10% theoretical 5G explanation] = 40%-50% total progress)
"""

import sys
import logging
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import DATA_PROCESSED_DIR
from src.data_processing import run_data_pipeline
from src.models_ml import run_lookback_horizon_grid
from src.explainability import run_explainability_analysis
from scripts.generate_midterm_presentation import generate_midterm_deck

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("MidtermRunner")


def main():
    print("=" * 78)
    print("   ΕΝΔΙΑΜΕΣΗ ΠΑΡΟΥΣΙΑΣΗ (40% - 50% ΤΩΝ ΖΗΤΟΥΜΕΝΩΝ ΤΗΣ ΕΡΓΑΣΙΑΣ)")
    print("   Θέμα 11: Πρόβλεψη Downlink Bitrate σε 5G Δίκτυα")
    print("=" * 78)

    print("\n[ΒΗΜΑ 1/3 - Ζητούμενο 2 (15%)] Προεπεξεργασία & Ενοποίηση των 135 Traces...")
    run_data_pipeline()

    print("\n[ΒΗΜΑ 2/3 - Ζητούμενο 3 (15%)] Εκπαίδευση XGBoost (Lookback & Horizon Grid)...")
    train_df = pd.read_csv(DATA_PROCESSED_DIR / "train_data.csv")
    test_df = pd.read_csv(DATA_PROCESSED_DIR / "test_data.csv")
    run_lookback_horizon_grid(train_df, test_df)

    print("\n[ΒΗΜΑ 3/3 - Ζητούμενο 4 (10%)] Ερμηνευσιμότητα Μοντέλου με SHAP (XAI)...")
    run_explainability_analysis()

    print("\n[ΠΑΡΟΥΣΙΑΣΗ] Δημιουργία Διαφανειών Ενδιάμεσης Παρουσίασης (40-50%)...")
    ppt_path = generate_midterm_deck()

    print("\n" + "=" * 78)
    print("   ΟΛΟΚΛΗΡΩΘΗΚΕ Η ΕΚΤΕΛΕΣΗ ΤΟΥ 40%-50% (ΠΡΟΠΑΡΑΣΚΕΥΑΣΤΙΚΗ ΦΑΣΗ)!")
    print(f"   Διαφάνειες Ενδιάμεσης Παρουσίασης: {ppt_path}")
    print("=" * 78)


if __name__ == "__main__":
    main()
