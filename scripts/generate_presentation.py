"""
Presentation Deck Generator Script (Full 100% Project Deliverable).
Generates an executive, comprehensive 20-slide Widescreen PowerPoint presentation
(presentation/Downlink_Bitrate_Forecasting_5G.pptx & presentation/Teliki_Parousiasi_5G_100_Percent.pptx)
with native PowerPoint tables, KPI callout cards, all 12+ high-resolution figures,
and detailed Greek speaker notes on every slide.

Authors:
- ΔΗΜΗΤΡΙΟΣ ΤΣΑΝΑΚΤΣΗΣ (Α.Μ.: 1100736)
- ΙΑΣΩΝΑΣ ΔΕΡΒΕΝΗΣ (Α.Μ.: 1097437)
"""

import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import BASE_DIR, PRESENTATION_DIR, FIGURES_DIR, RESULTS_DIR

# Authors Metadata
AUTHORS_LINE = "ΔΗΜΗΤΡΙΟΣ ΤΣΑΝΑΚΤΣΗΣ (Α.Μ.: 1100736)  |  ΙΑΣΩΝΑΣ ΔΕΡΒΕΝΗΣ (Α.Μ.: 1097437)"
AUTHOR_1 = "ΔΗΜΗΤΡΙΟΣ ΤΣΑΝΑΚΤΣΗΣ (Α.Μ.: 1100736)"
AUTHOR_2 = "ΙΑΣΩΝΑΣ ΔΕΡΒΕΝΗΣ (Α.Μ.: 1097437)"

# Corporate / Academic Color Palette
COLOR_NAVY = RGBColor(0x00, 0x33, 0x66)        # #003366 Primary Navy
COLOR_DARK_NAVY = RGBColor(0x0A, 0x19, 0x2F)   # #0A192F Deep Navy Cover
COLOR_BLUE = RGBColor(0x1F, 0x49, 0x7D)        # #1F497D Secondary Blue
COLOR_SKY = RGBColor(0x29, 0x80, 0xB9)         # #2980B9 Bright Blue Accent
COLOR_LIGHT_BLUE = RGBColor(0xEB, 0xF5, 0xFB)  # #EBF5FB Highlight Row Blue
COLOR_LIGHT_BG = RGBColor(0xF4, 0xF6, 0xF9)    # #F4F6F9 Soft Zebra Gray-Blue
COLOR_CARD_BG = RGBColor(0xF8, 0xFA, 0xFC)     # #F8FAFC Card Fill
COLOR_CARD_BORDER = RGBColor(0xD0, 0xD7, 0xDE) # #D0D7DE Subtle Border
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_DARK_TEXT = RGBColor(0x1E, 0x29, 0x3B)
COLOR_GRAY = RGBColor(0x64, 0x74, 0x8B)
COLOR_ACCENT = RGBColor(0x16, 0xA0, 0x85)      # #16A085 Teal/Green Accent
COLOR_LIGHT_GREEN = RGBColor(0xE8, 0xF8, 0xF5) # #E8F8F5 Highlight Row Green
COLOR_GOLD = RGBColor(0xF3, 0x9C, 0x12)        # #F39C12 Gold Accent
COLOR_CORAL = RGBColor(0xC0, 0x39, 0x2B)       # #C0392B Alert Red


def set_speaker_notes(slide, notes_text: str):
    """Adds Greek speaker notes to a slide."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text.strip()


def create_blank_slide_with_header(prs, title_text, category="5G NETWORK ARCHITECTURES & ML", slide_num=None, total_slides=20):
    """Creates a standard content slide with an academic header, badge, and author footer banner."""
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Subtle top bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_NAVY
    top_bar.line.fill.background()

    # Top Header Banner
    header_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.22), Inches(12.1), Inches(0.95))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category.upper()
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_SKY

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY

    # Thin separator line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.22), Inches(12.133), Inches(0.025))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_BLUE
    line.line.fill.background()

    # Footer separator line
    f_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(7.02), Inches(12.133), Inches(0.015))
    f_line.fill.solid()
    f_line.fill.fore_color.rgb = COLOR_CARD_BORDER
    f_line.line.fill.background()

    # Footer Left/Center: Course & Authors
    footer_box = slide.shapes.add_textbox(Inches(0.6), Inches(7.06), Inches(10.8), Inches(0.35))
    tf_f = footer_box.text_frame
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = f"Πανεπιστήμιο Πατρών / ISI  |  Θέμα 11: 5G Downlink Bitrate Forecasting  |  {AUTHORS_LINE}"
    p_f.font.size = Pt(8.5)
    p_f.font.bold = True
    p_f.font.color.rgb = COLOR_GRAY

    # Footer Right: Slide Number
    if slide_num is not None:
        num_box = slide.shapes.add_textbox(Inches(11.5), Inches(7.06), Inches(1.233), Inches(0.35))
        tf_n = num_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"Διαφάνεια {slide_num} / {total_slides}"
        p_n.font.size = Pt(8.5)
        p_n.font.bold = True
        p_n.font.color.rgb = COLOR_NAVY

    return slide


def add_kpi_card(slide, left, top, width, height, value_text, label_text, sub_text="", accent_color=COLOR_NAVY):
    """Adds a polished KPI callout card with a top colored accent stripe."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD_BG
    card.line.color.rgb = COLOR_CARD_BORDER
    card.line.width = Pt(1)

    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.07))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent_color
    stripe.line.fill.background()

    tbox = slide.shapes.add_textbox(left + Inches(0.08), top + Inches(0.1), width - Inches(0.16), height - Inches(0.14))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p_val = tf.paragraphs[0]
    p_val.alignment = PP_ALIGN.CENTER
    p_val.text = value_text
    p_val.font.size = Pt(16)
    p_val.font.bold = True
    p_val.font.color.rgb = accent_color

    p_lbl = tf.add_paragraph()
    p_lbl.alignment = PP_ALIGN.CENTER
    p_lbl.text = label_text
    p_lbl.font.size = Pt(9.5)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_DARK_TEXT

    if sub_text:
        p_sub = tf.add_paragraph()
        p_sub.alignment = PP_ALIGN.CENTER
        p_sub.text = sub_text
        p_sub.font.size = Pt(8)
        p_sub.font.color.rgb = COLOR_GRAY


def add_info_card(slide, left, top, width, height, title_text, bullets, accent_color=COLOR_NAVY, font_size=10):
    """Adds a structured content card with header and bullet points."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD_BG
    card.line.color.rgb = COLOR_CARD_BORDER
    card.line.width = Pt(1)

    header_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.36))
    header_bar.fill.solid()
    header_bar.fill.fore_color.rgb = accent_color
    header_bar.line.fill.background()

    htf = header_bar.text_frame
    htf.word_wrap = True
    p_h = htf.paragraphs[0]
    p_h.alignment = PP_ALIGN.LEFT
    p_h.text = f"  {title_text}"
    p_h.font.size = Pt(11)
    p_h.font.bold = True
    p_h.font.color.rgb = COLOR_WHITE

    tbox = slide.shapes.add_textbox(left + Inches(0.14), top + Inches(0.42), width - Inches(0.28), height - Inches(0.48))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    for idx, b in enumerate(bullets):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = b
        p.font.size = Pt(font_size)
        p.font.color.rgb = COLOR_DARK_TEXT
        p.space_after = Pt(4)


def add_styled_table(slide, left, top, width, height, headers, rows, col_widths=None, highlight_rows=None, font_size=9.5):
    """Creates a native PowerPoint table with Navy header and alternating zebra rows."""
    highlight_rows = set(highlight_rows or [])
    num_rows = len(rows) + 1
    num_cols = len(headers)

    table_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
    table = table_shape.table

    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = w

    # Style Header
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.06)
        tf.margin_top = tf.margin_bottom = Inches(0.03)
        p = tf.paragraphs[0]
        p.text = h_text
        p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
        p.font.size = Pt(font_size)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE

    # Style Data Rows
    for row_idx, r_data in enumerate(rows):
        is_hi = row_idx in highlight_rows
        bg_color = COLOR_LIGHT_GREEN if is_hi else (COLOR_LIGHT_BG if row_idx % 2 == 1 else COLOR_WHITE)
        for col_idx, val in enumerate(r_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_color
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = Inches(0.06)
            tf.margin_top = tf.margin_bottom = Inches(0.02)
            p = tf.paragraphs[0]
            p.text = str(val)
            p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER
            p.font.size = Pt(font_size)
            p.font.bold = is_hi or (col_idx == 0)
            p.font.color.rgb = COLOR_NAVY if is_hi else COLOR_DARK_TEXT

    return table


def generate_presentation_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    total_slides = 20
    slide_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Navy Elegance + Prominent Author Cards)
    # =========================================================================
    slide1 = prs.slides.add_slide(slide_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_DARK_NAVY
    bg1.line.fill.background()

    # Decorative Left Accent Pillar
    left_stripe = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.28), Inches(7.5))
    left_stripe.fill.solid()
    left_stripe.fill.fore_color.rgb = COLOR_ACCENT
    left_stripe.line.fill.background()

    # Top Institution Header
    tbox1 = slide1.shapes.add_textbox(Inches(0.8), Inches(0.55), Inches(11.8), Inches(3.6))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p_uni = tf1.paragraphs[0]
    p_uni.text = "ΠΑΝΕΠΙΣΤΗΜΙΟ ΠΑΤΡΩΝ — ΤΜΗΜΑ ΜΗΧΑΝΙΚΩΝ Η/Υ & ΠΛΗΡΟΦΟΡΙΚΗΣ (CEID)\nΕΡΕΥΝΗΤΙΚΟ ΙΝΣΤΙΤΟΥΤΟ ΒΙΟΜΗΧΑΝΙΚΩΝ ΣΥΣΤΗΜΑΤΩΝ (ISI)"
    p_uni.font.size = Pt(13)
    p_uni.font.bold = True
    p_uni.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    p_badge = tf1.add_paragraph()
    p_badge.text = "\nΤΕΛΙΚΗ ΠΑΡΟΥΣΙΑΣΗ ΕΡΓΑΣΙΑΣ (100% ΤΩΝ ΖΗΤΟΥΜΕΝΩΝ — ΘΕΜΑ 11)"
    p_badge.font.size = Pt(13)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_ACCENT

    p_main = tf1.add_paragraph()
    p_main.text = "Πρόβλεψη Downlink Bitrate (Throughput)\nΜε Βάση Μετρικές Ποιότητας Καναλιού"
    p_main.font.size = Pt(30)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_WHITE

    p_sub = tf1.add_paragraph()
    p_sub.text = "Προληπτική Διαχείριση Πόρων σε Δίκτυα 5G/6G μέσω Machine Learning, Explainable AI (TreeSHAP), Deep Learning (LSTM) & Foundation Models (IBM Granite TTM)"
    p_sub.font.size = Pt(14.5)
    p_sub.font.color.rgb = RGBColor(0x60, 0xA5, 0xFA)

    # Prominent Authors Card on Slide 1
    auth_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.35), Inches(11.7), Inches(1.55))
    auth_card.fill.solid()
    auth_card.fill.fore_color.rgb = RGBColor(0x11, 0x22, 0x40)
    auth_card.line.color.rgb = COLOR_ACCENT
    auth_card.line.width = Pt(1.5)

    atf = auth_card.text_frame
    atf.word_wrap = True
    atf.margin_left = Inches(0.25)
    atf.margin_top = Inches(0.15)

    p_a_hdr = atf.paragraphs[0]
    p_a_hdr.text = "ΣΥΓΓΡΑΦΕΙΣ / ΟΜΑΔΑ ΕΡΓΟΥ:"
    p_a_hdr.font.size = Pt(11)
    p_a_hdr.font.bold = True
    p_a_hdr.font.color.rgb = COLOR_ACCENT

    p_a1 = atf.add_paragraph()
    p_a1.text = f"•  {AUTHOR_1}        •  {AUTHOR_2}"
    p_a1.font.size = Pt(18)
    p_a1.font.bold = True
    p_a1.font.color.rgb = COLOR_WHITE

    p_a_sup = atf.add_paragraph()
    p_a_sup.text = "Μάθημα: Αρχιτεκτονικές Δικτύων Επόμενης Γενιάς, Τεχνολογίες και Εφαρμογές  |  Επιβλέπων: Παναγιώτης Μαράντης (pmaradis@isi.gr)  |  Χειμερινό Εξάμηνο 2026–2027"
    p_a_sup.font.size = Pt(11.5)
    p_a_sup.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    # Bottom KPI Strip on Cover
    cover_kpis = [
        ("135 Traces / 174.523s", "Πραγματικές Καταγραφές 5 Σεναρίων"),
        ("R² = 0.825 (XGBoost)", "Κορυφαία Ακρίβεια (RMSE 6,34 Mbps)"),
        ("-54,8% Σφάλμα (TTM)", "IBM Granite Foundation Fine-Tuning"),
        ("91,6% Recall (Δt=1s)", "5G Proactive QoS Early Warning")
    ]
    for idx, (k_val, k_lbl) in enumerate(cover_kpis):
        bx = Inches(0.8 + idx * 2.98)
        b_shape = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, Inches(6.15), Inches(2.78), Inches(0.9))
        b_shape.fill.solid()
        b_shape.fill.fore_color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        b_shape.line.color.rgb = RGBColor(0x33, 0x41, 0x55)
        btf = b_shape.text_frame
        btf.word_wrap = True
        p1 = btf.paragraphs[0]
        p1.alignment = PP_ALIGN.CENTER
        p1.text = k_val
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_GOLD if idx % 2 == 1 else COLOR_ACCENT
        p2 = btf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.text = k_lbl
        p2.font.size = Pt(9)
        p2.font.color.rgb = COLOR_WHITE

    set_speaker_notes(slide1, """
Καλησπέρα σας. Ονομαζόμαστε Δημήτριος Τσανακτσής (Α.Μ. 1100736) και Ιάσωνας Δερβενής (Α.Μ. 1097437).
Σήμερα θα σας παρουσιάσουμε την ολοκληρωμένη εργασία μας για το Θέμα 11: «Πρόβλεψη Downlink Bitrate (Throughput) με Βάση Μετρικές Ποιότητας Καναλιού και Προληπτική Διαχείριση Πόρων σε Δίκτυα 5G/6G», υπό την επίβλεψη του κ. Παναγιώτη Μαράντη.
Η παρουσίαση καλύπτει το 100% των 8 ζητουμένων της εργασίας, συνδυάζοντας κλασική Μηχανική Μάθηση (XGBoost), Επεξηγήσιμη Τεχνητή Νοημοσύνη (TreeSHAP), Βαθιά Μάθηση (PyTorch LSTM), Foundation Models χρονοσειρών (IBM Granite Tiny Time Mixer), ανάλυση Feature Pruning και προληπτική διαχείριση 5G QoS.
""")

    # =========================================================================
    # SLIDE 2: Overview, Authors Identity & 8 Project Deliverables
    # =========================================================================
    slide2 = create_blank_slide_with_header(
        prs,
        "Ταυτότητα Εργασίας & Δομή των 8 Ζητουμένων (100% Κάλυψη)",
        category="OVERVIEW & PROJECT DELIVERABLES",
        slide_num=2,
        total_slides=total_slides
    )

    # Top Author & Course Banner Card
    team_card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.38), Inches(12.133), Inches(0.95))
    team_card.fill.solid()
    team_card.fill.fore_color.rgb = COLOR_LIGHT_BLUE
    team_card.line.color.rgb = COLOR_SKY
    team_card.line.width = Pt(1.2)
    ttf = team_card.text_frame
    ttf.word_wrap = True
    ttf.margin_left = Inches(0.2)
    ttf.margin_top = Inches(0.08)

    pt1 = ttf.paragraphs[0]
    pt1.text = f"ΟΜΑΔΑ ΥΛΟΠΟΙΗΣΗΣ:   1) {AUTHOR_1}     |     2) {AUTHOR_2}"
    pt1.font.size = Pt(13)
    pt1.font.bold = True
    pt1.font.color.rgb = COLOR_NAVY

    pt2 = ttf.add_paragraph()
    pt2.text = "Επιβλέπων: Παναγιώτης Μαράντης (pmaradis@isi.gr)  •  Dataset: UCC MISL (135 Traces, 174.523 δείγματα)  •  GitHub: github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting"
    pt2.font.size = Pt(10)
    pt2.font.color.rgb = COLOR_DARK_TEXT

    # Table of all 8 requirements
    req_headers = ["Ζητούμενο", "Βαρύτητα", "Αντικείμενο & Μεθοδολογία", "Κύριο Πειραματικό Εύρημα / Παραδοτέο"]
    req_rows = [
        ["Ζητούμενο 1", "10%", "Τηλεπικοινωνιακή σημασία πρόβλεψης Downlink Bitrate σε 5G/6G", "Μετάβαση από Reactive AMC σε Proactive Handover, Slicing & MEC ABR"],
        ["Ζητούμενο 2", "15%", "Προεπεξεργασία, καθαρισμός '-' & Session-Aware Split (135 traces)", "174.523 δείγματα: 106 Train traces (131.370s) / 29 Test traces (43.153s) — 0% Leakage"],
        ["Ζητούμενο 3", "15%", "Μοντέλο XGBoost Regressor σε Grid L ∈ {5,10,20,30}s, H ∈ {1,3,5,10}s", "Βέλτιστο L=10, H=1: RMSE = 6.344,8 kbps, MAE = 3.275,5 kbps, R² = 0.825"],
        ["Ζητούμενο 4", "10%", "Explainable AI (TreeSHAP): Beeswarm, Bar, Dependence & Waterfall", "Κυρίαρχοι δείκτες: UL_bitrate (9.259 kbps), RSSI (1.103 kbps), Distance (764 kbps)"],
        ["Ζητούμενο 5", "15%", "Βαθιά Μάθηση με PyTorch LSTM (Lookback L=64s) & Σύγκριση", "LSTM RMSE = 14.473,4 kbps vs XGBoost 6.344,8 kbps (-56,2% σφάλμα, 100x ταχύτερο)"],
        ["Ζητούμενο 6", "15% (Bonus)", "Foundation Model: IBM Granite Tiny Time Mixer (Zero-Shot & Fine-Tune)", "Zero-Shot RMSE 18.642 kbps → Fine-Tuned (4 εποχές) RMSE 8.426 kbps (-54,8%!)"],
        ["Ζητούμενο 7", "10%", "Σταδιακή Αφαίρεση Μεταβλητών (100% → 75% → 50% → 25% KPIs)", "Με 2 μόνο KPIs (25%) το RMSE μεταβάλλεται μόλις +0,7%, χρόνος train -28,1%"],
        ["Ζητούμενο 8", "10%", "5G Proactive Network Management & Ένταξη σε NWDAF / O-RAN RIC", "Recall 91,6% (Δt=1s) και 85,7% (Δt=5s) για κατώφλι SLA τ = 5 Mbps"]
    ]
    add_styled_table(
        slide2,
        Inches(0.6), Inches(2.48), Inches(12.133), Inches(4.35),
        req_headers, req_rows,
        col_widths=[Inches(1.45), Inches(1.15), Inches(4.6), Inches(4.933)],
        highlight_rows=[2, 5, 7],
        font_size=9.5
    )

    set_speaker_notes(slide2, """
Στη δεύτερη διαφάνεια παρουσιάζουμε τη συνολική δομή της εργασίας μας, η οποία εκπονήθηκε από τον Δημήτριο Τσανακτσή (Α.Μ. 1100736) και τον Ιάσωνα Δερβενή (Α.Μ. 1097437).
Έχουμε υλοποιήσει και τα 8 ζητούμενα της εκφώνησης, συμπεριλαμβανομένου του Bonus ερωτήματος με τα Foundation Models (IBM Granite TTM).
Στον πίνακα βλέπετε συνοπτικά τη μεθοδολογία και το βασικό ποσοτικό αποτέλεσμα για κάθε ζητούμενο.
""")

    # =========================================================================
    # SLIDE 3: Requirement 1 (Part A) - Wireless Channel Stochasticity
    # =========================================================================
    slide3 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 1 (10%): Στοχαστικότητα Καναλιού & Περιορισμοί Reactive Διαχείρισης",
        category="REQUIREMENT 1 — TELECOMMUNICATIONS MOTIVATION",
        slide_num=3,
        total_slides=total_slides
    )

    add_info_card(
        slide3, Inches(0.6), Inches(1.4), Inches(5.9), Inches(3.6),
        "Αιτίες Έντονης Διακύμανσης Throughput σε 5G NR / 6G",
        [
            "1. Κινητικότητα Χρήστη (High Mobility & Doppler Shift):",
            "   • Μετακίνηση με όχημα ή τρένο προκαλεί ταχύτατη μεταβολή της γεωμετρίας ζεύξης και συχνές εναλλαγές κυψέλης (Handovers).",
            "2. Υψηλές Συχνότητες (Sub-6 GHz & mmWave 24–40 GHz):",
            "   • Έντονη εξασθένηση διάδοσης (Path Loss) και απότομη σκίαση (Shadowing / NLoS Blockage) από κτίρια, οχήματα και εμπόδια.",
            "3. Δυναμικός Φόρτος Κυψέλης (PRB Contention):",
            "   • Στοχαστικός ανταγωνισμός πολλαπλών UEs για τα διαθέσιμα Physical Resource Blocks (PRBs) στον MAC Scheduler.",
            "4. Πολυδιαδρομική Διάδοση (Multipath Fast Fading):",
            "   • Καταστρεπτικές συμβολές σημάτων σε κλίμακα χιλιοστοδευτερολέπτων."
        ],
        accent_color=COLOR_NAVY,
        font_size=10
    )

    add_info_card(
        slide3, Inches(6.8), Inches(1.4), Inches(5.933), Inches(3.6),
        "Αναδρομική (Reactive) vs Προληπτική (Proactive) Διαχείριση",
        [
            "❌ Παραδοσιακή Αναδρομική Προσέγγιση (Reactive):",
            "   • Το δίκτυο αντιδρά αφού πρώτα καταγραφεί πτώση SINR ή απώλεια πακέτων (HARQ NACKs).",
            "   • Οδηγεί σε καθυστερημένο Handover (Radio Link Failure - RLF), TCP congestion window reset και πάγωμα βίντεο (buffer underrun).",
            "✅ Προτεινόμενη Προληπτική Προσέγγιση (Proactive ML/DL):",
            "   • Πρόβλεψη του Downlink Bitrate σε ορίζοντα H = 1 έως 15 δευτερολέπτων πριν την κατάρρευση του καναλιού.",
            "   • Παρέχει κρίσιμο χρόνο αντίδρασης (Lead Time Δt) στα συστήματα 3GPP NWDAF και O-RAN Near-RT RIC."
        ],
        accent_color=COLOR_ACCENT,
        font_size=10
    )

    # Bottom comparison table / callouts
    add_kpi_card(slide3, Inches(0.6), Inches(5.2), Inches(2.85), Inches(1.55), "Sub-6 & mmWave", "Ευαισθησία Blockage", "Απότομες πτώσεις >15 dB σε NLoS", COLOR_CORAL)
    add_kpi_card(slide3, Inches(3.68), Inches(5.2), Inches(2.85), Inches(1.55), "1s – 15s Ahead", "Ορίζοντας Πρόβλεψης", "Έγκαιρη ενημέρωση MAC / RIC", COLOR_NAVY)
    add_kpi_card(slide3, Inches(6.76), Inches(5.2), Inches(2.85), Inches(1.55), "Zero RLF", "Στόχος Κινητικότητας", "Προ-συγχρονισμός Target gNodeB", COLOR_ACCENT)
    add_kpi_card(slide3, Inches(9.84), Inches(5.2), Inches(2.89), Inches(1.55), "eMBB & URLLC", "Εγγύηση SLA / QoS", "Προληπτική δέσμευση PRBs", COLOR_BLUE)

    set_speaker_notes(slide3, """
Στο 1ο Ζητούμενο εξετάζουμε γιατί η πρόβλεψη του Downlink Bitrate είναι θεμελιώδης στα δίκτυα 5G και 6G.
Το ασύρματο κανάλι είναι έντονα στοχαστικό λόγω της κινητικότητας του χρήστη, των φαινομένων Doppler, της σκίασης σε υψηλές συχνότητες και της συμφόρησης των PRBs.
Η κλασική αναδρομική (reactive) προσέγγιση αντιδρά κατόπιν εορτής, όταν ήδη έχουν χαθεί πακέτα ή έχει συμβεί Radio Link Failure.
Αντίθετα, η προληπτική πρόβλεψη 1 έως 15 δευτερόλεπτα νωρίτερα επιτρέπει στο δίκτυο να δράσει πριν ο χρήστης αντιληφθεί οποιαδήποτε υποβάθμιση.
""")

    # =========================================================================
    # SLIDE 4: Requirement 1 (Part B) - 4 Telecom Use Cases & Architecture Fig 13
    # =========================================================================
    slide4 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 1 (10%): Εφαρμογές Προληπτικής Πρόβλεψης & Αρχιτεκτονική Ελέγχου",
        category="REQUIREMENT 1 — PROACTIVE 5G USE CASES & PARADIGM SHIFT",
        slide_num=4,
        total_slides=total_slides
    )

    add_info_card(
        slide4, Inches(0.6), Inches(1.38), Inches(5.35), Inches(5.42),
        "4 Κύριες Τηλεπικοινωνιακές Εφαρμογές Προληπτικού Ελέγχου",
        [
            "1. Προληπτικό Handover & Beam Management (Δt ≥ 1–2s):",
            "   • Προ-συγχρονισμός UE context με τον Candidate Target gNB μέσω διεπαφής Xn πριν επέλθει Radio Link Failure (RLF).",
            "2. Δυναμική Κράτηση PRBs & Network Slicing (Δt ≥ 2–3s):",
            "   • Προληπτική δέσμευση επιπλέον Physical Resource Blocks (PRBs) στον MAC Scheduler για εγγύηση SLA σε eMBB/URLLC slices.",
            "3. MEC Video Streaming ABR / DASH Adaptation (Δt ≥ 3–5s):",
            "   • Προ-φόρτωση (pre-fetching) τμημάτων βίντεο στο buffer ή ομαλή προσαρμογή ανάλυσης χωρίς πάγωμα εικόνας (zero stall).",
            "4. Dual Connectivity (EN-DC / NR-DC) Steering (Δt ≥ 5–10s):",
            "   • Έγκαιρη δρομολόγηση πακέτων μέσω Secondary Cell Group (SCG) πριν καταρρεύσει ο κύριος ραδιοσύνδεσμος."
        ],
        accent_color=COLOR_NAVY, font_size=9.2
    )

    if (FIGURES_DIR / "13_5g_reactive_vs_proactive_arch.png").exists():
        slide4.shapes.add_picture(str(FIGURES_DIR / "13_5g_reactive_vs_proactive_arch.png"), Inches(6.1), Inches(1.42), width=Inches(6.63))

    set_speaker_notes(slide4, """
Εδώ αναλύουμε τους 4 βασικούς τηλεπικοινωνιακούς πυλώνες όπου αξιοποιείται η πρόβλεψη του Downlink Bitrate:
Πρώτον, στο Predictive Handover και Beam Management, όπου με προειδοποίηση 1-2 δευτερολέπτων αποφεύγουμε το Radio Link Failure.
Δεύτερον, στη δυναμική κράτηση PRBs για εγγύηση SLA σε Network Slices.
Τρίτον, στο Edge Video Streaming (ABR/DASH), όπου προ-γεμίζουμε το buffer πριν το όχημα μπει σε περιοχή χαμηλής κάλυψης.
Και τέταρτον, στο Dual Connectivity Traffic Steering για έγκαιρη δρομολόγηση πακέτων μέσω δευτερεύουσας κυψέλης.
""")

    # =========================================================================
    # SLIDE 5: Requirement 2 (Part A) - Dataset & Mobility Breakdown Table
    # =========================================================================
    slide5 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 2 (15%): Ανάλυση του UCC 4G/LTE & 5G Dataset (135 Traces)",
        category="REQUIREMENT 2 — DATASET & MOBILITY SCENARIOS",
        slide_num=5,
        total_slides=total_slides
    )

    # Left: Native Table of Mobility Scenarios
    mob_headers = ["Σενάριο Κίνησης", "Αριθμός Traces", "Δείγματα (1s)", "Ποσοστό (%)", "Χαρακτηριστικά Κίνησης & Καναλιού"]
    mob_rows = [
        ["Car (Αυτοκίνητο)", "53", "75.874", "43,48%", "Υψηλή ταχύτητα (έως 120 km/h), συχνά handovers, μεταβαλλόμενο SNR"],
        ["Train (Τρένο)", "20", "38.976", "22,33%", "Πολύ υψηλή ταχύτητα, έντονο Doppler shift, περιοχές αγροτικής κάλυψης"],
        ["Pedestrian (Πεζός)", "31", "33.629", "19,27%", "Χαμηλή ταχύτητα (<6 km/h), αστική σκίαση (urban canyon shadowing)"],
        ["Static (Στατικός)", "15", "15.261", "8,74%", "Μηδενική ταχύτητα, διακυμάνσεις κυρίως λόγω μεταβολής φόρτου κυψέλης"],
        ["Bus (Λεωφορείο)", "16", "10.783", "6,18%", "Αστική κίνηση με συχνές στάσεις, εναλλαγές LoS / NLoS"],
        ["ΣΥΝΟΛΟ DATASET", "135", "174.523", "100,0%", "> 48,5 ώρες πραγματικής τηλεμετρίας (1 δείγμα/δευτερόλεπτο)"]
    ]
    add_styled_table(
        slide5,
        Inches(0.6), Inches(1.38), Inches(6.3), Inches(3.75),
        mob_headers, mob_rows,
        col_widths=[Inches(1.35), Inches(0.85), Inches(0.95), Inches(0.85), Inches(2.3)],
        highlight_rows=[5],
        font_size=8.8
    )

    # KPI Callouts under table on left
    add_kpi_card(slide5, Inches(0.6), Inches(5.3), Inches(2.0), Inches(1.45), "174.523", "Συνολικά Δείγματα", "Ρυθμός 1 Hz (48,5 ώρες)", COLOR_NAVY)
    add_kpi_card(slide5, Inches(2.75), Inches(5.3), Inches(2.0), Inches(1.45), "10,8 Mbps", "Μέσο DL Bitrate", "Max: 173,0 Mbps", COLOR_ACCENT)
    add_kpi_card(slide5, Inches(4.9), Inches(5.3), Inches(2.0), Inches(1.45), "5 Σενάρια", "Κινητικότητα Χρήστη", "Car, Train, Ped, Static, Bus", COLOR_BLUE)

    # Right: Figure 01 EDA Distributions
    if (FIGURES_DIR / "01_eda_distributions.png").exists():
        slide5.shapes.add_picture(str(FIGURES_DIR / "01_eda_distributions.png"), Inches(7.05), Inches(1.45), width=Inches(5.68))

    set_speaker_notes(slide5, """
Στο 2ο Ζητούμενο παρουσιάζουμε το σύνολο δεδομένων πραγματικών κυψελωτών μετρήσεων του University College Cork (UCC MISL).
Ενώσαμε και τα 135 αρχεία CSV από τα 5 σενάρια κινητικότητας: Αυτοκίνητο (43,5%), Τρένο (22,3%), Πεζός (19,3%), Στατικός χρήστης (8,7%) και Λεωφορείο (6,2%).
Συνολικά προέκυψαν 174.523 δείγματα με χρονική ανάλυση 1 δευτερολέπτου, δηλαδή πάνω από 48,5 ώρες πραγματικής κίνησης.
Στο δεξί διάγραμμα φαίνονται οι κατανομές του Downlink Bitrate (με έντονη δεξιά ασυμμετρία, μέση τιμή 10,8 Mbps και μέγιστο 173 Mbps) καθώς και των βασικών ραδιοδεικτών.
""")

    # =========================================================================
    # SLIDE 6: Requirement 2 (Part B) - The 8 Radio KPIs Native Table + Fig 16
    # =========================================================================
    slide6 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 2 (15%): Οι 8 Ραδιοδείκτες Ποιότητας Καναλιού & Προφίλ Κινητικότητας",
        category="REQUIREMENT 2 — RADIO CHANNEL QUALITY METRICS & KINEMATICS",
        slide_num=6,
        total_slides=total_slides
    )

    kpi_headers = ["Μεταβλητή (KPI)", "Ρόλος", "Μονάδα", "Εύρος", "Τηλεπικοινωνιακή & Φυσική Σημασία στα Δίκτυα 4G/5G"]
    kpi_rows = [
        ["DL_bitrate", "Target (y)", "kbps", "0 – 173k", "Ρυθμός μετάδοσης Downlink (Throughput) — στόχος πρόβλεψης."],
        ["UL_bitrate", "Input #1", "kbps", "0 – 48,5k", "Ρυθμός Uplink: ενεργή ροή TCP ACKs και αμφίδρομος φόρτος συνεδρίας."],
        ["RSSI", "Input #2", "dBm", "-113.. -51", "Received Signal Strength Indicator: συνολική ευρυζωνική ισχύς."],
        ["ServingCell_Distance", "Input #3", "m", "15 – 25k+", "Απόσταση UE από Serving gNB: καθορίζει το Macro Path Loss."],
        ["Speed", "Input #4", "km/h", "0 – 145", "Ταχύτητα κίνησης UE: συνδέεται με Doppler spread & handovers."],
        ["SNR", "Input #5", "dB", "-20.. +35", "Signal-to-Noise Ratio: όριο χωρητικότητας Shannon C = B·log2(1+SNR)."],
        ["RSRQ", "Input #6", "dB", "-20.. -3", "Reference Signal Received Quality: αποτυπώνει συμφόρηση PRBs."],
        ["CQI", "Input #7", "4-bit", "1 – 15", "Channel Quality Indicator: επιλογή Modulation & Coding (MCS)."],
        ["RSRP", "Input #8", "dBm", "-140.. -44", "Reference Signal Received Power: ισχύς σημάτων αναφοράς."]
    ]
    add_styled_table(
        slide6,
        Inches(0.6), Inches(1.38), Inches(6.25), Inches(5.42),
        kpi_headers, kpi_rows,
        col_widths=[Inches(1.42), Inches(0.78), Inches(0.68), Inches(0.82), Inches(2.55)],
        highlight_rows=[0, 1, 2],
        font_size=8.3
    )

    if (FIGURES_DIR / "16_dataset_mobility_breakdown.png").exists():
        slide6.shapes.add_picture(str(FIGURES_DIR / "16_dataset_mobility_breakdown.png"), Inches(6.98), Inches(1.40), height=Inches(2.68))

    if (FIGURES_DIR / "02_eda_mobility_comparison.png").exists():
        slide6.shapes.add_picture(str(FIGURES_DIR / "02_eda_mobility_comparison.png"), Inches(6.98), Inches(4.20), height=Inches(2.68))

    set_speaker_notes(slide6, """
Στην 6η διαφάνεια παρουσιάζουμε αναλυτικά τη μεταβλητή-στόχο (DL_bitrate) και τις 8 αριθμητικές μετρικές ποιότητας και πλαισίου (Channel & Context KPIs) που χρησιμοποιούνται ως είσοδοι στα μοντέλα μας.
Δεξιά βλέπουμε το στατιστικό προφίλ των 5 σεναρίων κινητικότητας (κατανομή Train/Test traces, μέσο throughput έναντι ταχύτητας κίνησης, violin plots και πίνακα συσχέτισης Pearson).
""")

    # =========================================================================
    # SLIDE 7: Requirement 2 (Part C) - Preprocessing & Session-Aware Split
    # =========================================================================
    slide7 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 2 (15%): Καθαρισμός Δεδομένων & Αποτροπή Data Leakage",
        category="REQUIREMENT 2 — PREPROCESSING PIPELINE",
        slide_num=7,
        total_slides=total_slides
    )

    add_info_card(
        slide7, Inches(0.6), Inches(1.4), Inches(5.35), Inches(5.35),
        "Αυστηρή Μεθοδολογία Προεπεξεργασίας (src/data_processing.py)",
        [
            "1. Αντικατάσταση Missing Symbols ('-'):",
            "   • Στα ακατέργαστα CSV, οι ελλείπουσες τιμές (π.χ. σε CQI, RSSI, ServingCell_Distance) συμβολίζονται με '-'.",
            "   • Μετατροπή σε NaN και εφαρμογή Session-Aware Forward-Fill (ffill) & Backward-Fill (bfill) αυστηρά εντός του ίδιου trace_id.",
            "2. Session-Aware Train/Test Split (80% / 20% ανά Trace):",
            "   • Ένα τυχαίο ανακάτεμα γραμμών θα προκαλούσε σοβαρό χρονικό Data Leakage μεταξύ t και t+1!",
            "   • Χωρίσαμε τα δεδομένα σε επίπεδο ολόκληρων συνεδριών:",
            "     – Train Set: 106 traces → 131.370 δείγματα (80%)",
            "     – Test Set: 29 traces → 43.153 δείγματα (20%)",
            "3. Κανονικοποίηση (StandardScaler):",
            "   • Fit αποκλειστικά στο Train Set (μ, σ) και transform στο Test Set."
        ],
        accent_color=COLOR_NAVY,
        font_size=9.3
    )

    if (FIGURES_DIR / "14_preprocessing_pipeline_diagram.png").exists():
        slide7.shapes.add_picture(str(FIGURES_DIR / "14_preprocessing_pipeline_diagram.png"), Inches(6.1), Inches(1.45), width=Inches(6.63))
    elif (FIGURES_DIR / "02_eda_mobility_comparison.png").exists():
        slide7.shapes.add_picture(str(FIGURES_DIR / "02_eda_mobility_comparison.png"), Inches(6.1), Inches(1.45), width=Inches(6.63))

    set_speaker_notes(slide7, """
Ένα από τα πιο κρίσιμα σημεία της προεπεξεργασίας είναι η αποτροπή του χρονικού Data Leakage.
Πρώτον, καθαρίσαμε τους χαρακτήρες '-' εφαρμόζοντας forward-fill και backward-fill αποκλειστικά μέσα στο ίδιο trace_id, ώστε να μην μεταφέρεται πληροφορία από μία διαδρομή σε άλλη.
Δεύτερον, αντί για τυχαίο διαχωρισμό γραμμών, εφαρμόσαμε Session-Aware Split σε επίπεδο ολόκληρων traces: 106 traces (131.370 δείγματα) για εκπαίδευση και 29 εντελώς αθέατα traces (43.153 δείγματα) για αξιολόγηση.
Τρίτον, ο StandardScaler προσαρμόστηκε μόνο στο Train Set.
""")

    # =========================================================================
    # SLIDE 8: Requirement 3 (Part A) - XGBoost Sliding Window & Visuals
    # =========================================================================
    slide8 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 3 (15%): Πρόβλεψη με XGBoost Regressor & Κυλιόμενα Παράθυρα",
        category="REQUIREMENT 3 — MACHINE LEARNING FORECASTING",
        slide_num=8,
        total_slides=total_slides
    )

    add_info_card(
        slide8, Inches(0.6), Inches(1.38), Inches(4.55), Inches(3.7),
        "Κατασκευή Κυλιόμενων Παραθύρων (Sliding Windows)",
        [
            "• Για κάθε συνεχή καταγραφή εντός του ίδιου trace_id, ορίζουμε παράθυρο ιστορικού Lookback L και ορίζοντα πρόβλεψης Horizon H:",
            "   X_t = [x_{t-L+1}, ..., x_t] ∈ R^(L×8)  →  y_t = DL_bitrate_{t+H}",
            "• Εξετάστηκαν 16 συνδυασμοί (πλήρες Grid 4×4):",
            "   – Lookback L ∈ {5, 10, 20, 30} δευτερόλεπτα",
            "   – Horizon H ∈ {1, 3, 5, 10} δευτερόλεπτα μπροστά",
            "• Αρχιτεκτονική XGBoost Regressor:",
            "   – n_estimators = 100, max_depth = 6, lr = 0.08, tree_method = 'hist'",
            "• Βέλτιστο Σημείο Λειτουργίας (L=10s, H=1s):",
            "   – Η αύξηση του L πέραν των 10s προσφέρει < 0,2% κέρδος σε RMSE."
        ],
        accent_color=COLOR_NAVY,
        font_size=9.0
    )

    # 3 KPI Cards under left card
    add_kpi_card(slide8, Inches(0.6), Inches(5.22), Inches(1.44), Inches(1.52), "6.344,8", "RMSE (kbps)", "L=10s, H=1s", COLOR_ACCENT)
    add_kpi_card(slide8, Inches(2.15), Inches(5.22), Inches(1.44), Inches(1.52), "3.275,5", "MAE (kbps)", "Μέσο Σφάλμα", COLOR_NAVY)
    add_kpi_card(slide8, Inches(3.70), Inches(5.22), Inches(1.45), Inches(1.52), "R² = 0.825", "Κάλυψη", "0,6 μs/δείγμα", COLOR_BLUE)

    if (FIGURES_DIR / "15_sliding_window_mechanism.png").exists():
        slide8.shapes.add_picture(str(FIGURES_DIR / "15_sliding_window_mechanism.png"), Inches(5.35), Inches(1.38), height=Inches(2.68))

    if (FIGURES_DIR / "03_xgboost_horizons_lookback.png").exists():
        slide8.shapes.add_picture(str(FIGURES_DIR / "03_xgboost_horizons_lookback.png"), Inches(5.35), Inches(4.18), height=Inches(2.68))

    set_speaker_notes(slide8, """
Στο 3ο Ζητούμενο αναπτύξαμε το μοντέλο παλινδρόμησης XGBoost Regressor πάνω σε κυλιόμενα παράθυρα χρόνου (Sliding Windows).
Κάθε διάνυσμα εισόδου περιέχει τις τιμές των 8 ραδιοδεικτών για τα τελευταία L δευτερόλεπτα (διάσταση L επί 8) και προβλέπει το Downlink Bitrate μετά από H δευτερόλεπτα.
Στο δεξί σχήμα βλέπουμε πώς μεταβάλλονται τα RMSE και MAE για όλα τα L και H, καθώς και την εξαιρετική σύμπτωση της προβλεπόμενης τροχιάς (κόκκινη διακεκομμένη γραμμή) με την πραγματική κίνηση (μπλε γραμμή) στο Test Set.
Για L=10 και H=1 επιτυγχάνουμε R² = 0.825, RMSE = 6.344,8 kbps και χρόνο συμπερασμού κάτω από 1 μικροδευτερόλεπτο ανά δείγμα.
""")

    # =========================================================================
    # SLIDE 9: Requirement 3 (Part B) - Full 16-Row XGBoost Grid Table
    # =========================================================================
    slide9 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 3 (15%): Πλήρης Πίνακας Πειραματικού Πλέγματος XGBoost (16 Συνδυασμοί)",
        category="REQUIREMENT 3 — LOOKBACK & HORIZON SENSITIVITY GRID",
        slide_num=9,
        total_slides=total_slides
    )

    grid_headers = ["Lookback L (s)", "Horizon H (s)", "Διάσταση Εισόδου (L×8)", "RMSE (kbps)", "MAE (kbps)", "R² Score", "Χρόνος Train (s)", "Inference (μs/δείγμα)"]
    grid_rows = [
        ["5 s", "1 s", "40 features", "6.443,14", "3.298,32", "0.8191", "0,59 s", "0,6 μs"],
        ["5 s", "3 s", "40 features", "7.603,29", "4.120,36", "0.7481", "1,38 s", "1,0 μs"],
        ["5 s", "5 s", "40 features", "8.264,89", "4.581,98", "0.7025", "0,97 s", "0,9 μs"],
        ["5 s", "10 s", "40 features", "8.948,20", "5.026,15", "0.6515", "1,02 s", "0,8 μs"],
        ["10 s (Βέλτιστο)", "1 s", "80 features", "6.344,75", "3.275,46", "0.8247", "1,30 s", "0,6 μs"],
        ["10 s", "3 s", "80 features", "7.503,15", "3.997,99", "0.7548", "2,58 s", "0,7 μs"],
        ["10 s", "5 s", "80 features", "7.961,68", "4.345,59", "0.7241", "1,35 s", "0,9 μs"],
        ["10 s", "10 s", "80 features", "9.112,46", "5.111,83", "0.6391", "1,23 s", "0,6 μs"],
        ["20 s", "1 s", "160 features", "6.334,49", "3.279,33", "0.8257", "2,04 s", "1,2 μs"],
        ["20 s", "3 s", "160 features", "7.322,81", "3.974,25", "0.7672", "2,12 s", "1,3 μs"],
        ["20 s", "5 s", "160 features", "7.979,94", "4.359,93", "0.7238", "3,06 s", "1,1 μs"],
        ["20 s", "10 s", "160 features", "8.795,09", "4.922,86", "0.6653", "2,42 s", "1,3 μs"],
        ["30 s", "1 s", "240 features", "6.352,31", "3.255,53", "0.8255", "3,36 s", "0,9 μs"],
        ["30 s", "3 s", "240 features", "7.423,96", "3.952,57", "0.7618", "3,24 s", "1,2 μs"],
        ["30 s", "5 s", "240 features", "7.970,30", "4.337,05", "0.7256", "3,14 s", "1,4 μs"],
        ["30 s", "10 s", "240 features", "8.985,17", "4.977,16", "0.6520", "3,59 s", "1,4 μs"]
    ]
    add_styled_table(
        slide9,
        Inches(0.6), Inches(1.32), Inches(12.133), Inches(5.55),
        grid_headers, grid_rows,
        col_widths=[Inches(1.65), Inches(1.25), Inches(1.65), Inches(1.55), Inches(1.55), Inches(1.35), Inches(1.5), Inches(1.633)],
        highlight_rows=[4, 8],
        font_size=8.3
    )

    set_speaker_notes(slide9, """
Στην 9η διαφάνεια παραθέτουμε τον πλήρη πίνακα και των 16 πειραματικών συνδυασμών Lookback (L = 5, 10, 20, 30 δευτερόλεπτα) και Horizon (H = 1, 3, 5, 10 δευτερόλεπτα).
Παρατηρούμε δύο βασικά φαινόμενα:
Πρώτον, καθώς ο ορίζοντας H αυξάνεται από 1s σε 10s, το σφάλμα RMSE αυξάνεται μονοτονικά από ~6,34 Mbps σε ~9,11 Mbps και το R² υποχωρεί από 0.825 σε 0.639 λόγω της στοχαστικότητας του ασύρματου διαύλου.
Δεύτερον, η αύξηση του παραθύρου L από 10s σε 20s ή 30s βελτιώνει το RMSE λιγότερο από 0,16% (από 6.344,75 σε 6.334,49 kbps), ενώ τριπλασιάζει τα χαρακτηριστικά εισόδου (από 80 σε 240) και τον χρόνο εκπαίδευσης. Άρα το L=10 αποτελεί τη βέλτιστη επιλογή Pareto.
""")

    # =========================================================================
    # SLIDE 10: Requirement 4 (Part A) - TreeSHAP Global Ranking & Table
    # =========================================================================
    slide10 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 4 (10%): Επεξηγήσιμη Τεχνητή Νοημοσύνη (TreeSHAP) — Κατάταξη KPIs",
        category="REQUIREMENT 4 — EXPLAINABLE AI (TREESHAP)",
        slide_num=10,
        total_slides=total_slides
    )

    shap_headers = ["Κατάταξη", "Ραδιοδείκτης (KPI)", "Συνολικό Mean |SHAP| (kbps)", "Μερίδιο Επιρροής (%)", "Κορυφαίο Lag", "Τηλεπικοινωνιακή Ερμηνεία Σπουδαιότητας"]
    shap_rows = [
        ["#1", "UL_bitrate", "9.259,05 kbps", "65,85%", "UL_bitrate_t (6.475,7)", "Κυρίαρχος δείκτης: ενεργή ροή TCP ACKs και αμφίδρομη κίνηση συνεδρίας"],
        ["#2", "RSSI", "1.102,90 kbps", "7,84%", "RSSI_t (632,0)", "Συνολική λαμβανόμενη ενέργεια στο εύρος ζώνης του φέροντος"],
        ["#3", "ServingCell_Distance", "764,36 kbps", "5,44%", "Distance_t (181,5)", "Αποτυπώνει την εξασθένηση μεγάλης κλίμακας (Macro Path Loss)"],
        ["#4", "Speed", "754,83 kbps", "5,37%", "Speed_t-1 (153,6)", "Η ταχύτητα οχήματος καθορίζει το Doppler shift και τον ρυθμό handovers"],
        ["#5", "SNR", "739,19 kbps", "5,26%", "SNR_t (355,8)", "Καθορίζει το ανώτατο όριο χωρητικότητας Shannon και την τάξη QAM"],
        ["#6", "RSRQ", "565,73 kbps", "4,02%", "RSRQ_t (167,7)", "Δείκτης παρεμβολών γειτονικών κυψελών και φόρτου PRB"],
        ["#7", "CQI", "490,00 kbps", "3,48%", "CQI_t (235,3)", "Κβαντισμένος δείκτης 1–15 (συγχωνεύεται μερικώς από το συνεχές SNR)"],
        ["#8", "RSRP", "385,33 kbps", "2,74%", "RSRP_t (88,4)", "Υπερκαλύπτεται από τον συνδυασμό RSSI, RSRQ και ServingCell_Distance"]
    ]
    add_styled_table(
        slide10,
        Inches(0.6), Inches(1.38), Inches(6.95), Inches(5.4),
        shap_headers, shap_rows,
        col_widths=[Inches(0.72), Inches(1.35), Inches(1.18), Inches(0.88), Inches(1.15), Inches(1.67)],
        highlight_rows=[0, 1],
        font_size=8.4
    )

    if (FIGURES_DIR / "05_shap_feature_importance.png").exists():
        slide10.shapes.add_picture(str(FIGURES_DIR / "05_shap_feature_importance.png"), Inches(7.7), Inches(1.5), width=Inches(5.03))

    set_speaker_notes(slide10, """
Στο 4ο Ζητούμενο εφαρμόσαμε την τεχνική TreeSHAP (ακριβής υπολογισμός τιμών Shapley από τη θεωρία συνεργατικών παιγνίων) πάνω στο εκπαιδευμένο μοντέλο XGBoost (L=10, H=1) σε 1.500 δείγματα του Test Set.
Στον πίνακα βλέπουμε την κατάταξη και των 8 ραδιοδεικτών αθροίζοντας τη μέση απόλυτη τιμή SHAP σε όλα τα χρονικά lags (t έως t-9).
Το UL_bitrate κυριαρχεί με 9.259 kbps (65,85% της συνολικής επιρροής), καθώς στις συνδέσεις TCP η ροή λήψης (Downlink) συνοδεύεται άμεσα από ροή επιβεβαιώσεων (Uplink TCP ACKs).
Ακολουθούν το RSSI (1.102,9 kbps), η απόσταση από τον σταθμό βάσης (764,4 kbps), η ταχύτητα κίνησης (754,8 kbps) και το SNR (739,2 kbps).
""")

    # =========================================================================
    # SLIDE 11: Requirement 4 (Part B) - Beeswarm & Dependence Plots
    # =========================================================================
    slide11 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 4 (10%): Κατανομή SHAP Beeswarm & Μη-Γραμμικές Αλληλεπιδράσεις",
        category="REQUIREMENT 4 — BEESWARM & DEPENDENCE ANALYSIS",
        slide_num=11,
        total_slides=total_slides
    )

    if (FIGURES_DIR / "04_shap_summary_beeswarm.png").exists():
        slide11.shapes.add_picture(str(FIGURES_DIR / "04_shap_summary_beeswarm.png"), Inches(0.6), Inches(1.4), width=Inches(5.95))

    if (FIGURES_DIR / "06_shap_dependence_plots.png").exists():
        slide11.shapes.add_picture(str(FIGURES_DIR / "06_shap_dependence_plots.png"), Inches(6.7), Inches(1.4), width=Inches(6.03))

    add_info_card(
        slide11, Inches(0.6), Inches(5.05), Inches(12.133), Inches(1.8),
        "Φυσική Ερμηνεία των Διαγραμμάτων Beeswarm (Αριστερά) & Dependence (Δεξιά)",
        [
            "• Beeswarm Plot: Κάθε κουκκίδα είναι ένα δείγμα δοκιμής. Οι υψηλές τιμές (κόκκινο χρώμα) στα UL_bitrate_t, RSSI_t, SNR_t και CQI_t ωθούν την πρόβλεψη έντονα προς τα δεξιά (+SHAP έως +40 Mbps), ενώ οι χαμηλές τιμές (μπλε) μειώνουν το αναμενόμενο throughput.",
            "• Καμπύλη Κορεσμού SNR & CQI: Στο Dependence Plot φαίνεται ότι για SNR < 0 dB η συνεισφορά είναι αρνητική, αυξάνεται απότομα μεταξύ 5 dB και 20 dB (μετάβαση από QPSK σε 64-QAM/256-QAM) και εμφανίζει πλατό κορεσμού άνω των 22 dB.",
            "• Επίδραση Κινητικότητας (Speed & Distance): Μεγάλες αποστάσεις (> 3 km) και υψηλές ταχύτητες (> 80 km/h) ασκούν συστηματική αρνητική πίεση (-SHAP) λόγω path loss και συχνών handovers."
        ],
        accent_color=COLOR_NAVY,
        font_size=9.2
    )

    set_speaker_notes(slide11, """
Στην 11η διαφάνεια εξετάζουμε το Beeswarm plot (αριστερά) και τα Dependence plots (δεξιά).
Στο Beeswarm plot βλέπουμε όχι μόνο το μέγεθος αλλά και το πρόσημο της επίδρασης: υψηλές τιμές SNR, RSSI και CQI (κόκκινες κουκκίδες) αυξάνουν το προβλεπόμενο throughput, ενώ υψηλές τιμές στο ServingCell_Distance μειώνουν τον ρυθμό μετάδοσης.
Στα Dependence plots δεξιά αναδεικνύεται η μη-γραμμική σχέση Shannon/AMC: η επίδραση του SNR ανεβαίνει ραγδαία στη ζώνη 5 έως 20 dB όπου το 5G αλλάζει διαμόρφωση από QPSK σε 64-QAM και 256-QAM.
""")

    # =========================================================================
    # SLIDE 12: Requirement 4 (Part C) - Local Explanations (Waterfall Plots)
    # =========================================================================
    slide12 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 4 (10%): Τοπική Ερμηνεία Αποφάσεων — SHAP Waterfall Plots",
        category="REQUIREMENT 4 — LOCAL EXPLAINABILITY (CASE STUDIES)",
        slide_num=12,
        total_slides=total_slides
    )

    if (FIGURES_DIR / "07_shap_waterfall_local.png").exists():
        slide12.shapes.add_picture(str(FIGURES_DIR / "07_shap_waterfall_local.png"), Inches(0.6), Inches(1.4), width=Inches(12.133))

    add_info_card(
        slide12, Inches(0.6), Inches(4.85), Inches(5.9), Inches(1.95),
        "Περίπτωση Α (Αριστερά): Στιγμιότυπο Υψηλού Ρυθμού (Peak Burst)",
        [
            "• Βασική τιμή αναφοράς μοντέλου: E[f(X)] ≈ 10,8 Mbps.",
            "• Η συνδυασμένη παρουσία ισχυρού UL_bitrate_t (+2,55σ), υψηλού RSSI_t (+1,42σ) και εξαιρετικού SNR_t ωθεί την πρόβλεψη πάνω από τα 45 Mbps.",
            "• Επιβεβαιώνει ότι το μοντέλο αναγνωρίζει συνθήκες Line-of-Sight (LoS) κοντά στον σταθμό βάσης."
        ],
        accent_color=COLOR_ACCENT,
        font_size=9.2
    )

    add_info_card(
        slide12, Inches(6.8), Inches(4.85), Inches(5.933), Inches(1.95),
        "Περίπτωση Β (Δεξιά): Στιγμιότυπο Κατάρρευσης Ζεύξης (Congestion / Drop)",
        [
            "• Χαμηλή ενεργή κίνηση UL_bitrate_t (-0,42σ), υποβαθμισμένο RSSI_t (-1,18σ) και χαμηλό CQI/SNR ωθούν αρνητικά την πρόβλεψη.",
            "• Η τελική πρόβλεψη πέφτει κάτω από το όριο SLA των 5.000 kbps (~1,2 Mbps).",
            "• Στο O-RAN RIC, το Waterfall plot εξηγεί στον μηχανικό δικτύου αν η πτώση οφείλεται σε κάλυψη (RSRP/Distance) ή συμφόρηση (RSRQ)."
        ],
        accent_color=COLOR_CORAL,
        font_size=9.2
    )

    set_speaker_notes(slide12, """
Στη 12η διαφάνεια παρουσιάζουμε την τοπική επεξηγησιμότητα (Local Explainability) μέσω των διαγραμμάτων καταρράκτη (SHAP Waterfall) για δύο ακραία στιγμιότυπα.
Αριστερά βλέπουμε πώς το μοντέλο ξεκινά από τη μέση τιμή E[f(X)] = 10,8 Mbps και, λόγω υψηλού UL_bitrate, RSSI και SNR, καταλήγει σε πρόβλεψη υψηλού throughput.
Δεξιά βλέπουμε ένα επεισόδιο υποβάθμισης, όπου το χαμηλό RSSI και το κακό SNR ρίχνουν την πρόβλεψη κάτω από τα 2 Mbps. Αυτή η διαφάνεια είναι πολύτιμη για ένα σύστημα O-RAN RIC, ώστε ο πάροχος να γνωρίζει την ακριβή αιτία κάθε συναγερμού.
""")

    # =========================================================================
    # SLIDE 13: Requirement 5 - Deep Learning (PyTorch LSTM)
    # =========================================================================
    slide13 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 5 (15%): Πρόβλεψη Χρονοσειρών με Βαθιά Μάθηση (PyTorch LSTM)",
        category="REQUIREMENT 5 — DEEP LEARNING TIME-SERIES FORECASTER",
        slide_num=13,
        total_slides=total_slides
    )

    add_info_card(
        slide13, Inches(0.6), Inches(1.4), Inches(5.65), Inches(3.75),
        "Αρχιτεκτονική & Υπερπαράμετροι Δικτύου LSTM (src/models_dl.py)",
        [
            "• Είσοδος Χρονοσειράς (Sequence Input):",
            "   – Παράθυρο Lookback L = 64 δευτερόλεπτα × 8 ραδιοδείκτες → Τανυστής (Batch, 64, 8).",
            "• Επαναληπτικά Επίπεδα (Recurrent Backbone):",
            "   – 2 στοιβαγμένα επίπεδα LSTM (num_layers = 2) με hidden_dim = 64 κρυφές μονάδες.",
            "   – Inter-layer Dropout = 0.2 για αποτροπή υπερπροσαρμογής (overfitting).",
            "• Κεφαλή Παλινδρόμησης (Projection Head):",
            "   – Linear(64 → 32) → ReLU → Dropout(0.2) → Linear(32 → 1).",
            "• Διαδικασία Εκπαίδευσης:",
            "   – Optimizer: Adam (lr = 0.001, weight_decay = 1e-5) + ReduceLROnPlateau.",
            "   – Batch Size = 256, 12 εποχές με Early Stopping & Gradient Clipping (max_norm = 1.0)."
        ],
        accent_color=COLOR_NAVY,
        font_size=9.2
    )

    add_kpi_card(slide13, Inches(0.6), Inches(5.3), Inches(1.8), Inches(1.45), "14.473,4", "LSTM RMSE (kbps)", "Έναντι 6.344,8 του XGBoost", COLOR_CORAL)
    add_kpi_card(slide13, Inches(2.52), Inches(5.3), Inches(1.8), Inches(1.45), "6.935,7", "LSTM MAE (kbps)", "R² = 0.1015", COLOR_BLUE)
    add_kpi_card(slide13, Inches(4.45), Inches(5.3), Inches(1.8), Inches(1.45), "129,9 s", "Χρόνος Εκπαίδευσης", "Inference: 100,9 μs/δείγμα", COLOR_NAVY)

    if (FIGURES_DIR / "08_lstm_training_loss.png").exists():
        slide13.shapes.add_picture(str(FIGURES_DIR / "08_lstm_training_loss.png"), Inches(6.45), Inches(1.45), width=Inches(6.28))

    set_speaker_notes(slide13, """
Στο 5ο Ζητούμενο σχεδιάσαμε και εκπαιδεύσαμε ένα βαθύ επαναληπτικό νευρωνικό δίκτυο Long Short-Term Memory (LSTM) σε PyTorch, χρησιμοποιώντας παράθυρο ιστορικού L = 64 δευτερολέπτων.
Το δίκτυο αποτελείται από 2 επίπεδα LSTM με 64 κρυφές μονάδες, Dropout 0.2 και κεφαλή παλινδρόμησης 2 επιπέδων.
Στο δεξί διάγραμμα φαίνεται η ομαλή σύγκλιση της συνάρτησης απώλειας (Training & Validation Loss) στις 12 εποχές εκπαίδευσης.
Στο Test Set το LSTM πέτυχε RMSE = 14.473,4 kbps και MAE = 6.935,7 kbps, καθώς τα νευρωνικά δίκτυα ακολουθιών τείνουν να εξομαλύνουν (over-smooth) τις απότομες αιχμές (bursts) του ασύρματου καναλιού.
""")

    # =========================================================================
    # SLIDE 14: Requirement 6 (Bonus) - Foundation Model (IBM Granite TTM)
    # =========================================================================
    slide14 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 6 (15% Bonus): Foundation Models — IBM Granite Tiny Time Mixer (TTM)",
        category="REQUIREMENT 6 (BONUS) — TIME-SERIES FOUNDATION MODELS",
        slide_num=14,
        total_slides=total_slides
    )

    add_info_card(
        slide14, Inches(0.6), Inches(1.4), Inches(5.55), Inches(3.75),
        "Αρχιτεκτονική IBM Granite TTM & Transfer Learning",
        [
            "• Αρχιτεκτονική Patch-Level MLP-Mixer (src/models_foundation.py):",
            "   – Αντί για βαριά Self-Attention O(L²), το TTM τεμαχίζει το παράθυρο L=64s σε N=8 μη-επικαλυπτόμενα χρονικά Patches μήκους P=8s.",
            "   – Εφαρμόζει εναλλάξ Inter-Patch Time-Mixing και Intra-Patch Channel-Mixing με Residual Skip Connections και LayerNorm.",
            "• 1) Αξιολόγηση Zero-Shot (Χωρίς Εκπαίδευση στο Dataset μας):",
            "   – Απευθείας πρόβλεψη με τα προ-εκπαιδευμένα βάρη: RMSE = 18.641,96 kbps, MAE = 10.695,33 kbps.",
            "• 2) Αξιολόγηση Ταχύτατου Fine-Tuning (4 Εποχές — 24,7s):",
            "   – Με προσαρμογή μόλις 4 εποχών στα δεδομένα 5G, το RMSE κατακρημνίζεται στα 8.426,33 kbps (μείωση σφάλματος κατά -54,8%!).",
            "   – Επιτυγχάνει R² = 0.6954, ξεπερνώντας το εκπαιδευμένο από το μηδέν LSTM κατά 6.047 kbps!"
        ],
        accent_color=COLOR_NAVY,
        font_size=9.1
    )

    add_kpi_card(slide14, Inches(0.6), Inches(5.3), Inches(1.75), Inches(1.45), "18.642,0", "Zero-Shot RMSE", "Χωρίς κανένα training (0s)", COLOR_GRAY)
    add_kpi_card(slide14, Inches(2.48), Inches(5.3), Inches(1.75), Inches(1.45), "8.426,3", "Fine-Tuned RMSE", "Μείωση σφάλματος -54,8%!", COLOR_ACCENT)
    add_kpi_card(slide14, Inches(4.36), Inches(5.3), Inches(1.79), Inches(1.45), "R² = 0.695", "Fine-Tuned Fit", "Μόλις 24,7s Fine-Tuning", COLOR_GOLD)

    if (FIGURES_DIR / "10_foundation_model_performance.png").exists():
        slide14.shapes.add_picture(str(FIGURES_DIR / "10_foundation_model_performance.png"), Inches(6.3), Inches(1.45), width=Inches(6.43))

    set_speaker_notes(slide14, """
Στο 6ο Ζητούμενο (Bonus) αξιολογήσαμε το Time-Series Foundation Model IBM Granite Tiny Time Mixer (TTM), το οποίο βασίζεται σε αρχιτεκτονική Patch-based MLP-Mixer (8 patches των 8 δευτερολέπτων).
Σε Zero-Shot λειτουργία, χωρίς καμία απολύτως εκπαίδευση στα δικά μας δεδομένα, το μοντέλο πετυχαίνει RMSE = 18.642 kbps.
Όταν όμως εφαρμόζουμε ταχύτατο Fine-Tuning μόλις 4 εποχών (διάρκειας 24,7 δευτερολέπτων), το σφάλμα μειώνεται εντυπωσιακά κατά 54,8%, φτάνοντας τα 8.426,3 kbps και R² = 0.695!
Μάλιστα, το Fine-Tuned TTM ξεπερνά κατά 6.047 kbps το LSTM που εκπαιδεύτηκε από το μηδέν για 130 δευτερόλεπτα.
""")

    # =========================================================================
    # SLIDE 15: Comprehensive Model Comparison Table (All 4 Paradigms)
    # =========================================================================
    slide15 = create_blank_slide_with_header(
        prs,
        "Συγκριτική Αξιολόγηση Όλων των Μοντέλων (XGBoost vs LSTM vs TTM)",
        category="REQUIREMENTS 3, 5 & 6 — MULTI-MODEL BENCHMARKING",
        slide_num=15,
        total_slides=total_slides
    )

    comp_headers = [
        "Μοντέλο Πρόβλεψης", "Κατηγορία / Αρχιτεκτονική", "Lookback (L)",
        "RMSE (kbps)", "MAE (kbps)", "R² Score", "Χρόνος Train", "Inference / Δείγμα"
    ]
    comp_rows = [
        ["1. XGBoost Regressor", "Gradient Boosted Trees (100 δένδρα)", "10 s (80 dims)", "6.344,75", "3.275,46", "0.8247", "1,30 s", "0,6 μs (0,0006 ms)"],
        ["2. IBM Granite TTM (Fine-Tuned)", "Foundation Patch MLP-Mixer (4 εποχές)", "64 s (8 patches)", "8.426,33", "4.203,32", "0.6954", "24,67 s", "80,2 μs (0,0802 ms)"],
        ["3. PyTorch LSTM", "Deep Recurrent Net (2-Layer, 64 hidden)", "64 s (seq 64×8)", "14.473,36", "6.935,72", "0.1015", "129,87 s", "100,9 μs (0,1009 ms)"],
        ["4. IBM Granite TTM (Zero-Shot)", "Pretrained Foundation (0 εποχές)", "64 s (8 patches)", "18.641,96", "10.695,33", "-0.4906", "0,00 s", "79,3 μs (0,0793 ms)"]
    ]
    add_styled_table(
        slide15,
        Inches(0.6), Inches(1.38), Inches(12.133), Inches(2.55),
        comp_headers, comp_rows,
        col_widths=[Inches(2.15), Inches(2.55), Inches(1.25), Inches(1.25), Inches(1.25), Inches(1.05), Inches(1.2), Inches(1.433)],
        highlight_rows=[0, 1],
        font_size=9.0
    )

    if (FIGURES_DIR / "09_model_comparisons.png").exists():
        slide15.shapes.add_picture(str(FIGURES_DIR / "09_model_comparisons.png"), Inches(0.6), Inches(4.08), width=Inches(7.35))

    add_info_card(
        slide15, Inches(8.1), Inches(4.08), Inches(4.633), Inches(2.75),
        "Γιατί Υπερέχει το XGBoost στα Ραδιοδεδομένα;",
        [
            "• Ασυνεχείς Κατανομές & Αιχμές (Bursts): Τα δενδροειδή σύνολα (Decision Tree Ensembles) διαχωρίζουν τον χώρο χαρακτηριστικών με ακριβή κατώφλια (hard splits), συλλαμβάνοντας ακαριαία τις μεταβάσεις CQI/MCS.",
            "• Tabular Inductive Bias: Σύμφωνα με τους Grinsztajn et al. (NeurIPS 2022), τα GBDTs υπερέχουν των νευρωνικών δικτύων σε tabular μετρήσεις με έντονες ασυμμετρίες.",
            "• 100x Ταχύτερο Inference: Μόλις 0,6 μs/δείγμα — ιδανικό για εκτέλεση σε O-RAN Near-RT RIC xApp (< 10 ms loop)."
        ],
        accent_color=COLOR_NAVY,
        font_size=8.8
    )

    set_speaker_notes(slide15, """
Στη 15η διαφάνεια αντιπαραβάλλουμε συγκεντρωτικά και τα 4 μοντέλα που αναπτύξαμε.
Πρώτο κατατάσσεται το XGBoost Regressor με RMSE 6.344,75 kbps, R² = 0.825 και χρόνο συμπερασμού μόλις 0,6 μικροδευτερόλεπτα.
Δεύτερο έρχεται το Fine-Tuned Foundation Model (IBM Granite TTM) με RMSE 8.426,33 kbps και R² = 0.695.
Τρίτο ακολουθεί το PyTorch LSTM με RMSE 14.473,36 kbps και τέταρτο το Zero-Shot TTM.
Η υπεροχή του XGBoost εξηγείται επιστημονικά από την ικανότητα των δένδρων απόφασης να μοντελοποιούν ασυνεχή κατώφλια (όπως τα διακριτά βήματα MCS/CQI) χωρίς να εξομαλύνουν υπερβολικά τις απότομες μεταβολές.
""")

    # =========================================================================
    # SLIDE 16: Requirement 7 - SHAP-Guided Feature Pruning & Edge Latency
    # =========================================================================
    slide16 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 7 (10%): Σταδιακή Αφαίρεση Μεταβλητών (Feature Pruning) & Edge Latency",
        category="REQUIREMENT 7 — SHAP-GUIDED FEATURE PRUNING",
        slide_num=16,
        total_slides=total_slides
    )

    prune_headers = [
        "Στάδιο Κλαδέματος", "Διατηρούμενα KPIs (βάσει SHAP)", "Διάσταση (L=10)",
        "RMSE (kbps)", "MAE (kbps)", "R² Score", "Χρόνος Train", "Μείωση PUCCH Telemetry"
    ]
    prune_rows = [
        ["100% Features (8 KPIs)", "UL, RSSI, Dist, Speed, SNR, RSRQ, CQI, RSRP", "80 features", "6.447,05", "3.330,95", "0.8190", "0,57 s", "0% (Baseline)"],
        ["75% Features (6 KPIs)", "UL, RSSI, Dist, Speed, SNR, RSRQ (-RSRP, -CQI)", "60 features", "6.425,95", "3.311,15", "0.8201", "0,56 s", "-25% (Βέλτιστο RMSE!)"],
        ["50% Features (4 KPIs)", "UL, RSSI, ServingCell_Distance, Speed", "40 features", "6.605,38", "3.349,36", "0.8100", "0,51 s", "-50% Signaling Overhead"],
        ["25% Features (2 KPIs)", "Μόνο UL_bitrate & RSSI", "20 features", "6.494,28", "3.313,23", "0.8163", "0,41 s (-28,1%)", "-75% Signaling Overhead"]
    ]
    add_styled_table(
        slide16,
        Inches(0.6), Inches(1.38), Inches(12.133), Inches(2.35),
        prune_headers, prune_rows,
        col_widths=[Inches(1.85), Inches(3.25), Inches(1.2), Inches(1.15), Inches(1.15), Inches(0.95), Inches(1.18), Inches(1.403)],
        highlight_rows=[1, 3],
        font_size=8.8
    )

    if (FIGURES_DIR / "11_feature_pruning_accuracy_vs_latency.png").exists():
        slide16.shapes.add_picture(str(FIGURES_DIR / "11_feature_pruning_accuracy_vs_latency.png"), Inches(0.6), Inches(3.9), width=Inches(7.65))

    add_info_card(
        slide16, Inches(8.4), Inches(3.9), Inches(4.333), Inches(2.9),
        "Τηλεπικοινωνιακό Όφελος στο Edge / MEC",
        [
            "• Εξάλειψη Πλεονάζουσας Πληροφορίας (75% KPIs):",
            "  Αφαιρώντας τα RSRP και CQI, το RMSE βελτιώνεται ελαφρώς (6.425,95 kbps) λόγω μείωσης της πολυσυγγραμμικότητας!",
            "• Ultra-Lean Telemetry (25% KPIs):",
            "  Κρατώντας ΜΟΝΟ τα 2 κορυφαία χαρακτηριστικά (UL_bitrate & RSSI), το σφάλμα μεταβάλλεται μόλις κατά +0,73% (+47 kbps), ενώ ο χρόνος εκπαίδευσης μειώνεται κατά 28,1%.",
            "• Εξοικονόμηση Uplink Control (PUCCH):",
            "  Το UE δεν χρειάζεται να αποστέλλει συνεχείς αναφορές CSI/GPS, μειώνοντας κατά 75% το κόστος σηματοδοσίας."
        ],
        accent_color=COLOR_ACCENT,
        font_size=8.8
    )

    set_speaker_notes(slide16, """
Στο 7ο Ζητούμενο αξιοποιήσαμε την ιεράρχηση του TreeSHAP για να αφαιρέσουμε σταδιακά τις λιγότερο σημαντικές μεταβλητές: από 8 KPIs (100%) σε 6 KPIs (75%), 4 KPIs (50%) και τέλος μόνο 2 KPIs (25%).
Τα αποτελέσματα είναι εντυπωσιακά:
Στο 75% των χαρακτηριστικών (αφαιρώντας RSRP και CQI), το RMSE μειώνεται στα 6.425,95 kbps επειδή εξαλείφεται η συγγραμμικότητα μεταξύ των δεικτών ισχύος.
Ακόμη πιο εντυπωσιακά, στο 25% των χαρακτηριστικών (κρατώντας αποκλειστικά το UL_bitrate και το RSSI), διατηρούμε R² = 0.8163 με μόλις +0,7% διαφορά στο RMSE, μειώνοντας τον χρόνο εκπαίδευσης κατά 28,1% και το τηλεμετρικό φορτίο στο PUCCH κατά 75%!
""")

    # =========================================================================
    # SLIDE 17: Requirement 8 (Part A) - 5G Proactive Early Warning Table
    # =========================================================================
    slide17 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 8 (10%): 5G Proactive Network Management — Έγκαιρη Ανίχνευση Πτώσης QoS",
        category="REQUIREMENT 8 — PROACTIVE SLA & QOS DEGRADATION WARNING",
        slide_num=17,
        total_slides=total_slides
    )

    pro_headers = [
        "Ορίζοντας Προειδοποίησης (Δt)", "RMSE (kbps)", "R² Score",
        "Precision", "Recall (Ρυθμός Ανίχνευσης)", "False Alarm Rate", "F1-Score", "Εφικτές Προληπτικές Ενέργειες Δικτύου 5G"
    ]
    pro_rows = [
        ["Δt = 1 δευτερόλεπτο", "6.344,75", "0.8247", "94,23%", "91,65%", "6,43%", "0.9292", "Predictive Beam Switching, Fast Intra/Inter-gNB Handover"],
        ["Δt = 3 δευτερόλεπτα", "7.503,15", "0.7548", "92,82%", "88,32%", "7,84%", "0.9051", "+ Dynamic PRB Slice Reservation, MEC ABR Bitrate Adaptation"],
        ["Δt = 5 δευτερόλεπτα (Χρυσή Τομή)", "7.961,68", "0.7241", "92,55%", "85,74%", "7,93%", "0.8901", "+ Target gNB Context Pre-Fetch, Dual Connectivity (EN-DC/NR-DC)"],
        ["Δt = 10 δευτερόλεπτα", "9.112,46", "0.6391", "92,20%", "81,29%", "7,92%", "0.8640", "+ Carrier Aggregation Reconfig, Edge Buffer Pre-filling"],
        ["Δt = 15 δευτερόλεπτα", "9.599,50", "0.6003", "92,30%", "78,17%", "7,52%", "0.8465", "+ Core Network UPF Path Switching, Multi-RAT Offloading"]
    ]
    add_styled_table(
        slide17,
        Inches(0.6), Inches(1.38), Inches(12.133), Inches(2.5),
        pro_headers, pro_rows,
        col_widths=[Inches(1.85), Inches(1.1), Inches(0.85), Inches(0.95), Inches(1.55), Inches(1.15), Inches(0.9), Inches(3.783)],
        highlight_rows=[0, 2],
        font_size=8.6
    )

    if (FIGURES_DIR / "12_proactive_5g_early_warning_tradeoff.png").exists():
        slide17.shapes.add_picture(str(FIGURES_DIR / "12_proactive_5g_early_warning_tradeoff.png"), Inches(0.6), Inches(4.02), width=Inches(7.35))

    add_info_card(
        slide17, Inches(8.1), Inches(4.02), Inches(4.633), Inches(2.85),
        "Ανάλυση Trade-Off: Ακρίβεια vs Χρόνος Αντίδρασης",
        [
            "• Κατώφλι SLA (τ = 5.000 kbps / 5 Mbps): Κάτω από αυτό το όριο καταρρέει το 4K video streaming και παραβιάζεται το eMBB SLA.",
            "• Βραχύς Ορίζοντας (Δt = 1s): Κορυφαία αξιοπιστία (Recall 91,65%, False Alarms μόλις 6,43%, F1 = 0.929). Ιδανικός για γρήγορες αποφάσεις επιπέδου MAC/PHY.",
            "• Μέσος Ορίζοντας (Δt = 3–5s): Διατηρεί Recall 85,7%–88,3% (F1 ≈ 0.90), δίνοντας αρκετό χρόνο για προετοιμασία Handover και προσαρμογή MEC ABR.",
            "• Μακρύς Ορίζοντας (Δt = 10–15s): Το Recall υποχωρεί στο 78,2%, αλλά επιτρέπει στρατηγικές ενέργειες επιπέδου Core Network."
        ],
        accent_color=COLOR_NAVY,
        font_size=8.6
    )

    set_speaker_notes(slide17, """
Στο 8ο Ζητούμενο μελετήσαμε την προληπτική διαχείριση δικτύου 5G (Proactive Network Management) ορίζοντας ως συμβάν υποβάθμισης QoS την πτώση του Downlink Bitrate κάτω από το κατώφλι SLA των 5 Mbps (5.000 kbps).
Στον πίνακα βλέπουμε το θεμελιώδες Trade-Off μεταξύ της ακρίβειας πρόβλεψης και του διαθέσιμου χρόνου αντίδρασης (Lead Time Δt από 1 έως 15 δευτερόλεπτα):
Για Δt = 1s εντοπίζουμε το 91,65% των πτώσεων με μόλις 6,43% ψευδείς συναγερμούς (F1 = 0.929).
Στη «χρυσή τομή» των Δt = 5 δευτερολέπτων, διατηρούμε Recall 85,74% και F1 = 0.890, παρέχοντας 5 ολόκληρα δευτερόλεπτα στον ελεγκτή δικτύου για να εκτελέσει προληπτικό handover, δέσμευση PRBs ή υποβιβασμό ρυθμού ABR video χωρίς καμία διακοπή στην εμπειρία του χρήστη.
""")

    # =========================================================================
    # SLIDE 18: Requirement 8 (Part B) - 3GPP NWDAF & O-RAN RIC Architecture
    # =========================================================================
    slide18 = create_blank_slide_with_header(
        prs,
        "Ζητούμενο 8 (10%): Αρχιτεκτονική Ενορχήστρωσης σε 3GPP NWDAF & O-RAN RIC",
        category="REQUIREMENT 8 — 3GPP RELEASE 18 & O-RAN INTEGRATION",
        slide_num=18,
        total_slides=total_slides
    )

    add_info_card(
        slide18, Inches(0.6), Inches(1.4), Inches(3.9), Inches(5.35),
        "1. O-RAN Non-RT RIC (SMO Layer > 1s)",
        [
            "• Φιλοξενεί τα μοντέλα ως rApps στο Service Management & Orchestration (SMO).",
            "• Συλλέγει ιστορικά traces μέσω της διεπαφής O1.",
            "• Εκτελεί περιοδική επανεκπαίδευση (Retraining) του XGBoost και Fine-Tuning του IBM Granite TTM.",
            "• Εκτελεί την ανάλυση TreeSHAP & Feature Pruning, ενημερώνοντας την πολιτική συλλογής τηλεμετρίας μέσω της διεπαφής A1."
        ],
        accent_color=COLOR_NAVY,
        font_size=9.5
    )

    add_info_card(
        slide18, Inches(4.716), Inches(1.4), Inches(3.9), Inches(5.35),
        "2. O-RAN Near-RT RIC (xApp 10ms – 1s)",
        [
            "• Φιλοξενεί το εκπαιδευμένο μοντέλο XGBoost (L=10) ως ελαφρύ xApp.",
            "• Λαμβάνει real-time KPIs (UL_bitrate, RSSI, SNR, CQI) από τους κόμβους O-DU / O-CU μέσω της διεπαφής E2.",
            "• Χρόνος συμπερασμού: 0,6 μs/UE (επιτρέπει έλεγχο >10.000 UEs εντός του παραθύρου των 10 ms!).",
            "• Αποστέλλει μηνύματα E2 RIC Control για Dynamic PRB Slicing και Προληπτικό Handover."
        ],
        accent_color=COLOR_ACCENT,
        font_size=9.5
    )

    add_info_card(
        slide18, Inches(8.833), Inches(1.4), Inches(3.9), Inches(5.35),
        "3. 3GPP NWDAF (5G Core Release 18)",
        [
            "• Ενσωμάτωση στη λειτουργία Network Data Analytics Function (3GPP TS 23.288).",
            "• Εξάγει προβλέψεις QoS Sustainability Analytics μέσω της υπηρεσίας Nnwdaf_AnalyticsInfo.",
            "• Ενημερώνει το PCF (Policy Control Function) για προσαρμογή QoS Flows και το AMF για Mobility Management.",
            "• Ενεργοποιεί τον MEC Application Function (AF) για προληπτική προσαρμογή ABR Video Streaming."
        ],
        accent_color=COLOR_BLUE,
        font_size=9.5
    )

    set_speaker_notes(slide18, """
Στη 18η διαφάνεια παρουσιάζουμε πώς το σύστημά μας εντάσσεται απευθείας στα σύγχρονα πρότυπα 3GPP Release 18 και O-RAN:
Στο επίπεδο Non-RT RIC (SMO), ένα rApp εκτελεί την εκπαίδευση των μοντέλων και το SHAP Feature Pruning.
Στο επίπεδο Near-RT RIC, το μοντέλο XGBoost τρέχει ως xApp μέσω της διεπαφής E2. Επειδή χρειάζεται μόλις 0,6 μικροδευτερόλεπτα ανά δείγμα, μπορεί να εξυπηρετεί χιλιάδες ενεργά τερματικά σε πραγματικό χρόνο (< 10 ms).
Παράλληλα, στο 5G Core, το NWDAF δημοσιεύει QoS Sustainability Analytics προς τα PCF, AMF και τον MEC video server.
""")

    # =========================================================================
    # SLIDE 19: Key Scientific Conclusions & Reproducibility CLI Guide
    # =========================================================================
    slide19 = create_blank_slide_with_header(
        prs,
        "Συνοπτικά Συμπεράσματα & Οδηγός Εκτέλεσης Κώδικα (Live Demo)",
        category="CONCLUSIONS & REPRODUCIBILITY",
        slide_num=19,
        total_slides=total_slides
    )

    add_info_card(
        slide19, Inches(0.6), Inches(1.4), Inches(6.2), Inches(5.35),
        "Κύρια Επιστημονικά & Τεχνικά Συμπεράσματα",
        [
            "1. Ακρίβεια & Ταχύτητα XGBoost (Ζητ. 3 & 5):",
            "   • Το XGBoost (L=10, H=1) πέτυχε R² = 0.825 (RMSE 6,34 Mbps) και 0,6 μs latency, υπερέχοντας κατά 56,2% σε ακρίβεια και 100x σε ταχύτητα έναντι του LSTM.",
            "2. Επεξηγησιμότητα Καναλιού με TreeSHAP (Ζητ. 4):",
            "   • Τα UL_bitrate (65,8% επιρροή) και RSSI (7,8%) αποτελούν τους ισχυρότερους δείκτες πρόβλεψης, ακολουθούμενα από τα ServingCell_Distance, Speed και SNR.",
            "3. Ισχύς των Foundation Models (Ζητ. 6 Bonus):",
            "   • Το IBM Granite TTM με μόλις 4 εποχές Fine-Tuning (24,7s) μείωσε το Zero-Shot σφάλμα κατά 54,8% (RMSE 8,43 Mbps), ξεπερνώντας καθαρά το LSTM.",
            "4. Αποδοτικότητα Edge μέσω Feature Pruning (Ζητ. 7):",
            "   • Η αφαίρεση του 75% των KPIs (κρατώντας μόνο UL_bitrate & RSSI) διατηρεί την ακρίβεια σχεδόν αναλλοίωτη (+0,7% RMSE), μειώνοντας κατά 75% το κόστος τηλεμετρίας.",
            "5. Προληπτική Διαχείριση 5G QoS (Ζητ. 8):",
            "   • Επιτυγχάνεται Recall 91,65% (Δt=1s) και 85,74% (Δt=5s) για κατώφλι SLA 5 Mbps."
        ],
        accent_color=COLOR_NAVY,
        font_size=9.2
    )

    add_info_card(
        slide19, Inches(7.0), Inches(1.4), Inches(5.733), Inches(5.35),
        "Εντολές Εκτέλεσης & Αναπαραγωγιμότητας (Ready-to-Run CLI)",
        [
            "• Πλήρης Εκτέλεση Ολόκληρου του Pipeline (100%):",
            "  python scripts/run_pipeline.py --all",
            "• Εκτέλεση Ενδιάμεσης Φάσης (40%–50%):",
            "  python scripts/run_midterm_40pct.py",
            "• Τμηματική Εκτέλεση ανά Ζητούμενο:",
            "  python scripts/run_pipeline.py --preprocess   (Ζητ. 2)",
            "  python scripts/run_pipeline.py --ml           (Ζητ. 3: XGBoost Grid)",
            "  python scripts/run_pipeline.py --shap         (Ζητ. 4: TreeSHAP XAI)",
            "  python scripts/run_pipeline.py --dl           (Ζητ. 5: PyTorch LSTM)",
            "  python scripts/run_pipeline.py --foundation   (Ζητ. 6: IBM Granite TTM)",
            "  python scripts/run_pipeline.py --prune        (Ζητ. 7: Feature Pruning)",
            "  python scripts/run_pipeline.py --proactive    (Ζητ. 8: 5G Proactive QoS)",
            "• Αυτόματη Αναδημιουργία Αναφορών & Παρουσίασης:",
            "  python scripts/generate_report.py",
            "  python scripts/generate_presentation.py",
            "• Αυτοματοποιημένος Έλεγχος Ακεραιότητας:",
            "  python scripts/verify_all.py"
        ],
        accent_color=COLOR_ACCENT,
        font_size=9.0
    )

    set_speaker_notes(slide19, """
Στη 19η διαφάνεια συνοψίζουμε τα 5 κεντρικά ευρήματα της εργασίας μας και παραθέτουμε τις εντολές CLI με τις οποίες μπορεί να εκτελεστεί είτε ολόκληρο το pipeline είτε κάθε ζητούμενο ξεχωριστά.
Όλα τα αποτελέσματα, τα εκπαιδευμένα μοντέλα, οι πίνακες JSON, τα 12 διαγράμματα υψηλής ανάλυσης, οι τεχνικές αναφορές (Markdown, Word, PDF) και οι παρουσιάσεις παράγονται αυτόματα και επαληθεύονται με το script verify_all.py.
""")

    # =========================================================================
    # SLIDE 20: Closing / Q&A Slide (Dark Navy Elegance + Prominent Authors)
    # =========================================================================
    slide20 = prs.slides.add_slide(slide_layout)
    bg20 = slide20.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg20.fill.solid()
    bg20.fill.fore_color.rgb = COLOR_DARK_NAVY
    bg20.line.fill.background()

    left_stripe20 = slide20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.28), Inches(7.5))
    left_stripe20.fill.solid()
    left_stripe20.fill.fore_color.rgb = COLOR_ACCENT
    left_stripe20.line.fill.background()

    tbox20 = slide20.shapes.add_textbox(Inches(1.0), Inches(0.9), Inches(11.333), Inches(2.5))
    tf20 = tbox20.text_frame
    tf20.word_wrap = True

    p_end = tf20.paragraphs[0]
    p_end.alignment = PP_ALIGN.CENTER
    p_end.text = "Σας Ευχαριστούμε Πολύ για την Προσοχή σας!"
    p_end.font.size = Pt(34)
    p_end.font.bold = True
    p_end.font.color.rgb = COLOR_WHITE

    p_qa = tf20.add_paragraph()
    p_qa.alignment = PP_ALIGN.CENTER
    p_qa.text = "\nΕρωτήσεις & Συζήτηση (Q&A)"
    p_qa.font.size = Pt(22)
    p_qa.font.bold = True
    p_qa.font.color.rgb = COLOR_ACCENT

    # Prominent Author Block on Closing Slide
    close_card = slide20.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(3.2), Inches(10.333), Inches(2.45))
    close_card.fill.solid()
    close_card.fill.fore_color.rgb = RGBColor(0x11, 0x22, 0x40)
    close_card.line.color.rgb = COLOR_ACCENT
    close_card.line.width = Pt(1.5)

    ctf = close_card.text_frame
    ctf.word_wrap = True
    ctf.margin_top = Inches(0.22)

    pc1 = ctf.paragraphs[0]
    pc1.alignment = PP_ALIGN.CENTER
    pc1.text = "ΟΜΑΔΑ ΕΡΓΟΥ — ΠΑΝΕΠΙΣΤΗΜΙΟ ΠΑΤΡΩΝ (ΤΜΗΜΑ ΜΗΧΑΝΙΚΩΝ Η/Υ & ΠΛΗΡΟΦΟΡΙΚΗΣ)"
    pc1.font.size = Pt(12)
    pc1.font.bold = True
    pc1.font.color.rgb = COLOR_GOLD

    pc2 = ctf.add_paragraph()
    pc2.alignment = PP_ALIGN.CENTER
    pc2.text = f"\n{AUTHOR_1}\n{AUTHOR_2}\n"
    pc2.font.size = Pt(20)
    pc2.font.bold = True
    pc2.font.color.rgb = COLOR_WHITE

    pc3 = ctf.add_paragraph()
    pc3.alignment = PP_ALIGN.CENTER
    pc3.text = "Επιβλέπων: Παναγιώτης Μαράντης (pmaradis@isi.gr)  |  Θέμα 11: Πρόβλεψη Downlink Bitrate σε Δίκτυα 5G\nGitHub Repository: https://github.com/ghidrasondenuvos/5g-downlink-bitrate-forecasting"
    pc3.font.size = Pt(11.5)
    pc3.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    # Footer on Slide 20
    fbox20 = slide20.shapes.add_textbox(Inches(1.0), Inches(6.8), Inches(11.333), Inches(0.4))
    ftf20 = fbox20.text_frame
    fp20 = ftf20.paragraphs[0]
    fp20.alignment = PP_ALIGN.CENTER
    fp20.text = f"Πανεπιστήμιο Πατρών / ISI  |  {AUTHORS_LINE}  |  Διαφάνεια 20 / {total_slides}"
    fp20.font.size = Pt(10)
    fp20.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)

    set_speaker_notes(slide20, """
Σας ευχαριστούμε πολύ για την προσοχή σας!
Ο Δημήτριος Τσανακτσής (Α.Μ. 1100736) και ο Ιάσωνας Δερβενής (Α.Μ. 1097437) είμαστε στη διάθεσή σας για οποιαδήποτε ερώτηση σχετικά με τη μεθοδολογία, τα πειραματικά αποτελέσματα ή την αρχιτεκτονική του κώδικα.
""")

    # Save presentation to primary and backup paths
    PRESENTATION_DIR.mkdir(parents=True, exist_ok=True)
    out_pptx = PRESENTATION_DIR / "Downlink_Bitrate_Forecasting_5G.pptx"
    alt_pptx = PRESENTATION_DIR / "Teliki_Parousiasi_5G_100_Percent.pptx"

    try:
        prs.save(str(out_pptx))
        print(f"Presentation saved successfully to {out_pptx} ({len(prs.slides)} slides)")
    except PermissionError:
        print(f"[INFO] {out_pptx.name} is currently open in PowerPoint; saving to fallback {alt_pptx.name}.")

    try:
        prs.save(str(alt_pptx))
        print(f"Presentation also saved to {alt_pptx} ({len(prs.slides)} slides)")
    except PermissionError:
        pass

    return out_pptx


if __name__ == "__main__":
    generate_presentation_deck()
