import streamlit as st

def show_kpis(df, df_total, df_gender):
    latest = df_total['TIME_PERIOD'].max()
    first  = df_total['TIME_PERIOD'].min()
    prev   = sorted(df_total['TIME_PERIOD'].unique())[-2]
    year   = st.session_state.year
    sex    = st.session_state.sex

    # 🌍 Global Avg Rate — reacts to year + sex
    ys_data    = df[(df['TIME_PERIOD']==year) & (df['SEX_LABEL']==sex)]
    global_avg = ys_data['OBS_VALUE'].mean() if not ys_data.empty else df[df['TIME_PERIOD']==year]['OBS_VALUE'].mean()

    # ⚠️ Highest Risk Country — reacts to year + sex
    ys_grp      = ys_data.groupby('REF_AREA_LABEL')['OBS_VALUE'].mean()
    if ys_grp.empty:
        ys_grp  = df[df['TIME_PERIOD']==year].groupby('REF_AREA_LABEL')['OBS_VALUE'].mean()
    top_country = ys_grp.idxmax()
    top_val     = ys_grp.max()

    # ⚖️ Gender Gap — reacts to year only
    y_gender    = df_gender[df_gender['TIME_PERIOD']==year]
    gender_gap  = (y_gender[y_gender['SEX_LABEL']=='Male']['OBS_VALUE'].mean() -
                   y_gender[y_gender['SEX_LABEL']=='Female']['OBS_VALUE'].mean())

    # 📈 Most Improved — reacts to sex only
    sex_data    = df[df['SEX_LABEL']==sex] if sex != 'Total' else df_total
    latest_grp  = sex_data[sex_data['TIME_PERIOD']==latest].groupby('REF_AREA_LABEL')['OBS_VALUE'].mean()
    first_grp   = sex_data[sex_data['TIME_PERIOD']==first ].groupby('REF_AREA_LABEL')['OBS_VALUE'].mean()
    change      = (latest_grp - first_grp).dropna()
    improved     = change.idxmin() if not change.empty else df_total[df_total['TIME_PERIOD']==latest].groupby('REF_AREA_LABEL')['OBS_VALUE'].mean().sub(df_total[df_total['TIME_PERIOD']==first].groupby('REF_AREA_LABEL')['OBS_VALUE'].mean()).idxmin()
    improved_val = change.min()   if not change.empty else df_total[df_total['TIME_PERIOD']==latest].groupby('REF_AREA_LABEL')['OBS_VALUE'].mean().sub(df_total[df_total['TIME_PERIOD']==first].groupby('REF_AREA_LABEL')['OBS_VALUE'].mean()).min()

    # 📊 Global Trend — reacts to sex only
    sex_latest  = sex_data[sex_data['TIME_PERIOD']==latest]['OBS_VALUE'].mean()
    sex_prev    = sex_data[sex_data['TIME_PERIOD']==prev  ]['OBS_VALUE'].mean()
    trend_pct   = (sex_latest - sex_prev) / sex_prev * 100
    trend_label = "Worsening ↑" if trend_pct > 0 else "Improving ↓"
    trend_color = "#e05d5d"     if trend_pct > 0 else "#3ecf8e"

    cards = [
        ("#5A6480",    "Global Avg Rate",      f"{global_avg:.2f}",   "per 100k"),
        ("#e0ae27",    "Highest Risk Country", top_country,           f"{top_val:.2f}"),
        ("#5A6480",    "Gender Gap",           f"{gender_gap:.2f}",   "Male − Female"),
        ("#2bba7a",    "Most Improved",         improved,              f"{improved_val:.2f}"),
        (trend_color,  "Global Trend",          trend_label,           f"{trend_pct:+.1f}% vs prev yr"),
    ]

    cols = st.columns(5)
    for col, (color, label, value, sub) in zip(cols, cards):
        col.markdown(f"""
        <div style="background:rgba(150, 111, 214, 0.25);border:1px solid #966FD6;border-radius:12px;padding:16px 18px";rgba(249,155,255, 0.25)>
          <div style="color:#8899aa;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">{label}</div>
          <div style="color:{color};font-size:22px;font-weight:700;line-height:1.2">{value}</div>
          <div style="color:#5a7a9a;font-size:11px;margin-top:4px">{sub}</div>
        </div>""", unsafe_allow_html=True)


def show_trend_kpis(df_total):
    best_year        = df_total.groupby('TIME_PERIOD')['OBS_VALUE'].mean().idxmin()
    best_year_val    = df_total.groupby('TIME_PERIOD')['OBS_VALUE'].mean().min()
    best_country     = df_total.groupby('REF_AREA_LABEL')['OBS_VALUE'].mean().idxmin()
    best_country_val = df_total.groupby('REF_AREA_LABEL')['OBS_VALUE'].mean().min()

    c1, c2 = st.columns(2)
    c1.markdown(f"""
    <div style="background:rgba(150, 111, 214, 0.25);border:1px solid #966FD6;border-radius:12px;padding:16px 18px">
      <div style="color:#8899aa;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">Best Performing Year</div>
      <div style="color:#3ecf8e;font-size:26px;font-weight:700;line-height:1.2">{int(best_year)}</div>
      <div style="color:#5a7a9a;font-size:11px;margin-top:4px">avg rate {best_year_val:.2f} per 100k</div>
    </div>""", unsafe_allow_html=True)
    c2.markdown(f"""
    <div style="background:rgba(150, 111, 214, 0.25);border:1px solid #966FD6;border-radius:12px;padding:16px 18px">
      <div style="color:#8899aa;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">Best Performing Country</div>
      <div style="color:#3ecf8e;font-size:22px;font-weight:700;line-height:1.2">{best_country}</div>
      <div style="color:#5a7a9a;font-size:11px;margin-top:4px">avg rate {best_country_val:.2f} per 100k</div>
    </div>""", unsafe_allow_html=True)