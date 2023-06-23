from django.shortcuts import render, redirect
from .forms import PostAddForm, LoginForm, RegisterForm
from .models import Post
from django.db.models import F
from django.contrib.auth import login, logout
from django.contrib import messages



def index(request):
    """Главная страница"""
    posts = Post.objects.all()

    context = {
        'title': 'Главная страница',
        'posts': posts
    }
    return render(
        request, 
        'Cooking_Web/index.html', 
        context
    )

def category_list(request, pk):
    """Реакция на нажатие кнопки"""
    posts = Post.objects.filter(category_id=pk)

    context = {
        'title': posts[0].category.title if posts else 'Статей на данной категории не существует!',
        'posts': posts
    }
    return render(
        request, 
        'Cooking_web/index.html', 
        context
    )

def article_detail(request, pk):
    """Страница статьи"""
    article = Post.objects.get(pk=pk)
    Post.objects.filter(pk=pk).update(watched=F('watched') + 1)
    recommendations = Post.objects.all().order_by('-watched')[:4]

    context = {
        'title': article.title,
        'post': article,
        'recommendations': recommendations
     }

    return render(
        request, 
        'Cooking_web/article_detail.html',
        context
    )

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
