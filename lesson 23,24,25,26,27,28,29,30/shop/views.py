from random import randint
from typing import Any, Dict

from .forms import LoginForm, RegistrationForm, ReviewForm
from .models import Category, Product, Review

from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import DetailView, ListView
from django.shortcuts import render, redirect
from django.db.models.query import QuerySet



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
    """Вывод подкатегорий на отдельной странице"""
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
    

class ProductPage(DetailView):
    """Вывод товара на отдельной странице"""
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_page.html'

    def get_context_data(self, **kwargs):
        """Вывод дополнительных элементов на страничку"""
        context = super().get_context_data()
        product = Product.objects.get(
            slug=self.kwargs['slug']
        )
        context['title'] = product.title    
        products = Product.objects.filter(category=product.category)
        data = []
        for count in range(5):
            random_index = randint(0, len(products)-1)
            random_product = products[random_index]
            if random_product not in data and str(random_product) != product.title:
                data.append(random_product)
        context['products'] = data
        context['reviews'] = Review.objects.filter(product=product).order_by('-pk')
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()
        return context
    
def login_registration(request):
    """Регистрация пользователя"""
    context = {
        'title': 'Зарегистрироваться',
        'registration_form': RegistrationForm()
    }

    return render(request, 'shop/login_registration.html', context)

def login_authentication(request):
    """Аутендификации пользователя"""
    context = {
        'title': 'Войти',
        'login_form': LoginForm()
    }

    return render(request, 'shop/login_authentication.html', context)


def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')
    else:
        messages.error(request, 'Не верное имя пользователя или пароль')
        return redirect('login_authentication')


def user_logout(request):
    logout(request)
    return redirect('index')


def register(request):
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        print(form)
        form.save()
        messages.success(request, 'Аккаунт успешно создан. Войдите в аккаунт')
    else:
        for error in form.errors:
            print(form.errors[error].as_text())
            messages.error(request, form.errors[error].as_text())

    return redirect('login_registration')

def save_review(request, product_id):
    """Cохранения отзывов"""

    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        product = Product.objects.get(pk=product_id)
        review.product = product
        review.save()
        return redirect('product_page', product.slug)
