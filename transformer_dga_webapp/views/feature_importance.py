"""
Feature Importance page.

Shows permutation importance from grouped cross-validation.
"""

import streamlit as st
import plotly.graph_objects as go

from config.settings import PERMUTATION_IMPORTANCE, FEATURE_FORMULAS, TOOLTIPS
from utils.ui import tooltip


def render_feature_importance():
    """Render the feature importance page."""

    st.markdown('<div class="page-title">🎯 Feature Importance</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        'Permutation importance from grouped 5-fold cross-validation. '
        'Shows how much each gas feature contributes to model performance.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Explanation ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="info-box">
        <strong>What is permutation importance?</strong> For each gas feature,
        its values are randomly shuffled and the model is re-evaluated. The
        resulting decrease in macro F1-score indicates how much the model
        relied on that feature. A larger decrease means greater reliance.
        <br><br>
        <strong>Limitations:</strong> Permutation importance measures
        <em>predictive reliance</em> under the evaluation procedure, not
        causal or universal physical importance. It does not prove that a
        gas physically causes a particular fault type.
    </div>
    """, unsafe_allow_html=True)

    # ── Importance Chart ─────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">'
        + tooltip(
            "📊 Grouped-CV Permutation Importance",
            TOOLTIPS["feature_importance"],
        )
        + '</div>',
        unsafe_allow_html=True,
    )

    # Sort ascending for horizontal bar chart (top = most important)
    sorted_imp = sorted(PERMUTATION_IMPORTANCE, key=lambda x: x["Mean_Importance"])

    gases = [FEATURE_FORMULAS.get(p["Gas"], p["Gas"]) for p in sorted_imp]
    values = [p["Mean_Importance"] for p in sorted_imp]
    stds = [p["Fold_Std"] for p in sorted_imp]

    # Color gradient from low to high importance
    colors = ["#1E3A5F", "#1E6091", "#0EA5E9", "#06B6D4", "#00D4FF"]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=gases,
        x=values,
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color="rgba(0, 212, 255, 0.3)", width=1),
        ),
        error_x=dict(
            type="data",
            array=stds,
            color="#94A3B8",
            thickness=1.5,
            width=4,
        ),
        text=[f"{v:.4f}" for v in values],
        textposition="auto",
        textfont=dict(color="white", size=12, family="Inter"),
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", size=12, family="Inter"),
        margin=dict(l=0, r=40, t=10, b=50),
        height=350,
        xaxis=dict(
            title="Mean Decrease in Macro F1-Score After Shuffling",
            gridcolor="rgba(255,255,255,0.05)",
            zeroline=True,
            zerolinecolor="rgba(255,255,255,0.1)",
        ),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Data Table ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Importance Values</div>',
                unsafe_allow_html=True)

    table_html = """
    <div class="dga-card">
        <table class="styled-table">
            <thead><tr>
                <th>Rank</th>
                <th>Gas</th>
                <th>Formula</th>
                <th style="text-align: right;">Mean Macro-F1 Decrease</th>
                <th style="text-align: right;">Fold Std Dev</th>
            </tr></thead><tbody>
    """

    for rank, entry in enumerate(PERMUTATION_IMPORTANCE, 1):
        gas = entry["Gas"]
        formula = FEATURE_FORMULAS.get(gas, gas)
        val = entry["Mean_Importance"]
        std = entry["Fold_Std"]

        # Bar width for visual representation
        bar_width = int(val / 0.36 * 100)
        table_html += f"""
        <tr>
            <td style="font-weight: 700; color: #00D4FF;">{rank}</td>
            <td>{gas}</td>
            <td>{formula}</td>
            <td style="text-align: right;">
                <div style="display: flex; align-items: center; justify-content: flex-end; gap: 8px;">
                    <div style="width: {bar_width}px; height: 8px; background: linear-gradient(90deg, #0EA5E9, #00D4FF);
                                border-radius: 4px;"></div>
                    <span>{val:.4f}</span>
                </div>
            </td>
            <td style="text-align: right;">±{std:.4f}</td>
        </tr>
        """

    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

    # ── Interpretation ───────────────────────────────────────────────────
    st.markdown('<div class="section-header">💡 Interpretation Guide</div>',
                unsafe_allow_html=True)

    with st.expander("Learn more about permutation importance", expanded=False):
        st.markdown("""
        **How it works:**
        1. The Random Forest model is trained on each training fold.
        2. For each gas feature in the held-out fold, the values are randomly
           shuffled (permuted) while keeping all other features unchanged.
        3. The model is re-evaluated on the shuffled data.
        4. The decrease in macro F1-score measures how much the model relied
           on that feature.
        5. This is repeated 20 times per fold, and results are averaged
           across 5 folds.

        **Key findings:**
        - **C₂H₄ (Ethylene)** and **C₂H₂ (Acetylene)** are the most
          influential features, with similar importance levels.
        - **H₂ (Hydrogen)** has moderate importance.
        - **C₂H₆ (Ethane)** and **CH₄ (Methane)** contribute less but
          still improve the model.

        **Caveats:**
        - These values describe the model's statistical reliance, not
          physical causation.
        - Correlated features may share importance, potentially
          underestimating the true contribution of individual gases.
        - Results are specific to this model and dataset.
        """)

    st.markdown("""
    <div class="disclaimer">
        The importance values were computed using grouped 5-fold
        cross-validation with 20 permutation repeats per fold. They represent
        the model's average reliance on each feature across folds, not
        universally applicable diagnostic weights.
    </div>
    """, unsafe_allow_html=True)
