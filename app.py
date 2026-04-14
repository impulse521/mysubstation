import streamlit as st
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="Поиск ячеек ПС", layout="centered")

st.title("Поиск оборудования ПС")

@st.cache_data
def load_data():
    try:
        # Читаем 5 столбцов (A-E)
        df = pd.read_excel("base.xlsx", usecols="A:E", names=['pos', 'ru', 'cell', 'feeder', 'schema'])
        df['pos'] = df['pos'].astype(str).str.strip().str.upper()
        df = df.fillna("-")
        return df
    except Exception as e:
        st.error(f"Ошибка загрузки base.xlsx: {e}")
        return None

df = load_data()

query = st.text_input("Введите позиционный номер:", placeholder="Например: MP-3265").strip().upper()

if query:
    if df is not None:
        result = df[df['pos'] == query]
        
        if not result.empty:
            st.success("Позиция найдена!")
            row = result.iloc[0]
            
            st.info(f"**РУ:** {row['ru']}")
            st.info(f"**Ячейка:** {row['cell']}")
            st.info(f"**Фидер:** {row['feeder']}")
            st.warning(f"**Тип схемы:** {row['schema']}")
        else:
            st.error("Позиция не найдена в базе.")

if st.button("Очистить"):
    st.rerun()