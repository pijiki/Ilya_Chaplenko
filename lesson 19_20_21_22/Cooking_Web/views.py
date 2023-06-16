from django.shortcuts import render
from .models import Post, Category
from django.db.models import F

def index(request):
    """Главная страница"""
    posts = Post.objects.all()

    context = {
        'title': 'Главная страница',
        'posts': posts
    }
    return render(request, 'Cooking_Web/index.html', context)

def category_list(request, pk):
    """Реакция на нажатие кнопки"""
    posts = Post.objects.filter(category_id=pk)

    context = {
        'title': posts[0].category.title if posts else 'Статей на данной категории не существует!',
        'posts': posts
    }
    return render(request, 'Cooking_web/index.html', context)

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

    return render(request, 'Cooking_web/article_detail.html', context)