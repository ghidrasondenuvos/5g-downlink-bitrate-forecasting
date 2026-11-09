"""
Report Generation Script.
Generates a comprehensive 15-20 page Technical Academic Report in Markdown (.md),
Word Document (.docx), and PDF (.pdf) formats.
Covers all 8 project questions, methodology, mathematical formulations, figures, tables, and conclusions.
"""

import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from src.config import BASE_DIR, DOCS_DIR, FIGURES_DIR, RESULTS_DIR

# Register Unicode TrueType fonts (Arial) so Greek glyphs render cleanly in PDF
PDF_FONT_REG = "Helvetica"
PDF_FONT_BOLD = "Helvetica-Bold"
PDF_FONT_ITALIC = "Helvetica-Oblique"
try:
    win_fonts = Path(r"C:\Windows\Fonts")
    if (win_fonts / "arial.ttf").exists():
        pdfmetrics.registerFont(TTFont("ArialUni", str(win_fonts / "arial.ttf")))
        pdfmetrics.registerFont(TTFont("ArialUni-Bold", str(win_fonts / "arialbd.ttf")))
        pdfmetrics.registerFont(TTFont("ArialUni-Italic", str(win_fonts / "ariali.ttf")))
        pdfmetrics.registerFontFamily(
            "ArialUni",
            normal="ArialUni",
            bold="ArialUni-Bold",
            italic="ArialUni-Italic",
            boldItalic="ArialUni-Bold"
        )
        PDF_FONT_REG = "ArialUni"
        PDF_FONT_BOLD = "ArialUni-Bold"
        PDF_FONT_ITALIC = "ArialUni-Italic"
except Exception:
    pass


def set_cell_background(cell, fill_hex):
    """Sets background color of a Word table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def generate_markdown_report(metrics: dict) -> str:
    """Generates the Markdown version of the academic report."""
    md_content = r"""# ΠΑΝΕΠΙΣΤΗΜΙΟ ΠΑΤΡΩΝ / ΕΡΕΥΝΗΤΙΚΟ ΚΕΝΤΡΟ ISI
## ΤΜΗΜΑ ΜΗΧΑΝΙΚΩΝ Η/Υ & ΠΛΗΡΟΦΟΡΙΚΗΣ
### ΜΑΘΗΜΑ: ΑΡΧΙΤΕΚΤΟΝΙΚΕΣ ΔΙΚΤΥΩΝ ΕΠΟΜΕΝΗΣ ΓΕΝΙΑΣ, ΤΕΧΝΟΛΟΓΙΕΣ ΚΑΙ ΕΦΑΡΜΟΓΕΣ
**ΧΕΙΜΕΡΙΝΟ ΕΞΑΜΗΝΟ 2026-2027**

---

# ΤΕΧΝΙΚΗ ΑΝΑΦΟΡΑ PROJECT (ΘΕΜΑ 11)
## Πρόβλεψη Downlink Bitrate (Throughput) Με Βάση Μετρικές Ποιότητας Καναλιού & Προληπτική Διαχείριση Πόρων σε Δίκτυα 5G/6G

* **Συγγραφείς / Ομάδα Έργου:**
  * **Δημήτριος Τσανακτσής (Α.Μ.: 1100736)**
  * **Ιάσωνας Δερβενής (Α.Μ.: 1097437)**
* **Επιβλέπων:** Παναγιώτης Μαράντης (pmaradis@isi.gr)
* **GitHub Repository (Πηγαίος Κώδικας & Παραδοτέα):** [https://github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting](https://github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting)
* **Ημερομηνία Υποβολής:** Νοέμβριος 2026
* **Dataset:** 4G/LTE & 5G Key Performance Indicators (UCC MISL Dataset - 135 Cellular Traces, 174.523 δείγματα)
* **Τεχνολογίες & Εργαλεία:** Python 3.14, XGBoost, PyTorch, TreeSHAP, IBM Granite Tiny Time Mixer (TTM), Scikit-Learn, Pandas

---

## ΠΕΡΙΕΧΟΜΕΝΑ
1. [Εισαγωγή & Τηλεπικοινωνιακή Σημασία της Πρόβλεψης Throughput στα Δίκτυα 5G/6G](#1-εισαγωγή--τηλεπικοινωνιακή-σημασία)
2. [Περιγραφή & Προεπεξεργασία Δεδομένων (Data Preprocessing & Aggregation)](#2-προεπεξεργασία-δεδομένων)
3. [Πρόβλεψη με Μηχανική Μάθηση (XGBoost Regressor) & Ανάλυση Παραμέτρων (Lookback & Horizons)](#3-πρόβλεψη-με-xgboost)
4. [Επεξηγήσιμη Τεχνητή Νοημοσύνη (Explainable AI - TreeSHAP) & Ερμηνεία Μετρικών Καναλιού](#4-επεξηγήσιμη-τεχνητή-νοημοσύνη)
5. [Πρόβλεψη Χρονοσειρών με Deep Learning (PyTorch LSTM) & Συγκριτική Αξιολόγηση](#5-πρόβλεψη-με-lstm)
6. [Foundation Models για Χρονοσειρές: Zero-Shot & Fine-Tuning (IBM Granite Tiny Time Mixer)](#6-foundation-models)
7. [Σταδιακή Αφαίρεση Μεταβλητών (SHAP-Guided Feature Pruning) & Edge Computing Latency](#7-σταδιακή-αφαίρεση-μεταβλητών)
8. [5G Proactive Network Management: Προληπτική Διαχείριση Πόρων & Trade-Offs](#8-5g-proactive-network-management)
9. [Τηλεπικοινωνιακή Αρχιτεκτονική & Ενορχήστρωση σε 5G/6G (O-RAN RIC & NWDAF)](#9-τηλεπικοινωνιακή-αρχιτεκτονική)
10. [Συμπεράσματα & Μελλοντικές Επεκτάσεις](#10-συμπεράσματα)
11. [Βιβλιογραφικές Αναφορές](#11-βιβλιογραφία)

---

## 1. Εισαγωγή & Τηλεπικοινωνιακή Σημασία

### 1.1 Το Πρόβλημα της Στοχαστικής Συμπεριφοράς του Ασύρματου Καναλιού
Στα σύγχρονα κυψελωτά δίκτυα πέμπτης και έκτης γενιάς (5G NR / 6G), η διαθέσιμη ποιότητα σύνδεσης και ο ρυθμός μετάδοσης δεδομένων προς τον χρήστη (Downlink Bitrate / Throughput) παρουσιάζουν έντονη στοχαστικότητα και ταχύτατες διακυμάνσεις. Οι αιτίες εστιάζονται σε:
1. **Κινητικότητα Χρήστη (Mobility):** Μεταβολή της ταχύτητας και της θέσης του τερματικού (πεζός, επιβάτης σε ΙΧ, λεωφορείο ή τρένο), με αποτέλεσμα φαινόμενα Doppler shift και ραγδαίες αλλαγές στο path loss.
2. **Μικροκυματικές & mmWave Ζώνες Συχνοτήτων:** Χρήση συχνοτήτων άνω των 6 GHz και mmWave (24-40 GHz), όπου η εξασθένηση από εμπόδια (shadowing / blockage από κτίρια, οχήματα, ανθρώπους) είναι απότομη.
3. **Διακύμανση Φόρτου Κυψέλης (Cell Congestion):** Μεταβαλλόμενος ανταγωνισμός για τα διαθέσιμα Physical Resource Blocks (PRBs) μεταξύ πολλαπλών UEs.
4. **Πολυδιαδρομική Διάδοση (Multipath Fading):** Κατασκευαστικές και καταστροφικές συμβολές που προκαλούν fast fading σε κλίμακα χιλιοστοδευτερολέπτων.

### 1.2 Γιατί η Πρόβλεψη του Throughput είναι Θεμελιώδης στο 5G;
Παραδοσιακά, τα τηλεπικοινωνιακά δίκτυα αντιδρούν **αναδρομικά (reactively)**: μόλις ανιχνευθεί υποβάθμιση του καναλιού, ο αλγόριθμος Adaptive Modulation and Coding (AMC) μειώνει το Modulation Coding Scheme (MCS), ή η εφαρμογή streaming (π.χ. DASH/HLS) αντιμετωπίζει buffer stall (πάγωμα video) πριν υποβιβάσει την ανάλυση.

Αντιθέτως, η **προληπτική (proactive) πρόβλεψη του throughput** με ορίζοντα μερικών δευτερολέπτων προσφέρει:
* **Εγγύηση SLA σε Network Slices:** Στα slices eMBB (Enhanced Mobile Broadband) και URLLC (Ultra-Reliable Low-Latency Communication), ο προληπτικός υπολογισμός επιτρέπει την εκ των προτέρων δέσμευση φάσματος ώστε να μην παραβιαστεί το QoS.
* **Αποφυγή Radio Link Failure (RLF) & Προληπτικό Handover:** Έγκαιρη προετοιμασία μετάβασης (handover) σε γειτονικό σταθμό βάσης (gNodeB) ή αλλαγή beamforming beam πριν αποκοπεί η σύνδεση.
* **Βελτιστοποίηση Multi-Access Edge Computing (MEC) & Video Streaming:** Προσαρμογή του bitrate του βίντεο και προ-μεταφορά δεδομένων (pre-fetching / transcoding) στον διακομιστή άκρου.
* **Διαχείριση Διπλής Συνδεσιμότητας (Dual Connectivity - EN-DC / NR-DC):** Έγκαιρη ανακατεύθυνση των πακέτων δεδομένων μεταξύ Master Node και Secondary Node.

---

## 2. Προεπεξεργασία Δεδομένων (Data Preprocessing & Aggregation)

### 2.1 Χαρακτηριστικά του Dataset
Χρησιμοποιήθηκε το επίσημο dataset κυψελωτών μετρήσεων του University College Cork (UCC MISL - Raca et al.), το οποίο περιλαμβάνει:
* **135 πραγματικά traces** διάρκειας ~15 λεπτών έκαστο (δειγματοληψία 1 δείγμα ανά δευτερόλεπτο).
* **Συνολικά δείγματα:** **174.523 δευτερόλεπτα** (πάνω από 48,5 ώρες πραγματικών καταγραφών).
* **Σενάρια Κίνησης:**
  * `Car` (αυτοκίνητο): 75.874 δείγματα (53 traces)
  * `Train` (τρένο): 38.976 δείγματα (20 traces)
  * `Pedestrian` (πεζός): 33.629 δείγματα (31 traces)
  * `Static` (ακίνητος): 15.261 δείγματα (15 traces)
  * `Bus` (λεωφορείο): 10.783 δείγματα (16 traces)

### 2.2 Μεταβλητές & Φυσική Σημασία
| Μεταβλητή | Μονάδα | Περιγραφή & Τηλεπικοινωνιακή Σημασία |
| :--- | :--- | :--- |
| **DL_bitrate** | kbps | Στόχος πρόβλεψης: Ρυθμός μετάδοσης δεδομένων λήψης (Throughput) |
| **UL_bitrate** | kbps | Ρυθμός αποστολής δεδομένων (Uplink activity / TCP ACKs) |
| **RSRP** | dBm | Reference Signal Received Power: Ισχύς σήματος αναφοράς |
| **RSRQ** | dB | Reference Signal Received Quality: Ποιότητα λαμβανόμενου σήματος |
| **SNR** | dB | Signal-to-Noise Ratio: Λόγος σήματος προς θόρυβο |
| **CQI** | 1-15 | Channel Quality Indicator: 4-bit δείκτης υποστηριζόμενου MCS |
| **RSSI** | dBm | Received Signal Strength Indicator: Συνολική λαμβανόμενη ισχύς |
| **Speed** | km/h | Ταχύτητα κίνησης συσκευής (GPS velocity) |
| **ServingCell_Distance** | m | Ευκλείδεια απόσταση από τον εξυπηρετούντα σταθμό βάσης |

### 2.3 Στρατηγική Καθαρισμού & Session-Aware Split
1. **Διαχείριση Missing Values:** Εντοπίστηκαν σύμβολα `'-'` σε κολώνες όπως `CQI`, `RSSI`, `NRxRSRP`. Εφαρμόστηκε συνεδριακό forward-fill (`ffill`) και backward-fill (`bfill`) ανά trace (καθώς το κανάλι μεταβάλλεται ομαλά στο χρόνο) και εν συνεχεία καθολική διάμεσος.
2. **Αποτροπή Data Leakage (Session Split):** Αντί για τυχαίο ανακάτεμα γραμμών, πραγματοποιήθηκε διαχωρισμός σε επίπεδο ολόκληρων traces: 80% των traces για εκπαίδευση (131.370 δείγματα σε 106 traces) και 20% για δοκιμή (43.153 δείγματα σε 29 traces).
3. **Κανονικοποίηση (StandardScaler):** Το scaling προσαρμόστηκε αποκλειστικά στο train set και εφαρμόστηκε μετασχηματισμός στο test set.

![EDA Distributions](../results/figures/01_eda_distributions.png)
*Σχήμα 1: Κατανομές ραδιοδεικτών KPI και Downlink Throughput στο σύνολο δεδομένων.*

![EDA Mobility Comparison](../results/figures/02_eda_mobility_comparison.png)
*Σχήμα 2: Σύγκριση Downlink Bitrate ανά σενάριο κίνησης και πίνακας συσχέτισης μετρικών.*

---

## 3. Πρόβλεψη με XGBoost Regressor

### 3.1 Μεθοδολογία Ολισθαίνοντος Παραθύρου (Sliding Window)
Για κάθε συνεχή καταγραφή $i$, κατασκευάζονται παράθυρα εισόδου μεγέθους $L$ (lookback) για πρόβλεψη $H$ βήματα μπροστά:
$$\mathbf{X}_t = [x_{t-L+1}, x_{t-L+2}, \dots, x_t] \in \mathbb{R}^{L \times D}$$
$$y_t = \text{DL\_bitrate}_{t+H}$$

### 3.2 Πειραματικό Πλέγμα (Grid Evaluation: Lookbacks & Horizons)
Εξετάστηκαν συνδυασμοί:
* $L \in \{5, 10, 20, 30\}$ δευτερόλεπτα
* $H \in \{1, 3, 5, 10\}$ δευτερόλεπτα ahead

| Lookback $L$ (s) | Horizon $H$ (s) | RMSE (kbps) | MAE (kbps) | $R^2$ Score | Χρόνος Train (s) | Inference (ms/sample) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 5 | 1 | 6443.1 | 3298.3 | 0.819 | 0.6 | 0.001 |
| 5 | 3 | 7603.3 | 4120.4 | 0.748 | 1.4 | 0.001 |
| 5 | 5 | 8264.9 | 4582.0 | 0.703 | 1.0 | 0.001 |
| 5 | 10 | 8948.2 | 5026.1 | 0.651 | 1.0 | 0.001 |
| **10** | **1** | **6344.8** | **3275.5** | **0.825** | **1.3** | **0.001** |
| 10 | 3 | 7503.1 | 3998.0 | 0.755 | 2.6 | 0.001 |
| 10 | 5 | 7961.7 | 4345.6 | 0.724 | 1.3 | 0.001 |
| 10 | 10 | 9112.5 | 5111.8 | 0.639 | 1.2 | 0.001 |
| 20 | 1 | 6334.5 | 3279.3 | 0.826 | 2.0 | 0.001 |
| 20 | 3 | 7322.8 | 3974.2 | 0.767 | 2.1 | 0.001 |
| 20 | 5 | 7979.9 | 4359.9 | 0.724 | 3.1 | 0.001 |
| 20 | 10 | 8795.1 | 4922.9 | 0.665 | 2.4 | 0.001 |
| 30 | 1 | 6352.3 | 3255.5 | 0.826 | 3.4 | 0.001 |
| 30 | 3 | 7424.0 | 3952.6 | 0.762 | 3.2 | 0.001 |
| 30 | 5 | 7970.3 | 4337.1 | 0.726 | 3.1 | 0.001 |
| 30 | 10 | 8985.2 | 4977.2 | 0.652 | 3.6 | 0.001 |

### 3.3 Ανάλυση Αποτελεσμάτων
1. **Επίδραση Horizon ($H$):** Όσο αυξάνεται ο ορίζοντας πρόβλεψης από 1s σε 10s, το σφάλμα RMSE αυξάνεται μονοτονικά από 6.34 Mbps σε 9.11 Mbps ($+43.6\%$), ενώ το $R^2$ υποχωρεί από 0.825 σε 0.639. Αυτό είναι απόλυτα φυσικό λόγω της ταχείας διακύμανσης του ασύρματου καναλιού.
2. **Επίδραση Lookback ($L$):** Η αύξηση του lookback πέραν των 10 δευτερολέπτων ($L=20, 30$) προσφέρει οριακή βελτίωση ($<0.2\%$ στο RMSE), αλλά διπλασιάζει τον αριθμό των χαρακτηριστικών και τον χρόνο εκπαίδευσης. Συνεπώς, το σημείο $L=10$ αποτελεί τη βέλτιστη τομή απόδοσης-πολυπλοκότητας.

![XGBoost Grid Evaluation](../results/figures/03_xgboost_horizons_lookback.png)
*Σχήμα 3: Ευαισθησία μετρικών RMSE, MAE και πραγματική έναντι προβλεπόμενης τροχιάς.*

---

## 4. Επεξηγήσιμη Τεχνητή Νοημοσύνη (Explainable AI - TreeSHAP)

### 4.1 Μαθηματικό Υπόβαθρο Shapley Values
Η τεχνική TreeSHAP αποδίδει τη συνεισφορά κάθε χαρακτηριστικού $i$ στην πρόβλεψη $f(x)$ μέσω των τιμών Shapley από τη θεωρία συνεργατικών παιγνίων:
$$\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f(S \cup \{i\}) - f(S) \right]$$

### 4.2 Συγκεντρωτική Κατάταξη Σπουδαιότητας Χαρακτηριστικών
Από την ανάλυση TreeSHAP σε 1.500 δείγματα δοκιμής, προέκυψε η ακόλουθη συνολική σπουδαιότητα (άθροισμα $|SHAP|$ σε όλα τα time-lags):
1. **UL_bitrate:** $9.259,05\text{ kbps}$ impact (ισχυρότατος δείκτης: η κίνηση uplink συσχετίζεται άμεσα με TCP ACK traffic και ενεργές συνεδρίες λήψης).
2. **RSSI:** $1.102,90\text{ kbps}$ impact (συνολική λαμβανόμενη ισχύς που αντικατοπτρίζει την εγγύτητα και τη συνολική ενέργεια του καναλιού).
3. **ServingCell_Distance:** $764,36\text{ kbps}$ impact (επιβεβαιώνει την επίδραση του Large-Scale Path Loss).
4. **Speed:** $754,83\text{ kbps}$ impact (υψηλότερες ταχύτητες προκαλούν συχνότερα handovers και Doppler shifts).
5. **SNR:** $739,19\text{ kbps}$ impact (καθορίζει το Shannon channel capacity limit).
6. **RSRQ:** $702,68\text{ kbps}$ impact.
7. **CQI:** $686,30\text{ kbps}$ impact.
8. **RSRP:** $574,84\text{ kbps}$ impact.

![SHAP Beeswarm](../results/figures/04_shap_summary_beeswarm.png)
*Σχήμα 4: TreeSHAP Beeswarm plot που απεικονίζει τη θετική ή αρνητική επίδραση των τιμών κάθε χαρακτηριστικού.*

![SHAP Importance](../results/figures/05_shap_feature_importance.png)
*Σχήμα 5: Συνολική σπουδαιότητα ραδιοδεικτών κατά TreeSHAP.*

![SHAP Dependence](../results/figures/06_shap_dependence_plots.png)
*Σχήμα 6: Διαγράμματα εξάρτησης SHAP (Dependence plots) και μη-γραμμικές αλληλεπιδράσεις καναλιού.*

![SHAP Waterfall](../results/figures/07_shap_waterfall_local.png)
*Σχήμα 7: Τοπική ερμηνεία με καταρράκτη SHAP (Waterfall plots) για γεγονός υψηλού throughput έναντι απότομης υποβάθμισης σύνδεσης.*

---

## 5. Πρόβλεψη με Deep Learning (PyTorch LSTM)

### 5.1 Αρχιτεκτονική Νευρωνικού Δικτύου
Υλοποιήθηκε δίκτυο Long Short-Term Memory (LSTM) σε PyTorch:
* **Input Dimension:** 8 χαρακτηριστικά $\times$ 64 χρονικά βήματα (Lookback = 64 δευτερόλεπτα).
* **Κρυφά Επίπεδα:** 2 επίπεδα LSTM με $hidden\_dim = 64$ και $Dropout = 0.2$.
* **Projection Head:** Dense(64 $\to$ 32) $\to$ ReLU $\to$ Dropout(0.2) $\to$ Linear(32 $\to$ 1).
* **Βελτιστοποιητής:** Adam ($\eta = 0.001$, weight decay = $10^{-5}$), Loss Function: MSE.

### 5.2 Σύγκριση Αποτελεσμάτων: XGBoost έναντι LSTM
| Μετρική Αξιολόγησης | XGBoost Regressor | PyTorch LSTM | Σχόλιο & Υπεροχή |
| :--- | :---: | :---: | :--- |
| **Lookback Window ($L$)** | 10 samples | 64 samples | Το LSTM εκμεταλλεύεται ευρύτερο παράθυρο |
| **Prediction Horizon ($H$)** | 1 sample ahead | 1 sample ahead | Επόμενο δευτερόλεπτο |
| **RMSE (kbps)** | **6.344,8** | 14.473,4 | Το XGBoost πετυχαίνει **56,2% χαμηλότερο σφάλμα** |
| **MAE (kbps)** | **3.275,5** | 6.935,7 | Το XGBoost υπερέχει κατά **52,8%** |
| **Goodness-of-Fit ($R^2$)** | **0.825** | 0.102 | Εξαιρετική προσαρμογή του δένδρου απόφασης |
| **Χρόνος Εκπαίδευσης** | **1,3 δευτερόλεπτα** | 129,9 δευτερόλεπτα | Το XGBoost εκπαιδεύεται **100x ταχύτερα** |
| **Inference Latency** | **0,001 ms/δείγμα** | 0,101 ms/δείγμα | **100x ταχύτερη απόκριση στο Edge** |

![LSTM Loss Curve](../results/figures/08_lstm_training_loss.png)
*Σχήμα 8: Καμπύλη εκπαίδευσης και επικύρωσης του δικτύου LSTM.*

![Model Comparison](../results/figures/09_model_comparisons.png)
*Σχήμα 9: Συγκριτική αποτίμηση XGBoost έναντι PyTorch LSTM (Error, R² και Inference Latency).*

---

## 6. Foundation Models: Zero-Shot & Fine-Tuning (IBM Granite TTM)

### 6.1 Αρχιτεκτονική Tiny Time Mixer (TTM)
Το μοντέλο θεμελίωσης IBM Granite TTM βασίζεται σε αρχιτεκτονική Patch-based MLP-Mixer:
1. **Patchification:** Τεμαχισμός του παραθύρου 64 δευτερολέπτων σε 8 μη-επικαλυπτόμενα patches μήκους 8 δειγμάτων.
2. **Inter-Patch Time Mixing:** Γραμμικά επίπεδα ανάμιξης χρονικών συσχετίσεων μεταξύ των patches.
3. **Intra-Patch Channel Mixing:** Ανάμιξη των 8 ραδιοδιαύλων μέσα σε κάθε patch με υπολειμματικές συνδέσεις (residual skip connections).

### 6.2 Αποτελέσματα Zero-Shot & Fine-Tuning
| Μοντέλο | Κατάσταση Εκπαίδευσης | RMSE (kbps) | MAE (kbps) | $R^2$ Score |
| :--- | :--- | :---: | :---: | :---: |
| **IBM Granite TTM** | **Zero-Shot** (χωρίς εκπαίδευση) | 18.641,9 | 10.695,3 | < 0.0 |
| **IBM Granite TTM** | **Fine-Tuned** (4 εποχές προσαρμογής) | **8.426,3** | **4.203,3** | **0.695** |
| **PyTorch LSTM** | Εκπαίδευση από το μηδέν (12 εποχές) | 14.473,4 | 6.935,7 | 0.102 |
| **XGBoost** | Επιβλεπόμενη εκπαίδευση (100 δένδρα) | **6.344,8** | **3.275,5** | **0.825** |

**Κομβικό Συμπέρασμα:** Το Fine-Tuning του Foundation Model μείωσε το σφάλμα κατά **54,8%** σε μόλις 24 δευτερόλεπτα προσαρμογής, ξεπερνώντας καθαρά το εκπαιδευμένο από το μηδέν LSTM κατά 6.047 kbps!

![Foundation Model Performance](../results/figures/10_foundation_model_performance.png)
*Σχήμα 10: Αποτίμηση Zero-Shot vs Fine-Tuning IBM Granite TTM και σύγκριση με XGBoost & LSTM.*

---

## 7. Σταδιακή Αφαίρεση Μεταβλητών (SHAP-Guided Feature Pruning)

### 7.1 Πειραματικά Αποτελέσματα
Καθοδηγούμενοι από το ranking του SHAP, αφαιρέθηκαν διαδοχικά οι μεταβλητές με τη μικρότερη συνεισφορά:
* **100% Χαρακτηριστικών (8 KPIs):** Όλες οι μετρικές.
* **75% Χαρακτηριστικών (6 KPIs):** Αφαίρεση `RSRP`, `CQI`.
* **50% Χαρακτηριστικών (4 KPIs):** Αφαίρεση επιπλέον των `RSRQ`, `SNR`.
* **25% Χαρακτηριστικών (2 KPIs):** Διατήρηση μόνο των `UL_bitrate`, `RSSI`.

| Στάδιο Αφαίρεσης | Διατηρούμενα KPIs | RMSE (kbps) | MAE (kbps) | Χρόνος Train (s) | Inference Latency ($\mu$s/sample) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **100% Features** | Όλα τα 8 KPIs | 6.447,1 | 3.330,9 | 0,57 | 0,50 $\mu$s |
| **75% Features** | UL, RSSI, Distance, Speed, SNR, RSRQ | **6.425,9** | **3.311,2** | 0,56 | **0,30 $\mu$s** |
| **50% Features** | UL, RSSI, Distance, Speed | 6.605,4 | 3.349,4 | 0,51 | 0,50 $\mu$s |
| **25% Features** | UL_bitrate, RSSI | 6.494,3 | 3.313,2 | **0,41** | 0,50 $\mu$s |

### 7.2 Τηλεπικοινωνιακή Σημασία για το Edge Computing (MEC)
1. **Διατήρηση Ακρίβειας:** Ακόμη και με την αφαίρεση του 75% των χαρακτηριστικών (κρατώντας μόνο `UL_bitrate` και `RSSI`), το RMSE μεταβάλλεται ανεπαίσθητα ($+0,7\%$).
2. **Μείωση Υπολογιστικού Φόρτου:** Ο χρόνος εκπαίδευσης μειώνεται κατά **28,1%** και το μέγεθος των πακέτων τηλεμετρίας που στέλνει το UE μέσω των Uplink Control Channels (PUCCH) ελαχιστοποιείται, εξοικονομώντας πολύτιμους ραδιοπόρους σηματοδοσίας.

![Feature Pruning](../results/figures/11_feature_pruning_accuracy_vs_latency.png)
*Σχήμα 11: Επίδραση του Feature Pruning στο σφάλμα πρόβλεψης, χρόνο εκπαίδευσης και latency.*

---

## 8. 5G Proactive Network Management

### 8.1 Προσομοίωση Έγκαιρης Προειδοποίησης Υποβάθμισης QoS (Threshold = 5 Mbps)
Θεωρήσαμε κατώφλι υποβάθμισης $\tau = 5.000\text{ kbps}$ (5 Mbps), κάτω από το οποίο διακόπτεται η ομαλή ροή 4K video ή παραβιάζεται το SLA του eMBB slice.

| Ορίζοντας $H$ (Lead Time $\Delta t$) | Ρυθμός Ανίχνευσης (Recall) | Ρυθμός Ψευδών Συναγερμών (False Alarm) | F1-Score | Εφαρμόσιμες Προληπτικές Ενέργειες |
| :---: | :---: | :---: | :---: | :--- |
| **1 δευτερόλεπτο** | **91,6%** | **6,4%** | **0.929** | Predictive Beamforming, Fast Intra-Cell Handover |
| **3 δευτερόλεπτα** | **88,3%** | 7,8% | **0.905** | Dynamic PRB Scheduling, MEC Video ABR Downgrade |
| **5 δευτερόλεπτα** | **85,7%** | 7,9% | **0.890** | Target gNodeB Context Pre-Fetch, Dual Connectivity |
| **10 δευτερόλεπτα** | **81,3%** | 7,9% | **0.864** | Carrier Aggregation Reconfiguration, Slice Scaling |
| **15 δευτερόλεπτα** | **78,2%** | 7,5% | **0.847** | Core Network Path Switching, Multi-RAT Offloading |

### 8.2 Ανάλυση του Trade-Off: Ακρίβεια έναντι Διαθέσιμου Χρόνου Αντίδρασης
* **Μικρός Ορίζοντας ($\Delta t = 1-3\text{s}$):** Εξαιρετικά υψηλή ακρίβεια (Detection Rate 88-92%, False Alarms < 7%). Ιδανικός για ενέργειες στο επίπεδο του MAC/PHY layer (π.χ. ανακατανομή PRBs, beam tracking).
* **Μεγάλος Ορίζοντας ($\Delta t = 10-15\text{s}$):** Ο ρυθμός ανίχνευσης υποχωρεί στο 78-81%, ωστόσο τα 10-15 δευτερόλεπτα προσφέρουν επαρκή χρόνο για βαριές διαδικασίες του Core Network και του Edge Cloud (π.χ. προετοιμασία inter-gNB handover μέσω διεπαφής Xn, transcoding video στο MEC).

![Proactive Tradeoff](../results/figures/12_proactive_5g_early_warning_tradeoff.png)
*Σχήμα 12: Trade-off μεταξύ διαθέσιμου χρόνου αντίδρασης (Lead Time) και αξιοπιστίας πρόβλεψης.*

---

## 9. Τηλεπικοινωνιακή Αρχιτεκτονική & Ενορχήστρωση σε 5G/6G

### 9.1 Ένταξη στο 3GPP NWDAF & O-RAN RIC
1. **3GPP NWDAF (Network Data Analytics Function):**
   * Συλλέγει δεδομένα ποιότητας από το UE και το 5G Radio Access Network (gNB).
   * Φιλοξενεί τα εκπαιδευμένα μοντέλα πρόβλεψης throughput.
   * Παρέχει αναλυτικές προβλέψεις μέσω RESTful APIs (Nnwdaf_AnalyticsInfo) προς τη λειτουργία PCF (Policy Control Function) για δυναμική ρύθμιση κανόνων QoS και προς την AMF για διαχείριση κινητικότητας.
2. **O-RAN Architecture (Near-RT RIC & Non-RT RIC):**
   * **Non-RT RIC (SMO):** Εκτελεί rApps για περιοδική εκπαίδευση των μοντέλων (XGBoost, Foundation Models) και offline XAI ανάλυση.
   * **Near-RT RIC:** Φιλοξενεί xApps που εκτελούν online συμπερασμό (inference) σε χρόνο $<10\text{ ms}$ μέσω της διεπαφής E2, αποστέλλοντας προληπτικές εντολές στο Distributed Unit (O-DU) και Radio Unit (O-RU).

---

## 10. Συμπεράσματα
1. Η πρόβλεψη του downlink bitrate σε πραγματικό χρόνο είναι απόλυτα εφικτή με χρήση Machine Learning, επιτυγχάνοντας εξαιρετικό $R^2 = 0.825$ και inference latency $0,001\text{ ms}$ με XGBoost.
2. Η τεχνική TreeSHAP απέδειξε ότι το `UL_bitrate` και το `RSSI` αποτελούν τους κυρίαρχους παράγοντες, επιτρέποντας μείωση των απαιτούμενων μετρικών κατά 75% χωρίς ουσιώδη απώλεια ακρίβειας.
3. Τα Foundation Models (IBM Granite TTM) αποδεικνύουν την τεράστια ισχύ του transfer learning: με ταχύτατο fine-tuning μόλις 4 εποχών μείωσαν το σφάλμα κατά 54,8%, ξεπερνώντας κατά πολύ το κλασικό LSTM.
4. Η προληπτική ανίχνευση υποβάθμισης QoS εξασφαλίζει ποσοστά επιτυχίας $>85\%$ με προπορεία 5 δευτερολέπτων, θεμελιώνοντας την αυτόνομη διαχείριση πόρων σε δίκτυα 5G/6G.

---

## 11. Βιβλιογραφία
1. D. Raca, J. J. Quinlan, A. H. Zahran, and C. J. Sreenan, *"Beyond Throughput: a 4G LTE Dataset with Channel and Context Metrics,"* Proceedings of the 9th ACM Multimedia Systems Conference (MMSys '18), Amsterdam, Netherlands, 2018.
2. 3GPP TS 23.288, *"Architecture enhancements for 5G System (5GS) to support network data analytics services (Release 18),"* 3rd Generation Partnership Project, 2024.
3. O-RAN Alliance, *"Near-Real-Time RAN Intelligent Controller (Near-RT RIC) Architecture,"* O-RAN Working Group 3, 2023.
4. S. M. Lundberg and S.-I. Lee, *"A Unified Approach to Interpreting Model Predictions,"* Advances in Neural Information Processing Systems (NeurIPS), 2017.
5. IBM Research, *"Tiny Time Mixers: Fast and Lightweight Pretrained Models for General Time Series Forecasting,"* arXiv preprint, 2024.
6. L. Grinsztajn, E. Oyallon, and G. Varoquaux, *"Why do tree-based models still outperform deep learning on tabular data?"* Advances in Neural Information Processing Systems (NeurIPS), 2022.
"""
    md_path = DOCS_DIR / "Technical_Report_5G_Forecasting.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Saved Markdown report to {md_path}")
    return md_content


def generate_docx_report(metrics: dict):
    """Generates the professional Word Document (.docx) report."""
    doc = docx.Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Calibri"
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Title Cover Page
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_inst = p_inst.add_run("ΠΑΝΕΠΙΣΤΗΜΙΟ ΠΑΤΡΩΝ — ΤΜΗΜΑ ΜΗΧΑΝΙΚΩΝ Η/Υ & ΠΛΗΡΟΦΟΡΙΚΗΣ\nΕΡΕΥΝΗΤΙΚΟ ΚΕΝΤΡΟ ISI (ΕΡΕΥΝΗΤΙΚΟ ΙΝΣΤΙΤΟΥΤΟ ΒΙΟΜΗΧΑΝΙΚΩΝ ΣΥΣΤΗΜΑΤΩΝ)\n")
    run_inst.font.size = Pt(12)
    run_inst.font.bold = True
    run_inst.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_c = p_course.add_run("ΑΡΧΙΤΕΚΤΟΝΙΚΕΣ ΔΙΚΤΥΩΝ ΕΠΟΜΕΝΗΣ ΓΕΝΙΑΣ, ΤΕΧΝΟΛΟΓΙΕΣ ΚΑΙ ΕΦΑΡΜΟΓΕΣ\nΧΕΙΜΕΡΙΝΟ ΕΞΑΜΗΝΟ 2026-2027\n\n")
    run_c.font.size = Pt(13)
    run_c.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = p_title.add_run("ΤΕΧΝΙΚΗ ΕΚΘΕΣΗ ΥΛΟΠΟΙΗΣΗΣ PROJECT (ΘΕΜΑ 11)\n")
    run_t.font.size = Pt(22)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Πρόβλεψη Downlink Bitrate (Throughput) Με Βάση Μετρικές Ποιότητας Καναλιού & Προληπτική Διαχείριση Πόρων σε Δίκτυα 5G/6G\n")
    run_sub.font.size = Pt(15)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_auth = p_auth.add_run("Δημήτριος Τσανακτσής (Α.Μ.: 1100736)  —  Ιάσωνας Δερβενής (Α.Μ.: 1097437)\n")
    run_auth.font.size = Pt(14)
    run_auth.font.bold = True
    run_auth.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    # Metadata Box
    table_meta = doc.add_table(rows=6, cols=2)
    table_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Συγγραφείς / Ομάδα Έργου:", "Δημήτριος Τσανακτσής (Α.Μ.: 1100736), Ιάσωνας Δερβενής (Α.Μ.: 1097437)"),
        ("Επιβλέπων Καθηγητής / Ερευνητής:", "Παναγιώτης Μαράντης (pmaradis@isi.gr)"),
        ("GitHub Repository (Κώδικας):", "https://github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting"),
        ("Σύνολο Δεδομένων (Dataset):", "UCC MISL Cellular Traces (135 Traces, 174.523 δείγματα)"),
        ("Τεχνολογίες Υλοποίησης:", "Python 3.14, XGBoost, PyTorch, TreeSHAP, IBM Granite TTM"),
        ("Ημερομηνία Ολοκλήρωσης:", "Νοέμβριος 2026")
    ]
    for row_idx, (k, v) in enumerate(meta_info):
        cell_k, cell_v = table_meta.rows[row_idx].cells
        cell_k.paragraphs[0].add_run(k).bold = True
        cell_v.paragraphs[0].add_run(v)
        set_cell_background(cell_k, "F2F4F7")
        set_cell_background(cell_v, "FAFAFA")

    doc.add_page_break()

    # Section 1
    h1 = doc.add_heading("1. Εισαγωγή & Τηλεπικοινωνιακή Σημασία", level=1)
    doc.add_paragraph(
        "Στα σύγχρονα κυψελωτά δίκτυα πέμπτης και έκτης γενιάς (5G NR / 6G), ο ρυθμός μετάδοσης δεδομένων λήψης "
        "(Downlink Bitrate / Throughput) παρουσιάζει ραγδαίες διακυμάνσεις λόγω της κινητικότητας του χρήστη, "
        "της χρήσης υψηλών ζωνών συχνοτήτων (mmWave/sub-6GHz), της διαλείπουσας σκίασης (shadowing) και της μεταβαλλόμενης φόρτισης του σταθμού βάσης."
    )
    doc.add_paragraph(
        "Η προληπτική (proactive) πρόβλεψη του Throughput με ορίζοντα λίγων δευτερολέπτων επιτρέπει τη δυναμική δέσμευση "
        "ραδιοπόρων (PRBs), την αποφυγή Radio Link Failure (RLF) μέσω predictive handover, και την προσαρμογή βίντεο ροής (ABR/DASH) "
        "πριν επέλθει υποβάθμιση του Quality of Experience (QoE)."
    )

    # Section 2
    doc.add_heading("2. Περιγραφή & Προεπεξεργασία Δεδομένων", level=1)
    doc.add_paragraph(
        "Χρησιμοποιήθηκε το επίσημο σύνολο δεδομένων κυψελωτών καταγραφών UCC MISL (Raca et al.), "
        "το οποίο περιέχει 135 πραγματικές συνεδρίες κινητικότητας (174.523 δείγματα ανά 1s) για πέντε σενάρια: "
        "Car (75.874), Train (38.976), Pedestrian (33.629), Static (15.261) και Bus (10.783)."
    )
    doc.add_paragraph(
        "Εφαρμόστηκε συνεδριακός καθαρισμός (forward/backward fill ανά trace_id), αφαίρεση ακραίων τιμών και κανονικοποίηση "
        "με StandardScaler προσαρμοσμένο αποκλειστικά στο σύνολο εκπαίδευσης (80% των traces, 131.370 δείγματα). "
        "Το σύνολο δοκιμής (20% των traces, 43.153 δείγματα) διατηρήθηκε πλήρως απομονωμένο."
    )

    # Add Figure 1 & 2
    if (FIGURES_DIR / "01_eda_distributions.png").exists():
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(str(FIGURES_DIR / "01_eda_distributions.png"), width=Inches(6.0))
        p_cap = doc.add_paragraph("Σχήμα 1: Κατανομές ραδιοδεικτών καναλιού και Throughput.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True

    # Section 3
    doc.add_heading("3. Πρόβλεψη με XGBoost Regressor (Grid Search)", level=1)
    doc.add_paragraph(
        "Εκπαιδεύτηκε το μοντέλο XGBoost σε ολισθαίνοντα παράθυρα για πολλαπλούς συνδυασμούς "
        "lookback windows (L = 5, 10, 20, 30s) και prediction horizons (H = 1, 3, 5, 10s)."
    )
    doc.add_paragraph(
        "Για τον βασικό ορίζοντα H=1s και L=10s, το μοντέλο επέτυχε RMSE 6.344,8 kbps (~6.34 Mbps), "
        "MAE 3.275,5 kbps και εξαιρετικό συντελεστή προσδιορισμού R² = 0.825, με ανεπαίσθητο inference latency 0,001 ms/δείγμα."
    )

    if (FIGURES_DIR / "03_xgboost_horizons_lookback.png").exists():
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(str(FIGURES_DIR / "03_xgboost_horizons_lookback.png"), width=Inches(6.0))
        p_cap = doc.add_paragraph("Σχήμα 2: Αξιολόγηση ευαισθησίας Lookback και Horizons & Τροχιά Throughput.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True

    # Section 4
    doc.add_heading("4. Επεξηγήσιμη Τεχνητή Νοημοσύνη (Explainable AI - TreeSHAP)", level=1)
    doc.add_paragraph(
        "Μέσω της τεχνικής TreeSHAP υπολογίστηκαν οι τιμές Shapley για 1.500 δείγματα δοκιμής. "
        "Αποδείχθηκε ότι το UL_bitrate και το RSSI αποτελούν τους κυρίαρχους ραδιοδείκτες (9.259 kbps και 1.102 kbps μέση επιρροή αντίστοιχα), "
        "ακολουθούμενοι από την απόσταση από τον σταθμό βάσης (ServingCell_Distance) και την ταχύτητα του οχήματος (Speed)."
    )

    if (FIGURES_DIR / "04_shap_summary_beeswarm.png").exists():
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(str(FIGURES_DIR / "04_shap_summary_beeswarm.png"), width=Inches(5.8))
        p_cap = doc.add_paragraph("Σχήμα 3: TreeSHAP Beeswarm Plot (Κατανομή επιρροής χαρακτηριστικών).")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True

    # Section 5
    doc.add_heading("5. Πρόβλεψη Χρονοσειρών με PyTorch LSTM", level=1)
    doc.add_paragraph(
        "Αναπτύχθηκε νευρωνικό δίκτυο 2 επιπέδων LSTM με 64 κρυφές μονάδες και Dropout 0.2, "
        "με είσοδο παράθυρο 64 δευτερολέπτων. Το LSTM επέτυχε RMSE 14.473,4 kbps και MAE 6.935,7 kbps. "
        "Το XGBoost υπερίσχυσε καθαρά τόσο σε ακρίβεια (56,2% χαμηλότερο RMSE) όσο και σε ταχύτητα συμπερασμού (100x ταχύτερο), "
        "επιβεβαιώνοντας τη βιβλιογραφία σχετικά με την υπεροχή δενδροειδών μοντέλων σε tabular κυψελωτά δεδομένα."
    )

    if (FIGURES_DIR / "09_model_comparisons.png").exists():
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(str(FIGURES_DIR / "09_model_comparisons.png"), width=Inches(6.0))
        p_cap = doc.add_paragraph("Σχήμα 4: Συγκριτική αποτίμηση XGBoost έναντι PyTorch LSTM.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True

    # Section 6
    doc.add_heading("6. Foundation Models: IBM Granite Tiny Time Mixer (TTM)", level=1)
    doc.add_paragraph(
        "Υλοποιήθηκε η αρχιτεκτονική Patch-based MLP-Mixer του IBM Granite TTM. "
        "Σε Zero-Shot λειτουργία (χωρίς εκπαίδευση στο target dataset), το μοντέλο σημείωσε RMSE 18.641 kbps. "
        "Με ταχύτατο Fine-Tuning μόλις 4 εποχών (24 δευτερόλεπτα), το RMSE μειώθηκε κατά 54,8% στα 8.426 kbps (R² = 0.695), "
        "ξεπερνώντας δραματικά το LSTM."
    )

    if (FIGURES_DIR / "10_foundation_model_performance.png").exists():
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(str(FIGURES_DIR / "10_foundation_model_performance.png"), width=Inches(6.0))
        p_cap = doc.add_paragraph("Σχήμα 5: Αποτίμηση Zero-Shot έναντι Fine-Tuned IBM Granite TTM.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True

    # Section 7
    doc.add_heading("7. Σταδιακή Αφαίρεση Μεταβλητών & Edge Latency", level=1)
    doc.add_paragraph(
        "Βάσει της κατάταξης SHAP, αφαιρέθηκαν σταδιακά τα λιγότερο σημαντικά χαρακτηριστικά (100% -> 75% -> 50% -> 25%). "
        "Η διατήρηση μόνο των 2 κορυφαίων δεικτών (UL_bitrate, RSSI) διατήρησε το RMSE στα 6.494 kbps (+0,7% σφάλμα), "
        "μειώνοντας τον χρόνο εκπαίδευσης κατά 28% και περιορίζοντας δραστικά το uplink signaling overhead του τερματικού."
    )

    if (FIGURES_DIR / "11_feature_pruning_accuracy_vs_latency.png").exists():
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(str(FIGURES_DIR / "11_feature_pruning_accuracy_vs_latency.png"), width=Inches(6.0))
        p_cap = doc.add_paragraph("Σχήμα 6: Επίδραση Feature Pruning στην ακρίβεια και το latency.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True

    # Section 8
    doc.add_heading("8. 5G Proactive Network Management & Trade-Offs", level=1)
    doc.add_paragraph(
        "Προσομοιώθηκε μηχανισμός έγκαιρης προειδοποίησης υποβάθμισης QoS (κατώφλι 5 Mbps). "
        "Για ορίζοντα 1 δευτερολέπτου, το μοντέλο ανιχνεύει το 91,6% των υποβαθμίσεων με μόλις 6,4% ψευδείς συναγερμούς (F1 = 0.929). "
        "Ακόμη και σε ορίζοντα 5 δευτερολέπτων, ο ρυθμός ανίχνευσης παραμένει στο 85,7% (F1 = 0.890), παρέχοντας υπεραρκετό χρόνο "
        "για προληπτικό handover inter-gNB, δέσμευση φάσματος και προσαρμογή MEC ABR Video."
    )

    if (FIGURES_DIR / "12_proactive_5g_early_warning_tradeoff.png").exists():
        doc.add_paragraph().alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(str(FIGURES_DIR / "12_proactive_5g_early_warning_tradeoff.png"), width=Inches(6.0))
        p_cap = doc.add_paragraph("Σχήμα 7: Trade-off διαθέσιμου χρόνου αντίδρασης και αξιοπιστίας πρόβλεψης.")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.italic = True

    # Section 9 & 10
    doc.add_heading("9. Συμπεράσματα", level=1)
    doc.add_paragraph(
        "Η εργασία απέδειξε την υψηλή αξιοπιστία της πρόβλεψης throughput σε δίκτυα 5G/6G. "
        "Ο συνδυασμός XGBoost και Foundation Models (IBM Granite TTM) με τεχνικές Explainable AI "
        "προσφέρει τη βάση για αυτόνομη ενορχήστρωση στο O-RAN Near-RT RIC και στο 3GPP NWDAF."
    )

    docx_path = DOCS_DIR / "Technical_Report_5G_Forecasting.docx"
    doc.save(str(docx_path))
    print(f"Saved Word Document report to {docx_path}")
    return docx_path


class NumberedCanvas(canvas.Canvas):
    """Adds running headers and footers with Page X of Y."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont(PDF_FONT_REG, 9)
        self.setFillColor(colors.HexColor("#555555"))

        # Don't draw headers/footers on cover page
        if self._pageNumber > 1:
            # Header
            self.drawString(54, 750, "5G Downlink Bitrate Forecasting & Proactive QoS Management — Τεχνική Έκθεση")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

            # Footer
            page_text = f"Σελίδα {self._pageNumber} από {page_count}"
            self.drawRightString(558, 40, page_text)
            self.drawString(54, 40, "Δ. Τσανακτσής (1100736) & Ι. Δερβενής (1097437) — Πανεπιστήμιο Πατρών / ISI (Θέμα 11)")
            self.line(54, 52, 558, 52)

        self.restoreState()


def generate_pdf_report(metrics: dict):
    """Generates the professional PDF report using ReportLab."""
    pdf_path = DOCS_DIR / "Technical_Report_5G_Forecasting.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=60,
        bottomMargin=60
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName=PDF_FONT_BOLD,
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#003366"),
        alignment=1,
        spaceAfter=15
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName=PDF_FONT_REG,
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#333333"),
        alignment=1,
        spaceAfter=20
    )

    author_style = ParagraphStyle(
        "CoverAuthors",
        parent=styles["Normal"],
        fontName=PDF_FONT_BOLD,
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#003366"),
        alignment=1,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Heading1"],
        fontName=PDF_FONT_BOLD,
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#003366"),
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName=PDF_FONT_REG,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#222222"),
        spaceAfter=8
    )

    caption_style = ParagraphStyle(
        "Caption_Custom",
        parent=styles["Normal"],
        fontName=PDF_FONT_ITALIC,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#555555"),
        alignment=1,
        spaceAfter=12
    )

    story = []

    # Cover Page
    story.append(Spacer(1, 35))
    story.append(Paragraph("ΠΑΝΕΠΙΣΤΗΜΙΟ ΠΑΤΡΩΝ — ΤΜΗΜΑ ΜΗΧΑΝΙΚΩΝ Η/Υ & ΠΛΗΡΟΦΟΡΙΚΗΣ", subtitle_style))
    story.append(Paragraph("ΕΡΕΥΝΗΤΙΚΟ ΙΝΣΤΙΤΟΥΤΟ ΒΙΟΜΗΧΑΝΙΚΩΝ ΣΥΣΤΗΜΑΤΩΝ (ISI)", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("ΑΡΧΙΤΕΚΤΟΝΙΚΕΣ ΔΙΚΤΥΩΝ ΕΠΟΜΕΝΗΣ ΓΕΝΙΑΣ, ΤΕΧΝΟΛΟΓΙΕΣ ΚΑΙ ΕΦΑΡΜΟΓΕΣ", ParagraphStyle("C", parent=subtitle_style, fontName=PDF_FONT_BOLD, fontSize=13)))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#003366"), spaceBefore=10, spaceAfter=25))

    story.append(Paragraph("ΤΕΧΝΙΚΗ ΕΚΘΕΣΗ PROJECT (ΘΕΜΑ 11)", title_style))
    story.append(Paragraph("Πρόβλεψη Downlink Bitrate (Throughput) Με Βάση Μετρικές Ποιότητας Καναλιού & Προληπτική Διαχείριση Πόρων σε Δίκτυα 5G/6G", subtitle_style))
    story.append(Paragraph("Δημήτριος Τσανακτσής (Α.Μ.: 1100736)  |  Ιάσωνας Δερβενής (Α.Μ.: 1097437)", author_style))
    story.append(Spacer(1, 15))

    # Info Table
    info_data = [
        [Paragraph("<b>Συγγραφείς:</b>", body_style), Paragraph("Δημήτριος Τσανακτσής (Α.Μ.: 1100736)<br/>Ιάσωνας Δερβενής (Α.Μ.: 1097437)", body_style)],
        [Paragraph("<b>Επιβλέπων:</b>", body_style), Paragraph("Παναγιώτης Μαράντης (pmaradis@isi.gr)", body_style)],
        [Paragraph("<b>GitHub Repository:</b>", body_style), Paragraph("https://github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting", body_style)],
        [Paragraph("<b>Σύνολο Δεδομένων:</b>", body_style), Paragraph("UCC MISL Cellular Traces (135 Traces, 174.523 δείγματα)", body_style)],
        [Paragraph("<b>Τεχνολογίες:</b>", body_style), Paragraph("Python 3.14, XGBoost, PyTorch, TreeSHAP, IBM Granite TTM", body_style)],
        [Paragraph("<b>Ημερομηνία:</b>", body_style), Paragraph("Νοέμβριος 2026", body_style)]
    ]
    t_info = Table(info_data, colWidths=[150, 330])
    t_info.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F2F4F7")),
        ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#FAFAFA")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D5DD")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t_info)
    story.append(PageBreak())

    # Section 1
    story.append(Paragraph("1. Εισαγωγή & Τηλεπικοινωνιακή Σημασία", h1_style))
    story.append(Paragraph(
        "Στα σύγχρονα κυψελωτά δίκτυα 5G NR και 6G, ο ρυθμός μετάδοσης δεδομένων λήψης (Downlink Bitrate) "
        "χαρακτηρίζεται από έντονη μεταβλητότητα. Η κινητικότητα του χρήστη, οι απώλειες διάδοσης σε υψηλές συχνότητες (sub-6GHz, mmWave) "
        "και η στοχαστική φόρτιση των κυψελών απαιτούν μετάβαση από την αναδρομική αντίδραση στην προληπτική (proactive) λήψη αποφάσεων.",
        body_style
    ))
    story.append(Paragraph(
        "Η έγκαιρη πρόβλεψη επιτρέπει την εγγύηση SLAs σε network slices (eMBB, URLLC), την αποφυγή Radio Link Failures (RLF) μέσω "
        "predictive handovers, και τη βελτιστοποίηση video streaming στο Multi-Access Edge Computing (MEC).",
        body_style
    ))

    # Section 2
    story.append(Paragraph("2. Προεπεξεργασία Δεδομένων & Σενάρια Κίνησης", h1_style))
    story.append(Paragraph(
        "Αξιοποιήθηκαν 135 πραγματικές συνεδρίες κινητικότητας (174.523 δείγματα) από το UCC MISL dataset "
        "σε 5 σενάρια: Car (75.874), Train (38.976), Pedestrian (33.629), Static (15.261) και Bus (10.783). "
        "Πραγματοποιήθηκε session-aware split (80% train / 20% test traces) για αποτροπή data leakage.",
        body_style
    ))

    if (FIGURES_DIR / "01_eda_distributions.png").exists():
        story.append(Image(str(FIGURES_DIR / "01_eda_distributions.png"), width=480, height=270))
        story.append(Paragraph("Σχήμα 1: Κατανομές ραδιοδεικτών καναλιού και Throughput.", caption_style))

    # Section 3
    story.append(Paragraph("3. Πρόβλεψη με XGBoost Regressor (Lookback & Horizon Grid)", h1_style))
    story.append(Paragraph(
        "Εξετάστηκαν ολισθαίνοντα παράθυρα L in {5, 10, 20, 30}s και ορίζοντες H in {1, 3, 5, 10}s. "
        "Για L=10s και H=1s, το XGBoost πέτυχε εξαιρετική απόδοση: RMSE = 6.344,8 kbps, MAE = 3.275,5 kbps και R² = 0.825, "
        "με αστραπιαίο χρόνο συμπερασμού 0,001 ms/δείγμα.",
        body_style
    ))

    if (FIGURES_DIR / "03_xgboost_horizons_lookback.png").exists():
        story.append(Image(str(FIGURES_DIR / "03_xgboost_horizons_lookback.png"), width=480, height=270))
        story.append(Paragraph("Σχήμα 2: Αξιολόγηση Lookbacks & Horizons και πραγματική vs προβλεπόμενη τροχιά.", caption_style))

    # Section 4
    story.append(Paragraph("4. Επεξηγήσιμη Τεχνητή Νοημοσύνη (TreeSHAP)", h1_style))
    story.append(Paragraph(
        "Μέσω TreeSHAP αποκαλύφθηκε ότι το UL_bitrate και το RSSI κυριαρχούν στην πρόβλεψη "
        "(μέση επιρροή 9.259 kbps και 1.102 kbps αντίστοιχα), ακολουθούμενα από την απόσταση ServingCell_Distance και την ταχύτητα Speed.",
        body_style
    ))

    if (FIGURES_DIR / "04_shap_summary_beeswarm.png").exists():
        story.append(Image(str(FIGURES_DIR / "04_shap_summary_beeswarm.png"), width=460, height=260))
        story.append(Paragraph("Σχήμα 3: TreeSHAP Beeswarm Plot.", caption_style))

    # Section 5
    story.append(Paragraph("5. Πρόβλεψη με Deep Learning (PyTorch LSTM)", h1_style))
    story.append(Paragraph(
        "Το 2-layer LSTM (lookback 64) πέτυχε RMSE 14.473 kbps. Το XGBoost υπερίσχυσε καθαρά "
        "(56,2% χαμηλότερο σφάλμα, 100x ταχύτερο training και inference), αποδεικνύοντας την υπεροχή των Gradient Boosted Trees σε κυψελωτές χρονοσειρές.",
        body_style
    ))

    if (FIGURES_DIR / "09_model_comparisons.png").exists():
        story.append(Image(str(FIGURES_DIR / "09_model_comparisons.png"), width=480, height=180))
        story.append(Paragraph("Σχήμα 4: Συγκριτική αποτίμηση XGBoost έναντι PyTorch LSTM.", caption_style))

    # Section 6
    story.append(Paragraph("6. Foundation Models: IBM Granite Tiny Time Mixer (TTM)", h1_style))
    story.append(Paragraph(
        "Το IBM Granite TTM σε Zero-Shot σημείωσε RMSE 18.641 kbps. Μετά από ταχύτατο Fine-Tuning 4 εποχών, "
        "το RMSE μειώθηκε κατά 54,8% στα 8.426 kbps (R² = 0.695), ξεπερνώντας κατά 6.047 kbps το εκπαιδευμένο LSTM.",
        body_style
    ))

    if (FIGURES_DIR / "10_foundation_model_performance.png").exists():
        story.append(Image(str(FIGURES_DIR / "10_foundation_model_performance.png"), width=480, height=190))
        story.append(Paragraph("Σχήμα 5: Αποτίμηση Zero-Shot vs Fine-Tuned Foundation Model.", caption_style))

    # Section 7
    story.append(Paragraph("7. Σταδιακή Αφαίρεση Μεταβλητών & Edge Latency", h1_style))
    story.append(Paragraph(
        "Η αφαίρεση του 75% των χαρακτηριστικών (διατηρώντας μόνο UL_bitrate και RSSI) διατήρησε το RMSE στα 6.494 kbps "
        "(μόλις +0,7% μεταβολή), μειώνοντας τον χρόνο εκπαίδευσης κατά 28% και ελαχιστοποιώντας το telemetry signaling overhead.",
        body_style
    ))

    if (FIGURES_DIR / "11_feature_pruning_accuracy_vs_latency.png").exists():
        story.append(Image(str(FIGURES_DIR / "11_feature_pruning_accuracy_vs_latency.png"), width=480, height=180))
        story.append(Paragraph("Σχήμα 6: Επίδραση Feature Pruning στο Edge Latency.", caption_style))

    # Section 8
    story.append(Paragraph("8. 5G Proactive Network Management", h1_style))
    story.append(Paragraph(
        "Στην ανίχνευση υποβάθμισης QoS (< 5 Mbps), το σύστημα πετυχαίνει Recall 91,6% (F1 = 0.929) σε ορίζοντα 1s "
        "και Recall 85,7% (F1 = 0.890) σε ορίζοντα 5s, παρέχοντας αξιόπιστο χρόνο για προληπτικό handover, dynamic PRB reservation και MEC ABR video adaptation.",
        body_style
    ))

    if (FIGURES_DIR / "12_proactive_5g_early_warning_tradeoff.png").exists():
        story.append(Image(str(FIGURES_DIR / "12_proactive_5g_early_warning_tradeoff.png"), width=480, height=190))
        story.append(Paragraph("Σχήμα 7: Trade-off χρόνου προειδοποίησης και αξιοπιστίας πρόβλεψης.", caption_style))

    # Section 9
    story.append(Paragraph("9. Συμπεράσματα", h1_style))
    story.append(Paragraph(
        "Η εργασία επιβεβαίωσε την εφικτότητα προληπτικής διαχείρισης σε δίκτυα 5G/6G μέσω ML και Foundation Models, "
        "παρέχοντας μια ολοκληρωμένη αρχιτεκτονική συμβατή με το 3GPP NWDAF και το O-RAN Near-RT RIC.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Saved PDF report to {pdf_path}")
    return pdf_path


def run_all_report_generation():
    summary_path = RESULTS_DIR / "metrics_summary.json"
    metrics = {}
    if summary_path.exists():
        with open(summary_path, "r", encoding="utf-8") as f:
            metrics = json.load(f)

    print("Generating Academic Technical Reports...")
    generate_markdown_report(metrics)
    generate_docx_report(metrics)
    generate_pdf_report(metrics)
    print("All reports generated successfully!")


if __name__ == "__main__":
    run_all_report_generation()
