import streamlit as st
import plotly.express as px
from styles import LAYOUT

def show_map(df):
    dff = df[(df['TIME_PERIOD'] == st.session_state.year) & (df['SEX_LABEL'] == st.session_state.sex)]
    if dff.empty:
        st.warning("No data available."); return

    dff = dff.groupby(['REF_AREA','REF_AREA_LABEL'], as_index=False)['OBS_VALUE'].mean()

    # NOTE: choropleth colour scale (blue→green→yellow→red) intentionally preserved — severity indicator
    fig = px.choropleth(dff, locations='REF_AREA', locationmode='ISO-3',
        color='OBS_VALUE', hover_name='REF_AREA_LABEL',
        color_continuous_scale=[[0,"#36749e"],[0.4,"#369e3b"],[0.7,"#ffdd00"],[1,"#ff3c00"]],
        range_color=[dff['OBS_VALUE'].min(), dff['OBS_VALUE'].max()])

    layout = {**LAYOUT, "height": 460, "margin": dict(l=0,r=0,t=0,b=10),
        # CHANGED: colorbar bg was #131929 → #FFFFFF; border was #1e2d42 → #D0D8F0; tick was #8899aa → #5A6480
        "coloraxis_colorbar": dict(title="Rate/100k", tickfont=dict(color="#5A6480"), bgcolor="#FFFFFF", bordercolor="#D0D8F0"),
        # CHANGED: map bg was #0b1220 → #EEF0FB (light lavender); country/coast lines were #1e2d42 → #D0D8F0; ocean was #0b1220 → #EEF0FB
        "geo": dict(bgcolor='#EEF0FB', showframe=False, showcountries=True, countrycolor='#D0D8F0',
                    showcoastlines=True, coastlinecolor='#D0D8F0', showocean=True, oceancolor='#EEF0FB')}
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)