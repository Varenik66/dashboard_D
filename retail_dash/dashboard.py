import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 KPI Дашборд", layout="wide")
st.title("📊 Интерактивный дашборд розничной аналитики")

# === Загрузка файлов ===
abc_file = st.sidebar.file_uploader("📘 ABC-анализ", type="xlsx")
season_file = st.sidebar.file_uploader("🌤 Индекс сезонности", type="xlsx")
internet_file = st.sidebar.file_uploader("🌐 Интернет динамика", type="xlsx")
growth_file = st.sidebar.file_uploader("📈 Прирост прибыли", type="xlsx")
avg_price_file = st.sidebar.file_uploader("💰 Средняя цена продажи", type="xlsx")

# === Секция 1: ABC-Анализ ===
if abc_file:
    st.subheader("📘 ABC-анализ по месяцам")
    abc_df = pd.read_excel(abc_file)
    st.dataframe(abc_df, use_container_width=True)

# === Секция 2: Индекс сезонности ===
if season_file:
    st.subheader("🌤 Индекс сезонности по категориям")
    season_df = pd.read_excel(season_file)

    col_name = season_df.columns[0]
    selected_cat = st.selectbox("Выберите категорию", season_df[col_name].unique())
    season_value = season_df[season_df[col_name] == selected_cat].iloc[0, 1]

    st.metric(label=f"Сезонность: {selected_cat}", value=f"{season_value:.2%}")

# === Секция 3: График интернет-динамики ===
if internet_file:
    st.subheader("🌐 Динамика интернет-продаж")
    internet_df = pd.read_excel(internet_file)

    # Предполагаем: первая колонка — Название, остальные — месяцы
    melted = internet_df.melt(id_vars=internet_df.columns[0], var_name="Месяц", value_name="Значение")
    fig = px.line(melted, x="Месяц", y="Значение", color=internet_df.columns[0])
    st.plotly_chart(fig, use_container_width=True)

# === Секция 4: График прироста прибыли ===
if growth_file:
    st.subheader("📈 Прирост валовой прибыли")
    growth_df = pd.read_excel(growth_file)
    segment = st.selectbox("Выберите сегмент", growth_df["Названия строк"].unique())
    row = growth_df[growth_df["Названия строк"] == segment].drop(columns="Названия строк").T
    row.columns = ["Прирост (%)"]
    row = row.reset_index().rename(columns={"index": "Месяц"})

    fig = px.line(row, x="Месяц", y="Прирост (%)", title=f"Прирост по: {segment}")
    st.plotly_chart(fig, use_container_width=True)

# === Секция 5: Средняя цена продажи ===
if avg_price_file:
    st.subheader("💰 Средняя цена продажи (ASP)")
    asp_df = pd.read_excel(avg_price_file)
    segment = st.selectbox("Выберите сегмент ASP", asp_df["Названия строк"].unique())
    row = asp_df[asp_df["Названия строк"] == segment].drop(columns="Названия строк").T
    row.columns = ["ASP"]
    row = row.reset_index().rename(columns={"index": "Месяц"})

    fig = px.line(row, x="Месяц", y="ASP", title=f"Средняя цена: {segment}")
    st.plotly_chart(fig, use_container_width=True)
