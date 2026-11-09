# 5G Downlink Bitrate (Throughput) Forecasting & Proactive QoS Management
### Αρχιτεκτονικές Δικτύων Επόμενης Γενιάς, Τεχνολογίες και Εφαρμογές (Χειμερινό Εξάμηνο 2026-2027)
**Θέμα Project 11: Πρόβλεψη Downlink Bitrate (Throughput) Με Βάση Μετρικές Ποιότητας**  
**Επιβλέπων:** Παναγιώτης Μαράντης (`pmaradis@isi.gr`) — Ερευνητικό Κέντρο ISI / Πανεπιστήμιο Πατρών  
**GitHub Repository:** [https://github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting](https://github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting)  

---

## 📌 Περίληψη Έργου (Executive Summary)

Το παρόν project υλοποιεί ένα ολοκληρωμένο, παραγωγικό σύστημα πρόβλεψης του ρυθμού μετάδοσης δεδομένων λήψης (**Downlink Bitrate / Throughput**) σε πραγματικό χρόνο για σύγχρονα κυψελωτά δίκτυα **5G NR / 6G**, με στόχο την **προληπτική διαχείριση πόρων (Proactive QoS/QoE Management)** και την ένταξη στις αρχιτεκτονικές **3GPP NWDAF (Network Data Analytics Function)** και **O-RAN Near-RT RIC (RAN Intelligent Controller)**.

Χρησιμοποιήθηκαν **135 πραγματικές κυψελωτές καταγραφές (174.523 δείγματα)** από το επίσημο dataset του University College Cork (UCC MISL) για 5 σενάρια κινητικότητας (`car`, `train`, `pedestrian`, `static`, `bus`).

---

## 🚀 Έτοιμες Εντολές Εκτέλεσης (Ready-to-Run Commands)

### 1. Πλήρης Αυτοματοποιημένη Εκτέλεση (One-Click)
Μπορείτε να εκτελέσετε ολόκληρο το pipeline από την αρχή μέχρι το τέλος με μία εντολή:

#### Μέσω Windows Command Prompt (.bat):
```cmd
run.bat
```

#### Μέσω PowerShell (.ps1):
```powershell
.\run.ps1
```

#### Μέσω Python Pipeline CLI:
```bash
python scripts/run_pipeline.py --all
```

---

### 2. Τμηματική Εκτέλεση Ανά Ζητούμενο (Modular Execution)

| Ζητούμενο | Περιγραφή | Εντολή PowerShell / Bat | Εντολή Python CLI |
| :--- | :--- | :--- | :--- |
| **Προεπεξεργασία** | Καθαρισμός, Session Split & Scaling | `.\run.ps1 -Stage preprocess` | `python scripts/run_pipeline.py --preprocess` |
| **XGBoost Grid** | Πλέγμα Lookbacks & Horizons | `.\run.ps1 -Stage ml` | `python scripts/run_pipeline.py --ml` |
| **TreeSHAP XAI** | Επεξηγησιμότητα & Beeswarm Plots | `.\run.ps1 -Stage shap` | `python scripts/run_pipeline.py --shap` |
| **PyTorch LSTM** | Deep Learning Χρονοσειρών (Lookback 64) | `.\run.ps1 -Stage dl` | `python scripts/run_pipeline.py --dl` |
| **Foundation Model** | IBM Granite TTM (Zero-Shot & Fine-Tuning) | `.\run.ps1 -Stage foundation` | `python scripts/run_pipeline.py --foundation` |
| **Feature Pruning** | Σταδιακή Αφαίρεση Μεταβλητών & Latency | `.\run.ps1 -Stage prune` | `python scripts/run_pipeline.py --prune` |
| **5G Proactive** | Προληπτική Ανίχνευση Υποβάθμισης QoS | `.\run.ps1 -Stage proactive` | `python scripts/run_pipeline.py --proactive` |
| **Αναφορές** | Παραγωγή Αναφοράς (.pdf, .docx, .md) | `.\run.ps1 -Stage report` | `python scripts/run_pipeline.py --report` |
| **Παρουσίαση** | Παραγωγή Slide Deck (.pptx) | `.\run.ps1 -Stage presentation` | `python scripts/run_pipeline.py --presentation` |
| **Έλεγχος / Verify** | Πλήρης Έλεγχος Ακεραιότητας Αρχείων | `.\run.ps1 -Stage verify` | `python scripts/verify_all.py` |

---

## 📊 Σύνοψη Πειραματικών Αποτελεσμάτων

### 1. Σύγκριση Μοντέλων Πρόβλεψης Throughput
| Μοντέλο | Αρχιτεκτονική / Ρύθμιση | RMSE (kbps) | MAE (kbps) | $R^2$ Score | Χρόνος Train | Inference Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **XGBoost Regressor** | 100 Trees, Lookback 10s, Horizon 1s | **6.344,8** | **3.275,5** | **0.825** | **1,3s** | **0,001 ms/sample** |
| **IBM Granite TTM (FT)** | Patch-based MLP-Mixer (4 epochs fine-tuning) | **8.426,3** | **4.203,3** | **0.695** | 24,7s | 0,080 ms/sample |
| **PyTorch LSTM** | 2 Layers (64 hidden), Lookback 64s | 14.473,4 | 6.935,7 | 0.102 | 129,9s | 0,101 ms/sample |
| **IBM Granite TTM (ZS)** | Zero-Shot Foundation Model (χωρίς training) | 18.641,9 | 10.695,3 | < 0.0 | 0,0s | 0,080 ms/sample |

### 2. Κατάταξη Σπουδαιότητας Ραδιοδεικτών κατά TreeSHAP
1. **UL_bitrate ($9.259\text{ kbps}$ impact):** Η κίνηση Uplink αποτελεί ισχυρότατο δείκτη ενεργών συνεδριών λήψης (TCP ACKs).
2. **RSSI ($1.102\text{ kbps}$ impact):** Συνολική ενέργεια ασύρματου διαύλου.
3. **ServingCell_Distance ($764\text{ kbps}$ impact):** Επίδραση Large-Scale Path Loss.
4. **Speed ($754\text{ kbps}$ impact):** Ταχύτητα οχήματος (Doppler shifts, συχνά handovers).
5. **SNR ($739\text{ kbps}$ impact):** Όριο χωρητικότητας Shannon.
6. **RSRQ, CQI, RSRP:** Συμπληρωματικοί δείκτες ποιότητας σήματος.

### 3. Σταδιακή Αφαίρεση Μεταβλητών (Feature Pruning)
* **100% Χαρακτηριστικών (8 KPIs):** RMSE = 6.447 kbps, Inference = 0,50 $\mu$s.
* **75% Χαρακτηριστικών (6 KPIs):** RMSE = 6.425 kbps, Inference = 0,30 $\mu$s (**Βέλτιστο Edge Trade-off**).
* **25% Χαρακτηριστικών (2 KPIs: UL_bitrate, RSSI):** RMSE = 6.494 kbps (**Μόνο +0,7% σφάλμα με 75% λιγότερα δεδομένα τηλεμετρίας!**).

### 4. 5G Proactive QoS Degradation Early Warning (Threshold = 5 Mbps)
| Lead Time ($\Delta t$) | Ρυθμός Ανίχνευσης (Recall) | Ψευδείς Συναγερμοί (False Alarms) | F1-Score | Εφαρμόσιμες Προληπτικές Ενέργειες |
| :---: | :---: | :---: | :---: | :--- |
| **1 δευτερόλεπτο** | **91,6%** | **6,4%** | **0.929** | Predictive Beamforming, Fast Intra-Cell Handover |
| **3 δευτερόλεπτα** | **88,3%** | 7,8% | **0.905** | Dynamic PRB Scheduling, MEC Video ABR Downgrade |
| **5 δευτερόλεπτα** | **85,7%** | 7,9% | **0.890** | Target gNB Context Pre-Fetch, Dual Connectivity |
| **10 δευτερόλεπτα** | **81,3%** | 7,9% | **0.864** | Carrier Aggregation Reconfiguration, Slice Scaling |
| **15 δευτερόλεπτα** | **78,2%** | 7,5% | **0.847** | Core Network Path Switching, Multi-RAT Offloading |

---

## 📁 Δομή Αρχείων Έργου (Project Structure)

```
5g/
├── data/
│   ├── Dataset/                         # 135 raw cellular trace files (bus, car, pedestrian, static, train)
│   └── processed/
│       ├── combined_traces.csv          # 174,523 cleaned samples
│       ├── train_data.csv               # 131,370 train samples (106 traces)
│       ├── test_data.csv                # 43,153 test samples (29 traces)
│       ├── feature_scaler.joblib        # Fitted StandardScaler
│       └── metadata.json                # Summary dataset statistics
├── models/
│   ├── xgboost_best.joblib              # Best XGBoost Regressor model
│   ├── lstm_model.pt                    # Trained PyTorch LSTM checkpoint
│   └── foundation_ttm.pt                # Fine-tuned IBM Granite TTM checkpoint
├── results/
│   ├── figures/                         # 12 high-resolution figures
│   │   ├── 01_eda_distributions.png
│   │   ├── 02_eda_mobility_comparison.png
│   │   ├── 03_xgboost_horizons_lookback.png
│   │   ├── 04_shap_summary_beeswarm.png
│   │   ├── 05_shap_feature_importance.png
│   │   ├── 06_shap_dependence_plots.png
│   │   ├── 07_shap_waterfall_local.png
│   │   ├── 08_lstm_training_loss.png
│   │   ├── 09_model_comparisons.png
│   │   ├── 10_foundation_model_performance.png
│   │   ├── 11_feature_pruning_accuracy_vs_latency.png
│   │   └── 12_proactive_5g_early_warning_tradeoff.png
│   ├── xgboost_grid_results.json
│   ├── shap_importance.json
│   ├── lstm_results.json
│   ├── foundation_model_results.json
│   ├── feature_pruning_results.json
│   ├── proactive_management_results.json
│   └── metrics_summary.json
├── docs/
│   ├── Technical_Report_5G_Forecasting.pdf   # 3.9 MB Complete Academic Report
│   ├── Technical_Report_5G_Forecasting.docx  # 2.8 MB Word Report
│   └── Technical_Report_5G_Forecasting.md    # Full Markdown Report
├── presentation/
│   └── Downlink_Bitrate_Forecasting_5G.pptx # 3.7 MB, 16 Widescreen Presentation Slides
├── src/
│   ├── config.py                        # Constants, paths and hyperparameters
│   ├── data_processing.py               # Ingestion, cleaning, session split & scaling
│   ├── models_ml.py                     # XGBoost regressor & grid evaluation
│   ├── explainability.py                # TreeSHAP interpretability module
│   ├── models_dl.py                     # PyTorch LSTM time-series forecaster
│   ├── models_foundation.py             # IBM Granite TTM zero-shot & fine-tuning
│   ├── feature_pruning.py               # SHAP-guided pruning & latency benchmark
│   ├── proactive_5g.py                  # 5G QoS early warning simulation
│   └── summary.py                       # Metrics compiler
├── scripts/
│   ├── run_pipeline.py                  # Master CLI pipeline runner
│   ├── verify_all.py                    # Comprehensive test suite
│   ├── generate_report.py               # Generates .md, .docx, and .pdf reports
│   └── generate_presentation.py         # Generates .pptx presentation deck
├── run.bat                              # One-click Windows batch runner
├── run.ps1                              # One-click PowerShell runner
└── README.md                            # Comprehensive project documentation
```

---

## 🎓 Παραδοτέα Αξιολόγησης (Course Deliverables)

1. **Τελική Τεχνική Έκθεση (10-20 σελίδες):**
   * PDF: [`docs/Technical_Report_5G_Forecasting.pdf`](file:///C:/Users/dtsan/Desktop/supertrap/5g/docs/Technical_Report_5G_Forecasting.pdf)
   * Word: [`docs/Technical_Report_5G_Forecasting.docx`](file:///C:/Users/dtsan/Desktop/supertrap/5g/docs/Technical_Report_5G_Forecasting.docx)
   * Markdown: [`docs/Technical_Report_5G_Forecasting.md`](file:///C:/Users/dtsan/Desktop/supertrap/5g/docs/Technical_Report_5G_Forecasting.md)
2. **Παρουσίαση (Slide Deck για Ενδιάμεση & Τελική Εξέταση):**
   * PowerPoint: [`presentation/Downlink_Bitrate_Forecasting_5G.pptx`](file:///C:/Users/dtsan/Desktop/supertrap/5g/presentation/Downlink_Bitrate_Forecasting_5G.pptx)
3. **Πλήρης Πηγαίος Κώδικας & Εκτελέσιμα Scripts:**
   * Master CLI: [`scripts/run_pipeline.py`](file:///C:/Users/dtsan/Desktop/supertrap/5g/scripts/run_pipeline.py)
   * Verification Test: [`scripts/verify_all.py`](file:///C:/Users/dtsan/Desktop/supertrap/5g/scripts/verify_all.py)
   * Runners: [`run.bat`](file:///C:/Users/dtsan/Desktop/supertrap/5g/run.bat), [`run.ps1`](file:///C:/Users/dtsan/Desktop/supertrap/5g/run.ps1)
