import streamlit as st
import plotly.graph_objects as go
from styles import LAYOUT

COLORS = {"Total": "#1CA527", "Male": "#1C38A5", "Female": "#D11194"}

def _build(data, sex):
    fig = go.Figure()
    sexes = list(COLORS) if sex == "All" else [sex]
    for s in sexes:
        d = data[data['SEX_LABEL'] == s][['TIME_PERIOD', 'OBS_VALUE']].dropna()
        d = d.groupby('TIME_PERIOD')['OBS_VALUE'].first().reset_index()
        fig.add_trace(go.Scatter(x=d['TIME_PERIOD'], y=d['OBS_VALUE'], name=s,
            mode='lines+markers', line=dict(color=COLORS[s], width=2.5), marker=dict(size=5)))
    fig.update_layout(**LAYOUT, height=360, xaxis_title="Year", yaxis_title="Rate per 100k", hovermode="x unified")
    return fig

def show_line_chart(df):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Global Average Trend")
        sex = st.selectbox("Sex", ["All", "Total", "Male", "Female"], key="line_sex")
        st.plotly_chart(_build(df[df['REF_AREA_LABEL'] == 'World'], sex), use_container_width=True)
    with col2:
        st.subheader("Trend by Country")
        country = st.selectbox("Country", sorted(df['REF_AREA_LABEL'].dropna().unique()), key="line_country")
        st.plotly_chart(_build(df[df['REF_AREA_LABEL'] == country], sex), use_container_width=True)
        st.write(df[df['REF_AREA_LABEL'] == 'World'][['TIME_PERIOD', 'SEX_LABEL', 'OBS_VALUE']])