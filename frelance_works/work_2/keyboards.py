from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup



def generate_location_button():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="Отправить часовую зону", request_location=True)]
        ], resize_keyboard=True
    )

def main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="✅ Сделать отметку")],
            [KeyboardButton(text="📕 Профиль"),KeyboardButton(text="📊 Рейтинг"), KeyboardButton(text="⚙ Настройки")] 
        ], resize_keyboard=True 
    )

def back_main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="⬅ Назад")]
        ], resize_keyboard=True
    )

def setings():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text='Сменить Часовую Зону', callback_data='change_timezone'),
        InlineKeyboardButton(text='Админ Настройки', callback_data='admin_setings'),
        InlineKeyboardButton(text='⬅ Назад', callback_data='back')
    ]
    markup.add(*buttons)
    return markup

def admin_setings_function():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text='🥳 Обьявить Марафон', callback_data='start_holiday'),
        InlineKeyboardButton(text='🥂 Закончить Марафон', callback_data='finish_holiday')
    ]
    markup.add(*buttons)
    return markup

