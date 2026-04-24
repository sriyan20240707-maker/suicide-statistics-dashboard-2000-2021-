import streamlit as st
import plotly.graph_objects as go
from styles import LAYOUT

def show_pie_chart(df_gender):
    countries = sorted(df_gender['REF_AREA_LABEL'].dropna().unique())
    country   = st.selectbox("Country", ["All"] + countries, key="pie_country")

    d = df_gender[df_gender['TIME_PERIOD'] == st.session_state.year]
    if country != "All": d = d[d['REF_AREA_LABEL'] == country]

    pie = d.groupby('SEX_LABEL')['OBS_VALUE'].mean().reset_index()

    fig = go.Figure(go.Pie(labels=pie['SEX_LABEL'], values=pie['OBS_VALUE'], hole=0.6,
        # CHANGED: pie slice colours were #2EC4B6 / #F472B6 → #5B3FD6 (deep purple) / #C084FC (soft lavender)
        marker=dict(colors=["#2EC4B6","#F472B6"], line=dict(color="#FFFFFF", width=2)),  # CHANGED: line was #0b1220 → #FFFFFF
        textinfo='percent+label', textfont=dict(color="#1E2235")))   # CHANGED: text was #c8d6e8 → charcoal
    layout_override = {
        **LAYOUT,
        "height": 220,
        "margin": dict(l=5, r=60, t=10, b=10),
        "xaxis": dict(
            title="Rate per 100k",
            gridcolor="#D0D8F0",    # CHANGED: was #2EC4B6 → light periwinkle
            tickfont=dict(color="#5A6480")   # CHANGED: was #8899aa → slate
        ),
        "yaxis": dict(
            tickfont=dict(color="#1E2235"),  # CHANGED: was #c8d6e8 → charcoal
            gridcolor="#D0D8F0"     # CHANGED: was #2EC4B6 → light periwinkle
        )
    }

    fig.update_layout(**layout_override)
    st.plotly_chart(fig, use_container_width=True)