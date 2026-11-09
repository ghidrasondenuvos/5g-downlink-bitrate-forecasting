import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.gridspec as gridspec

# Use DejaVu Sans as primary font so all mathematical symbols (∈, ≥, σ, μ, ŷ) and Greek characters render cleanly
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
os.makedirs(FIG_DIR, exist_ok=True)


def draw_rounded_box(ax, x, y, w, h, facecolor, edgecolor, lw=2.0, radius=0.02, alpha=1.0, zorder=2):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=lw,
        alpha=alpha,
        zorder=zorder
    )
    ax.add_patch(box)
    return box


def draw_arrow(ax, x1, y1, x2, y2, color='#475569', lw=2.5, style='-|>', mutation_scale=18, ls='-', rad=0.0, zorder=3):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        connectionstyle=f"arc3,rad={rad}",
        arrowstyle=style,
        mutation_scale=mutation_scale,
        color=color,
        linewidth=lw,
        linestyle=ls,
        zorder=zorder
    )
    ax.add_patch(arrow)
    return arrow


# ==============================================================================
# FIGURE 13: 5G Reactive vs Proactive AI-Driven Management Architecture
# ==============================================================================
def generate_fig13_reactive_vs_proactive():
    fig = plt.figure(figsize=(16.5, 9.5), facecolor='#F8FAFC')
    gs = gridspec.GridSpec(2, 2, width_ratios=[3.35, 1.3], height_ratios=[1, 1],
                           hspace=0.24, wspace=0.13, left=0.025, right=0.975, top=0.84, bottom=0.06)

    # Title Banner
    fig.text(0.5, 0.945, "5G Resource Management Paradigm Shift: Reactive vs. Proactive AI Forecasting",
             ha='center', va='center', fontsize=18.5, fontweight='bold', color='#0F172A')
    fig.text(0.5, 0.908, "Comparing Traditional Threshold-Triggered Control (Κλασική Διαχείριση) with ML-Driven Lookahead Optimization (Προληπτική Διαχείριση με ML)",
             ha='center', va='center', fontsize=11.0, color='#475569', style='italic')

    # --------------------------------------------------------------------------
    # TOP LEFT PANEL: Reactive 5G Network Management
    # --------------------------------------------------------------------------
    ax_top = fig.add_subplot(gs[0, 0])
    ax_top.set_xlim(0, 1)
    ax_top.set_ylim(0, 1)
    ax_top.axis('off')

    draw_rounded_box(ax_top, 0.01, 0.03, 0.98, 0.94, facecolor='#FFF5F5', edgecolor='#FCA5A5', lw=2.2, radius=0.03, zorder=1)
    draw_rounded_box(ax_top, 0.01, 0.79, 0.98, 0.18, facecolor='#DC2626', edgecolor='#B91C1C', lw=1.5, radius=0.025, zorder=2)
    ax_top.text(0.025, 0.88, "A. REACTIVE 5G MANAGEMENT (Κλασική Διαχείριση)",
                fontsize=12.0, fontweight='bold', color='white', va='center', zorder=3)
    ax_top.text(0.975, 0.88, "Post-Degradation Response | SLA Violations",
                fontsize=10.0, fontweight='bold', color='#FEE2E2', va='center', ha='right', zorder=3)

    reactive_steps = [
        {
            "num": "1",
            "title": "Abrupt Signal Drop\n(Πτώση Σήματος)",
            "body": "• Urban Shadowing / Obstacles\n• High Mobility (Train / Car)\n• UE Enters Cell Edge Zone\n• Rapid RSRP & SINR Plunge",
            "foot": "t = 0 s (Event Onset)",
            "bg": "#FFFFFF", "edge": "#F87171", "badge": "#EF4444"
        },
        {
            "num": "2",
            "title": "Throughput Collapse\n(Κατάρρευση Ρυθμού)",
            "body": "• Link Adaptation Lags Behind\n• Block Error Rate (BLER) Spikes\n• DL_bitrate < 5 Mbps\n• Severe Channel Under-use",
            "foot": "t + 1s to t + 3s",
            "bg": "#FFFFFF", "edge": "#EF4444", "badge": "#DC2626"
        },
        {
            "num": "3",
            "title": "Packet Loss & Stalls\n(Υποβάθμιση QoE)",
            "body": "• RLC/PDCP Buffer Overflow\n• TCP Congestion Window Reset\n• 4K Video Buffering / Freeze\n• VoNR / XR Jitter Spike",
            "foot": "t + 3s to t + 6s",
            "bg": "#FFFFFF", "edge": "#DC2626", "badge": "#B91C1C"
        },
        {
            "num": "4",
            "title": "Delayed Action\n(Καθυστερημένη Δράση)",
            "body": "• Late A3 Handover Trigger\n• Emergency MCS Down-shift\n• Recovery Only After Outage\n• Poor User Experience",
            "foot": "t > 6s (Too Late!)",
            "bg": "#FEF2F2", "edge": "#991B1B", "badge": "#7F1D1D"
        }
    ]

    box_w = 0.215
    box_h = 0.62
    gap = 0.028
    start_x = 0.025
    y_pos = 0.10

    for i, st in enumerate(reactive_steps):
        x = start_x + i * (box_w + gap)
        draw_rounded_box(ax_top, x, y_pos, box_w, box_h, facecolor=st["bg"], edgecolor=st["edge"], lw=2.0, radius=0.025, zorder=3)

        circle = Circle((x + 0.024, y_pos + box_h - 0.08), 0.021, facecolor=st["badge"], edgecolor='white', lw=1.5, zorder=4)
        ax_top.add_patch(circle)
        ax_top.text(x + 0.024, y_pos + box_h - 0.08, st["num"], color='white', fontsize=9.5, fontweight='bold', ha='center', va='center', zorder=5)

        ax_top.text(x + 0.048, y_pos + box_h - 0.08, st["title"], color='#7F1D1D', fontsize=9.0, fontweight='bold', ha='left', va='center', zorder=4)
        ax_top.plot([x + 0.012, x + box_w - 0.012], [y_pos + box_h - 0.16, y_pos + box_h - 0.16], color='#FECACA', lw=1.2, zorder=4)
        ax_top.text(x + 0.012, y_pos + box_h - 0.20, st["body"], color='#334155', fontsize=8.4, ha='left', va='top', linespacing=1.42, zorder=4)

        draw_rounded_box(ax_top, x + 0.015, y_pos + 0.03, box_w - 0.03, 0.09, facecolor='#FEE2E2', edgecolor='#FCA5A5', lw=1.0, radius=0.015, zorder=4)
        ax_top.text(x + box_w / 2, y_pos + 0.075, st["foot"], color='#991B1B', fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=5)

        if i < len(reactive_steps) - 1:
            draw_arrow(ax_top, x + box_w + 0.003, y_pos + box_h / 2, x + box_w + gap - 0.003, y_pos + box_h / 2,
                       color='#DC2626', lw=2.8, mutation_scale=18, zorder=5)

    # --------------------------------------------------------------------------
    # BOTTOM LEFT PANEL: Proactive AI-Driven 5G Management
    # --------------------------------------------------------------------------
    ax_bot = fig.add_subplot(gs[1, 0])
    ax_bot.set_xlim(0, 1)
    ax_bot.set_ylim(0, 1)
    ax_bot.axis('off')

    draw_rounded_box(ax_bot, 0.01, 0.03, 0.98, 0.94, facecolor='#ECFDF5', edgecolor='#6EE7B7', lw=2.2, radius=0.03, zorder=1)
    draw_rounded_box(ax_bot, 0.01, 0.79, 0.98, 0.18, facecolor='#059669', edgecolor='#047857', lw=1.5, radius=0.025, zorder=2)
    ax_bot.text(0.025, 0.88, "B. PROACTIVE AI-DRIVEN 5G MANAGEMENT (Προληπτική Διαχείριση με ML)",
                fontsize=12.0, fontweight='bold', color='white', va='center', zorder=3)
    ax_bot.text(0.975, 0.88, "Anticipatory Control | QoE Preserved",
                fontsize=10.0, fontweight='bold', color='#D1FAE5', va='center', ha='right', zorder=3)

    proactive_steps = [
        {
            "num": "1",
            "title": "Real-Time UE KPIs\nLookback [t-L+1 ... t]",
            "body": "• Radio: RSRP, RSRQ, SNR, CQI, RSSI\n• Mobility: Speed, Cell Distance\n• Traffic: UL_bitrate (1 Hz stream)\n• Sliding Window L ∈ {5, 10, 20}s",
            "foot": "Continuous Telemetry",
            "bg": "#FFFFFF", "edge": "#38BDF8", "badge": "#0284C7", "foot_bg": "#E0F2FE", "foot_fg": "#0369A1"
        },
        {
            "num": "2",
            "title": "XGBoost / AI Engine\nat gNB / O-RAN RIC",
            "body": "• Near-RT RIC xApp Deployment\n• Processes L × 8 = 80 Features\n• Captures Non-Linear Fading\n• Ultra-Fast Inference (< 0.1 ms)",
            "foot": "Edge AI Inference",
            "bg": "#FFFFFF", "edge": "#10B981", "badge": "#059669", "foot_bg": "#D1FAE5", "foot_fg": "#065F46"
        },
        {
            "num": "3",
            "title": "Forecasts DL_bitrate\nat Horizon t + H sec",
            "body": "• Predicts y_hat(t + H) in kbps\n• Multi-Horizon H ∈ {1, 3, 5, 10}s\n• Early Outage Detection Alert\n• R² = 0.629 | MAE = 4,942 kbps",
            "foot": "Lookahead H = 1–10 s",
            "bg": "#FFFFFF", "edge": "#059669", "badge": "#047857", "foot_bg": "#D1FAE5", "foot_fg": "#065F46"
        },
        {
            "num": "4",
            "title": "Proactive Actions\nBEFORE Degradation",
            "body": "• Early Handover Preparation\n• Pre-emptive MCS Down-shift\n• Dynamic Extra PRB Allocation\n• ABR Video Pre-buffering",
            "foot": "Zero Packet Loss!",
            "bg": "#F0FDF4", "edge": "#047857", "badge": "#065F46", "foot_bg": "#A7F3D0", "foot_fg": "#064E3B"
        }
    ]

    for i, st in enumerate(proactive_steps):
        x = start_x + i * (box_w + gap)
        draw_rounded_box(ax_bot, x, y_pos, box_w, box_h, facecolor=st["bg"], edgecolor=st["edge"], lw=2.0, radius=0.025, zorder=3)

        circle = Circle((x + 0.024, y_pos + box_h - 0.08), 0.021, facecolor=st["badge"], edgecolor='white', lw=1.5, zorder=4)
        ax_bot.add_patch(circle)
        ax_bot.text(x + 0.024, y_pos + box_h - 0.08, st["num"], color='white', fontsize=9.5, fontweight='bold', ha='center', va='center', zorder=5)

        ax_bot.text(x + 0.048, y_pos + box_h - 0.08, st["title"], color='#064E3B', fontsize=9.0, fontweight='bold', ha='left', va='center', zorder=4)
        ax_bot.plot([x + 0.012, x + box_w - 0.012], [y_pos + box_h - 0.16, y_pos + box_h - 0.16], color='#A7F3D0', lw=1.2, zorder=4)
        ax_bot.text(x + 0.012, y_pos + box_h - 0.20, st["body"], color='#1E293B', fontsize=8.4, ha='left', va='top', linespacing=1.42, zorder=4)

        draw_rounded_box(ax_bot, x + 0.015, y_pos + 0.03, box_w - 0.03, 0.09, facecolor=st["foot_bg"], edgecolor=st["edge"], lw=1.0, radius=0.015, zorder=4)
        ax_bot.text(x + box_w / 2, y_pos + 0.075, st["foot"], color=st["foot_fg"], fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=5)

        if i < len(proactive_steps) - 1:
            draw_arrow(ax_bot, x + box_w + 0.003, y_pos + box_h / 2, x + box_w + gap - 0.003, y_pos + box_h / 2,
                       color='#059669', lw=2.8, mutation_scale=18, zorder=5)

    # --------------------------------------------------------------------------
    # RIGHT PANEL: Comparative Throughput Response Curve (Reactive vs Proactive)
    # --------------------------------------------------------------------------
    ax_right = fig.add_subplot(gs[:, 1])
    ax_right.set_facecolor('#FFFFFF')
    for spine in ['top', 'right']:
        ax_right.spines[spine].set_visible(False)

    t = np.linspace(0, 20, 200)
    reactive_tp = 18.0 - 15.5 * np.exp(-0.5 * ((t - 11.0) / 2.1) ** 2) + 0.6 * np.sin(t * 1.5)
    proactive_tp = 18.0 - 5.2 * np.exp(-0.5 * ((t - 10.5) / 2.6) ** 2) + 0.5 * np.sin(t * 1.5)

    ax_right.plot(t, proactive_tp, color='#059669', lw=3.0, label='Proactive AI Control\n(Early Handover / PRB Boost)')
    ax_right.plot(t, reactive_tp, color='#DC2626', lw=2.8, ls='--', label='Reactive Control\n(Post-Outage Recovery)')

    ax_right.axhline(5.0, color='#991B1B', lw=1.5, ls=':', zorder=2)
    ax_right.fill_between(t, 0, 5.0, color='#FEE2E2', alpha=0.55, label='SLA Outage Zone (< 5 Mbps)')
    ax_right.fill_between(t, reactive_tp, proactive_tp, where=(proactive_tp > reactive_tp),
                          color='#A7F3D0', alpha=0.45, label='Saved Capacity (AI Gain)')

    ax_right.annotate('AI Forecast Trigger\n(t = 6s, H = 5s ahead)',
                      xy=(6.0, proactive_tp[60]), xytext=(1.0, 21.5),
                      arrowprops=dict(arrowstyle='->', color='#047857', lw=2.0),
                      fontsize=8.8, fontweight='bold', color='#064E3B',
                      bbox=dict(boxstyle='round,pad=0.3', facecolor='#D1FAE5', edgecolor='#059669'))

    ax_right.annotate('Throughput Collapse!\n(2.4 Mbps < SLA)',
                      xy=(11.0, reactive_tp[110]), xytext=(8.8, 1.0),
                      arrowprops=dict(arrowstyle='->', color='#B91C1C', lw=2.0),
                      fontsize=8.8, fontweight='bold', color='#7F1D1D',
                      bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEE2E2', edgecolor='#DC2626'))

    ax_right.set_title("Impact on UE Downlink Throughput\nDuring Shadowing / Handover Event",
                       fontsize=11.5, fontweight='bold', color='#0F172A', pad=10)
    ax_right.set_xlabel("Time (seconds)", fontsize=10.0, fontweight='bold', color='#334155')
    ax_right.set_ylabel("Downlink Throughput (Mbps)", fontsize=10.0, fontweight='bold', color='#334155')
    ax_right.set_ylim(0, 26.5)
    ax_right.set_xlim(0, 20)
    ax_right.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1')
    ax_right.legend(loc='upper right', fontsize=8.4, frameon=True, facecolor='white', edgecolor='#CBD5E1')

    out_path = os.path.join(FIG_DIR, '13_5g_reactive_vs_proactive_arch.png')
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {out_path} ({os.path.getsize(out_path) / 1024:.1f} KB)")


# ==============================================================================
# FIGURE 14: 5-Stage Data Preprocessing Pipeline Diagram
# ==============================================================================
def generate_fig14_preprocessing_pipeline():
    fig = plt.figure(figsize=(16.5, 9.2), facecolor='#F8FAFC')
    ax = fig.add_axes([0.02, 0.03, 0.96, 0.93])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Main Title
    ax.text(0.5, 0.955, "End-to-End Leakage-Free Time-Series Preprocessing Pipeline (Requirement 2)",
            ha='center', va='center', fontsize=18.5, fontweight='bold', color='#0F172A')
    ax.text(0.5, 0.915, "From Raw 1 Hz Drive-Test Cellular Traces to Normalized Sliding-Window Tensors for Multi-Horizon Forecasting",
            ha='center', va='center', fontsize=11.2, color='#475569', style='italic')

    stages = [
        {
            "num": "STAGE 1",
            "title": "Raw UCC 4G/LTE\nDataset Ingestion",
            "subtitle": "5 Mobility Scenarios",
            "color": "#1E40AF", "bg": "#EFF6FF", "border": "#60A5FA",
            "items": [
                "• Modes: bus, car,\n  pedestrian, static, train",
                "• Total: 135 CSV Traces",
                "• 174,523 Rows @ 1 Hz",
                "• Radio, GPS & Traffic\n  KPIs per UE session",
                "• Unique trace_id tagged\n  per driving session"
            ],
            "metric": "135 Traces | 174,523 Rows"
        },
        {
            "num": "STAGE 2",
            "title": "Data Cleaning &\nSession Imputation",
            "subtitle": "Per-Trace Isolation",
            "color": "#0369A1", "bg": "#F0F9FF", "border": "#38BDF8",
            "items": [
                "• Replace missing '-'\n  strings with NaN",
                "• Session-Aware ffill()\n  & bfill() strictly per\n  trace_id (no bleed)",
                "• Domain Sanity Clipping:\n  - CQI ∈ [0, 15]\n  - DL/UL Bitrate ≥ 0\n  - Speed ≥ 0 km/h"
            ],
            "metric": "0% Missing | Physically Valid"
        },
        {
            "num": "STAGE 3",
            "title": "Leakage-Free\nStratified Trace Split",
            "subtitle": "Grouped by trace_id",
            "color": "#047857", "bg": "#ECFDF5", "border": "#34D399",
            "items": [
                "• Entire traces assigned\n  to Train or Test set",
                "• Stratified across all\n  5 mobility modes",
                "• 80% Train Split:\n  106 Traces (131,370 rows)",
                "• 20% Test Split:\n  29 Traces (43,153 rows)",
                "• Zero overlap in time!"
            ],
            "metric": "106 Train / 29 Test Traces"
        },
        {
            "num": "STAGE 4",
            "title": "Z-Score Feature\nNormalization",
            "subtitle": "Train-Only Fitting",
            "color": "#6D28D9", "bg": "#F5F3FF", "border": "#A78BFA",
            "items": [
                "• StandardScaler (μ=0, σ=1)\n  fitted ONLY on Train",
                "• 8 Scaled Input KPIs:\n  RSRP, RSRQ, SNR, CQI,\n  RSSI, Speed, UL_bitrate,\n  ServingCell_Distance",
                "• Target DL_bitrate kept\n  in raw kbps for direct\n  physical interpretation"
            ],
            "metric": "8 KPIs Scaled | Target in kbps"
        },
        {
            "num": "STAGE 5",
            "title": "Sliding Window\nTensor Generation",
            "subtitle": "Supervised Framing",
            "color": "#B45309", "bg": "#FFFBEB", "border": "#FBBF24",
            "items": [
                "• Lookback Window L:\n  [t - L + 1, ..., t]\n  L ∈ {5, 10, 20} sec",
                "• Input Tensor Shape:\n  X_t ∈ R^(L × 8) or R^(8L)",
                "• Forecast Target:\n  y_(t+H) = DL_bitrate(t+H)",
                "• Prediction Horizon:\n  H ∈ {1, 3, 5, 10} sec"
            ],
            "metric": "L × 8 Input → y(t + H)"
        }
    ]

    w = 0.172
    h = 0.64
    gap = 0.024
    start_x = 0.02
    y0 = 0.22

    for i, st in enumerate(stages):
        x = start_x + i * (w + gap)
        draw_rounded_box(ax, x, y0, w, h, facecolor=st["bg"], edgecolor=st["border"], lw=2.2, radius=0.025, zorder=2)

        draw_rounded_box(ax, x, y0 + h - 0.14, w, 0.14, facecolor=st["color"], edgecolor=st["color"], lw=1.0, radius=0.022, zorder=3)
        ax.text(x + w / 2, y0 + h - 0.035, st["num"], color='#E2E8F0', fontsize=9.2, fontweight='bold', ha='center', va='center', zorder=4)
        ax.text(x + w / 2, y0 + h - 0.092, st["title"], color='white', fontsize=10.5, fontweight='bold', ha='center', va='center', zorder=4)

        draw_rounded_box(ax, x + 0.015, y0 + h - 0.20, w - 0.03, 0.045, facecolor='white', edgecolor=st["border"], lw=1.2, radius=0.012, zorder=3)
        ax.text(x + w / 2, y0 + h - 0.177, st["subtitle"], color=st["color"], fontsize=9.0, fontweight='bold', ha='center', va='center', zorder=4)

        body_text = "\n\n".join(st["items"])
        ax.text(x + 0.012, y0 + h - 0.225, body_text, color='#1E293B', fontsize=8.8, ha='left', va='top', linespacing=1.28, zorder=4)

        draw_rounded_box(ax, x + 0.01, y0 + 0.018, w - 0.02, 0.055, facecolor=st["color"], edgecolor='white', lw=1.2, radius=0.015, zorder=4)
        ax.text(x + w / 2, y0 + 0.045, st["metric"], color='white', fontsize=8.5, fontweight='bold', ha='center', va='center', zorder=5)

        if i < len(stages) - 1:
            draw_arrow(ax, x + w + 0.002, y0 + h / 2, x + w + gap - 0.002, y0 + h / 2,
                       color=st["color"], lw=3.0, mutation_scale=20, zorder=5)

    # Bottom Methodological Guarantees Banner (Anti-Leakage Audit)
    draw_rounded_box(ax, 0.02, 0.02, 0.96, 0.16, facecolor='#0F172A', edgecolor='#334155', lw=2.0, radius=0.025, zorder=2)
    ax.text(0.5, 0.152, "METHODOLOGICAL INTEGRITY & DATA LEAKAGE PREVENTION GUARANTEES",
            color='#38BDF8', fontsize=11.2, fontweight='bold', ha='center', va='center', zorder=3)

    guarantees = [
        ("1. Zero Cross-Session Windowing",
         "Sliding windows [t-L+1 ... t+H] are generated strictly\ninside each individual trace_id; no window ever bridges\ntwo separate driving sessions."),
        ("2. Zero Temporal Split Leakage",
         "Splitting at the trace_id level (106 Train vs. 29 Test\ntraces) prevents adjacent 1 Hz samples from appearing\nin both Train and Test sets."),
        ("3. Zero Normalization Leakage",
         "StandardScaler parameters (μ, σ) are computed\nexclusively on the 131,370 training rows and applied\nblindly to the 43,153 test rows.")
    ]

    col_w = 0.302
    for idx, (g_title, g_desc) in enumerate(guarantees):
        gx = 0.032 + idx * 0.318
        draw_rounded_box(ax, gx, 0.032, col_w, 0.095, facecolor='#1E293B', edgecolor='#475569', lw=1.0, radius=0.015, zorder=3)
        ax.text(gx + 0.012, 0.108, g_title, color='#FACC15', fontsize=9.2, fontweight='bold', ha='left', va='center', zorder=4)
        ax.text(gx + 0.012, 0.062, g_desc, color='#E2E8F0', fontsize=8.0, ha='left', va='center', linespacing=1.25, zorder=4)

    out_path = os.path.join(FIG_DIR, '14_preprocessing_pipeline_diagram.png')
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {out_path} ({os.path.getsize(out_path) / 1024:.1f} KB)")


# ==============================================================================
# FIGURE 15: Sliding Window Mechanism on Real Test Data
# ==============================================================================
def generate_fig15_sliding_window():
    test_df = pd.read_csv(os.path.join(DATA_DIR, 'test_data.csv'))

    # Find a dynamic car trace segment with strong variation (high std) for clear visualization
    best_seg = None
    best_score = -1
    for tid, group in test_df.groupby('trace_id'):
        if len(group) >= 45 and ('car' in tid or 'train' in tid):
            vals = group['DL_bitrate'].values
            for start in range(5, min(len(vals) - 35, 120), 5):
                seg = vals[start:start + 32]
                if np.min(seg) > 1200 and np.max(seg) < 38000:
                    # Prefer segments where the window and horizon have nice variation
                    score = np.std(seg[8:28])
                    if score > best_score:
                        best_score = score
                        best_seg = group.iloc[start:start + 32].copy().reset_index(drop=True)

    selected_seg = best_seg if best_seg is not None else test_df.iloc[100:132].copy().reset_index(drop=True)

    fig = plt.figure(figsize=(16.5, 9.4), facecolor='#F8FAFC')
    gs = gridspec.GridSpec(2, 2, height_ratios=[1.18, 1.0], width_ratios=[1.32, 1.0],
                           hspace=0.36, wspace=0.16, left=0.055, right=0.965, top=0.83, bottom=0.07)

    fig.text(0.5, 0.945, "Supervised Time-Series Framing: Sliding Window & Multi-Horizon Forecasting Mechanism",
             ha='center', va='center', fontsize=18.0, fontweight='bold', color='#0F172A')
    fig.text(0.5, 0.908, "Transforming 8 Multivariate 1 Hz Cellular KPIs over Lookback Window L = 10s into Future Throughput Predictions at t + H",
             ha='center', va='center', fontsize=11.0, color='#475569', style='italic')

    # --------------------------------------------------------------------------
    # PANEL A (Top Full Span): Real DL_bitrate Time-Series with Lookback & Horizon
    # --------------------------------------------------------------------------
    ax_ts = fig.add_subplot(gs[0, :])
    ax_ts.set_facecolor('#FFFFFF')

    t_idx = np.arange(len(selected_seg))
    y_kbps = selected_seg['DL_bitrate'].values
    trace_name = selected_seg['trace_id'].iloc[0]

    t_curr = 17
    L = 10
    t_start = t_curr - L + 1  # 8
    H = 5
    t_target = t_curr + H     # 22

    ax_ts.axvspan(t_start, t_curr, color='#DBEAFE', alpha=0.72, zorder=1, label='Lookback Window L = 10s [t-9, ..., t]')
    ax_ts.axvspan(t_curr, t_target, color='#FEF3C7', alpha=0.75, zorder=1, label='Prediction Horizon H = 5s (H ∈ {1, 3, 5, 10}s)')

    ax_ts.axvline(t_start, color='#2563EB', ls='--', lw=1.8, zorder=2)
    ax_ts.axvline(t_curr, color='#1D4ED8', ls='-', lw=2.5, zorder=3)
    ax_ts.axvline(t_target, color='#DC2626', ls='--', lw=2.2, zorder=3)

    ax_ts.plot(t_idx, y_kbps, color='#64748B', lw=2.0, ls='-', alpha=0.65, zorder=2, label=f'Real Test Trace ({trace_name})')

    ax_ts.plot(t_idx[t_start:t_curr + 1], y_kbps[t_start:t_curr + 1], color='#1D4ED8', lw=3.5, marker='o',
               markersize=7, markerfacecolor='#2563EB', markeredgecolor='white', zorder=4, label='Observed Window Samples (Input History)')

    ax_ts.scatter([t_curr], [y_kbps[t_curr]], color='#1E3A8A', s=130, zorder=5, edgecolors='white', linewidth=2)

    ax_ts.scatter([t_target], [y_kbps[t_target]], color='#DC2626', marker='*', s=360, zorder=6,
                  edgecolors='#7F1D1D', linewidth=1.5, label=f'Forecast Target y(t + H) at t + {H}s ({y_kbps[t_target]:,.0f} kbps)')

    for h_alt, lbl_alt in [(1, 't+1s'), (3, 't+3s'), (10, 't+10s')]:
        idx_alt = t_curr + h_alt
        ax_ts.scatter([idx_alt], [y_kbps[idx_alt]], color='#F59E0B', marker='D', s=75, zorder=5, edgecolors='#78350F')
        ax_ts.text(idx_alt, y_kbps[idx_alt] + max(y_kbps) * 0.045, lbl_alt, fontsize=8.5, fontweight='bold',
                   color='#92400E', ha='center', va='bottom')

    arrow_forecast = FancyArrowPatch(
        (t_curr, y_kbps[t_curr]), (t_target, y_kbps[t_target]),
        connectionstyle="arc3,rad=-0.22",
        arrowstyle='-|>', mutation_scale=22,
        color='#DC2626', lw=2.8, ls='--', zorder=6
    )
    ax_ts.add_patch(arrow_forecast)

    y_max = max(y_kbps) * 1.42
    ax_ts.set_ylim(0, y_max)
    ax_ts.set_xlim(0, len(selected_seg) - 1)

    ax_ts.text((t_start + t_curr) / 2, y_max * 0.87,
               "LOOKBACK WINDOW (L = 10s)\n10 Past Observations [t-9, ..., t]",
               ha='center', va='center', fontsize=9.8, fontweight='bold', color='#1E3A8A',
               bbox=dict(boxstyle='round,pad=0.35', facecolor='#EFF6FF', edgecolor='#3B82F6', lw=1.5))

    ax_ts.text((t_curr + t_target) / 2, y_max * 0.87,
               "PREDICTION HORIZON (H = 5s)\nDirect Jump (t → t+H)",
               ha='center', va='center', fontsize=9.8, fontweight='bold', color='#991B1B',
               bbox=dict(boxstyle='round,pad=0.35', facecolor='#FEF2F2', edgecolor='#EF4444', lw=1.5))

    ax_ts.annotate('', xy=(t_curr + 1, y_max * 0.06), xytext=(t_start + 1, y_max * 0.06),
                   arrowprops=dict(arrowstyle='<->', color='#059669', lw=2.2, ls='-'))
    ax_ts.text((t_start + t_curr) / 2 + 1, y_max * 0.095,
               "Next Sliding Step (t + 1): Window shifts right by Δt = 1s → [t-8, ..., t+1]",
               ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#065F46',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='#D1FAE5', edgecolor='#10B981'))

    ax_ts.set_title("A. Real 5G/LTE Downlink Throughput Trace Showing Lookback Window [t-L+1 ... t] and Forecast Horizon (t + H)",
                    fontsize=12.0, fontweight='bold', color='#0F172A', loc='left', pad=10)
    ax_ts.set_xlabel("Time Step t (seconds @ 1 Hz sampling)", fontsize=10.0, fontweight='bold', color='#334155')
    ax_ts.set_ylabel("DL_bitrate (kbps)", fontsize=10.0, fontweight='bold', color='#334155')
    ax_ts.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1')
    ax_ts.legend(loc='upper right', fontsize=8.3, ncol=1,
                 frameon=True, facecolor='white', edgecolor='#CBD5E1')

    # --------------------------------------------------------------------------
    # PANEL B (Bottom Left): Multivariate Input Feature Matrix (8 KPIs x L=10s)
    # --------------------------------------------------------------------------
    ax_mat = fig.add_subplot(gs[1, 0])
    scaled_cols = [
        'RSRP_scaled', 'RSRQ_scaled', 'SNR_scaled', 'CQI_scaled',
        'RSSI_scaled', 'Speed_scaled', 'UL_bitrate_scaled', 'ServingCell_Distance_scaled'
    ]
    display_names = ['RSRP', 'RSRQ', 'SNR', 'CQI', 'RSSI', 'Speed', 'UL_bitrate', 'Cell_Dist']

    window_matrix = selected_seg.iloc[t_start:t_curr + 1][scaled_cols].values.T  # shape (8, 10)

    im = ax_mat.imshow(window_matrix, cmap='RdYlBu_r', aspect='auto', vmin=-2.0, vmax=2.0)
    ax_mat.set_yticks(np.arange(len(display_names)))
    ax_mat.set_yticklabels(display_names, fontsize=9.2, fontweight='bold', color='#1E293B')
    time_labels = [f"t-{9-k}" if k < 9 else "t" for k in range(10)]
    ax_mat.set_xticks(np.arange(10))
    ax_mat.set_xticklabels(time_labels, fontsize=9.2, fontweight='bold', color='#1E293B')

    for r in range(window_matrix.shape[0]):
        for c in range(window_matrix.shape[1]):
            val = window_matrix[r, c]
            txt_color = 'white' if abs(val) > 1.1 else '#0F172A'
            ax_mat.text(c, r, f"{val:.1f}", ha='center', va='center', fontsize=7.8, color=txt_color, fontweight='bold')

    cbar = fig.colorbar(im, ax=ax_mat, fraction=0.035, pad=0.02)
    cbar.set_label("Z-Score (σ)", fontsize=9, fontweight='bold')
    ax_mat.set_title("B. Multivariate Input Tensor X_t ∈ R^(8 × 10) (Normalized KPIs in Window)",
                     fontsize=11.5, fontweight='bold', color='#0F172A', loc='left', pad=10)
    ax_mat.set_xlabel("Lookback Time Steps [t-9 ... t]", fontsize=9.8, fontweight='bold', color='#334155')

    # --------------------------------------------------------------------------
    # PANEL C (Bottom Right): Flattening & Model Mapping to Scalar Target y_hat
    # --------------------------------------------------------------------------
    ax_map = fig.add_subplot(gs[1, 1])
    ax_map.set_xlim(0, 1)
    ax_map.set_ylim(0, 1)
    ax_map.axis('off')

    draw_rounded_box(ax_map, 0.01, 0.02, 0.98, 0.94, facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1.8, radius=0.03, zorder=1)
    ax_map.text(0.5, 0.90, "C. Feature Representation & Model Target Mapping",
                ha='center', va='center', fontsize=11.5, fontweight='bold', color='#0F172A')

    draw_rounded_box(ax_map, 0.04, 0.50, 0.27, 0.32, facecolor='#EFF6FF', edgecolor='#3B82F6', lw=1.8, radius=0.025, zorder=2)
    ax_map.text(0.175, 0.74, "Tabular Flattening", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1E40AF')
    ax_map.text(0.175, 0.61, "x_t ∈ R^80\n(L=10 × 8 KPIs)\n[RSRP_(t-9) ... Dist_t]", ha='center', va='center', fontsize=8.4, color='#1E293B')

    draw_rounded_box(ax_map, 0.04, 0.10, 0.27, 0.32, facecolor='#F5F3FF', edgecolor='#8B5CF6', lw=1.8, radius=0.025, zorder=2)
    ax_map.text(0.175, 0.34, "Sequential Tensor", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#5B21B6')
    ax_map.text(0.175, 0.21, "X_t ∈ R^(10 × 8)\nPreserves Temporal\nStep Ordering", ha='center', va='center', fontsize=8.4, color='#1E293B')

    draw_rounded_box(ax_map, 0.38, 0.50, 0.27, 0.32, facecolor='#ECFDF5', edgecolor='#10B981', lw=2.0, radius=0.025, zorder=2)
    ax_map.text(0.515, 0.74, "Tree & Linear Models", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#065F46')
    ax_map.text(0.515, 0.61, "• XGBoost (Best!)\n• Random Forest\n• Ridge Regression", ha='center', va='center', fontsize=8.4, color='#1E293B')

    draw_rounded_box(ax_map, 0.38, 0.10, 0.27, 0.32, facecolor='#FFFBEB', edgecolor='#F59E0B', lw=1.8, radius=0.025, zorder=2)
    ax_map.text(0.515, 0.34, "Deep Neural Nets", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#92400E')
    ax_map.text(0.515, 0.21, "• LSTM Network\n• 1D-CNN\n• Deep MLP", ha='center', va='center', fontsize=8.4, color='#1E293B')

    draw_rounded_box(ax_map, 0.72, 0.18, 0.24, 0.58, facecolor='#FEF2F2', edgecolor='#DC2626', lw=2.2, radius=0.03, zorder=2)
    ax_map.text(0.84, 0.67, "Scalar Target\nForecast", ha='center', va='center', fontsize=10.0, fontweight='bold', color='#991B1B')
    ax_map.text(0.84, 0.47, f"y_hat(t+H)\n\nDL_bitrate\nat t + {H}s\n({y_kbps[t_target]:,.0f} kbps)",
                ha='center', va='center', fontsize=9.0, fontweight='bold', color='#DC2626')
    ax_map.text(0.84, 0.25, "Direct Strategy per\nH ∈ {1, 3, 5, 10}s", ha='center', va='center', fontsize=7.8, color='#7F1D1D')

    draw_arrow(ax_map, 0.315, 0.66, 0.375, 0.66, color='#2563EB', lw=2.2, mutation_scale=15)
    draw_arrow(ax_map, 0.315, 0.26, 0.375, 0.26, color='#7C3AED', lw=2.2, mutation_scale=15)
    draw_arrow(ax_map, 0.655, 0.66, 0.715, 0.53, color='#059669', lw=2.2, mutation_scale=15)
    draw_arrow(ax_map, 0.655, 0.26, 0.715, 0.41, color='#D97706', lw=2.2, mutation_scale=15)

    out_path = os.path.join(FIG_DIR, '15_sliding_window_mechanism.png')
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {out_path} ({os.path.getsize(out_path) / 1024:.1f} KB)")


# ==============================================================================
# FIGURE 16: Dataset Mobility Breakdown & Statistical Dashboard
# ==============================================================================
def generate_fig16_mobility_breakdown():
    combined_df = pd.read_csv(os.path.join(DATA_DIR, 'combined_traces.csv'))
    train_df = pd.read_csv(os.path.join(DATA_DIR, 'train_data.csv'))
    test_df = pd.read_csv(os.path.join(DATA_DIR, 'test_data.csv'))
    with open(os.path.join(DATA_DIR, 'metadata.json'), 'r') as f:
        meta = json.load(f)

    modes = ['car', 'train', 'pedestrian', 'static', 'bus']
    mode_labels = ['Car\n(Αυτοκίνητο)', 'Train\n(Τρένο)', 'Pedestrian\n(Πεζός)', 'Static\n(Στατικό)', 'Bus\n(Λεωφορείο)']

    train_samples = [len(train_df[train_df['mobility_mode'] == m]) for m in modes]
    test_samples = [len(test_df[test_df['mobility_mode'] == m]) for m in modes]
    total_samples = [len(combined_df[combined_df['mobility_mode'] == m]) for m in modes]

    train_traces = [train_df[train_df['mobility_mode'] == m]['trace_id'].nunique() for m in modes]
    test_traces = [test_df[test_df['mobility_mode'] == m]['trace_id'].nunique() for m in modes]
    total_traces = [combined_df[combined_df['mobility_mode'] == m]['trace_id'].nunique() for m in modes]

    mean_tp = [combined_df[combined_df['mobility_mode'] == m]['DL_bitrate'].mean() for m in modes]
    median_tp = [combined_df[combined_df['mobility_mode'] == m]['DL_bitrate'].median() for m in modes]
    mean_speed = [combined_df[combined_df['mobility_mode'] == m]['Speed'].mean() for m in modes]
    max_speed = [combined_df[combined_df['mobility_mode'] == m]['Speed'].quantile(0.95) for m in modes]

    fig = plt.figure(figsize=(16.5, 9.0), facecolor='#F8FAFC')
    gs = gridspec.GridSpec(1, 2, width_ratios=[1.08, 1.12], wspace=0.18,
                           left=0.085, right=0.945, top=0.83, bottom=0.10)

    fig.text(0.5, 0.94, "UCC 4G/LTE Multi-Mobility Dataset Breakdown & Kinematic-Throughput Profile",
             ha='center', va='center', fontsize=18.5, fontweight='bold', color='#0F172A')
    fig.text(0.5, 0.902, f"Total: {meta['total_samples']:,} 1-Hz Samples across {meta['total_traces']} Traces | Stratified 80% Train ({meta['train_samples']:,} rows, {meta['train_traces']} traces) vs. 20% Test ({meta['test_samples']:,} rows, {meta['test_traces']} traces)",
             ha='center', va='center', fontsize=11.0, color='#475569', style='italic')

    # --------------------------------------------------------------------------
    # PANEL A: Horizontal Stacked Bar Chart of Train vs Test Split per Mobility
    # --------------------------------------------------------------------------
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_facecolor('#FFFFFF')
    for spine in ['top', 'right']:
        ax_a.spines[spine].set_visible(False)

    y_pos = np.arange(len(modes))
    bar_h = 0.56

    ax_a.barh(y_pos, train_samples, height=bar_h, color='#2563EB', edgecolor='white', lw=1.5,
              label=f"80% Train Set ({meta['train_samples']:,} rows | {meta['train_traces']} traces)")
    ax_a.barh(y_pos, test_samples, left=train_samples, height=bar_h, color='#F59E0B', edgecolor='white', lw=1.5,
              label=f"20% Test Set ({meta['test_samples']:,} rows | {meta['test_traces']} traces)")

    ax_a.set_yticks(y_pos)
    ax_a.set_yticklabels(mode_labels, fontsize=10.0, fontweight='bold', color='#1E293B')
    ax_a.invert_yaxis()
    ax_a.set_xlim(0, max(total_samples) * 1.36)
    ax_a.set_xlabel("Number of 1 Hz Samples (Rows)", fontsize=10.2, fontweight='bold', color='#334155')
    ax_a.set_title("A. Sample & Trace Distribution by Mobility Mode (80/20 Split)",
                   fontsize=12.0, fontweight='bold', color='#0F172A', loc='left', pad=12)
    ax_a.grid(True, axis='x', linestyle='--', alpha=0.45, color='#CBD5E1')

    for i in range(len(modes)):
        tot = total_samples[i]
        pct = tot / meta['total_samples'] * 100
        tr_c = train_traces[i]
        te_c = test_traces[i]
        tot_c = total_traces[i]
        if train_samples[i] > 18000:
            ax_a.text(train_samples[i] / 2, y_pos[i], f"{train_samples[i]:,}\n({tr_c} tr)",
                      ha='center', va='center', color='white', fontsize=8.3, fontweight='bold')
        ax_a.text(tot + 1200, y_pos[i],
                  f"{tot:,} rows ({pct:.1f}%)\n{tot_c} Traces ({tr_c} Train / {te_c} Test)",
                  ha='left', va='center', color='#0F172A', fontsize=9.0, fontweight='bold')

    ax_a.legend(loc='lower right', fontsize=9.0, frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1')

    # --------------------------------------------------------------------------
    # PANEL B: Mean Throughput (kbps) vs Mean Velocity (km/h) per Mobility Scenario
    # --------------------------------------------------------------------------
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_facecolor('#FFFFFF')
    ax_b.spines['top'].set_visible(False)

    x_pos = np.arange(len(modes))
    width = 0.36

    rects_tp = ax_b.bar(x_pos - width / 2, mean_tp, width, color='#059669', edgecolor='white', lw=1.5,
                        label='Mean DL Throughput (kbps)', zorder=3)
    ax_b.bar(x_pos - width / 2, median_tp, width * 0.55, color='#A7F3D0', edgecolor='#047857', lw=1.0,
             label='Median DL Throughput (kbps)', zorder=4)

    ax_b.set_ylabel("Downlink Throughput (kbps)", fontsize=10.2, fontweight='bold', color='#065F46')
    ax_b.tick_params(axis='y', colors='#065F46')
    ax_b.set_ylim(0, max(mean_tp) * 1.28)
    ax_b.set_xticks(x_pos)
    ax_b.set_xticklabels(mode_labels, fontsize=9.8, fontweight='bold', color='#1E293B')
    ax_b.grid(True, axis='y', linestyle='--', alpha=0.45, color='#CBD5E1', zorder=1)

    ax_b2 = ax_b.twinx()
    ax_b2.spines['top'].set_visible(False)
    rects_spd = ax_b2.bar(x_pos + width / 2, mean_speed, width, color='#7C3AED', edgecolor='white', lw=1.5,
                          label='Mean UE Velocity (km/h)', zorder=3)
    ax_b2.plot(x_pos + width / 2, max_speed, color='#DC2626', marker='^', lw=1.8, ls='--', markersize=7,
               label='95th Percentile Speed (km/h)', zorder=5)

    ax_b2.set_ylabel("UE Velocity (km/h)", fontsize=10.2, fontweight='bold', color='#5B21B6')
    ax_b2.tick_params(axis='y', colors='#5B21B6')
    ax_b2.set_ylim(0, max(max_speed) * 1.25)

    for i, rect in enumerate(rects_tp):
        h_val = rect.get_height()
        ax_b.text(rect.get_x() + rect.get_width() / 2, h_val + 300,
                  f"{h_val:,.0f}\nkbps", ha='center', va='bottom', fontsize=8.4, fontweight='bold', color='#065F46')

    for i, rect in enumerate(rects_spd):
        s_val = rect.get_height()
        x_off = 0.14 if modes[i] == 'pedestrian' else 0.0
        y_offset = 6.5 if modes[i] == 'pedestrian' else 1.8
        ax_b2.text(rect.get_x() + rect.get_width() / 2 + x_off, s_val + y_offset,
                   f"{s_val:.1f}\nkm/h", ha='center', va='bottom', fontsize=8.4, fontweight='bold', color='#5B21B6')

    ax_b.set_title("B. Mean Downlink Throughput (kbps) & UE Velocity (km/h) per Scenario",
                   fontsize=12.0, fontweight='bold', color='#0F172A', loc='left', pad=12)

    handles1, labels1 = ax_b.get_legend_handles_labels()
    handles2, labels2 = ax_b2.get_legend_handles_labels()
    ax_b.legend(handles1 + handles2, labels1 + labels2, loc='upper right', fontsize=8.4,
                frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', ncol=2)

    out_path = os.path.join(FIG_DIR, '16_dataset_mobility_breakdown.png')
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Saved: {out_path} ({os.path.getsize(out_path) / 1024:.1f} KB)")


if __name__ == '__main__':
    print("Generating 4 high-resolution presentation diagrams (300 DPI)...")
    generate_fig13_reactive_vs_proactive()
    generate_fig14_preprocessing_pipeline()
    generate_fig15_sliding_window()
    generate_fig16_mobility_breakdown()
    print("All 4 presentation diagrams generated successfully!")
