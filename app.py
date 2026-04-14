import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск оборудования", layout="centered")
st.title("🔎 Поиск оборудования ПС")

@st.cache_data
def load_data():
    try:
        # Читаем все данные, заменяя пустые ячейки на пустую строку
        df = pd.read_excel("base.xlsx", engine='openpyxl').fillna("")
        # Превращаем всё в текст для поиска
        df = df.astype(str)
        return df
    except Exception as e:
        st.error(f"Ошибка чтения base.xlsx: {e}")
        return None

df = load_data()

query = st.text_input("Введите позиционный номер:", placeholder="Например: X-8303-J1").strip().upper()

if query and df is not None:
    # Поиск по первой колонке (A)
    first_col = df.columns[0]
    result = df[df[first_col].str.upper().str.contains(query, na=False)]

    if not result.empty:
        st.success(f"Найдено записей: {len(result)}")
        for i in range(len(result)):
            row = result.iloc[i]
            # Создаем карточку с четкими названиями
            with st.expander(f"📍 Позиция: {row[first_col]}", expanded=True):
                # Сопоставляем буквы колонок с вашего скриншота с названиями
                # row.get('буква') вытащит данные именно из этой колонки
                st.write(f"**⚡ Фидер (B):** {row.get('B', '-')}")
                st.info(f"**🏗️ РУ (C):** {row.get('C', '-')}")
                st.info(f"**📦 Ячейка (D):** {row.get('D', '-')}")
                st.warning(f"**📑 Тип схемы (E):** {row.get('E', '-')}")
            st.markdown("---")
    else:
        st.error("Позиция не найдена.")

if st.button("Найти"):
    st.cache_data.clear()
    st.rerun()