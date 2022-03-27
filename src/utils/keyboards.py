from telebot import types
import emoji


def create_keyboard(*keys , resize_keyboard: bool=True, row_width: int=2):
    """create a keyboard with different keys

    :param keys: _description_
    :type keys: _type_
    :param resize_keyboard: resize the buttons, defaults to True
    :param row_width: the width of screen, defaults to 2
    """
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=resize_keyboard,
        row_width=row_width
    )
    keys = map(emoji.emojize, keys)
    buttons = list(map(types.KeyboardButton, keys))
    markup.add(*buttons)
    return markup
