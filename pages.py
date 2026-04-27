import streamlit as st
from map_chart import show_map
from line_chart1 import show_line_chart
from bar_chart1 import show_bar_chart
from pie_chart1 import show_pie_chart
from Pie_chart2 import show_pie_chart_2
from kpi import show_kpis


def show_home():
    if st.session_state.get("ribbon_img"):
        st.markdown(f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{st.session_state['ribbon_img']}");
            background-size: fill;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
     <div style="display:flex;
                flex-direction:column;
                align-items:center;
                justify-content:center;
                min-height:70vh;
                text-align:center;
                gap:16px">            
    <div style="display:flex;
                flex-direction:column;
                align-items:center;
                justify-content:center;
                min-height:70vh;
                text-align:center;
                gap:16px">
      <h1 style="color:#5B3FD6;font-size:80px;font-weight:700;line-height:1.1;margin:0;letter-spacing:3px;text-transform:uppercase">Global Suicide<br>Statistics Dashboard</h1>
      <p style="color:#1E2235;font-size:25px;max-width:520px;line-height:1.6;margin:0">Analysing mortality data across 233 countries from 2000 to 2021.</p>
      <div style="margin-top:16px;padding:18px 28px;background:rgba(238,240,251,0.85);border:1px solid #D0D8F0;border-radius:50px;max-width:600px;color:#1E2235;font-size:20px;font-style:italic;line-height:1.6">
        "Even the darkest night will end and the sun will rise."<br>
        <span style="color:#5A6480;font-size:18px">— Victor Hugo</span>
      </div>
      <p style="color:#E05D7B;font-size:17px">If you or someone you know is struggling, please reach out for help!</p>
    </div>""", unsafe_allow_html=True)


def _section(title):
    st.markdown(f'<div style="color:#1AADA4;font-size:15px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border-bottom:2px solid #1AA39A;padding-bottom:6px;margin:20px 0 12px 0">{title}</div>', unsafe_allow_html=True)


def _card(col, label, value, sub, color):
    col.markdown(f'''
        <div style="background:rgba(150,111,214,0.25);border:1px solid #966FD6;border-radius:12px;padding:16px 20px">
            <div style="color:#5A6480;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">{label}</div>
            <div style="color:{color};font-size:22px;font-weight:700">{value}</div>
            <div style="color:#8899AA;font-size:13px;margin-top:4px">{sub}</div>
        </div>''', unsafe_allow_html=True)


def show_global_overview(df, df_total, df_gender):
    _section("Key Performance Indicators")
    show_kpis(df, df_total, df_gender)
    _section("Global Suicide Rate Map")
    show_map(df)


def show_trends(df, df_total, df_gender):

    st.info("Trend charts are controlled by their own local filters.")

    # Read the sex filter — default to 'Total' on first load (before the widget exists).
    # "All" is treated the same as "Total" for KPI purposes (World Total = global aggregate).
    raw_sex = st.session_state.get("line_sex", "Total")
    kpi_sex = "Total" if raw_sex == "All" else raw_sex

    latest = df['TIME_PERIOD'].max()
    prev   = sorted(df['TIME_PERIOD'].unique())[-2]
    first  = df['TIME_PERIOD'].min()

    # -- World row filtered by kpi_sex --
    world     = df[df['REF_AREA_LABEL'] == 'World']
    world_sex = world[world['SEX_LABEL'] == kpi_sex]

    world_latest = world_sex[world_sex['TIME_PERIOD'] == latest]['OBS_VALUE']
    world_prev   = world_sex[world_sex['TIME_PERIOD'] == prev  ]['OBS_VALUE']
    trend_pct    = ((world_latest.values[0] - world_prev.values[0]) / world_prev.values[0] * 100) \
                   if not world_latest.empty and not world_prev.empty else 0

    # Best Performing Year: World row, filtered sex
    world_by_year = world_sex.set_index('TIME_PERIOD')['OBS_VALUE']
    best_year     = world_by_year.idxmin()
    best_year_val = world_by_year.min()

    # -- Country-level data filtered by kpi_sex --
    if kpi_sex == "Total":
        df_sex = df_total
    else:
        df_sex = df_gender[df_gender['SEX_LABEL'] == kpi_sex]

    change = (df_sex[df_sex['TIME_PERIOD']==latest].groupby('REF_AREA_LABEL')['OBS_VALUE'].first() -
              df_sex[df_sex['TIME_PERIOD']==first ].groupby('REF_AREA_LABEL')['OBS_VALUE'].first()).dropna()

    best_country     = df_sex.groupby('REF_AREA_LABEL')['OBS_VALUE'].mean().idxmin()
    best_country_val = df_sex.groupby('REF_AREA_LABEL')['OBS_VALUE'].mean().min()

    tc = "#E05D7B" if trend_pct > 0 else "#00B89C"

    _section(f"Key Performance Indicators — {kpi_sex}")
    c1, c2, c3, c4 = st.columns(4)
    _card(c1, "Global Trend",            "Worsening" if trend_pct > 0 else "Improving", f"{trend_pct:+.1f}% vs {int(prev)}", tc)
    _card(c2, "Most Improved Country",   change.idxmin(),      f"{change.min():.2f} change", "#00B89C")
    _card(c3, "Best Performing Year",    str(int(best_year)),  f"{best_year_val:.2f} rate (World)", "#00B89C")
    _card(c4, "Best Performing Country", best_country,         f"{best_country_val:.2f} avg rate", "#1AADA4")

    _section("Time Series")
    show_line_chart(df)


def show_country_analysis(df, df_gender, df_full):
    _section("Nations at a Glance")
    c1, c2 = st.columns([1.4, 1])
    with c1:
        show_bar_chart(df)
    with c2:
        _section("Regional Risk")
        show_pie_chart_2(df_full)
        _section("Gender Split")
        show_pie_chart(df_gender, df)