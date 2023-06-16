from typing import Iterable
from sqlalchemy.orm import Session
from sqlalchemy import update, delete, select
from sqlalchemy.sql.functions import sum
from sqlalchemy.exc import IntegrityError

from liblary.model import *

with Session(engine) as session:
    db_session = session


def db_check_user(chat_id: int) -> Users | None:
    """Проверка на существование юзера"""
    query = select(Users
    ).filter(
        Users.telegram_id == chat_id
    )
    result: Users | None = db_session.scalar(query)
    return result

def db_first_register_user(full_name: str, chat_id: int) -> None:
    """Первая регистрация юзера"""
    query = Users(full_name=full_name,
    telegram_id=chat_id
    )
    db_session.add(query)
    db_session.commit()

def db_finally_register_user(chat_id: int, phone: str) -> None:
    """Финальная регистрация юзера"""
    query = update(Users
    ).filter(
        Users.telegram_id == chat_id
    ).values(
        phone=phone
    )
    db_session.execute(query)
    db_session.commit()

def db_create_user_cart(chat_id: int) -> None:
    """Создание корзинки юзера"""
    subquery = db_session.scalar(select(Users
    ).filter(
        Users.telegram_id == chat_id)
    )
    query = Carts(user_id=subquery.user_id)
    db_session.add(query)
    db_session.commit()

def db_get_categories() -> Iterable:
    """Получение категорий"""
    return db_session.scalars(select(Categories))
       
def db_get_products(category_id: int) -> Iterable:
    """Получение продуктов"""
    query = select(Products
    ).filter(
        Products.category_id == category_id
    )
    return db_session.scalars(query)

def db_get_product(product_id: int) -> Products:
    """Получение информации о продукте"""
    query = select(Products
    ).filter(
        Products.product_id == product_id
    )
    return db_session.scalar(query)

def db_get_product_by_name(product_name: str) -> Products:
    """Получение информации о продукте по имени"""    
    query = select(Products
    ).filter(
        Products.product_name == product_name
    )
    return db_session.scalar(query)

def db_update_to_cart(price: DECIMAL, quantity: int, cart_id: int) -> None:
    quantity = 1 if quantity < 1 else quantity
    total_price = price * quantity
    query = update(Carts).where(
        Carts.cart_id == cart_id
    ).values(
        total_price=total_price,
        total_products=quantity
    )
    db_session.execute(query)
    db_session.commit()

def db_update_to_cart(price: DECIMAL, quantity: int, cart_id: int) -> None:
    """Обновление сообщения"""
    quantity = 1 if quantity < 1 else quantity
    total_price = price * quantity
    query = update(Carts).where(
        Carts.cart_id == cart_id
    ).values(
        total_price=total_price,
        total_products=quantity
    )
    db_session.execute(query)
    db_session.commit()

def db_get_final_price(chat_id: int) -> DECIMAL:
    query = select(
        sum(FinallyCarts.finall_price)
    ).join(
        Carts
    ).join(
        Users
    ).where(
        Users.telegram_id == chat_id
    )
    return db_session.scalar(query)

def insert_or_update_cart_product(cart_id: int, product_name: str,
        total_products: int, total_price: DECIMAL) -> bool:
    """Добавление или изменение заказа"""

    try:
        query = FinallyCarts(
            cart_id=cart_id,
            product_name=product_name,
            quantity=total_products,
            final_price=total_price
        )
        return True
    
    except:
        db_session.rollback()
        query = update(
            FinallyCarts
        ).where(
            FinallyCarts.product_name == product_name
        ).where(
            FinallyCarts.cart_id == cart_id
        ).values(
            quantity=total_products,
            final_price=total_price
        )
        return False
    
    finally:
        db_session.add(query)
        db_session.commit()
        
def db_get_cart_products(chat_id: int) -> Iterable:
    query = select(
        Finally_carts.product_name,
        Finally_carts.quantity,
        Finally_carts.final_price,
        Finally_carts.cart_id
    ).join(
        Carts
    ).join(
        Users
    ).where(
        Users.telegram_id == chat_id
    )
    return db_session.execute(query).fetchall()