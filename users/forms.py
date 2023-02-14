from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from users.models import User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'username1 form-control', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'username1 form-control', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'password1 form-control', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'password1 form-control', 'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'username1 form-control', 'placeholder': "Введите имя пользователя"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'password1 form-control', 'placeholder': "Введите пароль"}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'username1 form-control',
        'readonly': True}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'username1 form-control',
        'readonly': True}))
    status = forms.ChoiceField(required=True, widget=forms.EmailInput(attrs={
        'class': 'username1 form-control',
        'readonly': True}))


    class Meta:
        model = User
        fields = ('username', 'email', 'status')

