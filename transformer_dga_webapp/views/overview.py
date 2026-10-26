"""
Overview / Dashboard page.

Shows a summary of the application state and quick access to key features.
"""

import streamlit as st

from config.settings import (
    MODEL_COMPARISON,
    GROUPED_VALIDATION,
    TOOLTIPS,
    CLASS_LABELS,
)
from utils.ui import tooltip


def render_overview():
    """Render the main dashboard overview page."""

    st.markdown('<div class="page-title">📊 Dashboard Overview</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        'Welcome to the Transformer DGA Intelligence platform. '
        'Navigate using the sidebar to analyse transformer gas data, '
        'explore model performance, or review fault classifications.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Quick Stats ──────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Model Accuracy</div>
            <div class="metric-value">75.42%</div>
            <div style="font-size: 0.68rem; color: #64748B;">Holdout test</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Macro F1-Score</div>
            <div class="metric-value">73.82%</div>
            <div style="font-size: 0.68rem; color: #64748B;">Holdout test</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Fault Classes</div>
            <div class="metric-value">6</div>
            <div style="font-size: 0.68rem; color: #64748B;">PD, D1, D2, T1, T2, T3</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        analyses_count = len(st.session_state.get("analysis_history", []))
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Session Analyses</div>
            <div class="metric-value">{analyses_count}</div>
            <div style="font-size: 0.68rem; color: #64748B;">This session</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Quick Actions ────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🚀 Quick Actions</div>',
                unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("""
        <div class="dga-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔬</div>
            <div style="font-weight: 600; color: #E2E8F0; margin-bottom: 0.3rem;">
                New DGA Analysis
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8;">
                Enter gas readings and get a fault classification prediction.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="dga-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📖</div>
            <div style="font-weight: 600; color: #E2E8F0; margin-bottom: 0.3rem;">
                Fault Classification Guide
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8;">
                Learn about the six fault categories and their DGA patterns.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown("""
        <div class="dga-card" style="text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏆</div>
            <div style="font-weight: 600; color: #E2E8F0; margin-bottom: 0.3rem;">
                Model Performance
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8;">
                Review holdout metrics, cross-validation, and model comparisons.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Model Comparison Summary ─────────────────────────────────────────
    st.markdown(
        '<div class="section-header">'
        + tooltip("🏅 Model Comparison Summary", TOOLTIPS["accuracy"])
        + '</div>',
        unsafe_allow_html=True,
    )

    table_html = """
    <div class="dga-card">
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Model</th>
                    <th style="text-align: right;">Accuracy (%)</th>
                    <th style="text-align: right;">Macro F1</th>
                </tr>
            </thead>
            <tbody>
    """
    for entry in MODEL_COMPARISON:
        is_best = entry["Model"] == "Random Forest"
        name_style = ' style="color: #00D4FF; font-weight: 600;"' if is_best else ""
        badge = " 🏆" if is_best else ""
        table_html += f"""
                <tr>
                    <td{name_style}>{entry['Model']}{badge}</td>
                    <td style="text-align: right;">{entry['Accuracy']:.2f}%</td>
                    <td style="text-align: right;">{entry['Macro F1']:.4f}</td>
                </tr>
        """
    table_html += """
            </tbody>
        </table>
        <p style="font-size: 0.72rem; color: #64748B; margin-top: 0.5rem;">
            All models evaluated on the same 20% holdout test set.
            Random Forest selected as the production model.
        </p>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)

    # ── Grouped CV Summary ───────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">'
        + tooltip("📋 Grouped Cross-Validation Summary", TOOLTIPS["grouped_cv"])
        + '</div>',
        unsafe_allow_html=True,
    )

    gv = GROUPED_VALIDATION
    col_g1, col_g2, col_g3, col_g4 = st.columns(4)
    with col_g1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Mean Accuracy</div>
            <div class="metric-value">{gv['mean_accuracy']*100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Acc. Std Dev</div>
            <div class="metric-value">±{gv['accuracy_std']*100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Mean Macro F1</div>
            <div class="metric-value">{gv['mean_macro_f1']*100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col_g4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">F1 Std Dev</div>
            <div class="metric-value">±{gv['macro_f1_std']*100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
