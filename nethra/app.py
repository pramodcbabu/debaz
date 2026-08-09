# app.py
"""Nethra — UP 2027 MRP Election Intelligence Prototype

A Streamlit dashboard for booth-level vote-share prediction using
Multilevel Regression and Poststratification (MRP).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from src.mrp_engine import MRPEngine, MRPConfig, IS_MOCK

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nethra · UP 2027 Election Intelligence",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

.metric-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    color: #f1f5f9;
}
.metric-card .label  { font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-card .value  { font-size: 1.9rem; font-weight: 700; color: #38bdf8; line-height: 1.15; }
.metric-card .sublbl { font-size: 0.75rem; color: #64748b; }

.safe-badge      { background:#166534; color:#bbf7d0; padding:2px 10px; border-radius:999px; font-size:0.75rem; font-weight:600; }
.marginal-badge  { background:#92400e; color:#fef3c7; padding:2px 10px; border-radius:999px; font-size:0.75rem; font-weight:600; }
.atrisk-badge    { background:#7f1d1d; color:#fecaca; padding:2px 10px; border-radius:999px; font-size:0.75rem; font-weight:600; }

.section-header {
    font-size: 1.05rem; font-weight: 600; color: #e2e8f0;
    border-left: 3px solid #38bdf8; padding-left: 0.6rem;
    margin: 1.2rem 0 0.6rem 0;
}

div[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:12px;margin-bottom:0.25rem">
  <span style="font-size:2rem">🗳️</span>
  <div>
    <div style="font-size:1.5rem;font-weight:700;color:#f1f5f9;line-height:1.1">
      Nethra · UP 2027 Election Intelligence
    </div>
    <div style="font-size:0.8rem;color:#64748b">
      Booth-level vote-share projections via Multilevel Regression &amp; Poststratification (MRP)
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if IS_MOCK:
    st.warning("⚠️ **Demo Mode** — Running with calibrated deterministic priors (PyMC not installed). "
               "Predictions use structural coefficients derived from UP 2022 Form 20 data. "
               "Install `pymc` for full Bayesian posterior inference.", icon="⚠️")

st.divider()

# ── Sidebar controls ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Model Settings")

    draws = st.slider("MCMC Draws (real mode)", 100, 2000, 500, step=100,
                      disabled=IS_MOCK,
                      help="Number of posterior samples (ignored in demo mode)")
    tune  = st.slider("MCMC Tune steps (real mode)", 100, 1000, 300, step=100,
                      disabled=IS_MOCK)

    st.divider()
    st.markdown("### 🎯 Prior Sensitivity (Demo)")

    gamma1_scale = st.slider("HV sensitivity (γ₁ multiplier)", 0.5, 2.0, 1.0, 0.1,
                             help="How much historical volatility drives swing")
    gamma2_scale = st.slider("HM sensitivity (γ₂ multiplier)", 0.5, 2.0, 1.0, 0.1,
                             help="How much historical margin drives incumbency advantage")

    st.divider()
    st.markdown("### 🔍 Filter Booths")
    swing_filter = st.multiselect(
        "Show BJP classification",
        ["BJP Safe (>60%)", "BJP Likely (52–60%)", "Swing Marginal (48–52%)", "SP Threat (BJP <52%)", "SP Likely Win"],
        default=["BJP Safe (>60%)", "BJP Likely (52–60%)", "Swing Marginal (48–52%)", "SP Threat (BJP <52%)", "SP Likely Win"]
    )

# ── Load & run model ────────────────────────────────────────────────────────────
DATA_DIR = Path("data")

@st.cache_resource(show_spinner="Loading data & running MRP model…")
def run_engine(draws, tune, g1, g2):
    import src.mrp_engine as eng_module
    # Apply sensitivity multipliers to global priors
    eng_module.GAMMA1 = 0.80 * g1
    eng_module.GAMMA2 = 0.60 * g2

    engine = MRPEngine(DATA_DIR, config=MRPConfig(draws=draws, tune=tune))
    engine.load_data()
    engine.build_model()
    engine.fit()
    pred = engine.predict()
    return engine, pred

engine, pred_df = run_engine(draws, tune, gamma1_scale, gamma2_scale)

# Apply swing filter
if swing_filter:
    pred_df_filtered = pred_df[pred_df["swing_label"].isin(swing_filter)]
else:
    pred_df_filtered = pred_df

# ── Summary KPI cards ──────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

avg_bjp    = pred_df["bjp_share"].mean()
avg_sp     = pred_df["sp_share"].mean()
n_safe     = pred_df["swing_label"].isin(["BJP Safe (>60%)", "BJP Likely (52–60%)"]).sum()
n_swing    = pred_df["swing_label"].isin(["Swing Marginal (48–52%)", "SP Threat (BJP <52%)"]).sum()
swing_v    = pred_df.loc[pred_df["swing_label"].isin(["Swing Marginal (48–52%)", "SP Threat (BJP <52%)"]), "total_voters"].sum()
avg_lead   = pred_df["bjp_lead"].mean()

with col1:
    st.markdown(f"""<div class="metric-card">
      <div class="label">Avg BJP Projected Share</div>
      <div class="value" style="color:#fb923c">{avg_bjp:.1%}</div>
      <div class="sublbl">vs SP ~{avg_sp:.1%} · Across {len(pred_df)} booths</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="metric-card">
      <div class="label">BJP Safe/Likely Booths</div>
      <div class="value" style="color:#4ade80">{n_safe}</div>
      <div class="sublbl">BJP share &gt;52% projected</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="metric-card">
      <div class="label">Swing / At-Risk Booths</div>
      <div class="value" style="color:#f97316">{n_swing}</div>
      <div class="sublbl">Booths where SP can close gap</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""<div class="metric-card">
      <div class="label">Swing-Zone Voters</div>
      <div class="value" style="color:#f472b6">{swing_v:,}</div>
      <div class="sublbl">Voters in contested booths</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Map ─────────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📍 Booth-Level BJP vs SP Projection Map</div>', unsafe_allow_html=True)
st.caption("Colour = BJP classification for UP 2027 · Bubble size = registered voters · Hover for BJP/SP shares")

COLOR_MAP = {
    "BJP Safe (>60%)": "#f97316",
    "BJP Likely (52–60%)": "#fbbf24",
    "Swing Marginal (48–52%)": "#a78bfa",
    "SP Threat (BJP <52%)": "#38bdf8",
    "SP Likely Win": "#22d3ee",
}

fig_map = px.scatter_mapbox(
    pred_df_filtered,
    lat="lat", lon="lon",
    color="swing_label",
    color_discrete_map=COLOR_MAP,
    size="total_voters",
    size_max=22,
    zoom=11,
    center={"lat": pred_df["lat"].mean(), "lon": pred_df["lon"].mean()},
    mapbox_style="carto-darkmatter",
    hover_name="booth_id",
    hover_data={
        "predicted_share": ":.1%",
        "total_voters":    True,
        "historical_volatility_index": ":.3f",
        "historical_margin_of_victory": ":.3f",
        "wealth_index":    ":.2f",
        "lat": False, "lon": False,
    },
    custom_data=["predicted_share", "total_voters"],
    height=500,
)
fig_map.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    legend=dict(title="Swing Classification", font=dict(color="#e2e8f0"),
                bgcolor="rgba(15,23,42,0.8)", bordercolor="#334155", borderwidth=1),
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_map, use_container_width=True)

# ── Charts row ─────────────────────────────────────────────────────────────────
c_left, c_right = st.columns(2)

with c_left:
    st.markdown('<div class="section-header">📊 BJP vs SP — Projected Share by Booth</div>',
                unsafe_allow_html=True)
    st.caption("Orange = BJP · Blue = SP · Both expressed as % of total valid votes")

    booths_sorted = pred_df_filtered.sort_values("booth_id")["booth_id"].astype(str)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=pred_df_filtered.sort_values("booth_id")["booth_id"].astype(str),
        y=pred_df_filtered.sort_values("booth_id")["bjp_share"],
        name="BJP",
        marker_color="#f97316",
        hovertemplate="Booth %{x}<br>BJP: %{y:.1%}<extra></extra>",
    ))
    fig_bar.add_trace(go.Bar(
        x=pred_df_filtered.sort_values("booth_id")["booth_id"].astype(str),
        y=pred_df_filtered.sort_values("booth_id")["sp_share"],
        name="SP",
        marker_color="#38bdf8",
        hovertemplate="Booth %{x}<br>SP: %{y:.1%}<extra></extra>",
    ))
    fig_bar.add_hline(y=0.50, line_dash="dot", line_color="#94a3b8",
                      annotation_text="50% majority line", annotation_position="top right")
    fig_bar.update_layout(
        barmode="group",
        yaxis=dict(tickformat=".0%", range=[0.0, 0.80], title="Projected Vote Share"),
        xaxis=dict(title="Booth ID"),
        plot_bgcolor="#0f172a", paper_bgcolor="#0f172a",
        font=dict(color="#e2e8f0"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        height=360,
        margin=dict(t=10, b=10),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with c_right:
    st.markdown('<div class="section-header">📈 BJP Lead vs Historical Margin (HM)</div>',
                unsafe_allow_html=True)
    st.caption("Each point = one booth. BJP lead = BJP% − SP%. Colour = BJP classification.")

    fig_scatter = px.scatter(
        pred_df_filtered,
        x="historical_margin_of_victory",
        y="bjp_lead",
        color="swing_label",
        color_discrete_map=COLOR_MAP,
        size="total_voters",
        size_max=18,
        hover_name="booth_id",
        hover_data={"bjp_share": ":.1%", "sp_share": ":.1%", "bjp_lead": ":.1%"},
        labels={
            "historical_margin_of_victory": "Historical Margin of Victory (HM, 2022)",
            "bjp_lead": "Projected BJP Lead over SP",
        },
        height=360,
    )
    fig_scatter.add_hline(y=0.0, line_dash="solid", line_color="#ef4444",
                          annotation_text="SP = BJP (toss-up line)", annotation_position="bottom right")
    fig_scatter.update_layout(
        plot_bgcolor="#0f172a", paper_bgcolor="#0f172a",
        font=dict(color="#e2e8f0"),
        legend=dict(bgcolor="rgba(0,0,0,0)", title="BJP Status"),
        margin=dict(t=10, b=10),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ── Booth detail table ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🗂️ Booth-Level Prediction Table</div>',
            unsafe_allow_html=True)

display_cols = [
    "booth_id", "bjp_share", "sp_share", "bjp_lead",
    "ci_lower", "ci_upper", "swing_label", "total_voters",
    "historical_volatility_index", "historical_margin_of_victory",
]
table_df = pred_df_filtered[display_cols].copy()
for col in ["bjp_share", "sp_share", "bjp_lead", "ci_lower", "ci_upper"]:
    table_df[col] = table_df[col].map("{:+.1%}".format if col == "bjp_lead" else "{:.1%}".format)
table_df.columns = [
    "Booth ID", "BJP Share (proj.)", "SP Share (proj.)", "BJP Lead",
    "CI Lower", "CI Upper", "BJP Status", "Voters",
    "HV Index", "HM Index (2022)",
]
st.dataframe(table_df, use_container_width=True, hide_index=True)

# ── Demographic breakdown ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">👥 Demographic Strata Breakdown</div>',
            unsafe_allow_html=True)

# Aggregated by booth first
merged = engine.df.copy()
merged["_share"] = engine._deterministic_share(merged)

# Booth-level demographic composition
demo_agg = (
    merged.groupby(["booth_id","social_group"])["n_voters"]
    .sum().unstack(fill_value=0).reset_index()
)
demo_agg.columns.name = None

# Social group % per booth
soc_cols = [c for c in demo_agg.columns if c != "booth_id"]
total_per_booth = demo_agg[soc_cols].sum(axis=1)
for c in soc_cols:
    demo_agg[c + " %"] = (demo_agg[c] / total_per_booth * 100).round(1)

st.caption("All 15 booths · social group composition and predicted vote share")
display_demo = demo_agg[["booth_id"] + [c+" %" for c in soc_cols]].merge(
    pred_df[["booth_id","predicted_share","swing_label"]], on="booth_id"
)
display_demo["predicted_share"] = display_demo["predicted_share"].map("{:.1%}".format)
st.dataframe(display_demo, use_container_width=True, hide_index=True)

# Drill-down by booth
with st.expander("🔍 Stratum-level drill-down — select a booth"):
    selected_booth = st.selectbox(
        "Booth", sorted(merged["booth_id"].unique()), key="booth_drilldown"
    )
    booth_rows = merged[merged["booth_id"] == selected_booth][
        ["booth_id","gender","age_group","social_group","occupation","n_voters","_share"]
    ].copy()
    booth_rows["_share"] = booth_rows["_share"].map("{:.1%}".format)
    booth_rows.columns = ["Booth","Gender","Age Group","Social Group","Occupation","Voters","Pred. Share"]
    st.dataframe(booth_rows, use_container_width=True, hide_index=True)

# ── Download ───────────────────────────────────────────────────────────────────
st.divider()
dl_csv = pred_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Full Predictions (CSV)",
    data=dl_csv,
    file_name="nethra_up2027_predictions.csv",
    mime="text/csv",
)

st.caption("Nethra Prototype · Demo mode with calibrated priors · Not for public distribution")
