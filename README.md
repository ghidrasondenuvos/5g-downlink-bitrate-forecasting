# Πρόβλεψη Downlink Bitrate (Throughput) σε Δίκτυα 5G & Προληπτική Διαχείριση Πόρων

**Μάθημα:** Αρχιτεκτονικές Δικτύων Επόμενης Γενιάς, Τεχνολογίες και Εφαρμογές (Χειμερινό Εξάμηνο 2026–2027)  
**Θέμα Project 11:** Πρόβλεψη Downlink Bitrate (Throughput) Με Βάση Μετρικές Ποιότητας  
**Συγγραφείς / Ομάδα Έργου:**
- **Δημήτριος Τσανακτσής (Α.Μ.: 1100736)** — **ΔΗΜΗΤΡΙΟΣ ΤΣΑΝΑΚΤΣΗΣ (Α.Μ.: 1100736)**
- **Ιάσωνας Δερβενής (Α.Μ.: 1097437)** — **ΙΑΣΩΝΑΣ ΔΕΡΒΕΝΗΣ (Α.Μ.: 1097437)**

**Επιβλέπων:** Παναγιώτης Μαράντης (`pmaradis@isi.gr`) — Ερευνητικό Κέντρο ISI / Πανεπιστήμιο Πατρών  
**GitHub Repository:** [https://github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting](https://github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting)

---

## 📌 Περίληψη Έργου (Executive Summary)

Το παρόν αποθετήριο περιλαμβάνει τόσο την **Ενδιάμεση Παρουσίαση (40%–50% των ζητουμένων: Ζητούμενα 1–4)** όσο και την **Πλήρη / Τελική Υλοποίηση (100% των ζητουμένων: Ζητούμενα 1–8)** για την πρόβλεψη του ρυθμού μετάδοσης δεδομένων λήψης (**Downlink Bitrate / Throughput**) σε πραγματικό χρόνο σε κυψελωτά δίκτυα **5G NR / 6G**, με στόχο την **προληπτική διαχείριση πόρων (Proactive QoS/QoE Management)** και την ένταξη στις αρχιτεκτονικές **3GPP NWDAF** και **O-RAN Near-RT RIC**.

Χρησιμοποιήθηκαν **135 πραγματικές κυψελωτές καταγραφές (`174.523` δείγματα με ρυθμό `1 Hz`)** από το επίσημο dataset του University College Cork (UCC MISL) για 5 σενάρια κινητικότητας (`car`, `train`, `pedestrian`, `static`, `bus`).

---

## 🎓 Παραδοτέα Παρουσιάσεων & Τεχνικών Αναφορών

### Α. Ενδιάμεση Παρουσίαση (40%–50% της Εργασίας — Ζητούμενα 1 έως 4)
- **Παρουσίαση PowerPoint:** [`presentation/Endiamesi_Parousiasi_5G_40_50_Percent.pptx`](presentation/Endiamesi_Parousiasi_5G_40_50_Percent.pptx)
- **Script Εκτέλεσης Live Demo (40%–50%):** `python scripts/run_midterm_40pct.py` (ή `run.bat`)
- **Καλυπτόμενα Ζητούμενα (40%–50%):**
  1. **Ζητούμενο 1 (10%):** Τηλεπικοινωνιακή ανάλυση της σημασίας πρόβλεψης του Downlink Bitrate στα σύγχρονα δίκτυα 5G (Proactive Handover, MCS adaptation, Resource Allocation).
  2. **Ζητούμενο 2 (15% — `src/data_processing.py`):** Φόρτωση και ένωση των **135 CSV traces** (`174.523` δείγματα), καθαρισμός των τιμών `'-'` με session-aware `ffill`/`bfill` ανά `trace_id`, διαχωρισμός σε **80% Train** (`106 traces = 131.370 δείγματα`) και **20% Test** (`29 traces = 43.153 δείγματα`) χωρίς data leakage, και κανονικοποίηση με `StandardScaler`.
  3. **Ζητούμενο 3 (15% — `src/models_ml.py`):** Εκπαίδευση μοντέλου παλινδρόμησης **XGBoost Regressor** σε κυλιόμενα παράθυρα χρόνου (`Sliding Windows`) για **Lookback Windows** $L \in \{5, 10, 20, 30\}\text{s}$ και **Prediction Horizons** $H \in \{1, 3, 5, 10\}\text{s}$.
  4. **Ζητούμενο 4 (10% — `src/explainability.py`):** Εφαρμογή **Explainable AI (TreeSHAP)** πάνω στο εκπαιδευμένο μοντέλο XGBoost για την εύρεση των σημαντικότερων μεταβλητών (`UL_bitrate`, `RSSI`, `ServingCell_Distance`, `Speed`, `SNR`, `RSRQ`, `CQI`, `RSRP`).

### Β. Τελική Παρουσίαση & Πλήρης Τεχνική Έκθεση (100% της Εργασίας — Ζητούμενα 1 έως 8)
- **Πλήρης Παρουσίαση PowerPoint (20 Διαφάνειες):** [`presentation/Downlink_Bitrate_Forecasting_5G.pptx`](presentation/Downlink_Bitrate_Forecasting_5G.pptx) & [`presentation/Teliki_Parousiasi_5G_100_Percent.pptx`](presentation/Teliki_Parousiasi_5G_100_Percent.pptx)
- **Τεχνική Αναφορά PDF:** [`docs/Technical_Report_5G_Forecasting.pdf`](docs/Technical_Report_5G_Forecasting.pdf)
- **Τεχνική Αναφορά Word (.docx):** [`docs/Technical_Report_5G_Forecasting.docx`](docs/Technical_Report_5G_Forecasting.docx)
- **Τεχνική Αναφορά Markdown (.md):** [`docs/Technical_Report_5G_Forecasting.md`](docs/Technical_Report_5G_Forecasting.md)
- **Επιπλέον Καλυπτόμενα Ζητούμενα (50%–100%):**
  5. **Ζητούμενο 5 (15% — `src/models_dl.py`):** Εκπαίδευση μοντέλου Deep Learning (**PyTorch LSTM** 2 επιπέδων με παράθυρο 64 δειγμάτων) και σύγκριση με το XGBoost.
  6. **Ζητούμενο 6 (15% Bonus — `src/models_foundation.py`):** Time-Series Foundation Model (**IBM Granite Tiny Time Mixer - TTM**) σε **Zero-Shot** και **Fine-Tuning** (54,8% μείωση σφάλματος RMSE σε 4 εποχές).
  7. **Ζητούμενο 7 (10% — `src/feature_pruning.py`):** Σταδιακή αφαίρεση λιγότερο σημαντικών μεταβλητών βάσει SHAP (100% → 75% → 50% → 25% KPIs) και αξιολόγηση ακρίβειας vs χρόνου εκπαίδευσης/πρόβλεψης.
  8. **Ζητούμενο 8 (10% — `src/proactive_5g.py`):** Μελέτη **5G Proactive Network Management** (έγκαιρη ανίχνευση πτώσης ρυθμού μετάδοσης κάτω από 5 Mbps και trade-off ακρίβειας vs διαθέσιμου χρόνου αντίδρασης $\Delta t \in \{1, 3, 5, 10, 15\}\text{s}$).

---

## 🚀 Εντολές Εκτέλεσης (Ready-to-Run Commands)

```bash
pip install -r requirements.txt
```

### 1. Εκτέλεση Ενδιάμεσης Παρουσίασης (40%–50%)
```bash
run.bat
# ή
python scripts/run_midterm_40pct.py
```

### 2. Εκτέλεση Ολόκληρου του Pipeline (100% των Ζητουμένων)
```bash
python scripts/run_pipeline.py --all
```

### 3. Τμηματική Εκτέλεση Ανά Ζητούμενο (Modular CLI)

| Ζητούμενο | Περιγραφή | Εντολή Python CLI |
| :--- | :--- | :--- |
| **Προεπεξεργασία (Ζητ. 2)** | Καθαρισμός, Session Split & Scaling | `python scripts/run_pipeline.py --preprocess` |
| **XGBoost Grid (Ζητ. 3)** | Πλέγμα Lookbacks & Horizons | `python scripts/run_pipeline.py --ml` |
| **TreeSHAP XAI (Ζητ. 4)** | Επεξηγησιμότητα & Beeswarm/Waterfall Plots | `python scripts/run_pipeline.py --shap` |
| **PyTorch LSTM (Ζητ. 5)** | Deep Learning Χρονοσειρών (Lookback 64) | `python scripts/run_pipeline.py --dl` |
| **Foundation Model (Ζητ. 6)** | IBM Granite TTM (Zero-Shot & Fine-Tuning) | `python scripts/run_pipeline.py --foundation` |
| **Feature Pruning (Ζητ. 7)** | Σταδιακή Αφαίρεση Μεταβλητών & Latency | `python scripts/run_pipeline.py --prune` |
| **5G Proactive (Ζητ. 8)** | Προληπτική Ανίχνευση Υποβάθμισης QoS | `python scripts/run_pipeline.py --proactive` |
| **Αναφορές (.md/.docx/.pdf)** | Παραγωγή Τεχνικής Έκθεσης | `python scripts/generate_report.py` |
| **Παρουσιάσεις (.pptx)** | Παραγωγή Παρουσιάσεων | `python scripts/generate_presentation.py` |
| **Έλεγχος / Verify** | Πλήρης Έλεγχος Ακεραιότητας Αρχείων | `python scripts/verify_all.py` |

---

## 📊 Σύνοψη Πειραματικών Αποτελεσμάτων

### 1. Σύγκριση Μοντέλων Πρόβλεψης Throughput ($H = 1\text{s}$)
| Μοντέλο | Αρχιτεκτονική / Ρύθμιση | RMSE (kbps) | MAE (kbps) | $R^2$ Score | Χρόνος Train | Inference Latency |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **XGBoost Regressor** | 100 Trees, Lookback 10s, Horizon 1s | **6.344,8** | **3.275,5** | **0.825** | **1,3s** | **0,0006 ms/sample** |
| **IBM Granite TTM (FT)** | Patch-based MLP-Mixer (4 epochs fine-tuning) | **8.426,3** | **4.203,3** | **0.695** | 24,7s | 0,0802 ms/sample |
| **PyTorch LSTM** | 2 Layers (64 hidden), Lookback 64s | 14.473,4 | 6.935,7 | 0.102 | 129,9s | 0,1009 ms/sample |
| **IBM Granite TTM (ZS)** | Zero-Shot Foundation Model (χωρίς training) | 18.641,9 | 10.695,3 | -0.491 | 0,0s | 0,0793 ms/sample |

### 2. Κατάταξη Σπουδαιότητας Ραδιοδεικτών κατά TreeSHAP
1. **`UL_bitrate` ($9.259,05\text{ kbps}$ impact — 65,85%):** Η κίνηση Uplink αποτελεί ισχυρότατο δείκτη ενεργών συνεδριών λήψης (TCP ACKs).
2. **`RSSI` ($1.102,90\text{ kbps}$ impact — 7,84%):** Συνολική ενέργεια ασύρματου διαύλου.
3. **`ServingCell_Distance` ($764,36\text{ kbps}$ impact — 5,44%):** Επίδραση Large-Scale Path Loss.
4. **`Speed` ($754,83\text{ kbps}$ impact — 5,37%):** Ταχύτητα οχήματος (Doppler shifts, συχνά handovers).
5. **`SNR` ($739,19\text{ kbps}$ impact — 5,26%):** Όριο χωρητικότητας Shannon.
6. **`RSRQ` ($565,73\text{ kbps}$), `CQI` ($490,00\text{ kbps}$), `RSRP` ($385,33\text{ kbps}$):** Συμπληρωματικοί δείκτες ποιότητας σήματος.

### 3. 5G Proactive QoS Degradation Early Warning (Threshold $\tau = 5\text{ Mbps}$)
| Lead Time ($\Delta t$) | Ρυθμός Ανίχνευσης (Recall) | Ψευδείς Συναγερμοί (False Alarms) | F1-Score | Εφαρμόσιμες Προληπτικές Ενέργειες |
| :---: | :---: | :---: | :---: | :--- |
| **1 δευτερόλεπτο** | **91,65%** | **6,43%** | **0.929** | Predictive Beamforming, Fast Intra-Cell Handover |
| **3 δευτερόλεπτα** | **88,32%** | 7,84% | **0.905** | Dynamic PRB Scheduling, MEC Video ABR Downgrade |
| **5 δευτερόλεπτα** | **85,74%** | 7,93% | **0.890** | Target gNB Context Pre-Fetch, Dual Connectivity |
| **10 δευτερόλεπτα** | **81,29%** | 7,92% | **0.864** | Carrier Aggregation Reconfiguration, Slice Scaling |
| **15 δευτερόλεπτα** | **78,17%** | 7,52% | **0.847** | Core Network Path Switching, Multi-RAT Offloading |
