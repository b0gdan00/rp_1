from telebot import TeleBot



bot = TeleBot('7784381573:AAHKYDRFrFqK7g5qbYn_BiEBk9qGWS_g3nA')
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'TEst')
    
    
    
bot.infinity_polling()