"""
New DGA Analysis page — single transformer input and batch fleet analysis.
"""

import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from config.settings import (
    FEATURE_NAMES,
    FEATURE_LABELS,
    FEATURE_FORMULAS,
    CLASS_DESCRIPTIONS,
    TOOLTIPS,
    DEMO_SAMPLES,
)
from backend.prediction import predict_transformer_fault
from backend.duval import calculate_duval_triangle_1
from backend.unit_conversion import SUPPORTED_UNITS
from utils.ui import tooltip


def render_analysis():
    """Render the gas input form and batch fleet analysis interface."""

    st.markdown('<div class="page-title">🔬 New DGA Analysis</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        'Enter single transformer dissolved gas measurements or upload a multi-transformer batch spreadsheet for automated fleet fault screening.'
        '</div>',
        unsafe_allow_html=True,
    )

    tab_single, tab_batch = st.tabs([
        "🧪 Single Transformer Analysis",
        "📁 Batch Fleet Analysis (Excel / CSV)",
    ])

    # =========================================================================
    # TAB 1: Single Transformer Analysis
    # =========================================================================
    with tab_single:
        # Instructions
        st.markdown("""
        <div class="info-box">
            <strong>Instructions:</strong> Enter the five gas concentration values
            from your laboratory DGA report. All values must be in
            <strong>ppm (parts per million)</strong>, matching the unit used in the
            training dataset. The model expects exactly five gases in the order
            shown below. Do not leave any field empty.
        </div>
        """, unsafe_allow_html=True)

        # Unit selector
        st.markdown(
            '<div class="section-header">'
            + tooltip("📐 Concentration Unit", TOOLTIPS["concentration_unit"])
            + '</div>',
            unsafe_allow_html=True,
        )

        unit = st.selectbox(
            "Select concentration unit",
            SUPPORTED_UNITS,
            index=0,
            help=TOOLTIPS["concentration_unit"],
            label_visibility="collapsed",
            key="single_unit_select",
        )

        # Demo sample loader
        st.markdown('<div class="section-header">📋 Load Demonstration Example</div>',
                    unsafe_allow_html=True)

        if "last_demo_choice" not in st.session_state:
            st.session_state.last_demo_choice = "(None — enter your own values)"

        # Initialize input values if not present
        for gas in FEATURE_NAMES:
            if f"input_{gas}" not in st.session_state:
                st.session_state[f"input_{gas}"] = 0.0

        demo_options = ["(None — enter your own values)"] + list(DEMO_SAMPLES.keys())
        demo_idx = demo_options.index(st.session_state.last_demo_choice) if st.session_state.last_demo_choice in demo_options else 0

        demo_choice = st.selectbox(
            "Select a demonstration sample",
            demo_options,
            index=demo_idx,
            help="Fill the gas fields with illustrative sample values for testing.",
            label_visibility="collapsed",
            key="demo_sample_select",
        )

        # Set demo values in session state
        if demo_choice != st.session_state.last_demo_choice:
            st.session_state.last_demo_choice = demo_choice
            if demo_choice != "(None — enter your own values)":
                demo = DEMO_SAMPLES[demo_choice]
                for gas in FEATURE_NAMES:
                    st.session_state[f"input_{gas}"] = float(demo[gas])
            else:
                for gas in FEATURE_NAMES:
                    st.session_state[f"input_{gas}"] = 0.0
            st.rerun()

        if st.session_state.last_demo_choice != "(None — enter your own values)":
            demo = DEMO_SAMPLES.get(st.session_state.last_demo_choice, {})
            st.markdown(f"""
            <div class="info-box" style="border-color: rgba(20, 184, 166, 0.3);">
                <strong>Demo loaded ({st.session_state.last_demo_choice}):</strong> {demo.get('description', '')}
            </div>
            """, unsafe_allow_html=True)

        # Gas input form
        st.markdown(
            '<div class="section-header">'
            + tooltip(
                "🧪 Enter Transformer Dissolved Gas Measurements",
                "Enter five gas concentrations from your DGA laboratory report. "
                "All values should be non-negative numbers in the selected unit.",
            )
            + '</div>',
            unsafe_allow_html=True,
        )

        # Create input fields
        gas_values = {}

        # First row: H2, CH4, C2H6
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                tooltip(
                    f"**{FEATURE_FORMULAS['H2']} — Hydrogen**",
                    TOOLTIPS["H2"],
                ),
                unsafe_allow_html=True,
            )
            gas_values["H2"] = st.number_input(
                f"H₂ ({unit})",
                min_value=0.0,
                step=1.0,
                format="%.2f",
                key="input_H2",
                help=TOOLTIPS["H2"],
                label_visibility="collapsed",
            )

        with col2:
            st.markdown(
                tooltip(
                    f"**{FEATURE_FORMULAS['CH4']} — Methane**",
                    TOOLTIPS["CH4"],
                ),
                unsafe_allow_html=True,
            )
            gas_values["CH4"] = st.number_input(
                f"CH₄ ({unit})",
                min_value=0.0,
                step=1.0,
                format="%.2f",
                key="input_CH4",
                help=TOOLTIPS["CH4"],
                label_visibility="collapsed",
            )

        with col3:
            st.markdown(
                tooltip(
                    f"**{FEATURE_FORMULAS['C2H6']} — Ethane**",
                    TOOLTIPS["C2H6"],
                ),
                unsafe_allow_html=True,
            )
            gas_values["C2H6"] = st.number_input(
                f"C₂H₆ ({unit})",
                min_value=0.0,
                step=1.0,
                format="%.2f",
                key="input_C2H6",
                help=TOOLTIPS["C2H6"],
                label_visibility="collapsed",
            )

        # Second row: C2H4, C2H2, Transformer Label
        col4, col5, col6 = st.columns(3)

        with col4:
            st.markdown(
                tooltip(
                    f"**{FEATURE_FORMULAS['C2H4']} — Ethylene**",
                    TOOLTIPS["C2H4"],
                ),
                unsafe_allow_html=True,
            )
            gas_values["C2H4"] = st.number_input(
                f"C₂H₄ ({unit})",
                min_value=0.0,
                step=1.0,
                format="%.2f",
                key="input_C2H4",
                help=TOOLTIPS["C2H4"],
                label_visibility="collapsed",
            )

        with col5:
            st.markdown(
                tooltip(
                    f"**{FEATURE_FORMULAS['C2H2']} — Acetylene**",
                    TOOLTIPS["C2H2"],
                ),
                unsafe_allow_html=True,
            )
            gas_values["C2H2"] = st.number_input(
                f"C₂H₂ ({unit})",
                min_value=0.0,
                step=1.0,
                format="%.2f",
                key="input_C2H2",
                help=TOOLTIPS["C2H2"],
                label_visibility="collapsed",
            )

        with col6:
            st.markdown("**Transformer Label** (optional)", unsafe_allow_html=True)
            tx_label = st.text_input(
                "Transformer label",
                value=st.session_state.get("transformer_label", ""),
                placeholder="e.g. TX-2024-A",
                label_visibility="collapsed",
                key="single_tx_label",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Action button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            analyse_clicked = st.button(
                "⚡ Analyse Transformer",
                use_container_width=True,
                type="primary",
                help=TOOLTIPS["analyse_button"],
                key="btn_analyse_single",
            )

        if analyse_clicked:
            all_zero = all(v == 0.0 for v in gas_values.values())
            if all_zero:
                st.error(
                    "⚠️ All gas values are zero. Please enter at least one "
                    "non-zero gas concentration from your laboratory report."
                )
                return

            with st.spinner("Running analysis..."):
                result = predict_transformer_fault(
                    gas_values=gas_values,
                    unit=unit,
                    transformer_label=tx_label,
                    user_name=st.session_state.get("user_name", ""),
                )

            if not result.success:
                st.markdown('<div class="section-header" style="color: #EF4444;">❌ Analysis Failed</div>',
                            unsafe_allow_html=True)
                for error in result.errors:
                    st.markdown(f'<div class="error-box">⚠️ {error}</div>',
                                unsafe_allow_html=True)
                return

            st.session_state.last_result = result
            st.session_state.show_results = True

            history_entry = {
                "reference_id": result.reference_id,
                "timestamp": result.timestamp,
                "predicted_class": result.predicted_class,
                "transformer_label": result.transformer_label,
                "gas_values": dict(result.gas_values_input),
            }
            st.session_state.analysis_history.append(history_entry)
            st.rerun()

    # =========================================================================
    # TAB 2: Batch Fleet Analysis
    # =========================================================================
    with tab_batch:
        st.markdown('<div class="section-header">📁 Fleet DGA Batch Screening</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.6;">
            Upload an Excel (<code>.xlsx</code>) or CSV (<code>.csv</code>) file with multiple transformer DGA laboratory records.
            The machine learning model will screen all units, calculate probability distributions, cross-verify against Duval Triangle 1,
            and generate a consolidated fleet risk report.
        </p>
        """, unsafe_allow_html=True)

        # Template Download
        sample_df = pd.DataFrame([
            {"Transformer_ID": "TX-Substation-01", "H2": 120.0, "CH4": 250.0, "C2H6": 85.0, "C2H4": 410.0, "C2H2": 5.0, "Substation": "North Grid", "Rating_MVA": 100},
            {"Transformer_ID": "TX-Substation-02", "H2": 350.0, "CH4": 45.0, "C2H6": 12.0, "C2H4": 30.0, "C2H2": 180.0, "Substation": "South Grid", "Rating_MVA": 160},
            {"Transformer_ID": "TX-Substation-03", "H2": 890.0, "CH4": 15.0, "C2H6": 8.0, "C2H4": 5.0, "C2H2": 3.0, "Substation": "East Yard", "Rating_MVA": 50},
            {"Transformer_ID": "TX-Substation-04", "H2": 45.0, "CH4": 25.0, "C2H6": 15.0, "C2H4": 10.0, "C2H2": 1.0, "Substation": "West Plant", "Rating_MVA": 25},
            {"Transformer_ID": "TX-Substation-05", "H2": 310.0, "CH4": 620.0, "C2H6": 450.0, "C2H4": 890.0, "C2H2": 14.0, "Substation": "Industrial Feeder", "Rating_MVA": 200},
        ])
        csv_template = sample_df.to_csv(index=False)

        col_t1, col_t2 = st.columns([1, 2])
        with col_t1:
            st.download_button(
                "📥 Download CSV Batch Template",
                data=csv_template,
                file_name="dga_batch_fleet_template.csv",
                mime="text/csv",
                help="Download sample CSV template with pre-filled gas columns",
                use_container_width=True,
            )

        # File uploader
        uploaded_file = st.file_uploader(
            "Upload Fleet DGA Data File (CSV or Excel)",
            type=["csv", "xlsx", "xls"],
            help="File must contain columns: H2, CH4, C2H6, C2H4, C2H2 in ppm.",
        )

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df_upload = pd.read_csv(uploaded_file)
                else:
                    df_upload = pd.read_excel(uploaded_file)

                st.success(f"Successfully loaded {len(df_upload)} records from `{uploaded_file.name}`")

                # Column name matching (case-insensitive)
                col_map = {str(c).strip().upper(): c for c in df_upload.columns}
                missing_cols = [g for g in FEATURE_NAMES if g not in col_map]

                if missing_cols:
                    st.error(f"Missing required gas columns: {', '.join(missing_cols)}. File must contain H2, CH4, C2H6, C2H4, C2H2.")
                else:
                    id_col = col_map.get("TRANSFORMER_ID") or col_map.get("TRANSFORMER ID") or col_map.get("ID") or col_map.get("UNIT")

                    results_list = []
                    for idx, row in df_upload.iterrows():
                        tx_name = str(row[id_col]) if id_col else f"Unit-{idx+1:03d}"
                        g_vals = {g: float(row[col_map[g]]) if pd.notnull(row[col_map[g]]) else 0.0 for g in FEATURE_NAMES}

                        pred_res = predict_transformer_fault(g_vals, unit="ppm", transformer_label=tx_name)
                        duval_res = calculate_duval_triangle_1(g_vals["CH4"], g_vals["C2H4"], g_vals["C2H2"])

                        top_prob = 0.0
                        if pred_res.probabilities and pred_res.predicted_class in pred_res.probabilities:
                            top_prob = pred_res.probabilities[pred_res.predicted_class]

                        risk_level = "Low"
                        if pred_res.predicted_class in ["D2", "T3"]:
                            risk_level = "Critical"
                        elif pred_res.predicted_class in ["D1", "T2"]:
                            risk_level = "Medium"

                        results_list.append({
                            "Transformer_ID": tx_name,
                            "Predicted_Class": pred_res.predicted_class,
                            "Class_Name": pred_res.class_description.get("name", ""),
                            "Category": pred_res.class_description.get("category", "General"),
                            "Confidence": f"{top_prob:.1%}",
                            "Duval_Zone": duval_res.get("zone", "N/A"),
                            "Risk_Level": risk_level,
                            "H2": g_vals["H2"],
                            "CH4": g_vals["CH4"],
                            "C2H6": g_vals["C2H6"],
                            "C2H4": g_vals["C2H4"],
                            "C2H2": g_vals["C2H2"],
                        })

                    res_df = pd.DataFrame(results_list)

                    # ── Fleet KPI Summary Cards ──
                    st.markdown('<div class="section-header">📊 Fleet Health Overview</div>', unsafe_allow_html=True)
                    m1, m2, m3, m4 = st.columns(4)
                    with m1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">Total Units Tested</div>
                            <div class="metric-value">{len(res_df)}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with m2:
                        crit_cnt = len(res_df[res_df["Risk_Level"] == "Critical"])
                        st.markdown(f"""
                        <div class="metric-card" style="border-color: rgba(239, 68, 68, 0.4);">
                            <div class="metric-label">Critical Alerts (D2/T3)</div>
                            <div class="metric-value" style="color: #EF4444;">{crit_cnt}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with m3:
                        med_cnt = len(res_df[res_df["Risk_Level"] == "Medium"])
                        st.markdown(f"""
                        <div class="metric-card" style="border-color: rgba(245, 158, 11, 0.4);">
                            <div class="metric-label">Moderate Alerts (D1/T2)</div>
                            <div class="metric-value" style="color: #F59E0B;">{med_cnt}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with m4:
                        low_cnt = len(res_df[res_df["Risk_Level"] == "Low"])
                        st.markdown(f"""
                        <div class="metric-card" style="border-color: rgba(16, 185, 129, 0.4);">
                            <div class="metric-label">Low Risk / PD (T1/PD)</div>
                            <div class="metric-value" style="color: #10B981;">{low_cnt}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # ── Chart & Table ──
                    col_chart, col_empty = st.columns([1, 1])
                    with col_chart:
                        class_counts = res_df["Predicted_Class"].value_counts().reset_index()
                        class_counts.columns = ["Class", "Count"]
                        fig_donut = px.pie(
                            class_counts,
                            values="Count",
                            names="Class",
                            title="Fleet Fault Distribution Breakdown",
                            hole=0.45,
                            color_discrete_sequence=["#EF4444", "#F59E0B", "#10B981", "#3B82F6", "#8B5CF6", "#EC4899"],
                        )
                        fig_donut.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#CBD5E1"),
                            margin=dict(l=10, r=10, t=40, b=10),
                            height=280,
                        )
                        st.plotly_chart(fig_donut, use_container_width=True)

                    # ── Full Fleet Data Table ──
                    st.markdown('<div class="section-header">📋 Diagnostic Results Table</div>', unsafe_allow_html=True)
                    st.dataframe(res_df, use_container_width=True, height=280)

                    # ── Download Fleet Report ──
                    res_csv = res_df.to_csv(index=False)
                    st.download_button(
                        "📄 Download Complete Fleet Report (CSV)",
                        data=res_csv,
                        file_name=f"DGA_Fleet_Diagnostic_Report.csv",
                        mime="text/csv",
                        type="primary",
                    )

            except Exception as e:
                st.error(f"Error processing batch file: {e}")
