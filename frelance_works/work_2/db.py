import sqlite3


def create_user_table():
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        nick_name TEXT,
        telegram_id BIGINT NOT NULL UNIQUE,
        lng TEXT,
        lat TEXT,
        score INT DEFAULT 0
    );
    ''')
    database.commit()
    database.close()

def select_user(chat_id):
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE telegram_id = ?
    ''', (chat_id,))
    user = cursor.fetchall()
    database.close()
    return user

def first_register_user(chat_id,nick_name, full_name):
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id,nick_name, full_name) VALUES (?,?,?)  
    ''', (chat_id, nick_name, full_name))
    database.commit()
    database.close()

def update_user_register(lng, lat, chat_id):
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE users SET lng = ?, lat = ? WHERE telegram_id = ?
    ''', (lng, lat, chat_id))
    database.commit()
    database.close()

def get_lng_lat_user(chat_id):
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT lng, lat FROM users WHERE telegram_id = ?
    ''', (chat_id,))
    lng_lat = cursor.fetchall()
    database.close()
    return lng_lat

def get_score(chat_id):
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT score FROM users WHERE telegram_id = ?
    ''', (chat_id,))
    score = cursor.fetchone()[0]
    database.close()
    if score == None: score = 0
    return score

def commit_score(score, chat_id):
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE users SET score = ?  WHERE telegram_id = ?
    ''', (score, chat_id,))
    database.commit()
    database.close()

def create_table_holiday():
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS table_holiday(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status_holiday TEXT
    );
    ''')
    database.commit()
    database.close()

def update_table_holiday(status_holiday):
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO table_holiday(status_holiday) VALUES (?)
    ''', (status_holiday,))
    database.commit() #    UPDATE table_holiday SET status_holiday = ?
    database.close()

def get_table_holiday():
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT status_holiday
    FROM table_holiday
    ''')
    start_finish = cursor.fetchone()
    database.close()
    return start_finish

def winer_user():
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute(''' 
    SELECT full_name, telegram_id FROM users
    ORDER BY score DESC LIMIT 1
    ''')
    winer_user = cursor.fetchone()
    database.close()
    return winer_user

def get_rating():
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute(''' 
    SELECT * FROM users
    ORDER BY score DESC
    ''')
    rating = cursor.fetchall()
    database.close()
    return rating

def get_count_id():
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''     
    SELECT COUNT(user_id)
    FROM users
    ''')
    sum_id = cursor.fetchone()
    database.close()
    return sum_id

def create_winer_user():
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS win_users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        winer_user TEXT,
        nick_name TEXT,
        ball TEXT
    );
    ''')
    database.commit()
    database.close()

def insert_win_user(winer_user, ball, nick_name):
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO win_users (winer_user, ball, nick_name)
    VALUES (?,?,?)
    ''', (winer_user, ball, nick_name,))
    database.commit()
    database.close()

def get_win_user():
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM win_users ORDER BY id DESC LIMIT 1
    ''')
    user_win = cursor.fetchall()
    database.close()
    return user_win

def update_ball():
    database = sqlite3.connect('telegram_bot.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE users SET score = 0
    ''')
    database.commit()
    database.close()