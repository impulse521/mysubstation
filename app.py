import streamlit as st
import pandas as pd

st.set_page_config(page_title="Поиск оборудования", layout="centered")
st.title("🔎 Поиск по базе ПС")

@st.cache_data
def load_data():
    try:
        # Считываем весь лист без ограничений по колонкам
        df = pd.read_excel("base.xlsx")
        # Убираем лишние пробелы в названиях колонок и данных
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Ошибка чтения Excel: {e}")
        return None

df = load_data()

query = st.text_input("Введите номер (позицию):").strip().upper()

if query and df is not None:
    # Ищем во всем файле строки, где есть ваш текст
    # Мы ищем по первой колонке (обычно это Позиция)
    first_col = df.columns[0]
    mask = df[first_col].astype(str).str.upper().str.contains(query, na=False)
    result = df[mask]

    if not result.empty:
        for i in range(len(result)):
            row = result.iloc[i]
            with st.container():
                st.write(f"### 📍 Позиция: {row[0]}")
                # Выводим все данные, которые есть в этой строке
                cols = st.columns(2)
                for idx, col_name in enumerate(df.columns[1:]):
                    with cols[idx % 2]:
                        st.metric(label=col_name, value=str(row[col_name]))
                st.markdown("---")
    else:
        st.error("Ничего не найдено")

if st.button("Обновить базу"):
    st.cache_data.clear()
    st.rerun()