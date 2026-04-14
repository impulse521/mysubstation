import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск оборудования", layout="centered")
st.title("🔎 Поиск по базе ПС")

@st.cache_data
def load_data():
    try:
        # Загружаем Excel. engine='openpyxl' важен для файлов .xlsx
        df = pd.read_excel("base.xlsx", engine='openpyxl')
        # Превращаем все данные в текст, чтобы поиск работал корректно
        df = df.astype(str)
        return df
    except Exception as e:
        st.error(f"Ошибка чтения base.xlsx: {e}")
        return None

df = load_data()

query = st.text_input("Введите номер (позицию):").strip().upper()

if query and df is not None:
    # Ищем во всем файле строки, где в ПЕРВОЙ колонке есть ваш текст
    first_column_name = df.columns[0]
    result = df[df[first_column_name].str.upper().str.contains(query, na=False)]

    if not result.empty:
        st.success(f"Найдено записей: {len(result)}")
        for i in range(len(result)):
            row = result.iloc[i]
            # Создаем красивую карточку для каждой находки
            with st.expander(f"📍 Позиция: {row[first_column_name]}", expanded=True):
                # Выводим все остальные колонки из Excel
                for col_name in df.columns[1:]:
                    st.write(f"**{col_name}:** {row[col_name]}")
            st.markdown("---")
    else:
        st.error("Ничего не найдено. Проверьте правильность ввода.")

if st.button("Найти"):
    st.cache_data.clear()
    st.rerun()
