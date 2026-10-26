"""
Model Performance page.

Shows holdout comparison, RF classification report, confusion matrix,
and grouped cross-validation results.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from config.settings import (
    MODEL_COMPARISON,
    GROUPED_VALIDATION,
    TOOLTIPS,
    CLASS_LABELS,
)
from backend.model_loader import load_metadata
from utils.ui import tooltip


def render_model_performance():
    """Render the model performance page."""

    st.markdown('<div class="page-title">🏆 Model Performance</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        'Recorded evaluation metrics from the holdout test set and grouped '
        'cross-validation. All values are sourced from the original project results.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Model Comparison ─────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">'
        + tooltip("📊 Holdout Model Comparison", TOOLTIPS["accuracy"])
        + '</div>',
        unsafe_allow_html=True,
    )

    # Bar chart
    models = [m["Model"] for m in MODEL_COMPARISON]
    accuracies = [m["Accuracy"] for m in MODEL_COMPARISON]
    f1_scores = [m["Macro F1"] * 100 for m in MODEL_COMPARISON]

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name="Accuracy (%)",
        x=models,
        y=accuracies,
        marker_color="#0EA5E9",
        text=[f"{v:.1f}%" for v in accuracies],
        textposition="auto",
        textfont=dict(color="white", size=10),
    ))
    fig_comp.add_trace(go.Bar(
        name="Macro F1 (%)",
        x=models,
        y=f1_scores,
        marker_color="#14B8A6",
        text=[f"{v:.1f}%" for v in f1_scores],
        textposition="auto",
        textfont=dict(color="white", size=10),
    ))
    fig_comp.update_layout(
        barmode="group",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", size=11),
        margin=dict(l=0, r=20, t=10, b=80),
        height=380,
        yaxis=dict(
            title="Score (%)",
            gridcolor="rgba(255,255,255,0.05)",
            range=[0, 100],
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
        ),
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # Table
    st.markdown("""
    <div class="info-box" style="font-size: 0.78rem;">
        All models were evaluated on the same 20% holdout test set
        (random_state=42, stratified). The Random Forest was selected as
        the best model based on macro F1-score.
    </div>
    """, unsafe_allow_html=True)

    table_html = """
    <div class="dga-card">
        <table class="styled-table">
            <thead><tr>
                <th>Model</th>
                <th style="text-align: right;">Accuracy (%)</th>
                <th style="text-align: right;">Macro F1</th>
            </tr></thead><tbody>
    """
    for entry in MODEL_COMPARISON:
        is_best = entry["Model"] == "Random Forest"
        style = ' style="color: #00D4FF; font-weight: 600;"' if is_best else ""
        badge = " 🏆" if is_best else ""
        table_html += f"""
        <tr>
            <td{style}>{entry['Model']}{badge}</td>
            <td style="text-align: right;">{entry['Accuracy']:.2f}%</td>
            <td style="text-align: right;">{entry['Macro F1']:.4f}</td>
        </tr>
        """
    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

    # ── RF Classification Report ─────────────────────────────────────────
    st.markdown(
        '<div class="section-header">'
        + tooltip("📋 Random Forest — Per-Class Metrics (Holdout)", TOOLTIPS["f1_score"])
        + '</div>',
        unsafe_allow_html=True,
    )

    try:
        metadata = load_metadata()
        report = metadata.get("holdout_metrics", {}).get("classification_report", {})

        if report:
            report_html = """
            <div class="dga-card">
                <table class="styled-table">
                    <thead><tr>
                        <th>Class</th>
                        <th style="text-align: right;">Precision</th>
                        <th style="text-align: right;">Recall</th>
                        <th style="text-align: right;">F1-Score</th>
                        <th style="text-align: right;">Support</th>
                    </tr></thead><tbody>
            """
            for cls in CLASS_LABELS:
                if cls in report:
                    metrics = report[cls]
                    report_html += f"""
                    <tr>
                        <td style="font-weight: 600; color: #00D4FF;">{cls}</td>
                        <td style="text-align: right;">{metrics.get('precision', 0):.4f}</td>
                        <td style="text-align: right;">{metrics.get('recall', 0):.4f}</td>
                        <td style="text-align: right;">{metrics.get('f1-score', 0):.4f}</td>
                        <td style="text-align: right;">{int(metrics.get('support', 0))}</td>
                    </tr>
                    """
            report_html += "</tbody></table></div>"
            st.markdown(report_html, unsafe_allow_html=True)

            # Per-class bar chart
            class_names = []
            precisions = []
            recalls = []
            f1s = []
            for cls in CLASS_LABELS:
                if cls in report:
                    class_names.append(cls)
                    precisions.append(report[cls].get("precision", 0))
                    recalls.append(report[cls].get("recall", 0))
                    f1s.append(report[cls].get("f1-score", 0))

            if class_names:
                fig_cls = go.Figure()
                fig_cls.add_trace(go.Bar(
                    name="Precision", x=class_names, y=precisions,
                    marker_color="#3B82F6",
                ))
                fig_cls.add_trace(go.Bar(
                    name="Recall", x=class_names, y=recalls,
                    marker_color="#14B8A6",
                ))
                fig_cls.add_trace(go.Bar(
                    name="F1-Score", x=class_names, y=f1s,
                    marker_color="#F59E0B",
                ))
                fig_cls.update_layout(
                    barmode="group",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#CBD5E1", size=11),
                    margin=dict(l=0, r=20, t=10, b=60),
                    height=320,
                    yaxis=dict(
                        title="Score",
                        gridcolor="rgba(255,255,255,0.05)",
                        range=[0, 1],
                    ),
                    legend=dict(
                        orientation="h", yanchor="bottom", y=-0.22,
                        xanchor="center", x=0.5,
                    ),
                )
                st.plotly_chart(fig_cls, use_container_width=True)

    except Exception as e:
        st.warning(f"Could not load classification report: {e}")

    # ── Confusion Matrix ─────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">'
        + tooltip("🔲 Confusion Matrix (Holdout)", TOOLTIPS["confusion_matrix"])
        + '</div>',
        unsafe_allow_html=True,
    )

    try:
        metadata = load_metadata()
        cm = metadata.get("confusion_matrix")
        cm_labels = metadata.get("confusion_matrix_labels", CLASS_LABELS)

        if cm:
            cm_array = np.array(cm)
            fig_cm = px.imshow(
                cm_array,
                labels=dict(x="Predicted", y="Actual", color="Count"),
                x=cm_labels,
                y=cm_labels,
                text_auto=True,
                color_continuous_scale=[
                    [0, "#0A0E1A"],
                    [0.25, "#0E4D65"],
                    [0.5, "#0EA5E9"],
                    [0.75, "#06B6D4"],
                    [1, "#00D4FF"],
                ],
            )
            fig_cm.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#CBD5E1", size=11),
                margin=dict(l=0, r=20, t=10, b=30),
                height=400,
            )
            st.plotly_chart(fig_cm, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not load confusion matrix: {e}")

    # ── Grouped Cross-Validation ─────────────────────────────────────────
    st.markdown(
        '<div class="section-header">'
        + tooltip("📊 Grouped 5-Fold Cross-Validation", TOOLTIPS["grouped_cv"])
        + '</div>',
        unsafe_allow_html=True,
    )

    gv = GROUPED_VALIDATION
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Mean Accuracy</div>
            <div class="metric-value">{gv['mean_accuracy']*100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Accuracy Std Dev</div>
            <div class="metric-value">±{gv['accuracy_std']*100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Mean Macro F1</div>
            <div class="metric-value">{gv['mean_macro_f1']*100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">F1 Std Dev</div>
            <div class="metric-value">±{gv['macro_f1_std']*100:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <strong>About grouped cross-validation:</strong> Identical five-gas
        measurement vectors are kept in the same fold, reducing one form of
        repeated-input leakage. This provides a more realistic estimate of
        generalisation performance than standard cross-validation on this dataset.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card">
        <p style="color: #94A3B8; font-size: 0.82rem; line-height: 1.6;">
            <strong style="color: #E2E8F0;">Technical note:</strong>
            The pooled out-of-fold macro F1 and the mean fold macro F1 are
            different calculations. Pooled out-of-fold F1 collects all
            predictions across folds before computing the metric. Mean fold
            F1 computes the metric within each fold and then averages. These
            values may differ slightly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Dataset Limitations ──────────────────────────────────────────────
    st.markdown('<div class="section-header">⚠️ Dataset Methodology Notes</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-box">
        <strong>Conflicting repeated readings:</strong> The original dataset
        contains some identical five-gas measurement vectors that are assigned
        different fault labels. These represent a genuine ambiguity in the
        source data. They were not deleted or relabelled — they remain in the
        dataset as received. The grouped cross-validation addresses one aspect
        of this issue by ensuring identical readings stay in the same fold.
    </div>
    """, unsafe_allow_html=True)
