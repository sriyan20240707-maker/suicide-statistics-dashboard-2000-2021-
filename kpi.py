import streamlit as st

def show_kpis(df, df_total, df_gender):
    latest = df_total['TIME_PERIOD'].max()
    first  = df_total['TIME_PERIOD'].min()
    prev   = sorted(df_total['TIME_PERIOD'].unique())[-2]
    year   = st.session_state.year
    sex    = st.session_state.sex

    # Global Avg Rate — use World row directly
    world = df[(df['REF_AREA_LABEL'] == 'World') & (df['TIME_PERIOD'] == year) & (df['SEX_LABEL'] == sex)]
    global_avg = world['OBS_VALUE'].values[0] if not world.empty else 0

    # Highest Risk Country — use actual country values
    ys_data     = df_total[df_total['TIME_PERIOD'] == year]
    ys_grp      = ys_data.groupby('REF_AREA_LABEL')['OBS_VALUE'].first()
    top_country = ys_grp.idxmax()
    top_val     = ys_grp.max()

    # Gender Gap — reacts to year only
    y_gender   = df_gender[df_gender['TIME_PERIOD'] == year]
    gender_gap = (y_gender[y_gender['SEX_LABEL'] == 'Male']['OBS_VALUE'].mean() -
                  y_gender[y_gender['SEX_LABEL'] == 'Female']['OBS_VALUE'].mean())

    # Most Improved — reacts to sex only
    sex_data    = df[df['SEX_LABEL'] == sex] if sex != 'Total' else df_total
    latest_grp  = sex_data[sex_data['TIME_PERIOD'] == latest].groupby('REF_AREA_LABEL')['OBS_VALUE'].first()
    first_grp   = sex_data[sex_data['TIME_PERIOD'] == first].groupby('REF_AREA_LABEL')['OBS_VALUE'].first()
    change      = (latest_grp - first_grp).dropna()
    improved    = change.idxmin() if not change.empty else "N/A"
    improved_val = change.min() if not change.empty else 0

    # Global Trend — use World row
    world_latest = df[(df['REF_AREA_LABEL'] == 'World') & (df['TIME_PERIOD'] == latest) & (df['SEX_LABEL'] == sex)]['OBS_VALUE']
    world_prev   = df[(df['REF_AREA_LABEL'] == 'World') & (df['TIME_PERIOD'] == prev)   & (df['SEX_LABEL'] == sex)]['OBS_VALUE']
    trend_pct    = ((world_latest.values[0] - world_prev.values[0]) / world_prev.values[0] * 100) if not world_latest.empty and not world_prev.empty else 0
    trend_label  = "Worsening" if trend_pct > 0 else "Improving"
    trend_color  = "#e05d5d" if trend_pct > 0 else "#3ecf8e"

    cards = [
        ("#5A6480",   "Global Avg Rate",      f"{global_avg:.2f}", "per 100k"),
        ("#e0ae27",   "Highest Risk Country", top_country,         f"{top_val:.2f}"),
        ("#5A6480",   "Gender Gap",           f"{gender_gap:.2f}", "Male - Female"),
        ("#2bba7a",   "Most Improved",        improved,            f"{improved_val:.2f}"),
        (trend_color, "Global Trend",         trend_label,         f"{trend_pct:+.1f}% vs prev year"),
    ]

    cols = st.columns(5)
    for col, (color, label, value, sub) in zip(cols, cards):
        col.markdown(f"""
        <div style="background:rgba(150,111,214,0.25);border:1px solid #966FD6;border-radius:12px;padding:16px 18px">
          <div style="color:#8899aa;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px">{label}</div>
          <div style="color:{color};font-size:22px;font-weight:700;line-height:1.2">{value}</div>
          <div style="color:#5a7a9a;font-size:11px;margin-top:4px">{sub}</div>
        </div>""", unsafe_allow_html=True)
