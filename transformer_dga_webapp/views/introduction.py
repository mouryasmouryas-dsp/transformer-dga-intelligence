"""
Introduction page — project overview shown after welcome.

Explains DGA, the ML approach, capabilities, and recorded model performance.
"""

import streamlit as st

from config.settings import TOOLTIPS


def render_introduction():
    """Render the project introduction page."""

    st.markdown("""
    <div class="animate-fade-in" style="text-align: center; margin-bottom: 1.5rem;">
        <div style="font-size: 2.5rem;">⚡</div>
        <div class="page-title">Transformer DGA Intelligence</div>
        <div class="page-subtitle">
            PRML-Based Power Transformer Fault Diagnosis Using Dissolved Gas Analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Greeting ─────────────────────────────────────────────────────────
    user = st.session_state.get("user_name", "")
    if user:
        st.markdown(
            f'<div class="dga-card" style="text-align: center;">'
            f'<p style="color: #00D4FF; font-size: 1.1rem; font-weight: 600;">'
            f'Welcome, {user}. Let\'s explore your transformer\'s DGA profile.</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── What is DGA? ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🔍 What is Dissolved Gas Analysis?</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card">
        <p style="color: #CBD5E1; line-height: 1.7; font-size: 0.9rem;">
            Dissolved Gas Analysis (DGA) examines gases dissolved in the insulating
            oil of power transformers. Different types of electrical and thermal
            faults produce characteristic patterns of dissolved gases. By measuring
            five key gases — <strong style="color: #00D4FF;">Hydrogen (H₂)</strong>,
            <strong style="color: #00D4FF;">Methane (CH₄)</strong>,
            <strong style="color: #00D4FF;">Ethane (C₂H₆)</strong>,
            <strong style="color: #00D4FF;">Ethylene (C₂H₄)</strong>, and
            <strong style="color: #00D4FF;">Acetylene (C₂H₂)</strong> —
            engineers can gain evidence about possible fault conditions inside the
            transformer.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Why ML? ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🤖 Why Use Machine Learning?</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card">
        <p style="color: #CBD5E1; line-height: 1.7; font-size: 0.9rem;">
            A trained classifier can identify patterns in labelled historical data
            and suggest a likely fault category based on the gas concentration
            profile. This can supplement — but not replace — traditional DGA
            interpretation methods and engineering judgement.
        </p>
        <p style="color: #94A3B8; line-height: 1.7; font-size: 0.82rem; margin-top: 0.5rem;">
            <strong>Important:</strong> A machine-learning prediction is not a
            confirmed physical diagnosis. It identifies a statistical pattern
            similar to one of the training categories.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── How does it work? ────────────────────────────────────────────────
    st.markdown('<div class="section-header">⚙️ How Does the Application Work?</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card" style="text-align: center; padding: 1.5rem;">
        <div style="display: flex; flex-wrap: wrap; justify-content: center;
                    align-items: center; gap: 0.3rem;">
            <span class="workflow-step">🧪 Laboratory DGA Measurement</span>
            <span class="workflow-arrow">→</span>
            <span class="workflow-step">📐 Unit Normalisation</span>
            <span class="workflow-arrow">→</span>
            <span class="workflow-step">✅ Input Validation</span>
            <span class="workflow-arrow">→</span>
            <span class="workflow-step">🌲 Trained Random Forest</span>
            <span class="workflow-arrow">→</span>
            <span class="workflow-step">🏷️ Predicted Class</span>
            <span class="workflow-arrow">→</span>
            <span class="workflow-step">📊 Diagnostic Summary & Review</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Capabilities ─────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🎯 Project Capabilities</div>',
                unsafe_allow_html=True)

    caps = [
        ("🧪", "Five-Gas Input Analysis",
         "Enter H₂, CH₄, C₂H₆, C₂H₄, C₂H₂ concentrations from your DGA report."),
        ("🏷️", "Six-Class Fault Classification",
         "PD, D1, D2, T1, T2, T3 — covering discharge and thermal fault categories."),
        ("📊", "Interactive Visualisation",
         "Plotly-powered charts for gas profiles, model scores, and performance."),
        ("📈", "Class Probability Estimates",
         "Random Forest probability estimates for all six classes (not calibrated)."),
        ("🏆", "Historical Model Performance",
         "Holdout metrics, grouped cross-validation, and model comparison."),
        ("📥", "Downloadable Reports",
         "PDF and CSV exports with full prediction details and disclaimers."),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(caps):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="capability-card">
                <div class="capability-icon">{icon}</div>
                <div class="capability-title">{title}</div>
                <div class="capability-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Model Performance Card ───────────────────────────────────────────
    st.markdown('<div class="section-header">🏆 Recorded Model Performance</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="dga-card">
            <p style="color: #00D4FF; font-weight: 600; font-size: 0.9rem;
                      margin-bottom: 0.8rem;">Holdout Test Evaluation</p>
            <div style="display: flex; justify-content: space-around;">
                <div class="metric-card" style="flex: 1; margin-right: 0.5rem;">
                    <div class="metric-label">Accuracy</div>
                    <div class="metric-value">75.42%</div>
                </div>
                <div class="metric-card" style="flex: 1;">
                    <div class="metric-label">Macro F1</div>
                    <div class="metric-value">73.82%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="dga-card">
            <p style="color: #00D4FF; font-weight: 600; font-size: 0.9rem;
                      margin-bottom: 0.8rem;">Grouped 5-Fold Cross-Validation</p>
            <div style="display: flex; justify-content: space-around;">
                <div class="metric-card" style="flex: 1; margin-right: 0.5rem;">
                    <div class="metric-label">Mean Accuracy</div>
                    <div class="metric-value">77.51%</div>
                </div>
                <div class="metric-card" style="flex: 1;">
                    <div class="metric-label">Mean Macro F1</div>
                    <div class="metric-value">76.78%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        These are experimental results on the available dataset. They do not
        establish the same level of accuracy on unseen transformers or in
        operational field conditions.
    </div>
    """, unsafe_allow_html=True)

    # ── Start button ─────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        if st.button(
            "⚡ Start Transformer Analysis",
            use_container_width=True,
            type="primary",
        ):
            st.session_state.intro_seen = True
            st.rerun()
