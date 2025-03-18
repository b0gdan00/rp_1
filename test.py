import streamlit as st
import random
import pandas as pd
import time

st.set_page_config(page_title="Мониторинг теплицы", layout="wide")

# Заголовок
st.title("🌱 Мониторинг теплицы")

# Функция для генерации случайных данных
def get_sensor_data():
    return {
        "Температура (°C)": round(random.uniform(18, 30), 2),
        "Влажность (%)": round(random.uniform(40, 80), 2),
        "CO₂ (ppm)": round(random.uniform(300, 800), 2),
        "Освещенность (люкс)": round(random.uniform(100, 1000), 2),
    }

# Инициализация состояния
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame([get_sensor_data() for _ in range(10)])

# Автоматическое обновление через 5 секунд
placeholder = st.empty()  # Контейнер для обновления
while True:
    new_data = get_sensor_data()
    st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_data])], ignore_index=True)

    with placeholder.container():  # Обновление без мерцания
        col1, col2, col3, col4 = st.columns(4)
        latest_data = st.session_state.history.iloc[-1]

        col1.metric("🌡 Температура", f"{latest_data['Температура (°C)']} °C")
        col2.metric("💧 Влажность", f"{latest_data['Влажность (%)']} %")
        col3.metric("🫁 CO₂", f"{latest_data['CO₂ (ppm)']} ppm")
        col4.metric("🔆 Освещенность", f"{latest_data['Освещенность (люкс)']} люкс")

        # Выбор графика
        selected_param = st.selectbox("📊 Выберите параметр для графика", st.session_state.history.columns)
        st.line_chart(st.session_state.history[selected_param])

    time.sleep(5)  # Обновление каждые 5 секунд
    st.rerun()  # Обновляем страницу
