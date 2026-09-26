import telebot, dotenv

BOT_TOKEN = dotenv.get_key(".env", "TELEGRAM_BOT_TOKEN")

tb = telebot.TeleBot(token=BOT_TOKEN)

def send_message(chat_id, text):
    tb.send_message(chat_id=chat_id, text=text)