"""
About the Project page.
"""

import streamlit as st


def render_about():
    """Render the About the Project page."""

    st.markdown('<div class="page-title">ℹ️ About the Project</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        'Background, methodology, and credits for the Transformer DGA '
        'Intelligence platform.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Project Overview ─────────────────────────────────────────────────
    st.markdown("""
    <div class="dga-card">
        <p style="color: #00D4FF; font-weight: 600; font-size: 1rem; margin-bottom: 0.5rem;">
            Transformer DGA Intelligence
        </p>
        <p style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.7;">
            This application was developed as part of a Pattern Recognition
            and Machine Learning (PRML) project at IIT Tirupati. It applies
            supervised classification techniques to dissolved gas analysis
            (DGA) data from power transformers, with the goal of
            experimentally predicting fault categories from five gas
            concentration measurements.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Methodology ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🔬 Methodology</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card">
        <ol style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.8; padding-left: 1.2rem;">
            <li><strong style="color: #00D4FF;">Data Collection:</strong>
                The dataset (IEEE_STANDARD.xlsx) contains 589 records with
                five gas features and six fault labels. After removing 2
                exact duplicate rows, 587 unique records remain.</li>
            <li><strong style="color: #00D4FF;">Exploratory Data Analysis:</strong>
                Gas distributions, class balance, correlations, and data
                quality were assessed.</li>
            <li><strong style="color: #00D4FF;">Model Development:</strong>
                Five classifiers were trained and compared — Gaussian Naive
                Bayes, Logistic Regression, SVM (initial and tuned), and
                Random Forest.</li>
            <li><strong style="color: #00D4FF;">Evaluation:</strong>
                All models were evaluated on the same 20% stratified holdout
                test set. The Random Forest was further assessed using grouped
                5-fold cross-validation with permutation importance.</li>
            <li><strong style="color: #00D4FF;">Deployment:</strong>
                The best model (Random Forest, 75.42% holdout accuracy) was
                saved and integrated into this Streamlit web application.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # ── Technology Stack ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">🛠️ Technology Stack</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="dga-card">
            <p style="color: #00D4FF; font-weight: 600; margin-bottom: 0.5rem;">
                Machine Learning
            </p>
            <ul style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.7; padding-left: 1rem;">
                <li>Python 3.14</li>
                <li>scikit-learn — model training and evaluation</li>
                <li>pandas — data manipulation</li>
                <li>NumPy — numerical computing</li>
                <li>joblib — model serialisation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="dga-card">
            <p style="color: #00D4FF; font-weight: 600; margin-bottom: 0.5rem;">
                Web Application
            </p>
            <ul style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.7; padding-left: 1rem;">
                <li>Streamlit — interactive web framework</li>
                <li>Plotly — interactive visualisations</li>
                <li>FPDF2 — PDF report generation</li>
                <li>Custom CSS — premium UI theming</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Dataset ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📚 Dataset</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card">
        <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.7;">
            The dataset used in this project is sourced from an IEEE standard
            DGA dataset. It contains dissolved gas measurements from power
            transformers with six labelled fault categories: PD (Partial
            Discharge), D1 (Low-Energy Discharge), D2 (High-Energy Discharge),
            T1 (Thermal < 300°C), T2 (Thermal 300–700°C), and T3
            (Thermal > 700°C).
        </p>
        <p style="color: #94A3B8; font-size: 0.82rem; line-height: 1.6; margin-top: 0.5rem;">
            <strong>Note:</strong> The dataset contains some repeated gas
            measurement vectors with conflicting fault labels. This ambiguity
            was retained as received and is documented as a methodological
            limitation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Credits ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">👨‍💻 Credits</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card" style="text-align: center;">
        <p style="color: #00D4FF; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.3rem;">
            Mourya Abbadasari
        </p>
        <p style="color: #94A3B8; font-size: 0.88rem;">
            Electrical Engineering, IIT Tirupati
        </p>
        <p style="color: #64748B; font-size: 0.78rem; margin-top: 0.8rem;">
            This project was developed as an academic exercise in applying
            pattern recognition and machine learning techniques to power
            system diagnostics.
        </p>
    </div>
    """, unsafe_allow_html=True)
