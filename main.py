from telebot import TeleBot
from arduino_connector import ArduinoSerial
import time







bot = TeleBot('7784381573:AAHKYDRFrFqK7g5qbYn_BiEBk9qGWS_g3nA')
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет Аня')
    arduino = ArduinoSerial()  # Automatically detect the port
    print(f"Connected to Arduino on {arduino.port}")
    arduino.start_listener()
    arduino.send_command("ping", 0)
    print(arduino.get_response())
    
    arduino.send_command("set_led", 1)
    time.sleep(3)
    arduino.send_command("set_led", 0)
    time.sleep(3)
    arduino.send_command("test_data", 0)
    print(arduino.get_response())
    bot.send_message(message.chat.id, str(arduino.get_response()))
    
    
bot.infinity_polling()