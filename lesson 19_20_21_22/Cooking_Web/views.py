from typing import Any
from .forms import PostAddForm, LoginForm, RegisterForm
from .models import Post, Category
from .forms import PostAddForm, LoginForm

from django.db.models import F, Q
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.views import PasswordChangeView


class Index(ListView):
    """Вывод на главную страницу"""

    model = Post
    context_object_name  = 'posts'
    template_name = 'Cooking_web/index.html'
    extra_context = { 
        'title': 'Главная станица'
    }
    def get_queryset(self):
        """Добавление фильтрации"""
        return Post.objects.filter(
            published=True
        )
    
class ArticleByCategory(Index):
    """Реакция на нажатие кнопки категорий"""
    
    def get_queryset(self):
        """Добавление фильтрации"""
        return Post.objects.filter(
            category_id = self.kwargs['pk'],
            published = True
        )
           
    def get_context_data(self, *, objects_list=None, **kwargs):
        """Для динамических данных"""
        context = super().get_context_data()
        category = Category.objects.get(
            pk=self.kwargs['pk']
        )
        context['title'] = category.title
        return context

class PostDetail(DetailView):
    """Страница статьи"""
    model = Post
    template_name = 'Cooking_web/article_detail.html'

    def get_queryset(self):
        """Добавление фильтрации"""
        return Post.objects.filter(
            category_id = self.kwargs['pk']
        )
    
    def get_context_data(self, **kwargs):
        """Для динамических данных"""
        context = super().get_context_data()
    # art
    # icle = Post.objects.get(pk=pk)
    # Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
    # recommendations = Post.objects.all().order_by('-watched')[:4]

    # context = {
    #     'title': article.title,
    #     'post': article,
    #     'recommendations': recommendations
    #  }

    # return render(
    #     request, 
    #     'Cooking_web/article_detail.html',
    #     context
    # )

def add_post(request):
    """Добавление статьи от юзера"""
    if request.method == 'POST':
        form = PostAddForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post.objects.create(**form.cleaned_data)
            post.save()
            return redirect('article_detail', post.pk)
    else:
        form = PostAddForm()
    
    context = {
        'form': form,
        'title': "Добавить статью"
    }
    return render(
        request, 
        'Cooking_web/article_add_form.html', 
        context
    )

def user_login(request):
    """Аутендификация юзера"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт')
            return redirect('index')
    else:
        form = LoginForm()

    context = {
        'title': 'Авторизация пользователя',
        'form': form
    }

    return render(request, 'Cooking_web/login_form.html', context)


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    return redirect('index')

def register(request):
    """Регистрация юзера"""
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    else: 
        form = RegisterForm()
    
    context = {
        'title': 'Регистрация пользователя',
        'form': form
    }
    return render(request, 'Cooking_web/register.html', context)
