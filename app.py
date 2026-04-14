import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск ПС", layout="centered")
st.title("🔎 Поиск оборудования ПС")

@st.cache_data
def load_data():
    try:
        # Читаем Excel, удаляя лишние пробелы в названиях
        df = pd.read_excel("base.xlsx", engine='openpyxl')
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("—") # Заменяем пустоты на прочерк
    except Exception as e:
        st.error(f"Ошибка: {e}")
        return None

df = load_data()

query = st.text_input("Введите номер позиции:", placeholder="Например: X-8303-J1").strip().upper()

if query and df is not None:
    # Поиск по первой колонке
    first_col = df.columns[0]
    result = df[df[first_col].astype(str).str.upper().str.contains(query, na=False)]

    if not result.empty:
        st.success(f"Найдено записей: {len(result)}")
        for i in range(len(result)):
            row = result.iloc[i]
            with st.expander(f"📍 Позиция: {row[first_col]}", expanded=True):
                # Выводим все столбцы красиво
                for col in df.columns[1:]:
                    st.write(f"**{col}:** {row[col]}")
            st.markdown("---")
    else:
        st.error("Ничего не найдено.")

if st.button("🔄 Найти"):
    st.cache_data.clear()
    st.rerun()
