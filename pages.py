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
      
      <h1 style="color:#5B3FD6;
                font-size:80px;
                font-weight:700;
                line-height:1.1;
                margin:0;
                letter-spacing:3px;
                text-transform:uppercase">Global Suicide<br>Statistics Dashboard</h1>
      <!-- CHANGED: title colour was #0b1220 → #5B3FD6 (deep purple) -->
      <p style="color:#1E2235;
                font-size:25px;
                max-width:520px;
                line-height:1.6;
                margin:0">Analysing mortality data across 233 countries from 2000 to 2021.</p>
      <!-- CHANGED: subtitle colour was #0b1220 → #1E2235 (charcoal) -->
      <div style="margin-top:16px;
                padding:18px 28px;
                background: rgba(238, 240, 251, 0.85);
                border:1px solid #D0D8F0;
                border-radius:50px;
                max-width:600px;
                color:#1E2235;
                font-size:20px;
                font-style:italic;
                line-height:1.6">
        "Even the darkest night will end and the sun will rise."<br>
        <span style="color:#5A6480;
                font-size:18px">— Victor Hugo</span>
      </div>
      <p style="color:#E05D7B;
                font-size:17px">If you or someone you know is struggling, please reach out for help!</p>
    </div>""", unsafe_allow_html=True)

# CHANGED: section divider colour was #3ce1ff → #1AADA4 (teal); bg label colour was #3ce1ff → #1AADA4
def _section(title):
    st.markdown(f'<div style="color:#1AADA4;font-size:15px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border-bottom:2px solid #1AA39A;padding-bottom:6px;margin:20px 0 12px 0">{title}</div>', unsafe_allow_html=True)
    # CHANGED: text colour was #3ce1ff → #1AADA4; border was #1e2d42 → #D0D8F0

def show_global_overview(df, df_total, df_gender):
    _section("Key Performance Indicators")
    show_kpis(df, df_total, df_gender)
    _section("Global Suicide Rate Map")
    show_map(df)

def show_trends(df, df_total, df_gender):
    st.info("📈 Trend charts are controlled by their own local filters.")
    latest = df_total['TIME_PERIOD'].max()
    prev   = sorted(df_total['TIME_PERIOD'].unique())[-2]
    first  = df_total['TIME_PERIOD'].min()

    trend_pct = (df_total[df_total['TIME_PERIOD']==latest]['OBS_VALUE'].mean() -
                 df_total[df_total['TIME_PERIOD']==prev  ]['OBS_VALUE'].mean()) / \
                 df_total[df_total['TIME_PERIOD']==prev  ]['OBS_VALUE'].mean() * 100
    change = (df_total[df_total['TIME_PERIOD']==latest].groupby('REF_AREA_LABEL')['OBS_VALUE'].mean() -
              df_total[df_total['TIME_PERIOD']==first ].groupby('REF_AREA_LABEL')['OBS_VALUE'].mean()).dropna()

    yearly_avg       = df_total.groupby('TIME_PERIOD')['OBS_VALUE'].mean()
    best_year        = yearly_avg.idxmin()
    best_year_val    = yearly_avg.min()
    country_avg      = df_total.groupby('REF_AREA_LABEL')['OBS_VALUE'].mean()
    best_country     = country_avg.idxmin()
    best_country_val = country_avg.min()

    # CHANGED: trend colour was #f76a6a / #3ecf8e → #E05D7B / #00B89C
    tc = "#E05D7B" if trend_pct > 0 else "#00B89C"

    _section("Summary")
    c1, c2, c3, c4 = st.columns(4)

    # CHANGED: all card backgrounds were #131929 → rgba(6,148,148, 0.15); borders were #1e2d42 → #D0D8F0
    c1.markdown(f'''
        <div style="background:rgba(6,148,148, 0.15);border:1px solid #D0D8F0;border-radius:12px;padding:16px 20px;box-shadow:0 2px 8px rgba(91,63,214,0.20)">
            <div style="color:#5A6480;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">
                📊 Global Trend
            </div>
            <div style="color:{tc};font-size:22px;font-weight:700">
                {"Worsening ↑" if trend_pct > 0 else "Improving ↓"}
            </div>
            <div style="color:{tc};font-size:13px;margin-top:4px">
                {trend_pct:+.1f}% vs previous year
            </div>
        </div>''', unsafe_allow_html=True)

    c2.markdown(f'''
        <div style="background:rgba(6,148,148, 0.15);border:1px solid #D0D8F0;border-radius:12px;padding:16px 20px;box-shadow:0 2px 8px rgba(91,63,214,0.20)">
            <div style="color:#5A6480;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">
                📈 Most Improved Country
            </div>
            <div style="color:#00B89C;font-size:20px;font-weight:700">
                {change.idxmin()}
            </div>
            <div style="color:#00B89C;font-size:13px;margin-top:4px">
                {change.min():.2f} change
            </div>
        </div>''', unsafe_allow_html=True)

    c3.markdown(f'''
        <div style="background:rgba(6,148,148, 0.15);border:1px solid #D0D8F0;border-radius:12px;padding:16px 20px;box-shadow:0 2px 8px rgba(91,63,214,0.20)">
            <div style="color:#5A6480;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">
                🏆 Best Performing Year
            </div>
            <div style="color:#00B89C;font-size:22px;font-weight:700">
                {best_year}
            </div>
            <div style="color:#8899AA;font-size:13px;margin-top:4px">
                {best_year_val:.2f} avg rate
            </div>
        </div>''', unsafe_allow_html=True)

    c4.markdown(f'''
        <div style="background:rgba(6,148,148, 0.15);border:1px solid #D0D8F0;border-radius:12px;padding:16px 20px;box-shadow:0 2px 8px rgba(91,63,214,0.20)">
            <div style="color:#5A6480;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">
                🌟 Best Performing Country
            </div>
            <div style="color:#1AADA4;font-size:22px;font-weight:700">
                {best_country}
            </div>
            <!-- CHANGED: value colour was #3ce1ff → #1AADA4 (teal) -->
            <div style="color:#8899AA;font-size:13px;margin-top:4px">
                {best_country_val:.2f} avg rate
            </div>
        </div>''', unsafe_allow_html=True)

    _section("Time Series")
    show_line_chart(df)


def show_country_analysis(df, df_total, df_gender):
    _section("Nations at a Glance")
    c1, c2 = st.columns([1.4, 1])
    with c1:
        show_bar_chart(df)
    with c2:
        _section("Regional Risk")
        show_pie_chart_2(df)
        _section("Gender Split")
        show_pie_chart(df_gender)