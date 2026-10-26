"""
Analysis History page — session-only storage of past predictions.
"""

import streamlit as st


def render_history():
    """Render the analysis history page."""

    st.markdown('<div class="page-title">📋 Analysis History</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        'Session-only record of analyses performed during this session. '
        'Data is cleared when you close the browser or reset the session.'
        '</div>',
        unsafe_allow_html=True,
    )

    history = st.session_state.get("analysis_history", [])

    if not history:
        st.markdown("""
        <div class="dga-card" style="text-align: center; padding: 2rem;">
            <p style="font-size: 2rem; margin-bottom: 0.5rem;">📋</p>
            <p style="color: #94A3B8; font-size: 0.95rem;">
                No analyses performed in this session yet.
            </p>
            <p style="color: #64748B; font-size: 0.82rem;">
                Navigate to "New DGA Analysis" to submit gas readings.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown(f"""
    <div class="info-box">
        <strong>{len(history)}</strong> analysis/analyses performed in this session.
        This data is temporary and will be lost when the session ends.
    </div>
    """, unsafe_allow_html=True)

    # ── History Table ────────────────────────────────────────────────────
    table_html = """
    <div class="dga-card">
        <table class="styled-table">
            <thead><tr>
                <th>#</th>
                <th>Reference ID</th>
                <th>Timestamp</th>
                <th>Predicted Class</th>
                <th>Transformer</th>
                <th>H₂</th><th>CH₄</th><th>C₂H₆</th><th>C₂H₄</th><th>C₂H₂</th>
            </tr></thead><tbody>
    """

    for i, entry in enumerate(reversed(history), 1):
        gases = entry.get("gas_values", {})
        table_html += f"""
        <tr>
            <td>{i}</td>
            <td style="color: #00D4FF; font-size: 0.78rem;">{entry.get('reference_id', 'N/A')}</td>
            <td style="font-size: 0.78rem;">{entry.get('timestamp', 'N/A')}</td>
            <td style="font-weight: 600;">{entry.get('predicted_class', 'N/A')}</td>
            <td>{entry.get('transformer_label', 'N/A') or '—'}</td>
            <td style="text-align: right;">{gases.get('H2', 'N/A')}</td>
            <td style="text-align: right;">{gases.get('CH4', 'N/A')}</td>
            <td style="text-align: right;">{gases.get('C2H6', 'N/A')}</td>
            <td style="text-align: right;">{gases.get('C2H4', 'N/A')}</td>
            <td style="text-align: right;">{gases.get('C2H2', 'N/A')}</td>
        </tr>
        """

    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

    # ── Clear History ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🗑️ Clear Analysis History", use_container_width=True):
            st.session_state.analysis_history = []
            st.rerun()

    st.markdown("""
    <div class="disclaimer">
        Analysis history is stored in session memory only. It is not saved
        to disk, transmitted to external services, or retained after the
        session ends. Use the PDF or CSV download buttons on the results
        page to keep a permanent record of individual analyses.
    </div>
    """, unsafe_allow_html=True)
