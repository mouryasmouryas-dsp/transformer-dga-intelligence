"""
Limitations and Safety page.
"""

import streamlit as st


def render_limitations():
    """Render the Limitations and Safety page."""

    st.markdown('<div class="page-title">⚠️ Limitations & Safety</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        'Important limitations, safety considerations, and responsible use '
        'guidelines for this experimental tool.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Model Limitations ────────────────────────────────────────────────
    st.markdown('<div class="section-header">🔬 Model Limitations</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card">
        <ul style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.8; padding-left: 1.2rem;">
            <li>The model is a <strong>Random Forest classifier</strong> trained
                on a specific historical dataset (587 samples after deduplication).
                It may not generalise to transformers with different designs,
                oil types, or operating conditions.</li>
            <li>The recorded holdout accuracy is <strong>75.42%</strong> and
                macro F1-score is <strong>0.7382</strong>. Approximately
                <strong>one in four predictions may be incorrect</strong>
                on data similar to the training set.</li>
            <li>The model has <strong>not been validated on independent field data</strong>
                from operational transformers.</li>
            <li>Class probability estimates from Random Forest are
                <strong>not calibrated</strong>. They should not be treated as
                reliable risk percentages.</li>
            <li>The model uses only <strong>five gas concentrations</strong>.
                It does not consider oil temperature, transformer age, load
                history, total dissolved gas, moisture, or other diagnostic
                parameters.</li>
            <li>The training dataset contains <strong>conflicting records</strong>
                — identical gas readings with different fault labels. This
                inherent ambiguity limits achievable accuracy.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── What the Model Cannot Do ─────────────────────────────────────────
    st.markdown('<div class="section-header">🚫 What This Tool Cannot Do</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-box" style="font-size: 0.88rem; line-height: 1.7;">
        <ul style="padding-left: 1.2rem; margin: 0;">
            <li>It <strong>cannot confirm</strong> the exact physical fault,
                its location, or its severity.</li>
            <li>It <strong>cannot estimate</strong> the remaining useful life
                of a transformer.</li>
            <li>It <strong>cannot replace</strong> professional transformer
                inspection, condition assessment, or engineering judgement.</li>
            <li>It <strong>cannot diagnose</strong> faults not represented in
                the six training categories.</li>
            <li>It <strong>cannot certify</strong> that a transformer is safe
                for continued operation.</li>
            <li>It <strong>should not be used</strong> as the sole basis for
                operational decisions such as de-energising, re-energising,
                or loading a transformer.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── Responsible Use ──────────────────────────────────────────────────
    st.markdown('<div class="section-header">✅ Responsible Use Guidelines</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card">
        <ol style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.8; padding-left: 1.2rem;">
            <li>Use this tool for <strong>exploratory screening and educational
                purposes</strong> only.</li>
            <li>Always have predictions <strong>reviewed by a qualified
                transformer engineer</strong> before taking any action.</li>
            <li>Combine DGA results with <strong>other diagnostic techniques</strong>
                — electrical tests, thermal imaging, visual inspection, oil
                quality analysis, and trend monitoring.</li>
            <li>Consider the <strong>transformer's history, age, loading
                pattern, and operating environment</strong> when interpreting
                results.</li>
            <li>Monitor <strong>gas trends over time</strong> rather than
                relying on a single measurement point.</li>
            <li>Report any <strong>unexpected or suspicious results</strong>
                to qualified engineering personnel.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    # ── Privacy ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🔒 Privacy & Data Handling</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card">
        <ul style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.8; padding-left: 1.2rem;">
            <li>This application <strong>does not transmit</strong> your gas
                readings or personal information to third-party services.</li>
            <li><strong>No account creation</strong> is required.</li>
            <li>Session data is <strong>temporary</strong> and is cleared when
                you close the browser or reset the session.</li>
            <li>Downloaded reports are generated <strong>locally</strong> and
                are not uploaded anywhere.</li>
            <li>The application does <strong>not store</strong> your data
                permanently unless you explicitly save a downloaded report.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── Disclaimer ───────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📜 Full Disclaimer</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card" style="border-color: rgba(239, 68, 68, 0.3);">
        <p style="color: #FCA5A5; font-size: 0.9rem; line-height: 1.7; font-weight: 500;">
            This application is an experimental academic tool. It records the
            output of a machine-learning classifier trained on a specific
            historical dataset. It is <strong>not</strong> a certified
            transformer condition assessment system, a replacement for
            professional engineering analysis, or an approved diagnostic
            instrument.
        </p>
        <p style="color: #94A3B8; font-size: 0.85rem; line-height: 1.7; margin-top: 0.8rem;">
            The developers of this application accept no liability for
            decisions made based on its output. All operational decisions
            regarding power transformers must be made by qualified
            professionals using appropriate engineering standards, procedures,
            and diagnostic instruments.
        </p>
    </div>
    """, unsafe_allow_html=True)
