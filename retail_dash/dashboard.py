# import streamlit as st
# import pandas as pd
# import plotly.express as px
#
# st.set_page_config(page_title="KPI Дашборд", layout="wide")
#
# st.title("📊 Интерактивный дашборд по приросту валовой прибыли")
# st.markdown("Загрузите файл с расчетами и анализируйте прирост по сегментам.")
#
# # Загрузка Excel
# uploaded_file = st.file_uploader("📎 Загрузите Excel-файл", type=["xlsx"])
#
# if uploaded_file:
#     df = pd.read_excel(uploaded_file)
#
#     if "Названия строк" not in df.columns:
#         st.error("Файл должен содержать колонку 'Названия строк'")
#     else:
#         segments = df["Названия строк"].unique()
#         months = list(df.columns[1:])  # Предполагаем, что месяцы идут с 2-й колонки
#
#         st.sidebar.header("📌 Фильтры")
#         selected_segments = st.sidebar.multiselect("Выберите сегменты", segments, default=segments[:3])
#
#         filtered_df = df[df["Названия строк"].isin(selected_segments)]
#
#         # Перевод в длинный формат для plotly
#         melted_df = filtered_df.melt(id_vars="Названия строк", var_name="Месяц", value_name="Прирост")
#
#         col1, col2 = st.columns(2)
#
#         with col1:
#             st.subheader("📈 Линейный график прироста")
#             fig = px.line(melted_df, x="Месяц", y="Прирост", color="Названия строк",
#                           markers=True, labels={"Названия строк": "Сегмент"})
#             fig.update_layout(legend_title_text="Сегмент", height=400)
#             st.plotly_chart(fig, use_container_width=True)
#
#         with col2:
#             st.subheader("📊 Столбчатая диаграмма (суммарный прирост)")
#             sum_df = melted_df.groupby("Названия строк")["Прирост"].sum().reset_index()
#             fig2 = px.bar(sum_df, x="Названия строк", y="Прирост", color="Названия строк",
#                           labels={"Прирост": "Суммарный прирост (%)"}, height=400)
#             st.plotly_chart(fig2, use_container_width=True)
#
#         st.markdown("---")
#         st.subheader("📋 Таблица данных")
#         st.dataframe(filtered_df, use_container_width=True)
#
# else:
#     st.info("Загрузите Excel-файл, чтобы увидеть дашборд.")


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 KPI Дашборд", layout="wide")
st.title("📊 Интерактивный дашборд розничной аналитики")

# === Загрузка данных из локальных файлов (внутри репозитория) ===
abc_df = pd.read_excel("retail_dash/abc_analysis_dynamic.xlsx")
season_df = pd.read_excel("retail_dash/seasonality_index.xlsx")
internet_df = pd.read_excel("retail_dash/internet_dynamic.xlsx")
growth_df = pd.read_excel("retail_dash/growth_table.xlsx")
asp_df = pd.read_excel("retail_dash/avg_price.xlsx")


# === Секция 1: ABC-анализ ===
st.subheader("📘 ABC-анализ по месяцам")
st.dataframe(abc_df, use_container_width=True)

# === Секция 2: Индекс сезонности ===
st.subheader("🌤 Индекс сезонности")
col_name = season_df.columns[0]
selected_cat = st.selectbox("Выберите категорию", season_df[col_name].unique())
season_value = season_df[season_df[col_name] == selected_cat].iloc[0, 1]
st.metric(label=f"Сезонность для: {selected_cat}", value=f"{season_value:.2%}")

# === Секция 3: Динамика интернет-продаж ===
st.subheader("🌐 Интернет-динамика")
melted_internet = internet_df.melt(id_vars=internet_df.columns[0], var_name="Месяц", value_name="Значение")
fig_internet = px.line(melted_internet, x="Месяц", y="Значение", color=internet_df.columns[0])
st.plotly_chart(fig_internet, use_container_width=True)

# === Секция 4: Прирост прибыли ===
st.subheader("📈 Прирост валовой прибыли")
segment = st.selectbox("Выберите сегмент прироста", growth_df["Названия строк"].unique())
row = growth_df[growth_df["Названия строк"] == segment].drop(columns="Названия строк").T
row.columns = ["Прирост (%)"]
row = row.reset_index().rename(columns={"index": "Месяц"})
fig_growth = px.line(row, x="Месяц", y="Прирост (%)", title=f"Прирост: {segment}")
st.plotly_chart(fig_growth, use_container_width=True)

# === Секция 5: Средняя цена продажи ===
st.subheader("💰 Средняя цена продажи (ASP)")
segment_asp = st.selectbox("Выберите сегмент ASP", asp_df["Названия строк"].unique())
row_asp = asp_df[asp_df["Названия строк"] == segment_asp].drop(columns="Названия строк").T
row_asp.columns = ["ASP"]
row_asp = row_asp.reset_index().rename(columns={"index": "Месяц"})
fig_asp = px.line(row_asp, x="Месяц", y="ASP", title=f"Средняя цена: {segment_asp}")
st.plotly_chart(fig_asp, use_container_width=True)
