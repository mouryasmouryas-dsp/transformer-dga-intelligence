"""
Results page — displayed after a successful prediction.

Shows predicted class, probabilities, gas profile chart,
warnings, and download options.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from config.settings import (
    FEATURE_NAMES,
    FEATURE_LABELS,
    FEATURE_FORMULAS,
    CLASS_DESCRIPTIONS,
    TOOLTIPS,
    PERMUTATION_IMPORTANCE,
)
from backend.reporting import generate_pdf_report, generate_csv_report
from backend.duval import calculate_duval_triangle_1
from utils.ui import tooltip


def render_results():
    """Render the prediction results page."""

    result = st.session_state.get("last_result")
    if not result or not result.success:
        st.warning("No analysis results available. Please run a new analysis.")
        return

    # ── Header ───────────────────────────────────────────────────────────
    st.markdown('<div class="page-title animate-fade-in">📊 Analysis Results</div>',
                unsafe_allow_html=True)

    # ── Main Result Card ─────────────────────────────────────────────────
    class_info = result.class_description
    category = class_info.get("category", "Unknown")
    badge_class = "badge-electrical" if category == "Electrical" else "badge-thermal"

    st.markdown(f"""
    <div class="dga-card animate-fade-in">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
            <div>
                <p style="color: #64748B; font-size: 0.75rem; margin-bottom: 0.3rem;">
                    Reference: {result.reference_id} | {result.timestamp}
                </p>
                <p style="color: #94A3B8; font-size: 0.8rem;">
                    Transformer: {result.transformer_label or 'Not specified'} |
                    Model: v{result.model_version}
                </p>
            </div>
            <div>
                <span class="result-badge {badge_class}">
                    {result.predicted_class} — {class_info.get('name', '')}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Predicted Class Explanation ───────────────────────────────────────
    st.markdown(
        '<div class="section-header">'
        + tooltip("🏷️ Predicted Fault Class", TOOLTIPS["predicted_class"])
        + '</div>',
        unsafe_allow_html=True,
    )

    col_class, col_sep = st.columns([3, 1])
    with col_class:
        st.markdown(f"""
        <div class="dga-card">
            <p style="color: #00D4FF; font-weight: 700; font-size: 1.2rem; margin-bottom: 0.5rem;">
                {result.predicted_class} — {class_info.get('name', '')}
            </p>
            <p style="color: #94A3B8; font-size: 0.78rem; margin-bottom: 0.5rem;">
                Category: <strong style="color: #E2E8F0;">{category}</strong>
            </p>
            <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.6; margin-bottom: 0.8rem;">
                {class_info.get('description', '')}
            </p>
            <div style="background: rgba(0, 212, 255, 0.05); border-radius: 6px;
                        padding: 0.7rem; margin-bottom: 0.5rem;">
                <p style="color: #94A3B8; font-size: 0.82rem; line-height: 1.5;">
                    <strong style="color: #00D4FF;">DGA Context:</strong>
                    {class_info.get('dga_context', '')}
                </p>
            </div>
            <div style="background: rgba(245, 158, 11, 0.08); border-radius: 6px; padding: 0.7rem;">
                <p style="color: #FCD34D; font-size: 0.82rem; line-height: 1.5;">
                    <strong>⚠️ Engineering Note:</strong>
                    {class_info.get('engineering_note', '')}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Interpretation Guide ─────────────────────────────────────────────
    st.markdown("""
    <div class="dga-card" style="border-color: rgba(100, 116, 139, 0.2);">
        <p style="color: #94A3B8; font-size: 0.82rem; font-weight: 600; margin-bottom: 0.5rem;">
            Understanding This Result:
        </p>
        <ol style="color: #94A3B8; font-size: 0.78rem; line-height: 1.7; padding-left: 1.2rem;">
            <li><strong style="color: #CBD5E1;">What the model predicted:</strong>
                The gas pattern most closely matches the training data labelled as the above class.</li>
            <li><strong style="color: #CBD5E1;">What the model's training data supports:</strong>
                The model was trained on 587 records from the IEEE standard dataset with six fault categories.</li>
            <li><strong style="color: #CBD5E1;">What cannot be concluded:</strong>
                This prediction does not confirm the exact physical fault, its severity, or the remaining useful life.</li>
            <li><strong style="color: #CBD5E1;">Required next step:</strong>
                All DGA-based assessments should be reviewed by a qualified transformer engineer.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # ── Charts Row ───────────────────────────────────────────────────────
    col_chart1, col_chart2 = st.columns(2)

    # ── Probability Chart ────────────────────────────────────────────────
    with col_chart1:
        st.markdown(
            '<div class="section-header">'
            + tooltip("📊 Class Probability Estimates", TOOLTIPS["model_probability"])
            + '</div>',
            unsafe_allow_html=True,
        )

        if result.probabilities:
            sorted_probs = sorted(
                result.probabilities.items(),
                key=lambda x: x[1],
                reverse=False,
            )
            classes = [c for c, _ in sorted_probs]
            probs = [p for _, p in sorted_probs]

            colors = []
            for c in classes:
                if c == result.predicted_class:
                    colors.append("#00D4FF")
                else:
                    cat = CLASS_DESCRIPTIONS.get(c, {}).get("category", "")
                    if cat == "Electrical":
                        colors.append("#3B82F6")
                    else:
                        colors.append("#F59E0B")

            fig_prob = go.Figure(go.Bar(
                y=classes,
                x=probs,
                orientation="h",
                marker_color=colors,
                text=[f"{p:.1%}" for p in probs],
                textposition="auto",
                textfont=dict(color="white", size=11),
            ))

            fig_prob.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#CBD5E1", size=11),
                margin=dict(l=0, r=20, t=10, b=30),
                height=300,
                xaxis=dict(
                    title="Estimated Probability",
                    range=[0, 1],
                    gridcolor="rgba(255,255,255,0.05)",
                    tickformat=".0%",
                ),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            )
            st.plotly_chart(fig_prob, use_container_width=True)

            st.markdown("""
            <div class="disclaimer" style="font-size: 0.72rem;">
                These are model-estimated probabilities from the Random Forest,
                not calibrated diagnostic certainties. The model has not been
                assessed for probability calibration.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Probability estimates are not available for this prediction.")

    # ── Gas Profile Chart ────────────────────────────────────────────────
    with col_chart2:
        st.markdown('<div class="section-header">🧪 Gas Concentration Profile</div>',
                    unsafe_allow_html=True)

        gas_names = [FEATURE_FORMULAS[g] for g in FEATURE_NAMES]
        gas_vals = [float(result.gas_values_input.get(g, 0)) for g in FEATURE_NAMES]

        fig_gas = go.Figure(go.Bar(
            x=gas_names,
            y=gas_vals,
            marker_color=["#06B6D4", "#0EA5E9", "#3B82F6", "#8B5CF6", "#EC4899"],
            text=[f"{v:,.1f}" for v in gas_vals],
            textposition="auto",
            textfont=dict(color="white", size=11),
        ))

        fig_gas.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=11),
            margin=dict(l=0, r=20, t=10, b=30),
            height=300,
            yaxis=dict(
                title=f"Concentration ({result.input_unit})",
                gridcolor="rgba(255,255,255,0.05)",
            ),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(fig_gas, use_container_width=True)

        # Log scale option
        show_log = st.checkbox(
            "Show logarithmic scale",
            help="Useful when gas concentrations differ greatly in magnitude. "
                 "Zero values are replaced with a small positive value for display.",
        )
        if show_log:
            log_vals = [max(v, 0.01) for v in gas_vals]  # Handle zeros
            fig_log = go.Figure(go.Bar(
                x=gas_names,
                y=log_vals,
                marker_color=["#06B6D4", "#0EA5E9", "#3B82F6", "#8B5CF6", "#EC4899"],
                text=[f"{v:,.1f}" for v in gas_vals],
                textposition="auto",
                textfont=dict(color="white", size=10),
            ))
            fig_log.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#CBD5E1", size=11),
                margin=dict(l=0, r=20, t=10, b=30),
                height=280,
                yaxis=dict(
                    title=f"Log Concentration ({result.input_unit})",
                    type="log",
                    gridcolor="rgba(255,255,255,0.05)",
                ),
            )
            st.plotly_chart(fig_log, use_container_width=True)
            st.markdown(
                '<p style="font-size: 0.72rem; color: #64748B;">'
                'Zero values are shown as 0.01 on the log scale for display purposes.</p>',
                unsafe_allow_html=True,
            )

    # ── Classical Engineering Cross-Verification: Duval Triangle 1 ───────
    st.markdown(
        '<div class="section-header">'
        + tooltip("🔺 Classical Engineering Cross-Verification: Duval Triangle 1",
                  "IEEE C57.104 and IEC 60599 classical diagnostic method based on %CH4, %C2H4, and %C2H2.")
        + '</div>',
        unsafe_allow_html=True,
    )

    ch4_val = float(result.gas_values_input.get("CH4", 0))
    c2h4_val = float(result.gas_values_input.get("C2H4", 0))
    c2h2_val = float(result.gas_values_input.get("C2H2", 0))
    duval_res = calculate_duval_triangle_1(ch4_val, c2h4_val, c2h2_val)

    col_duval1, col_duval2 = st.columns([1.2, 1])

    with col_duval1:
        if duval_res["valid"]:
            fig_duval = go.Figure()

            fig_duval.add_trace(go.Scatterternary(
                a=[duval_res["pct_ch4"]],
                b=[duval_res["pct_c2h4"]],
                c=[duval_res["pct_c2h2"]],
                mode="markers+text",
                marker=dict(symbol="star", size=18, color="#00D4FF", line=dict(color="#FFFFFF", width=2)),
                text=[f"📍 {result.transformer_label or 'Unit'}"],
                textposition="top center",
                name="Current Transformer",
            ))

            fig_duval.update_layout(
                ternary=dict(
                    sum=100,
                    aaxis=dict(title="% CH₄ (Methane)", gridcolor="rgba(52,211,153,0.3)", color="#34D399", min=0.01),
                    baxis=dict(title="% C₂H₄ (Ethylene)", gridcolor="rgba(248,113,113,0.3)", color="#F87171", min=0.01),
                    caxis=dict(title="% C₂H₂ (Acetylene)", gridcolor="rgba(192,132,252,0.3)", color="#C084FC", min=0.01),
                    bgcolor="rgba(15,23,42,0.95)",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#CBD5E1", size=11),
                margin=dict(l=10, r=10, t=20, b=20),
                height=340,
                showlegend=False,
            )
            st.plotly_chart(fig_duval, use_container_width=True)
        else:
            st.info("Insufficient hydrocarbon concentrations to plot Duval Triangle 1.")

    with col_duval2:
        match_status = "Direct Agreement" if duval_res.get("zone") == result.predicted_class else "Complementary Finding"
        status_color = "#10B981" if duval_res.get("zone") == result.predicted_class else "#F59E0B"

        st.markdown(f"""
        <div class="dga-card" style="border-left: 4px solid {status_color}; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                <span style="font-size: 0.8rem; text-transform: uppercase; color: #94A3B8; font-weight: 600;">Method Comparison</span>
                <span style="background: rgba(255,255,255,0.05); border: 1px solid {status_color}; color: {status_color}; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; font-weight: 600;">{match_status}</span>
            </div>
            <div style="margin-bottom: 0.8rem;">
                <p style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 0.2rem;">Machine Learning Model (Random Forest):</p>
                <p style="font-size: 1.1rem; color: #00D4FF; font-weight: 700; margin: 0;">{result.predicted_class} — {result.class_description.get('name', '')}</p>
            </div>
            <div style="margin-bottom: 0.8rem;">
                <p style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 0.2rem;">Classical Duval Triangle 1 Zone:</p>
                <p style="font-size: 1.1rem; color: #CBD5E1; font-weight: 700; margin: 0;">{duval_res.get('zone', 'N/A')} — {duval_res.get('zone_name', '')}</p>
            </div>
            <div style="font-size: 0.78rem; color: #64748B; line-height: 1.5; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 0.6rem;">
                Coordinates: <strong>%CH₄: {duval_res['pct_ch4']}%</strong> | <strong>%C₂H₄: {duval_res['pct_c2h4']}%</strong> | <strong>%C₂H₂: {duval_res['pct_c2h2']}%</strong><br/>
                <em>Note: While Duval Triangle 1 evaluates 3 gases, the PRML Random Forest model incorporates all 5 key gases (including H₂ and C₂H₆) capturing subtle early discharge and degradation patterns.</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Gas Readings Table ───────────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Input Summary</div>',
                unsafe_allow_html=True)

    table_html = """
    <div class="dga-card">
        <table class="styled-table">
            <thead><tr>
                <th>Gas</th><th>Formula</th>
                <th style="text-align: right;">Input Value</th>
                <th style="text-align: right;">Unit</th>
            </tr></thead><tbody>
    """
    for gas in FEATURE_NAMES:
        val = result.gas_values_input.get(gas, 0)
        table_html += f"""
        <tr>
            <td>{FEATURE_LABELS[gas].split(' — ')[1]}</td>
            <td>{FEATURE_FORMULAS[gas]}</td>
            <td style="text-align: right;">{float(val):,.2f}</td>
            <td style="text-align: right;">{result.input_unit}</td>
        </tr>
        """
    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

    # ── Feature Importance Context ───────────────────────────────────────
    st.markdown(
        '<div class="section-header">'
        + tooltip("🎯 Global Feature Importance Context", TOOLTIPS["feature_importance"])
        + '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="info-box">
        <strong>Note:</strong> The chart below shows <em>global</em> permutation
        importance from the grouped cross-validation — how much the model relies
        on each gas feature overall. It does <strong>not</strong> explain why
        this particular prediction was made. A gas with high global importance
        may not have been the dominant factor for this specific input.
    </div>
    """, unsafe_allow_html=True)

    imp_gases = [FEATURE_FORMULAS.get(p["Gas"], p["Gas"]) for p in PERMUTATION_IMPORTANCE]
    imp_vals = [p["Mean_Importance"] for p in PERMUTATION_IMPORTANCE]

    fig_imp = go.Figure(go.Bar(
        y=imp_gases,
        x=imp_vals,
        orientation="h",
        marker_color="#14B8A6",
        text=[f"{v:.4f}" for v in imp_vals],
        textposition="auto",
        textfont=dict(color="white", size=11),
    ))
    fig_imp.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", size=11),
        margin=dict(l=0, r=20, t=10, b=30),
        height=250,
        xaxis=dict(title="Mean Macro-F1 Decrease", gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
    )
    st.plotly_chart(fig_imp, use_container_width=True)

    # ── Warnings ─────────────────────────────────────────────────────────
    if result.warnings:
        st.markdown('<div class="section-header">⚠️ Warnings</div>',
                    unsafe_allow_html=True)
        for warning in result.warnings:
            st.markdown(
                f'<div class="warning-box">⚠️ {warning}</div>',
                unsafe_allow_html=True,
            )

    # ── Disclaimer ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="disclaimer">
        <strong>Experimental Use Only:</strong> This prediction is generated by an
        experimental Random Forest classifier. It is not a certified transformer
        condition assessment or a substitute for professional engineering judgement.
        All results should be reviewed by a qualified transformer engineer.
    </div>
    """, unsafe_allow_html=True)

    # ── Action Buttons ───────────────────────────────────────────────────
    st.markdown('<div class="section-header">📥 Actions</div>',
                unsafe_allow_html=True)

    col_d1, col_d2, col_d3, col_d4 = st.columns(4)

    with col_d1:
        try:
            pdf_bytes = generate_pdf_report(result)
            st.download_button(
                "📄 Download PDF Report",
                data=pdf_bytes,
                file_name=f"DGA_Report_{result.reference_id}.pdf",
                mime="application/pdf",
                use_container_width=True,
                help=TOOLTIPS["download_pdf"],
            )
        except Exception as e:
            st.error(f"PDF generation error: {e}")

    with col_d2:
        try:
            csv_content = generate_csv_report(result)
            st.download_button(
                "📊 Download CSV Result",
                data=csv_content,
                file_name=f"DGA_Result_{result.reference_id}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"CSV generation error: {e}")

    with col_d3:
        if st.button("🔬 Analyse Another", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.last_result = None
            st.rerun()

    with col_d4:
        if st.button("📊 Return to Dashboard", use_container_width=True):
            st.session_state.show_results = False
            st.rerun()
