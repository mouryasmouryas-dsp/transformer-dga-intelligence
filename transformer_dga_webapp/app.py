"""
Transformer DGA Intelligence
=============================
PRML-Based Power Transformer Fault Diagnosis Using Dissolved Gas Analysis

Main Streamlit application entry point.
Designed and developed by Mourya Abbadasari | Electrical Engineering, IIT Tirupati
"""

import streamlit as st

# ─── Page configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Transformer DGA Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "**Transformer DGA Intelligence**\n\n"
            "PRML-Based Power Transformer Fault Diagnosis Using "
            "Dissolved Gas Analysis\n\n"
            "Designed and developed by Mourya Abbadasari | "
            "Electrical Engineering, IIT Tirupati"
        ),
    },
)


# ─── Custom CSS ──────────────────────────────────────────────────────────────
def load_custom_css():
    """Inject premium custom CSS for the industrial dashboard aesthetic."""
    st.markdown("""
    <style>
    /* ── Import Google Font ─────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global ─────────────────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main .block-container {
        padding-top: 1.5rem;
        max-width: 1200px;
    }

    /* ── Sidebar ────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A0E1A 0%, #111827 50%, #0F172A 100%);
        border-right: 1px solid rgba(0, 212, 255, 0.15);
    }

    [data-testid="stSidebar"] .stRadio > label {
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* ── Cards ──────────────────────────────────────────────────────── */
    .dga-card {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .dga-card:hover {
        border-color: rgba(0, 212, 255, 0.35);
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.1);
        transform: translateY(-2px);
    }

    /* ── Metric Cards ──────────────────────────────────────────────── */
    .metric-card {
        background: linear-gradient(135deg, #111827 0%, #1E293B 100%);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        border-color: rgba(0, 212, 255, 0.5);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #00D4FF;
        margin: 0.3rem 0;
    }

    .metric-label {
        font-size: 0.78rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
    }

    /* ── Headers ────────────────────────────────────────────────────── */
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00D4FF, #0EA5E9, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }

    .page-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #E2E8F0;
        margin: 1.5rem 0 0.75rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(0, 212, 255, 0.15);
    }

    /* ── Result Badge ──────────────────────────────────────────────── */
    .result-badge {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 0.02em;
    }

    .badge-electrical {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(99, 102, 241, 0.2));
        border: 1px solid rgba(59, 130, 246, 0.4);
        color: #93C5FD;
    }

    .badge-thermal {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(239, 68, 68, 0.2));
        border: 1px solid rgba(245, 158, 11, 0.4);
        color: #FCD34D;
    }

    /* ── Tooltips ───────────────────────────────────────────────────── */
    .dga-tooltip {
        position: relative;
        display: inline-flex;
        align-items: center;
        cursor: help;
    }

    .dga-tooltip .tooltip-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background: rgba(0, 212, 255, 0.15);
        color: #00D4FF;
        font-size: 10px;
        font-weight: 700;
        margin-left: 4px;
        transition: all 0.2s ease;
    }

    .dga-tooltip:hover .tooltip-icon {
        background: rgba(0, 212, 255, 0.3);
    }

    .dga-tooltip .tooltip-content {
        visibility: hidden;
        opacity: 0;
        position: absolute;
        z-index: 1000;
        bottom: calc(100% + 8px);
        left: 50%;
        transform: translateX(-50%);
        width: 280px;
        padding: 10px 14px;
        background: rgba(15, 23, 42, 0.97);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 212, 255, 0.25);
        border-radius: 8px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
        color: #CBD5E1;
        font-size: 0.78rem;
        line-height: 1.45;
        font-weight: 400;
        transition: all 0.25s ease;
    }

    .dga-tooltip:hover .tooltip-content,
    .dga-tooltip:focus-within .tooltip-content {
        visibility: visible;
        opacity: 1;
    }

    /* ── Warning Box ───────────────────────────────────────────────── */
    .warning-box {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        color: #FCD34D;
        font-size: 0.85rem;
    }

    .error-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        color: #FCA5A5;
        font-size: 0.85rem;
    }

    /* ── Info Box ───────────────────────────────────────────────────── */
    .info-box {
        background: rgba(0, 212, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        color: #94A3B8;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    /* ── Disclaimer ────────────────────────────────────────────────── */
    .disclaimer {
        background: rgba(100, 116, 139, 0.1);
        border: 1px solid rgba(100, 116, 139, 0.2);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin: 1rem 0;
        color: #94A3B8;
        font-size: 0.78rem;
        font-style: italic;
        line-height: 1.5;
    }

    /* ── Footer ────────────────────────────────────────────────────── */
    .app-footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-top: 3rem;
        border-top: 1px solid rgba(0, 212, 255, 0.1);
        color: #64748B;
        font-size: 0.78rem;
    }

    .app-footer a {
        color: #00D4FF;
        text-decoration: none;
    }

    /* ── Welcome Hero ──────────────────────────────────────────────── */
    .hero-container {
        text-align: center;
        padding: 2rem 1rem;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00D4FF 0%, #0EA5E9 30%, #06B6D4 60%, #14B8A6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.03em;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #94A3B8;
        max-width: 600px;
        margin: 0 auto 1.5rem auto;
        line-height: 1.6;
    }

    .hero-tagline {
        font-size: 0.9rem;
        color: #64748B;
        font-style: italic;
        margin-top: 1rem;
    }

    /* ── Capability Cards ──────────────────────────────────────────── */
    .capability-card {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(0, 212, 255, 0.12);
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }

    .capability-card:hover {
        border-color: rgba(0, 212, 255, 0.3);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.08);
    }

    .capability-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }

    .capability-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #E2E8F0;
        margin-bottom: 0.3rem;
    }

    .capability-desc {
        font-size: 0.72rem;
        color: #94A3B8;
        line-height: 1.4;
    }

    /* ── Workflow Step ──────────────────────────────────────────────── */
    .workflow-step {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: rgba(0, 212, 255, 0.08);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 8px;
        margin: 0.2rem;
        font-size: 0.8rem;
        color: #CBD5E1;
    }

    .workflow-arrow {
        display: inline-block;
        color: #00D4FF;
        font-size: 1.2rem;
        margin: 0 0.3rem;
        vertical-align: middle;
    }

    /* ── Animations ─────────────────────────────────────────────────── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out;
    }

    /* ── Stacked bar fix ───────────────────────────────────────────── */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2);
    }

    /* ── Table styling ─────────────────────────────────────────────── */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }

    .styled-table th {
        background: rgba(0, 212, 255, 0.1);
        color: #00D4FF;
        padding: 0.6rem 0.8rem;
        text-align: left;
        border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        font-weight: 600;
        font-size: 0.8rem;
    }

    .styled-table td {
        padding: 0.5rem 0.8rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        color: #CBD5E1;
    }

    .styled-table tr:hover td {
        background: rgba(0, 212, 255, 0.03);
    }

    /* Style Streamlit collapsedControl (3-bars hamburger button on mobile) */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        background: #111827 !important;
        border: 2px solid #00D4FF !important;
        border-radius: 8px !important;
        padding: 4px 8px !important;
        margin: 6px !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.4) !important;
        z-index: 1000000 !important;
    }

    [data-testid="collapsedControl"] svg {
        fill: #00D4FF !important;
        stroke: #00D4FF !important;
        width: 24px !important;
        height: 24px !important;
    }

    /* Hide Streamlit's default top-right menu and footer, but keep collapsedControl */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# ─── Helper functions ────────────────────────────────────────────────────────
from utils.ui import tooltip, render_footer


# ─── Session state initialisation ────────────────────────────────────────────
def init_session_state():
    """Initialise all session state variables."""
    defaults = {
        "page": "welcome",
        "user_name": "",
        "user_purpose": "",
        "user_org": "",
        "transformer_label": "",
        "welcomed": False,
        "intro_seen": False,
        "analysis_history": [],
        "last_result": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ─── Page imports ────────────────────────────────────────────────────────────
from views.welcome import render_welcome
from views.introduction import render_introduction
from views.overview import render_overview
from views.dga_guide import render_dga_guide
from views.analysis import render_analysis
from views.results import render_results
from views.fault_guide import render_fault_guide
from views.model_performance import render_model_performance
from views.feature_importance import render_feature_importance
from views.visualisation import render_visualisation
from views.about import render_about
from views.limitations import render_limitations
from views.history import render_history


# ─── Navigation options ──────────────────────────────────────────────────────
NAV_OPTIONS = [
    "📊 Overview",
    "📘 DGA Knowledge Guide",
    "🔬 New DGA Analysis",
    "📖 Fault Classification Guide",
    "📈 Gas Data Visualisation",
    "🏆 Model Performance",
    "🎯 Feature Importance",
    "📋 Analysis History",
    "ℹ️ About the Project",
    "⚠️ Limitations & Safety",
]


# ─── Main application ───────────────────────────────────────────────────────
def main():
    """Main application entry point."""
    load_custom_css()
    init_session_state()

    # Track active page in session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "📊 Overview"

    # ── Welcome flow (no sidebar) ────────────────────────────────────────
    if not st.session_state.welcomed:
        render_welcome()
        render_footer()
        return

    if not st.session_state.intro_seen:
        render_introduction()
        render_footer()
        return

    # ── Mobile Top Navigation Bar (3 bars = / ☰) ──────────────────────────
    with st.container():
        mob_col1, mob_col2 = st.columns([1, 3])
        with mob_col1:
            if st.button("☰ Menu", key="mobile_menu_btn", help="Click to open or close navigation menu"):
                st.session_state.mobile_menu_open = not st.session_state.get("mobile_menu_open", False)
                st.rerun()

        with mob_col2:
            st.markdown(
                f'<div style="text-align: right; padding: 6px 12px; background: rgba(17, 24, 39, 0.7); '
                f'border: 1px solid rgba(0, 212, 255, 0.25); border-radius: 8px; color: #00D4FF; '
                f'font-size: 0.85rem; font-weight: 600;">'
                f'📍 {st.session_state.current_page}</div>',
                unsafe_allow_html=True,
            )

    # When ☰ Menu is clicked on mobile / desktop
    if st.session_state.get("mobile_menu_open", False):
        st.markdown("""
        <div class="dga-card" style="border: 2px solid #00D4FF; margin-bottom: 1rem; padding: 1rem; background: #0A0E1A;">
            <p style="color: #00D4FF; font-weight: 700; margin-bottom: 0.8rem; font-size: 0.95rem;">
                ☰ Navigation Menu — Tap any section to open:
            </p>
        </div>
        """, unsafe_allow_html=True)
        menu_cols = st.columns(2)
        for i, opt in enumerate(NAV_OPTIONS):
            c = menu_cols[i % 2]
            btn_type = "primary" if opt == st.session_state.current_page else "secondary"
            if c.button(opt, key=f"mob_nav_opt_{i}", use_container_width=True, type=btn_type):
                st.session_state.current_page = opt
                st.session_state.show_results = False
                st.session_state.mobile_menu_open = False
                st.rerun()
        st.markdown("---")

    # ── Sidebar navigation ───────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
            <div style="font-size: 1.8rem;">⚡</div>
            <div style="font-size: 0.95rem; font-weight: 700; color: #00D4FF;
                        margin-top: 0.3rem; letter-spacing: -0.01em;">
                DGA Intelligence
            </div>
            <div style="font-size: 0.65rem; color: #64748B; margin-top: 0.2rem;">
                Transformer Fault Diagnosis
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Greeting
        user_display = st.session_state.user_name or "User"
        st.markdown(
            f'<p style="color: #94A3B8; font-size: 0.8rem; margin-bottom: 0.5rem;">'
            f'👋 Welcome, <strong style="color: #E2E8F0;">{user_display}</strong></p>',
            unsafe_allow_html=True,
        )

        current_idx = NAV_OPTIONS.index(st.session_state.current_page) if st.session_state.current_page in NAV_OPTIONS else 0
        selected = st.radio(
            "Navigation",
            NAV_OPTIONS,
            index=current_idx,
            label_visibility="collapsed",
            key="sidebar_radio_selection",
        )

        if selected != st.session_state.current_page:
            st.session_state.current_page = selected
            st.session_state.show_results = False
            st.rerun()

        st.markdown("---")

        # Session controls
        if st.button("🔄 Clear Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        st.markdown(
            '<p style="color: #475569; font-size: 0.65rem; text-align: center; '
            'margin-top: 1rem;">v1.0.0 | Mourya Abbadasari</p>',
            unsafe_allow_html=True,
        )

    # ── Page routing ─────────────────────────────────────────────────────
    # Check if we should show results
    if st.session_state.get("show_results") and st.session_state.last_result:
        render_results()
        render_footer()
        return

    page_map = {
        "📊 Overview": render_overview,
        "📘 DGA Knowledge Guide": render_dga_guide,
        "🔬 New DGA Analysis": render_analysis,
        "📖 Fault Classification Guide": render_fault_guide,
        "📈 Gas Data Visualisation": render_visualisation,
        "🏆 Model Performance": render_model_performance,
        "🎯 Feature Importance": render_feature_importance,
        "📋 Analysis History": render_history,
        "ℹ️ About the Project": render_about,
        "⚠️ Limitations & Safety": render_limitations,
    }

    render_fn = page_map.get(st.session_state.current_page, render_overview)
    render_fn()
    render_footer()


if __name__ == "__main__":
    main()
