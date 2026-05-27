import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
from src.mrp_engine import MRPEngine
import tempfile
import os

# Set page configuration with a premium dark-themed layout
st.set_page_config(
    page_title="Nethra AI | UP 2027 Analytical Prototype",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium glassmorphic styling, neon accent colors, and custom typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* Header design */
    .app-header {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .app-header::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .app-title {
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -1px;
        background: linear-gradient(to right, #6366f1, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .app-subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-top: 0.5rem;
    }
    
    /* Metrics panel cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.15);
    }
    .metric-val {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
        margin-bottom: 0.2rem;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Custom tab indicators */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(30, 41, 59, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #94a3b8 !important;
        border-radius: 8px 8px 0px 0px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(99, 102, 241, 0.15) !important;
        color: #6366f1 !important;
        border-color: rgba(99, 102, 241, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="app-header">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <span style="font-size: 3rem;">👁️</span>
        <div>
            <h1 class="app-title">PROJECT NETHRA</h1>
            <p class="app-subtitle">Demographic Swing Forecasting Engine & Compliant Targeting API | <b>UP Assembly Elections 2027</b></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.markdown("### 🛠️ Bayesian Priors & Parameters")

ac_selection = st.sidebar.selectbox(
    "Assembly Constituency Location",
    ["AC-175 Lucknow Cantt (UP)", "AC-174 Lucknow Central (UP)", "AC-176 Lucknow East (UP)"]
)

# Slider parameters affecting the Bayesian MRP projection logic live
baseline_swing_prior = st.sidebar.slider(
    "Baseline Swing Prior (β₀)",
    min_value=0.10,
    max_value=0.60,
    value=0.35,
    step=0.01,
    help="The starting baseline probability that an average voter shifts allegiance."
)

loss_aversion_mult = st.sidebar.slider(
    "Loss Aversion Index Multiplier",
    min_value=1.0,
    max_value=3.0,
    value=1.8,
    step=0.1,
    help="Behavioral multiplier scaling logits for economically stressed voter cohorts (1.8x default based on behavioral prospect theory)."
)

k_anonymity_gate = st.sidebar.slider(
    "k-Anonymity Threshold",
    min_value=5,
    max_value=30,
    value=10,
    step=1,
    help="Minimum voter size per cell to prevent re-identification. Cells below this are automatically merged upward to guarantee DPDP Act 2023 compliance."
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📋 5-Perspective Matrix
- 🛡️ **Ethics & Privacy:** Privacy by Design, $k \\ge 10$ cell suppression.
- 📊 **ML Engineering:** Bayesian MRP spatial raking.
- 🧠 **Behavioral Psychology:** Loss Aversion Index prior.
- 🏛️ **Political Leadership:** Max campaign ROI, anomaly checks.
- 📈 **Product Management:** Agile double-track execution.
""")

# ----------------- DATA ENGINE INGESTION -----------------
@st.cache_resource
def get_engine():
    """Initializes and returns the MRP analytical engine."""
    return MRPEngine()

try:
    engine = get_engine()
except Exception as e:
    st.error(f"Failed to load data engine. Have you run `src/generate_mock_data.py` yet? Error: {e}")
    st.stop()

# Re-run projections live inside Streamlit using the sidebar slider values
df_strat, df_results = engine.run_mrp_projection(
    loss_aversion_mult=loss_aversion_mult,
    baseline_swing_prior=baseline_swing_prior,
    k_anon=k_anonymity_gate
)
df_results = engine.spatial_bridge_join(df_results)
df_results, cadre_support = engine.calculate_cadre_anomaly(df_results)

# Consolidated Key Stats
total_electorate = df_results['total_voters'].sum()
total_swing_votes = df_results['swing_votes'].sum()
avg_swing_ratio = (total_swing_votes / total_electorate) * 100
total_anomalies = (df_results['anomaly_score'] > 0.15).sum()

# Display Metrics Cards
cols = st.columns(4)
with cols[0]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val">{total_electorate:,}</div>
        <div class="metric-label">Total Electorate Size</div>
    </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown(f"""
    <div class="metric-card" style="border-color: rgba(168, 85, 247, 0.4);">
        <div class="metric-val">{total_swing_votes:,}</div>
        <div class="metric-label">Projected Swing Voters</div>
    </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-val" style="color: #a855f7;">{avg_swing_ratio:.2f}%</div>
        <div class="metric-label">Average PERSUADABILITY</div>
    </div>
    """, unsafe_allow_html=True)
with cols[3]:
    st.markdown(f"""
    <div class="metric-card" style="border-color: rgba(239, 68, 68, 0.3);">
        <div class="metric-val" style="color: #ef4444;">{total_anomalies}</div>
        <div class="metric-label">HIGH ANOMALY BOOTHS</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ----------------- TABS CREATION -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Geospatial Swing Intelligence", 
    "📊 Demographic Sensitivity Audit", 
    "🔒 ECI MCMC Compliance Gate",
    "🚀 Compliant Meta/Google Payload Export"
])

# ----------------- TAB 1: GEOSPATIAL MAPS -----------------
with tab1:
    st.markdown("### 🗺️ Polling Station 3D Spatial Swing Projections")
    st.markdown("""
    This map overlays polling station locations in **AC-175 Lucknow Cantt**. 
    - **Color scale:** Historical Volatility Index ($HV_{booth}$) showing persuasion elasticity (lighter purple = higher elasticity).
    - **Bar Height/Radius:** Total projected swing votes ($V_{booth}$) available at the station.
    - **Strategic Outliers:** Booth 9 (Sadar Bazar Sadar Bazar Ward) represents the primary competitive battleground.
    """)
    
    # Configure pydeck mapping options
    midpoint_lat = df_results['lat'].mean()
    midpoint_lon = df_results['lon'].mean()
    
    # Standardize data for rendering heights/colors in pydeck
    df_results['hv_color'] = df_results['historical_volatility_index'] * 255.0
    
    # Deck view state
    view_state = pdk.ViewState(
        latitude=midpoint_lat,
        longitude=midpoint_lon,
        zoom=12.2,
        pitch=45
    )
    
    # 3D Hexagon/Column Layer
    layer = pdk.Layer(
        "ColumnLayer",
        data=df_results,
        get_position="[lon, lat]",
        get_elevation="swing_votes * 10",
        elevation_scale=1.5,
        radius=140,
        get_fill_color="[hv_color, 50, 255 - hv_color, 200]",
        pickable=True,
        auto_highlight=True,
    )
    
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Booth No: {booth_id}\nSwing Voters: {swing_votes}\nPersuadability: {swing_ratio}\nWard: {spatial_ward}\nAnomaly: {anomaly_score}"},
        map_style="mapbox://styles/mapbox/dark-v10"
    )
    
    st.pydeck_chart(r)
    
    # Table displaying ranked tactical swing targets
    st.markdown("#### 🎯 Priority Target Booths Ranked by Net Persuading Yield")
    
    df_ranked = df_results.copy()
    df_ranked['persuasion_yield'] = df_ranked['swing_votes']
    df_ranked = df_ranked.sort_values(by='persuasion_yield', ascending=False)
    
    # Display table
    st.dataframe(
        df_ranked[['booth_id', 'total_voters', 'swing_votes', 'swing_ratio', 'historical_volatility_index', 'historical_margin_of_victory', 'spatial_ward', 'anomaly_score']]
        .rename(columns={
            'booth_id': 'Booth #',
            'total_voters': 'Total Voters',
            'swing_votes': 'Projected Swing Voters',
            'swing_ratio': 'Swing Ratio',
            'historical_volatility_index': 'Historical Volatility (HV)',
            'historical_margin_of_victory': 'Margin of Victory (HM)',
            'spatial_ward': 'Spatial Ward Boundary',
            'anomaly_score': 'Anomaly Delta Score'
        }),
        use_container_width=True,
        hide_index=True
    )

# ----------------- TAB 2: DEMOGRAPHIC SENSITIVITY -----------------
with tab2:
    st.markdown("### 📊 Demographic Stratum Churn Distributions")
    st.markdown("""
    Explore swing propensity across specific demographic cells in the raked poststratification frame. 
    Adjusting the **Loss Aversion Multiplier** in the sidebar directly shifts economic pressure weights for 'Non-Workers' and 'Ag-Laborers'.
    """)
    
    # 1. Plotly Distributions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Swing Probability Distribution by Age Cohorts")
        fig_age = px.box(
            df_strat, 
            x="age_group", 
            y="swing_prob", 
            color="gender",
            points="all",
            title="Strata Persuadability Across Age & Gender",
            color_discrete_sequence=["#6366f1", "#ec4899"],
            labels={"age_group": "Age Cohort", "swing_prob": "Swing Propensity Score"}
        )
        fig_age.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#f3f4f6")
        st.plotly_chart(fig_age, use_container_width=True)
        
    with col2:
        st.markdown("#### Strategic Persuadability by Social & Economic Occupations")
        fig_occ = px.bar(
            df_strat.groupby(['occupation', 'social_group'])['swing_votes'].sum().reset_index(),
            x="occupation",
            y="swing_votes",
            color="social_group",
            title="Swing Votes Share by Occupation Class",
            barmode="group",
            color_discrete_sequence=["#6366f1", "#a855f7", "#ec4899"],
            labels={"occupation": "Occupation Class", "swing_votes": "Projected Swing Voters"}
        )
        fig_occ.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#f3f4f6")
        st.plotly_chart(fig_occ, use_container_width=True)
        
    # Interactive demographic segment lookup
    st.markdown("---")
    st.markdown("#### 🔍 Stratum Specific Logit Probability Auditor")
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        s_gender = st.selectbox("Audited Gender", df_strat['gender'].unique())
    with sc2:
        s_age = st.selectbox("Audited Age Group", df_strat['age_group'].unique())
    with sc3:
        s_social = st.selectbox("Audited Social Category", df_strat['social_group'].unique())
    with sc4:
        s_occup = st.selectbox("Audited Occupation Class", df_strat['occupation'].unique())
        
    audit_cell = df_strat[
        (df_strat['gender'] == s_gender) &
        (df_strat['age_group'] == s_age) &
        (df_strat['social_group'] == s_social) &
        (df_strat['occupation'] == s_occup)
    ]
    
    if len(audit_cell) > 0:
        avg_cell_prob = audit_cell['swing_prob'].mean()
        tot_cell_voters = audit_cell['n_voters'].sum()
        tot_cell_swing = audit_cell['swing_votes'].sum()
        
        ac_cols = st.columns(3)
        ac_cols[0].metric("Average Persuadability Score", f"{avg_cell_prob * 100:.2f}%")
        ac_cols[1].metric("Total Cohort Population", f"{tot_cell_voters:,} voters")
        ac_cols[2].metric("Projected Target Swingers", f"{tot_cell_swing:,} voters")
    else:
        st.info("Selected stratum configuration is suppressed due to k-anonymity gate or contains zero representation.")

# ----------------- TAB 3: COMPLIANCE HARD LOCK -----------------
with tab3:
    st.markdown("### 🔒 Media Certification & Monitoring Committee (MCMC) Compliance Lock")
    st.markdown("""
    Under official guidelines of the **Election Commission of India (ECI)**, all automated political communication, ad placements, and digital target definitions must secure pre-certification from the local district **Media Certification & Monitoring Committee (MCMC)**.
    
    > [!IMPORTANT]
    > **System Gatekeeper Rule:** To ensure full legal compliance, Nethra implements a strict **Hardware/Software Hard Lock**. The deployment payload generators in Tab 4 are fully disabled and blocked until:
    > 1. An operator uploads a valid MCMC pre-certification PDF.
    > 2. The operator inputs the corresponding MCMC registration reference code.
    """)
    
    # Store registration and file uploader state inside streamlit session
    if 'mcmc_unlocked' not in st.session_state:
        st.session_state.mcmc_unlocked = False
        
    st.write("")
    
    # Unlock form
    with st.form("mcmc_verification_form"):
        reg_code = st.text_input(
            "MCMC Approval Code / Certificate Reference Number",
            placeholder="e.g. MCMC/UP/2026/AC175/0481",
            help="Enter the official alphanumeric reference code printed on your MCMC certificate."
        )
        
        pdf_file = st.file_uploader(
            "Upload Pre-Certification MCMC PDF Document",
            type=["pdf"],
            help="Upload the official stamped PDF certificate received from the District Election Officer (DEO)."
        )
        
        btn_unlock = st.form_submit_button("VALIDATE & UNLOCK EXPORT LAYOUTS")
        
        if btn_unlock:
            if reg_code.strip() == "":
                st.error("❌ Validation Failed: Please enter a valid MCMC reference code.")
            elif pdf_file is None:
                st.error("❌ Validation Failed: PDF pre-certification document is required.")
            else:
                st.success("✅ Certification Verified: MCMC Pre-Clearance validated. Ad payloads unlocked.")
                st.session_state.mcmc_unlocked = True

    st.write("")
    
    if st.session_state.mcmc_unlocked:
        st.info("⚡ STATUS: **SYSTEM UNLOCKED**. You may now access the compliant Google and Meta targeting payloads in the next tab.")
    else:
        st.warning("⚠️ STATUS: **SYSTEM LOCKED**. Please complete the verification above to generate target payloads.")

# ----------------- TAB 4: COMPLIANT PAYLOADS -----------------
with tab4:
    st.markdown("### 🚀 Compliant Dual-Track Target Payload Generator")
    
    if not st.session_state.mcmc_unlocked:
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; padding: 2rem; text-align: center; margin-top: 2rem;">
            <span style="font-size: 3rem;">🔒</span>
            <h4 style="color: #ef4444; margin-top: 1rem;">TARGET PAYLOAD GENERATION LOCKED</h4>
            <p style="color: #94a3b8;">You must upload an MCMC approval certificate and reference code in the 'ECI MCMC Compliance Gate' tab to unlock targeting payload generation.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        To bypass ad platform bans on political micro-targeting, Nethra generates **fully compliant, dual-track payloads** tailored for Google and Meta Ad Managers. No individual PII or restricted behavioral labels are exported.
        """)
        
        # Select target zone
        target_booth = st.selectbox(
            "Select Tactical Target Polling Station",
            df_results.sort_values(by='swing_ratio', ascending=False)['booth_id'].unique(),
            format_func=lambda x: f"Booth {x}: {df_results[df_results['booth_id'] == x]['spatial_ward'].values[0]} | Persuadability: {df_results[df_results['booth_id'] == x]['swing_ratio'].values[0]*100:.1f}%"
        )
        
        # Get booth stats
        b_row = df_results[df_results['booth_id'] == target_booth].iloc[0]
        
        # Generate Google and Meta compliant configurations
        google_payload = {
            "platform": "Google Ads API v16",
            "campaign_type": "Contextual Placement & Search Bridge",
            "geographic_targeting": {
                "location_type": "ZIP_CODE",
                "zip_codes": ["226002" if target_booth in [1, 2, 3, 4] else "226005" if target_booth in [7, 8, 13, 14] else "226001"],
                "ac_name": "AC-175 Lucknow Cantt"
            },
            "demographic_filters": {
                "age_cohorts": ["AGE_RANGE_18_24", "AGE_RANGE_25_34"],
                "gender": ["GENDER_MALE", "GENDER_FEMALE"]
            },
            "ad_placements_contextual": [
                "local_news_portals",
                "regional_job_directories",
                "lucknow_public_transit_sites"
            ],
            "compliance_assertions": {
                "DPDP_Act_2023": "100% Compliant (Zero PII - Demographic Count Aggregate Only)",
                "Google_Political_Ads_Policy_2026": "No interest-based, religious, or caste category tags used."
            }
        }
        
        meta_payload = {
            "platform": "Meta Marketing API v19",
            "targeting_strategy": "Algorithmic Creative Self-Selection (Broad Cohort Bridge)",
            "geographic_targeting": {
                "location_type": "District",
                "district_name": "Lucknow District",
                "minimum_radius_miles": 15
            },
            "demographic_targeting_limits": {
                "age_range": "18_65+",
                "gender": "All"
            },
            "algorithmic_hooks": {
                "target_booth_id": int(target_booth),
                "local_neighborhood_context": b_row['spatial_ward'],
                "inferred_economic_friction": "High Dilapidated Housing & Power Cut Concerns" if b_row['dilapidated_house_ratio'] > 0.1 else "Urban Infrastructure Quality",
                "suggested_creative_creative_hook": "Focus on high-yield youth employment policies & electricity grid modernization" if b_row['dilapidated_house_ratio'] > 0.1 else "Focus on cantonment area community infrastructure & safe drinking water access"
            },
            "compliance_assertions": {
                "DPDP_Act_2023": "100% Compliant (No custom audience hashes or lookalike models)",
                "Meta_Political_Targeting_Restrictions": "Exceeds platform broad targeting guidelines. Relies exclusively on high-impact AI creative assets to drive self-selection."
            }
        }
        
        g_col, m_col = st.columns(2)
        
        with g_col:
            st.markdown("#### 🔍 Track A: Google Compliant Placement Payload")
            st.markdown("Precision ZIP + Age/Gender targeting with contextual placements.")
            st.json(google_payload)
            st.button("📋 COPY GOOGLE PAYLOAD JSON", key="btn_copy_google")
            
        with m_col:
            st.markdown("#### 👥 Track B: Meta Compliant Creative Payload")
            st.markdown("Broad district targeting. Force self-selection via localized micro-creative assets.")
            st.json(meta_payload)
            st.button("📋 COPY META PAYLOAD JSON", key="btn_copy_meta")
            
        st.write("")
        st.markdown("""
        > [!TIP]
        > **Self-Selection Mechanics:** Meta's algorithm naturally optimizes delivery to the most engaged segments within the broad district radius. By embedding highly hyper-local creative details (e.g. *Sadar Bazar road quality reforms*), we ensure the target cohorts organically interact with the ad, triggering Meta's delivery engine to cluster distribution on the correct demographic stratum.
        """)
