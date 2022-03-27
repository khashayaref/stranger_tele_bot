import os
import telebot


bot = telebot.TeleBot(os.environ.get('NASHENAS_BOT_TOKEN'),parse_mode='HTML')