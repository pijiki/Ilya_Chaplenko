from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from .models import Category, Product

class Page(ListView):
    """Главная страница"""

    model = Product
    extra_context = {
        'title': 'Главная страница',
    }
    template_name = 'shop/index.html'



