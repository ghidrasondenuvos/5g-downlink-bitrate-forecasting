"""
Midterm (40-50% Progress) Presentation Deck Generator Script.
Generates a clean, focused 7-slide PowerPoint presentation strictly for the
Preparatory / Intermediate Presentation (Ενδιάμεση Παρουσίαση - 40-50% προόδου)
covering ONLY Requirements 1, 2, 3 (and basic 4), leaving Requirements 5-8 as Next Steps.
"""

import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import PRESENTATION_DIR, FIGURES_DIR

COLOR_NAVY = RGBColor(0x00, 0x33, 0x66)
COLOR_BLUE = RGBColor(0x1F, 0x49, 0x7D)
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_DARK_TEXT = RGBColor(0x22, 0x22, 0x22)
COLOR_GRAY = RGBColor(0x7F, 0x8C, 0x8D)


def create_slide(prs, title_text, subtitle_category="ΕΝΔΙΑΜΕΣΗ ΠΑΡΟΥΣΙΑΣΗ (40-50% ΠΡΟΟΔΟΥ)"):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)

    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = subtitle_category
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_GRAY

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY

    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.7), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_BLUE
    line.line.color.rgb = COLOR_BLUE

    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.4))
    tf_f = footer_box.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = "Θέμα 11: Πρόβλεψη Downlink Bitrate σε 5G | Ενδιάμεση Παρουσίαση (40%-50%)"
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = COLOR_GRAY

    return slide


def generate_midterm_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # SLIDE 1: Title Slide
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.3), Inches(5.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "ΕΝΔΙΑΜΕΣΗ ΠΑΡΟΥΣΙΑΣΗ ΠΡΟΟΔΟΥ (40% - 50%)"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(0x34, 0x98, 0xDB)

    p1 = tf1.add_paragraph()
    p1.text = "\nΘέμα 11: Πρόβλεψη Downlink Bitrate (Throughput)\nΜε Βάση Μετρικές Ποιότητας Καναλιού"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_WHITE

    p2 = tf1.add_paragraph()
    p2.text = "\nΜάθημα: Αρχιτεκτονικές Δικτύων Επόμενης Γενιάς, Τεχνολογίες και Εφαρμογές\nΕπιβλέπων: Παναγιώτης Μαράντης (pmaradis@isi.gr)\nΧειμερινό Εξάμηνο 2026-2027"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(0xEC, 0xF0, 0xF1)

    # SLIDE 2: Ζητούμενο 1 (10%) - Τηλεπικοινωνιακό Πρόβλημα 5G
    s2 = create_slide(prs, "1. Σημασία Πρόβλεψης Downlink Bitrate στα Δίκτυα 5G (Ζητούμενο 1 - 10%)")
    tb2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    bullets_s2 = [
        ("Το Τηλεπικοινωνιακό Πρόβλημα στα 5G Δίκτυα:",
         "Ο ρυθμός μετάδοσης (Downlink Bitrate) μεταβάλλεται έντονα λόγω κινητικότητας (handovers, Doppler), αστικού shadowing και παρεμβολών."),
        ("Γιατί δεν αρκεί η κλασική (Reactive) διαχείριση:",
         "Όταν το δίκτυο αντιδρά αφού πέσει το throughput, ο χρήστης έχει ήδη υποστεί διακοπή (π.χ. video buffering ή αύξηση latency σε URLLC)."),
        ("Τι κερδίζουμε με την Πρόβλεψη (Proactive Management):",
         "• Προληπτικό Handover σε γειτονικό σταθμό βάσης (gNB) πριν χαθεί η ζεύξη.\n"
         "• Έγκαιρη προσαρμογή Modulation & Coding Scheme (MCS) και Resource Blocks (PRBs).\n"
         "• Προσαρμογή ρυθμού ροής εφαρμογών (Adaptive Video Bitrate / Buffering)."),
        ("Στόχος της Εργασίας:",
         "Πρόβλεψη του μελλοντικού DL_bitrate χρησιμοποιώντας ιστορικά παράθυρα (Lookback Windows) από μετρικές ραδιοκαναλιού (RSRP, RSRQ, SNR, CQI, RSSI, Speed).")
    ]
    for idx, (head, body) in enumerate(bullets_s2):
        p = tf2.paragraphs[0] if idx == 0 else tf2.add_paragraph()
        p.text = f"▪ {head}"
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        p.space_after = Pt(2)

        pb = tf2.add_paragraph()
        pb.text = f"   {body}"
        pb.font.size = Pt(13)
        pb.font.color.rgb = COLOR_DARK_TEXT
        pb.space_after = Pt(12)

    # SLIDE 3: Ζητούμενο 2 (15%) - Προεπεξεργασία & Ενοποίηση Traces
    s3 = create_slide(prs, "2. Προεπεξεργασία Δεδομένων & Ενοποίηση Traces (Ζητούμενο 2 - 15%)")
    tb3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.4), Inches(5.0))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    bullets_s3 = [
        ("Ενοποίηση Δεδομένων (UCC Cellular Dataset):",
         "Συνενώθηκαν 135 αρχεία CSV από τα 5 σενάρια κίνησης (bus, car, pedestrian, static, train) -> 174.523 συνολικές εγγραφές (1 Hz)."),
        ("Καθαρισμός Null / Παυλών ('-'):",
         "Οι ελλείπουσες μετρήσεις (συμβολιζόμενες ως '-') μετατράπηκαν σε NaN και συμπληρώθηκαν ανά trace (ffill/bfill) ώστε να μην αλλοιώνεται η χρονική συνέχεια."),
        ("Διαχωρισμός Train / Test (80% - 20%):",
         "Έγινε ανά trace_id (106 traces = 131.370 δείγματα Train | 29 traces = 43.153 δείγματα Test) για αποφυγή data leakage μεταξύ χρονικών στιγμών."),
        ("Κανονικοποίηση (StandardScaler):",
         "Εφαρμόστηκε Z-score κανονικοποίηση (fit μόνο στο Train set) στις 8 αριθμητικές μετρικές εισόδου.")
    ]
    for idx, (head, body) in enumerate(bullets_s3):
        p = tf3.paragraphs[0] if idx == 0 else tf3.add_paragraph()
        p.text = f"• {head}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        pb = tf3.add_paragraph()
        pb.text = f"  {body}"
        pb.font.size = Pt(12)
        pb.font.color.rgb = COLOR_DARK_TEXT
        pb.space_after = Pt(10)

    fig2 = FIGURES_DIR / "02_eda_mobility_comparison.png"
    if fig2.exists():
        s3.shapes.add_picture(str(fig2), Inches(6.4), Inches(1.9), width=Inches(6.2))

    # SLIDE 4: Ζητούμενο 3 (15%) - XGBoost Regressor (Lookback & Horizon)
    s4 = create_slide(prs, "3. Μοντέλο Παλινδρόμησης XGBoost: Lookback & Horizon (Ζητούμενο 3 - 15%)")
    tb4 = s4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.3), Inches(5.0))
    tf4 = tb4.text_frame
    tf4.word_wrap = True

    bullets_s4 = [
        ("Κατασκευή Sliding Windows:",
         "Για κάθε χρονική στιγμή t, το διάνυσμα εισόδου περιλαμβάνει τις L προηγούμενες μετρήσεις και προβλέπει το DL_bitrate στη στιγμή t + H."),
        ("Πειραματικός Έλεγχος Παραμέτρων:",
         "• Lookback Windows (L): 5, 10, 20, 30 δευτερόλεπτα.\n"
         "• Prediction Horizons (H): 1, 3, 5, 10 δευτερόλεπτα μπροστά."),
        ("Αποτελέσματα Μετρικών (για L=10):",
         "• H = 1s: RMSE = 857.6 kbps | MAE = 507.6 kbps\n"
         "• H = 3s: RMSE = 1044.4 kbps | MAE = 626.8 kbps\n"
         "• H = 5s: RMSE = 1106.4 kbps | MAE = 674.8 kbps\n"
         "• H = 10s: RMSE = 1179.9 kbps | MAE = 747.8 kbps"),
        ("Βασικό Συμπέρασμα:",
         "Το Lookback L=10s αρκεί για τη βέλτιστη πρόβλεψη. Καθώς αυξάνεται ο ορίζοντας H (από 1s σε 10s), το σφάλμα αυξάνεται λόγω στοχαστικότητας του καναλιού.")
    ]
    for idx, (head, body) in enumerate(bullets_s4):
        p = tf4.paragraphs[0] if idx == 0 else tf4.add_paragraph()
        p.text = f"• {head}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        pb = tf4.add_paragraph()
        pb.text = f"  {body}"
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = COLOR_DARK_TEXT
        pb.space_after = Pt(8)

    fig3 = FIGURES_DIR / "03_xgboost_horizons_lookback.png"
    if fig3.exists():
        s4.shapes.add_picture(str(fig3), Inches(6.3), Inches(1.8), width=Inches(6.2))

    # SLIDE 5: Ζητούμενο 4 (10%) - Explainable AI (SHAP)
    s5 = create_slide(prs, "4. Ερμηνευσιμότητα Μοντέλου με Explainable AI - SHAP (Ζητούμενο 4 - 10%)")
    tb5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.3), Inches(5.0))
    tf5 = tb5.text_frame
    tf5.word_wrap = True

    bullets_s5 = [
        ("Γιατί χρησιμοποιούμε SHAP (TreeExplainer):",
         "Για να ανοίξουμε το 'μαύρο κουτί' του XGBoost και να εντοπίσουμε ποιες μετρικές καθορίζουν την πρόβλεψη του Downlink Bitrate."),
        ("Κατάταξη Σημαντικότητας Μεταβλητών (Mean |SHAP|):",
         "1. UL_bitrate (615.9 kbps): Ενδεικτικό ενεργής κίνησης & φόρτου.\n"
         "2. RSSI (115.6 kbps): Συνολική λαμβανόμενη ισχύς.\n"
         "3. ServingCell_Distance (104.5 kbps): Απόσταση από τον σταθμό βάσης (Path Loss).\n"
         "4. Speed (99.4 kbps): Ταχύτητα κίνησης χρήστη (Doppler / Handovers).\n"
         "5. SNR & RSRP (88.3 & 79.6 kbps): Καθαρότητα & ισχύς σήματος αναφοράς."),
        ("Χρονική Επίδραση (Lags):",
         "Οι πιο πρόσφατες μετρήσεις (χρονικές στιγμές t και t-1) έχουν τη μεγαλύτερη βαρύτητα στην πρόβλεψη.")
    ]
    for idx, (head, body) in enumerate(bullets_s5):
        p = tf5.paragraphs[0] if idx == 0 else tf5.add_paragraph()
        p.text = f"• {head}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        pb = tf5.add_paragraph()
        pb.text = f"  {body}"
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = COLOR_DARK_TEXT
        pb.space_after = Pt(8)

    fig5 = FIGURES_DIR / "05_shap_feature_importance.png"
    if fig5.exists():
        s5.shapes.add_picture(str(fig5), Inches(6.3), Inches(2.0), width=Inches(6.2))

    # SLIDE 6: Σύνοψη Ποσοστού Ολοκλήρωσης & Επόμενα Βήματα (Υπόλοιπο 50-60%)
    s6 = create_slide(prs, "5. Σύνοψη Προόδου (40-50%) & Επόμενα Βήματα για την Τελική Παρουσίαση")
    tb6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.7), Inches(5.0))
    tf6 = tb6.text_frame
    tf6.word_wrap = True

    steps = [
        ("ΟΛΟΚΛΗΡΩΜΕΝΟ ΤΜΗΜΑ — ΕΝΔΙΑΜΕΣΗ ΦΑΣΗ (50% ΤΩΝ ΖΗΤΟΥΜΕΝΩΝ):",
         "✔ Ζητούμενο 1 (10%): Ανάλυση τηλεπικοινωνιακού προβλήματος πρόβλεψης throughput σε 5G.\n"
         "✔ Ζητούμενο 2 (15%): Προεπεξεργασία, καθαρισμός '-', ένωση 135 traces, κανονικοποίηση & train/test split.\n"
         "✔ Ζητούμενο 3 (15%): Εκπαίδευση XGBoost Regressor για πολλαπλά Lookback Windows & Prediction Horizons (RMSE, MAE, MAPE).\n"
         "✔ Ζητούμενο 4 (10%): Εφαρμογή Explainable AI (SHAP) για εύρεση των σημαντικότερων μετρικών ποιότητας."),
        ("ΕΠΟΜΕΝΑ ΒΗΜΑΤΑ — ΤΕΛΙΚΗ ΦΑΣΗ (ΥΠΟΛΟΙΠΟ 50% ΤΩΝ ΖΗΤΟΥΜΕΝΩΝ):",
         "⏳ Ζητούμενο 5 (15%): Υλοποίηση μοντέλου Deep Learning (LSTM με παράθυρο 64 δειγμάτων) και σύγκριση με το XGBoost.\n"
         "⏳ Ζητούμενο 6 - Bonus (10%): Δοκιμή Foundation Model χρονοσειρών (IBM Granite Tiny Time Mixer - Zero-shot & Fine-tuning).\n"
         "⏳ Ζητούμενο 7 (10%): Σταδιακή αφαίρεση λιγότερο σημαντικών μεταβλητών (βάσει SHAP) και μέτρηση χρόνου εκπαίδευσης/πρόβλεψης.\n"
         "⏳ Ζητούμενο 8 (15%): Μελέτη 5G Proactive Network Management (έγκαιρη ανίχνευση πτώσης bitrate & trade-off ακρίβειας vs χρόνου αντίδρασης).")
    ]
    for idx, (head, body) in enumerate(steps):
        p = tf6.paragraphs[0] if idx == 0 else tf6.add_paragraph()
        p.text = head
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY if idx == 0 else COLOR_BLUE
        p.space_after = Pt(6)

        pb = tf6.add_paragraph()
        pb.text = body
        pb.font.size = Pt(13.5)
        pb.font.color.rgb = COLOR_DARK_TEXT
        pb.space_after = Pt(18)

    out_path = PRESENTATION_DIR / "Endiamesi_Parousiasi_5G_40_50_Percent.pptx"
    prs.save(str(out_path))
    print(f"Midterm presentation saved to: {out_path}")
    return out_path


if __name__ == "__main__":
    generate_midterm_deck()
