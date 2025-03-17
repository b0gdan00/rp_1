from fastapi import FastAPI
from arduino_connector import ArduinoSerial

app = FastAPI()
try:
    arduino = ArduinoSerial()
except Exception as e:
    print(e)
    arduino = None

@app.get("/status")
def get_status():
    """Получить текущее состояние LED"""
    return {"status": arduino.send_command("led ?")}


@app.post("/led/{state}")
def control_led(state: str):
    """Управление LED (включение/выключение)"""
    if state not in ["on", "off"]:
        return {"error": "Invalid state. Use 'on' or 'off'."}
    
    return {"response": arduino.send_command(f"led {state}")}



@app.on_event("shutdown")
def shutdown_event():
    """Закрываем соединение с Arduino при завершении работы сервера"""
    arduino.close()
