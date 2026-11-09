"""
Midterm (40% - 50% Progress) Comprehensive 18-Slide Academic Presentation Generator.
Generates `presentation/Endiamesi_Parousiasi_5G_40_50_Percent.pptx` for the
Preparatory / Intermediate Presentation (Ενδιάμεση Παρουσίαση 40%–50% προόδου)
covering Requirements 1, 2, 3, and 4 in full technical depth, with Requirements 5-8
presented in the project roadmap and future work.

Team:
- ΔΗΜΗΤΡΙΟΣ ΤΣΑΝΑΚΤΣΗΣ (Α.Μ.: 1100736)
- ΙΑΣΩΝΑΣ ΔΕΡΒΕΝΗΣ (Α.Μ.: 1097437)
"""

import sys
import json
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import PRESENTATION_DIR, FIGURES_DIR, RESULTS_DIR, DATA_PROCESSED_DIR

# Academic Color Palette
COLOR_NAVY = RGBColor(0x00, 0x33, 0x66)        # #003366 Primary Navy
COLOR_BLUE = RGBColor(0x1F, 0x49, 0x7D)        # #1F497D Royal Blue
COLOR_LIGHT_BLUE = RGBColor(0x34, 0x98, 0xDB)  # #3498DB Sky Accent
COLOR_TEAL = RGBColor(0x27, 0xAE, 0x60)        # #27AE60 Teal / Green
COLOR_DARK_GREEN = RGBColor(0x1E, 0x84, 0x49)  # #1E8449 Deep Green
COLOR_ORANGE = RGBColor(0xE6, 0x7E, 0x22)      # #E67E22 Orange Accent
COLOR_RED = RGBColor(0xC0, 0x39, 0x2B)         # #C0392B Alert Red
COLOR_PURPLE = RGBColor(0x6C, 0x34, 0x83)      # #6C3483 Academic Purple
COLOR_CARD_BG = RGBColor(0xF4, 0xF6, 0xF9)     # #F4F6F9 Light Card Background
COLOR_ALT_ROW = RGBColor(0xEB, 0xF2, 0xFA)     # #EBF2FA Table Alternating Row
COLOR_BORDER = RGBColor(0xCB, 0xD5, 0xE1)      # #CBD5E1 Subtle Border
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_DARK_TEXT = RGBColor(0x1E, 0x29, 0x3B)
COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)
COLOR_GOLD = RGBColor(0xF1, 0xC4, 0x0F)

STUDENT_1 = "ΔΗΜΗΤΡΙΟΣ ΤΣΑΝΑΚΤΣΗΣ (Α.Μ.: 1100736)"
STUDENT_2 = "ΙΑΣΩΝΑΣ ΔΕΡΒΕΝΗΣ (Α.Μ.: 1097437)"
STUDENTS_INLINE = f"{STUDENT_1}  |  {STUDENT_2}"
TOTAL_SLIDES = 18


def set_slide_notes(slide, notes_text: str):
    """Adds detailed Greek speaker notes to the slide."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text.strip()


def create_content_slide(prs, slide_num: int, title_text: str, category_text: str):
    """Creates a standardized academic slide with header banner, slide number, and student footer."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Top subtle background strip
    top_strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.18))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = RGBColor(0xF8, 0xFA, 0xFC)
    top_strip.line.fill.background()

    # Left vertical accent bar in header
    accent_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.22), Inches(0.10), Inches(0.80))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = COLOR_NAVY
    accent_bar.line.fill.background()

    # Category & Title Textbox
    header_box = slide.shapes.add_textbox(Inches(0.72), Inches(0.18), Inches(10.8), Inches(0.90))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = COLOR_BLUE

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY

    # Slide Number Badge on top right
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(11.75), Inches(0.30), Inches(1.08), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = COLOR_NAVY
    badge.line.fill.background()
    tf_b = badge.text_frame
    tf_b.word_wrap = False
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = f"{slide_num} / {TOTAL_SLIDES}"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = COLOR_WHITE

    # Header bottom divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.16), Inches(12.333), Inches(0.03))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_BLUE
    line.line.fill.background()

    # Footer Bar
    footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(7.05), Inches(12.333), Inches(0.015))
    footer_line.fill.solid()
    footer_line.fill.fore_color.rgb = COLOR_BORDER
    footer_line.line.fill.background()

    footer_box = slide.shapes.add_textbox(Inches(0.5), Inches(7.10), Inches(12.333), Inches(0.32))
    tf_f = footer_box.text_frame
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = (
        f"Πανεπιστήμιο Πατρών — ΤΜΗΥΠ | Θέμα 11: Πρόβλεψη Downlink Bitrate σε 5G (Ενδιάμεση Παρουσίαση 40%–50%)   •   "
        f"{STUDENT_1}  &  {STUDENT_2}"
    )
    p_f.font.size = Pt(8.5)
    p_f.font.bold = True
    p_f.font.color.rgb = COLOR_MUTED

    return slide


def add_card(
    slide,
    left: float,
    top: float,
    width: float,
    height: float,
    title: str = None,
    bullets: list = None,
    bg_color: RGBColor = COLOR_CARD_BG,
    border_color: RGBColor = COLOR_BLUE,
    header_bg: RGBColor = None,
    title_color: RGBColor = COLOR_NAVY,
    font_size: float = 11.0,
    title_size: float = 13.0
):
    """Adds a styled rectangular or header-topped card with structured bullet points."""
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    card.adjustments[0] = 0.02
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)

    content_top = top + 0.08
    content_height = height - 0.16

    if header_bg is not None and title:
        hbar_h = 0.38
        hbar = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(hbar_h)
        )
        hbar.adjustments[0] = 0.02
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = header_bg
        hbar.line.color.rgb = header_bg
        tf_h = hbar.text_frame
        tf_h.word_wrap = True
        p_h = tf_h.paragraphs[0]
        p_h.text = title
        p_h.font.size = Pt(title_size)
        p_h.font.bold = True
        p_h.font.color.rgb = COLOR_WHITE
        p_h.alignment = PP_ALIGN.LEFT
        tf_h.margin_left = Inches(0.14)
        content_top = top + hbar_h + 0.06
        content_height = height - hbar_h - 0.12

    tb = slide.shapes.add_textbox(
        Inches(left + 0.12), Inches(content_top), Inches(width - 0.24), Inches(content_height)
    )
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    first_para = True
    if header_bg is None and title:
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(title_size)
        p_t.font.bold = True
        p_t.font.color.rgb = title_color
        p_t.space_after = Pt(5)
        first_para = False

    if bullets:
        for item in bullets:
            p = tf.paragraphs[0] if first_para else tf.add_paragraph()
            first_para = False
            if isinstance(item, tuple):
                lead, body = item
                r1 = p.add_run()
                r1.text = f"{lead} "
                r1.font.bold = True
                r1.font.size = Pt(font_size)
                r1.font.color.rgb = title_color

                r2 = p.add_run()
                r2.text = body
                r2.font.bold = False
                r2.font.size = Pt(font_size)
                r2.font.color.rgb = COLOR_DARK_TEXT
            else:
                p.text = str(item)
                p.font.size = Pt(font_size)
                p.font.color.rgb = COLOR_DARK_TEXT
            p.space_after = Pt(4)

    return tb


def add_kpi_card(
    slide,
    left: float,
    top: float,
    width: float,
    height: float,
    big_value: str,
    label: str,
    sublabel: str = "",
    accent_color: RGBColor = COLOR_NAVY,
    bg_color: RGBColor = COLOR_CARD_BG
):
    """Creates a visual KPI metric card with a top colored accent bar."""
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    card.adjustments[0] = 0.04
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = accent_color
    card.line.width = Pt(1.5)

    top_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(left + 0.02), Inches(top + 0.02), Inches(width - 0.04), Inches(0.08)
    )
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = accent_color
    top_bar.line.fill.background()

    tb = slide.shapes.add_textbox(
        Inches(left + 0.08), Inches(top + 0.12), Inches(width - 0.16), Inches(height - 0.16)
    )
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_val = tf.paragraphs[0]
    p_val.alignment = PP_ALIGN.CENTER
    p_val.text = big_value
    p_val.font.size = Pt(18)
    p_val.font.bold = True
    p_val.font.color.rgb = accent_color
    p_val.space_after = Pt(2)

    p_lbl = tf.add_paragraph()
    p_lbl.alignment = PP_ALIGN.CENTER
    p_lbl.text = label
    p_lbl.font.size = Pt(10)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_DARK_TEXT

    if sublabel:
        p_sub = tf.add_paragraph()
        p_sub.alignment = PP_ALIGN.CENTER
        p_sub.text = sublabel
        p_sub.font.size = Pt(8.5)
        p_sub.font.color.rgb = COLOR_MUTED


def add_styled_table(
    slide,
    left: float,
    top: float,
    width: float,
    height: float,
    headers: list[str],
    rows: list[list[str]],
    col_widths: list[float] = None,
    header_bg: RGBColor = COLOR_NAVY,
    font_size: float = 9.5,
    header_font_size: float = 10.0,
    highlight_rows: dict = None,
    bold_cols: set = None
):
    """Adds a cleanly formatted native PowerPoint table."""
    num_rows = len(rows) + 1
    num_cols = len(headers)
    table_shape = slide.shapes.add_table(
        num_rows, num_cols, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    table = table_shape.table

    if col_widths and len(col_widths) == num_cols:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = Inches(w)

    # Format Header
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_bg
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.06)
        tf.margin_right = Inches(0.06)
        tf.margin_top = Inches(0.03)
        tf.margin_bottom = Inches(0.03)
        p = tf.paragraphs[0]
        p.text = h_text
        p.font.size = Pt(header_font_size)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    # Format Body Rows
    highlight_rows = highlight_rows or {}
    bold_cols = bold_cols or {0}

    for r_idx, r_data in enumerate(rows):
        row_bg = highlight_rows.get(r_idx, COLOR_WHITE if r_idx % 2 == 0 else COLOR_ALT_ROW)
        for c_idx, val in enumerate(r_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.06)
            tf.margin_right = Inches(0.06)
            tf.margin_top = Inches(0.02)
            tf.margin_bottom = Inches(0.02)
            p = tf.paragraphs[0]
            p.text = str(val)
            p.font.size = Pt(font_size)
            p.font.bold = (c_idx in bold_cols) or (r_idx in highlight_rows)
            p.font.color.rgb = COLOR_NAVY if (r_idx in highlight_rows) else COLOR_DARK_TEXT
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    return table


def add_picture_fit(
    slide,
    img_path: Path,
    left: float,
    top: float,
    max_w: float,
    max_h: float,
    with_frame: bool = True,
    caption: str = None
):
    """Inserts an image centered within (left, top, max_w, max_h) preserving aspect ratio."""
    if not img_path.exists():
        add_card(
            slide, left, top, max_w, max_h,
            title="Διάγραμμα σε Προετοιμασία",
            bullets=[f"Αρχείο: {img_path.name}"],
            border_color=COLOR_ORANGE
        )
        return

    if with_frame:
        frame = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(max_w), Inches(max_h)
        )
        frame.adjustments[0] = 0.015
        frame.fill.solid()
        frame.fill.fore_color.rgb = COLOR_WHITE
        frame.line.color.rgb = COLOR_BORDER
        frame.line.width = Pt(1.2)

    pad = 0.08 if with_frame else 0.0
    cap_h = 0.26 if caption else 0.0
    avail_w = max_w - 2 * pad
    avail_h = max_h - 2 * pad - cap_h

    with Image.open(img_path) as im:
        w_px, h_px = im.size
    aspect = w_px / float(h_px)

    fit_w = avail_w
    fit_h = fit_w / aspect
    if fit_h > avail_h:
        fit_h = avail_h
        fit_w = fit_h * aspect

    img_left = left + pad + (avail_w - fit_w) / 2.0
    img_top = top + pad + (avail_h - fit_h) / 2.0

    slide.shapes.add_picture(str(img_path), Inches(img_left), Inches(img_top), width=Inches(fit_w), height=Inches(fit_h))

    if caption:
        cap_box = slide.shapes.add_textbox(
            Inches(left + 0.08), Inches(top + max_h - cap_h - 0.02), Inches(max_w - 0.16), Inches(cap_h)
        )
        tf_c = cap_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.alignment = PP_ALIGN.CENTER
        p_c.text = caption
        p_c.font.size = Pt(8.5)
        p_c.font.italic = True
        p_c.font.color.rgb = COLOR_MUTED


def generate_midterm_deck() -> Path:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Load experimental JSON artifacts if available
    grid_path = RESULTS_DIR / "xgboost_grid_results.json"
    grid_data = []
    if grid_path.exists():
        with open(grid_path, "r", encoding="utf-8") as f:
            grid_data = json.load(f)

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Navy Academic Elegance)
    # =========================================================================
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_NAVY
    bg1.line.fill.background()

    # Left decorative accent stripes
    stripe1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.28), Inches(7.5))
    stripe1.fill.solid()
    stripe1.fill.fore_color.rgb = COLOR_TEAL
    stripe1.line.fill.background()

    stripe2 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.28), Inches(0), Inches(0.10), Inches(7.5))
    stripe2.fill.solid()
    stripe2.fill.fore_color.rgb = COLOR_LIGHT_BLUE
    stripe2.line.fill.background()

    # University Header Banner Box
    uni_box = s1.shapes.add_textbox(Inches(0.9), Inches(0.55), Inches(11.6), Inches(1.1))
    tf_uni = uni_box.text_frame
    tf_uni.word_wrap = True
    p_u1 = tf_uni.paragraphs[0]
    p_u1.text = "ΠΑΝΕΠΙΣΤΗΜΙΟ ΠΑΤΡΩΝ — ΠΟΛΥΤΕΧΝΙΚΗ ΣΧΟΛΗ"
    p_u1.font.size = Pt(14)
    p_u1.font.bold = True
    p_u1.font.color.rgb = COLOR_LIGHT_BLUE

    p_u2 = tf_uni.add_paragraph()
    p_u2.text = "ΤΜΗΜΑ ΜΗΧΑΝΙΚΩΝ ΗΛΕΚΤΡΟΝΙΚΩΝ ΥΠΟΛΟΓΙΣΤΩΝ ΚΑΙ ΠΛΗΡΟΦΟΡΙΚΗΣ (ΤΜΗΥΠ)"
    p_u2.font.size = Pt(12)
    p_u2.font.bold = True
    p_u2.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    # Phase Pill Badge
    phase_badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.55), Inches(5.8), Inches(0.48))
    phase_badge.fill.solid()
    phase_badge.fill.fore_color.rgb = COLOR_TEAL
    phase_badge.line.fill.background()
    tf_pb = phase_badge.text_frame
    p_pb = tf_pb.paragraphs[0]
    p_pb.alignment = PP_ALIGN.CENTER
    p_pb.text = "ΕΝΔΙΑΜΕΣΗ ΠΑΡΟΥΣΙΑΣΗ ΠΡΟΟΔΟΥ (40% – 50%)"
    p_pb.font.size = Pt(13)
    p_pb.font.bold = True
    p_pb.font.color.rgb = COLOR_WHITE

    # Main Title & Subtitle
    title_box = s1.shapes.add_textbox(Inches(0.9), Inches(2.20), Inches(11.6), Inches(2.2))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t1 = tf_t.paragraphs[0]
    p_t1.text = "Θέμα 11: Πρόβλεψη Downlink Bitrate (Throughput)\nΜε Βάση Μετρικές Ποιότητας Καναλιού"
    p_t1.font.size = Pt(30)
    p_t1.font.bold = True
    p_t1.font.color.rgb = COLOR_WHITE
    p_t1.space_after = Pt(10)

    p_t2 = tf_t.add_paragraph()
    p_t2.text = (
        "Ανάλυση Τηλεπικοινωνιακού Προβλήματος 5G, Προεπεξεργασία Πραγματικών Traces Κινητικότητας,\n"
        "Πρόβλεψη Χρονοσειρών με XGBoost Regressor & Ερμηνευσιμότητα μέσω Explainable AI (TreeSHAP)"
    )
    p_t2.font.size = Pt(14)
    p_t2.font.color.rgb = RGBColor(0x93, 0xC5, 0xFD)

    # Student Team Prominent Card
    team_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(4.65), Inches(7.1), Inches(2.15))
    team_card.adjustments[0] = 0.03
    team_card.fill.solid()
    team_card.fill.fore_color.rgb = RGBColor(0x0A, 0x25, 0x47)
    team_card.line.color.rgb = COLOR_LIGHT_BLUE
    team_card.line.width = Pt(2.0)

    tf_tc = team_card.text_frame
    tf_tc.word_wrap = True
    tf_tc.margin_left = Inches(0.25)
    tf_tc.margin_top = Inches(0.18)

    p_tc0 = tf_tc.paragraphs[0]
    p_tc0.text = "ΟΜΑΔΑ ΕΡΓΟΥ — ΕΡΕΥΝΗΤΙΚΗ ΥΛΟΠΟΙΗΣΗ:"
    p_tc0.font.size = Pt(11.5)
    p_tc0.font.bold = True
    p_tc0.font.color.rgb = COLOR_GOLD
    p_tc0.space_after = Pt(8)

    p_tc1 = tf_tc.add_paragraph()
    p_tc1.text = f"👤  {STUDENT_1}"
    p_tc1.font.size = Pt(16.5)
    p_tc1.font.bold = True
    p_tc1.font.color.rgb = COLOR_WHITE
    p_tc1.space_after = Pt(6)

    p_tc2 = tf_tc.add_paragraph()
    p_tc2.text = f"👤  {STUDENT_2}"
    p_tc2.font.size = Pt(16.5)
    p_tc2.font.bold = True
    p_tc2.font.color.rgb = COLOR_WHITE

    # Course & Supervisor Card on Right
    course_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.25), Inches(4.65), Inches(4.35), Inches(2.15))
    course_card.adjustments[0] = 0.03
    course_card.fill.solid()
    course_card.fill.fore_color.rgb = RGBColor(0x0A, 0x25, 0x47)
    course_card.line.color.rgb = COLOR_TEAL
    course_card.line.width = Pt(1.8)

    tf_cc = course_card.text_frame
    tf_cc.word_wrap = True
    tf_cc.margin_left = Inches(0.20)
    tf_cc.margin_top = Inches(0.18)

    p_cc0 = tf_cc.paragraphs[0]
    p_cc0.text = "ΣΤΟΙΧΕΙΑ ΜΑΘΗΜΑΤΟΣ:"
    p_cc0.font.size = Pt(11)
    p_cc0.font.bold = True
    p_cc0.font.color.rgb = COLOR_TEAL
    p_cc0.space_after = Pt(6)

    p_cc1 = tf_cc.add_paragraph()
    p_cc1.text = "Αρχιτεκτονικές Δικτύων Επόμενης Γενιάς,\nΤεχνολογίες και Εφαρμογές"
    p_cc1.font.size = Pt(12)
    p_cc1.font.bold = True
    p_cc1.font.color.rgb = COLOR_WHITE
    p_cc1.space_after = Pt(6)

    p_cc2 = tf_cc.add_paragraph()
    p_cc2.text = "Επιβλέπων: Παναγιώτης Μαράντης (pmaradis@isi.gr)\nΑκαδημαϊκό Έτος: Χειμερινό Εξάμηνο 2026–2027"
    p_cc2.font.size = Pt(10.5)
    p_cc2.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)

    set_slide_notes(
        s1,
        "Καλησπέρα σας. Ονομάζομαι Δημήτριος Τσανακτσής (Α.Μ. 1100736) και μαζί με τον συνάδελφό μου Ιάσωνα Δερβένη (Α.Μ. 1097437) "
        "σας παρουσιάζουμε την Ενδιάμεση Παρουσίαση Προόδου (40%–50%) για το Θέμα 11: «Πρόβλεψη Downlink Bitrate (Throughput) με Βάση "
        "Μετρικές Ποιότητας Καναλιού», στο πλαίσιο του μαθήματος Αρχιτεκτονικές Δικτύων Επόμενης Γενιάς με επιβλέποντα τον κ. Παναγιώτη Μαράντη. "
        "Στη σημερινή παρουσίαση θα αναλύσουμε σε πλήρες τεχνικό βάθος τα πρώτα 4 ζητούμενα της εργασίας που αποτελούν το 50% του έργου, "
        "και θα κλείσουμε με τον οδικό χάρτη για την τελική φάση."
    )

    # =========================================================================
    # SLIDE 2: Δομή Εργασίας & Κατανομή Ποσοστών (0% -> 100%)
    # =========================================================================
    s2 = create_content_slide(
        prs, 2,
        "Δομή Εργασίας, Κατανομή Βαρύτητας & Ομάδα Έργου (0% → 100%)",
        "ΕΠΙΣΚΟΠΗΣΗ ΕΡΓΟΥ & ΠΡΟΟΔΟΣ ΕΝΔΙΑΜΕΣΗΣ ΦΑΣΗΣ (50%)"
    )

    headers_s2 = ["Ζητούμενο", "Περιγραφή Παραδοτέου (Θέμα 11)", "Ποσοστό", "Φάση", "Κατάσταση"]
    rows_s2 = [
        ["Ζητούμενο 1", "Ανάλυση τηλεπικοινωνιακού προβλήματος πρόβλεψης DL Bitrate σε 5G", "10%", "Φάση Α (Ενδιάμεση)", "✔ ΟΛΟΚΛΗΡΩΘΗΚΕ"],
        ["Ζητούμενο 2", "Προεπεξεργασία 135 traces, καθαρισμός '-', split & κανονικοποίηση", "15%", "Φάση Α (Ενδιάμεση)", "✔ ΟΛΟΚΛΗΡΩΘΗΚΕ"],
        ["Ζητούμενο 3", "Μοντέλο XGBoost Regressor σε πολλαπλά Lookback (L) & Horizons (H)", "15%", "Φάση Α (Ενδιάμεση)", "✔ ΟΛΟΚΛΗΡΩΘΗΚΕ"],
        ["Ζητούμενο 4", "Ερμηνευσιμότητα μοντέλου με Explainable AI (TreeSHAP)", "10%", "Φάση Α (Ενδιάμεση)", "✔ ΟΛΟΚΛΗΡΩΘΗΚΕ"],
        ["Ζητούμενο 5", "Υλοποίηση Deep Learning (PyTorch LSTM με παράθυρο L=64) vs XGBoost", "15%", "Φάση Β (Τελική)", "⏳ ΕΠΟΜΕΝΑ ΒΗΜΑΤΑ"],
        ["Ζητούμενο 6", "Bonus: Time-Series Foundation Model (IBM Granite Tiny Time Mixer)", "10%", "Φάση Β (Τελική)", "⏳ ΕΠΟΜΕΝΑ ΒΗΜΑΤΑ"],
        ["Ζητούμενο 7", "Σταδιακή αφαίρεση μεταβλητών βάσει SHAP (Accuracy vs Latency)", "10%", "Φάση Β (Τελική)", "⏳ ΕΠΟΜΕΝΑ ΒΗΜΑΤΑ"],
        ["Ζητούμενο 8", "5G Proactive Network Management (Έγκαιρη ανίχνευση πτώσης QoS)", "15%", "Φάση Β (Τελική)", "⏳ ΕΠΟΜΕΝΑ ΒΗΜΑΤΑ"],
    ]
    highlight_s2 = {
        0: RGBColor(0xE8, 0xF8, 0xF5),
        1: RGBColor(0xE8, 0xF8, 0xF5),
        2: RGBColor(0xE8, 0xF8, 0xF5),
        3: RGBColor(0xE8, 0xF8, 0xF5),
    }
    add_styled_table(
        s2, left=0.5, top=1.35, width=8.65, height=5.45,
        headers=headers_s2, rows=rows_s2,
        col_widths=[1.25, 4.10, 0.85, 1.30, 1.15],
        font_size=9.5, header_font_size=10.0,
        highlight_rows=highlight_s2, bold_cols={0, 2, 4}
    )

    # Right Side KPI & Team Cards
    add_kpi_card(
        s2, left=9.35, top=1.35, width=1.68, height=1.25,
        big_value="50%", label="Πρόοδος Φάσης Α",
        sublabel="Ζητούμενα 1 έως 4", accent_color=COLOR_TEAL
    )
    add_kpi_card(
        s2, left=11.15, top=1.35, width=1.68, height=1.25,
        big_value="174.523", label="Δείγματα (1 Hz)",
        sublabel="135 Traces Κίνησης", accent_color=COLOR_BLUE
    )

    add_card(
        s2, left=9.35, top=2.75, width=3.48, height=2.05,
        title="Ομάδα Έργου & Κατανομή Ρόλων",
        header_bg=COLOR_NAVY,
        border_color=COLOR_NAVY,
        font_size=10.0,
        bullets=[
            ("Δημήτριος Τσανακτσής (Α.Μ.: 1100736):", "Ανάλυση 5G προβλήματος (Ζ1), προεπεξεργασία & EDA (Ζ2), αξιολόγηση μετρικών."),
            ("Ιάσωνας Δερβένης (Α.Μ.: 1097437):", "Σχεδίαση παραθύρων & XGBoost Grid Search (Ζ3), ανάλυση Explainable AI / TreeSHAP (Ζ4).")
        ]
    )

    add_card(
        s2, left=9.35, top=4.95, width=3.48, height=1.85,
        title="Στόχος Ενδιάμεσης Παρουσίασης",
        header_bg=COLOR_TEAL,
        border_color=COLOR_TEAL,
        font_size=9.8,
        bullets=[
            ("1. Θεμελίωση 5G:", "Μετάβαση από Reactive σε Proactive έλεγχο."),
            ("2. Αυστηρή Μεθοδολογία:", "Μηδενικό Data Leakage στα 135 traces."),
            ("3. Πλήρης Αξιολόγηση ML & XAI:", "16 μοντέλα XGBoost (L×H) + ερμηνεία SHAP.")
        ]
    )

    set_slide_notes(
        s2,
        "Στη 2η διαφάνεια παρουσιάζουμε τη συνολική δομή του Θέματος 11 και το πώς κατανέμονται τα ποσοστά βαθμολόγησης. "
        "Η εργασία χωρίζεται σε δύο ισοβαρή τμήματα: τη Φάση Α (Ενδιάμεση Παρουσίαση, 50%) που περιλαμβάνει τα Ζητούμενα 1, 2, 3 και 4 "
        "τα οποία έχουν ολοκληρωθεί πλήρως, και τη Φάση Β (Τελική Παρουσίαση, 50%) που περιλαμβάνει τα Ζητούμενα 5 έως 8. "
        "Η ομάδα μας αποτελείται από τον Δημήτριο Τσανακτσή (Α.Μ. 1100736) και τον Ιάσωνα Δερβένη (Α.Μ. 1097437)."
    )

    # =========================================================================
    # SLIDE 3: Ζητούμενο 1 (10%) — Το Τηλεπικοινωνιακό Πρόβλημα στα Δίκτυα 5G
    # =========================================================================
    s3 = create_content_slide(
        prs, 3,
        "Ζητούμενο 1 (10%) — Το Τηλεπικοινωνιακό Πρόβλημα στα Δίκτυα 5G NR",
        "ΖΗΤΟΥΜΕΝΟ 1: ΤΗΛΕΠΙΚΟΙΝΩΝΙΑΚΗ ΑΝΑΛΥΣΗ & ΔΙΑΚΥΜΑΝΣΕΙΣ ΡΥΘΜΟΥ ΜΕΤΑΔΟΣΗΣ"
    )

    add_card(
        s3, left=0.5, top=1.35, width=6.05, height=4.15,
        title="Αίτια Έντονης Στοχαστικότητας Καναλιού 5G NR",
        header_bg=COLOR_NAVY,
        border_color=COLOR_NAVY,
        font_size=10.5,
        bullets=[
            ("1. Εξασθένηση Φάσματος Sub-6 GHz & mmWave (FR1 / FR2):",
             "Οι υψηλές συχνότητες φέροντος παρουσιάζουν αυξημένο Free-Space Path Loss και έντονη απορρόφηση από φυσικά εμπόδια."),
            ("2. Αστική Σκίαση (Urban Shadowing) & Non-Line-of-Sight:",
             "Κτίρια, γέφυρες, σήραγγες και βαρέα οχήματα προκαλούν απότομες πτώσεις ισχύος (RSRP/RSSI) της τάξης των 15–25 dB μέσα σε λίγα δευτερόλεπτα."),
            ("3. Πολυδιαδρομική Διάδοση (Multipath Fast Fading):",
             "Συμβολή ανακλώμενων κυμάτων που οδηγεί σε ραγδαίες διακυμάνσεις του λόγου σήματος προς θόρυβο (SNR) και του δείκτη CQI."),
            ("4. Υψηλή Κινητικότητα & Φαινόμενο Doppler (f_d = v·f_c / c):",
             "Σε σενάρια αυτοκινήτου (Car) και τρένου (Train > 120 km/h), η μετατόπιση συχνότητας αποσυντονίζει την εκτίμηση καναλιού."),
            ("5. Συχνές Πομπές Handover & Παρεμβολές (Inter-Cell Interference):",
             "Στα όρια κυψέλης (Cell Edge), το RSRQ καταρρέει λόγω παρεμβολών γειτονικών gNBs και καθυστερήσεων μεταβίβασης.")
        ]
    )

    add_card(
        s3, left=6.75, top=1.35, width=6.08, height=4.15,
        title="Επιπτώσεις Απρόβλεπτης Πτώσης Throughput στις Υπηρεσίες 5G",
        header_bg=COLOR_BLUE,
        border_color=COLOR_BLUE,
        font_size=10.5,
        bullets=[
            ("▪ eMBB (Enhanced Mobile Broadband — 4K/8K Video, Cloud Gaming, XR):",
             "Αιφνίδια πτώση του DL_bitrate κάτω από το κατώφλι των 5 Mbps προκαλεί άδειασμα του buffer αναπαραγωγής (video stall/re-buffering) και πτώση ανάλυσης."),
            ("▪ URLLC (Ultra-Reliable Low-Latency Communications):",
             "Η καθυστερημένη προσαρμογή του Modulation & Coding Scheme (MCS) εκτοξεύει το Block Error Rate (BLER > 10%), απαιτώντας πολλαπλές επαναμεταδόσεις HARQ που παραβιάζουν το αυστηρό όριο καθυστέρησης (< 1–5 ms)."),
            ("▪ V2X & Σιδηροδρομικές Επικοινωνίες (Connected Vehicles / Railways):",
             "Κατά τη διέλευση από ζώνες χαμηλής κάλυψης, η απώλεια ρυθμού μετάδοσης διακόπτει τη ροή τηλεμετρίας HD χαρτών και σηματοδοσίας ασφαλείας."),
            ("▪ Επίπεδο Μεταφοράς (TCP Congestion Control Collapse):",
             "Τα χαμένα πακέτα στο ραδιοκανάλι ερμηνεύονται από το TCP ως συμφόρηση δικτύου, μειώνοντας στο μισό το Congestion Window (cwnd) και υποχρησιμοποιώντας το κανάλι ακόμα και μετά την ανάκαμψη του σήματος!")
        ]
    )

    # Bottom 4 KPI Callout Cards
    add_kpi_card(
        s3, left=0.5, top=5.65, width=2.92, height=1.22,
        big_value="0 – 173 Mbps", label="Εύρος DL_bitrate Dataset",
        sublabel="Ακραία δυναμική διακύμανση", accent_color=COLOR_NAVY
    )
    add_kpi_card(
        s3, left=3.63, top=5.65, width=2.92, height=1.22,
        big_value="15 – 25 dB", label="Βύθιση Ισχύος Shadowing",
        sublabel="Εντός παραθύρου 1–3 sec", accent_color=COLOR_RED
    )
    add_kpi_card(
        s3, left=6.76, top=5.65, width=2.92, height=1.22,
        big_value="BLER > 10%", label="Αστοχία Link Adaptation",
        sublabel="Όταν το CQI report καθυστερεί", accent_color=COLOR_ORANGE
    )
    add_kpi_card(
        s3, left=9.90, top=5.65, width=2.93, height=1.22,
        big_value="< 5 Mbps", label="Κατώφλι Κινδύνου SLA",
        sublabel="Κρίσιμο όριο για 4K / XR ροές", accent_color=COLOR_TEAL
    )

    set_slide_notes(
        s3,
        "Ξεκινώντας με το Ζητούμενο 1 (10%), εξετάζουμε γιατί η πρόβλεψη του Downlink Bitrate αποτελεί θεμελιώδες πρόβλημα στα δίκτυα 5G NR. "
        "Το ασύρματο κανάλι υπόκειται σε έντονη στοχαστικότητα λόγω πέντε παραγόντων: της εξασθένησης στις ζώνες Sub-6GHz και mmWave, "
        "της αστικής σκίασης (shadowing) από κτίρια που ρίχνει την ισχύ κατά 15-25 dB μέσα σε λίγα δευτερόλεπτα, του multipath fast fading, "
        "του φαινομένου Doppler σε κινούμενα οχήματα/τρένα και των συχνών handovers στα όρια των κυψελών. "
        "Όταν το throughput πέφτει απροειδοποίητα, οι υπηρεσίες eMBB παθαίνουν buffering, οι υπηρεσίες URLLC υφίστανται αύξηση του BLER και "
        "καθυστέρηση λόγω επαναμεταδόσεων HARQ, ενώ το πρωτόκολλο TCP μειώνει δραματικά το παράθυρο μετάδοσης."
    )

    # =========================================================================
    # SLIDE 4: Ζητούμενο 1 (10%) — Reactive vs. Proactive Διαχείριση Πόρων 5G
    # =========================================================================
    s4 = create_content_slide(
        prs, 4,
        "Ζητούμενο 1 (10%) — Reactive vs. Proactive Διαχείριση Πόρων 5G",
        "ΖΗΤΟΥΜΕΝΟ 1: ΜΕΤΑΒΑΣΗ ΑΠΟ ΚΛΑΣΙΚΟ ΕΛΕΓΧΟ ΣΕ ΠΡΟΛΗΠΤΙΚΗ ΔΙΑΧΕΙΡΙΣΗ ΜΕ ML"
    )

    fig13 = FIGURES_DIR / "13_5g_reactive_vs_proactive_arch.png"
    add_picture_fit(
        s4, fig13, left=0.5, top=1.32, max_w=7.75, max_h=5.55,
        caption="Σχήμα 1: Σύγκριση Κλασικής (Reactive) και Προληπτικής (Proactive AI) Αρχιτεκτονικής 5G (O-RAN Near-RT RIC)"
    )

    add_card(
        s4, left=8.42, top=1.32, width=4.41, height=1.70,
        title="Γιατί Αποτυγχάνει η Κλασική (Reactive) Διαχείριση;",
        header_bg=COLOR_RED,
        border_color=COLOR_RED,
        font_size=9.5,
        bullets=[
            ("• Αντίδραση Κατόπιν Εορτής (t > 6s):",
             "Το δίκτυο ανιχνεύει το πρόβλημα μόνο αφού αυξηθούν τα πακέτα NACK και καταρρεύσει το DL_bitrate."),
            ("• Αποτέλεσμα:",
             "Radio Link Failure (RLF), απώλεια πακέτων στο RLC buffer και παραβίαση του SLA πριν ολοκληρωθεί το Handover.")
        ]
    )

    add_card(
        s4, left=8.42, top=3.14, width=4.41, height=3.73,
        title="4 Μηχανισμοί Proactive 5G μέσω Πρόβλεψης (t + H)",
        header_bg=COLOR_TEAL,
        border_color=COLOR_TEAL,
        font_size=9.5,
        bullets=[
            ("1. Προληπτικό Handover (Conditional Handover - 3GPP Rel.16):",
             "Αν προβλεφθεί πτώση ρυθμού σε ορίζοντα H=3–5s, ο σταθμός βάσης (gNB) προ-δεσμεύει πόρους στον γειτονικό σταθμό πριν χαθεί η ζεύξη."),
            ("2. Προληπτικό Link Adaptation (MCS & HARQ):",
             "Έγκαιρη μείωση του δείκτη MCS (π.χ. από 64-QAM σε 16-QAM/QPSK) πριν την είσοδο σε ζώνη σκίασης, διατηρώντας το BLER < 1%."),
            ("3. Δυναμικός Προγραμματισμός Πόρων (MAC PRB Scheduling):",
             "Ο scheduler του gNB ή το O-RAN Near-RT RIC (xApp) εκχωρεί επιπλέον Physical Resource Blocks (PRBs) σε χρήστες με επικείμενη υποβάθμιση."),
            ("4. Cross-Layer Προσαρμογή Εφαρμογών (ABR Pre-Buffering):",
             "Ενημέρωση του MEC video server ώστε να προ-φορτώσει (pre-buffer) τμήματα βίντεο όσο το κανάλι είναι ακόμη ισχυρό.")
        ]
    )

    set_slide_notes(
        s4,
        "Στη διαφάνεια 4 παρουσιάζουμε τη σύγκριση μεταξύ της κλασικής Reactive διαχείρισης και της προτεινόμενης Proactive διαχείρισης μέσω Μηχανικής Μάθησης. "
        "Στην κλασική προσέγγιση (πάνω αριστερά στο διάγραμμα), το δίκτυο αντιδρά αφού πρώτα καταρρεύσει το σήμα και χαθούν πακέτα, με αποτέλεσμα "
        "ο χρήστης να βιώνει διακοπή υπηρεσίας. Αντίθετα, ενσωματώνοντας ένα μοντέλο πρόβλεψης στον σταθμό βάσης (gNB) ή ως xApp στον Near-RT RIC "
        "της αρχιτεκτονικής O-RAN, προβλέπουμε το DL_bitrate σε ορίζοντα H=1 έως 10 δευτερόλεπτα μπροστά. Αυτό ξεκλειδώνει 4 κρίσιμους μηχανισμούς: "
        "Conditional Handover πριν την αποσύνδεση, έγκαιρη προσαρμογή MCS, δυναμική δέσμευση PRBs στον MAC scheduler και προ-φόρτωση video buffer."
    )

    # =========================================================================
    # SLIDE 5: Ζητούμενο 2 (15%) — Παρουσίαση του UCC 4G/LTE Dataset & Σενάρια Κίνησης
    # =========================================================================
    s5 = create_content_slide(
        prs, 5,
        "Ζητούμενο 2 (15%) — Το Σύνολο Δεδομένων UCC & τα 5 Σενάρια Κινητικότητας",
        "ΖΗΤΟΥΜΕΝΟ 2: ΑΝΑΛΥΣΗ ΔΕΔΟΜΕΝΩΝ ΠΕΔΙΟΥ (135 TRACES | 174.523 ΕΓΓΡΑΦΕΣ)"
    )

    headers_s5 = ["Σενάριο Κίνησης", "Traces (Σύνολο)", "Train / Test Traces", "Δείγματα (1 Hz)", "Ποσοστό", "Μέση Ταχύτητα", "Μέσο DL_bitrate"]
    rows_s5 = [
        ["Car (Αυτοκίνητο)", "53 traces", "42 Train / 11 Test", "75.874", "43,5%", "26,5 km/h", "13.866 kbps"],
        ["Train (Τρένο)", "20 traces", "16 Train / 4 Test", "38.976", "22,3%", "77,7 km/h", "4.985 kbps"],
        ["Pedestrian (Πεζός)", "31 traces", "24 Train / 7 Test", "33.629", "19,3%", "2,2 km/h", "10.987 kbps"],
        ["Static (Στατικό)", "15 traces", "12 Train / 3 Test", "15.261", "8,7%", "3,7 km/h", "10.813 kbps"],
        ["Bus (Λεωφορείο)", "16 traces", "12 Train / 4 Test", "10.783", "6,2%", "14,8 km/h", "10.004 kbps"],
        ["ΣΥΝΟΛΟ DATASET", "135 traces", "106 Train / 29 Test", "174.523", "100,0%", "31,4 km/h", "10.822 kbps"],
    ]
    add_styled_table(
        s5, left=0.5, top=1.32, width=12.33, height=2.25,
        headers=headers_s5, rows=rows_s5,
        col_widths=[2.15, 1.45, 1.95, 1.65, 1.15, 1.75, 2.23],
        font_size=9.2, header_font_size=9.5,
        highlight_rows={5: RGBColor(0xD6, 0xEA, 0xF8)},
        bold_cols={0, 1, 3, 6}
    )

    fig16 = FIGURES_DIR / "16_dataset_mobility_breakdown.png"
    add_picture_fit(
        s5, fig16, left=0.5, top=3.68, max_w=12.33, max_h=3.25,
        caption="Σχήμα 2: Κατανομή δειγμάτων και traces ανά σενάριο κίνησης (80/20 split) και προφίλ Μέσου Throughput vs Ταχύτητας Κίνησης"
    )

    set_slide_notes(
        s5,
        "Προχωράμε στο Ζητούμενο 2 (15%), το οποίο αφορά την ενοποίηση και προεπεξεργασία του πραγματικού συνόλου δεδομένων του University College Cork (UCC). "
        "Φορτώσαμε και ενοποιήσαμε συνολικά 135 αρχεία CSV (traces) από 5 διαφορετικά σενάρια κινητικότητας: αυτοκίνητο (53 traces, 75.874 δείγματα), "
        "τρένο (20 traces, 38.976 δείγματα), πεζός (31 traces, 33.629 δείγματα), στατικός χρήστης (15 traces, 15.261 δείγματα) και λεωφορείο (16 traces, 10.783 δείγματα). "
        "Συνολικά έχουμε 174.523 μετρήσεις με ρυθμό δειγματοληψίας 1 Hz (μία μέτρηση ανά δευτερόλεπτο, δηλαδή πάνω από 48,5 ώρες πραγματικής τηλεμετρίας). "
        "Όπως φαίνεται στον πίνακα και στο γράφημα, το σενάριο του τρένου εμφανίζει τη μεγαλύτερη μέση ταχύτητα (77,7 km/h) και το χαμηλότερο μέσο throughput (4.985 kbps) λόγω των συνεχών handovers."
    )

    # =========================================================================
    # SLIDE 6: Ζητούμενο 2 (15%) — Ανάλυση των Μετρικών Ποιότητας Ραδιοκαναλιού (KPIs)
    # =========================================================================
    s6 = create_content_slide(
        prs, 6,
        "Ζητούμενο 2 (15%) — Ανάλυση των Μετρικών Ποιότητας Ραδιοκαναλιού (KPIs)",
        "ΖΗΤΟΥΜΕΝΟ 2: ΦΥΣΙΚΗ ΕΡΜΗΝΕΙΑ ΤΩΝ 8 ΜΕΤΑΒΛΗΤΩΝ ΕΙΣΟΔΟΥ & ΤΗΣ ΜΕΤΑΒΛΗΤΗΣ ΣΤΟΧΟΥ"
    )

    headers_s6 = ["Μεταβλητή (KPI)", "Ρόλος", "Μονάδα", "Εύρος Dataset", "Φυσική Σημασία στα Πρότυπα 3GPP LTE / 5G NR"]
    rows_s6 = [
        ["RSRP", "Είσοδος (X)", "dBm", "[-200, -44]", "Reference Signal Received Power: Μέση ισχύς των σημάτων αναφοράς (CRS/SSB) από την εξυπηρετούσα κυψέλη."],
        ["RSRQ", "Είσοδος (X)", "dB", "[-24, +4]", "Reference Signal Received Quality: Λόγος N·RSRP/RSSI· μετρά την ποιότητα σήματος υπό την παρουσία παρεμβολών."],
        ["SNR", "Είσοδος (X)", "dB", "[-30, +33]", "Signal-to-Noise Ratio: Λόγος ισχύος σήματος προς θόρυβο· καθορίζει άμεσα τη θεωρητική χωρητικότητα Shannon."],
        ["CQI", "Είσοδος (X)", "Δείκτης 1–15", "[1, 15]", "Channel Quality Indicator: Αναφορά του UE προς τον σταθμό βάσης για την επιλογή βέλτιστου σχήματος MCS."],
        ["RSSI", "Είσοδος (X)", "dBm", "[-113, -45]", "Received Signal Strength Indicator: Συνολική λαμβανόμενη ισχύς στο εύρος ζώνης (σήμα + παρεμβολές + θόρυβος)."],
        ["Speed", "Είσοδος (X)", "km/h", "[0, 163]", "Ταχύτητα κίνησης τερματικού (GPS): Συνδέεται με τη μετατόπιση Doppler (f_d) και τη συχνότητα των handovers."],
        ["UL_bitrate", "Είσοδος (X)", "kbps", "[0, 48.204]", "Ρυθμός μετάδοσης Uplink: Αντικατοπτρίζει την ενεργή αμφίδρομη κίνηση (TCP ACKs) και τη δέσμευση πόρων."],
        ["ServingCell_Distance", "Είσοδος (X)", "m (μέτρα)", "[12, 35.800]", "Ευκλείδεια απόσταση UE – Σταθμού Βάσης: Καθορίζει τις απώλειες διαδρομής μεγάλης κλίμακας (Macro Path Loss)."],
        ["DL_bitrate (Στόχος)", "Στόχος (y)", "kbps", "[0, 173.016]", "Ρυθμός μετάδοσης Downlink (Throughput): Η μεταβλητή προς πρόβλεψη στις μελλοντικές χρονικές στιγμές t + H."],
    ]
    add_styled_table(
        s6, left=0.5, top=1.32, width=12.33, height=4.35,
        headers=headers_s6, rows=rows_s6,
        col_widths=[2.10, 1.25, 1.15, 1.45, 6.38],
        font_size=9.2, header_font_size=9.8,
        highlight_rows={8: RGBColor(0xFD, 0xED, 0xEC)},
        bold_cols={0, 1, 2}
    )

    # Bottom 3 summary explanation cards
    add_card(
        s6, left=0.5, top=5.80, width=3.95, height=1.12,
        title="1. Μετρικές Φυσικού Επιπέδου (PHY)",
        border_color=COLOR_NAVY, font_size=9.2, title_size=10.5,
        bullets=[("RSRP, RSRQ, SNR, CQI, RSSI:", "Αποτυπώνουν την στιγμιαία ποιότητα της ραδιοζεύξης, τον θόρυβο και τις παρεμβολές ομοκαναλικών κυψελών.")]
    )
    add_card(
        s6, left=4.68, top=5.80, width=3.95, height=1.12,
        title="2. Γεωμετρικές & Κινηματικές Μετρικές",
        border_color=COLOR_TEAL, font_size=9.2, title_size=10.5,
        bullets=[("Speed & ServingCell_Distance:", "Περιγράφουν τη δυναμική απομάκρυνση από την κεραία και την ταχύτητα διέλευσης από ζώνες σκίασης.")]
    )
    add_card(
        s6, left=8.88, top=5.80, width=3.95, height=1.12,
        title="3. Μετρική Επιπέδου Κίνησης (Traffic)",
        border_color=COLOR_ORANGE, font_size=9.2, title_size=10.5,
        bullets=[("UL_bitrate → DL_bitrate:", "Ισχυρός δείκτης ενεργού συνόδου εφαρμογής και ροής πακέτων επιβεβαίωσης TCP ACK.")]
    )

    set_slide_notes(
        s6,
        "Στη διαφάνεια 6 παρουσιάζουμε αναλυτικά τις 8 αριθμητικές μετρικές εισόδου και τη μεταβλητή-στόχο DL_bitrate. "
        "Οι 8 μεταβλητές εισόδου χωρίζονται σε τρεις φυσικές κατηγορίες: "
        "Πρώτον, τις 5 μετρικές ραδιοκαναλιού του προτύπου 3GPP: RSRP (ισχύς σήματος αναφοράς σε dBm), RSRQ (ποιότητα σήματος σε dB), "
        "SNR (λόγος σήματος προς θόρυβο σε dB), CQI (δείκτης ποιότητας καναλιού από 1 έως 15) και RSSI (συνολική λαμβανόμενη ισχύς). "
        "Δεύτερον, τις 2 κινηματικές/γεωμετρικές μετρικές: την ταχύτητα κίνησης Speed (km/h) και την απόσταση από τον σταθμό βάσης ServingCell_Distance (m). "
        "Τρίτον, τον ρυθμό μετάδοσης Uplink (UL_bitrate σε kbps), ο οποίος αποτυπώνει την ενεργή κίνηση της συνεδρίας."
    )

    # =========================================================================
    # SLIDE 7: Ζητούμενο 2 (15%) — Σωλήνωση Προεπεξεργασίας & Καθαρισμός Null Τιμών ('-')
    # =========================================================================
    s7 = create_content_slide(
        prs, 7,
        "Ζητούμενο 2 (15%) — Σωλήνωση Προεπεξεργασίας & Καθαρισμός Τιμών ('-')",
        "ΖΗΤΟΥΜΕΝΟ 2: ΔΙΑΤΗΡΗΣΗ ΧΡΟΝΙΚΗΣ ΣΥΝΕΧΕΙΑΣ 1 Hz & ΚΑΘΑΡΙΣΜΟΣ ΑΝΑ TRACE"
    )

    fig14 = FIGURES_DIR / "14_preprocessing_pipeline_diagram.png"
    add_picture_fit(
        s7, fig14, left=0.5, top=1.30, max_w=12.33, max_h=3.65,
        caption="Σχήμα 3: Πενταφασική Σωλήνωση Προεπεξεργασίας Χρονοσειρών (Ingestion → Imputation → Trace Split → Scaling → Windowing)"
    )

    add_card(
        s7, left=0.5, top=5.05, width=4.0, height=1.88,
        title="Το Πρόβλημα των Συμβόλων '-' στα CSV",
        header_bg=COLOR_RED, border_color=COLOR_RED, font_size=9.3, title_size=11.0,
        bullets=[
            ("• Μη έγκυρες εγγραφές:", "Κατά τη διάρκεια handovers ή προσωρινής απώλειας GPS/CQI, ο καταγραφέας γράφει το αλφαριθμητικό '-' αντί αριθμού."),
            ("• Γιατί ΔΕΝ διαγράφουμε γραμμές (dropna):", "Η διαγραφή γραμμών καταστρέφει τον σταθερό βηματισμό Δt = 1s, αλλοιώνοντας τους ορίζοντες t + H!")
        ]
    )

    add_card(
        s7, left=4.66, top=5.05, width=4.0, height=1.88,
        title="Session-Aware Συμπλήρωση (ffill / bfill)",
        header_bg=COLOR_BLUE, border_color=COLOR_BLUE, font_size=9.3, title_size=11.0,
        bullets=[
            ("• Μετατροπή σε NaN:", "Όλα τα '-', 'None', '' μετατρέπονται σε float NaN μέσω pd.to_numeric(..., errors='coerce')."),
            ("• Απομόνωση ανά trace_id:", "Εφαρμογή groupby('trace_id').transform(lambda g: g.ffill().bfill()) ώστε καμία τιμή να μην διαρρέει μεταξύ διαφορετικών διαδρομών.")
        ]
    )

    add_card(
        s7, left=8.83, top=5.05, width=4.0, height=1.88,
        title="Φυσικοί Περιορισμοί Πεδίου (Domain Clipping)",
        header_bg=COLOR_TEAL, border_color=COLOR_TEAL, font_size=9.3, title_size=11.0,
        bullets=[
            ("• Έλεγχος Φυσικών Ορίων 3GPP:",
             "Επιβολή αυστηρών ορίων: CQI ∈ [0, 15], DL_bitrate ≥ 0 kbps, UL_bitrate ≥ 0 kbps, Speed ∈ [0, 250] km/h."),
            ("• Τελικό Αποτέλεσμα:", "174.523 πλήρως καθαρές, συνεχείς εγγραφές (0% missing values).")
        ]
    )

    set_slide_notes(
        s7,
        "Στη διαφάνεια 7 αναλύουμε τη σωλήνωση προεπεξεργασίας που υλοποιήσαμε στο αρχείο src/data_processing.py. "
        "Στα ακατέργαστα αρχεία CSV, όποτε το τερματικό έχανε στιγμιαία τη μέτρηση κάποιου δείκτη (π.χ. CQI ή ServingCell_Distance κατά το handover), "
        "καταγραφόταν ο χαρακτήρας της παύλας ('-'). Αν κάναμε απλή διαγραφή γραμμών (dropna), θα δημιουργούνταν χρονικά κενά στην ακολουθία 1 Hz "
        "και το παράθυρο των 10 βημάτων δεν θα αντιστοιχούσε πλέον σε 10 δευτερόλεπτα. "
        "Γι' αυτό μετατρέψαμε τις παύλες σε NaN και εφαρμόσαμε session-aware forward-fill και backward-fill αυστηρά εντός του κάθε trace_id ξεχωριστά, "
        "ώστε να διατηρηθεί η χρονική συνέχεια χωρίς καμία ανάμειξη διαφορετικών διαδρομών."
    )

    # =========================================================================
    # SLIDE 8: Ζητούμενο 2 (15%) — Χωρισμός Train/Test Χωρίς Data Leakage & Κανονικοποίηση
    # =========================================================================
    s8 = create_content_slide(
        prs, 8,
        "Ζητούμενο 2 (15%) — Αποτροπή Data Leakage & Κανονικοποίηση (StandardScaler)",
        "ΖΗΤΟΥΜΕΝΟ 2: STRATIFIED TRACE-LEVEL SPLIT (80% / 20%) & Z-SCORE ΚΑΝΟΝΙΚΟΠΟΙΗΣΗ"
    )

    headers_s8 = ["Κριτήριο Σύγκρισης", "❌ Τυχαίος Χωρισμός Γραμμών (Random Row Split)", "✔ Χωρισμός ανά Συνεδρία (Stratified Trace Split — Δική μας Επιλογή)"]
    rows_s8 = [
        ["Μονάδα Διαχωρισμού", "Μεμονωμένες χρονικές στιγμές t (γραμμές CSV)", "Ολόκληρα αρχεία διαδρομών (πλήρη trace_id sessions)"],
        ["Χρονική Επικάλυψη", "Η στιγμή t στο Train και η t+1 στο Test απέχουν μόλις 1 sec!", "Μηδενική χρονική επικάλυψη· ανεξάρτητες διαδρομές"],
        ["Επικάλυψη Παραθύρων", "Τα Sliding Windows [t-L+1..t] μοιράζονται 90% κοινές τιμές!", "Κανένα παράθυρο Train δεν τέμνεται με παράθυρο Test"],
        ["Αξιοπιστία Μετρικών", "Τεχνητά διογκωμένο R² (σοβαρό Temporal Data Leakage)", "Ρεαλιστική αξιολόγηση γενίκευσης σε άγνωστες διαδρομές UE"],
        ["Κατανομή Δεδομένων", "Μη ελεγχόμενη συνέχεια χρονοσειράς", "80% Train (106 traces / 131.370 δείγματα) | 20% Test (29 traces / 43.153 δείγματα)"],
    ]
    add_styled_table(
        s8, left=0.5, top=1.32, width=12.33, height=2.65,
        headers=headers_s8, rows=rows_s8,
        col_widths=[2.45, 4.80, 5.08],
        font_size=9.5, header_font_size=10.0,
        bold_cols={0, 2}
    )

    add_card(
        s8, left=0.5, top=4.15, width=6.05, height=2.75,
        title="Stratified Split ανά Σενάριο Κινητικότητας (80% – 20%)",
        header_bg=COLOR_NAVY, border_color=COLOR_NAVY, font_size=10.0,
        bullets=[
            ("• Διαστρωματωμένη Επιλογή (Stratification):",
             "Για κάθε ένα από τα 5 σενάρια (bus, car, pedestrian, static, train), το 80% των traces επιλέγεται τυχαία (seed=42) για εκπαίδευση και το 20% για έλεγχο."),
            ("• Σύνολο Εκπαίδευσης (Train Set):",
             "106 πλήρη traces → 131.370 χρονικές εγγραφές (75,3% των δειγμάτων)."),
            ("• Σύνολο Ελέγχου (Test Set):",
             "29 πλήρη traces → 43.153 χρονικές εγγραφές (24,7% των δειγμάτων).")
        ]
    )

    add_card(
        s8, left=6.78, top=4.15, width=6.05, height=2.75,
        title="Κανονικοποίηση Z-Score (StandardScaler Χωρίς Leakage)",
        header_bg=COLOR_TEAL, border_color=COLOR_TEAL, font_size=10.0,
        bullets=[
            ("• Μαθηματικός Μετασχηματισμός:",
             "z = (x - μ_train) / σ_train, ώστε κάθε μία από τις 8 μετρικές εισόδου να έχει μέση τιμή μ = 0 και τυπική απόκλιση σ = 1."),
            ("• Αυστηρή Εκπαίδευση ΜΟΝΟ στο Train Set:",
             "Ο StandardScaler καλεί scaler.fit(train_df[NUMERIC_FEATURES]) αποκλειστικά στο Train set και εφαρμόζει scaler.transform() στο Test set."),
            ("• Διατήρηση Φυσικής Κλίμακας Στόχου:",
             "Το DL_bitrate διατηρείται σε kbps για άμεση φυσική ερμηνεία των RMSE και MAE.")
        ]
    )

    set_slide_notes(
        s8,
        "Στη διαφάνεια 8 παρουσιάζουμε μία από τις πιο κρίσιμες μεθοδολογικές επιλογές της εργασίας μας: την αποτροπή του Data Leakage. "
        "Σε δεδομένα χρονοσειρών 1 Hz, αν κάναμε τυχαίο χωρισμό γραμμών (random row split), η μέτρηση στο δευτερόλεπτο t θα βρισκόταν στο Train set "
        "και η μέτρηση στο t+1 στο Test set, προκαλώντας90% επικάλυψη στα κυλιόμενα παράθυρα! "
        "Αντί γι' αυτό, εφαρμόσαμε Stratified Trace-Level Split: χωρίσαμε ολόκληρα τα αρχεία διαδρομών ανά σενάριο κίνησης σε 106 traces εκπαίδευσης "
        "(131.370 δείγματα) και 29 traces ελέγχου (43.153 δείγματα). Επιπλέον, ο StandardScaler (z = (x-μ)/σ) υπολογίζει τις παραμέτρους μ και σ "
        "αποκλειστικά πάνω στο Train set και αποθηκεύεται στο feature_scaler.joblib."
    )

    # =========================================================================
    # SLIDE 9: Ζητούμενο 2 (15%) — Ερευνητική Ανάλυση Δεδομένων (EDA): Κατανομές KPIs
    # =========================================================================
    s9 = create_content_slide(
        prs, 9,
        "Ζητούμενο 2 (15%) — Ερευνητική Ανάλυση Δεδομένων (EDA): Κατανομές KPIs",
        "ΖΗΤΟΥΜΕΝΟ 2: ΣΤΑΤΙΣΤΙΚΕΣ ΙΔΙΟΤΗΤΕΣ ΚΑΝΑΛΙΟΥ & ΑΣΥΜΜΕΤΡΙΑ THROUGHPUT"
    )

    fig1 = FIGURES_DIR / "01_eda_distributions.png"
    add_picture_fit(
        s9, fig1, left=0.5, top=1.32, max_w=7.75, max_h=5.55,
        caption="Σχήμα 4: Ιστογράμματα κατανομής και καμπύλες πυκνότητας (KDE) των 6 βασικών μετρικών (DL_bitrate, RSRP, RSRQ, SNR, CQI, Speed)"
    )

    add_card(
        s9, left=8.42, top=1.32, width=4.41, height=3.85,
        title="Στατιστικά Ευρήματα Κατανομών (EDA)",
        header_bg=COLOR_NAVY, border_color=COLOR_NAVY, font_size=9.5,
        bullets=[
            ("1. Έντονα Δεξιά Ασύμμετρη Κατανομή DL_bitrate:",
             "Παρουσιάζει θετική ασυμμετρία (right-skewed / heavy-tailed). Σε τυπικά κανονικοποιημένα/ενεργά υποσύνολα: Mean = 1.401,2 kbps (Std = 2.135,4 kbps, Max = 17.510 kbps), ενώ στο πλήρες εύρος αιχμών φτάνει: Mean = 10.822,3 kbps, Median = 5.370 kbps, Max = 173.016 kbps."),
            ("2. Διτροπική Συμπεριφορά RSRP & RSRQ:",
             "Το RSRP επικεντρώνεται μεταξύ -115 dBm και -75 dBm. Το RSRQ εμφανίζει δύο διακριτές κορυφές: μία γύρω στα -13 dB (φορτωμένη κυψέλη με παρεμβολές) και μία στα -2 dB (καθαρή ζεύξη)."),
            ("3. Διακριτή Κατανομή CQI (1 έως 15):",
             "Κυριαρχούν οι τιμές CQI ∈ {6, 7, 8, 9}, που αντιστοιχούν σε διαμόρφωση 16-QAM, με δευτερεύουσες αιχμές στο CQI=2 (QPSK) και CQI=12–15 (64-QAM)."),
            ("4. Πολυτροπική Ταχύτητα (Multi-modal Speed):",
             "Έντονη συγκέντρωση στο 0–5 km/h (Static/Pedestrian), δεύτερη ζώνη στα 20–60 km/h (Bus/Car) και ουρά έως 160+ km/h (Train).")
        ]
    )

    # 2 KPI Cards on bottom right
    add_kpi_card(
        s9, left=8.42, top=5.32, width=2.14, height=1.55,
        big_value="1.401 / 10.822", label="Mean DL_bitrate (kbps)",
        sublabel="Υποσύνολο αναφοράς / Πλήρες Dataset", accent_color=COLOR_BLUE
    )
    add_kpi_card(
        s9, left=10.69, top=5.32, width=2.14, height=1.55,
        big_value="2.135 / 14.150", label="Std DL_bitrate (kbps)",
        sublabel="Υψηλή τυπική απόκλιση (σ > μ)", accent_color=COLOR_ORANGE
    )

    set_slide_notes(
        s9,
        "Στη διαφάνεια 9 παρουσιάζουμε την Ερευνητική Ανάλυση Δεδομένων (EDA) για τις κατανομές των μετρικών ποιότητας. "
        "Παρατηρούμε ότι ο ρυθμός μετάδοσης DL_bitrate δεν ακολουθεί κανονική κατανομή, αλλά έντονα ασύμμετρη κατανομή προς τα δεξιά (right-skewed) "
        "όπου η τυπική απόκλιση υπερβαίνει τη μέση τιμή (Mean = 1.401,2 kbps, Std = 2.135,4 kbps, Max = 17.510 kbps στο τυπικό κανονικοποιημένο προφίλ "
        "και Mean = 10.822,3 kbps, Std = 14.149,7 kbps, Max = 173.016 kbps στο σύνολο των αιχμών). "
        "Επίσης, το RSRQ παρουσιάζει διτροπική κατανομή (bimodal), διαχωρίζοντας καθαρά τις καταστάσεις χαμηλών παρεμβολών (-2 dB) από τις καταστάσεις "
        "έντονης ομοκαναλικής παρεμβολής (-13 dB). Αυτή η μη-γραμμική και πολυτροπική φύση των δεδομένων αιτιολογεί την επιλογή μη-γραμμικών μοντέλων όπως το XGBoost."
    )

    # =========================================================================
    # SLIDE 10: Ζητούμενο 2 (15%) — Επίδραση Κινητικότητας & Συσχετίσεις Μεταβλητών
    # =========================================================================
    s10 = create_content_slide(
        prs, 10,
        "Ζητούμενο 2 (15%) — Επίδραση Κινητικότητας & Πίνακας Συσχετίσεων (Pearson)",
        "ΖΗΤΟΥΜΕΝΟ 2: ΔΙΑΚΥΜΑΝΣΗ ΑΝΑ ΣΕΝΑΡΙΟ ΚΙΝΗΣΗΣ & ΣΥΣΧΕΤΙΣΕΙΣ ΜΕΤΑΒΛΗΤΩΝ"
    )

    fig2 = FIGURES_DIR / "02_eda_mobility_comparison.png"
    add_picture_fit(
        s10, fig2, left=0.5, top=1.32, max_w=7.75, max_h=5.55,
        caption="Σχήμα 5: Boxplots DL_bitrate ανά σενάριο κίνησης (αριστερά) και Θερμικός Χάρτης Συσχέτισης Pearson (δεξιά)"
    )

    add_card(
        s10, left=8.42, top=1.32, width=4.41, height=2.68,
        title="Ανάλυση Επίδρασης Κινητικότητας (Boxplots)",
        header_bg=COLOR_NAVY, border_color=COLOR_NAVY, font_size=9.5,
        bullets=[
            ("• Υψηλή Διασπορά στο Αυτοκίνητο (Car):",
             "Εμφανίζει το μεγαλύτερο ενδοτεταρτημοριακό εύρος (IQR) λόγω εναλλαγής ανοιχτών αυτοκινητοδρόμων (υψηλό SNR) και αστικού ιστού."),
            ("• Κατάρρευση Ρυθμού στο Τρένο (Train):",
             "Η διάμεσος (median) πέφτει δραστικά λόγω ταχυτήτων έως 160 km/h, μετατόπισης Doppler και συνεχών cell handovers."),
            ("• Σταθερότητα σε Pedestrian & Static:",
             "Πιο προβλέψιμο κανάλι με λιγότερες αλλαγές εξυπηρετούσας κυψέλης.")
        ]
    )

    add_card(
        s10, left=8.42, top=4.14, width=4.41, height=2.73,
        title="Ευρήματα Πίνακα Συσχέτισης Pearson (r)",
        header_bg=COLOR_TEAL, border_color=COLOR_TEAL, font_size=9.5,
        bullets=[
            ("• Θετική Συσχέτιση με DL_bitrate:",
             "UL_bitrate, SNR, CQI, RSRP και RSSI εμφανίζουν θετικό συντελεστή Pearson με το throughput."),
            ("• Ισχυρή Σύζευξη Μετρικών Ισχύος:",
             "RSRP ↔ RSSI και SNR ↔ CQI παρουσιάζουν ισχυρή θετική γραμμική συσχέτιση (ο δείκτης CQI υπολογίζεται από το SINR)."),
            ("• Γιατί δεν αρκεί η Γραμμική Παλινδρόμηση:",
             "Οι γραμμικοί συντελεστές r είναι μέτριοι διότι η σχέση καναλιού-throughput εξαρτάται από χρονικές υστερήσεις (lags) και μη-γραμμικά κατώφλια MCS.")
        ]
    )

    set_slide_notes(
        s10,
        "Στη διαφάνεια 10 εξετάζουμε πώς επηρεάζει το σενάριο κινητικότητας τον ρυθμό μετάδοσης καθώς και τον πίνακα γραμμικής συσχέτισης Pearson. "
        "Στο αριστερό γράφημα (Boxplots), βλέπουμε ότι το σενάριο Car έχει τη μεγαλύτερη διακύμανση (IQR), ενώ το σενάριο Train εμφανίζει τη χαμηλότερη "
        "διάμεσο λόγω των αλλεπάλληλων handovers σε υψηλές ταχύτητες. "
        "Στο δεξί γράφημα (Correlation Heatmap), παρατηρούμε θετική συσχέτιση του DL_bitrate με τα UL_bitrate, SNR, CQI και RSRP. "
        "Ωστόσο, επειδή οι μεμονωμένες γραμμικές συσχετίσεις δεν μπορούν να συλλάβουν τη μνήμη του καναλιού και τα μη-γραμμικά σκαλοπάτια του MCS, "
        "προχωράμε στην κατασκευή κυλιόμενων παραθύρων χρόνου (Sliding Windows) στο Ζητούμενο 3."
    )

    # =========================================================================
    # SLIDE 11: Ζητούμενο 3 (15%) — Κατασκευή Κυλιόμενων Παραθύρων Χρονοσειρών (Sliding Windows)
    # =========================================================================
    s11 = create_content_slide(
        prs, 11,
        "Ζητούμενο 3 (15%) — Μετασχηματισμός Κυλιόμενων Παραθύρων (Sliding Windows)",
        "ΖΗΤΟΥΜΕΝΟ 3: ΜΑΘΗΜΑΤΙΚΗ ΑΝΑΠΑΡΑΣΤΑΣΗ LOOKBACK (L) & PREDICTION HORIZON (H)"
    )

    fig15 = FIGURES_DIR / "15_sliding_window_mechanism.png"
    add_picture_fit(
        s11, fig15, left=0.5, top=1.32, max_w=7.85, max_h=5.55,
        caption="Σχήμα 6: Μηχανισμός Κυλιόμενου Παραθύρου (L=10s) και Ορίζοντα Πρόβλεψης (t+H) πάνω σε πραγματικό trace δοκιμής"
    )

    add_card(
        s11, left=8.50, top=1.32, width=4.33, height=3.15,
        title="Μαθηματική Formulation Παραθύρων",
        header_bg=COLOR_NAVY, border_color=COLOR_NAVY, font_size=9.5,
        bullets=[
            ("• Πολυμεταβλητό Διάνυσμα Στιγμής t:",
             "x_t ∈ ℝ^8 (οι 8 κανονικοποιημένες μετρικές ποιότητας στη χρονική στιγμή t)."),
            ("• Παράθυρο Ιστορικού (Lookback L):",
             "X_t = [x_{t-L+1}, x_{t-L+2}, ..., x_t] ∈ ℝ^{L × 8}."),
            ("• Flattening για Δέντρα Αποφάσεων (XGBoost):",
             "Το μητρώο L × 8 μετασχηματίζεται σε επίπεδο διάνυσμα χαρακτηριστικών x̃_t ∈ ℝ^{8L} (π.χ. για L=10 → 80 χαρακτηριστικά εισόδου)."),
            ("• Μεταβλητή Στόχος σε Ορίζοντα H:",
             "y_{t+H} = DL_bitrate(t + H) ∈ ℝ_+ (σε kbps).")
        ]
    )

    add_card(
        s11, left=8.50, top=4.60, width=4.33, height=2.27,
        title="Προστασία Ορίων Συνεδρίας (Boundary Safety)",
        header_bg=COLOR_TEAL, border_color=COLOR_TEAL, font_size=9.5,
        bullets=[
            ("• Αυστηρό GroupBy ανά trace_id:",
             "Η συνάρτηση create_sliding_windows() παράγει παράθυρα αποκλειστικά εντός του ίδιου trace_id."),
            ("• Πλήθος Παραθύρων ανά Trace (μήκους N):",
             "Παράγονται ακριβώς (N - L - H + 1) έγκυρα ζεύγη (X_t, y_{t+H})."),
            ("• Grid Παραμέτρων που Εξετάστηκε:",
             "Lookback L ∈ {5, 10, 20, 30}s × Horizon H ∈ {1, 3, 5, 10}s (16 συνδυασμοί).")
        ]
    )

    set_slide_notes(
        s11,
        "Εισερχόμαστε στο Ζητούμενο 3 (15%), όπου μετατρέπουμε το πρόβλημα πρόβλεψης χρονοσειράς σε πρόβλημα επιβλεπόμενης παλινδρόμησης (Supervised Regression) "
        "μέσω κυλιόμενων παραθύρων (Sliding Windows). Για κάθε χρονική στιγμή t, λαμβάνουμε τις L προηγούμενες μετρήσεις των 8 μετρικών καναλιού "
        "από τη στιγμή t-L+1 έως τη στιγμή t. Έτσι σχηματίζεται ένας τανυστής διαστάσεων L επί 8, ο οποίος επιπεδώνεται (flattened) σε διάνυσμα "
        "8 επί L χαρακτηριστικών για να τροφοδοτήσει τον XGBoost Regressor. Στόχος του μοντέλου είναι να προβλέψει την τιμή του DL_bitrate στη χρονική "
        "στιγμή t + H, όπου H είναι ο ορίζοντας πρόβλεψης σε δευτερόλεπτα. Τα παράθυρα δημιουργούνται αυστηρά εντός κάθε trace_id."
    )

    # =========================================================================
    # SLIDE 12: Ζητούμενο 3 (15%) — Αρχιτεκτονική Μοντέλου XGBoost Regressor & Μετρικές
    # =========================================================================
    s12 = create_content_slide(
        prs, 12,
        "Ζητούμενο 3 (15%) — Αρχιτεκτονική XGBoost Regressor & Μετρικές Αξιολόγησης",
        "ΖΗΤΟΥΜΕΝΟ 3: GRADIENT BOOSTED DECISION TREES & ΜΑΘΗΜΑΤΙΚΟΙ ΟΡΙΣΜΟΙ ΜΕΤΡΙΚΩΝ"
    )

    add_card(
        s12, left=0.5, top=1.32, width=5.95, height=3.15,
        title="Γιατί Επιλέχθηκε ο Αλγόριθμος XGBoost Regressor;",
        header_bg=COLOR_NAVY, border_color=COLOR_NAVY, font_size=9.8,
        bullets=[
            ("1. Αριστεία σε Δομημένα Χαρακτηριστικά Υστέρησης (Tabular Lags):",
             "Τα Gradient Boosted Decision Trees (GBDT) διαχωρίζουν μη-γραμμικά το χώρο των 8×L χαρακτηριστικών, εντοπίζοντας απότομα κατώφλια (π.χ. πτώση SNR + αύξηση Speed)."),
            ("2. Ενσωματωμένη Ομαλοποίηση (L1/L2 Regularization):",
             "Ελαχιστοποιεί την αντικειμενική συνάρτηση L = Σ l(y_i, ŷ_i) + Σ Ω(f_k), όπου Ω(f) = γT + ½λ||w||², αποτρέποντας την υπερπροσαρμογή (overfitting) σε θορυβώδεις μετρήσεις."),
            ("3. Υπερ-Ταχύς Χρόνος Συμπερασμού (Sub-millisecond Inference):",
             "Ιδανικό για εκτέλεση σε πραγματικό χρόνο στον σταθμό βάσης (gNB / O-RAN Near-RT RIC) με καθυστέρηση < 0,0015 ms ανά δείγμα!")
        ]
    )

    # Hyperparameters Table on bottom left
    headers_hp = ["Υπερπαράμετρος XGBoost", "Τιμή", "Ρόλος στη Μάθηση Χρονοσειρών 5G"]
    rows_hp = [
        ["n_estimators", "150", "Πλήθος διαδοχικών δέντρων ενίσχυσης (boosting rounds)"],
        ["max_depth", "6", "Μέγιστο βάθος δέντρου (συλλαμβάνει αλληλεπιδράσεις έως 6ου βαθμού)"],
        ["learning_rate (η)", "0.08", "Βήμα συρρίκνωσης (shrinkage) για ομαλή σύγκλιση"],
        ["subsample", "0.85", "Τυχαία δειγματοληψία 85% των παραθύρων ανά δέντρο"],
        ["colsample_bytree", "0.85", "Δειγματοληψία 85% των 8×L χαρακτηριστικών ανά δέντρο"],
    ]
    add_styled_table(
        s12, left=0.5, top=4.60, width=5.95, height=2.28,
        headers=headers_hp, rows=rows_hp,
        col_widths=[1.85, 0.85, 3.25],
        font_size=9.0, header_font_size=9.5,
        bold_cols={0, 1}
    )

    # Right Side: 4 Metrics Cards
    metrics_cards = [
        ("RMSE — Root Mean Squared Error (kbps)",
         "RMSE = √[ (1/N) · Σ (y_i - ŷ_i)² ]",
         "Τιμωρεί αυστηρά τα μεγάλα σφάλματα πρόβλεψης (τετραγωνικός όρος). Κρίσιμο σε δίκτυα 5G γιατί οι μεγάλες αποκλίσεις σε αιχμές ή βυθίσεις οδηγούν σε εσφαλμένα handovers.",
         COLOR_NAVY),
        ("MAE — Mean Absolute Error (kbps)",
         "MAE = (1/N) · Σ |y_i - ŷ_i|",
         "Μετρά τη μέση απόλυτη απόκλιση σε kbps με ίση βαρύτητα σε όλα τα δείγματα. Είναι ανθεκτικότερη (robust) απέναντι σε ακραίες στιγμιαίες τιμές (outliers) του καναλιού.",
         COLOR_BLUE),
        ("MAPE — Mean Absolute Percentage Error (%)",
         "MAPE = (100% / N) · Σ ( |y_i - ŷ_i| / max(y_i, ε) )",
         "Αποτυπώνει το σχετικό ποσοστιαίο σφάλμα. Επειδή σε περιόδους αδράνειας το y_i προσεγγίζει το 0 kbps, χρησιμοποιούμε κατώφλι ασφαλείας ε = 1.0 kbps.",
         COLOR_ORANGE),
        ("R² — Συντελεστής Προσδιορισμού (Coefficient of Determination)",
         "R² = 1 - [ Σ(y_i - ŷ_i)² / Σ(y_i - ȳ)² ]",
         "Εκφράζει το ποσοστό της συνολικής διακύμανσης του DL_bitrate που εξηγείται από το μοντέλο (R² = 0,825 για L=10, H=1s).",
         COLOR_TEAL),
    ]

    for idx, (m_title, m_eq, m_desc, m_col) in enumerate(metrics_cards):
        top_pos = 1.32 + idx * 1.41
        add_card(
            s12, left=6.65, top=top_pos, width=6.18, height=1.32,
            title=f"{m_title}   |   {m_eq}",
            header_bg=m_col, border_color=m_col,
            font_size=9.1, title_size=10.0,
            bullets=[m_desc]
        )

    set_slide_notes(
        s12,
        "Στη διαφάνεια 12 παρουσιάζουμε την αρχιτεκτονική του XGBoost Regressor και τις 4 μετρικές αξιολόγησης που χρησιμοποιήσαμε. "
        "Το XGBoost επιλέχθηκε διότι διαχειρίζεται εξαιρετικά τα 8 επί L χαρακτηριστικά υστέρησης, διαθέτει ενσωματωμένη L1/L2 ομαλοποίηση "
        "και επιτυγχάνει χρόνο πρόβλεψης κάτω από 1 μικροδευτερόλεπτο ανά δείγμα. Χρησιμοποιήσαμε 150 δέντρα, μέγιστο βάθος 6 και learning rate 0.08. "
        "Στα δεξιά παρουσιάζουμε τους μαθηματικούς τύπους και τη φυσική σημασία των μετρικών RMSE (που τιμωρεί τα μεγάλα σφάλματα), "
        "MAE (μέσο απόλυτο σφάλμα σε kbps), MAPE (σχετικό ποσοστιαίο σφάλμα) και R² (ποσοστό εξηγούμενης διακύμανσης)."
    )

    # =========================================================================
    # SLIDE 13: Ζητούμενο 3 (15%) — Πλήρης Πίνακας Πειραματικών Αποτελεσμάτων (Lookback L vs Horizon H)
    # =========================================================================
    s13 = create_content_slide(
        prs, 13,
        "Ζητούμενο 3 (15%) — Πλήρης Πίνακας Αποτελεσμάτων Grid Search (16 Συνδυασμοί L × H)",
        "ΖΗΤΟΥΜΕΝΟ 3: ΠΕΙΡΑΜΑΤΙΚΗ ΑΞΙΟΛΟΓΗΣΗ LOOKBACK L ∈ {5, 10, 20, 30}s & HORIZON H ∈ {1, 3, 5, 10}s"
    )

    headers_s13 = ["Lookback L", "Horizon H", "Είσοδοι (8×L)", "RMSE (kbps)", "MAE (kbps)", "MAPE (%)", "R² Score", "Train (s)", "Infer (ms)"]
    rows_s13 = []
    if grid_data:
        for item in grid_data:
            rows_s13.append([
                f"L = {item['lookback']}s",
                f"H = {item['horizon']}s",
                f"{item['num_features_in']} feats",
                f"{item['rmse']:,.2f}",
                f"{item['mae']:,.2f}",
                f"{item['mape']:,.1f}%",
                f"{item['r2']:.4f}",
                f"{item['train_time_sec']:.2f}s",
                f"{item['infer_time_ms_per_sample']:.4f}"
            ])
    else:
        rows_s13 = [
            ["L = 5s", "H = 1s", "40 feats", "6,443.14", "3,298.32", "6,839.1%", "0.8191", "0.59s", "0.0006"],
            ["L = 10s", "H = 1s", "80 feats", "6,344.75", "3,275.46", "5,869.6%", "0.8247", "1.30s", "0.0006"],
        ]

    # Highlight the L=10 rows (indices 4, 5, 6, 7) and best R2 row
    highlight_s13 = {
        4: RGBColor(0xD4, 0xEF, 0xDF),  # L=10, H=1 (Primary Baseline)
        8: RGBColor(0xEB, 0xF5, 0xFB),  # L=20, H=1
    }
    add_styled_table(
        s13, left=0.5, top=1.28, width=8.65, height=5.62,
        headers=headers_s13, rows=rows_s13,
        col_widths=[1.00, 0.95, 1.05, 1.15, 1.10, 1.05, 0.85, 0.75, 0.75],
        font_size=8.3, header_font_size=8.8,
        highlight_rows=highlight_s13, bold_cols={0, 1, 3, 6}
    )

    # Right Side Analysis & Reference Benchmark Card
    add_card(
        s13, left=9.30, top=1.28, width=3.53, height=2.95,
        title="Επίδοση Βέλτιστου Παραθύρου (L = 10s)",
        header_bg=COLOR_NAVY, border_color=COLOR_NAVY, font_size=9.2, title_size=10.8,
        bullets=[
            ("▪ Κανονικοποιημένο Προφίλ Αναφοράς (L=10s):",
             "\n• H = 1s: RMSE = 857,6 kbps | MAE = 507,6 kbps"
             "\n• H = 3s: RMSE = 1.044,4 kbps | MAE = 626,8 kbps"
             "\n• H = 5s: RMSE = 1.106,4 kbps | MAE = 674,8 kbps"
             "\n• H = 10s: RMSE = 1.179,9 kbps | MAE = 747,8 kbps"),
            ("▪ Πλήρης Κλίμακα (Raw Dataset 0–173 Mbps):",
             "\n• H = 1s: RMSE = 6.344,75 kbps | R² = 0,8247"
             "\n• H = 3s: RMSE = 7.503,15 kbps | R² = 0,7548"
             "\n• H = 5s: RMSE = 7.961,68 kbps | R² = 0,7241"
             "\n• H = 10s: RMSE = 9.112,46 kbps | R² = 0,6391")
        ]
    )

    add_card(
        s13, left=9.30, top=4.35, width=3.53, height=2.55,
        title="Βασικά Πειραματικά Συμπεράσματα",
        header_bg=COLOR_TEAL, border_color=COLOR_TEAL, font_size=9.2, title_size=10.8,
        bullets=[
            ("1. Σημείο Ισορροπίας L = 10s (80 χαρακτηριστικά):",
             "Μειώνει το RMSE κατά ~100 kbps σε σχέση με το L=5s, με χρόνο εκπαίδευσης μόλις 1,30s."),
            ("2. Φθίνουσα Απόδοση για L = 20s & 30s:",
             "Ο τριπλασιασμός των χαρακτηριστικών (240 είσοδοι για L=30) αυξάνει τον χρόνο εκπαίδευσης κατά 160% με < 0,1% κέρδος σε R²."),
            ("3. Εξαιρετική Ταχύτητα Συμπερασμού:",
             "0,0006 ms/δείγμα (> 1,6 εκατ. προβλέψεις/sec)!")
        ]
    )

    set_slide_notes(
        s13,
        "Στη διαφάνεια 13 παρουσιάζουμε τον πλήρη πίνακα των 16 πειραματικών συνδυασμών του Ζητουμένου 3, για Lookback L = 5, 10, 20, 30 δευτερόλεπτα "
        "και Prediction Horizon H = 1, 3, 5, 10 δευτερόλεπτα. Παρατηρούμε ότι το παράθυρο L = 10s (80 χαρακτηριστικά εισόδου) αποτελεί το βέλτιστο "
        "σημείο λειτουργίας (sweet spot): επιτυγχάνει R² = 0,8247 στον ορίζοντα H=1s (RMSE = 857,6 kbps / MAE = 507,6 kbps στο τυπικό κανονικοποιημένο "
        "προφίλ αναφοράς και RMSE = 6.344,75 kbps / MAE = 3.275,46 kbps στην πλήρη κλίμακα 0–173 Mbps). "
        "Αυξάνοντας το L σε 20 ή 30 δευτερόλεπτα, ο αριθμός των χαρακτηριστικών ανεβαίνει στα 160 και 240, διπλασιάζοντας τον χρόνο εκπαίδευσης χωρίς ουσιαστική βελτίωση ακρίβειας."
    )

    # =========================================================================
    # SLIDE 14: Ζητούμενο 3 (15%) — Ανάλυση Ευαισθησίας Παραμέτρων & Παρακολούθηση Τροχιάς
    # =========================================================================
    s14 = create_content_slide(
        prs, 14,
        "Ζητούμενο 3 (15%) — Ανάλυση Ευαισθησίας (L vs H) & Παρακολούθηση Τροχιάς",
        "ΖΗΤΟΥΜΕΝΟ 3: ΚΑΜΠΥΛΕΣ ΣΦΑΛΜΑΤΟΣ ΑΝΑ ΟΡΙΖΟΝΤΑ & ΠΑΡΑΚΟΛΟΥΘΗΣΗ ΠΡΑΓΜΑΤΙΚΟΥ THROUGHPUT"
    )

    fig3 = FIGURES_DIR / "03_xgboost_horizons_lookback.png"
    add_picture_fit(
        s14, fig3, left=0.5, top=1.32, max_w=7.85, max_h=5.55,
        caption="Σχήμα 7: Ευαισθησία RMSE, MAE, MAPE ως προς τον ορίζοντα H και παρακολούθηση πραγματικής τροχιάς (Actual vs Predicted)"
    )

    add_card(
        s14, left=8.50, top=1.32, width=4.33, height=2.85,
        title="Γιατί Αυξάνεται το Σφάλμα με τον Ορίζοντα H;",
        header_bg=COLOR_NAVY, border_color=COLOR_NAVY, font_size=9.4,
        bullets=[
            ("• Μονοτονική Αύξηση Σφάλματος (H: 1s → 10s):",
             "Καθώς ο ορίζοντας H αυξάνεται από 1s σε 10s, το RMSE αυξάνεται από 857,6 σε 1.179,9 kbps (+37,6%) [ή από 6.344,8 σε 9.112,5 kbps σε πλήρη κλίμακα]."),
            ("• Φυσική Εξήγηση (Channel Coherence Time):",
             "Σε 10 δευτερόλεπτα ένα όχημα με ταχύτητα 72 km/h διανύει 200 μέτρα! Στο διάστημα αυτό συμβαίνουν νέα φαινόμενα σκίασης (shadowing) και handovers που δεν υπήρχαν στο ιστορικό [t-L+1..t]."),
            ("• Συμπέρασμα για το Lookback L:",
             "Η μνήμη του ασύρματου καναλιού εξαντλείται στα 10 δευτερόλεπτα· παλαιότερες μετρήσεις (20–30s πριν) προσθέτουν μόνο θόρυβο.")
        ]
    )

    add_card(
        s14, left=8.50, top=4.30, width=4.33, height=2.57,
        title="Αξιολόγηση Παρακολούθησης Τροχιάς (Κάτω Δεξιά)",
        header_bg=COLOR_BLUE, border_color=COLOR_BLUE, font_size=9.4,
        bullets=[
            ("• Ακριβής Σύλληψη Αιχμών & Βυθίσεων:",
             "Η κόκκινη διακεκομμένη καμπύλη (XGBoost Predicted) ακολουθεί πιστά την μπλε καμπύλη (Actual Throughput) τόσο στις εξάρσεις (15–24 Mbps) όσο και στις απότομες πτώσεις (< 2 Mbps)."),
            ("• Μηδενική Υστέρηση Φάσης σε H = 1s – 3s:",
             "Επιτρέπει στον 5G MAC Scheduler να γνωρίζει εκ των προτέρων πότε η ζεύξη πρόκειται να καταρρεύσει.")
        ]
    )

    set_slide_notes(
        s14,
        "Στη διαφάνεια 14 αναλύουμε τα τέσσερα επιμέρους γραφήματα ευαισθησίας του XGBoost. "
        "Στα τρία πρώτα διαγράμματα (RMSE, MAE και MAPE ως προς το Prediction Horizon H), βλέπουμε καθαρά ότι όλες οι καμπύλες Lookback L=10, 20 και 30 "
        "συμπίπτουν σχεδόν απόλυτα, αποδεικνύοντας ότι 10 δευτερόλεπτα ιστορικού επαρκούν πλήρως. Αντίθετα, όταν αυξάνεται ο ορίζοντας H από 1 σε 10 δευτερόλεπτα, "
        "το σφάλμα αυξάνεται μονοτονικά, διότι το όχημα μετακινείται σε νέο ραδιοπεριβάλλον. "
        "Στο κάτω δεξιά διάγραμμα βλέπουμε την παρακολούθηση τροχιάς (Trajectory Tracking) σε ένα τμήμα 200 δευτερολέπτων του Test set, όπου το XGBoost "
        "προβλέπει με εξαιρετική ακρίβεια τόσο τις κορυφές όσο και τις βυθίσεις του throughput."
    )

    # =========================================================================
    # SLIDE 15: Ζητούμενο 4 (10%) — Ερμηνευσιμότητα Μοντέλου με Explainable AI (TreeSHAP)
    # =========================================================================
    s15 = create_content_slide(
        prs, 15,
        "Ζητούμενο 4 (10%) — Ερμηνευσιμότητα Μοντέλου με Explainable AI (TreeSHAP)",
        "ΖΗΤΟΥΜΕΝΟ 4: ΘΕΩΡΙΑ ΠΑΙΓΝΙΩΝ SHAPLEY & ΚΑΤΑΤΑΞΗ ΣΠΟΥΔΑΙΟΤΗΤΑΣ ΜΕΤΡΙΚΩΝ 5G"
    )

    fig5 = FIGURES_DIR / "05_shap_feature_importance.png"
    add_picture_fit(
        s15, fig5, left=0.5, top=1.32, max_w=5.95, max_h=3.95,
        caption="Σχήμα 8: Αθροιστική Σπουδαιότητα Μεταβλητών (Cumulative Mean |SHAP| ανά Radio KPI)"
    )

    add_card(
        s15, left=0.5, top=5.38, width=5.95, height=1.52,
        title="Μαθηματική Βάση TreeSHAP (Θεωρία Παιγνίων)",
        header_bg=COLOR_NAVY, border_color=COLOR_NAVY, font_size=9.2, title_size=10.5,
        bullets=[
            ("• Προσθετική Απόδοση Χαρακτηριστικών:",
             "f(x) = E[f(x)] + Σ_{i=1}^{80} φ_i, όπου φ_i η τιμή Shapley (σε kbps) του χαρακτηριστικού i."),
            ("• Γιατί TreeSHAP;",
             "Υπολογίζει τις ακριβείς τιμές Shapley σε πολυωνυμικό χρόνο O(TLD²) πάνω στα δέντρα του XGBoost (L=10, H=1).")
        ]
    )

    # Right Side Table of all 8 KPIs ranked by SHAP
    headers_s15 = ["Κατάταξη", "Μετρική (KPI)", "Mean |SHAP| (Norm / Raw)", "Τηλεπικοινωνιακή Ερμηνεία Επίδρασης στο 5G DL_bitrate"]
    rows_s15 = [
        ["#1", "UL_bitrate", "615,9 / 9.259,0 kbps", "Κυρίαρχος δείκτης! Αποτυπώνει την ενεργή κίνηση της συνεδρίας και τη ροή πακέτων επιβεβαίωσης TCP ACK."],
        ["#2", "RSSI", "115,6 / 1.102,9 kbps", "Συνολική λαμβανόμενη ενέργεια στο εύρος ζώνης· αντανακλά άμεσα τη διαθέσιμη ισχύ φέροντος."],
        ["#3", "ServingCell_Distance", "104,5 / 764,4 kbps", "Καθορίζει το Large-Scale Path Loss· μεγάλη απόσταση σημαίνει όρια κυψέλης (Cell Edge)."],
        ["#4", "Speed", "99,4 / 754,8 kbps", "Η υψηλή ταχύτητα προκαλεί Doppler shift, γρήγορο fading και συχνές διακοπές λόγω Handover."],
        ["#5", "SNR", "88,3 / 739,2 kbps", "Καθαρότητα σήματος προς θόρυβο· καθορίζει την ανώτατη χωρητικότητα κατά τον νόμο Shannon."],
        ["#6", "RSRP", "79,6 / 385,3 kbps", "Ισχύς σημάτων αναφοράς της εξυπηρετούσας κυψέλης· βασικό κριτήριο ενεργοποίησης A3 Handover."],
        ["#7", "RSRQ", "49,0 / 565,7 kbps", "Ποιότητα λήψης υπό παρεμβολές γειτονικών σταθμών βάσης (Inter-Cell Interference)."],
        ["#8", "CQI", "41,3 / 490,0 kbps", "Κβαντισμένος δείκτης 1–15 (η πληροφορία του υπερκαλύπτεται εν μέρει από το συνεχές SNR)."],
    ]
    add_styled_table(
        s15, left=6.60, top=1.32, width=6.23, height=5.58,
        headers=headers_s15, rows=rows_s15,
        col_widths=[0.72, 1.38, 1.48, 2.65],
        font_size=8.6, header_font_size=9.2,
        highlight_rows={0: RGBColor(0xE8, 0xF8, 0xF5), 1: RGBColor(0xEB, 0xF5, 0xFB)},
        bold_cols={0, 1, 2}
    )

    set_slide_notes(
        s15,
        "Προχωράμε στο Ζητούμενο 4 (10%), το οποίο αφορά την Ερμηνευσιμότητα του Μοντέλου (Explainable AI) με τη μέθοδο TreeSHAP. "
        "Ένα βασικό μειονέκτημα των σύνθετων μοντέλων Ensemble είναι ότι λειτουργούν ως 'μαύρο κουτί' (black box). Με το TreeSHAP υπολογίζουμε "
        "τις τιμές Shapley (φ_i) από τη Θεωρία Παιγνίων, οι οποίες μετρούν σε kbps τη συνεισφορά κάθε χαρακτηριστικού στην τελική πρόβλεψη. "
        "Αθροίζοντας τα|SHAP| across των 10 χρονικών υστερήσεων για κάθε μία από τις 8 μετρικές, προκύπτει η κατάταξη του πίνακα: "
        "1η μετρική είναι το UL_bitrate (615,9 kbps στο κανονικοποιημένο προφίλ / 9.259 kbps σε πλήρη κλίμακα), 2η το RSSI (115,6 kbps), "
        "3η η απόσταση ServingCell_Distance (104,5 kbps), 4η η ταχύτητα Speed (99,4 kbps), και ακολουθούν τα SNR (88,3), RSRP (79,6), RSRQ (49,0) και CQI (41,3)."
    )

    # =========================================================================
    # SLIDE 16: Ζητούμενο 4 (10%) — Ανάλυση Χρονικών Υστερήσεων (Beeswarm) & Μη-Γραμμικών Εξαρτήσεων
    # =========================================================================
    s16 = create_content_slide(
        prs, 16,
        "Ζητούμενο 4 (10%) — Ανάλυση Υστερήσεων (Beeswarm) & Μη-Γραμμικών Εξαρτήσεων",
        "ΖΗΤΟΥΜΕΝΟ 4: ΧΡΟΝΙΚΗ ΒΑΡΥΤΗΤΑ LAGS (t, t-1) & ΑΛΛΗΛΕΠΙΔΡΑΣΕΙΣ ΚΑΝΑΛΙΟΥ"
    )

    fig4 = FIGURES_DIR / "04_shap_summary_beeswarm.png"
    fig6 = FIGURES_DIR / "06_shap_dependence_plots.png"

    add_picture_fit(
        s16, fig4, left=0.5, top=1.30, max_w=6.05, max_h=3.85,
        caption="Σχήμα 9: SHAP Summary Beeswarm Plot των 15 σημαντικότερων χρονικών υστερήσεων (Lagged Features)"
    )
    add_picture_fit(
        s16, fig6, left=6.75, top=1.30, max_w=6.08, max_h=3.85,
        caption="Σχήμα 10: SHAP Dependence Plots (Μη-γραμμική εξάρτηση και αλληλεπίδραση χαρακτηριστικών)"
    )

    add_card(
        s16, left=0.5, top=5.25, width=6.05, height=1.68,
        title="Ερμηνεία Beeswarm Plot (Αριστερά)",
        header_bg=COLOR_NAVY, border_color=COLOR_NAVY, font_size=9.2, title_size=10.5,
        bullets=[
            ("• Κυριαρχία των Πιο Πρόσφατων Στιγμών (t και t-1):",
             "Τα χαρακτηριστικά UL_bitrate_t, UL_bitrate_t-1, RSSI_t, SNR_t και CQI_t καταλαμβάνουν τις πρώτες θέσεις."),
            ("• Κατεύθυνση Επίδρασης (Χρώμα Κόκκινο vs Μπλε):",
             "Υψηλές τιμές (κόκκινες κουκκίδες) των UL_bitrate_t, RSSI_t, SNR_t και CQI_t ωθούν την πρόβλεψη έντονα προς τα δεξιά (+SHAP kbps), ενώ υψηλές τιμές του ServingCell_Distance_t μειώνουν το προβλεπόμενο throughput.")
        ]
    )

    add_card(
        s16, left=6.75, top=5.25, width=6.08, height=1.68,
        title="Ερμηνεία Dependence Plots (Δεξιά)",
        header_bg=COLOR_TEAL, border_color=COLOR_TEAL, font_size=9.2, title_size=10.5,
        bullets=[
            ("• Μη-Γραμμική Καμπύλη Κόρου & Κατωφλίου:",
             "Όταν η κίνηση ή η ποιότητα καναλιού είναι κάτω από τον μέσο όρο (αρνητικό Z-score), η επίδραση SHAP είναι σταθερά αρνητική. Μόλις ξεπεραστεί το κατώφλι ενεργής μετάδοσης, η συνεισφορά αυξάνεται απότομα."),
            ("• Διαχρονική Συνέργεια (t με t-1):",
             "Ο χρωματισμός αλληλεπίδρασης δείχνει ότι υψηλό σήμα/ρυθμός τόσο στη στιγμή t όσο και στη στιγμή t-1 πολλαπλασιάζει τη θετική επίδραση.")
        ]
    )

    set_slide_notes(
        s16,
        "Στη διαφάνεια 16 εμβαθύνουμε στα δύο βασικά διαγράμματα του SHAP: το Beeswarm Plot (αριστερά) και τα Dependence Plots (δεξιά). "
        "Στο Beeswarm Plot βλέπουμε μεμονωμένα τις χρονικές υστερήσεις (lags): οι πιο πρόσφατες μετρήσεις στις στιγμές t και t-1 (UL_bitrate_t, "
        "UL_bitrate_t-1, RSSI_t, SNR_t, CQI_t) έχουν τη μεγαλύτερη βαρύτητα, επιβεβαιώνοντας την ισχυρή αυτοσυσχέτιση πρώτης τάξης του καναλιού. "
        "Οι κόκκινες κουκκίδες (υψηλές τιμές) στα SNR_t, RSSI_t και CQI_t δίνουν θετικό SHAP (αυξάνουν το DL_bitrate), ενώ οι κόκκινες κουκκίδες "
        "στο ServingCell_Distance_t δίνουν αρνητικό SHAP (καθώς ο χρήστης απομακρύνεται από την κεραία, ο ρυθμός πέφτει)."
    )

    # =========================================================================
    # SLIDE 17: Ζητούμενο 4 (10%) — Τοπική Ερμηνεία Αποφάσεων (Local Waterfall: Υψηλό vs Χαμηλό Bitrate)
    # =========================================================================
    s17 = create_content_slide(
        prs, 17,
        "Ζητούμενο 4 (10%) — Τοπική Ερμηνεία Αποφάσεων (Local SHAP Waterfall Plots)",
        "ΖΗΤΟΥΜΕΝΟ 4: ΔΙΑΓΝΩΣΗ ΜΕΜΟΝΩΜΕΝΩΝ ΣΥΜΒΑΝΤΩΝ (ΥΨΗΛΟ THROUGHPUT VS ΚΑΤΑΡΡΕΥΣΗ QoS)"
    )

    fig7 = FIGURES_DIR / "07_shap_waterfall_local.png"
    add_picture_fit(
        s17, fig7, left=0.5, top=1.30, max_w=12.33, max_h=3.85,
        caption="Σχήμα 11: SHAP Waterfall Plots για δύο ακραία δείγματα του Test Set: Συμβάν Υψηλού Ρυθμού (αριστερά) vs Συμβάν Υποβάθμισης Καναλιού (δεξιά)"
    )

    add_card(
        s17, left=0.5, top=5.25, width=6.05, height=1.68,
        title="Αριστερό Waterfall: Συμβάν Αιχμής (High Throughput)",
        header_bg=COLOR_TEAL, border_color=COLOR_TEAL, font_size=9.3, title_size=10.5,
        bullets=[
            ("• Από τη Βασική Τιμή E[f(x)] στην Τελική Πρόβλεψη f(x):",
             "Ξεκινώντας από τη μέση πρόβλεψη του μοντέλου E[f(x)], οι ισχυρές θετικές τιμές των UL_bitrate_t, UL_bitrate_t-1, RSSI_t και SNR_t προσθέτουν δεκάδες χιλιάδες kbps (κόκκινα βέλη προς τα δεξιά)."),
            ("• Φυσική Ερμηνεία:",
             "Χρήστης κοντά στον σταθμό βάσης με άριστο SNR και ενεργή αμφίδρομη ροή δεδομένων.")
        ]
    )

    add_card(
        s17, left=6.75, top=5.25, width=6.08, height=1.68,
        title="Δεξί Waterfall: Συμβάν Υποβάθμισης (Low Throughput / Outage)",
        header_bg=COLOR_RED, border_color=COLOR_RED, font_size=9.3, title_size=10.5,
        bullets=[
            ("• Κατάρρευση Ρυθμού (Μπλε Βέλη Αρνητικής Συνεισφοράς):",
             "Οι χαμηλές τιμές στα UL_bitrate_t, RSSI_t, CQI_t και SNR_t αφαιρούν συνολικά > 10.000 kbps από τη μέση τιμή E[f(x)], οδηγώντας την πρόβλεψη κοντά στο 0 kbps."),
            ("• Χρησιμότητα για τον Μηχανικό Δικτύου 5G (Automated Root-Cause Analysis):",
             "Το O-RAN RIC γνωρίζει όχι μόνο ότι θα πέσει ο ρυθμός, αλλά και το ΑΚΡΙΒΕΣ ΑΙΤΙΟ (π.χ. πτώση RSSI/SNR λόγω σκίασης vs αδράνεια κίνησης)!")
        ]
    )

    set_slide_notes(
        s17,
        "Στη διαφάνεια 17 παρουσιάζουμε την τοπική ερμηνευσιμότητα (Local Explainability) μέσω των διαγραμμάτων SHAP Waterfall. "
        "Ενώ τα προηγούμενα γραφήματα έδειχναν τη συνολική συμπεριφορά του μοντέλου σε όλο το Test set, το Waterfall plot εξηγεί μία μεμονωμένη απόφαση! "
        "Αριστερά βλέπουμε ένα συμβάν υψηλού ρυθμού μετάδοσης, όπου τα κόκκινα βέλη δείχνουν πώς το υψηλό UL_bitrate και το ισχυρό RSSI εκτοξεύουν την πρόβλεψη. "
        "Δεξιά βλέπουμε ένα συμβάν κατάρρευσης (Low Throughput Event), όπου τα μπλε βέλη ωθούν την πρόβλεψη προς το μηδέν. "
        "Αυτό δίνει στον ελεγκτή του δικτύου 5G τη δυνατότητα αυτόματης διάγνωσης αιτίου (Root-Cause Analysis) σε πραγματικό χρόνο."
    )

    # =========================================================================
    # SLIDE 18: Σύνοψη Ενδιάμεσης Φάσης (50%), Live Demo & Επόμενα Βήματα (Τελική Φάση)
    # =========================================================================
    s18 = create_content_slide(
        prs, 18,
        "Σύνοψη Ενδιάμεσης Φάσης (50%), Live Demo & Οδικός Χάρτης Τελικής Φάσης",
        "ΣΥΜΠΕΡΑΣΜΑΤΑ ΦΑΣΗΣ Α (40%–50%) & ΕΠΟΜΕΝΑ ΒΗΜΑΤΑ (ΖΗΤΟΥΜΕΝΑ 5 – 8)"
    )

    add_card(
        s18, left=0.5, top=1.30, width=6.05, height=3.10,
        title="✔ Τι Ολοκληρώθηκε στην Ενδιάμεση Φάση (Πρώτο 50%)",
        header_bg=COLOR_TEAL, border_color=COLOR_TEAL, font_size=9.5, title_size=11.0,
        bullets=[
            ("✔ Ζητούμενο 1 (10% — Τηλεπικοινωνιακή Ανάλυση 5G):",
             "Τεκμηρίωση στοχαστικότητας 5G NR και σχεδίαση των 4 μηχανισμών Proactive Resource Management (CHO, MCS, PRB, ABR)."),
            ("✔ Ζητούμενο 2 (15% — Προεπεξεργασία & EDA):",
             "Ενοποίηση 135 traces (174.523 δείγματα), καθαρισμός '-' με session-aware ffill/bfill, Stratified Trace Split (106/29 traces) χωρίς Data Leakage & StandardScaler."),
            ("✔ Ζητούμενο 3 (15% — XGBoost Lookback & Horizon Grid):",
             "Πλήρης αξιολόγηση 16 συνδυασμών L ∈ {5,10,20,30}s × H ∈ {1,3,5,10}s. Βέλτιστο L=10s (R²=0,825, RMSE=857,6 kbps norm / 6.344,8 kbps raw, Infer=0,0006 ms)."),
            ("✔ Ζητούμενο 4 (10% — Explainable AI με TreeSHAP):",
             "Κατάταξη των 8 KPIs, ανάλυση χρονικών υστερήσεων (Beeswarm), μη-γραμμικών εξαρτήσεων (Dependence) και τοπικών αποφάσεων (Waterfall).")
        ]
    )

    add_card(
        s18, left=6.75, top=1.30, width=6.08, height=3.10,
        title="⏳ Οδικός Χάρτης Τελικής Παρουσίασης (Υπόλοιπο 50%)",
        header_bg=COLOR_BLUE, border_color=COLOR_BLUE, font_size=9.5, title_size=11.0,
        bullets=[
            ("⏳ Ζητούμενο 5 (15% — Deep Learning με PyTorch LSTM):",
             "Υλοποίηση νευρωνικού δικτύου LSTM 2 επιπέδων με παράθυρο L = 64 δειγμάτων και άμεση σύγκριση ακρίβειας και κόστους με το XGBoost."),
            ("⏳ Ζητούμενο 6 (10% Bonus — Time-Series Foundation Model):",
             "Αξιολόγηση του προ-εκπαιδευμένου μοντέλου IBM Granite Tiny Time Mixer (TTM) σε σενάρια Zero-Shot και Fine-Tuning."),
            ("⏳ Ζητούμενο 7 (10% — Σταδιακή Αφαίρεση Μεταβλητών / Pruning):",
             "Αφαίρεση των λιγότερο σημαντικών KPIs (βάσει SHAP) και μέτρηση του trade-off μεταξύ ακρίβειας (RMSE) και χρόνου εκπαίδευσης/πρόβλεψης."),
            ("⏳ Ζητούμενο 8 (15% — 5G Proactive Network Management):",
             "Προληπτική ανίχνευση πτώσης ρυθμού κάτω από το όριο SLA (< 5 Mbps) και ποσοτικοποίηση του trade-off Ακρίβειας vs Διαθέσιμου Χρόνου Αντίδρασης.")
        ]
    )

    # Bottom Left: Live Demo Execution Card
    add_card(
        s18, left=0.5, top=4.55, width=6.05, height=2.35,
        title="💻 Εκτέλεση Live Demo Ενδιάμεσης Φάσης (1-Click Reproducible)",
        header_bg=COLOR_NAVY, border_color=COLOR_NAVY, font_size=9.6, title_size=11.0,
        bullets=[
            ("• Αυτόματη Εκτέλεση Ενδιάμεσης Φάσης (40%–50%):",
             "   .\\run.bat midterm   ή   python scripts/run_midterm_40pct.py"),
            ("• Τι Εκτελεί Ζωντανά το Script:",
             "1. Φόρτωση, καθαρισμός και χωρισμός των 135 CSV traces (src/data_processing.py).\n"
             "2. Εκπαίδευση & αξιολόγηση των 16 μοντέλων XGBoost (src/models_ml.py).\n"
             "3. Υπολογισμός τιμών TreeSHAP & εξαγωγή γραφημάτων (src/explainability.py).\n"
             "4. Αυτόματη δημιουργία της παρούσας παρουσίασης PowerPoint!")
        ]
    )

    # Bottom Right: Prominent Team & Q&A Closing Card
    closing_card = s18.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.75), Inches(4.55), Inches(6.08), Inches(2.35)
    )
    closing_card.adjustments[0] = 0.03
    closing_card.fill.solid()
    closing_card.fill.fore_color.rgb = COLOR_NAVY
    closing_card.line.color.rgb = COLOR_GOLD
    closing_card.line.width = Pt(2.2)

    tf_cl = closing_card.text_frame
    tf_cl.word_wrap = True
    tf_cl.margin_left = Inches(0.22)
    tf_cl.margin_top = Inches(0.16)

    p_cl0 = tf_cl.paragraphs[0]
    p_cl0.alignment = PP_ALIGN.CENTER
    p_cl0.text = "ΕΥΧΑΡΙΣΤΟΥΜΕ ΠΟΛΥ ΓΙΑ ΤΗΝ ΠΡΟΣΟΧΗ ΣΑΣ!\nΕρωτήσεις & Συζήτηση (Q&A)"
    p_cl0.font.size = Pt(14)
    p_cl0.font.bold = True
    p_cl0.font.color.rgb = COLOR_GOLD
    p_cl0.space_after = Pt(10)

    p_cl1 = tf_cl.add_paragraph()
    p_cl1.alignment = PP_ALIGN.CENTER
    p_cl1.text = f"👤  {STUDENT_1}"
    p_cl1.font.size = Pt(14)
    p_cl1.font.bold = True
    p_cl1.font.color.rgb = COLOR_WHITE
    p_cl1.space_after = Pt(4)

    p_cl2 = tf_cl.add_paragraph()
    p_cl2.alignment = PP_ALIGN.CENTER
    p_cl2.text = f"👤  {STUDENT_2}"
    p_cl2.font.size = Pt(14)
    p_cl2.font.bold = True
    p_cl2.font.color.rgb = COLOR_WHITE
    p_cl2.space_after = Pt(6)

    p_cl3 = tf_cl.add_paragraph()
    p_cl3.alignment = PP_ALIGN.CENTER
    p_cl3.text = "Τμήμα Μηχανικών Η/Υ & Πληροφορικής — Πανεπιστήμιο Πατρών"
    p_cl3.font.size = Pt(10)
    p_cl3.font.color.rgb = COLOR_LIGHT_BLUE

    set_slide_notes(
        s18,
        "Κλείνοντας την παρουσίασή μας στη διαφάνεια 18, συνοψίζουμε τα 4 πρώτα ζητούμενα που ολοκληρώσαμε (το 50% της εργασίας): "
        "την τηλεπικοινωνιακή ανάλυση του προβλήματος στα 5G δίκτυα, την πλήρη προεπεξεργασία των 135 traces χωρίς data leakage, "
        "το εκτεταμένο Grid Search των 16 μοντέλων XGBoost και την ερμηνευσιμότητα μέσω TreeSHAP. "
        "Για το Live Demo, αρκεί η εντολή .\\run.bat midterm ή python scripts/run_midterm_40pct.py. "
        "Στην τελική φάση θα προχωρήσουμε στα Ζητούμενα 5 έως 8: στο νευρωνικό δίκτυο LSTM (παράθυρο 64 δειγμάτων), στο Foundation Model "
        "IBM Granite Tiny Time Mixer, στο Feature Pruning βάσει SHAP και στη μελέτη του 5G Proactive Network Management. "
        "Σας ευχαριστούμε πολύ — Δημήτριος Τσανακτσής (1100736) και Ιάσωνας Δερβένης (1097437). Είμαστε στη διάθεσή σας για ερωτήσεις!"
    )

    out_path = PRESENTATION_DIR / "Endiamesi_Parousiasi_5G_40_50_Percent.pptx"
    prs.save(str(out_path))
    print(f"Midterm presentation (18 slides) saved to: {out_path}")
    return out_path


if __name__ == "__main__":
    generate_midterm_deck()
