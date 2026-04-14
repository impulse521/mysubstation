import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск ячеек ПС", layout="centered")

st.title("🔎 Поиск оборудования ПС")

@st.cache_data
def load_data():
    try:
        # Читаем 5 столбцов согласно вашему фото:
        # A=pos, B=feeder, C=ru, D=cell, E=schema
        df = pd.read_excel("base.xlsx", usecols="A:E", names=['pos', 'feeder', 'ru', 'cell', 'schema'])
        df['pos'] = df['pos'].astype(str).str.strip().str.upper()
        df = df.fillna("-")
        return df
    except Exception as e:
        st.error(f"Ошибка загрузки base.xlsx: {e}")
        return None

df = load_data()

query = st.text_input("Введите позиционный номер:", placeholder="Например: A80-ASU-LSP-006").strip().upper()

if query:
    if df is not None:
        # Ищем все совпадения (на случай, если номеров несколько)
        result = df[df['pos'].str.contains(query, na=False, regex=False)]
        
        if not result.empty:
            st.success(f"Найдено совпадений: {len(result)}")
            for i in range(len(result)):
                row = result.iloc[i]
                with st.expander(f"📍 Позиция: {row['pos']}", expanded=True):
                    st.info(f"**РУ:** {row['ru']}")
                    st.info(f"**Ячейка:** {row['cell']}")
                    st.info(f"**Фидер:** {row['feeder']}")
                    st.warning(f"**Тип схемы:** {row['schema']}")
        else:
            st.error("Позиция не найдена.")

if st.button("Очистить"):
    st.rerun()