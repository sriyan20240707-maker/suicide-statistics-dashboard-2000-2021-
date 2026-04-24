import streamlit as st
import plotly.graph_objects as go
from styles import LAYOUT

def show_bar_chart(df):
    data = df[(df['TIME_PERIOD']==st.session_state.year) & (df['SEX_LABEL']==st.session_state.sex)]
    if data.empty:
        st.warning("No data available.")
        return

    ranked = data.groupby('REF_AREA_LABEL')['OBS_VALUE'].mean().sort_values(ascending=False).reset_index()
    ranked.columns = ['Country', 'Rate']

    show = st.selectbox("Show", ["Highest 10", "Lowest 10", "All Countries"], key="bar_rank")
    
    if show == "Highest 10":
        bar = ranked.head(10)
    elif show == "Lowest 10":
        bar = ranked.tail(10).sort_values('Rate', ascending=False)
    else:
        bar = ranked

    # NOTE: Blue→red severity gradient intentionally preserved — not changed
    mn, mx = ranked['Rate'].min(), ranked['Rate'].max()
    colors = [f"hsl({int(220-(220*(r-mn)/(mx-mn+1e-9)))},70%,55%)" for r in bar['Rate']]

    if 'bar_start' not in st.session_state or show != "All Countries":
        st.session_state.bar_start = 0
    start = st.session_state.bar_start
    visible = 10 if show == "All Countries" else len(bar)

    fig = go.Figure(go.Bar(
        x=bar['Country'],
        y=bar['Rate'],
        marker_color=colors,
        hovertemplate="<b>%{x}</b><br>Rate: %{y:.2f}<extra></extra>"
    ))

    layout_override = {
        **LAYOUT,
        "height": 583,
        "showlegend": False,
        "bargap": 0.25,
        "xaxis": dict(
            range=[start - .5, start + visible - .5],
            tickangle=-40,
            gridcolor="#D0D8F0",       # CHANGED: was #2EC4B6 → light periwinkle border
            tickfont=dict(color="#5A6480")   # CHANGED: was #8899aa → slate
        ),
        "yaxis": dict(
            title="Rate per 100k",
            gridcolor="#D0D8F0",       # CHANGED: was #2EC4B6 → light periwinkle border
            tickfont=dict(color="#5A6480")   # CHANGED: was #8899aa → slate
        )
    }

    fig.update_layout(**layout_override)
    st.plotly_chart(fig, use_container_width=True)

    if show == "All Countries":
        c1, _, c3 = st.columns([1, 8, 1])
        if c1.button("◀ Prev"):
            st.session_state.bar_start = max(0, start - 10)
        if c3.button("Next ▶"):
            st.session_state.bar_start = min(len(ranked) - 10, start + 10)