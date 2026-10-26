"""
Gas Data Visualisation page.

Interactive charts for exploring the training dataset distributions.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os

from config.settings import (
    FEATURE_NAMES,
    FEATURE_FORMULAS,
    FEATURE_LABELS,
    CLASS_LABELS,
    DATASET_PATH,
    TOOLTIPS,
)
from utils.ui import tooltip


@st.cache_data
def load_dataset():
    """Load and preprocess the dataset for visualisation."""
    df = pd.read_excel(DATASET_PATH)
    df = df.rename(columns={"故障类型": "Fault Type"})
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def render_visualisation():
    """Render the gas data visualisation page."""

    st.markdown('<div class="page-title">📈 Gas Data Visualisation</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        'Interactive visualisations of the training dataset gas distributions '
        'and class-wise patterns.'
        '</div>',
        unsafe_allow_html=True,
    )

    try:
        df = load_dataset()
    except Exception as e:
        st.error(f"Could not load dataset: {e}")
        return

    # ── Dataset Summary ──────────────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Dataset Summary</div>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Samples</div>
            <div class="metric-value">{len(df)}</div>
            <div style="font-size: 0.68rem; color: #64748B;">After deduplication</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Features</div>
            <div class="metric-value">5</div>
            <div style="font-size: 0.68rem; color: #64748B;">Gas concentrations</div>
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

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Class Distribution ───────────────────────────────────────────────
    st.markdown('<div class="section-header">🏷️ Fault Class Distribution</div>',
                unsafe_allow_html=True)

    class_counts = df["Fault Type"].value_counts().sort_index()
    colors_map = {
        "PD": "#06B6D4", "D1": "#3B82F6", "D2": "#8B5CF6",
        "T1": "#F59E0B", "T2": "#EF4444", "T3": "#EC4899",
    }

    fig_dist = go.Figure(go.Bar(
        x=class_counts.index.tolist(),
        y=class_counts.values.tolist(),
        marker_color=[colors_map.get(c, "#0EA5E9") for c in class_counts.index],
        text=class_counts.values.tolist(),
        textposition="auto",
        textfont=dict(color="white", size=12),
    ))
    fig_dist.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", size=11),
        margin=dict(l=0, r=20, t=10, b=30),
        height=300,
        yaxis=dict(title="Count", gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(title="Fault Class"),
    )
    st.plotly_chart(fig_dist, use_container_width=True)

    # ── Gas Distributions ────────────────────────────────────────────────
    st.markdown('<div class="section-header">📊 Gas Concentration Distributions</div>',
                unsafe_allow_html=True)

    gas_select = st.selectbox(
        "Select gas to visualise",
        FEATURE_NAMES,
        format_func=lambda g: FEATURE_LABELS[g],
        help="Choose a gas feature to see its distribution across fault classes.",
    )

    col_box, col_hist = st.columns(2)

    with col_box:
        fig_box = px.box(
            df,
            x="Fault Type",
            y=gas_select,
            color="Fault Type",
            color_discrete_map=colors_map,
            category_orders={"Fault Type": CLASS_LABELS},
        )
        fig_box.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=11),
            margin=dict(l=0, r=20, t=10, b=30),
            height=350,
            showlegend=False,
            yaxis=dict(
                title=f"{FEATURE_FORMULAS[gas_select]} (ppm)",
                gridcolor="rgba(255,255,255,0.05)",
            ),
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col_hist:
        fig_hist = px.histogram(
            df,
            x=gas_select,
            color="Fault Type",
            color_discrete_map=colors_map,
            nbins=30,
            opacity=0.7,
            barmode="overlay",
            category_orders={"Fault Type": CLASS_LABELS},
        )
        fig_hist.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=11),
            margin=dict(l=0, r=20, t=10, b=30),
            height=350,
            xaxis=dict(
                title=f"{FEATURE_FORMULAS[gas_select]} (ppm)",
                gridcolor="rgba(255,255,255,0.05)",
            ),
            yaxis=dict(title="Count", gridcolor="rgba(255,255,255,0.05)"),
            legend=dict(
                orientation="h", yanchor="bottom", y=-0.3,
                xanchor="center", x=0.5,
            ),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # ── Correlation Heatmap ──────────────────────────────────────────────
    st.markdown('<div class="section-header">🔗 Gas Feature Correlation</div>',
                unsafe_allow_html=True)

    corr = df[FEATURE_NAMES].corr()
    gas_labels = [FEATURE_FORMULAS[g] for g in FEATURE_NAMES]

    fig_corr = px.imshow(
        corr.values,
        x=gas_labels,
        y=gas_labels,
        text_auto=".2f",
        color_continuous_scale=[
            [0, "#0A0E1A"],
            [0.5, "#0EA5E9"],
            [1, "#00D4FF"],
        ],
        zmin=-1, zmax=1,
    )
    fig_corr.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", size=11),
        margin=dict(l=0, r=20, t=10, b=30),
        height=400,
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    # ── Gas Statistics Table ─────────────────────────────────────────────
    st.markdown('<div class="section-header">📊 Gas Concentration Statistics</div>',
                unsafe_allow_html=True)

    stats = df[FEATURE_NAMES].describe().round(2)

    table_html = """
    <div class="dga-card">
        <table class="styled-table">
            <thead><tr><th>Statistic</th>
    """
    for gas in FEATURE_NAMES:
        table_html += f"<th style='text-align: right;'>{FEATURE_FORMULAS[gas]}</th>"
    table_html += "</tr></thead><tbody>"

    for stat_name in ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]:
        table_html += f"<tr><td style='font-weight: 500;'>{stat_name}</td>"
        for gas in FEATURE_NAMES:
            val = stats.loc[stat_name, gas]
            table_html += f"<td style='text-align: right;'>{val:,.2f}</td>"
        table_html += "</tr>"

    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)
