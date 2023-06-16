from database import *
from keyboards import *


from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMedia, LabeledPrice
                                                        




bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

