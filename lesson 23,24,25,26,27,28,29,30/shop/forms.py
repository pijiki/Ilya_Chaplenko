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
    """Форма Отзывов"""

    class Meta:
        """Поведенческий харакатер класса"""
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

class CustomerForm(forms.ModelForm):
    """Форма Контактной информации"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@gmail.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998 XX XXX XXX'
            })
        }

class ShippingForm(forms.ModelForm):
    """Форма Адреса доставки"""

    class Meta:
        """Поведенческий харакатер класса"""
        model = ShippingAddress
        fields = ('city', 'state', 'street')
        widgets = {
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Город'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Район'
            }),
            'street': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Улица/Дом/Квартира'
            })
        }