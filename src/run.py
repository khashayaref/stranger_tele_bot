
import os

import emoji
import telebot
from telebot import types

from src.bot import bot
from src.db import db
from src.filters import IsAdmin
from src.utils.constants import keyboards, keys, states
from src.utils.io import write_json


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
        @self.bot.message_handler(commands=['start'])
        def start(message):
            """
            /start command to start a connection
            """
            self.send_message(message.chat.id, 
            f'Hi {message.chat.first_name}, welcome to our group',
            reply_markup=keyboards.main)
            
            db.users.update_one({'chat.id': message.chat.id},
            {'$set':message.json}, upsert=True)

            self.update_state(message.chat.id,states.main)

        @self.bot.message_handler(regexp=emoji.emojize(keys.random_connect))
        def random_connect(message):
            """randomly connect to another user
            """
            self.send_message(message.chat.id,
                'Connecting you to a random stranger',
                reply_markup=keyboards.exit
            )

            self.update_state(message.chat.id, states.random_connection)

            other_user = db.users.find_one(
                {'$and':[
                    {'state':states.random_connection},
                    {'chat.id':{'$ne': message.chat.id}}
                    ]}
            )
            if not other_user:
                return
            #update other_user state
            self.update_state(other_user['chat']['id'],states.connected)
            self.send_message(other_user['chat']['id'], f'You are connected to {message["chat"]["id"]}')
            #update current user state
            self.update_state(message.chat.id,states.connected)
            self.send_message(message.chat.id, f'You are connected to {other_user["chat"]["id"]}')

            #store connected users
            db.users.update_one({'chat.id':message.chat.id},
            {'$set':{'connected_to':other_user['chat']['id']}})

            db.users.update_one({'chat.id':other_user['chat']['id']},
            {'$set':{'connected_to':message.chat.id}})


        @self.bot.message_handler(regexp=emoji.emojize(keys.exit))
        def exit(message):
            """exit from chat or connecting state
            """
            self.send_message(message.chat.id,
            keys.exit,
            reply_markup=keyboards.main)
            self.update_state(message.chat.id, states.main)

            # get other user
            connected_to = db.users.find_one({'chat.id': message.chat.id})['connected_to']
            if not connected_to:
                return
            #update other user state and terminate the connection
            self.update_state(connected_to, states.main)
            self.send_message(connected_to,keys.exit, reply_markup=keyboards.main)

            # remove connected users
            db.users.update_one({'chat.id':connected_to}, {'$set':{'connected_to': None}})
            db.users.update_one({'chat.id': message.chat.id}, {'$set':{'connected_to': None}}) 
            

        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            self.send_message(message.chat.id, 'You are admin of this group!')

        @self.bot.message_handler(func=lambda _: True)
        def echo_all(message):
            """echo messages to two stranger users
            """
            # print(emoji.demojize(message.text))
            # write_json(message.json, 'message.json')
            user = db.users.find_one({'chat.id': message.chat.id})
            if (not user) or (user['state'] != states.connected) or (user['connected_to'] == None):
                return
            self.send_message(user['connected_to'], message.text)
    
    def run(self):
        self.bot.infinity_polling(timeout=40)

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """send message to telegram bot
        """
        if emojize:
            text = emoji.emojize(text,use_aliases=True)
        self.bot.send_message(chat_id, text, reply_markup=reply_markup)
    
    @staticmethod
    def update_state(chat_id, state):
        """
        Update the state of the user
        """
        db.users.update_one(
            {'chat.id': chat_id},
            {'$set':{'state': state}},
            upsert=True
        )
        
        
                 
if __name__ == '__main__':
    bot = Bot(telebot=bot)
    bot.run()
