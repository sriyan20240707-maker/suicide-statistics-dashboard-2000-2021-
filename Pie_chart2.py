import streamlit as st
import plotly.graph_objects as go
from styles import LAYOUT

REGIONS = ['East Asia & Pacific','Europe & Central Asia','Latin America & Caribbean',
           'Middle East, North Africa, Afghanistan & Pakistan','North America',
           'South Asia','Sub-Saharan Africa','Eastern & Southern Africa','Western & Central Africa']

def show_pie_chart_2(df):
    d = (df[(df['TIME_PERIOD']==st.session_state.year) & (df['SEX_LABEL']==st.session_state.sex) & df['REF_AREA_LABEL'].isin(REGIONS)]
         .groupby('REF_AREA_LABEL')['OBS_VALUE'].mean().reset_index().sort_values('OBS_VALUE'))

    if d.empty:
        st.warning("No data available.")
        return

    # NOTE: Blue→red severity gradient intentionally preserved — severity indicator
    mn, mx = d['OBS_VALUE'].min(), d['OBS_VALUE'].max()
    colors = [f"hsl({int(220-(220*(r-mn)/(mx-mn+1e-9)))},70%,55%)" for r in d['OBS_VALUE']]

    fig = go.Figure(go.Bar(
        x=d['OBS_VALUE'],
        y=d['REF_AREA_LABEL'],
        orientation='h',
        marker_color=colors,
        text=d['OBS_VALUE'].map('{:.2f}'.format),
        textposition='outside',
        textfont=dict(color="#5A6480")   # CHANGED: was #8899aa → slate
    ))

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