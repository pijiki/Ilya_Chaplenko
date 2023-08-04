from django.urls import path
from .views import *

urlpatterns = [
    path('', Page.as_view(), name='index'),
    path('category/<slug:slug>/', SubCategoryPage.as_view(), name='category_detail'),
    path('product/<slug:slug>/', ProductPage.as_view(), name='product_page'),
    path('login_registration/', login_registration, name='login_registration'),
    path('login_authentication/', login_authentication, name='login_authentication'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', register, name='register'),
    path('save_review/<int:product_id>/', save_review, name='save_review'),
]