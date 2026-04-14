import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск оборудования", layout="centered")

st.title("🔎 Поиск оборудования ПС")

@st.cache_data
def load_data():
    try:
        # Загружаем данные
        df = pd.read_excel("base.xlsx", engine='openpyxl').fillna("—")
        return df
    except Exception as e:
        st.error(f"Ошибка загрузки базы: {e}")
        return None

df = load_data()

# Создаем колонки: 80% под ввод, 20% под кнопку сброса
col_input, col_clear = st.columns([4, 1])

with col_input:
    query = st.text_input("Введите номер позиции:", placeholder="X-8303-P1-S", label_visibility="collapsed").strip().upper()

with col_clear:
    if st.button("Сброс", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# Логика поиска
if query and df is not None:
    # Определяем колонку с позициями (обычно первая)
    first_col = df.columns[0]
    result = df[df[first_col].astype(str).str.upper().str.contains(query, na=False)]

    if not result.empty:
        st.success(f"Найдено: {len(result)}")
        for i in range(len(result)):
            row = result.iloc[i]
            with st.expander(f"📍 Позиция: {row[0]}", expanded=True):
                # Вывод с вашими названиями по порядку столбцов в Excel
                st.write(f"**Наименование:** {row[1]}")
                st.write(f"**РУ:** {row[2]}")
                st.write(f"**Ячейка:** {row[3]}")
                st.write(f"**Схема:** {row[4]}")
            st.markdown("---")
    else:
        st.error("Позиция не найдена")

st.markdown("<small>Введите номер и нажмите Enter для поиска</small>", unsafe_allow_html=True)
