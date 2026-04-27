import streamlit as st
import plotly.graph_objects as go
from styles import LAYOUT

def show_pie_chart(df_gender, df):
    countries = sorted(df_gender['REF_AREA_LABEL'].dropna().unique())
    country = st.selectbox("Country", ["All"] + countries, key="pie_country")

    d = df_gender[df_gender['TIME_PERIOD'] == st.session_state.year]
    if country != "All":
        d = d[d['REF_AREA_LABEL'] == country]

    pie = d.groupby('SEX_LABEL')['OBS_VALUE'].mean().reset_index()

    fig = go.Figure(go.Pie(
        labels=pie['SEX_LABEL'],
        values=pie['OBS_VALUE'],
        hole=0.6,
        marker=dict(colors=["#2EC4B6", "#F472B6"], line=dict(color="#FFFFFF", width=2)),
        textinfo='percent+label',
        textfont=dict(color="#1E2235")
    ))

    layout_override = {
        **LAYOUT,
        "height": 220,
        "margin": dict(l=5, r=60, t=10, b=10),
    }
    fig.update_layout(**layout_override)

    chart_col, stats_col = st.columns([2, 1])

    with chart_col:
        st.plotly_chart(fig, use_container_width=True)

    with stats_col:
        male_rate = df_gender[
            (df_gender['SEX_LABEL'] == 'Male') &
            (df_gender['TIME_PERIOD'] == st.session_state.year) &
            (df_gender['REF_AREA_LABEL'] == country if country != "All" else True)
        ]['OBS_VALUE'].mean()

        female_rate = df_gender[
            (df_gender['SEX_LABEL'] == 'Female') &
            (df_gender['TIME_PERIOD'] == st.session_state.year) &
            (df_gender['REF_AREA_LABEL'] == country if country != "All" else True)
        ]['OBS_VALUE'].mean()

        total_rate = df[
            (df['SEX_LABEL'] == 'Total') &
            (df['TIME_PERIOD'] == st.session_state.year) &
            (df['REF_AREA_LABEL'] == country if country != "All" else True)
        ]['OBS_VALUE'].mean()

        all_countries = df[
            (df['SEX_LABEL'] == 'Total') &
            (df['TIME_PERIOD'] == st.session_state.year)
        ].groupby('REF_AREA_LABEL')['OBS_VALUE'].mean().sort_values(ascending=False)

        rank = list(all_countries.index).index(country) + 1 if country != "All" and country in all_countries.index else "N/A"

# Side stats
        st.markdown(f"""
        <div style='
            font-size:15px;
            color:#1E2235;
            background:rgba(150, 111, 214, 0.15);
            border: 2px solid #966FD6;
            border-radius: 10px;
            padding: 5px;
        '>
            <b>{ country if country != 'All' else 'Global'} ({int(st.session_state.year)})</b>
            <hr style='border-color:#2EC4B6; margin: 8px 0;'>
            <b>Global Rank:</b> #{rank}<br><br>
            <b>Total Rate:</b> {total_rate:.2f}<br><br>
            <b>Male Rate:</b> {male_rate:.2f}<br><br>
            <b>Female Rate:</b> {female_rate:.2f}
        </div>
        """, unsafe_allow_html=True)