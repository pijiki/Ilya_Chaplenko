# https://t.me/dost_avka_bot

from database import *
from keyboards import *

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMedia, LabeledPrice
                                                        



import os
from dotenv import *
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN')
PAYMENT = os.getenv('PAYMENT')


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
    print(phone)
    update_user_to_finish_register(phone, chat_id)
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
@dp.message_handler(lambda message: message.text ==  '✅ Сделать заказ')
async def make_order(message: Message):
    chat_id = message.chat.id
    cart_id = get_user_cart_id(chat_id)
    await bot.send_message(chat_id, "Погнали", reply_markup=back_to_main_menu())
    await message.answer('Выберите категорию: ', reply_markup=generate_category_menu(cart_id))

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
    cart_id = get_user_cart_id(chat_id)
    await bot.edit_message_text(text="Выберите категорию: ", chat_id=chat_id, 
                                message_id=message_id, reply_markup=generate_category_menu(cart_id))
    
@dp.message_handler(regexp=r'Главное меню')
async def main_menu(message: Message):
    message.message_id -= 1
    chat_id = message.chat.id
    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    await show_main_menu(message)

@dp.callback_query_handler(lambda call: 'product_' in call.data)
async def show_detail_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    product_id = int(call.data.split('_')[-1])
    product = get_product_detail(product_id)
    cart_id = get_user_cart_id(chat_id)
    update_to_cart(cost=product[3], quantity=1, cart_id=cart_id)
    cost, _ = get_cost_product(cart_id)
    await bot.send_message(chat_id, 'Выберите модификатор:',  reply_markup=back_to_menu())
    await bot.delete_message(chat_id, message_id)
    with open(product[-1], mode='rb') as img:
        await bot.send_photo(chat_id=chat_id, photo=img,
                             caption=f'{product[2]}\nИнгредиенты: {product[-2]}\nЦена: {cost} сум',
                             reply_markup=generate_product_price(1))


@dp.callback_query_handler(lambda call: 'action' in call.data)
async def quantity_plus_minus(call: CallbackQuery):
    action = call.data.split()[-1]
    message_id = call.message.message_id
    chat_id = call.from_user.id
    try:
        cart_id = get_user_cart_id(chat_id)
        cost, quantity = get_cost_product(cart_id)
    except:
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, "К сожалению вы еще не отправили нам контакт",
                               reply_markup=generate_phone_button())

    product_name = call.message['caption'].split('\n')[0]
    product_info = get_detail_product(product_name)
    if action == '+':
        update_to_cart(product_info[3], quantity + 1, cart_id)
    else:
        update_to_cart(product_info[3], quantity - 1, cart_id)

    cost, quantity = get_cost_product(cart_id)
    try:
        with open(product_info[-1], mode='rb') as img:
            await bot.edit_message_media(media=InputMedia(media=img,
                                                          caption=f'{product_info[2]}\nИнгредиенты: {product_info[4]}\nЦена: {cost} сум',
                                                          type='photo'),
                                         chat_id=chat_id,
                                         message_id=message_id,
                                         reply_markup=generate_product_price(quantity))
    except:
        pass

@dp.callback_query_handler(regexp = r'put_into_cart')
async def put_into_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    cart_id = get_user_cart_id(chat_id)
    cost, quantity = get_cost_product(cart_id)
    product_name = call.message['caption'].split('\n')[0]

    if insert_or_update_cart_product(cart_id, product_name, quantity, cost):
        await bot.answer_callback_query(call.id, "Продукт добавлен")
    else:
        await bot.answer_callback_query(call.id, "Количество изменено")    


@dp.callback_query_handler(regexp=r'cart')
async def show_cart(call: CallbackQuery):
    message_id = call.message.message_id
    chat_id = call.from_user.id
    cart_id = get_user_cart_id(chat_id)
    await bot.delete_message(chat_id, message_id)
    try:     update_total_product_total_price(cart_id)
    except: await call.answer('Ваша корзина пуста!')
    total_products, total_price = get_total_product_price(cart_id)
    cart_products = get_cart_products(cart_id)
    text, i = 'Ваша корзинка: \n\n', 0
    list_name = []
    for name, quantity, price in cart_products:
        i += 1
        list_name.append(name)
        await bot.send_message(chat_id, f'{i}.\n{name}\nКолличество: {quantity}\nЦена: {price}\n\n')
    if total_products and total_price:
        text += f'Общее количество продуктов: {total_products}\nОбщая стоимость корзины: {total_price}'
        await bot.send_message(chat_id, text, reply_markup=buy_food(list_name))
    else: await bot.send_message(chat_id, "Ваша корзинa пуста 🤥")



@dp.message_handler(regexp=r'⬅ Назад')
async def return_menu(message: Message):
    message.message_id -= 1
    await bot.delete_message(message.chat.id, message.message_id)
    await make_order(message)

@dp.message_handler(regexp=r'📒 История')
async def show_history(message: Message):
    chat_id = message.from_user.id
    history = read_history(chat_id)
    cart_id = get_user_cart_id(chat_id)
    await message.answer('Последние заказы',
                         reply_markup=back_to_main_menu())
    for name, quantity, price in history[:3]:
        await message.answer(f'''
Название: <b>{name}</b>
Колличество: <b>{quantity}</b>
Цена: <b>{price}</b>
        ''')
    
@dp.message_handler(regexp=r'🛒 Корзинка')
async def show_basket(message: Message):
    message_id = message.message_id
    chat_id = message.from_user.id
    cart_id = get_user_cart_id(chat_id)
    await bot.delete_message(chat_id, message_id)
    try:     update_total_product_total_price(cart_id)
    except: await message.answer('Ваша корзина пуста!')
    total_products, total_price = get_total_product_price(cart_id)
    cart_products = get_cart_products(cart_id)
    i, list_name = i, []
    await bot.send_message(chat_id, 'Ваша корзинка:')
    for name, quantity, price in cart_products:
        i += 1
        list_name.append(name)
        text += f'{i}.\nНазвание <b>{name}</b>\nКолличество: {quantity}\nЦена: {price}\n\n'
    if total_products and total_price:
        text += f'Общее количество продуктов: {total_products}\nОбщая стоимость корзины: {total_price}'
        await bot.send_message(chat_id, text=text, reply_markup=buy_food())
    else: await bot.send_message(chat_id, "Ваша корзинa пуста 🤥")

@dp.callback_query_handler(lambda call: 'order_action' in call.data)
async def order_plus_minus(call: CallbackQuery):
    action = call.data.split()[-1]
    message_id = call.message.message_id
    chat_id = call.from_user.id
    try:
        cart_id = get_user_cart_id(chat_id)
        cost, quantity = get_cost_product(cart_id)
    except:
        await bot.delete_message(chat_id, message_id)
        await bot.send_message(chat_id, "К сожалению вы еще не отправили нам контакт",
                               reply_markup=generate_phone_button())

    product_name = call.message['caption'].split('\n')[0]
    product_info = get_detail_product(product_name)
    if action == '+':
        update_to_cart(product_info[3], quantity + 1, cart_id)
    else:
        update_to_cart(product_info[3], quantity - 1, cart_id)
    cost, quantity = get_cost_product(cart_id)
    await bot.edit_message_text(chat_id, f'')
    cost, quantity = get_cost_product(cart_id)
    
@dp.callback_query_handler(regexp=r'buy')
async def purchace_product(call: CallbackQuery):
    message_id = call.message.message_id
    chat_id = call.from_user.id
    cart_id = get_user_cart_id(chat_id)
    cart_products = get_cart_products(cart_id)
    for name, quantity, price in cart_products:
        insert_history(chat_id, name, quantity, price)
    delete_all()
    await bot.delete_message(chat_id, message_id)    
    total_products, total_price = get_total_product_price(cart_id)
    cart_products = get_cart_products(cart_id)
    text, i = 'Ваша корзинка: \n\n', 0
    for name, quantity, price in cart_products:
        i += 1
        text += f'{i}.\n{name}\nКолличество: {quantity}\nЦена: {price}\n\n'
    if total_products and total_price:
        text += f'Общее количество продуктов: {total_products}\nОбщая стоимость корзины: {total_price}'

    await bot.send_invoice(
        chat_id=chat_id,
        title=f"Заказ №{cart_id}",
        description=text,
        payload="bot-defined invoice payload",
        provider_token=PAYMENT,
        currency='UZS',
        prices= [
            LabeledPrice(label="Общая стоимость", amount=int(total_price ** 100)),
            LabeledPrice(label="Доставка", amount=10000)
         ]

    )
    await bot.send_message(chat_id, text='Оплачено')
    
@dp.callback_query_handler(regexp=r'delete')
async def delete_product(call: CallbackQuery):
    delete_id = call.data.split('_')[-1]
    delete_product_id(id=delete_id)
    await bot.answer_callback_query(call.id, 'Продукт удален')
    await show_cart(call)


@dp.message_handler(regexp=r'⚙ Настройки')
async def show_admin(message: Message):
    chat_id = message.chat.id
    if chat_id == int(ADMIN):
        await message.answer('Доступ разрешен!',reply_markup=setings_user())
    else: 
        await message.answer('Выберите настройки',reply_markup=setings_user())


executor.start_polling(dp)

