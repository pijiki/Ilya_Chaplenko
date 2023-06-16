from sqlalchemy import String, Integer, BigInteger, DECIMAL, create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy.schema import UniqueConstraint

from liblary.config import DB_NAME, DB_HOST, DB_PASSWORD, DB_USER


engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}", echo=False)


class Base(DeclarativeBase):
    pass


class Users(Base):
    """Создание таблицы юзера"""
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50))
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    phone: Mapped[int] = mapped_column(BigInteger)

    def __str__(self):
        return f"User(user_id={self.user_id!r}, " \
               f"cart={self.cart!r}, " \
               f"full_name={self.full_name!r}, " \
               f"telegram_id={self.telegram_id!r}, " \
               f"phone={self.phone!r}) "

    def __repr__(self):
        return str(self)
    

class Carts(Base):
    """Создание временной корзинки юзера"""
    __tablename__ = "carts"

    cart_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), unique=True)
    total_price: Mapped[DECIMAL] = mapped_column(DECIMAL(12, 2), default=0)
    total_products: Mapped[int] = mapped_column(Integer, default=0)


    def __str__(self):
        return f"Cart(cart_id={self.cart_id!r}, " \
               f"user_id={self.user_id!r}, " \
               f"total_price={self.total_price!r}," \
               f"total_products={self.total_products!r}) "

    def __repr__(self):
        return str(self)


class FinallyCarts(Base):
    """Создание финальной корзинки юзера"""
    __tablename__ = "finally_carts"

    finally_id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.cart_id'))
    product_name: Mapped[str] = mapped_column(String(60), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    finall_price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2))
    __table_args__ = (UniqueConstraint('cart_id', 'product_name'),)

    def __str__(self):
        return f"FinallyCarts(finally_id={self.finally_id!r}, " \
               f"cart_id={self.cart_id!r}, " \
               f"product_name={self.product_name!r}, " \
               f"quantity={self.quantity!r}, " \
               f"final_price={self.final_price!r}) "

    def __repr__(self):
        return str(self)


class Categories(Base):
    """Создание категорий продуктов"""
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    def __str__(self):
        return f"Categories(category_id={self.category_id!r}, " \
               f"category_name={self.category_name!r}) "

    def __repr__(self):
        return str(self)


class Products(Base):
    """Создание таблицы продуктов"""
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.category_id'))
    product_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    product_price: Mapped[DECIMAL] = mapped_column(DECIMAL(12, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    image: Mapped[str] = mapped_column(String)
    
    def __str__(self):
        return f"Products(product_id={self.product_id}, " \
               f"category_id={self.category_id}, " \
               f"product_name={self.product_name}, " \
               f"product_price={self.product_price}, " \
               f"description={self.description}, " \
               f"image={self.image}) "
    
    def __repr__(self):
        return str(self)
    

class History(Base):
    """Создание истории покупок"""
    __tablename__ = "histories"

    history_id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(ForeignKey('users.telegram_id'))
    name: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    def __str__(self):
        return f"Histories(history_id={self.history_id}, " \
               f"telegram_id={self.telegram_id}, " \
               f"name={self.name}, " \
               f"quantity={self.quantity}, " \
               f"price={self.price}) "
    
    def __repr__(self):
        return str(self)
    
def main():
    """Только для создания таблиц и первичного наполнения"""
    Base.metadata.create_all(engine)
    categories = ('Лаваши', 'Донары', 'Хот-Доги', 'Десерты', 'Напитки', 'Соусы')
    products = (
        (1, 'Мини лаваш', 20000, 'Мясо, тесто, помидоры', 'media/lavash/lavash_1.jpg'),
        (1, 'Мини говяжий', 22000, 'Мясо, тесто, помидоры', 'media/lavash/lavash_2.jpg'),
        (1, 'Мини с сыром', 24000, 'Мясо, тесто, помидоры', 'media/lavash/lavash_3.jpg')
    )
    with Session(engine) as session:
        for category in categories:
            query = Categories(category_name=category)
            session.add(query)
            session.commit()
        for product in products:
            query = Products(
                category_id=product[1],
                product_name=product[2],
                product_price= product[3],
                description=product[4],
                image=product[5]
            )
            session.add(query)
            session.commit()

if __name__ == '__main__':
    main()