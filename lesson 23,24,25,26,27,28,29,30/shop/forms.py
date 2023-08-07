from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *

class LoginForm(AuthenticationForm):
    """Форма аутендификации"""

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))

class RegistrationForm(UserCreationForm):
    """Форма регистрации"""

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))

    try_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        """Поведенческий харакатер класса"""
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Почта'
            })
        }


class ReviewForm(forms.ModelForm):
    """Отзывы"""

    class Meta:
        model = Review
        fields = ('text','grade')
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш отзыв..'
            }),
            'grade': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Оценка'
            })
        }
