#  https://t.me/Utro_DobroeBot

from db import *
from keyboards import *

from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, \
                                    InputMediaVideo, InputMediaPhoto
import pytz
import datetime
from timezonefinder import TimezoneFinder

import os
from dotenv import *
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN')
MANAGER = os.getenv('MANAGER')
bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

def get_time (lat, lng):
    tf = TimezoneFinder(in_memory=True)
    timezone = tf.timezone_at(lng=lng, lat=lat)
    now = datetime.datetime.now(pytz.timezone(timezone))
    return timezone, now


@dp.message_handler(commands=['start', 'help', 'about'])
async def command_start(message: Message):
    if message.text == '/start': 
        await message.answer("Вас приветствует Бот для соревнования по утреннему подъему")
        await country_user(message)
    elif message.text == '/about':
        await message.answer("Этот бот был создан для\nМарафонов по утреннему подъему. \nГрафик времени: 5:00, 6:00, 7:00")
    elif message.text == '/help':
        await message.answer('У вас возникли проблемы с Ботом? \nПишите в личку @Cashboris')
async def country_user(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.full_name
    user = select_user(chat_id)
    nick_name = message.from_user.username
    if user:
        await message.answer('Авторизация прошла успешно')
        await show_main_menu(message) 
    else:
        first_register_user(chat_id, nick_name, full_name)
        await message.answer("Для регистрации нажмите на кнопку!",
                             reply_markup=generate_location_button())

@dp.message_handler(content_types=['location']) 
async def finish_register(message: Message):
    chat_id = message.chat.id
    message_id = message.message_id
    await bot.delete_message(chat_id, message_id)
    lat = message.location.latitude
    lng = message.location.longitude
    update_user_register(lng, lat, chat_id)
    await message.answer("Регистрация прошла успешно")
    await show_main_menu(message)

async def show_main_menu(message: Message):
    await message.answer('Выберите направление:',
                         reply_markup=main_menu())


@dp.message_handler(regexp=r'✅ Сделать отметку')
async def make_mark(message: Message):
    chat_id = message.chat.id 
    try:
        lng, lat =  get_lng_lat_user(chat_id)[0]
    except:
        await message.answer('Вы еще не отправили Часовой Пояс!', 
                             reply_markup=generate_location_button())
    hours = str(get_time(lng=float(lng), lat=float(lat))).split()[4].split(',')[0]
    minutes = str(get_time(lng=float(lng), lat=float(lat))).split()[5].split(',')[0]
    status_holiday = get_table_holiday()[0]
    if status_holiday == 'True':
        if hours in ['5','6','7'] and  int(minutes) > 45:
            await message.answer('Скиньте видеоролик в кружке.',
                                reply_markup=back_main_menu()) 
        else:
            await message.answer('Извените, еще не время.')
    else:
            await message.answer('Извените, марафон еще не начачался.')

@dp.message_handler(content_types=['video_note'])
async def confirmation_video(message: Message):
    chat_id = message.chat.id 
    message_id = message.message_id
    await bot.delete_message(chat_id, message_id)
    lng, lat =  get_lng_lat_user(chat_id)[0]
    try:
        hours = str(get_time(lng=float(lng), lat=float(lat))).split()[4].split(',')[0]
        minutes = str(get_time(lng=float(lng), lat=float(lat))).split()[5].split(',')[0]
        status_holiday = get_table_holiday()[0]
    except:
        await message.answer('Вы еще не отправиили часовой пояс!', 
                             reply_markup=generate_location_button())
    if status_holiday == 'True':
        if hours in ['5','6','7'] and int(minutes) > 45:
            score = int(get_score(chat_id))
            score += 1
            commit_score(score, chat_id)
            await bot.send_media_group(MANAGER, 
                    [InputMediaVideo(message.video_note.file_id)])
            await bot.send_message(MANAGER, f'''
Имя: <b>{message.from_user.full_name}</b>
Ник: <b>{message.from_user.username}</b>
            ''')
            await message.answer('Вам был добавлен балл')
            await show_main_menu(message)
        else: pass
    else: pass

@dp.message_handler(regexp=r'⬅ Назад')
async def back(message: Message):
    await show_main_menu(message)

@dp.message_handler(regexp=r'📕 Профиль')   
async def my_info(message: Message):
    chat_id = message.chat.id 
    lng, lat =  get_lng_lat_user(chat_id)[0]
    UTC = str(get_time(lng=float(lng), lat=float(lat))).split()[-2].split('+')[2].split(':')[0]     
    score = get_score(chat_id)
    await message.answer(f'''
Ваше Имя: <b>{message.from_user.full_name}</b>
Баллы: <b>{score}</b>
Время: UTC +{UTC}
        ''')


@dp.message_handler(regexp=r'📊 Рейтинг')   
async def rating(message: Message):
    chat_id = message.chat.id 
    i = 0
    status_holiday = get_table_holiday()[0]
    if status_holiday == 'True':
        await message.answer('Топ 10')
        sum_id = get_count_id()[0]
        for user in range(sum_id):
            i += 1
            if i != 11:
                user_name = get_rating()[user][1]
                nick_name = get_rating()[user][2]
                score = get_rating()[user][-2]
                await message.answer(f'''
{i}. 
Имя: <b>{user_name}</b>
Ник: <b>@{nick_name}</b>
Баллы: <b>{score}</b>
                ''')
            else: break
    else: 
        user_win = get_win_user()
        await message.answer(f'''
🎉Победитель прошлого марафона🎉z
Имя: <b>{user_win[0][1]}</b>
Ник: <b>{user_win[0][3]}</b>
Баллы: <b>{user_win[0][2]}</b>
        ''')

@dp.message_handler(regexp=r'⚙ Настройки')   
async def my_info(message: Message):
    await message.answer('Выберете настройки:',
                         reply_markup=setings())

@dp.callback_query_handler(lambda call: 'change_timezone' in call.data)
async def change_timezone(call: CallbackQuery):
    chat_id = call.message.chat.id 
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id)      
    await bot.send_message(chat_id, 'Нажмите на кнопку!',
                           reply_markup=generate_location_button())
    
@dp.callback_query_handler(lambda call: 'back' in call.data)
async def back_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id)    
    await bot.send_message(chat_id=chat_id, text="",
                                 reply_markup=main_menu())

@dp.callback_query_handler(lambda call: 'admin_setings' in call.data)
async def admin_setings(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id) 
    if chat_id == int(ADMIN):
        await bot.send_message(chat_id, text='Приветствую вас Админ')
        await bot.send_message(chat_id, text='Выберите кнопки:',
                                 reply_markup=admin_setings_function())
    else:
        await bot.send_message(chat_id, text='Упсс, вы не Админ')

@dp.callback_query_handler(lambda call: 'start_holiday' in call.data)    
async def start_holiday(call: CallbackQuery):
    chat_id = call.message.chat.id  
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id) 
    update_ball()
    await bot.send_message(chat_id, 'Марафон Начат!',
                           reply_markup=back_main_menu())
    update_table_holiday(status_holiday='True')

@dp.callback_query_handler(lambda call: 'finish_holiday' in call.data)    
async def finish_holiday(call: CallbackQuery):
    chat_id = call.message.chat.id  
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id) 
    user, id = winer_user()
    chat_user = select_user(id)
    insert_win_user(user, chat_user[0][2], chat_user[0][-1])
    await bot.send_message(chat_id, f'''
Победитель: {chat_user[0][1]}
Ник: @{chat_user[0][2]}
Набрано Баллов: {chat_user[0][-1]} 
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
    ''')
    update_ball()
    await bot.send_message(chat_id, 'Марафон Закончен!',
                           reply_markup=back_main_menu())
    update_table_holiday(status_holiday='False')
executor.start_polling(dp)

 
