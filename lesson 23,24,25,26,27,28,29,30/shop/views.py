from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from .models import Category, Product

class Page(ListView):
    """Главная страница"""

    model = Product
    context_object_name = 'categories'
    extra_context = {
        'title': 'Главная страница',
    }
    template_name = 'shop/index.html'


    def get_queryset(self):
        """Вывод родительских категорий"""

        categories = Category.objects.filter(
            parent=None
        )
        return categories
    
    def get_context_data(self, **kwargs):
        """Вывод дополнительных элементов на главную страничку"""
        context = super().get_context_data()
        context['top_products'] = Product.objects.order_by('-watched')[:8]
        return context

class SubCategoryPage(ListView):
    """Вывод подкатегорий на другой странице"""
    model = Product
    context_object_name = 'products'
    template_name = 'shop/category_page.html'

    def get_queryset(self):
        """Получение всех товаров по категории"""
        type_field = self.request.GET.get('type')

        if type_field:
            products = Product.objects.filter(category__slug=type_field)
            return products


        parent_category = Category.objects.get(
            slug=self.kwargs['slug']
        )   
        subcategories = parent_category.subcategories.all()
        products = Product.objects.filter(
            category__in=subcategories).order_by('?')
        
        sort_field = self.request.GET.get('sort')
        if sort_field:
            products = products.order_by(sort_field)
        return products
    
    def get_context_data(self, **kwargs):
        """Вывод дополнительных элементов на страничку"""
        context = super().get_context_data()
        parent_category = Category.objects.get(
            slug=self.kwargs['slug']
        )
        context['category'] = parent_category
        context['title'] = parent_category.title
        return context