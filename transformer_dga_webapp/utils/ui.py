"""
UI components and helpers for Transformer DGA Intelligence.
"""

import streamlit as st


def tooltip(label: str, help_text: str, tag: str = "span") -> str:
    """Generate an HTML tooltip with accessible markup."""
    return (
        f'<{tag} class="dga-tooltip" tabindex="0">{label}'
        f'<span class="tooltip-icon" role="img" aria-label="Help">?</span>'
        f'<span class="tooltip-content" role="tooltip">{help_text}</span>'
        f'</{tag}>'
    )


def render_footer():
    """Render the application footer."""
    st.markdown("""
    <div class="app-footer">
        <p>Designed and developed by <strong>Mourya Abbadasari</strong> | Electrical Engineering, IIT Tirupati</p>
        <p style="margin-top: 0.3rem;">Transformer DGA Intelligence — PRML-Based Power Transformer Fault Diagnosis</p>
        <p style="margin-top: 0.3rem; font-size: 0.7rem;">
            "Turning Dissolved Gas Data into Actionable Diagnostic Insights."
        </p>
    </div>
    """, unsafe_allow_html=True)
