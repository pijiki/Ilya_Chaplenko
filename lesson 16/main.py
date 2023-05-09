# https://t.me/dost_avka_bot

from database import *
from keyboards import *


from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove


import os
from dotenv import *
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN')


bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    await message.answer(f"Здравствуйте <b>{message.from_user.full_name}</b>")
    await register_user(message)

async def register_user(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    user = first_select_user(chat_id)

    if user:
        await message.answer('Авторизация прошла успешно')
        await show_main_menu(message)
    else:
        first_register_user(chat_id, full_name)
        await message.answer("Для регистрации нажмите на кнопку",
                             reply_markup=generate_phone_button())


@dp.message_handler(content_types=['contact'])
async def finish_register(message: Message):
    chat_id = message.chat.id
    phone = message.contact.phone_number
    update_user_to_finish_register(chat_id, phone)
    await create_cart_for_user(message)
    await message.answer("Регистрация прошла успешно")
    await show_main_menu(message)


async def create_cart_for_user(message):
    chat_id = message.chat.id
    try:
        insert_to_cart(chat_id)
    except:
        pass


async def show_main_menu(message: Message):
    await message.answer("Выберите направление", reply_markup=generate_main_menu())
@dp.message_handler(lambda message: message.text == 'Главное меню')
async def main_menu(message: Message):
    await show_main_menu(message)

@dp.message_handler(lambda message: message.text ==  '✅ Сделать заказ')
async def make_order(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Погнали", reply_markup=back_to_main_menu())
    await message.answer('Выберите категорию: ', reply_markup=generate_category_menu())

@dp.callback_query_handler(lambda call: 'category_' in call.data)
async def show_products(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, category_id = call.data.split('_')
    category_id = int(category_id)
    await bot.edit_message_text("Выберите продукт: ", chat_id, message_id,
                                reply_markup=generate_products_by_category(category_id))
@dp.callback_query_handler(lambda call: 'Назад' in call.data)
async def back_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text("Выберите категорию: ", chat_id, message_id,
                                reply_markup=generate_category_menu())
    
@dp.message_handler(lambda message: message.text == '📒 История')
async def show_history(message: Message):
    await message.answer('TODO HISTORY')

@dp.message_handler(lambda message: message.text == '🛒 Корзинка')
async def show_basket(message: Message):
    await message.answer('TODO BASKET', )

@dp.message_handler(lambda message: message.text == '⚙ Настройки')
async def show_admin(message: Message):
    chat_id = message.chat.id
    if chat_id == int(ADMIN):
        await message.answer('Доступ разрешен!',
                              reply_markup=admin_setings())
    else: 
        await message.answer('Доступ запрещен!')
    

executor.start_polling(dp)

