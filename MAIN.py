import streamlit as st
import pandas as pd
from styles import apply_sidebar
from pages import show_home, show_global_overview, show_trends, show_country_analysis

st.set_page_config(page_title="Global Suicide Statistics", layout="wide")

df = pd.read_csv(r"C:\Users\User\Downloads\Final_WB_WDI_SH_STA_SUIC_.csv")
df = df[['REF_AREA','REF_AREA_LABEL','SEX_LABEL','TIME_PERIOD','OBS_VALUE']].dropna()
df['OBS_VALUE']   = pd.to_numeric(df['OBS_VALUE'],   errors='coerce')
df['TIME_PERIOD'] = pd.to_numeric(df['TIME_PERIOD'], errors='coerce')

df_total  = df[df['SEX_LABEL'] == 'Total']
df_gender = df[df['SEX_LABEL'].isin(['Male','Female'])]

page = apply_sidebar()
if   page == "🏠 Home":              show_home()
elif page == "🌍 Global Overview":   show_global_overview(df, df_total, df_gender)
elif page == "📈 Trends":            show_trends(df, df_total, df_gender)
elif page == "📊 Country Analysis":  show_country_analysis(df, df_gender)