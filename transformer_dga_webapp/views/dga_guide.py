"""
DGA & Transformer Engineering Knowledge Guide
===============================================
Comprehensive illustrated guide based on:
'Dissolved Gas Analysis (DGA) in Power Transformers:
Origin of Gases, Fault Mechanisms and Their Interpretation'
Prepared by: Mourya Abbadasari | Electrical Engineering, IIT Tirupati
"""

import os
import streamlit as st
from config.settings import APP_DIR, TOOLTIPS
from utils.ui import tooltip


def render_molecule_svg(gas_name: str) -> str:
    """Return crisp 3D-styled SVG for gas molecules."""
    svgs = {
        "H2": """
        <svg width="140" height="70" viewBox="0 0 140 70" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="hGrad" cx="35%" cy="35%" r="65%">
                    <stop offset="0%" stop-color="#FFFFFF"/>
                    <stop offset="60%" stop-color="#CBD5E1"/>
                    <stop offset="100%" stop-color="#64748B"/>
                </radialGradient>
            </defs>
            <!-- Bond -->
            <line x1="45" y1="35" x2="95" y2="35" stroke="#94A3B8" stroke-width="8" stroke-linecap="round"/>
            <!-- H atoms -->
            <circle cx="45" cy="35" r="22" fill="url(#hGrad)" stroke="#475569" stroke-width="1.5"/>
            <text x="45" y="41" font-size="14" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
            <circle cx="95" cy="35" r="22" fill="url(#hGrad)" stroke="#475569" stroke-width="1.5"/>
            <text x="95" y="41" font-size="14" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
        </svg>
        """,
        "CH4": """
        <svg width="140" height="110" viewBox="0 0 140 110" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="cGrad" cx="35%" cy="35%" r="65%">
                    <stop offset="0%" stop-color="#64748B"/>
                    <stop offset="60%" stop-color="#334155"/>
                    <stop offset="100%" stop-color="#0F172A"/>
                </radialGradient>
                <radialGradient id="hGrad2" cx="35%" cy="35%" r="65%">
                    <stop offset="0%" stop-color="#FFFFFF"/>
                    <stop offset="60%" stop-color="#CBD5E1"/>
                    <stop offset="100%" stop-color="#64748B"/>
                </radialGradient>
            </defs>
            <!-- Bonds -->
            <line x1="70" y1="55" x2="70" y2="18" stroke="#94A3B8" stroke-width="6"/>
            <line x1="70" y1="55" x2="30" y2="78" stroke="#94A3B8" stroke-width="6"/>
            <line x1="70" y1="55" x2="110" y2="78" stroke="#94A3B8" stroke-width="6"/>
            <line x1="70" y1="55" x2="70" y2="92" stroke="#94A3B8" stroke-width="5" stroke-dasharray="3,3"/>
            <!-- H atoms -->
            <circle cx="70" cy="18" r="14" fill="url(#hGrad2)" stroke="#475569"/>
            <text x="70" y="22" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
            <circle cx="30" cy="78" r="14" fill="url(#hGrad2)" stroke="#475569"/>
            <text x="30" y="82" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
            <circle cx="110" cy="78" r="14" fill="url(#hGrad2)" stroke="#475569"/>
            <text x="110" y="82" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
            <circle cx="70" cy="92" r="13" fill="url(#hGrad2)" stroke="#475569"/>
            <text x="70" y="96" font-size="9" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
            <!-- C atom -->
            <circle cx="70" cy="55" r="22" fill="url(#cGrad)" stroke="#00D4FF" stroke-width="1.5"/>
            <text x="70" y="61" font-size="15" font-weight="bold" fill="#00D4FF" text-anchor="middle">C</text>
        </svg>
        """,
        "C2H6": """
        <svg width="160" height="90" viewBox="0 0 160 90" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="cGrad2" cx="35%" cy="35%" r="65%">
                    <stop offset="0%" stop-color="#64748B"/>
                    <stop offset="60%" stop-color="#334155"/>
                    <stop offset="100%" stop-color="#0F172A"/>
                </radialGradient>
                <radialGradient id="hGrad3" cx="35%" cy="35%" r="65%">
                    <stop offset="0%" stop-color="#FFFFFF"/>
                    <stop offset="60%" stop-color="#CBD5E1"/>
                    <stop offset="100%" stop-color="#64748B"/>
                </radialGradient>
            </defs>
            <!-- C-C bond -->
            <line x1="55" y1="45" x2="105" y2="45" stroke="#00D4FF" stroke-width="6"/>
            <!-- C-H bonds -->
            <line x1="55" y1="45" x2="30" y2="20" stroke="#94A3B8" stroke-width="4"/>
            <line x1="55" y1="45" x2="20" y2="52" stroke="#94A3B8" stroke-width="4"/>
            <line x1="55" y1="45" x2="35" y2="75" stroke="#94A3B8" stroke-width="4"/>
            <line x1="105" y1="45" x2="130" y2="20" stroke="#94A3B8" stroke-width="4"/>
            <line x1="105" y1="45" x2="140" y2="52" stroke="#94A3B8" stroke-width="4"/>
            <line x1="105" y1="45" x2="125" y2="75" stroke="#94A3B8" stroke-width="4"/>
            <!-- H atoms -->
            <circle cx="30" cy="20" r="11" fill="url(#hGrad3)"/>
            <circle cx="20" cy="52" r="11" fill="url(#hGrad3)"/>
            <circle cx="35" cy="75" r="11" fill="url(#hGrad3)"/>
            <circle cx="130" cy="20" r="11" fill="url(#hGrad3)"/>
            <circle cx="140" cy="52" r="11" fill="url(#hGrad3)"/>
            <circle cx="125" cy="75" r="11" fill="url(#hGrad3)"/>
            <!-- C atoms -->
            <circle cx="55" cy="45" r="18" fill="url(#cGrad2)" stroke="#00D4FF"/>
            <text x="55" y="50" font-size="12" font-weight="bold" fill="#00D4FF" text-anchor="middle">C</text>
            <circle cx="105" cy="45" r="18" fill="url(#cGrad2)" stroke="#00D4FF"/>
            <text x="105" y="50" font-size="12" font-weight="bold" fill="#00D4FF" text-anchor="middle">C</text>
        </svg>
        """,
        "C2H4": """
        <svg width="150" height="90" viewBox="0 0 150 90" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="cGrad3" cx="35%" cy="35%" r="65%">
                    <stop offset="0%" stop-color="#64748B"/>
                    <stop offset="60%" stop-color="#334155"/>
                    <stop offset="100%" stop-color="#0F172A"/>
                </radialGradient>
                <radialGradient id="hGrad4" cx="35%" cy="35%" r="65%">
                    <stop offset="0%" stop-color="#FFFFFF"/>
                    <stop offset="60%" stop-color="#CBD5E1"/>
                    <stop offset="100%" stop-color="#64748B"/>
                </radialGradient>
            </defs>
            <!-- Double bond C=C -->
            <line x1="50" y1="41" x2="100" y2="41" stroke="#EF4444" stroke-width="4"/>
            <line x1="50" y1="49" x2="100" y2="49" stroke="#EF4444" stroke-width="4"/>
            <!-- C-H bonds -->
            <line x1="50" y1="45" x2="22" y2="20" stroke="#94A3B8" stroke-width="4"/>
            <line x1="50" y1="45" x2="22" y2="70" stroke="#94A3B8" stroke-width="4"/>
            <line x1="100" y1="45" x2="128" y2="20" stroke="#94A3B8" stroke-width="4"/>
            <line x1="100" y1="45" x2="128" y2="70" stroke="#94A3B8" stroke-width="4"/>
            <!-- H atoms -->
            <circle cx="22" cy="20" r="12" fill="url(#hGrad4)"/>
            <text x="22" y="24" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
            <circle cx="22" cy="70" r="12" fill="url(#hGrad4)"/>
            <text x="22" y="74" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
            <circle cx="128" cy="20" r="12" fill="url(#hGrad4)"/>
            <text x="128" y="24" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
            <circle cx="128" cy="70" r="12" fill="url(#hGrad4)"/>
            <text x="128" y="74" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
            <!-- C atoms -->
            <circle cx="50" cy="45" r="18" fill="url(#cGrad3)" stroke="#EF4444" stroke-width="1.5"/>
            <text x="50" y="50" font-size="12" font-weight="bold" fill="#FCA5A5" text-anchor="middle">C</text>
            <circle cx="100" cy="45" r="18" fill="url(#cGrad3)" stroke="#EF4444" stroke-width="1.5"/>
            <text x="100" y="50" font-size="12" font-weight="bold" fill="#FCA5A5" text-anchor="middle">C</text>
        </svg>
        """,
        "C2H2": """
        <svg width="150" height="70" viewBox="0 0 150 70" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="cGrad4" cx="35%" cy="35%" r="65%">
                    <stop offset="0%" stop-color="#64748B"/>
                    <stop offset="60%" stop-color="#334155"/>
                    <stop offset="100%" stop-color="#0F172A"/>
                </radialGradient>
                <radialGradient id="hGrad5" cx="35%" cy="35%" r="65%">
                    <stop offset="0%" stop-color="#FFFFFF"/>
                    <stop offset="60%" stop-color="#CBD5E1"/>
                    <stop offset="100%" stop-color="#64748B"/>
                </radialGradient>
            </defs>
            <!-- Triple bond C≡C -->
            <line x1="50" y1="30" x2="100" y2="30" stroke="#A855F7" stroke-width="3"/>
            <line x1="50" y1="35" x2="100" y2="35" stroke="#A855F7" stroke-width="3"/>
            <line x1="50" y1="40" x2="100" y2="40" stroke="#A855F7" stroke-width="3"/>
            <!-- C-H bonds (Linear) -->
            <line x1="50" y1="35" x2="20" y2="35" stroke="#94A3B8" stroke-width="4"/>
            <line x1="100" y1="35" x2="130" y2="35" stroke="#94A3B8" stroke-width="4"/>
            <!-- H atoms -->
            <circle cx="20" cy="35" r="12" fill="url(#hGrad5)"/>
            <text x="20" y="39" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
            <circle cx="130" cy="35" r="12" fill="url(#hGrad5)"/>
            <text x="130" y="39" font-size="10" font-weight="bold" fill="#0F172A" text-anchor="middle">H</text>
            <!-- C atoms -->
            <circle cx="50" cy="35" r="18" fill="url(#cGrad4)" stroke="#A855F7" stroke-width="1.5"/>
            <text x="50" y="40" font-size="12" font-weight="bold" fill="#E9D5FF" text-anchor="middle">C</text>
            <circle cx="100" cy="35" r="18" fill="url(#cGrad4)" stroke="#A855F7" stroke-width="1.5"/>
            <text x="100" y="40" font-size="12" font-weight="bold" fill="#E9D5FF" text-anchor="middle">C</text>
        </svg>
        """,
    }
    return svgs.get(gas_name, "")


def render_dga_guide():
    """Render the full illustrated DGA and Transformer engineering guide."""

    # ── Header Banner ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0A192F 0%, #1E293B 100%); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 12px; padding: 1.5rem; text-align: center; margin-bottom: 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
        <div style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, #00D4FF, #38BDF8, #818CF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.4rem;">
            Dissolved Gas Analysis (DGA) in Power Transformers
        </div>
        <div style="font-size: 1.1rem; color: #E2E8F0; font-weight: 600; margin-bottom: 0.4rem;">
            Origin of Gases, Fault Mechanisms and Their Interpretation
        </div>
        <div style="font-size: 0.85rem; color: #94A3B8; max-width: 800px; margin: 0 auto; line-height: 1.5;">
            A Complete Guide for Understanding How Gases Form in a Transformer and How They Help in Fault Detection
        </div>
        <div style="margin-top: 0.8rem; font-size: 0.75rem; color: #38BDF8; font-weight: 600;">
            Prepared by: Mourya Abbadasari | Electrical Engineering, IIT Tirupati
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick Jump Tabs ──────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "1. Transformer Structure",
        "2. Gas Formation & Lab GC",
        "3. Five Key Gases",
        "4. Fault Matrix",
        "5. Overall Process",
        "6. Engineering Notes",
    ])

    # ── Tab 1: Internal Structure ────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-header">1. Power Transformer – Internal Structure</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.6;">
            A power transformer is one of the most critical and expensive assets in an electrical substation.
            It operates under severe dielectric and thermal stresses. Understanding its internal construction
            explains where faults originate and how dissolved gases accumulate in the oil.
        </p>
        """, unsafe_allow_html=True)

        img_path = os.path.join(APP_DIR, "assets", "transformer_structure.jpg")
        if os.path.exists(img_path):
            st.image(img_path, caption="Figure 1: High-Voltage Power Transformer Internal Cutaway Architecture", use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="dga-card">
                <h4 style="color: #00D4FF; margin-top:0;">🛡️ Oil Preservation & Enclosure</h4>
                <ul style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.6; padding-left: 1.2rem;">
                    <li><strong>Conservator Tank:</strong> Mounted above the main tank to provide space for oil thermal expansion and contraction while keeping the main tank completely full.</li>
                    <li><strong>Main Tank:</strong> Sturdy sealed steel tank containing the active core-and-coil assembly submerged in insulating oil.</li>
                    <li><strong>Radiators & Fans:</strong> Natural or forced air cooling system dissipating heat generated by $I^2R$ copper losses and iron core losses.</li>
                    <li><strong>Buchholz Relay:</strong> Installed on the pipe between main tank and conservator; senses gas accumulation and oil surges during internal faults.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="dga-card">
                <h4 style="color: #38BDF8; margin-top:0;">⚡ Active Magnetic & Electrical Core</h4>
                <ul style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.6; padding-left: 1.2rem;">
                    <li><strong>HV & LV Bushings:</strong> Insulated hollow ceramic/resin sleeves that safely transmit high-voltage current through the grounded metallic tank wall.</li>
                    <li><strong>Copper Windings:</strong> Primary and secondary coiled conductors carrying electrical power, insulated by cellulose Kraft paper.</li>
                    <li><strong>Laminated Silicon Steel Core:</strong> Transfers electromagnetic flux between primary and secondary windings with minimal eddy current losses.</li>
                    <li><strong>Insulating Mineral Oil:</strong> Provides high dielectric breakdown strength (>30 kV) and acts as the liquid cooling medium.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: Gas Formation & Lab GC ─────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-header">2. How Gases Form Inside a Transformer</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; flex-direction: column; gap: 0.8rem; margin-bottom: 1.5rem;">
            <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid #EF4444; padding: 0.8rem; border-radius: 4px;">
                <strong style="color: #F87171;">Step 1: Electrical or Thermal Stress</strong><br/>
                <span style="color: #CBD5E1; font-size: 0.85rem;">Partial discharge, localized arcing, excessive load overheating, or insulation degradation triggers thermal and electrical stress.</span>
            </div>
            <div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid #F59E0B; padding: 0.8rem; border-radius: 4px;">
                <strong style="color: #FBBF24;">Step 2: Decomposition of Insulation</strong><br/>
                <span style="color: #CBD5E1; font-size: 0.85rem;">Transformer hydrocarbon oil ($C_n H_{2n+2}$) and cellulose paper ($(C_6 H_{10} O_5)_n$) crack and dissociate under energy stress.</span>
            </div>
            <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; padding: 0.8rem; border-radius: 4px;">
                <strong style="color: #34D399;">Step 3: Formation of Key Gases</strong><br/>
                <span style="color: #CBD5E1; font-size: 0.85rem;">Chemical free radical reactions produce five key gases: Hydrogen ($H_2$), Methane ($CH_4$), Ethane ($C_2H_6$), Ethylene ($C_2H_4$), and Acetylene ($C_2H_2$).</span>
            </div>
            <div style="background: rgba(56, 189, 248, 0.1); border-left: 4px solid #38BDF8; padding: 0.8rem; border-radius: 4px;">
                <strong style="color: #38BDF8;">Step 4: Gases Dissolve in Oil</strong><br/>
                <span style="color: #CBD5E1; font-size: 0.85rem;">Generated gases dissolve readily into surrounding oil bulk and distribute throughout the tank over time.</span>
            </div>
            <div style="background: rgba(168, 85, 247, 0.1); border-left: 4px solid #A855F7; padding: 0.8rem; border-radius: 4px;">
                <strong style="color: #C084FC;">Step 5: Oil Sample Taken for Laboratory DGA</strong><br/>
                <span style="color: #CBD5E1; font-size: 0.85rem;">A sample is extracted using a precision sampling valve and tested via Gas Chromatography to quantify parts-per-million (ppm) levels.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">3. Oil Sampling & Laboratory Gas Chromatography (GC)</div>', unsafe_allow_html=True)
        img_gc = os.path.join(APP_DIR, "assets", "oil_sampling_gc.jpg")
        if os.path.exists(img_gc):
            st.image(img_gc, caption="Figure 2: Professional Oil Sampling with Glass Syringe & Laboratory Gas Chromatograph (GC)", use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="dga-card">
                <h4 style="color: #00D4FF; margin-top:0;">🧪 Oil Sample Collection</h4>
                <p style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.5;">
                    Oil is extracted from designated lower sampling valves using gas-tight glass syringes or sealed stainless steel containers conforming to <strong>ASTM D3613 / IEC 60567</strong>.
                    It is vital to purge lines and avoid atmospheric contamination (air bubbles or moisture) which distort dissolved gas ratios.
                </p>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="dga-card">
                <h4 style="color: #38BDF8; margin-top:0;">🔬 Laboratory GC Analysis</h4>
                <p style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.5;">
                    Dissolved gases are stripped from the oil matrix using vacuum extraction or headspace stripping and injected into a Gas Chromatograph equipped with <strong>TCD</strong> (Thermal Conductivity Detector for $H_2, O_2, N_2$) and <strong>FID</strong> (Flame Ionization Detector with methanizer for hydrocarbons $CH_4, C_2H_6, C_2H_4, C_2H_2, CO, CO_2$).
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 3: The 5 Key Gases ────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-header">5. The Five Key Gases Used in This Project</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color: #CBD5E1; font-size: 0.9rem;">
            While transformers generate several trace gases, dissolved gas analysis relies primarily on five diagnostic hydrocarbon gases plus hydrogen. Each gas reflects a distinct chemical bond cracking energy:
        </p>
        """, unsafe_allow_html=True)

        # 5 Gas Cards
        gases_info = [
            {
                "gas": "H2",
                "title": "1. Hydrogen (H₂)",
                "color": "#38BDF8",
                "border": "rgba(56, 189, 248, 0.4)",
                "formation": "Produced by low-energy electrical discharges, corona, ionization, and energetic reactions breaking $C-H$ bonds.",
                "faults": "Partial Discharge (PD), low-energy sparking, and general electrical stressing.",
                "key": "Often the first gas to evolve. Elevated $H_2$ with negligible hydrocarbons strongly suggests corona or partial discharge.",
            },
            {
                "gas": "CH4",
                "title": "2. Methane (CH₄)",
                "color": "#34D399",
                "border": "rgba(52, 211, 153, 0.4)",
                "formation": "Formed due to decomposition of oil hydrocarbons at relatively lower temperatures ($< 300^\\circ\\text{C}$).",
                "faults": "Low-temperature thermal overheating (T1) and accompanying low-energy discharges.",
                "key": "Methane presence alone is not sufficient; its ratio against $C_2H_6$ and $C_2H_4$ establishes temperature severity.",
            },
            {
                "gas": "C2H6",
                "title": "3. Ethane (C₂H₆)",
                "color": "#FBBF24",
                "border": "rgba(251, 191, 36, 0.4)",
                "formation": "Produced by thermal decomposition of oil and paper at moderate temperatures ($150^\\circ\\text{C} - 300^\\circ\\text{C}$).",
                "faults": "Low-temperature thermal faults (T1 range), core hot spots, or circulating currents.",
                "key": "High ethane relative to methane signals thermal decomposition of paper insulation and localized oil degradation.",
            },
            {
                "gas": "C2H4",
                "title": "4. Ethylene (C₂H₄)",
                "color": "#F87171",
                "border": "rgba(248, 113, 113, 0.4)",
                "formation": "Requires higher thermal energy ($> 300^\\circ\\text{C}$ to $> 700^\\circ\\text{C}$) to form double carbon bonds ($C=C$).",
                "faults": "Medium to high-temperature thermal faults (T2 and T3 range), severe core or winding hot spots.",
                "key": "Primary indicator of severe thermal severity. Elevated ethylene demands urgent engineering review of transformer cooling.",
            },
            {
                "gas": "C2H2",
                "title": "5. Acetylene (C₂H₂)",
                "color": "#C084FC",
                "border": "rgba(192, 132, 252, 0.4)",
                "formation": "Produced under extreme temperature conditions ($> 700^\\circ\\text{C}$ to $> 1000^\\circ\\text{C}$) that create triple carbon bonds ($C\\equiv C$).",
                "faults": "High-energy electrical arcing (D2), flashover, or catastrophic thermal runaway.",
                "key": "CRITICAL DANGER GAS: Even small concentrations (> 2-5 ppm) require immediate attention and possible de-energization.",
            },
        ]

        for g in gases_info:
            col_l, col_r = st.columns([1, 2.5])
            with col_l:
                st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.95); border: 1px solid {g['border']}; border-radius: 10px; padding: 1rem; text-align: center; height: 100%;">
                    <div style="color: {g['color']}; font-weight: 700; font-size: 1rem; margin-bottom: 0.5rem;">{g['title']}</div>
                    {render_molecule_svg(g['gas'])}
                    <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 0.5rem;">Molecular Structure</div>
                </div>
                """, unsafe_allow_html=True)
            with col_r:
                st.markdown(f"""
                <div class="dga-card" style="border-left: 4px solid {g['color']};">
                    <p style="margin-bottom: 0.4rem;"><strong style="color: {g['color']};">Formation Mechanism:</strong> <span style="color: #CBD5E1; font-size: 0.85rem;">{g['formation']}</span></p>
                    <p style="margin-bottom: 0.4rem;"><strong style="color: #E2E8F0;">Associated Faults:</strong> <span style="color: #94A3B8; font-size: 0.85rem;">{g['faults']}</span></p>
                    <p style="margin-bottom: 0;"><strong style="color: #FCD34D;">Key Diagnostic Point:</strong> <span style="color: #CBD5E1; font-size: 0.85rem;">{g['key']}</span></p>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)

    # ── Tab 4: Fault Matrix ───────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-header">6. How Different Faults Produce Different Gases</div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color: #CBD5E1; font-size: 0.9rem;">
            According to IEEE C57.104 and IEC 60599 international standards, internal faults are classified into six fundamental categories based on their energy levels and physical origin:
        </p>
        """, unsafe_allow_html=True)

        st.markdown("""
        <table class="styled-table" style="width: 100%; font-size: 0.85rem;">
            <thead>
                <tr style="background: rgba(0, 212, 255, 0.15); color: #00D4FF;">
                    <th>Fault Type</th>
                    <th>Full Name</th>
                    <th>Physical Fault Condition</th>
                    <th>Typical Gas Behavior (Signature Trend)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong style="color: #38BDF8;">PD</strong></td>
                    <td>Partial Discharge</td>
                    <td>Low-energy electrical discharges, gas cavities in paper, voids</td>
                    <td>High <strong>H₂</strong>, some <strong>CH₄</strong>, negligible <strong>C₂H₂</strong></td>
                </tr>
                <tr>
                    <td><strong style="color: #60A5FA;">D1</strong></td>
                    <td>Low-Energy Discharge</td>
                    <td>Sparking, floating potential breakdown, carbon tracking</td>
                    <td>Moderate <strong>H₂</strong>, <strong>CH₄</strong>, <strong>C₂H₆</strong>, trace <strong>C₂H₂</strong></td>
                </tr>
                <tr>
                    <td><strong style="color: #818CF8;">D2</strong></td>
                    <td>High-Energy Discharge</td>
                    <td>Continuous arcing, power flashover, short circuits</td>
                    <td>High <strong>H₂</strong>, High <strong>C₂H₂</strong>, moderate <strong>CH₄</strong>, <strong>C₂H₆</strong></td>
                </tr>
                <tr>
                    <td><strong style="color: #FBBF24;">T1</strong></td>
                    <td>Thermal Fault &lt; 300 °C</td>
                    <td>Low-temperature overheating, paper insulation degradation</td>
                    <td>Dominant <strong>CH₄</strong> and <strong>C₂H₆</strong>, low <strong>C₂H₄</strong></td>
                </tr>
                <tr>
                    <td><strong style="color: #FB923C;">T2</strong></td>
                    <td>Thermal Fault 300 °C – 700 °C</td>
                    <td>Medium-temperature overheating of core or windings</td>
                    <td>Higher <strong>C₂H₄</strong>, moderate <strong>C₂H₆</strong>, some <strong>CH₄</strong></td>
                </tr>
                <tr>
                    <td><strong style="color: #F87171;">T3</strong></td>
                    <td>Thermal Fault &gt; 700 °C</td>
                    <td>Critical hot spot, core bolts, copper melting, tank currents</td>
                    <td>Dominant <strong>C₂H₄</strong>, small trace <strong>C₂H₂</strong>, lower <strong>CH₄</strong>, <strong>C₂H₆</strong></td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    # ── Tab 5: Overall Process ────────────────────────────────────────────────
    with tab5:
        st.markdown('<div class="section-header">7. Overall Process from Fault to Machine Learning Prediction</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(15, 23, 42, 0.95); border: 1px solid rgba(0, 212, 255, 0.2); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 0.5rem; text-align: center;">
                <div style="flex: 1; min-width: 130px; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 8px; padding: 0.8rem 0.5rem;">
                    <div style="font-size: 1.4rem;">⚡</div>
                    <div style="color: #F87171; font-weight: 700; font-size: 0.85rem;">1. Fault Occurs</div>
                    <div style="color: #94A3B8; font-size: 0.7rem; margin-top: 0.2rem;">Electrical or Thermal Stress</div>
                </div>
                <div style="color: #00D4FF; font-size: 1.2rem;">➔</div>
                <div style="flex: 1; min-width: 130px; background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 8px; padding: 0.8rem 0.5rem;">
                    <div style="font-size: 1.4rem;">🔥</div>
                    <div style="color: #FBBF24; font-weight: 700; font-size: 0.85rem;">2. Insulation Decomposes</div>
                    <div style="color: #94A3B8; font-size: 0.7rem; margin-top: 0.2rem;">Mineral Oil & Paper Breakdown</div>
                </div>
                <div style="color: #00D4FF; font-size: 1.2rem;">➔</div>
                <div style="flex: 1; min-width: 130px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 8px; padding: 0.8rem 0.5rem;">
                    <div style="font-size: 1.4rem;">💨</div>
                    <div style="color: #34D399; font-weight: 700; font-size: 0.85rem;">3. Gases Formed</div>
                    <div style="color: #94A3B8; font-size: 0.7rem; margin-top: 0.2rem;">H₂, CH₄, C₂H₆, C₂H₄, C₂H₂</div>
                </div>
                <div style="color: #00D4FF; font-size: 1.2rem;">➔</div>
                <div style="flex: 1; min-width: 130px; background: rgba(56, 189, 248, 0.15); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 8px; padding: 0.8rem 0.5rem;">
                    <div style="font-size: 1.4rem;">💧</div>
                    <div style="color: #38BDF8; font-weight: 700; font-size: 0.85rem;">4. Gases Dissolve</div>
                    <div style="color: #94A3B8; font-size: 0.7rem; margin-top: 0.2rem;">Dispersed in Oil Bulk</div>
                </div>
                <div style="color: #00D4FF; font-size: 1.2rem;">➔</div>
                <div style="flex: 1; min-width: 130px; background: rgba(168, 85, 247, 0.15); border: 1px solid rgba(168, 85, 247, 0.4); border-radius: 8px; padding: 0.8rem 0.5rem;">
                    <div style="font-size: 1.4rem;">🧪</div>
                    <div style="color: #C084FC; font-weight: 700; font-size: 0.85rem;">5. Lab GC Analysis</div>
                    <div style="color: #94A3B8; font-size: 0.7rem; margin-top: 0.2rem;">Concentrations in ppm (μL/L)</div>
                </div>
                <div style="color: #00D4FF; font-size: 1.2rem;">➔</div>
                <div style="flex: 1; min-width: 130px; background: rgba(0, 212, 255, 0.15); border: 1px solid rgba(0, 212, 255, 0.5); border-radius: 8px; padding: 0.8rem 0.5rem;">
                    <div style="font-size: 1.4rem;">🤖</div>
                    <div style="color: #00D4FF; font-weight: 700; font-size: 0.85rem;">6. Model Prediction</div>
                    <div style="color: #94A3B8; font-size: 0.7rem; margin-top: 0.2rem;">Predicts PD, D1, D2, T1, T2, T3</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Tab 6: Engineering Notes ──────────────────────────────────────────────
    with tab6:
        st.markdown('<div class="section-header">8. Important Notes, Practical Guidelines & Limitations</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="dga-card">
            <h4 style="color: #00D4FF; margin-top:0;">📋 Key Operational Guidelines</h4>
            <ul style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.7; padding-left: 1.2rem;">
                <li><strong>Gas Concentration Rates (ppm/day):</strong> The rate of gas increase is often far more diagnostic than absolute single ppm values. A sudden spike in gas generation rate indicates an active developing fault.</li>
                <li><strong>Multi-Fault Scenarios:</strong> In real transformers, more than one fault can occur simultaneously (e.g. overheating leading to insulation breakdown and sparking). One gas can participate in multiple signatures.</li>
                <li><strong>Role of PRML Machine Learning:</strong> Traditional ratio methods (Rogers, Dornenburg, Duval triangle) can leave data points in unclassified zones. The Random Forest pattern-recognition model evaluates nonlinear combinations across all 5 gases simultaneously.</li>
                <li><strong>Decision Support Tool:</strong> Model predictions identify statistical pattern matches. They serve as experimental screening recommendations and should always be verified alongside breakdown voltage (BDV), moisture analysis, and physical inspection.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: right; padding: 1rem 0; color: #64748B; font-size: 0.78rem;">
            Information guide curated by <strong>Mourya Abbadasari</strong> | Electrical Engineering, IIT Tirupati
        </div>
        """, unsafe_allow_html=True)
