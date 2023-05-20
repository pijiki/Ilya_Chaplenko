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
    (1, 'Мини лаваш', 20000, 'Мясо, тесто, помидоры', 'lesson 16,17,18/media/lavash/lavash_1.jpg'),
    (1, 'Мини говяжий', 22000, 'Мясо, тесто, помидоры', 'lesson 16,17,18/media/lavash/lavash_2.jpg'),
    (1, 'Мини с сыром', 24000, 'Мясо, тесто, помидоры', 'lesson 16,17,18/media/lavash/lavash_3.jpg'),  
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

def get_product_detail(product_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM products WHERE product_id = ?
    ''', (product_id,))
    product = cursor.fetchone()
    database.close()
    return product

def get_user_cart_id(chat_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT cart_id, total_price, total_products FROM carts WHERE user_id = (
         SELECT user_id FROM users WHERE telegram_id = ?
    )
    ''', (chat_id,))
    cart_id = cursor.fetchone()[0]
    database.close()
    return cart_id


def get_detail_product(product_name):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT * FROM products WHERE product_name = ?
    ''', (product_name,))
    product_info = cursor.fetchone()
    database.close()
    return product_info


def update_to_cart(cost, quantity, cart_id):
    if quantity < 1: quantity = 1
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE carts SET total_price = ?, total_products = ? WHERE cart_id =?
    ''', (cost * quantity, quantity, cart_id))
    database.commit()
    database.close()


def get_cost_product(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT total_price, total_products FROM carts WHERE cart_id = ?
    ''', (cart_id,))
    info = cursor.fetchone()
    database.close()
    return info


def get_sum_price_from_cart(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT SUM(final_price) from cart_products WHERE cart_id = ?
    ''', (cart_id,))
    summary_price = cursor.fetchone()
    database.close()
    return summary_price


def insert_or_update_cart_product(cart_id, product_name, quantity, cost):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()

    try:
        cursor.execute('''
        INSERT INTO cart_products (cart_id, product_name, quantity, final_price ) VALUES (?, ?, ?, ?)
        ''', (cart_id, product_name, quantity, cost))
        return True
    except:
        cursor.execute('''
        UPDATE cart_products SET quantity = ?,  final_price = ?
        WHERE product_name = ? AND cart_id = ?
        ''', (quantity, cost, product_name, cart_id))
        return False
    finally:
        database.commit()
        database.close()


def update_total_product_total_price(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    UPDATE carts SET total_products = (
        SELECT SUM(quantity) FROM cart_products WHERE cart_id = :cart_id 
    ), 
    total_price = (
        SELECT SUM(final_price) FROM cart_products WHERE cart_id = :cart_id
    )
    WHERE cart_id = :cart_id
    ''', {'cart_id': cart_id})
    database.commit()
    database.close()


def get_total_product_price(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT total_products, total_price FROM carts WHERE cart_id = ?
    ''', (cart_id,))
    total_products, total_price = cursor.fetchone()
    database.close()
    return total_products, total_price


def get_cart_products(cart_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT product_name, quantity, final_price FROM cart_products WHERE cart_id = ?
    ''', (cart_id, ))
    cart_products = cursor.fetchall()
    database.close()
    return cart_products

def create_history():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id BIGINT,
        name VARCHAR,
        quantity INTEGER NOT NULL,
        price INTEGER NOT NULL
        );
    ''')
    database.commit()
    database.close()

def delete_all():
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_products
    ''')
    database.commit()
    database.close()
    
def insert_history(telegram_id, name, quantity, price):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO history (telegram_id,name,quantity,price)
    VALUES (?, ?, ?, ?)
    ''', (telegram_id, name, quantity, price,))
    database.commit()
    database.close()

def read_history(telegram_id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT name, quantity, price
    FROM history
    WHERE telegram_id = (?);
    ''', (telegram_id,))
    history = cursor.fetchall()
    database.close()
    return history[::-1]

def delete_product_id(id):
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    DELETE FROM cart_products
    WHERE product_name = ?;
    ''', (id,))
    database.commit()
    database.close()

# def create_language():
#     database = sqlite3.connect('fastfood.db')
#     cursor = database.cursor()
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS lang(
#     language VARCHAR
#     )
#     ''')
#     database.commit()
#     database.close()

# def insert_language(lang):
#     database = sqlite3.connect('fastfood.db')
#     cursor = database.cursor()
#     cursor.execute(''' 
#     INSERT INTO lang (language)
#     VALUES (?)
#     ''', (lang,))
#     database.commit()
#     database.close()

# def get_language():
#     database = sqlite3.connect('fastfood.db')
#     cursor = database.cursor()
#     cursor.execute(''' 
#     SELECT language FROM lang;
#     ''')
#     lang = cursor.fetchone()
#     database.close()
#     return lang[0]