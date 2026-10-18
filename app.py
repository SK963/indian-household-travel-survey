import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="National Household Travel & Domestic Tourism Survey (NHTS 2025-26)",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS FOR MODERN, SLEEK AESTHETICS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
        border-radius: 20px;
        padding: 32px 36px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .badge-pill {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .badge-blue { background: rgba(59, 130, 246, 0.2); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.4); }
    .badge-emerald { background: rgba(16, 185, 129, 0.2); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.4); }
    .badge-amber { background: rgba(245, 158, 11, 0.2); color: #fcd34d; border: 1px solid rgba(245, 158, 11, 0.4); }
    .badge-purple { background: rgba(168, 85, 247, 0.2); color: #d8b4fe; border: 1px solid rgba(168, 85, 247, 0.4); }
    
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    .metric-value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.1;
        margin-top: 6px;
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #10b981;
        font-weight: 600;
        margin-top: 6px;
    }
    
    .insight-box {
        background: #f8fafc;
        border-left: 4px solid #6366f1;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 16px 0;
        color: #1e293b;
    }
    
    .section-divider {
        margin: 28px 0 16px 0;
        padding-bottom: 6px;
        border-bottom: 2px solid #f1f5f9;
        font-weight: 800;
        font-size: 1.15rem;
        color: #1e293b;
    }
    
    div[data-testid="stMetricValue"] {
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING UTILITY
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    out_dir = Path("output")
    data = {}
    
    if (out_dir / "nhts_report_key_indicators.csv").exists():
        data["indicators"] = pd.read_csv(out_dir / "nhts_report_key_indicators.csv")
    if (out_dir / "table4_worker_modes.csv").exists():
        data["worker_modes"] = pd.read_csv(out_dir / "table4_worker_modes.csv")
    if (out_dir / "table2_student_modes.csv").exists():
        data["student_modes"] = pd.read_csv(out_dir / "table2_student_modes.csv")
    if (out_dir / "table5_daily_trip_purposes.csv").exists():
        data["daily_purposes"] = pd.read_csv(out_dir / "table5_daily_trip_purposes.csv")
    if (out_dir / "fig5_monthly_commute_costs.csv").exists():
        data["costs"] = pd.read_csv(out_dir / "fig5_monthly_commute_costs.csv")
    if (out_dir / "tourism_seasonality.csv").exists():
        data["seasonality"] = pd.read_csv(out_dir / "tourism_seasonality.csv")
    if (out_dir / "top_destination_states.csv").exists():
        data["top_states"] = pd.read_csv(out_dir / "top_destination_states.csv")
    if (out_dir / "spend_categories.csv").exists():
        data["spend_categories"] = pd.read_csv(out_dir / "spend_categories.csv")
        
    return data

DATA = load_data()

# -----------------------------------------------------------------------------
# CHART BUILDER HELPER FUNCTIONS (MODULAR & REUSABLE)
# -----------------------------------------------------------------------------
def build_worker_modes_fig():
    if "worker_modes" not in DATA:
        return None
    df = DATA["worker_modes"]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["Primary Mode"][:8],
        x=df["Rural (%)"][:8],
        name="Rural",
        orientation='h',
        marker=dict(color="#3b82f6")
    ))
    fig.add_trace(go.Bar(
        y=df["Primary Mode"][:8],
        x=df["Urban (%)"][:8],
        name="Urban",
        orientation='h',
        marker=dict(color="#f97316")
    ))
    fig.add_trace(go.Bar(
        y=df["Primary Mode"][:8],
        x=df["Rural+Urban (%)"][:8],
        name="All-India",
        orientation='h',
        marker=dict(color="#10b981")
    ))
    fig.update_layout(
        barmode='group',
        title="Primary Mode of Transport for Workers (Age 15+)",
        xaxis_title="Share of Workers (%)",
        yaxis=dict(autorange="reversed"),
        template="plotly_white",
        height=400,
        margin=dict(l=10, r=10, t=50, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def build_transit_hotspots_fig():
    transit_df = pd.DataFrame({
        "State / Region": ["All-India (Urban)", "Delhi", "West Bengal", "Maharashtra"],
        "Mass Transit Share (%)": [5.0, 14.4, 16.5, 20.7]
    })
    fig = px.bar(
        transit_df,
        x="Mass Transit Share (%)",
        y="State / Region",
        orientation='h',
        text="Mass Transit Share (%)",
        color="Mass Transit Share (%)",
        color_continuous_scale="Purples",
        title="Suburban Rail & Metro Commute Share (Hotspots)"
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(template="plotly_white", height=400, margin=dict(l=10, r=10, t=50, b=30), showlegend=False)
    return fig

def build_gender_gap_fig():
    gender_prop = pd.DataFrame({
        "Sector": ["Rural", "Rural", "Urban", "Urban", "Rural+Urban", "Rural+Urban"],
        "Gender": ["Male", "Female", "Male", "Female", "Male", "Female"],
        "Trip Participation Rate (%)": [59.6, 37.7, 66.6, 52.9, 61.9, 41.9]
    })
    fig = px.bar(
        gender_prop,
        x="Sector",
        y="Trip Participation Rate (%)",
        color="Gender",
        barmode="group",
        text="Trip Participation Rate (%)",
        color_discrete_map={"Male": "#2563eb", "Female": "#ec4899"},
        title="Worker Commute Trip Participation Rate by Gender"
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        template="plotly_white", 
        yaxis=dict(range=[0, 80]), 
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def build_student_modes_fig():
    if "student_modes" not in DATA:
        return None
    df = DATA["student_modes"]
    fig = px.bar(
        df.head(6),
        x="Primary Mode",
        y=["Age 6-14 years (%)", "Age 15-29 years (%)", "Age 6 years & above (%)"],
        barmode="group",
        title="Primary Travel Mode for Students by Age Group",
        color_discrete_sequence=["#0ea5e9", "#8b5cf6", "#10b981"]
    )
    fig.update_layout(
        template="plotly_white", 
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def build_student_departure_fig():
    df = pd.DataFrame({
        "Departure Window": ["Before 7 AM", "7–8 AM", "8–9 AM", "9–10 AM", "After 10 AM"],
        "Student Share (%)": [10.9, 26.6, 35.7, 19.7, 7.1]
    })
    fig = px.line(
        df,
        x="Departure Window",
        y="Student Share (%)",
        markers=True,
        title="Student Departure Times (Peak: 8:00–9:00 AM)",
        color_discrete_sequence=["#2563eb"]
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(template="plotly_white", yaxis=dict(range=[0, 45]), height=360)
    return fig

def build_worker_departure_fig():
    df = pd.DataFrame({
        "Departure Window": [
            "Before 6 AM", "6–8 AM", "8–10 AM", "10 AM–12 PM", 
            "12–4 PM", "4–6 PM", "6–8 PM", "After 8 PM"
        ],
        "Rural (%)": [5.2, 36.1, 54.4, 2.5, 0.9, 0.4, 0.3, 0.2],
        "Urban (%)": [4.0, 29.8, 59.8, 3.8, 1.3, 0.6, 0.4, 0.3],
        "All-India (%)": [4.7, 33.7, 56.5, 3.2, 1.1, 0.5, 0.3, 0.2]
    })
    fig = px.line(
        df,
        x="Departure Window",
        y=["Rural (%)", "Urban (%)", "All-India (%)"],
        markers=True,
        title="Worker Departure Times (Peak: 8:00–10:00 AM)",
        color_discrete_sequence=["#3b82f6", "#f97316", "#10b981"]
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=7))
    fig.update_layout(
        template="plotly_white", 
        yaxis=dict(range=[0, 70]), 
        height=360,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def build_commute_costs_fig():
    if "costs" not in DATA:
        return None
    df = DATA["costs"]
    fig = px.bar(
        df,
        x="Sector",
        y=["Male Workers (INR)", "Female Workers (INR)", "All Workers (INR)", "Students (INR)"],
        barmode="group",
        title="Average Monthly Commute Expenditure (INR)",
        color_discrete_sequence=["#2563eb", "#ec4899", "#10b981", "#f59e0b"]
    )
    fig.update_layout(
        template="plotly_white", 
        height=380, 
        yaxis_title="Monthly Cost in Rs.",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def build_overnight_modes_fig():
    df = pd.DataFrame({
        "Mode": ["Bus", "Railways", "Car", "Two-wheeler", "Others / Air / Water"],
        "Share (%)": [55.8, 17.7, 15.1, 8.8, 2.6]
    })
    fig = px.pie(
        df,
        names="Mode",
        values="Share (%)",
        hole=0.45,
        title="Overnight Travel Modal Split (Bus + Rail: 73.5%)",
        color_discrete_sequence=["#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#94a3b8"]
    )
    fig.update_layout(template="plotly_white", height=370)
    return fig

def build_overnight_purposes_fig():
    df = pd.DataFrame({
        "Leading Purpose": [
            "Social, Communication & Religious",
            "Culture, Leisure, Sports & Tourism",
            "Self-care & Maintenance (Health)",
            "Other Purposes (Business, etc.)"
        ],
        "All-India (%)": [70.2, 7.4, 6.5, 15.9]
    })
    fig = px.bar(
        df,
        x="All-India (%)",
        y="Leading Purpose",
        orientation='h',
        text="All-India (%)",
        title="Overnight Travel Motivations (Social/Religious: 70.2%)",
        color="All-India (%)",
        color_continuous_scale="Viridis"
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(template="plotly_white", height=370, showlegend=False)
    return fig

def build_seasonality_fig():
    if "seasonality" not in DATA:
        return None
    fig = px.line(
        DATA["seasonality"],
        x="Month",
        y="Trips",
        markers=True,
        title="Seasonality of Domestic Travel (Monthly Sample Trips)",
        color_discrete_sequence=["#8b5cf6"]
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(template="plotly_white", height=370)
    return fig

def build_top_states_fig():
    if "top_states" not in DATA:
        return None
    fig = px.bar(
        DATA["top_states"],
        x="Trips",
        y="State",
        orientation='h',
        title="Top 10 Destination States for Overnight Travel",
        color="Trips",
        color_continuous_scale="Blues"
    )
    fig.update_layout(template="plotly_white", height=370, yaxis=dict(autorange="reversed"), showlegend=False)
    return fig

def build_spend_categories_fig():
    if "spend_categories" not in DATA:
        return None
    fig = px.pie(
        DATA["spend_categories"],
        names="Category",
        values="Total Sample Spend (Cr ₹)",
        hole=0.45,
        title="Breakdown of Sample Expenditure (Rs. 259.6 Crores Total)",
        color_discrete_sequence=["#ef4444", "#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6"]
    )
    fig.update_layout(template="plotly_white", height=370)
    return fig

def build_daily_modes_fig():
    df = pd.DataFrame({
        "Transport Mode": ["Two-wheeler", "Walk", "Auto-rickshaw", "Bicycle", "Bus", "Others"],
        "Trip Share (%)": [32.2, 24.9, 18.9, 12.6, 8.5, 2.9]
    })
    fig = px.bar(
        df,
        x="Transport Mode",
        y="Trip Share (%)",
        color="Transport Mode",
        text="Trip Share (%)",
        title="Primary Mode for Non-Work, Non-School Local Trips",
        color_discrete_sequence=["#3b82f6", "#10b981", "#f97316", "#8b5cf6", "#ec4899", "#94a3b8"]
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(template="plotly_white", height=370, showlegend=False, yaxis=dict(range=[0, 38]))
    return fig

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION & FILTERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/55/Emblem_of_India.svg", width=65)
    st.markdown("### **NSS 80th Round (2025–26)**")
    st.caption("National Statistics Office (NSO) | MoSPI")
    
    st.markdown("---")
    st.markdown("#### Filter & View Options")
    sector_filter = st.radio(
        "Geography / Sector Scope:",
        ["All-India (Rural + Urban)", "Rural Sector", "Urban Sector"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("#### Official Reference Documents")
    st.markdown("""
    * [NHTS Factsheet / Report](National%20Household%20Travel%20Survey%20Report.pdf)
    * [Field Instructions (Vol. I)](docs/DTES_Vol_I.pdf)
    * [Survey Schedules (Vol. II)](docs/DTES_Vol_II.pdf)
    * [Estimation Procedures](docs/Estimation_Procedure_DTES.pdf)
    * [Variable Layouts (Excel)](docs/Data_Layout80211.xlsx)
    """)
    
    st.markdown("---")
    st.caption("Microdata Identifier: `DDI-IND-MOSPI-NSSO-DTES-2025-26` | Schedule 21.1")

# -----------------------------------------------------------------------------
# MAIN HERO SECTION
# -----------------------------------------------------------------------------
st.markdown("""
<div class="main-hero">
    <div>
        <span class="badge-pill badge-blue">NSS 80th Round</span>
        <span class="badge-pill badge-emerald">July 2025 – June 2026</span>
        <span class="badge-pill badge-amber">MoSPI / NSO</span>
        <span class="badge-pill badge-purple">Schedule 21.1 Microdata</span>
    </div>
    <h1 style="color: white; margin-top: 14px; margin-bottom: 6px; font-weight: 800; font-size: 2.2rem;">
        National Household Travel & Domestic Tourism Survey
    </h1>
    <p style="color: #cbd5e1; font-size: 1.05rem; max-width: 900px; margin-bottom: 0;">
        Interactive benchmark intelligence dashboard exploring daily workforce and student commuting mobility, 
        travel expenditure disparities, peak congestion windows, and overnight domestic tourism patterns across India.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# KEY METRIC KPI ROW
# -----------------------------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Worker 2-Wheeler Share</div>
        <div class="metric-value">42.6%</div>
        <div class="metric-sub">52.3% in Urban Areas</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Overnight Bus + Rail</div>
        <div class="metric-value">73.5%</div>
        <div class="metric-sub">Bus 55.8% | Rail 17.7%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Avg Journey Time</div>
        <div class="metric-value">25 min</div>
        <div class="metric-sub">23 min for Students</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Monthly Commute Spend</div>
        <div class="metric-value">₹785</div>
        <div class="metric-sub">₹1,044 in Urban Areas</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Central Survey Sample</div>
        <div class="metric-value">246k</div>
        <div class="metric-sub">Households in 24,651 FSUs</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB NAVIGATION (MASTER VISUAL DASHBOARD FIRST)
# -----------------------------------------------------------------------------
tabs = st.tabs([
    "Master Visual Dashboard",
    "Executive Summary & Scorecard",
    "Workforce Mobility & Gender Gap",
    "Student Commuting",
    "Durations & Peak Hours",
    "Monthly Costs & Disparities",
    "Domestic Overnight Tourism",
    "Daily Short Trips",
    "Microdata Explorer"
])

# =============================================================================
# TAB 0: MASTER VISUAL DASHBOARD (ALL PRIMARY CHARTS IN ONE SEAMLESS VIEW)
# =============================================================================
with tabs[0]:
    st.markdown("""
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px 24px; margin-bottom: 24px;">
        <h3 style="margin-top: 0; margin-bottom: 6px; color: #0f172a; font-weight: 800;">
            Master Visual Dashboard: All Headline Charts at a Glance
        </h3>
        <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 0;">
            This main page consolidates all primary visual benchmarks across workforce commuting, student education access, 
            peak congestion rush curves, travel expenditures, and overnight tourism. Click on individual tabs for granular tables and deeper drill-downs.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Visual Row 1: Workforce Mobility & Mass Transit Surges
    st.markdown("<div class='section-divider'>1. Workforce Commuting & Mass Transit Surges</div>", unsafe_allow_html=True)
    col_r1_a, col_r1_b = st.columns(2)
    with col_r1_a:
        fig_wm = build_worker_modes_fig()
        if fig_wm: st.plotly_chart(fig_wm, use_container_width=True)
        st.caption("Key Insight: Two-wheelers carry 42.6% of Indian workers (52.3% urban). Walking & cycling account for ~39% combined.")
    with col_r1_b:
        fig_th = build_transit_hotspots_fig()
        if fig_th: st.plotly_chart(fig_th, use_container_width=True)
        st.caption("Key Insight: Metro and suburban rail surge in Maharashtra (20.7%), West Bengal (16.5%), and Delhi (14.4%) vs 5.0% national urban avg.")

    # Visual Row 2: Student Commuting & Gender Participation Divide
    st.markdown("<div class='section-divider'>2. Student Mode Transitions & Worker Gender Divide</div>", unsafe_allow_html=True)
    col_r2_a, col_r2_b = st.columns(2)
    with col_r2_a:
        fig_sm = build_student_modes_fig()
        if fig_sm: st.plotly_chart(fig_sm, use_container_width=True)
        st.caption("Key Insight: Walking drops in half from 47.3% (age 6-14) to 22.2% (15-29), while bicycles double to 21.4% in college.")
    with col_r2_b:
        fig_gg = build_gender_gap_fig()
        if fig_gg: st.plotly_chart(fig_gg, use_container_width=True)
        st.caption("Key Insight: Rural women have a 21.9% lower commute trip participation rate (37.7%) compared to men (59.6%).")

    # Visual Row 3: Peak Morning Rush Hour Curves
    st.markdown("<div class='section-divider'>3. Commute Peak Rush Hour Curves</div>", unsafe_allow_html=True)
    col_r3_a, col_r3_b = st.columns(2)
    with col_r3_a:
        fig_sd = build_student_departure_fig()
        if fig_sd: st.plotly_chart(fig_sd, use_container_width=True)
        st.caption("Key Insight: 82.0% of students depart between 7:00 and 10:00 AM, peaking sharply between 8:00 and 9:00 AM (35.7%).")
    with col_r3_b:
        fig_wd = build_worker_departure_fig()
        if fig_wd: st.plotly_chart(fig_wd, use_container_width=True)
        st.caption("Key Insight: 94.9% of workers leave before 10:00 AM, with 56.5% departing during the 8:00-10:00 AM rush.")

    # Visual Row 4: Monthly Commute Spend & Daily Non-Work Trips
    st.markdown("<div class='section-divider'>4. Commute Expenditure Disparities & Local Mobility</div>", unsafe_allow_html=True)
    col_r4_a, col_r4_b = st.columns(2)
    with col_r4_a:
        fig_cc = build_commute_costs_fig()
        if fig_cc: st.plotly_chart(fig_cc, use_container_width=True)
        st.caption("Key Insight: Male workers spend Rs. 835/mo vs Rs. 533/mo for female workers. Rural men spend more than double women (Rs. 674 vs Rs. 307).")
    with col_r4_b:
        fig_dm = build_daily_modes_fig()
        if fig_dm: st.plotly_chart(fig_dm, use_container_width=True)
        st.caption("Key Insight: Two-wheelers (32.2%), walking (24.9%), and auto-rickshaws (18.9%) lead short within-day local mobility.")

    # Visual Row 5: Domestic Overnight Tourism Modes & Motivations
    st.markdown("<div class='section-divider'>5. Domestic Overnight Tourism: Transport Modes & Motivations</div>", unsafe_allow_html=True)
    col_r5_a, col_r5_b = st.columns(2)
    with col_r5_a:
        fig_om = build_overnight_modes_fig()
        if fig_om: st.plotly_chart(fig_om, use_container_width=True)
        st.caption("Key Insight: Public transport anchors overnight travel: Buses (55.8%) and Railways (17.7%) carry 73.5% of all journeys.")
    with col_r5_b:
        fig_op = build_overnight_purposes_fig()
        if fig_op: st.plotly_chart(fig_op, use_container_width=True)
        st.caption("Key Insight: Social visits and religious pilgrimages represent 70.2% of all domestic overnight travel.")

    # Visual Row 6: Tourism Seasonality & Top Destinations
    st.markdown("<div class='section-divider'>6. Travel Seasonality & Top Destination States</div>", unsafe_allow_html=True)
    col_r6_a, col_r6_b = st.columns(2)
    with col_r6_a:
        fig_se = build_seasonality_fig()
        if fig_se: st.plotly_chart(fig_se, use_container_width=True)
        st.caption("Key Insight: Domestic travel surges in February (pilgrimage season), May (summer holidays), and August-October (festive season).")
    with col_r6_b:
        fig_ts = build_top_states_fig()
        if fig_ts: st.plotly_chart(fig_ts, use_container_width=True)
        st.caption("Key Insight: Uttar Pradesh leads nationwide due to massive pilgrimage hubs (Varanasi, Ayodhya, Mathura, Prayagraj).")

    # Visual Row 7: Expenditure Breakdown
    st.markdown("<div class='section-divider'>7. Itemized Travel Spend Breakdown</div>", unsafe_allow_html=True)
    col_r7_a, col_r7_b = st.columns([3, 2])
    with col_r7_a:
        fig_sc = build_spend_categories_fig()
        if fig_sc: st.plotly_chart(fig_sc, use_container_width=True)
    with col_r7_b:
        st.markdown("""
        <div class="insight-box" style="margin-top: 30px;">
            <b>Where Household Travel Money Goes:</b>
            <ul style="margin-top: 8px; padding-left: 20px;">
                <li><b>Medical Expenses</b>: Medical travel is the largest single financial drain, averaging <b>Rs. 13,751 per trip</b> (Rs. 121.4 Cr in sample).</li>
                <li><b>Transport & Lodging</b>: Transport accounts for Rs. 40.1 Cr and Accommodation Rs. 31.6 Cr.</li>
                <li><b>Digital Booking Gap</b>: Only 17.0% of trips booked accommodation or transit directly online; 46.0% booked directly offline.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# TAB 1: EXECUTIVE SUMMARY & SCORECARD
# =============================================================================
with tabs[1]:
    st.markdown("### Headline National Findings")
    
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown("""
        <div class="insight-box">
            <b>Key Strategic Takeaways from the Official MoSPI Survey Report:</b>
            <ul style="margin-top: 8px; margin-bottom: 0; padding-left: 20px;">
                <li><b>Two-Wheelers are the Engine of India's Workforce</b>: 42.6% of all workers use two-wheelers for commuting, surging to 52.3% in urban India.</li>
                <li><b>Active Transport Carries 40% of Commuters</b>: Walking (28.3%) and Bicycles (10.7%) form a massive green mobility backbone, especially in rural districts.</li>
                <li><b>Mass Transit Regional Spikes</b>: Suburban rail, metro, monorail, and trams carry 5.0% of urban workers nationwide, but usage reaches <b>20.7% in Maharashtra</b>, <b>16.5% in West Bengal</b>, and <b>14.4% in Delhi</b>.</li>
                <li><b>High Commute Efficiency (<30 Mins)</b>: 87.6% of students and 83.4% of workers reach their destination in under half an hour.</li>
                <li><b>Significant Gender Mobility Spend Gap</b>: Nationally, male workers spend Rs. 835/month on fixed-workplace commutes versus Rs. 533/month for women. In rural India, men spend more than double (Rs. 674 vs Rs. 307).</li>
                <li><b>Public Transport Anchors Overnight Travel</b>: Buses (55.8%) and inter-city rail (17.7%) carry 73.5% of all household overnight trips.</li>
                <li><b>Social & Religious Motivations Rule</b>: 70.2% of overnight household journeys are driven by social visits and religious pilgrimages.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if "worker_modes" in DATA:
            df_wm = DATA["worker_modes"]
            fig_overview = px.bar(
                df_wm.head(6),
                x="Primary Mode",
                y=["Rural (%)", "Urban (%)", "Rural+Urban (%)"],
                barmode="group",
                title="Primary Commuting Mode by Sector (Top 6 Modes)",
                color_discrete_sequence=["#3b82f6", "#f97316", "#10b981"]
            )
            fig_overview.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20), height=360)
            st.plotly_chart(fig_overview, use_container_width=True)
            
    with col_b:
        st.markdown("#### Core Indicators Scorecard")
        if "indicators" in DATA:
            st.dataframe(
                DATA["indicators"][["Domain", "Indicator", "All-India"]],
                use_container_width=True,
                height=480,
                hide_index=True
            )

# =============================================================================
# TAB 2: WORKFORCE MOBILITY & GENDER GAP
# =============================================================================
with tabs[2]:
    st.markdown("### Workforce Commuting & The Gender Mobility Divide")
    
    col_w1, col_w2 = st.columns([3, 2])
    with col_w1:
        fig_wm = build_worker_modes_fig()
        if fig_wm: st.plotly_chart(fig_wm, use_container_width=True)
            
    with col_w2:
        st.markdown("#### Urban Mass Transit Surges")
        fig_th = build_transit_hotspots_fig()
        if fig_th: st.plotly_chart(fig_th, use_container_width=True)
        
        st.markdown("""
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 12px 16px; border-radius: 12px; font-size: 0.88rem;">
            <b>Mass Transit Hotspots</b>: While metro and suburban rail account for only 5.0% of urban commutes nationwide, 
            over <b>1 in 5 urban workers in Maharashtra (20.7%)</b> rely on local suburban trains and metro systems.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Gender Gap in Commute Trip Participation (Table 3)")
    
    col_g1, col_g2 = st.columns([3, 2])
    with col_g1:
        fig_gg = build_gender_gap_fig()
        if fig_gg: st.plotly_chart(fig_gg, use_container_width=True)
        
    with col_g2:
        st.markdown("""
        <div class="insight-box" style="border-left-color: #ec4899;">
            <b>The Gender Commuting Divide:</b>
            <p style="margin-top: 8px;">
            In rural India, only <b>37.7% of women workers</b> report making daily travel trips to a workplace, 
            compared to <b>59.6% of men</b> — a massive <b>21.9% gap</b>. 
            This reflects a combination of home-based agricultural tasks, informal localized work, and severe lack of safe, dedicated rural mobility options for women.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# TAB 3: STUDENT COMMUTING
# =============================================================================
with tabs[3]:
    st.markdown("### Student Commuting Mobility (Age 6+)")
    
    col_s1, col_s2 = st.columns([3, 2])
    with col_s1:
        fig_sm = build_student_modes_fig()
        if fig_sm: st.plotly_chart(fig_sm, use_container_width=True)
            
    with col_s2:
        st.markdown("#### Mode Shift from School to College")
        st.markdown("""
        <div class="insight-box" style="border-left-color: #0ea5e9;">
            <b>Dramatic Travel Transition as Children Grow:</b>
            <ul style="margin-top: 8px; padding-left: 20px;">
                <li><b>Walking drops in half</b>: From <b>47.3%</b> among school children (6–14) to <b>22.2%</b> among youth (15–29) as institutions move further away from home.</li>
                <li><b>Bicycles surge</b>: Bicycle usage nearly doubles from <b>11.9%</b> to <b>21.4%</b>.</li>
                <li><b>Bus Reliance</b>: Buses carry <b>28.4%</b> of school children and <b>31.0%</b> of college students.</li>
                <li><b>Auto-rickshaws</b>: Expand from 7.7% to 14.6% in higher education.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# TAB 4: DURATIONS & PEAK HOURS
# =============================================================================
with tabs[4]:
    st.markdown("### Commute Durations & Rush Hour Curves")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        fig_sd = build_student_departure_fig()
        if fig_sd: st.plotly_chart(fig_sd, use_container_width=True)
        st.caption("**82.0%** of all students depart between 7:00 AM and 10:00 AM.")
        
    with col_d2:
        fig_wd = build_worker_departure_fig()
        if fig_wd: st.plotly_chart(fig_wd, use_container_width=True)
        st.caption("**94.9%** of workers depart before 10:00 AM (56.5% between 8:00–10:00 AM).")

# =============================================================================
# TAB 5: MONTHLY COSTS & DISPARITIES
# =============================================================================
with tabs[5]:
    st.markdown("### Monthly Commuting Costs & The Gender Mobility Tax")
    
    col_c1, col_c2 = st.columns([3, 2])
    with col_c1:
        fig_cc = build_commute_costs_fig()
        if fig_cc: st.plotly_chart(fig_cc, use_container_width=True)
            
    with col_c2:
        st.markdown("""
        <div class="insight-box" style="border-left-color: #f59e0b;">
            <b>Economic Burden of Commuting:</b>
            <ul style="margin-top: 8px; padding-left: 20px;">
                <li><b>Urban Cost Premium</b>: Workers in urban India spend an average of <b>Rs. 1,044/month</b> compared to <b>Rs. 612/month</b> in rural areas (a 70.6% premium).</li>
                <li><b>Female Spend Disparity</b>: Male workers spend Rs. 835/month versus Rs. 533/month for women nationally.</li>
                <li><b>Rural Disparity Ratio</b>: In rural areas, women spend only <b>Rs. 307/month</b> vs <b>Rs. 674/month</b> for men — reflecting higher dependence on walking and constrained willingness or ability to pay for motorized transit.</li>
                <li><b>Student Commute Costs</b>: Average Rs. 443/month nationally (Rs. 617 in urban centres vs Rs. 361 in villages).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# TAB 6: DOMESTIC OVERNIGHT TOURISM
# =============================================================================
with tabs[6]:
    st.markdown("### Domestic Overnight Tourism & Travel Patterns")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        fig_om = build_overnight_modes_fig()
        if fig_om: st.plotly_chart(fig_om, use_container_width=True)
        
    with col_t2:
        fig_op = build_overnight_purposes_fig()
        if fig_op: st.plotly_chart(fig_op, use_container_width=True)

    st.markdown("---")
    st.markdown("#### Empirical Microdata Deep-Dive (Levels 04 & 06)")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        fig_se = build_seasonality_fig()
        if fig_se: st.plotly_chart(fig_se, use_container_width=True)
        st.caption("Travel surges in **Feb** (auspicious pilgrimage season), **May** (summer school break), and **Aug/Oct** (festivals).")
            
    with col_e2:
        fig_ts = build_top_states_fig()
        if fig_ts: st.plotly_chart(fig_ts, use_container_width=True)
        st.caption("**Uttar Pradesh** leads overwhelmingly due to major pilgrimage centers (Varanasi, Ayodhya, Mathura, Prayagraj).")

    if "spend_categories" in DATA:
        st.markdown("#### Where Does the Domestic Traveler Spend? (Itemized Anatomy)")
        col_sp1, col_sp2 = st.columns([3, 2])
        with col_sp1:
            fig_sc = build_spend_categories_fig()
            if fig_sc: st.plotly_chart(fig_sc, use_container_width=True)
            
        with col_sp2:
            st.dataframe(DATA["spend_categories"], use_container_width=True, height=280, hide_index=True)
            st.markdown("""
            <div style="background: #fef2f2; border: 1px solid #fecaca; padding: 12px; border-radius: 10px; font-size: 0.85rem;">
                <b>Medical Spend Alert</b>: Healthcare/treatment is the largest single travel expenditure item, 
                averaging <b>Rs. 13,751 per medical trip</b>, demonstrating massive out-of-pocket healthcare travel in India.
            </div>
            """, unsafe_allow_html=True)

# =============================================================================
# TAB 7: DAILY SHORT TRIPS
# =============================================================================
with tabs[7]:
    st.markdown("### Daily Non-Work, Non-School Local Trips (Within 24 Hours)")
    
    col_sh1, col_sh2 = st.columns([3, 2])
    with col_sh1:
        fig_dm = build_daily_modes_fig()
        if fig_dm: st.plotly_chart(fig_dm, use_container_width=True)
        
    with col_sh2:
        if "daily_purposes" in DATA:
            st.markdown("#### Table (5): Purpose of Short Daily Trips")
            st.dataframe(DATA["daily_purposes"][["Rural+Urban (%)"]], use_container_width=True, height=360)
            st.caption("Over **54%** of daily trips serve unpaid household domestic needs (errands, grocery, caregiving).")

# =============================================================================
# TAB 8: MICRODATA EXPLORER
# =============================================================================
with tabs[8]:
    st.markdown("### Interactive Microdata & Benchmark Dataset Explorer")
    st.caption("Inspect and download the clean CSV tables generated from the NSS 80th Round survey.")
    
    selected_dataset = st.selectbox(
        "Select Dataset to Inspect:",
        [
            "Headline Indicators (26 Metrics)",
            "Worker Commuting Modes (Table 4)",
            "Student Commuting Modes (Table 2)",
            "Monthly Commute Costs (Fig 5)",
            "Daily Short Trip Purposes (Table 5)",
            "Tourism Seasonality by Month",
            "Top Destination States",
            "Itemized Spend Categories"
        ]
    )
    
    mapping = {
        "Headline Indicators (26 Metrics)": "indicators",
        "Worker Commuting Modes (Table 4)": "worker_modes",
        "Student Commuting Modes (Table 2)": "student_modes",
        "Monthly Commute Costs (Fig 5)": "costs",
        "Daily Short Trip Purposes (Table 5)": "daily_purposes",
        "Tourism Seasonality by Month": "seasonality",
        "Top Destination States": "top_states",
        "Itemized Spend Categories": "spend_categories"
    }
    
    key = mapping[selected_dataset]
    if key in DATA:
        df_target = DATA[key]
        st.dataframe(df_target, use_container_width=True, height=400)
        
        csv_bytes = df_target.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download {selected_dataset} as CSV",
            data=csv_bytes,
            file_name=f"{key}.csv",
            mime="text/csv"
        )
    else:
        st.warning("Dataset not found in output directory.")

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding-bottom: 20px;">
    <b>National Household Travel Survey (NHTS) & Domestic Tourism Expenditure Survey (DTES)</b><br>
    NSS 80th Round (July 2025 – June 2026) | Household Survey Division (HSD), National Statistics Office (NSO), MoSPI<br>
    Built with Streamlit & Plotly • Complete microdata unit-level dataset validated against Schedule 21.1
</div>
""", unsafe_allow_html=True)
