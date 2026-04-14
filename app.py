import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск оборудования", layout="centered")
st.title("🔎 Поиск оборудования ПС")

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("base.xlsx", engine='openpyxl').fillna("—")
        return df
    except Exception as e:
        st.error(f"Ошибка загрузки базы: {e}")
        return None

df = load_data()

col_input, col_clear = st.columns([4, 1])

with col_input:
    # Теперь в подсказке указано, что искать можно и по названию
    query = st.text_input("Поиск", placeholder="Введите номер или наименование...", label_visibility="collapsed").strip().upper()

with col_clear:
    if st.button("Сброс", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if query and df is not None:
    # Извлекаем названия первых двух колонок (A и B)
    cols = df.columns
    pos_col = cols[0]    # Позиция
    name_col = cols[1]   # Наименование
    
    # Ищем совпадение либо в колонке "Позиция", либо в колонке "Наименование"
    mask = (df[pos_col].astype(str).str.upper().str.contains(query, na=False)) | \
           (df[name_col].astype(str).str.upper().str.contains(query, na=False))
    
    result = df[mask]

    if not result.empty:
        st.success(f"Найдено записей: {len(result)}")
        for i in range(len(result)):
            row = result.iloc[i]
            # Заголовок карточки — Позиционный номер
            with st.expander(f"📍 {row.iloc[0]} — {row.iloc[1]}", expanded=True):
                st.write(f"**Наименование:** {row.iloc[1]}")
                st.write(f"**РУ:** {row.iloc[2]}")
                st.write(f"**Ячейка:** {row.iloc[3]}")
                st.write(f"**Мощность:** {row.iloc[4]}")
                st.write(f"**Схема:** {row.iloc[5]}")
            st.markdown("---")
    else:
        st.error("Ничего не найдено.")
