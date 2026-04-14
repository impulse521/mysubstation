import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск оборудования", layout="centered")
st.title("🔎 Поиск оборудования ПС")

@st.cache_data
def load_data():
    try:
        # Читаем Excel, заголовки будут буквами, если они так в файле
        df = pd.read_excel("base.xlsx", engine='openpyxl').fillna("—")
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Ошибка: {e}")
        return None

df = load_data()

query = st.text_input("Введите номер позиции:", placeholder="Например: X-8303-P1-S").strip().upper()

if query and df is not None:
    first_col = df.columns[0]
    result = df[df[first_col].astype(str).str.upper().str.contains(query, na=False)]

    if not result.empty:
        st.success(f"Найдено записей: {len(result)}")
        for i in range(len(result)):
            row = result.iloc[i]
            with st.expander(f"📍 Позиция: {row[first_col]}", expanded=True):
                # Назначаем названия буквам столбцов
                st.write(f"**Наименование:** {row.get('B', row.iloc[1] if len(row)>1 else '—')}")
                st.write(f"**РУ:** {row.get('C', row.iloc[2] if len(row)>2 else '—')}")
                st.write(f"**Ячейка:** {row.get('D', row.iloc[3] if len(row)>3 else '—')}")
                st.write(f"**Схема:** {row.get('E', row.iloc[4] if len(row)>4 else '—')}")
            st.markdown("---")
    else:
        st.error("Ничего не найдено.")

if st.button("🔄 Найти"):
    st.cache_data.clear()
    st.rerun()
