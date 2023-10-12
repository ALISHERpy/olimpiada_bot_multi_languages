from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from tgbot import static_text 
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_TEST, CONFIRM_BROADCAST, DECLINE_BROADCAST



def main_keys() -> ReplyKeyboardMarkup:
    buttons = [
        [ KeyboardButton(text=static_text.About_comp), KeyboardButton(text=static_text.Register_users),],
        [ KeyboardButton(text=static_text.Litsey), ],
        [ KeyboardButton(text=static_text.test_ber), ],
    
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)


def inline_keys_start() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(static_text.TEST_boshlash, callback_data='get_start'),
        InlineKeyboardButton(static_text.TEST_bekor, callback_data='get_back')
    ]]

    return InlineKeyboardMarkup(buttons)

def Answers_confirm() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(static_text.Confirmed, callback_data='confirmed'),
        InlineKeyboardButton(static_text.NOT_Confirmed, callback_data='not_confirmed')
    ]]

    return InlineKeyboardMarkup(buttons)


def inline_language_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
        InlineKeyboardButton(static_text.uzbekcha, callback_data='uz'),
        InlineKeyboardButton(static_text.ruscha, callback_data='ru'),
    ],
     [
        InlineKeyboardButton(static_text.TEST_bekor, callback_data='get_back')
    ],
    ]

    return InlineKeyboardMarkup(buttons)


