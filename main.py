from flask import Flask, Response, render_template, request, jsonify
import json
import time
import random

# Ініціалізація Flask-додатку
app = Flask(__name__)

# Стан регулювання параметрів (True - увімкнено, False - вимкнено)
control_states = {
    "temp": False, 
    "humidity": False, 
    "co2": False
}

# Діапазони значень для регулювання
slider_values = {
    "temp": {"min": 15, "max": 30},
    "humidity": {"min": 30, "max": 80},
    "co2": {"min": 300, "max": 600}
}


### === Функції логіки === ###

def generate_data():
    """Генерація випадкових значень параметрів кожні 5 секунд"""
    while True:
        temperature = random.randint(10, 35)
        humidity = random.randint(20, 90)
        co2 = random.randint(200, 700)

        # Автоматичне включення виконавчих механізмів, якщо параметр виходить за межі
        control_states["temp"] = not (slider_values["temp"]["min"] <= temperature <= slider_values["temp"]["max"])
        control_states["humidity"] = not (slider_values["humidity"]["min"] <= humidity <= slider_values["humidity"]["max"])
        control_states["co2"] = not (slider_values["co2"]["min"] <= co2 <= slider_values["co2"]["max"])

        # Формування даних для відправки клієнту
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "co2": co2,
            "greenery": random.randint(100, 500),
            "ten": control_states["temp"],    # ТЕН увімкнено, якщо температура виходить за межі
            "light": control_states["humidity"],  # Світло увімкнено, якщо вологість виходить за межі
            "vent": control_states["co2"]    # Вентиляція увімкнена, якщо CO₂ виходить за межі
        }

        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(5)


### === Маршрути Flask === ###

@app.route('/')
def index():
    """Головна сторінка"""
    return render_template('index.html')

@app.route('/stream')
def stream():
    """Потокова передача оновлених даних"""
    return Response(generate_data(), mimetype="text/event-stream")

@app.route('/toggle/<name>', methods=['POST'])
def toggle(name):
    """Ручне перемикання стану параметра (вкл/викл)"""
    if name in control_states:
        control_states[name] = not control_states[name]
    return jsonify({"status": "success", "state": control_states[name]})

@app.route('/set_slider', methods=['POST'])
def set_slider():
    """Оновлення меж діапазонів для контролю параметрів"""
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON data"}), 400

    slider_type = data.get("type")
    min_val = data.get("min")
    max_val = data.get("max")

    if slider_type not in slider_values:
        return jsonify({"status": "error", "message": "Invalid slider type"}), 400

    if min_val is None or max_val is None:
        return jsonify({"status": "error", "message": "Missing min or max values"}), 400

    slider_values[slider_type] = {"min": min_val, "max": max_val}
    return jsonify({"status": "success", "updated": slider_values[slider_type]})

@app.route('/get_sliders')
def get_sliders():
    """Отримання поточних меж діапазонів для контролю параметрів"""
    return jsonify(slider_values)

# Запуск серверу у режимі відлагодження
if __name__ == '__main__':
    app.run(debug=True)
