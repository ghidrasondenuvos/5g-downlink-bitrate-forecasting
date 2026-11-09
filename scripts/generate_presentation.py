"""
Presentation Deck Generator Script.
Generates an executive, professional PowerPoint slide deck (presentation/Downlink_Bitrate_Forecasting_5G.pptx)
for the 20-minute Intermediate and Final Examinations.
"""

import sys
import json
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import BASE_DIR, PRESENTATION_DIR, FIGURES_DIR, RESULTS_DIR


# Corporate / Academic Color Palette
COLOR_NAVY = RGBColor(0x00, 0x33, 0x66)       # #003366 Primary
COLOR_BLUE = RGBColor(0x1F, 0x49, 0x7D)       # #1F497D Secondary
COLOR_LIGHT_BG = RGBColor(0xF4, 0xF6, 0xF9)   # #F4F6F9 Background
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_DARK_TEXT = RGBColor(0x22, 0x22, 0x22)
COLOR_GRAY = RGBColor(0x7F, 0x8C, 0x8D)
COLOR_ACCENT = RGBColor(0x27, 0xAE, 0x60)     # Green accent


def create_blank_slide_with_header(prs, title_text, category="5G NETWORK ARCHITECTURES & ML"):
    """Creates a standard content slide with an elegant header and footer banner."""
    slide_layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(slide_layout)

    # Top Header Banner
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_GRAY

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY

    # Thin separator line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_BLUE
    line.line.color.rgb = COLOR_BLUE

    # Footer
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.4))
    tf_f = footer_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "Πανεπιστήμιο Πατρών / ISI | Θέμα 11: 5G Downlink Bitrate Forecasting | Χειμερινό Εξάμηνο 2026-2027"
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = COLOR_GRAY

    return slide


def generate_presentation_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # ----------------------------------------------------
    # SLIDE 1: Title Slide (Dark Navy Elegance)
    # ----------------------------------------------------
    slide_layout = prs.slide_layouts[6]
    slide1 = prs.slides.add_slide(slide_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.fill.background()

    tbox1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.0))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p_uni = tf1.paragraphs[0]
    p_uni.text = "ΠΑΝΕΠΙΣΤΗΜΙΟ ΠΑΤΡΩΝ — ΤΜΗΜΑ ΜΗΧΑΝΙΚΩΝ Η/Υ & ΠΛΗΡΟΦΟΡΙΚΗΣ\nΕΡΕΥΝΗΤΙΚΟ ΙΝΣΤΙΤΟΥΤΟ ΒΙΟΜΗΧΑΝΙΚΩΝ ΣΥΣΤΗΜΑΤΩΝ (ISI)"
    p_uni.font.size = Pt(13)
    p_uni.font.bold = True
    p_uni.font.color.rgb = RGBColor(0xBD, 0xC3, 0xC7)

    p_main = tf1.add_paragraph()
    p_main.text = "\nΠρόβλεψη Downlink Bitrate (Throughput)\nΜε Βάση Μετρικές Ποιότητας Καναλιού"
    p_main.font.size = Pt(28)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_WHITE

    p_sub = tf1.add_paragraph()
    p_sub.text = "Προληπτική Διαχείριση Πόρων σε Δίκτυα 5G/6G μέσω ML, Explainable AI & Foundation Models\n"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(0x34, 0x98, 0xDB)

    p_auth = tf1.add_paragraph()
    p_auth.text = "Μάθημα: Αρχιτεκτονικές Δικτύων Επόμενης Γενιάς, Τεχνολογίες και Εφαρμογές (Θέμα 11)\nΕπιβλέπων: Παναγιώτης Μαράντης (pmaradis@isi.gr) | Χειμερινό Εξάμηνο 2026-2027\nGitHub Repository: https://github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting"
    p_auth.font.size = Pt(12)
    p_auth.font.color.rgb = RGBColor(0xEC, 0xF0, 0xF1)

    # ----------------------------------------------------
    # SLIDE 2: Executive Summary & Table of Contents
    # ----------------------------------------------------
    slide2 = create_blank_slide_with_header(prs, "Περιεχόμενα Παρουσίασης & Δομή Έργου")
    tbox2 = slide2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf2 = tbox2.text_frame
    tf2.word_wrap = True

    sections = [
        ("01", "Τηλεπικοινωνιακή Σημασία & Στοχαστική Συμπεριφορά 5G", "Γιατί η πρόβλεψη Throughput είναι αναγκαία για SLA, Handover & Slicing."),
        ("02", "Προεπεξεργασία & Ανάλυση Συνεδριών Κινητικότητας", "Καθαρισμός, κανονικοποίηση και session-aware split σε 174.523 δείγματα (135 traces)."),
        ("03", "Πρόβλεψη με XGBoost Regressor (Lookbacks & Horizons)", "Αξιολόγηση παραμέτρων εισόδου L ∈ [5,30]s και οριζόντων H ∈ [1,10]s."),
        ("04", "Επεξηγήσιμη Τεχνητή Νοημοσύνη (TreeSHAP XAI)", "Ανάλυση σπουδαιότητας ραδιοδεικτών, beeswarm plots και εξαρτήσεις καναλιού."),
        ("05", "Πρόβλεψη με Deep Learning (PyTorch LSTM)", "Αρχιτεκτονική χρονοσειρών 2 επιπέδων και σύγκριση απόδοσης με XGBoost."),
        ("06", "Foundation Models (IBM Granite Tiny Time Mixer - TTM)", "Zero-Shot συμπερασμός και ταχύτατο Fine-Tuning με 54,8% μείωση σφάλματος."),
        ("07", "Σταδιακή Αφαίρεση Μεταβλητών & Edge Latency", "Feature pruning βάσει SHAP και βελτιστοποίηση uplink control signaling."),
        ("08", "5G Proactive Network Management (QoS Early Warning)", "Προληπτική ανίχνευση υποβάθμισης (Recall 91,6%) και ένταξη στο 3GPP NWDAF / O-RAN RIC.")
    ]

    for num, title, desc in sections:
        p = tf2.add_paragraph()
        r_num = p.add_run()
        r_num.text = f"[{num}]  {title} — "
        r_num.font.bold = True
        r_num.font.size = Pt(12)
        r_num.font.color.rgb = COLOR_NAVY
        r_desc = p.add_run()
        r_desc.text = desc
        r_desc.font.size = Pt(11)
        r_desc.font.color.rgb = COLOR_DARK_TEXT

    # ----------------------------------------------------
    # SLIDE 3: Problem Statement: Why Throughput Forecasting?
    # ----------------------------------------------------
    slide3 = create_blank_slide_with_header(prs, "1. Τηλεπικοινωνιακή Σημασία της Πρόβλεψης στα Δίκτυα 5G/6G")
    tbox3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.8))
    tf3 = tbox3.text_frame
    tf3.word_wrap = True

    pts3 = [
        "Στοχαστικότητα Ασύρματου Καναλιού: mmWave / sub-6GHz, διαλείπουσα σκίαση (shadowing), fast fading και έντονη κινητικότητα χρήστη.",
        "Περιορισμοί Αναδρομικής Διαχείρισης (Reactive): Η αντίδραση κατόπιν εορτής οδηγεί σε Radio Link Failure (RLF), buffer underruns σε 4K streaming και παραβίαση SLA.",
        "Οφέλη Προληπτικής Πρόβλεψης (Proactive):",
        "  • Predictive Handover: Προ-συγχρονισμός με candidate target gNB.",
        "  • Network Slicing: Δυναμική κράτηση Physical Resource Blocks (PRBs) για eMBB & URLLC.",
        "  • MEC Video Transcoding: Προληπτική προσαρμογή ABR bitrate.",
        "  • Dual Connectivity (EN-DC / NR-DC): Έγκαιρη δρομολόγηση πακέτων."
    ]
    for pt in pts3:
        p = tf3.add_paragraph()
        p.text = pt
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_after = Pt(6)

    # Add diagram or callout box on right
    cbox3 = slide3.shapes.add_textbox(Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.8))
    tf_c = cbox3.text_frame
    tf_c.word_wrap = True
    p_b = tf_c.paragraphs[0]
    p_b.text = "ΑΡΧΙΤΕΚΤΟΝΙΚΗ ΠΡΟΛΗΠΤΙΚΗΣ ΔΙΑΧΕΙΡΙΣΗΣ"
    p_b.font.bold = True
    p_b.font.size = Pt(13)
    p_b.font.color.rgb = COLOR_BLUE

    steps = [
        "1. Real-time Telemetry: Συλλογή RSRP, RSRQ, SNR, CQI, RSSI ανά 1s.",
        "2. ML/DL Engine: Πρόβλεψη Throughput (DL_bitrate) για τα επόμενα 1-15 δευτερόλεπτα.",
        "3. Anomaly & SLA Predictor: Έγκαιρος εντοπισμός επικείμενης πτώσης κάτω από το όριο (π.χ. < 5 Mbps).",
        "4. Proactive Execution: Εντολή σε Near-RT RIC / MAC Scheduler πριν επηρεαστεί ο τελικός χρήστης."
    ]
    for s in steps:
        p = tf_c.add_paragraph()
        p.text = s
        p.font.size = Pt(11)
        p.space_after = Pt(8)

    # ----------------------------------------------------
    # SLIDE 4: Dataset & Mobility Scenarios
    # ----------------------------------------------------
    slide4 = create_blank_slide_with_header(prs, "2. Περιγραφή & Ανάλυση Δεδομένων (UCC MISL Dataset)")
    if (FIGURES_DIR / "01_eda_distributions.png").exists():
        slide4.shapes.add_picture(str(FIGURES_DIR / "01_eda_distributions.png"), Inches(0.8), Inches(1.8), width=Inches(7.0))

    tbox4 = slide4.shapes.add_textbox(Inches(8.1), Inches(1.8), Inches(4.5), Inches(4.8))
    tf4 = tbox4.text_frame
    tf4.word_wrap = True
    p = tf4.paragraphs[0]
    p.text = "ΧΑΡΑΚΤΗΡΙΣΤΙΚΑ DATASET"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_NAVY

    ds_info = [
        "135 κυψελωτές καταγραφές (traces).",
        "174.523 δείγματα (granularity 1s, >48,5 ώρες).",
        "5 Σενάρια Κινητικότητας:",
        "  • Car (αυτοκίνητο): 75.874 δείγματα",
        "  • Train (τρένο): 38.976 δείγματα",
        "  • Pedestrian (πεζός): 33.629 δείγματα",
        "  • Static (ακίνητος): 15.261 δείγματα",
        "  • Bus (λεωφορείο): 10.783 δείγματα",
        "Βασικές Μετρικές:",
        "  • Throughput: Mean 10,8 Mbps, Max 173 Mbps",
        "  • Signal: RSRP (-140 to -44 dBm), CQI (1-15)"
    ]
    for inf in ds_info:
        p = tf4.add_paragraph()
        p.text = inf
        p.font.size = Pt(10)
        p.space_after = Pt(3)

    # ----------------------------------------------------
    # SLIDE 5: Data Preprocessing & Session-Aware Split
    # ----------------------------------------------------
    slide5 = create_blank_slide_with_header(prs, "2. Προεπεξεργασία & Αποτροπή Data Leakage")
    if (FIGURES_DIR / "02_eda_mobility_comparison.png").exists():
        slide5.shapes.add_picture(str(FIGURES_DIR / "02_eda_mobility_comparison.png"), Inches(0.8), Inches(1.8), width=Inches(7.2))

    tbox5 = slide5.shapes.add_textbox(Inches(8.2), Inches(1.8), Inches(4.3), Inches(4.8))
    tf5 = tbox5.text_frame
    tf5.word_wrap = True
    p = tf5.paragraphs[0]
    p.text = "ΜΕΘΟΔΟΛΟΓΙΑ ΠΡΟΕΠΕΞΕΡΓΑΣΙΑΣ"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_NAVY

    prep_steps = [
        "1. Διαχείριση Missing Values: Μετατροπή '-' σε NaN, ενδο-συνεδριακό ffill/bfill ανά trace_id.",
        "2. Session-Aware Split: Διαχωρισμός σε επίπεδο ολόκληρων traces:",
        "  • Train: 80% (131.370 δείγματα σε 106 traces)",
        "  • Test: 20% (43.153 δείγματα σε 29 traces)",
        "  • Μηδενικό data leakage μεταξύ χρονικά συνεχόμενων σημείων!",
        "3. Κανονικοποίηση (StandardScaler): Fit αποκλειστικά στο train set, transform στο test set."
    ]
    for ps in prep_steps:
        p = tf5.add_paragraph()
        p.text = ps
        p.font.size = Pt(10)
        p.space_after = Pt(5)

    # ----------------------------------------------------
    # SLIDE 6: XGBoost Regressor & Sensitivity Analysis
    # ----------------------------------------------------
    slide6 = create_blank_slide_with_header(prs, "3. Μοντέλο Μηχανικής Μάθησης (XGBoost Regressor)")
    if (FIGURES_DIR / "03_xgboost_horizons_lookback.png").exists():
        slide6.shapes.add_picture(str(FIGURES_DIR / "03_xgboost_horizons_lookback.png"), Inches(0.8), Inches(1.8), width=Inches(7.5))

    tbox6 = slide6.shapes.add_textbox(Inches(8.5), Inches(1.8), Inches(4.1), Inches(4.8))
    tf6 = tbox6.text_frame
    tf6.word_wrap = True
    p = tf6.paragraphs[0]
    p.text = "ΑΠΟΤΕΛΕΣΜΑΤΑ GRID SEARCH"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_NAVY

    grid_pts = [
        "Lookbacks (L): 5, 10, 20, 30 δείγματα.",
        "Horizons (H): 1, 3, 5, 10 βήματα ahead.",
        "Βέλτιστη Απόδοση (L=10, H=1):",
        "  • RMSE: 6.344,8 kbps (~6,34 Mbps)",
        "  • MAE: 3.275,5 kbps (~3,27 Mbps)",
        "  • R² Score: 0.825 (εξαιρετικό fit)",
        "  • Train Time: 1,3 δευτερόλεπτα",
        "  • Inference: 0,001 ms/δείγμα!",
        "Συμπέρασμα:",
        "Η αύξηση του lookback πέραν του 10 προσφέρει <0.2% βελτίωση, ενώ το σφάλμα αυξάνεται μονοτονικά με τον ορίζοντα H."
    ]
    for gp in grid_pts:
        p = tf6.add_paragraph()
        p.text = gp
        p.font.size = Pt(10)
        p.space_after = Pt(3)

    # ----------------------------------------------------
    # SLIDE 7: Explainable AI (TreeSHAP Beeswarm & Importance)
    # ----------------------------------------------------
    slide7 = create_blank_slide_with_header(prs, "4. Επεξηγήσιμη Τεχνητή Νοημοσύνη (TreeSHAP XAI)")
    if (FIGURES_DIR / "04_shap_summary_beeswarm.png").exists():
        slide7.shapes.add_picture(str(FIGURES_DIR / "04_shap_summary_beeswarm.png"), Inches(0.8), Inches(1.8), width=Inches(6.8))

    tbox7 = slide7.shapes.add_textbox(Inches(7.8), Inches(1.8), Inches(4.7), Inches(4.8))
    tf7 = tbox7.text_frame
    tf7.word_wrap = True
    p = tf7.paragraphs[0]
    p.text = "ΚΑΤΑΤΑΞΗ ΣΠΟΥΔΑΙΟΤΗΤΑΣ SHAP"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_NAVY

    shap_pts = [
        "1. UL_bitrate (9.259 kbps impact): Κυρίαρχος δείκτης. Η κίνηση Uplink σηματοδοτεί ενεργές TCP ACK ροές λήψης.",
        "2. RSSI (1.102 kbps impact): Συνολική ενέργεια ασύρματου διαύλου.",
        "3. ServingCell_Distance (764 kbps): Επίδραση του Large-scale Path Loss.",
        "4. Speed (754 kbps): Η ταχύτητα οχήματος προκαλεί Doppler shifts και συχνά cell handovers.",
        "5. SNR (739 kbps): Καθορίζει το Shannon channel capacity limit.",
        "6. CQI, RSRQ, RSRP: Συμπληρωματικοί δείκτες ποιότητας."
    ]
    for sp in shap_pts:
        p = tf7.add_paragraph()
        p.text = sp
        p.font.size = Pt(10)
        p.space_after = Pt(4)

    # ----------------------------------------------------
    # SLIDE 8: XAI Local Explanations (Waterfall Plots)
    # ----------------------------------------------------
    slide8 = create_blank_slide_with_header(prs, "4. Τοπικές Εξηγήσεις SHAP Waterfall (High vs Low Throughput)")
    if (FIGURES_DIR / "07_shap_waterfall_local.png").exists():
        slide8.shapes.add_picture(str(FIGURES_DIR / "07_shap_waterfall_local.png"), Inches(0.8), Inches(1.8), width=Inches(11.7))

    # ----------------------------------------------------
    # SLIDE 9: Deep Learning: PyTorch LSTM Forecaster
    # ----------------------------------------------------
    slide9 = create_blank_slide_with_header(prs, "5. Πρόβλεψη Χρονοσειρών με Deep Learning (PyTorch LSTM)")
    if (FIGURES_DIR / "08_lstm_training_loss.png").exists():
        slide9.shapes.add_picture(str(FIGURES_DIR / "08_lstm_training_loss.png"), Inches(0.8), Inches(1.8), width=Inches(6.2))

    tbox9 = slide9.shapes.add_textbox(Inches(7.3), Inches(1.8), Inches(5.2), Inches(4.8))
    tf9 = tbox9.text_frame
    tf9.word_wrap = True
    p = tf9.paragraphs[0]
    p.text = "ΑΡΧΙΤΕΚΤΟΝΙΚΗ & ΕΚΠΑΙΔΕΥΣΗ LSTM"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_NAVY

    lstm_pts = [
        "Δομή Μοντέλου:",
        "  • Lookback Window: 64 χρονικά βήματα (1s granularity).",
        "  • 2 Επίπεδα LSTM με 64 hidden units και Dropout 0.2.",
        "  • Linear Regression Projection Head (Dense 64 -> 32 -> 1).",
        "  • Optimizer: Adam (lr = 0.001), Loss: MSE.",
        "Αποτελέσματα Δοκιμής:",
        "  • RMSE: 14.473,4 kbps (~14,47 Mbps)",
        "  • MAE: 6.935,7 kbps (~6,93 Mbps)",
        "  • R² Score: 0.102",
        "  • Χρόνος Εκπαίδευσης: 129,9s | Inference: 0,101 ms/sample"
    ]
    for lp in lstm_pts:
        p = tf9.add_paragraph()
        p.text = lp
        p.font.size = Pt(10)
        p.space_after = Pt(3)

    # ----------------------------------------------------
    # SLIDE 10: Model Comparison: XGBoost vs LSTM
    # ----------------------------------------------------
    slide10 = create_blank_slide_with_header(prs, "5. Συγκριτική Αξιολόγηση: XGBoost έναντι LSTM")
    if (FIGURES_DIR / "09_model_comparisons.png").exists():
        slide10.shapes.add_picture(str(FIGURES_DIR / "09_model_comparisons.png"), Inches(0.8), Inches(1.8), width=Inches(11.7))

    # ----------------------------------------------------
    # SLIDE 11: Foundation Models (IBM Granite TTM)
    # ----------------------------------------------------
    slide11 = create_blank_slide_with_header(prs, "6. Foundation Models: IBM Granite Tiny Time Mixer (TTM)")
    if (FIGURES_DIR / "10_foundation_model_performance.png").exists():
        slide11.shapes.add_picture(str(FIGURES_DIR / "10_foundation_model_performance.png"), Inches(0.8), Inches(1.8), width=Inches(6.8))

    tbox11 = slide11.shapes.add_textbox(Inches(7.8), Inches(1.8), Inches(4.7), Inches(4.8))
    tf11 = tbox11.text_frame
    tf11.word_wrap = True
    p = tf11.paragraphs[0]
    p.text = "ZERO-SHOT & FINE-TUNING"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_NAVY

    ttm_pts = [
        "Αρχιτεκτονική TTM (Patch-based MLP-Mixer):",
        "  • Patchification: Τεμαχισμός 64s σε 8 patches των 8s.",
        "  • Inter-patch time mixing & intra-patch channel mixing.",
        "Zero-Shot Απόδοση:",
        "  • RMSE: 18.641,9 kbps (χωρίς καμία προηγούμενη εκπαίδευση στο target dataset).",
        "Fine-Tuning Απόδοση (4 εποχές, 24 δευτερόλεπτα):",
        "  • RMSE: 8.426,3 kbps (μείωση σφάλματος κατά 54,8%!).",
        "  • R²: 0.695 (υπερέχει κατά 6.047 kbps έναντι του LSTM).",
        "Κομβικό Συμπέρασμα: Τα Foundation Models προσφέρουν τεράστια ισχύ transfer learning σε κυψελωτές χρονοσειρές."
    ]
    for tp in ttm_pts:
        p = tf11.add_paragraph()
        p.text = tp
        p.font.size = Pt(10)
        p.space_after = Pt(3)

    # ----------------------------------------------------
    # SLIDE 12: SHAP-Guided Feature Pruning
    # ----------------------------------------------------
    slide12 = create_blank_slide_with_header(prs, "7. Σταδιακή Αφαίρεση Μεταβλητών & Edge Efficiency")
    if (FIGURES_DIR / "11_feature_pruning_accuracy_vs_latency.png").exists():
        slide12.shapes.add_picture(str(FIGURES_DIR / "11_feature_pruning_accuracy_vs_latency.png"), Inches(0.8), Inches(1.8), width=Inches(11.7))

    # ----------------------------------------------------
    # SLIDE 13: 5G Proactive QoS Management & Early Warnings
    # ----------------------------------------------------
    slide13 = create_blank_slide_with_header(prs, "8. 5G Proactive Network Management (QoS Early Warning)")
    if (FIGURES_DIR / "12_proactive_5g_early_warning_tradeoff.png").exists():
        slide13.shapes.add_picture(str(FIGURES_DIR / "12_proactive_5g_early_warning_tradeoff.png"), Inches(0.8), Inches(1.8), width=Inches(6.8))

    tbox13 = slide13.shapes.add_textbox(Inches(7.8), Inches(1.8), Inches(4.7), Inches(4.8))
    tf13 = tbox13.text_frame
    tf13.word_wrap = True
    p = tf13.paragraphs[0]
    p.text = "ΑΝΙΧΝΕΥΣΗ ΥΠΟΒΑΘΜΙΣΗΣ (THRESHOLD = 5 Mbps)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_NAVY

    proact_pts = [
        "Lead Time Δt = 1s:",
        "  • Recall: 91,6% | False Alarms: 6,4% | F1: 0.929",
        "Lead Time Δt = 3s:",
        "  • Recall: 88,3% | False Alarms: 7,8% | F1: 0.905",
        "Lead Time Δt = 5s:",
        "  • Recall: 85,7% | False Alarms: 7,9% | F1: 0.890",
        "Lead Time Δt = 10s:",
        "  • Recall: 81,3% | False Alarms: 7,9% | F1: 0.864",
        "Lead Time Δt = 15s:",
        "  • Recall: 78,2% | False Alarms: 7,5% | F1: 0.847",
        "Trade-Off:",
        "Στα 5 δευτερόλεπτα προπορείας, διατηρείται ακρίβεια 85,7% παρέχοντας επαρκή χρόνο για προληπτικό handover."
    ]
    for pp in proact_pts:
        p = tf13.add_paragraph()
        p.text = pp
        p.font.size = Pt(10)
        p.space_after = Pt(3)

    # ----------------------------------------------------
    # SLIDE 14: Action Catalog & Architecture (3GPP NWDAF & O-RAN RIC)
    # ----------------------------------------------------
    slide14 = create_blank_slide_with_header(prs, "8. Ενορχήστρωση & Ένταξη στο 3GPP NWDAF και O-RAN RIC")
    tbox14 = slide14.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
    tf14 = tbox14.text_frame
    tf14.word_wrap = True

    arch_sections = [
        ("3GPP NWDAF (Network Data Analytics Function):", [
            "Συλλέγει μετρήσεις από UEs και gNodeBs.",
            "Υπολογίζει προβλέψεις Throughput και αποστέλλει QoS analytics (Nnwdaf_AnalyticsInfo) στο PCF (Policy Control Function).",
            "Ενεργοποιεί δυναμική προσαρμογή κανόνων SLA και QoS profile."
        ]),
        ("O-RAN Architecture (Near-RT RIC & Non-RT RIC):", [
            "Non-RT RIC (SMO): Φιλοξενεί rApps για offline μοντελοποίηση, training και SHAP ανάλυση.",
            "Near-RT RIC (xApp): Online συμπερασμός (< 10 ms latency) μέσω E2 interface.",
            "Προληπτική αποστολή εντολών ελέγχου στο O-DU (Distributed Unit) για PRB reallocation και Beam Switching."
        ]),
        ("Κατάλογος Προληπτικών Ενεργειών (Action Catalog):", [
            "• Predictive Handover (Lead time >= 1s): Αποφυγή Radio Link Failures.",
            "• Dynamic PRB Reservation (Lead time >= 2s): Εγγύηση εύρους ζώνης για eMBB slices.",
            "• MEC Video ABR Adaptation (Lead time >= 3s): Προσαρμογή ανάλυσης DASH/HLS πριν αδειάσει το buffer.",
            "• Dual Connectivity Traffic Steering (Lead time >= 5s): Προληπτική αλλαγή SCG leg."
        ])
    ]

    for title, bullets in arch_sections:
        p = tf14.add_paragraph()
        p.text = title
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_NAVY
        p.space_after = Pt(2)
        for b in bullets:
            p_b = tf14.add_paragraph()
            p_b.text = f"  • {b}"
            p_b.font.size = Pt(10)
            p_b.font.color.rgb = COLOR_DARK_TEXT
            p_b.space_after = Pt(2)

    # ----------------------------------------------------
    # SLIDE 15: Conclusions & Live Demo Commands
    # ----------------------------------------------------
    slide15 = create_blank_slide_with_header(prs, "Συμπεράσματα & Εντολές Εκτέλεσης (Demo)")
    tbox15 = slide15.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.8))
    tf15 = tbox15.text_frame
    tf15.word_wrap = True
    p = tf15.paragraphs[0]
    p.text = "ΚΥΡΙΑ ΕΥΡΗΜΑΤΑ"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_NAVY

    finds = [
        "1. Το XGBoost κυριαρχεί σε ακρίβεια (R² = 0.825) και ταχύτητα (0,001 ms/sample) έναντι του LSTM.",
        "2. Το TreeSHAP αποκάλυψε ότι UL_bitrate και RSSI εξηγούν το μεγαλύτερο μέρος της διακύμανσης του Throughput.",
        "3. Η σταδιακή αφαίρεση του 75% των χαρακτηριστικών διατηρεί την ακρίβεια άθικτη, μειώνοντας το edge latency.",
        "4. Το Foundation Model (IBM Granite TTM) με 4 εποχές fine-tuning πέτυχε 54,8% μείωση σφάλματος.",
        "5. Η προληπτική ανίχνευση υποβάθμισης επιτυγχάνει 85,7% επιτυχία με 5s διαθέσιμο χρόνο αντίδρασης."
    ]
    for f in finds:
        p = tf15.add_paragraph()
        p.text = f
        p.font.size = Pt(10)
        p.space_after = Pt(4)

    # Right side: Commands box
    tbox15_r = slide15.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.4), Inches(4.8))
    tf15_r = tbox15_r.text_frame
    tf15_r.word_wrap = True
    p = tf15_r.paragraphs[0]
    p.text = "ΕΤΟΙΜΕΣ ΕΝΤΟΛΕΣ ΕΚΤΕΛΕΣΗΣ (READY RUNNERS)"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_ACCENT

    cmds = [
        "Πλήρης Αυτοματοποιημένη Εκτέλεση (One-Click):",
        "  .\\run.bat   ή   .\\run.ps1",
        "Εκτέλεση μέσω Python Pipeline CLI:",
        "  python scripts/run_pipeline.py --all",
        "Τμηματική Εκτέλεση Ανά Ζητούμενο:",
        "  python scripts/run_pipeline.py --preprocess",
        "  python scripts/run_pipeline.py --ml",
        "  python scripts/run_pipeline.py --shap",
        "  python scripts/run_pipeline.py --dl",
        "  python scripts/run_pipeline.py --foundation",
        "  python scripts/run_pipeline.py --prune",
        "  python scripts/run_pipeline.py --proactive",
        "Έλεγχος & Επαλήθευση Αποτελεσμάτων:",
        "  python scripts/verify_all.py"
    ]
    for c in cmds:
        p = tf15_r.add_paragraph()
        p.text = c
        p.font.size = Pt(10)
        p.font.name = "Consolas"
        p.space_after = Pt(2)

    # ----------------------------------------------------
    # SLIDE 16: Closing / Q&A Slide
    # ----------------------------------------------------
    slide16 = prs.slides.add_slide(slide_layout)
    bg16 = slide16.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg16.fill.solid()
    bg16.fill.fore_color.rgb = COLOR_NAVY
    bg16.line.fill.background()

    tbox16 = slide16.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.333), Inches(3.5))
    tf16 = tbox16.text_frame
    tf16.word_wrap = True

    p_end = tf16.paragraphs[0]
    p_end.alignment = PP_ALIGN.CENTER
    p_end.text = "Ευχαριστώ για την Προσοχή σας!"
    p_end.font.size = Pt(36)
    p_end.font.bold = True
    p_end.font.color.rgb = COLOR_WHITE

    p_qa = tf16.add_paragraph()
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.text = "\nΕρωτήσεις & Συζήτηση (Q&A)\n\n"
    p_qa.font.size = Pt(20)
    p_qa.font.color.rgb = RGBColor(0x34, 0x98, 0xDB)

    p_cont = tf16.add_paragraph()
    p_cont.alignment = PP_ALIGN.CENTER
    p_cont.text = "GitHub Repository: https://github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting\n5G Downlink Bitrate Forecasting & Proactive Management System"
    p_cont.font.size = Pt(13)
    p_cont.font.color.rgb = RGBColor(0xBD, 0xC3, 0xC7)

    # Save presentation
    out_pptx = PRESENTATION_DIR / "Downlink_Bitrate_Forecasting_5G.pptx"
    try:
        prs.save(str(out_pptx))
        print(f"Presentation saved successfully to {out_pptx}")
    except PermissionError:
        print(f"[INFO] {out_pptx.name} is currently open in PowerPoint; keeping existing file.")
    return out_pptx


if __name__ == "__main__":
    generate_presentation_deck()
