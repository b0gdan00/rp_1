from telebot import TeleBot
from arduino_connector import ArduinoSerial
import time


arduino = ArduinoSerial()

bot = TeleBot('7784381573:AAHKYDRFrFqK7g5qbYn_BiEBk9qGWS_g3nA')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, arduino.send_command('led ?'))
    
    
@bot.message_handler(commands=['led'])
def start(message):
    print(arduino.send_command('led ?'))
    if arduino.send_command('led ?') == "ON":
        bot.send_message(message.chat.id, arduino.send_command('led off'))
    else:
        bot.send_message(message.chat.id, arduino.send_command('led on'))
    
    
try:    
    bot.infinity_polling()
except:
    print('Error')
finally:
    arduino.close()