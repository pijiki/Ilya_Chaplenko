from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:pk>/', category_list, name='category_list'),
    path('post/<int:pk>/', article_detail, name='article_detail'),
    path('add_article/', add_post, name='add'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
]
