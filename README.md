# Πρόβλεψη Downlink Bitrate σε Δίκτυα 5G — Ενδιάμεση Παρουσίαση (40%–50%)

**Μάθημα:** Αρχιτεκτονικές Δικτύων Επόμενης Γενιάς, Τεχνολογίες και Εφαρμογές (Χειμερινό Εξάμηνο 2026–2027)  
**Θέμα 11:** Πρόβλεψη Downlink Bitrate (Throughput) Με Βάση Μετρικές Ποιότητας  
**Επιβλέπων:** Παναγιώτης Μαράντης (`pmaradis@isi.gr`)

---

## Περιεχόμενα Προπαρασκευαστικής / Ενδιάμεσης Φάσης (40%–50% της Εργασίας)

Αυτό το αποθετήριο περιέχει την υλοποίηση του **πρώτου 40%–50%** των ζητουμένων της εργασίας για την Ενδιάμεση Παρουσίαση:

1. **Ζητούμενο 1 (10%):** Τηλεπικοινωνιακή ανάλυση της σημασίας πρόβλεψης του Downlink Bitrate στα σύγχρονα δίκτυα 5G (Proactive Handover, MCS adaptation, Resource Allocation).
2. **Ζητούμενο 2 (15% — `src/data_processing.py`):**
   - Φόρτωση και ένωση των **135 CSV traces** (`174.523` δείγματα) από τα 5 σενάρια κίνησης (`bus`, `car`, `pedestrian`, `static`, `train`) του UCC 4G/LTE Dataset.
   - Καθαρισμός των τιμών `'-'` (nulls) με session-aware `ffill`/`bfill` ανά `trace_id`.
   - Διαχωρισμός σε **80% Train** (`106 traces = 131.370 δείγματα`) και **20% Test** (`29 traces = 43.153 δείγματα`) χωρίς data leakage.
   - Κανονικοποίηση των 8 αριθμητικών μετρικών ποιότητας καναλιού με `StandardScaler`.
3. **Ζητούμενο 3 (15% — `src/models_ml.py`):**
   - Εκπαίδευση μοντέλου παλινδρόμησης **XGBoost Regressor** σε κυλιόμενα παράθυρα χρόνου (`Sliding Windows`).
   - Πειραματική αξιολόγηση για **Lookback Windows** $L \in \{5, 10, 20, 30\}$ δευτερόλεπτα και **Prediction Horizons** $H \in \{1, 3, 5, 10\}$ δευτερόλεπτα.
   - Υπολογισμός και ανάλυση των μετρικών **RMSE**, **MAE**, **MAPE** (για $L=10, H=1$: $\text{RMSE} = 857.6\text{ kbps}$, $\text{MAE} = 507.6\text{ kbps}$).
4. **Ζητούμενο 4 (10% — `src/explainability.py`):**
   - Εφαρμογή **Explainable AI (TreeSHAP)** πάνω στο εκπαιδευμένο μοντέλο XGBoost για την εύρεση των σημαντικότερων μεταβλητών (`UL_bitrate`, `RSSI`, `ServingCell_Distance`, `Speed`, `SNR`, `RSRP`, `RSRQ`, `CQI`).

---

## Δομή Αρχείων (40%–50%)

- `src/config.py`: Βασικές ρυθμίσεις, μονοπάτια και ορισμός των 8 μετρικών εισόδου.
- `src/data_processing.py`: Προεπεξεργασία, καθαρισμός `'-'`, ένωση των 135 traces, κανονικοποίηση και χωρισμός Train/Test.
- `src/models_ml.py`: Εκπαίδευση και αξιολόγηση του XGBoost Regressor για διαφορετικά Lookback & Horizon.
- `src/explainability.py`: Ανάλυση σημαντικότητας μεταβλητών με SHAP.
- `scripts/run_midterm_40pct.py`: Ενιαίο script εκτέλεσης της ενδιάμεσης φάσης (40%–50%).
- `presentation/Endiamesi_Parousiasi_5G_40_50_Percent.pptx`: Οι **6 διαφάνειες** της Ενδιάμεσης Παρουσίασης.
- `results/figures/`: Τα γραφήματα της ενδιάμεσης φάσης (`01` έως `07`).

---

## Εκτέλεση (Live Demo Ενδιάμεσης Παρουσίασης)

```bash
pip install -r requirements.txt
run.bat
```
*(ή `python scripts/run_midterm_40pct.py`)*

---

## Επόμενα Βήματα (Υπόλοιπο 50%–60% έως την Τελική Παρουσίαση)
- **Ζητούμενο 5:** Εκπαίδευση μοντέλου Deep Learning (**LSTM** με παράθυρο 64 δειγμάτων) και σύγκριση με το XGBoost.
- **Ζητούμενο 6 (Bonus):** Δοκιμή Time-Series Foundation Model (**IBM Granite Tiny Time Mixer** — Zero-shot & Fine-tuning).
- **Ζητούμενο 7:** Σταδιακή αφαίρεση λιγότερο σημαντικών μεταβλητών (βάσει SHAP) και αξιολόγηση χρόνου εκπαίδευσης/πρόβλεψης.
- **Ζητούμενο 8:** Μελέτη **5G Proactive Network Management** (έγκαιρη ανίχνευση πτώσης ρυθμού μετάδοσης και trade-off ακρίβειας vs διαθέσιμου χρόνου αντίδρασης).
