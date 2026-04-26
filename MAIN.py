import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from styles import apply_sidebar
from pages import show_home, show_global_overview, show_trends, show_country_analysis

st.set_page_config(page_title="Global Suicide Statistics", layout="wide")

df = pd.read_csv("FINAL_WB_WDI_SH_STA_SUIC_.csv")
df = df[['REF_AREA','REF_AREA_LABEL','SEX_LABEL','TIME_PERIOD','OBS_VALUE']].dropna()
df['OBS_VALUE']   = pd.to_numeric(df['OBS_VALUE'],   errors='coerce')
df['TIME_PERIOD'] = pd.to_numeric(df['TIME_PERIOD'], errors='coerce')

# ── All non-country labels to exclude from country-level charts ──
REGIONS = [
    'East Asia & Pacific','Europe & Central Asia','Latin America & Caribbean',
    'Middle East, North Africa, Afghanistan & Pakistan','North America',
    'South Asia','Sub-Saharan Africa','Eastern & Southern Africa',
    'Western & Central Africa','Arab World','Euro area','European Union',
    'Central Europe and the Baltics','World'
]

NON_COUNTRIES = [
    'High income','Low income','Low & middle income','Lower middle income',
    'Middle income','Upper middle income','IBRD only','IDA & IBRD total',
    'IDA blend','IDA only','IDA total','Early-demographic dividend',
    'Late-demographic dividend','Post-demographic dividend','Pre-demographic dividend',
    'Fragile and conflict affected situations','Heavily indebted poor countries (HIPC)',
    'Least developed countries: UN classification','OECD members','Small states',
    'Other small states','Pacific island small states','Caribbean small states',
    'East Asia & Pacific (IDA & IBRD)','Europe & Central Asia (IDA & IBRD)',
    'Latin America & Caribbean (IDA & IBRD)',
    'Middle East, North Africa, Afghanistan & Pakistan (IDA & IBRD)',
    'South Asia (IDA & IBRD)','Sub-Saharan Africa (IDA & IBRD)',
    'East Asia & Pacific (excluding high income)',
    'Europe & Central Asia (excluding high income)',
    'Latin America & Caribbean (excluding high income)',
    'Middle East, North Africa, Afghanistan & Pakistan (excluding high income)',
    'Sub-Saharan Africa (excluding high income)',
]

EXCLUDE = REGIONS + NON_COUNTRIES

# df = full dataset (used only for regional chart)
# df_countries = countries only (used everywhere else)
df_countries = df[~df['REF_AREA_LABEL'].isin(EXCLUDE)].reset_index(drop=True)

df_total   = df_countries[df_countries['SEX_LABEL'] == 'Total']
df_gender  = df_countries[df_countries['SEX_LABEL'].isin(['Male','Female'])]

page = apply_sidebar()
if   page == "🏠 Home":             show_home()
elif page == "🌍 Global Overview":  show_global_overview(df_countries, df_total, df_gender)
elif page == "📈 Trends":           show_trends(df_countries, df_total, df_gender)
elif page == "📊 Country Analysis": show_country_analysis(df_countries, df_gender, df)