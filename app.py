import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск оборудования", layout="centered")
st.title("🔎 Поиск оборудования ПС")

@st.cache_data
def load_data():
    try:
        # Загружаем Excel без привязки к названиям колонок
        df = pd.read_excel("base.xlsx", engine='openpyxl').fillna("—")
        return df
    except Exception as e:
        st.error(f"Ошибка загрузки базы: {e}")
        return None

df = load_data()

# Колонки для ввода: текстовое поле + кнопка Найти
col_input, col_clear = st.columns([5, 1])

with col_input:
    query = st.text_input("Поиск", placeholder="Введите номер позиции и нажмите Enter...", label_visibility="collapsed").strip().upper()

with col_clear:
    if st.button("Найти", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if query and df is not None:
    # Поиск по самому первому столбцу (А)
    first_col_name = df.columns[0]
    result = df[df[first_col_name].astype(str).str.upper().str.contains(query, na=False)]

    if not result.empty:
        st.success(f"Найдено: {len(result)}")
        for i in range(len(result)):
            row = result.iloc[i]
            # .iloc[номер] берет данные по порядку: 0-первый, 1-второй и т.д.
            with st.expander(f"📍 Позиция: {row.iloc[0]}", expanded=True):
                st.write(f"**Наименование:** {row.iloc[1] if len(row) > 1 else '—'}")
                st.write(f"**РУ:** {row.iloc[2] if len(row) > 2 else '—'}")
                st.write(f"**Ячейка:** {row.iloc[3] if len(row) > 3 else '—'}")
                st.write(f"**Мощность:** {row.iloc[4] if len(row) > 4 else '—'}")
                st.write(f"**Схема:** {row.iloc[5] if len(row) > 5 else '—'}")
            st.markdown("---")
    else:
        st.error("Ничего не найдено.")
