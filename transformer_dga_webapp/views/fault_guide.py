"""
Fault Classification Guide page.

Educational reference for the six fault categories with searchable cards.
"""

import streamlit as st

from config.settings import CLASS_DESCRIPTIONS, CLASS_LABELS, TOOLTIPS


def render_fault_guide():
    """Render the fault classification guide."""

    st.markdown('<div class="page-title">📖 Fault Classification Guide</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        'Reference guide for the six fault categories used by the trained model. '
        'These descriptions are based on the dataset labelling and general DGA '
        'interpretation context.'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Search / Filter ──────────────────────────────────────────────────
    search = st.text_input(
        "🔍 Search fault classes",
        placeholder="Type to filter (e.g. 'thermal', 'discharge', 'PD')...",
        help="Filter the fault class cards by keyword.",
    )

    # ── Summary Table ────────────────────────────────────────────────────
    st.markdown('<div class="section-header">📋 Class Reference Table</div>',
                unsafe_allow_html=True)

    table_html = """
    <div class="dga-card">
        <table class="styled-table">
            <thead>
                <tr>
                    <th>Code</th>
                    <th>Fault Type</th>
                    <th>Category</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
    """

    for label in CLASS_LABELS:
        info = CLASS_DESCRIPTIONS[label]
        # Filter
        if search:
            search_lower = search.lower()
            match = (
                search_lower in label.lower()
                or search_lower in info["name"].lower()
                or search_lower in info["category"].lower()
                or search_lower in info["description"].lower()
            )
            if not match:
                continue

        cat_color = "#3B82F6" if info["category"] == "Electrical" else "#F59E0B"
        table_html += f"""
            <tr>
                <td style="font-weight: 700; color: #00D4FF;">{label}</td>
                <td>{info['name']}</td>
                <td><span style="color: {cat_color}; font-weight: 500;">{info['category']}</span></td>
                <td style="font-size: 0.78rem;">{info['description'][:120]}...</td>
            </tr>
        """

    table_html += "</tbody></table></div>"
    st.markdown(table_html, unsafe_allow_html=True)

    # ── Detailed Cards ───────────────────────────────────────────────────
    st.markdown('<div class="section-header">🗂️ Detailed Fault Class Cards</div>',
                unsafe_allow_html=True)

    icons = {
        "PD": "🔌", "D1": "⚡", "D2": "💥",
        "T1": "🌡️", "T2": "🔥", "T3": "🌋",
    }

    for label in CLASS_LABELS:
        info = CLASS_DESCRIPTIONS[label]

        # Filter
        if search:
            search_lower = search.lower()
            match = (
                search_lower in label.lower()
                or search_lower in info["name"].lower()
                or search_lower in info["category"].lower()
                or search_lower in info["description"].lower()
                or search_lower in info.get("dga_context", "").lower()
            )
            if not match:
                continue

        icon = icons.get(label, "📌")
        cat_color = "#3B82F6" if info["category"] == "Electrical" else "#F59E0B"
        badge = "badge-electrical" if info["category"] == "Electrical" else "badge-thermal"

        st.markdown(f"""
        <div class="dga-card">
            <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.8rem;">
                <span style="font-size: 2rem;">{icon}</span>
                <div>
                    <span class="result-badge {badge}">{label}</span>
                    <span style="color: #E2E8F0; font-weight: 600; font-size: 1rem; margin-left: 0.5rem;">
                        {info['name']}
                    </span>
                </div>
            </div>

            <p style="color: #94A3B8; font-size: 0.78rem; margin-bottom: 0.5rem;">
                Category: <span style="color: {cat_color}; font-weight: 500;">{info['category']}</span>
            </p>

            <p style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.65; margin-bottom: 0.8rem;">
                {info['description']}
            </p>

            <div style="background: rgba(0, 212, 255, 0.05); border-radius: 6px;
                        padding: 0.7rem; margin-bottom: 0.6rem;">
                <p style="color: #94A3B8; font-size: 0.82rem; line-height: 1.5;">
                    <strong style="color: #00D4FF;">DGA Interpretation Context:</strong>
                    {info.get('dga_context', 'No additional DGA context available.')}
                </p>
            </div>

            <div style="background: rgba(245, 158, 11, 0.08); border-radius: 6px; padding: 0.7rem;">
                <p style="color: #FCD34D; font-size: 0.82rem; line-height: 1.5;">
                    <strong>⚠️ Engineering Review Note:</strong>
                    {info.get('engineering_note', 'Professional engineering review is recommended.')}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Important caveats ────────────────────────────────────────────────
    st.markdown('<div class="section-header">⚠️ Important Caveats</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="dga-card">
        <ul style="color: #94A3B8; font-size: 0.85rem; line-height: 1.8; padding-left: 1.2rem;">
            <li>These fault descriptions are based on general DGA interpretation
                literature and the dataset labelling scheme.</li>
            <li>The trained model predicts which category the gas pattern most
                closely resembles — it does not diagnose the physical fault.</li>
            <li>Temperature ranges (e.g. T1 < 300°C) are approximate
                conventional boundaries used in the classification scheme, not
                precise measurements.</li>
            <li>Different transformer designs, oil types, and operating conditions
                can influence gas generation patterns.</li>
            <li>Always combine DGA results with other diagnostic techniques and
                professional engineering judgement.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
