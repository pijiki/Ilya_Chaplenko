import os
from dotenv import *
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
ADMIN = os.getenv('ADMIN')
CLICK = os.getenv('CLICK')

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')