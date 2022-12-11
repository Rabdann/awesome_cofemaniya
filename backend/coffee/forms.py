from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import re

from .models import CoffeeModel


class CoffeeForm(forms.ModelForm):
    class Meta:
        model = CoffeeModel
        fields = ['name', 'description', 'price', 'volume', 'recipe', 'ingredients']

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите название кофе',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите описание кофе',
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите цену, используйте целые числа',
                }
            ),
            'volume': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Укажите объем кофе, используйте число с плавающей точкой',
                }
            ),
            'recipe': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Опишите рецепт приготовления данного кофе',
                    'rows': 5,
                }
            ),
            'ingredients': forms.CheckboxSelectMultiple(
                attrs={
                    'placeholder': 'Выберите ингредиенты',
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.match(r'\d', name):
            raise ValidationError('Название не должно начинаться с цифры')
        return name


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2,
    )
    email = forms.CharField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control', }),
    )
    password1 = forms.CharField(
        label='Придумайте пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Ваш логин',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2,
    )
    password = forms.CharField(
        label='Ваш пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Заголовок письма',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Введите тему письма с предложениями или жалобами'},
        ),
    )
    content = forms.CharField(
        label='Текст письма',
        widget=forms.Textarea(
            attrs={'class': 'form-control',
                   'rows': 11,
                   'placeholder': 'Введите текст для предложений или жалоб'}
        )
    )
