import sqlite3


def create_user_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        telegram_id BIGINT NOT NULL UNIQUE,
        phone TEXT
    );
    ''')
    database.commit()
    database.close()




def create_carts_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carts(
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(user_id) UNIQUE,
        total_price DECIMAL(12, 2) DEFAULT 0,
        total_products INTEGER DEFAULT 0
    );
    ''')
    database.commit()
    database.close()




def create_cart_products_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_products(
        cart_product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER REFERENCES carts(cart_id),
        product_name VARCHAR(50) NOT NULL,
        quantity INTEGER NOT NULL,
        final_price DECIMAL(10, 2) NOT NULL,
        UNIQUE(cart_id, product_name) 
    );
    ''')

    database.commit()
    database.close()




def create_categories_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories(
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name VARCHAR(20) NOT NULL UNIQUE
    )
    ''')

    database.commit()
    database.close()




def create_products_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        product_name VARCHAR(20) NOT NULL UNIQUE,
        price DECIMAL(12, 2) NOT NULL,
        description VARCHAR(100),
        image TEXT,
        FOREIGN KEY(category_id) REFERENCES categories(category_id)
    );
    ''')

    database.commit()
    database.close()



def insert_category_admin(category): # TODO 
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO categories(category_name) VALUES (?)
    ''', (category))
    database.commit()
    database.close() 


def insert_products_admin(category_id, product_name, price, description, image): # TODO
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO products(category_id, product_name, price, description, image) VALUES
    (?, ?, ?, ?)
    ''', (category_id, product_name, price, description, image))

    database.commit()
    database.close()



def insert_categories():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO categories(category_name) VALUES
    ('Лаваши'),
    ('Донары'),
    ('Хот-Доги'),
    ('Десерты'),
    ('Напитки'),
    ('Соусы')
    ''')

    database.commit()
    database.close()




def insert_products_table():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO products(category_id, product_name, price, description, image) VALUES
    (1, 'Мини лаваш', 20000, 'Мясо, тесто, помидоры', 'media/lavash/lavash_1.jpg'),
    (1, 'Мини говяжий', 22000, 'Мясо, тесто, помидоры', 'media/lavash/lavash_2.jpg'),
    (1, 'Мини с сыром', 24000, 'Мясо, тесто, помидоры', 'media/lavash/lavash_3.jpg')  
    ''')

    database.commit()
    database.close()



def first_select_user(chat_id):
    """Проверка на существования пользователя"""
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE telegram_id = ?
    ''', (chat_id,))
    user = cursor.fetchone()
    database.close()
    return user


def first_register_user(chat_id, full_name):
    """Регистрация пользователя"""
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO users(telegram_id, full_name) VALUES (?,?)  
    ''', (chat_id, full_name))
    database.commit()
    database.close()


def update_user_to_finish_register(phone, chat_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE users SET phone = ? WHERE telegram_id = ?
    ''', (phone, chat_id))
    database.commit()
    database.close()


def insert_to_cart(chat_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO carts(user_id) VALUES 
    (
        (SELECT user_id FROM users WHERE telegram_id = ?)
    )
    ''', (chat_id,))
    database.commit()
    database.close()


def get_all_categories():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM categories;
    ''')
    categories = cursor.fetchall()
    database.close()
    return categories


def get_products_by_category(category_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_id, product_name FROM products WHERE category_id = ?
    ''', (category_id,))
    products = cursor.fetchall()
    database.close()
    return products

