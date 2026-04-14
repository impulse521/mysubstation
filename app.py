import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск оборудования", layout="wide")

st.title("🔎 Поиск оборудования ПС")

@st.cache_data
def load_data():
    try:
        # Читаем Excel, преобразуем всё в текст
        df = pd.read_excel("base.xlsx", engine='openpyxl').fillna("—")
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Ошибка загрузки base.xlsx: {e}")
        return None

df = load_data()

# Создаем две колонки для ввода: 4 части для текста, 1 часть для кнопки
col_input, col_btn = st.columns([4, 1])

with col_input:
    query = st.text_input("Введите номер позиции:", placeholder="X-8303-P1-S", label_visibility="collapsed").strip().upper()

with col_btn:
    find_clicked = st.button("Найти", use_container_width=True)

# Поиск срабатывает при нажатии кнопки или при нажатии Enter в поле
if (query or find_clicked) and df is not None:
    first_col = df.columns[0]
    result = df[df[first_col].astype(str).str.upper().str.contains(query, na=False)]

    if not result.empty:
        st.success(f"Найдено записей: {len(result)}")
        for i in range(len(result)):
            row = result.iloc[i]
            with st.expander(f"📍 Позиция: {row[first_col]}", expanded=True):
                # Вывод с вашими названиями
                st.write(f"**Наименование:** {row.iloc[1] if len(row)>1 else '—'}")
                st.write(f"**РУ:** {row.iloc[2] if len(row)>2 else '—'}")
                st.write(f"**Ячейка:** {row.iloc[3] if len(row)>3 else '—'}")
                st.write(f"**Схема:** {row.iloc[4] if len(row)>4 else '—'}")
            st.markdown("---")
    elif query:
        st.error("Ничего не найдено.")

# Кнопка обновления базы внизу страницы
if st.sidebar.button("🔄 Найти"):
    st.cache_data.clear()
    st.rerun()
