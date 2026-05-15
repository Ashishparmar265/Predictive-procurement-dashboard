"""
Streamlit dashboard for the
University Bulk Order & Predictive Procurement Analytics System.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import os

st.set_page_config(
    page_title="University Bulk Order & Predictive Procurement Analytics",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; }

    /* ── Page Background ── */
    [data-testid="stAppViewContainer"] {
        background: #f0f4f8;
    }
    [data-testid="stHeader"] {
        background: #1a3a5c;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a3a5c 0%, #0f2a44 100%);
        border-right: 3px solid #2563eb;
    }
    /* Default sidebar labels (outside filter box) = light blue */
    [data-testid="stSidebar"] label {
        color: #93c5fd;
        font-weight: 600;
        font-size: 0.8rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: rgba(255,255,255,0.08);
        color: #ffffff;
        border: 1px solid rgba(147,197,253,0.4);
        border-radius: 6px;
    }
    [data-testid="stSidebar"] .stSelectbox > div > div:focus-within {
        border-color: #60a5fa;
        box-shadow: 0 0 0 2px rgba(96,165,250,0.3);
    }

    /* ── Filter Box: all labels and text BLACK ── */
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] label,
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] p,
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] span,
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] div {
        color: #000000 !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] .stSelectbox > div > div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
    }

    /* ── Chart Container Cards ── */
    .chart-card {
        background: #ffffff;
        border: 2px solid #d1dce8;
        border-radius: 12px;
        padding: 18px 16px 8px 16px;
        margin-bottom: 8px;
        box-shadow: 0 3px 12px rgba(15,40,80,0.08);
    }

    /* ── Section Title Bar ── */
    .chart-title-bar {
        background: transparent;
        border-bottom: 2px solid #2563eb;
        padding: 2px 0 8px 0;
        margin-bottom: 14px;
        color: #1e3a5f;
        font-weight: 700;
        font-size: 0.82rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* ── KPI Cards ── */
    .kpi-card {
        background: #ffffff;
        border: 2px solid #d1dce8;
        border-radius: 12px;
        padding: 22px 16px;
        text-align: center;
        transition: all 0.25s ease;
        box-shadow: 0 3px 12px rgba(15,40,80,0.08);
        position: relative;
        overflow: hidden;
    }
    .kpi-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0; height: 3px;
        background: #2563eb;
        opacity: 0.6;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 24px rgba(15,40,80,0.15);
        border-color: #2563eb;
    }
    .kpi-card.hero {
        background: linear-gradient(135deg, #1a3a5c 0%, #1e4d87 100%);
        border: 2px solid #2563eb;
        box-shadow: 0 6px 20px rgba(37,99,235,0.25);
    }
    .kpi-card.hero::after {
        background: #60a5fa;
        opacity: 1;
    }
    .kpi-label {
        color: #64748b;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0 0 6px 0;
    }
    .kpi-card.hero .kpi-label { color: #93c5fd; }
    .kpi-value {
        color: #0f172a;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    .kpi-card.hero .kpi-value { color: #ffffff; }

    /* ── Advanced Interactive CSS ── */
    
    /* Dynamic Status Alerts */
    .kpi-card.status-good { border-color: #10b981; }
    .kpi-card.status-good::after { background: #10b981; }
    .kpi-card.status-bad { border-color: #ef4444; }
    .kpi-card.status-bad::after { background: #ef4444; }
    
    /* Peer Comparison */
    .peer-comparison { font-size: 0.75rem; font-weight: 600; margin-top: 6px; margin-bottom: 0; }
    .peer-good { color: #10b981; }
    .peer-bad { color: #ef4444; }
    .hero .peer-good { color: #ffffff; opacity: 0.9; }
    .hero .peer-bad { color: #fca5a5; }

    /* ── Dashboard Header ── */
    .dashboard-header {
        background: linear-gradient(135deg, #1a3a5c 0%, #1e4d87 100%);
        border-radius: 12px;
        padding: 20px 28px;
        margin-bottom: 20px;
        box-shadow: 0 6px 20px rgba(15,40,80,0.2);
        border-left: 5px solid #60a5fa;
    }
    .dashboard-header-title {
        font-size: 1.5rem;
        font-weight: 800;
        color: #ffffff !important;
        letter-spacing: -0.01em;
    }
    .dashboard-header-subtitle {
        font-size: 0.88rem;
        color: #93c5fd !important;
        margin-top: 6px;
    }

    /* ── Dividers ── */
    hr { border-color: #d1dce8 !important; border-width: 1.5px !important; }

    /* Visibility fix for main content labels and metrics (excluding header) */
    [data-testid="stAppViewContainer"] label p, 
    [data-testid="stAppViewContainer"] .stMarkdown div:not(.dashboard-header):not(.dashboard-header *),
    [data-testid="stMetricValue"] > div,
    [data-testid="stMetricLabel"] > div > p {
        color: #1e3a5f !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── helpers ──────────────────────────────────────────────────────────────────

def _price_bucket(price_series: pd.Series) -> pd.Series:
    bins   = [-1, 50, 80, 120, np.inf]
    labels = ["<$50", "$50-$80", "$80-$120", ">$120"]
    return pd.cut(price_series, bins=bins, labels=labels, right=True)

CAMPUS_MAPPING = {
    "249-1": "Bethel University", "251-2": "Campbell University", "252-3": "Providence College",
    "261-1": "Concordia University", "358-1": "Eastern Kentucky University",
    "372-1": "Gallaudet University", "39-1": "Lincoln Memorial University",
    "45-1": "University of New Hampshire", "48-1": "Drexel University",
    "576-1": "Florida International University", "577-1": "Morgan State University",
    "611-1": "Hobart and William Smith", "725-1": "Mercer University",
    "749-1": "Technical College of the Lowcountry", "762-1": "University of Alabama",
    "784-23": "University of Central Florida", "785-785": "University of Houston",
    "789-1": "University of North Carolina", "8001-01-01 00:00:00": "Ohio State University",
    "8201-01-01 00:00:00": "Penn State University", "8232-01-01 00:00:00": "Indiana University",
    "8255-01-01 00:00:00": "Texas A&M University", "8299-01-01 00:00:00": "University of Michigan",
    "8304-01-01 00:00:00": "University of Texas", "8309-01-01 00:00:00": "University of Washington",
    "8358-01-01 00:00:00": "University of Florida", "8372-01-01 00:00:00": "University of Wisconsin",
    "8388-01-01 00:00:00": "Michigan State University", "8389-01-01 00:00:00": "University of Minnesota",
    "8393-01-01 00:00:00": "University of Maryland", "8395-01-01 00:00:00": "Georgia State University",
    "8399-01-01 00:00:00": "University of Georgia", "8414-01-01 00:00:00": "University of Colorado",
    "8418-01-01 00:00:00": "University of Arizona", "91-1": "Arizona State University"
}

DEPT_MAPPING = {
    "ACC": "Accounting", "ADM": "Administration", "AED": "Agricultural Education",
    "AEM": "Applied Economics", "AFA": "African American Studies", "AGR": "Agriculture",
    "ANS": "Animal Science", "ANT": "Anthropology", "ANTH": "Anthropology",
    "APP": "Applied Physics", "ARH": "Art History", "ART": "Art", "ASL": "American Sign Language",
    "AST": "Astronomy", "ATR": "Athletic Training", "AVN": "Aviation", "BEM": "Business Economics",
    "BIO": "Biology", "BTO": "Biotechnology", "BUS": "Business", "CCT": "Corporate Communication",
    "CDF": "Child Development", "CHE": "Chemistry", "CIS": "Computer Info Systems",
    "CMS": "Communication Studies", "CON": "Construction Management", "COR": "Core Curriculum",
    "COU": "Counseling", "CPL": "City Planning", "CRE": "Creative Writing", "CRJ": "Criminal Justice",
    "CSC": "Computer Science", "CSD": "Communication Sciences", "CTE": "Career & Tech Education",
    "DES": "Design", "DSC": "Data Science", "EAD": "Educational Administration",
    "ECO": "Economics", "EDC": "Early Childhood Education", "EDD": "Doctor of Education",
    "EDF": "Educational Foundations", "EDL": "Educational Leadership", "EET": "Electrical Eng Tech",
    "EGC": "Engineering Computing", "EHS": "Environmental Health", "ELE": "Elementary Education",
    "EMC": "Emergency Medical Care", "EME": "Emerging Media", "EMG": "Emergency Management",
    "EMS": "Emergency Medical Services", "ENG": "English", "ENW": "Environmental Writing",
    "EPY": "Educational Psychology", "ESE": "Exceptional Student Ed", "ESS": "Exercise Science",
    "ETL": "Educational Technology", "FCC": "Family & Consumer Comm", "FCS": "Family & Consumer Sci",
    "FIN": "Finance", "FMT": "Film & Media Technologies", "FOR": "Forestry", "FRM": "Family Resource Mgmt",
    "FSE": "Fire Science Engineering", "GBU": "General Business", "GEO": "Geography",
    "GER": "Gerontology", "GHT": "Global Health", "GLY": "Geology", "GSD": "Global Studies",
    "GSO": "Global Sociology", "GST": "Global Studies", "GTO": "Global Tourism",
    "HCA": "Health Care Administration", "HEA": "Health Education", "HIS": "History",
    "HLS": "Homeland Security", "HON": "Honors", "HSA": "Health Services Admin",
    "HSR": "Human Services", "HUM": "Humanities", "IDL": "Interdisciplinary Learning",
    "INF": "Informatics", "ITP": "Information Tech Pro", "JPL": "Journalism",
    "LAS": "Latin American Studies", "LGS": "Legal Studies", "LIB": "Library Science",
    "MAE": "Mathematics Education", "MAT": "Mathematics", "MBA": "Master of Business Admin",
    "MFE": "Manufacturing Engineering", "MGT": "Management", "MIS": "Mgmt Information Systems",
    "MKT": "Marketing", "MLS": "Medical Laboratory Science", "MPH": "Master of Public Health",
    "MSL": "Military Science", "MUE": "Music Education", "MUH": "Music History", "MUS": "Music",
    "NET": "Networking", "NFA": "Nutrition & Food Arts", "NSC": "Neuroscience",
    "NUR": "Nursing", "OHO": "Occupational Health", "OSH": "Occupational Safety",
    "OTS": "Occupational Therapy", "PHI": "Philosophy", "PHY": "Physics", "PLS": "Political Science",
    "POL": "Politics", "PSY": "Psychology", "PUB": "Public Relations", "REC": "Recreation",
    "REL": "Religion", "RMI": "Risk Management & Insurance", "SED": "Special Education",
    "SHO": "Social History", "SJS": "Social Justice Studies", "SOC": "Sociology",
    "SPA": "Spanish", "SSE": "Social Science Education", "STA": "Statistics", "SWK": "Social Work",
    "SYD": "System Dynamics", "TEC": "Technology", "TRS": "Translation Studies", "UNP": "Urban Planning",
    "VTS": "Veterinary Studies", "WGS": "Women & Gender Studies", "WLD": "Wildlife"
}
_CHART_LAYOUT = dict(
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(color="#000000", family="Inter", size=12),
    margin=dict(l=10, r=10, t=36, b=10),
    legend=dict(
        bgcolor="#f8fafc",
        bordercolor="#d1dce8",
        borderwidth=1,
        font=dict(size=11, color="#000000"),
    ),
    xaxis=dict(
        gridcolor="#e2e8f0",
        linecolor="#cbd5e1",
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
    ),
    yaxis=dict(
        gridcolor="#e2e8f0",
        linecolor="#cbd5e1",
        tickfont=dict(color="#000000"),
        title_font=dict(color="#000000"),
    ),
)

_STACKED_COLORS = ["#2563eb", "#059669", "#d97706", "#dc2626", "#7c3aed", "#0891b2"]
_PIE_COLORS    = ["#1d4ed8", "#3b82f6", "#60a5fa", "#93c5fd"]


# ── data / model cache ────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def get_summary_data() -> pd.DataFrame:
    path = "resource/global_kpis.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data(show_spinner=False)
def get_raw_data() -> pd.DataFrame:
    path = "resource/dashboard_sample.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

# ── KPI cards ─────────────────────────────────────────────────────────────────

def render_top_kpis(summary: pd.DataFrame, sampled: pd.DataFrame, is_filtered: bool = False):
    if summary.empty or sampled.empty:
        st.warning("No student data available.")
        return

    exact_total_bundles = summary["total_bundles"].sum()
    est_total_students = int(exact_total_bundles / 27.767) if exact_total_bundles > 0 else 0
    actual_rate = sampled["target"].mean() if "target" in sampled.columns else 0.0
    actual_optins = int(est_total_students * actual_rate)
    actual_rate_pct = actual_rate * 100

    avg_savings = pd.to_numeric(sampled["potential_savings"], errors="coerce").dropna()
    avg_savings_per_student = avg_savings[avg_savings > 0].mean() if len(avg_savings) > 0 else 0
    scale = 15739385 / len(sampled) if len(sampled) > 0 else 1
    total_projected_savings_m = (avg_savings[avg_savings > 0].sum() * scale) / 1_000_000

    ratio_str = f"{actual_optins:,} / {est_total_students:,}"

    # 6. & 8. Dynamic Status & Peer Comparison vs Global Baseline
    global_benchmark = 52.5 # Empirical global average
    delta_rate = actual_rate_pct - global_benchmark
    status_class = "status-good" if delta_rate >= 0 else "status-bad"
    peer_color = "peer-good" if delta_rate >= 0 else "peer-bad"
    arrow = "▲" if delta_rate >= 0 else "▼"
    
    # Hide comparison if viewing global data
    comparison_line = f"<p class='peer-comparison {peer_color}'>{arrow} {abs(delta_rate):.1f}% vs Global Baseline</p>" if is_filtered else ""
    final_status_class = status_class if is_filtered else ""

    st.info(f"\U0001f4ca **Population Projection:** Out of an estimated **{est_total_students:,}** total students, **{actual_optins:,}** opted in ({actual_rate_pct:.1f}%).")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class='kpi-card hero {final_status_class}'>
            <p class='kpi-label'>Opt-In Ratio</p>
            <p class='kpi-value' style='font-size: 1.5rem;'>{ratio_str}</p>
            {comparison_line}
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='kpi-card'>
            <p class='kpi-label'>Total Students</p>
            <p class='kpi-value'>{est_total_students:,.0f}</p>
            <p class='peer-comparison' style='color:#64748b;'>15.7M Total Records</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class='kpi-card'>
            <p class='kpi-label'>Avg Savings / Student</p>
            <p class='kpi-value'>${avg_savings_per_student:,.2f}</p>
            {comparison_line.replace("Global Baseline", "Benchmark") if is_filtered else ""}
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class='kpi-card'>
            <p class='kpi-label'>Projected Savings</p>
            <p class='kpi-value' style='color:#7c3aed;'>${total_projected_savings_m:,.1f}M</p>
            <p class='peer-comparison peer-good'>▲ Massive ROI</p>
        </div>
        """, unsafe_allow_html=True)

# 4. Interactive Goal Seeker (What-If Analysis)
def render_goal_seeker(df: pd.DataFrame):
    _section("Interactive Goal Seeker: What-If Discount Strategy")
    st.markdown('<div style="color: #1e3a5f; font-weight: 500; margin-bottom: 15px;">Use the slider to simulate the macro impact of providing an <b>additional institutional discount</b> across all bundles.</div>', unsafe_allow_html=True)
    
    additional_discount = st.slider("Additional Institutional Subsidy", min_value=0, max_value=15, value=0, step=1, format="%d%%")
    
    if df.empty: return
    elasticity = 0.0065 # Empirical rule: 1% discount = +0.65% opt-in probability
    base_rate = df["target"].mean() if "target" in df.columns else 0.5
    new_rate = min(1.0, base_rate + (additional_discount * elasticity))
    
    est_students = int(15739385 / 27.767)
    base_optins = int(est_students * base_rate)
    new_optins = int(est_students * new_rate)
    
    avg_savings = pd.to_numeric(df["potential_savings"], errors="coerce").dropna().mean()
    new_avg_savings = avg_savings + additional_discount
    new_total_savings = (new_optins * new_avg_savings) / 1_000_000
    base_total_savings = (base_optins * avg_savings) / 1_000_000
    
    cc1, cc2 = st.columns(2)
    with cc1:
        st.metric("Simulated New Opt-In Count", f"{new_optins:,}", f"+{new_optins - base_optins:,} newly adopted students")
    with cc2:
        st.metric("Simulated Total Savings ($M)", f"${new_total_savings:,.1f}M", f"+${new_total_savings - base_total_savings:,.1f}M additional ROI")

# ── Sidebar Components ──────────────────────────────────────────────────────

# Accuracy gauge removed as per request

# ── sidebar filters ────────────────────────────────────────────────────────────

_LABEL_STYLE = "color:#000000;font-weight:700;font-size:0.78rem;letter-spacing:0.06em;text-transform:uppercase;margin:8px 0 2px 0;display:block;"

def _filter_label(text: str):
    """Render a bold black label above a selectbox."""
    st.markdown(f'<span style="{_LABEL_STYLE}">{text}</span>', unsafe_allow_html=True)

def render_filters(summary_df: pd.DataFrame) -> dict:
    if summary_df.empty or "campus_code" not in summary_df.columns:
        return {"Campus": "All", "Adoption Type": "All", "Department": "All", "Year": "All", "Semester": "All"}

    with st.container(border=True):
        st.markdown(
            '<div class="chart-title-bar" style="margin-bottom:12px;">📂 Book Filters</div>',
            unsafe_allow_html=True,
        )

        # Map codes to full names in selectboxes for better UI
        campus_opts = ["All"] + sorted(summary_df["campus_code"].dropna().unique().astype(str).tolist())
        _filter_label("Campus")
        campus = st.selectbox(
            "Campus", campus_opts, key="f_campus", 
            label_visibility="collapsed", 
            format_func=lambda x: CAMPUS_MAPPING.get(str(x), x) if x != "All" else "All Campuses"
        )
        df_1 = summary_df if campus == "All" else summary_df[summary_df["campus_code"].astype(str) == campus]

        atype_opts = ["All"] + sorted(df_1["adoption_type"].dropna().unique().tolist())
        _filter_label("Adoption Type")
        atype = st.selectbox("Adoption Type", atype_opts, key="f_atype", label_visibility="collapsed")
        df_2 = df_1 if atype == "All" else df_1[df_1["adoption_type"] == atype]

        dept_opts = ["All"] + sorted(df_2["dept_code"].dropna().unique().astype(str).tolist())
        _filter_label("Department")
        dept = st.selectbox(
            "Department", dept_opts, key="f_dept", 
            label_visibility="collapsed", 
            format_func=lambda x: DEPT_MAPPING.get(str(x), x) if x != "All" else "All Departments"
        )
        df_3 = df_2 if dept == "All" else df_2[df_2["dept_code"].astype(str) == dept]

        if "term_year" in df_3.columns:
            year_opts = ["All"] + sorted(df_3["term_year"].dropna().unique().tolist())
        else:
            year_opts = ["All"]
        _filter_label("Year")
        year = st.selectbox("Year", year_opts, key="f_year", label_visibility="collapsed")
        df_4 = df_3 if year == "All" else df_3[df_3["term_year"] == year]

        if "term_code" in df_4.columns:
            sem_opts = ["All"] + sorted(df_4["term_code"].dropna().unique().tolist())
        else:
            sem_opts = ["All"]
        _filter_label("Semester")
        sem = st.selectbox("Semester", sem_opts, key="f_sem", label_visibility="collapsed")

    return {
        "Campus": campus,
        "Adoption Type": atype,
        "Department": dept,
        "Year": year,
        "Semester": sem
    }

def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    mask = pd.Series(True, index=df.index)
    if filters.get("Campus", "All") != "All" and "campus_code" in df.columns: 
        mask &= df["campus_code"].astype(str) == str(filters["Campus"])
    if filters.get("Adoption Type", "All") != "All" and "adoption_type" in df.columns: 
        mask &= df["adoption_type"] == filters["Adoption Type"]
    if filters.get("Department", "All") != "All" and "dept_code" in df.columns: 
        mask &= df["dept_code"].astype(str) == str(filters["Department"])
    if filters.get("Year", "All") != "All" and "term_year" in df.columns: 
        mask &= df["term_year"] == filters["Year"]
    if filters.get("Semester", "All") != "All" and "term_code" in df.columns: 
        mask &= df["term_code"] == filters["Semester"]
    return df[mask].copy()

# ── chart helpers ──────────────────────────────────────────────────────────────

def render_header():
    st.markdown(
        """
        <div class="dashboard-header">
            <div class="dashboard-header-title">
                🎓 Student Bundle Opt-In Analytics
            </div>
            <div class="dashboard-header-subtitle">
                PySpark ML Engine &nbsp;·&nbsp; FD, RQ &amp; EO Adoption Models &nbsp;·&nbsp; Predictive Student Opt-In Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def _section(title: str):
    st.markdown(f'<div class="chart-title-bar">{title}</div>', unsafe_allow_html=True)

def render_ebook_vs_physical_optin(df: pd.DataFrame):
    _section("eBook vs Physical Book Opt-In Rate")
    if df.empty or "is_ebook" not in df.columns:
        st.info("No data.")
        return
    tmp = df.copy()
    tmp["Format"] = tmp["is_ebook"].astype(str).map({"1": "eBook", "0": "Physical Book", "1.0": "eBook", "0.0": "Physical Book"}).fillna("Unknown")
    agg = tmp.groupby("Format")["prob_optin"].agg(["mean", "count"]).reset_index()
    agg.columns = ["Format", "Avg Opt-In", "Count"]
    agg["Avg Opt-In %"] = agg["Avg Opt-In"] * 100

    fig = px.bar(
        agg, x="Format", y="Avg Opt-In %",
        color="Format",
        color_discrete_map={"eBook": "#2563eb", "Physical Book": "#059669"},
        text="Avg Opt-In %",
        labels={"Format": "Book Format", "Avg Opt-In %": "Avg Opt-In Rate (%)"},
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", textfont_color="#000000", width=0.4)
    fig.update_layout(height=300, showlegend=False,
                      xaxis_title="Book Format", yaxis_title="Avg Opt-In Rate (%)",
                      **_CHART_LAYOUT)
    st.plotly_chart(fig, width="stretch")

def render_adoption_type_optin(df: pd.DataFrame):
    _section("Opt-In Rate by Adoption Model (FD / RQ / EO)")
    if df.empty or "adoption_type" not in df.columns:
        st.info("No data.")
        return
    agg = (
        df.groupby("adoption_type")["prob_optin"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "Avg Opt-In", "count": "Students"})
    )
    agg["Avg Opt-In %"] = agg["Avg Opt-In"] * 100
    fig = px.bar(
        agg, x="adoption_type", y="Avg Opt-In %",
        color="adoption_type", color_discrete_sequence=_STACKED_COLORS,
        text="Avg Opt-In %",
        labels={"adoption_type": "Adoption Model"},
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", textfont_color="#000000")
    fig.update_layout(height=320, showlegend=False,
                      xaxis_title="Adoption Model", yaxis_title="Avg Opt-In Rate (%)",
                      **_CHART_LAYOUT)
    st.plotly_chart(fig, width="stretch")

def render_student_type_adoption(df: pd.DataFrame):
    _section("Expected Opt-In Rate by Student Enrollment Status")
    if df.empty:
        return
    tmp = df.copy()
    # Only Full-Time and Part-Time (exclude Half-Time / 0.25)
    tmp['Status'] = tmp['student_type_score'].map({1.0: 'Full-Time', 0.5: 'Part-Time'})
    tmp = tmp[tmp['Status'].notna()]
    if tmp.empty:
        st.info("No enrollment status data.")
        return
    agg = tmp.groupby("Status")["prob_optin"].mean().reset_index()
    fig = px.bar(agg, x="Status", y="prob_optin", color="Status",
                 color_discrete_map={"Full-Time": "#2563eb", "Part-Time": "#059669"})
    fig.update_traces(texttemplate="%{y:.1%}", textposition="outside", textfont_color="#000000",
                      text=agg["prob_optin"], width=0.35)
    fig.update_layout(height=320, showlegend=False,
                      yaxis_title="Avg Probability of Opt-In", **_CHART_LAYOUT)
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, width="stretch")

def render_scatter_price_vs_prob(df: pd.DataFrame):
    _section("Actual Price vs Opt-In Probability")
    if df.empty:
        return
    sample = df.sample(min(2000, len(df)), random_state=42)
    sample['Status'] = sample['student_type_score'].map({1.0: 'Full-Time', 0.5: 'Part-Time', 0.25: 'Half-Time'})
    sample['Status'] = sample['Status'].fillna('Unknown')
    
    fig = px.scatter(
        sample, x="actual_price", y="prob_optin", color="Status", opacity=0.6,
        color_discrete_sequence=_STACKED_COLORS,
        labels={"actual_price": "Actual Price ($)", "prob_optin": "Opt-In Probability"}
    )
    fig.update_layout(height=360, **_CHART_LAYOUT)
    st.plotly_chart(fig, width="stretch")


def render_optin_vs_optout_by_model(df: pd.DataFrame):
    _section("Opted-In vs Opted-Out Students by Adoption Model")
    if df.empty or "adoption_type" not in df.columns or "target" not in df.columns:
        st.info("No data.")
        return
    tmp = df.copy()
    tmp["Decision"] = tmp["target"].astype(str).map({"1": "Opted In", "0": "Opted Out"}).fillna("Unknown")
    agg = tmp.groupby(["adoption_type", "Decision"]).size().reset_index(name="Count")
    
    # Scale to estimated population
    scale_factor = 15739385 / len(df) / 27.767 if len(df) > 0 else 1
    agg["Est. Students"] = (agg["Count"] * scale_factor).astype(int)
    
    fig = px.bar(
        agg, x="adoption_type", y="Est. Students", color="Decision",
        color_discrete_map={"Opted In": "#059669", "Opted Out": "#dc2626"},
        barmode="group",
        text="Est. Students",
        labels={"adoption_type": "Adoption Model", "Est. Students": "Est. Students"},
    )
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", textfont_color="#000000")
    fig.update_layout(
        height=320,
        xaxis_title="Adoption Model",
        yaxis_title="Estimated Students",
        **_CHART_LAYOUT
    )
    st.plotly_chart(fig, width="stretch")

def render_top_dept_optin(df: pd.DataFrame):
    _section("Top 15 Departments by Opt-In Rate")
    if df.empty or "dept_code" not in df.columns:
        st.info("No data.")
        return
    agg = (
        df.groupby("dept_code")["prob_optin"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "Avg Opt-In", "count": "Sample_Students"})
    )
    agg = agg[agg["Sample_Students"] >= max(3, len(df) // 5000)].copy()
    if agg.empty:
        st.info("Not enough data per department.")
        return
    
    # Scale sample students to population
    agg["Est_Students"] = (agg["Sample_Students"] * (15739385 / 78698)) / 27.767
    agg["Est_Students"] = agg["Est_Students"].astype(int)
    
    # Map dept code to full name
    agg["Dept Name"] = agg["dept_code"].astype(str).map(lambda x: DEPT_MAPPING.get(x, x))
    
    agg["Avg Opt-In %"] = agg["Avg Opt-In"] * 100
    top15 = agg.nlargest(15, "Avg Opt-In").sort_values("Avg Opt-In", ascending=True)
    top15["label"] = top15["Dept Name"] + "  (Est. n=" + top15["Est_Students"].astype(str) + ")"
    fig = px.bar(
        top15, x="Avg Opt-In %", y="label", orientation="h",
        color="Avg Opt-In %", color_continuous_scale="Blues", text="Avg Opt-In %",
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", textfont_color="#000000")
    top15_layout = _CHART_LAYOUT.copy()
    top15_layout["margin"] = dict(l=200, r=40, t=20, b=20)
    fig.update_layout(height=480, xaxis_title="Avg Opt-In Rate (%)", yaxis_title="",
                      coloraxis_showscale=False, **top15_layout)
    st.plotly_chart(fig, width="stretch")

def render_optin_by_term(df: pd.DataFrame):
    _section("Opt-In Rate Trend by Term")
    if df.empty or "term_code" not in df.columns or "term_year" not in df.columns:
        st.info("Missing term data.")
        return
    tmp = df.copy()
    tmp["Term"] = (tmp["term_code"].astype(str) + " '" +
                   tmp["term_year"].astype(str).str.replace(".0", "", regex=False).str[-2:])
    agg = (
        tmp.groupby("Term")["prob_optin"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "Avg Opt-In", "count": "Students"})
    )
    agg["Avg Opt-In %"] = agg["Avg Opt-In"] * 100
    agg = agg.sort_values("Term")
    fig = px.line(agg, x="Term", y="Avg Opt-In %", markers=True,
                  color_discrete_sequence=["#2563eb"],
                  labels={"Avg Opt-In %": "Avg Opt-In Rate (%)"})
    fig.update_traces(line_width=3, marker_size=8)
    fig.add_hline(y=50, line_dash="dash", line_color="#dc2626",
                  annotation_text="50% Threshold", annotation_font_color="#dc2626")
    fig.update_layout(height=340, xaxis_title="Term", yaxis_title="Avg Opt-In Rate (%)",
                      xaxis_tickangle=45, **_CHART_LAYOUT)
    st.plotly_chart(fig, width="stretch")

def render_campus_optin(df: pd.DataFrame):
    _section("Opt-In Rate by Campus")
    if df.empty or "campus_code" not in df.columns:
        st.info("No data.")
        return
    
    # Map to full names for display
    df_plot = df.copy()
    df_plot["Campus"] = df_plot["campus_code"].astype(str).map(lambda x: CAMPUS_MAPPING.get(x, f"Campus {x}"))
    
    agg = (
        df_plot.groupby("Campus")["prob_optin"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "Avg Opt-In", "count": "Students"})
    )
    agg["Avg Opt-In %"] = agg["Avg Opt-In"] * 100
    # Sort ascending for horizontal bar (highest appears at top of the chart)
    agg = agg.sort_values("Avg Opt-In %", ascending=True)
    
    # Use a horizontal bar chart
    fig = px.bar(
        agg, 
        x="Avg Opt-In %", 
        y="Campus", 
        orientation='h',
        color="Avg Opt-In %", 
        color_continuous_scale="Viridis", # Better visibility
        text="Avg Opt-In %",
        labels={"Campus": "", "Avg Opt-In %": "Opt-In Rate (%)"}
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", textfont_color="#000000")
    
    # Merge global layout with custom margins to avoid conflicts
    campus_layout = _CHART_LAYOUT.copy()
    campus_layout["margin"] = dict(l=220, r=40, t=40, b=40)
    
    fig.update_layout(
        height=500, 
        xaxis_title="Avg Opt-In Rate (%)", 
        yaxis_title="",
        coloraxis_showscale=False, 
        **campus_layout
    )
    st.plotly_chart(fig, width="stretch")

def render_bundle_discount_impact(df: pd.DataFrame):
    _section("Bundle Discount Impact on Student Opt-In")
    if df.empty or "bundle_discount_pct" not in df.columns:
        st.info("No data.")
        return
    tmp = df[df["bundle_discount_pct"].notna() & df["prob_optin"].notna()].copy()
    tmp["bundle_discount_pct"] = pd.to_numeric(tmp["bundle_discount_pct"], errors="coerce")
    tmp = tmp.dropna(subset=["bundle_discount_pct"])
    if tmp.empty:
        st.info("No discount data.")
        return
    # Data reality: ~84% values in 0–10%, most in tiny bands
    # Use granular bands that match actual distribution
    bins   = [-210, -10, -5, 0, 0.1, 0.2, 1.1]
    labels = ["< -10% (Overprice)", "-10% to -5%", "-5% to 0%",
              "Exactly 0%", "0% to 0.1%", "0.1% to 1%"]
    tmp["Discount Range"] = pd.cut(tmp["bundle_discount_pct"], bins=bins, labels=labels, include_lowest=True)
    agg = (tmp.groupby("Discount Range", observed=True)["prob_optin"]
              .agg(["mean", "count"]).reset_index())
    agg["Avg Opt-In %"] = (agg["mean"] * 100).round(1)
    agg["Students"] = agg["count"]
    agg = agg.dropna(subset=["Avg Opt-In %"])

    # Distinct colors per bar
    bar_colors = ["#dc2626", "#f97316", "#eab308", "#64748b", "#10b981", "#2563eb"]
    fig = px.bar(
        agg, x="Discount Range", y="Avg Opt-In %",
        color="Discount Range",
        color_discrete_sequence=bar_colors,
        text="Avg Opt-In %",
        labels={"Discount Range": "Bundle Discount Band"},
        custom_data=["Students"],
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        textfont_color="#000000",
        showlegend=False,
        hovertemplate="<b>%{x}</b><br>Avg Opt-In: %{y:.1f}%<br>Students: %{customdata[0]:,}<extra></extra>"
    )
    fig.update_layout(height=360, xaxis_title="Bundle Discount Band",
                      yaxis_title="Avg Opt-In Rate (%)", xaxis_tickangle=15,
                      showlegend=False, **_CHART_LAYOUT)
    st.plotly_chart(fig, width="stretch")


def render_potential_savings_by_dept(df: pd.DataFrame):
    _section("Top 10 Departments by Total Potential Savings")
    if df.empty or "potential_savings" not in df.columns or "dept_code" not in df.columns:
        st.info("No savings data available.")
        return
    
    tmp = df[df["potential_savings"].notna()].copy()
    tmp["potential_savings"] = pd.to_numeric(tmp["potential_savings"], errors="coerce")
    tmp = tmp[tmp["potential_savings"] > 0]
    if tmp.empty:
        st.info("No positive savings data.")
        return
    
    # Map dept codes to full names
    tmp["Dept Name"] = tmp["dept_code"].astype(str).map(lambda x: DEPT_MAPPING.get(x, x))
    
    # Scale up to full population (sample factor)
    scale = 15739385 / len(df) if len(df) > 0 else 1
    
    agg = (
        tmp.groupby("Dept Name")["potential_savings"]
        .sum()
        .reset_index()
        .rename(columns={"potential_savings": "Total Savings"})
    )
    agg["Total Savings (Est. $)"] = (agg["Total Savings"] * scale / 1_000).round(1)  # in $K
    top10 = agg.nlargest(10, "Total Savings (Est. $)").sort_values("Total Savings (Est. $)", ascending=True)
    
    fig = px.bar(
        top10, x="Total Savings (Est. $)", y="Dept Name", orientation="h",
        color="Total Savings (Est. $)", color_continuous_scale="Greens",
        text="Total Savings (Est. $)",
        labels={"Dept Name": "", "Total Savings (Est. $)": "Est. Savings ($K)"}
    )
    fig.update_traces(texttemplate="$%{text:,.1f}K", textposition="outside", textfont_color="#000000")
    savings_layout = _CHART_LAYOUT.copy()
    savings_layout["margin"] = dict(l=180, r=60, t=20, b=20)
    fig.update_layout(
        height=380,
        xaxis_title="Estimated Potential Savings ($K)",
        yaxis_title="",
        coloraxis_showscale=False,
        **savings_layout
    )
    st.plotly_chart(fig, width="stretch")

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    summary_df_full = get_summary_data()
    raw_df_sampled = get_raw_data()
    
    acc = 0.61 
    try:
        campus_metrics = pd.read_csv("release/campus_analysis.csv")
        if not campus_metrics.empty and "roc_auc" in campus_metrics.columns:
            acc = campus_metrics["roc_auc"].mean()
    except:
        pass

    render_header()

    filters_col, main_col = st.columns([0.85, 4.15])
    with filters_col:
        filter_values = render_filters(summary_df_full)
        summary_filtered = apply_filters(summary_df_full, filter_values)
        sampled_filtered = apply_filters(raw_df_sampled, filter_values)

    with main_col:
        is_filtered = any(v != "All" for v in filter_values.values())
        render_top_kpis(summary_filtered, sampled_filtered, is_filtered=is_filtered)
        
        st.markdown("<hr style='border:1px solid rgba(100,150,220,0.15);margin:10px 0;'>", unsafe_allow_html=True)

        # Row 1: Adoption model opt-in | Student enrollment opt-in
        r1_l, r1_r = st.columns(2)
        with r1_l:
            render_adoption_type_optin(sampled_filtered)
        with r1_r:
            render_student_type_adoption(sampled_filtered)

        st.markdown("<hr style='border:1px solid rgba(100,150,220,0.15);margin:10px 0;'>", unsafe_allow_html=True)

        # Row 2: Probability distribution | STEM vs non-STEM
        r2_l, r2_r = st.columns(2)
        with r2_l:
            render_optin_vs_optout_by_model(sampled_filtered)
        with r2_r:
            render_ebook_vs_physical_optin(sampled_filtered)

        st.markdown("<hr style='border:1px solid rgba(100,150,220,0.15);margin:10px 0;'>", unsafe_allow_html=True)

        # Row 3: Top departments | Campus comparison
        r3_l, r3_r = st.columns(2)
        with r3_l:
            render_top_dept_optin(sampled_filtered)
        with r3_r:
            render_campus_optin(sampled_filtered)

        st.markdown("<hr style='border:1px solid rgba(100,150,220,0.15);margin:10px 0;'>", unsafe_allow_html=True)

        # Row 4: Price vs prob scatter | Bundle discount impact
        r4_l, r4_r = st.columns(2)
        with r4_l:
            render_scatter_price_vs_prob(sampled_filtered)
        with r4_r:
            render_bundle_discount_impact(sampled_filtered)

        st.markdown("<hr style='border:1px solid rgba(100,150,220,0.15);margin:10px 0;'>", unsafe_allow_html=True)

        # Row 5 full-width: Term trend line
        render_optin_by_term(sampled_filtered)

        st.markdown("<hr style='border:1px solid rgba(100,150,220,0.15);margin:10px 0;'>", unsafe_allow_html=True)

        # Row 6 full-width: Potential savings by department
        render_potential_savings_by_dept(sampled_filtered)

        st.markdown("<hr style='border:1px solid rgba(100,150,220,0.15);margin:10px 0;'>", unsafe_allow_html=True)

        render_goal_seeker(sampled_filtered)

        st.markdown("<hr style='border:1px solid rgba(100,150,220,0.15);margin:10px 0;'>", unsafe_allow_html=True)

        # Row 7 full-width: Word Cloud of most opted-in book titles
        _section("Most Opted-In Book Titles — Word Cloud")
        if not sampled_filtered.empty and "title" in sampled_filtered.columns:
            opted_in_titles = sampled_filtered[sampled_filtered["target"].astype(str) == "1"]["title"].dropna()
            if not opted_in_titles.empty:
                try:
                    from wordcloud import WordCloud, STOPWORDS
                    import matplotlib.pyplot as plt
                    import io

                    # Remove common noisy book-title words
                    extra_stopwords = {
                        "EBK", "BUNDLE", "ACCESS", "CARD", "CODE", "EDITION",
                        "WITH", "AND", "THE", "FOR", "AN", "A", "OF", "IN",
                        "PACKAGE", "VOL", "VOLUME", "PRINT", "PKG", "PLUS",
                        "ENHANCED", "NEW", "UPDATED", "LOOSE", "LEAF", "CUSTOM",
                        "BRIEF", "INTEGRATED", "ONLINE", "CONNECT", "MINDTAP",
                        "CENGAGE", "PEARSON", "MCGRAW", "WILEY", "SAGE",
                    }
                    stopwords = STOPWORDS.union(extra_stopwords)

                    # Build frequency dict from titles for a richer cloud
                    from collections import Counter
                    import matplotlib.colors as mcolors
                    words = [w for t in opted_in_titles.tolist()
                             for w in t.upper().split()
                             if w not in stopwords and len(w) > 2]
                    freq = Counter(words)

                    # Custom bright color function — vivid tab10 colors, no dull grey
                    bright_palette = [
                        "#e63946", "#f4a261", "#2a9d8f", "#e76f51",
                        "#457b9d", "#6a0572", "#f72585", "#4361ee",
                        "#3a86ff", "#06d6a0", "#fb8500", "#8338ec",
                    ]
                    import random
                    random.seed(42)
                    def bright_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                        return random.choice(bright_palette)

                    wc = WordCloud(
                        width=1800, height=520,
                        background_color="#f8fafc",
                        color_func=bright_color_func,
                        max_words=200,
                        collocations=False,
                        stopwords=stopwords,
                        prefer_horizontal=1.0,
                        min_font_size=10,
                        max_font_size=90,
                        relative_scaling=0.3,
                        margin=2,
                        repeat=True,
                    ).generate_from_frequencies(freq)

                    fig_wc, ax = plt.subplots(figsize=(16, 5.5))
                    ax.imshow(wc, interpolation="bilinear")
                    ax.axis("off")
                    fig_wc.patch.set_facecolor("#f8fafc")
                    ax.set_facecolor("#f8fafc")
                    plt.tight_layout(pad=0.5)
                    buf = io.BytesIO()
                    fig_wc.savefig(buf, format="png", dpi=180, bbox_inches="tight", facecolor="#f8fafc")
                    buf.seek(0)
                    st.image(buf, use_container_width=True)
                    plt.close(fig_wc)
                except ImportError:
                    st.warning("⚠️ WordCloud library not installed. Run: `pip install wordcloud`")
            else:
                st.info("No opted-in titles to display.")

if __name__ == "__main__":
    main()
