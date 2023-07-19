from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    """Категории товаров"""
    title = models.CharField(
        max_length=150, 
        verbose_name='Название категории'
    )

    image = models.ImageField(
        upload_to='categories/', 
        null=True, blank=True, 
        verbose_name='Изображение'
    )

    slug = models.SlugField(
        unique=True, 
        null=True
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='subcategories'
    )
    def get_absolute_url(self):
        pass

    def __str__(self):
        """Строковое представление"""
        return self.title

    def __repr__(self):
        """Подобие строкового представления"""
        return f'Категория: pk={self.pk}, title={self.title}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    """Товары"""

    title = models.CharField(
        max_length=255, 
        verbose_name='Название товара'
    )

    price = models.FloatField(
        verbose_name='Цена'
    )

    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата создания'
    )

    watched = models.IntegerField(
        default=0, 
        verbose_name='Просмотры'
    )

    quantity = models.IntegerField(
        default=0, 
        verbose_name='Количество на складе'
    )

    description = models.TextField(
        default='Здесь скоро будет описание', 
        verbose_name='Описание товара'
    )

    info = models.TextField(
        default='Дополнительная информация о продукте', 
        verbose_name='Информация о товаре'
    )

    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name='Категория', 
        related_name='products'
    )

    slug = models.SlugField(
        unique=True, 
        null=True
    )

    size = models.IntegerField(
        default=30, 
        verbose_name='Размер в мм'
    )

    color = models.CharField(
        max_length=30, 
        default='Серебро', 
        verbose_name='Цвет/Материал'
    )

    def get_absolute_url(self):
        pass

    def __str__(self):
        """Строковое представление"""
        return self.title

    def __repr__(self):
        """Подобие строкового представления"""
        return f'Товар: pk={self.pk}, title={self.title} price={self.price}'

    class Meta:
        """Характер Класса"""
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Gallery(models.Model):
    """Картинки товаров"""
    image = models.ImageField(
        upload_to='products/', 
        verbose_name='Изображение'
    )

    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images'
    )

    class Meta:
        """Характер Класса"""
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея товаров'