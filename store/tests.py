from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from store.models import Order
from store.views import find_order
from users.models import User, EmailVerification


class StoreTestCase(TestCase):
    fixtures = [
        "store/fixtures/lessons.json"
    ]

    def setUp(self):
        self.data = {
            'username': 'testuser', 'email': 'testuser@example.com',
            'password1': 'GSDFGdfdfg!1', 'password2': 'GSDFGdfdfg!1',
        }

    def test_list(self):
        """Проверка работы главной страницы"""
        path = reverse('store:store')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'store/index.html')
        self.client.post(reverse('users:registration'), self.data)
        response = self.client.get(path)
        self.assertNotContains(response, 'Выйти')
        self.client.login(username=self.data['username'], password=self.data['password1'])
        response = self.client.get(reverse('store:store'))
        self.assertContains(response, 'Выйти')

    def test_access(self):
        """Проверка доступа к урокам аккаунта без оплаты"""

        self.client.post(reverse('users:registration'), self.data)
        response = self.client.get(reverse('store:lessons', args=[4]))
        self.assertRedirects(response, reverse('store:store'))
        self.client.login(username=self.data['username'], password=self.data['password1'])
        response = self.client.get(reverse('store:lessons', args=[4]))
        self.assertRedirects(response, reverse('store:store'))


    def test_access_after_payment(self):
        """Оплата, проверка доступа, создание заказа"""

        self.client.post(reverse('users:registration'), self.data)
        user = User.objects.get(username=self.data['username'])
        self.client.login(username=self.data['username'], password=self.data['password1'])
        self.client.get(reverse('store:order', kwargs={'pk': 1}))
        order = Order.objects.get(initiator=user.id)
        find_order(order.id)
        response = self.client.get(reverse('store:lessons', args=[4]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Урок №')
        user = User.objects.get(username=self.data['username'])
        self.assertEqual(user.status, 1)
        order = Order.objects.get(initiator=user.id)
        self.assertEqual(order.status, 1)


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
        email_verification.update(expiration=email_verification.first().expiration - timedelta(hours=49))
        path = reverse('users:email_verification',
                       kwargs={'email': new_user.email, 'code': email_verification.first().code})
        self.client.get(path)
        new_user = User.objects.get(username=self.data['username'])
        self.assertFalse(new_user.is_verified_email)

    def test_user_login(self):
        """Проверка вход, выход"""

        self.client.post(self.path, self.data)
        response = self.client.get(reverse('store:store'))
        self.assertNotContains(response, 'Выйти')
        self.client.login(username=self.data['username'], password=self.data['password1'])
        response = self.client.get(reverse('store:store'))
        self.assertContains(response, 'Выйти')

        """Проверка появления ошибок"""

        path = reverse('users:login', )
        response = self.client.post(path, {
            'username': 'testuser1123', 'password': 'GSDFGdfdfg!1234'
        })
        self.assertContains(response,
                            'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
        response = self.client.post(path, {
            'username': 'testuser', 'password': 'GSDFGdfdfgdfgfdg!1234'
        })
        self.assertContains(response,
                            'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')


from django.test import TestCase

# Create your tests here.
