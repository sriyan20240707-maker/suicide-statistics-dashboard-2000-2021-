import streamlit as st
import base64

# ── CHANGED: Light purple/teal/white theme replacing dark theme ──────────────
# Shared Plotly theme applied to every chart
LAYOUT = dict(
    paper_bgcolor="rgba(6,148,148, 0.0)",          # CHANGED: was #131929 (dark) → pure white
    plot_bgcolor="rgba(6,148,148, 0.0.0)",           # CHANGED: was #131929 (dark) → soft white
    font=dict(color="#1E2235", size=12),    # CHANGED: was #c8d6e8 → charcoal text
    xaxis=dict(gridcolor="#D0D8F0", tickfont=dict(color="#5A6480")),   # CHANGED: was #1e2d42 / #8899aa
    yaxis=dict(gridcolor="#D0D8F0", tickfont=dict(color="#5A6480")),   # CHANGED: was #1e2d42 / #8899aa
    legend=dict(bgcolor="rgba(255,255,255,0.8)", font=dict(color="#1E2235")),  # CHANGED: was dark bg
    hoverlabel=dict(bgcolor="#EEF0FB", font_color="#1E2235"),          # CHANGED: was #0d1625 / #e8f0fe
    margin=dict(l=10, r=10, t=36, b=10),
)

def get_base64_img(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def apply_sidebar():
    for key, val in [('page', "🏠 Home"), ('year', 2021), ('sex', "Total")]:
        if key not in st.session_state:
            st.session_state[key] = val

    # Load ribbon image for home page background
    try:
        img_b64 = get_base64_img(r"E:\BDA\YEAR 2\SEM 02\DSPLC\CW2\pics\Suicide-prevention-ribbon-PO.png")
        st.session_state['ribbon_img'] = img_b64
    except:
        st.session_state['ribbon_img'] = None

    st.markdown(
        """<style>         
    [data-testid="stSidebarCollapseButton"],[data-testid="stSidebarHeader"]
                {display:none!important}
    [data-testid="stSidebar"]
                {width:120px!important;
                min-width:100px!important;
                max-width:120px!important}
    [data-testid="stSidebar"]>div:first-child
                {background:#2E1F5E!important;
                border-right:2px solid #2EC4B6!important;
                display:flex!important;
                flex-direction:column!important;
                align-items:center!important;
                padding:20px 0!important}
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"]
                {display:flex!important;
                flex-direction:column!important;
                align-items:center!important;
                gap:40px!important}
    [data-testid="stSidebar"] button
                {width:100px!important;
                height:56px!important;
                border-radius:12px!important;
                background:D9F5F2!important;
                border:none!important;
                font-size:22px!important;
                color:#EEF0FB!important}
    [data-testid="stSidebar"] button:focus
                {background:#2D3D4D!important}
    [data-testid="stSidebar"] [data-testid="stSelectbox"]
                {width:100px!important}
    [data-testid="stSidebar"] [data-testid="stSelectbox"]>div
                {font-size:12px!important;
                background:#EEF0FB!important;
                border:1px solid #D0D8F0!important;
                border-radius:8px!important}
    [data-testid="stMetric"]
                {background:#000000!important;
                border:1px solid #D0D8F0!important;
                border-radius:12px!important;
                padding:16px 20px!important}
    [data-testid="stMetricLabel"]
                {color:#5A6480!important;
                font-size:11px!important;
                font-weight:600!important;
                letter-spacing:.8px!important;
                text-transform:uppercase!important}
    [data-testid="stMetricValue"]
                {color:rgba(6,148,148, 0.20)!important;
                font-size:6px!important;
                font-weight:700!important}
    [data-testid="stPlotlyChart"]
                {background:rgba(6,148,148, 0.20)!important;
                border:4px solid #D0D8F0!important;
                border-radius:12px!important;
                padding:8px!important}
    [data-testid="stSelectbox"]>div
                {background:#FFFFFF!important;
                border:1px solid #D0D8F0!important;
                border-radius:8px!important;
                color:#1E2235!important}
    [data-testid="stTextInput"] input
                {background:#FFFFFF!important;
                border:1px solid #D0D8F0!important;
                border-radius:8px!important;
                color:#1E2235!important}
    [data-testid="stButton"] button
                {background:#131929!important;
                border:1px solid #D0D8F0!important;
                border-radius:8px!important;
                color:#5A6480!important}
    .stApp
                {background:#F7F9FC}
    .block-container
                {padding:30px 28px 40px!important;
                max-width:100%!important}
    .stApp h2,.stApp h3
                {color:#1E2235!important;
                font-weight:600!important;
                font-size:15px!important}
    </style>""", unsafe_allow_html=True)

    pages = {
        "🏠  Home":       "🏠 Home",
        "🌍  World view": "🌍 Global Overview",
        "📈  Trends":     "📈 Trends",
        "📊  Deep Dive":  "📊 Country Analysis"
    }

    with st.sidebar:
        for emoji, page_name in pages.items():
            if st.button(emoji, key=f"btn_{emoji}"):
                st.session_state.page = page_name
                st.rerun()

        # CHANGED: was #3ce1ff44 → purple tint divider
        st.markdown('<hr style="width:100px;border-color:#7C6CF244;margin:12px 0">', unsafe_allow_html=True)

        for label, key, opts in [("YEAR", "year", list(range(2000, 2022))), ("SEX", "sex", ["Total", "Male", "Female"])]:
            # CHANGED: label colour was #3ce1ff → bright teal #2EC4B6
            st.markdown(f'<p style="color:#2EC4B6;font-size:14px;font-weight:700;text-align:center;letter-spacing:1.5px;text-transform:uppercase;margin:12px 0 -12px 0">{label}</p>', unsafe_allow_html=True)
            st.session_state[key] = st.selectbox(
                label, opts,
                index=opts.index(st.session_state[key]),
                key=f"{key}_filter",
                label_visibility="collapsed"
            )

    return st.session_state.page