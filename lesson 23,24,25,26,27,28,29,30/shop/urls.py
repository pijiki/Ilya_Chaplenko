from django.urls import path
from .views import *

urlpatterns = [
    path('', Page.as_view(), name='index'),
]