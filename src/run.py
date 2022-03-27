
import os

import emoji
import telebot
from telebot import apihelper, types

from src.bot import bot
from src.filters import IsAdmin
from src.utils.constants import keyboards
from src.utils.io import write_json
import emoji


# bot = telebot.TeleBot(os.environ.get('NASHENAS_BOT_TOKEN'))
class Bot:
    """Telegram bot for connection randomly two strangers to talk
    """
    def __init__(self, telebot):
        # self.bot = telebot.TeleBot(os.environ.get('NASHENAS_BOT_TOKEN'))
        # self.echo_all = self.bot.message_handler(func=lambda message: True)(self.echo_all)
        self.bot = telebot
        # register custom filter
        self.bot.add_custom_filter(IsAdmin())
        # register handlers
        self.handlers()
        # run bot
        # self.bot.infinity_polling()

    def handlers(self):
        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(message.chat.id, 'You are admin of this group!')

        @self.bot.message_handler(func=lambda _: True)
        def echo_all(message):
            # print(emoji.demojize(message.text))
            # write_json(message.json, 'message.json')
            self.send_message(message.chat.id, message.text,reply_markup=keyboards.main)
    
    def run(self):
        self.bot.infinity_polling(timeout=40)

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """send message to telegram bot
        """
        if emojize:
            text = emoji.emojize(text,use_aliases=True)
        self.bot.send_message(chat_id, text, reply_markup=reply_markup)
        

        

	 			

if __name__ == '__main__':
	bot = Bot(telebot=bot)
	bot.run()
