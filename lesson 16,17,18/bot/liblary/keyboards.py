from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup

from database import *

def generate_phone_button():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text="Отправить свой контакт", request_contact=True)]
        ], resize_keyboard=True
    )

def generate_main_menu():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text='✅ Сделать заказ')],
            [KeyboardButton(text='📒 История'), KeyboardButton(text='🛒 Корзинка'), KeyboardButton(text='⚙ Настройки')]
        ], resize_keyboard=True
    )

def back_to_main_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='Главное меню')]
    ], resize_keyboard=True)

def generate_category_menu(cart_id):
    summary_price = get_sum_price_from_cart(cart_id)[0]
    categories = get_all_categories()

    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
    InlineKeyboardButton(text=f'Ваша корзинка  ({summary_price if summary_price else 0} сумм)', callback_data='cart')
    )
    buttons = []
    for category in categories:
        bnt = InlineKeyboardButton(text=category[1], callback_data=f"category_{category[0]}")
        buttons.append(bnt)
    markup.add(*buttons)
    return markup


def generate_products_by_category(category_id):
    markup = InlineKeyboardMarkup(row_width=2)
    products = get_products_by_category(category_id)
    buttons = []
    for product in products:
        btn = InlineKeyboardButton(text=product[1], callback_data=f"product_{product[0]}")
        buttons.append(btn)
    markup.add(*buttons)
    markup.row(
    InlineKeyboardButton(text='⬅ Назад', callback_data='Назад')
    )
    return markup

def admin_setings():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(text='➕ Добавить категорию TODO')],
            [KeyboardButton(text='➖ Удалить категорию TODO')],
            [KeyboardButton(text='Главное меню')]
        ], resize_keyboard=True
    )

def setings_user():
    markup = InlineKeyboardMarkup(row_width=3)
    markup.row(
        InlineKeyboardButton(text='⌨ Сменить язык', callback_data='language'),
        InlineKeyboardButton(text='📞 Сменить номер', callback_data='number')
    )
    return markup

def generate_product_price(quantity):
    markup = InlineKeyboardMarkup(row_width=3)
    number = quantity
    buttons = [
        InlineKeyboardButton(text='➖', callback_data='action -'),
        InlineKeyboardButton(text=f'{number}', callback_data=f'{number}'),
        InlineKeyboardButton(text='➕', callback_data='action +'),
        InlineKeyboardButton(text='Положить в корзину 😋', callback_data='put_into_cart')
    ]
    markup.add(*buttons)
    return markup


def back_to_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='⬅ Назад')]
    ], resize_keyboard=True)



def buy_food():
    markup = InlineKeyboardMarkup(row_width=3)
    button = [
        InlineKeyboardButton(text='Заказать', callback_data='buy')]
    markup.add(*button)
    return markup

def button (list_name):
    markup = InlineKeyboardMarkup(row_width=3)
    for name in list_name:
        buttons = [
            InlineKeyboardButton(text='➖', callback_data='order_action -'),
            InlineKeyboardButton(text='❌', callback_data=f'delete_{name}'),
            InlineKeyboardButton(text='➕', callback_data='order_action +'),
            ]
        markup.add(*buttons)
    return markup