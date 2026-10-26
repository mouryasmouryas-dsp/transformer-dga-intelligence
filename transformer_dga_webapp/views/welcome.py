"""
Welcome page — first screen the user sees.

Collects user name and purpose before entering the main application.
"""

import streamlit as st


def render_welcome():
    """Render the welcome page with user entry form."""

    # ── Hero Section ─────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-container animate-fade-in">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">⚡</div>
        <div class="hero-title">Transformer DGA Intelligence</div>
        <div class="hero-subtitle">
            An intelligent, data-driven approach to exploratory transformer
            fault classification using dissolved gas analysis.
        </div>
        <div class="hero-tagline">
            "Turning Dissolved Gas Data into Actionable Diagnostic Insights."
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Welcome message ──────────────────────────────────────────────────
    st.markdown("""
    <div class="dga-card animate-fade-in" style="max-width: 650px; margin: 0 auto;">
        <p style="color: #CBD5E1; font-size: 0.95rem; text-align: center; margin-bottom: 0.5rem;">
            Hello, welcome! Let's understand your transformer through
            dissolved gas analysis.
        </p>
        <p style="color: #64748B; font-size: 0.8rem; text-align: center;">
            Please provide the following details to get started.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Entry form ───────────────────────────────────────────────────────
    col_left, col_form, col_right = st.columns([1, 2, 1])

    with col_form:
        with st.form("welcome_form"):
            st.markdown(
                '<p class="section-header">👤 User Details</p>',
                unsafe_allow_html=True,
            )

            name = st.text_input(
                "Your Name *",
                placeholder="Enter your name",
                help="Required. Used for personalised greetings and reports.",
            )

            purpose_options = [
                "Select your purpose...",
                "Academic learning and demonstration",
                "Student project or research",
                "Transformer condition screening",
                "Maintenance and engineering assessment",
                "Research and data analysis",
                "Other",
            ]

            purpose = st.selectbox(
                "Purpose of Use *",
                purpose_options,
                help="Required. Helps us tailor the experience.",
            )

            org = st.text_input(
                "Organisation / Institution (optional)",
                placeholder="e.g. IIT Tirupati",
                help="Optional. Your organisation or institution name.",
            )

            transformer_label = st.text_input(
                "Transformer Identification Label (optional)",
                placeholder="e.g. TX-2024-A or Substation 5 Unit 3",
                help=(
                    "Optional. A non-sensitive reference label for the "
                    "transformer you are analysing. This is not stored "
                    "permanently."
                ),
            )

            st.markdown("<br>", unsafe_allow_html=True)

            submitted = st.form_submit_button(
                "🚀 Continue",
                use_container_width=True,
                type="primary",
            )

            if submitted:
                # Validate
                errors = []
                if not name or not name.strip():
                    errors.append(
                        "**Name** is required. Please enter your name."
                    )
                if purpose == "Select your purpose...":
                    errors.append(
                        "**Purpose of Use** is required. "
                        "Please select a purpose."
                    )

                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    st.session_state.user_name = name.strip()
                    st.session_state.user_purpose = purpose
                    st.session_state.user_org = org.strip()
                    st.session_state.transformer_label = transformer_label.strip()
                    st.session_state.welcomed = True
                    st.rerun()

    # ── Disclaimer ───────────────────────────────────────────────────────
    st.markdown("""
    <div class="disclaimer" style="max-width: 650px; margin: 1rem auto;">
        <strong>Privacy:</strong> This application does not require account
        creation, does not store personal data permanently, and does not
        transmit your information to third-party services. Session data is
        temporary and cleared when you close the browser or reset the session.
    </div>
    """, unsafe_allow_html=True)
