from datetime import timedelta
from http import HTTPStatus
from time import sleep

import requests
from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import User, EmailVerification


class TestDataBase(TestCase):
    fixtures = [
        "users/fixtures/users.json"
    ]

    def setUp(self):
        self.data = {
            'username': 'testuser', 'email': 'testuser@example.com',
            'password1': 'GSDFGdfdfg!1', 'password2': 'GSDFGdfdfg!1',
        }
        self.user = User.objects.get(username='admin')
        self.path = reverse('users:registration')

    def test_user_exists(self):

        """Проверка наличия существующего пользователя"""

        users = User.objects.all()
        users_number = users.count()
        user = users.first()
        self.assertEqual(users_number, 1)
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(self.user.check_password('123'))

    def test_new_user(self):

        """Создание нового пользователя"""

        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        new_user = User.objects.get(username=username)
        self.assertEqual(new_user.status, User.STANDARD)
        self.assertEqual(new_user.email, 'testuser@example.com')
        self.assertFalse(new_user.is_verified_email)

    def test_email_verification(self):

        """Подтверждение email для нового пользователя"""

        username = self.data['username']
        self.client.post(self.path, self.data)
        new_user = User.objects.get(username=username)
        email_verification = EmailVerification.objects.filter(user=new_user.id)
        self.assertEqual(email_verification.count(), 1)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )
        path = reverse('users:email_verification',
                       kwargs={'email': self.data['email'], 'code': email_verification.first().code})
        self.client.get(path)
        new_user = User.objects.get(username=username)
        self.assertTrue(new_user.is_verified_email)

    def test_user_registration_post_error(self):

        """Проверка на уникальность логина, email. Совпадение паролей"""

        User.objects.create(username=self.data['username'],
                            email="sdasd@mail.ru")
        response = self.client.post(self.path, self.data)
        self.assertFormError(response, form='form', field='username',
                             errors='Пользователь с таким именем уже существует.')
        response = self.client.post(self.path, {
            'username': 'testuser1', 'email': 'sdasd@mail.ru',
            'password1': 'GSDFGdfdfg!1', 'password2': 'GSDFGdfdfg!1',
        })
        self.assertFormError(response, form='form', field='email',
                             errors='Пользователь с таким Email уже существует.')
        response = self.client.post(self.path, {
            'username': 'testuser1', 'email': 'sdasd@mail.ru',
            'password1': 'GSDFGdfdfg!1234', 'password2': 'GSDFGdfdfg!1',
        })
        self.assertFormError(response, form='form', field='password2',
                             errors='Введенные пароли не совпадают.')

        """Проверка подтвержения Email при истекшем сроке"""

        new_user = User.objects.get(username=self.data['username'])
        email_verification = EmailVerification.objects.filter(user=new_user.id)
        email_verification.update(expiration=email_verification.first().expiration-timedelta(hours=49))
        path = reverse('users:email_verification',
                       kwargs={'email': new_user.email, 'code': email_verification.first().code})
        self.client.get(path)
        new_user = User.objects.get(username=self.data['username'])
        self.assertFalse(new_user.is_verified_email)

    def test_user_login(self):

        """Проверка вход, выход"""

        response = self.client.post(self.path, self.data)
        self.assertRedirects(response, reverse('users:login'))
        response = self.client.get(reverse('store:store'))
        self.assertNotContains(response, 'Выйти')
        response = self.client.post(reverse('users:login'), {'username': 'testuser', 'password': 'GSDFGdfdfg!1'})
        self.assertRedirects(response, reverse('users:profile', kwargs={'pk': User.objects.get(username=self.data['username']).pk}))
        response = self.client.get(reverse('store:store'))
        self.assertContains(response, 'Выйти')

        """Проверка появления ошибок"""

        path = reverse('users:login',)
        response = self.client.post(path, {
            'username': 'testuser1123',  'password': 'GSDFGdfdfg!1234'
        })
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
        response = self.client.post(path, {
            'username': 'testuser', 'password': 'GSDFGdfdfgdfgfdg!1234'
        })
        self.assertContains(response,
                            'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')






















