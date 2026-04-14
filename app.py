import streamlit as st
import pandas as pd

# Настройка страницы
st.set_page_config(page_title=Поиск ячеек ПС, layout=centered)

st.title(🔎 Поиск оборудования ПС)

@st.cache_data
def load_data()
    try
        # Читаем 5 столбцов (A-E) Позиция, РУ, Ячейка, Фидер, Тип схемы
        df = pd.read_excel(base.xlsx, usecols=AE, names=['pos', 'ru', 'cell', 'feeder', 'schema'])
        # Приводим позиции к единому виду для поиска
        df['pos'] = df['pos'].astype(str).str.strip().str.upper()
        # Заменяем пустые значения на текст не указано
        df = df.fillna(—)
        return df
    except Exception as e
        st.error(fОшибка загрузки базы {e})
        return None

df = load_data()

# Поле ввода
query = st.text_input(Введите позиционный номер, placeholder=Например MP-3265).strip().upper()

if query
    if df is not None
        result = df[df['pos'] == query]
        
        if not result.empty
            st.success(✅ Позиция найдена!)
            row = result.iloc[0]
            
            # Вывод всех параметров
            st.info(f📍 РУ {row['ru']})
            st.info(f📦 Ячейка {row['cell']})
            st.info(f⚡ Фидер {row['feeder']})
            st.warning(f📑 Тип схемы {row['schema']}) # Тот самый новый столбец
        else
            st.error(❌ Позиция не найдена в базе.)
    else
        st.error(Файл base.xlsx не найден или поврежден.)

# Кнопка для сброса
if st.button(Очистить)
    st.rerun()