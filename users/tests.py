from datetime import timedelta
from time import sleep

import requests
from django.test import TestCase
from django.utils.timezone import now

from users.models import User, EmailVerification


class TestDataBase(TestCase):
    fixtures = [
        "users/fixtures/users.json"
    ]

    def setUp(self):

        self.user = User.objects.get(username='admin')
        self.new_user = User.objects.create(username='testuser', email='testuser@example.com', password='password')


    def test_user_exists(self):
        users = User.objects.all()
        users_number = users.count()
        user = users.first()
        self.assertEqual(users_number, 2)
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(self.user.check_password('123'))



    def test_new_user_(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(user.status, User.STANDARD)
        self.assertEqual(user.password, 'password')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertFalse(user.is_verified_email)


    def test_email_verification(self):
        email_verification = EmailVerification.objects.filter(user=self.new_user)
        email_verification1 = email_verification.count()

        self.assertEqual(email_verification1, 1)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )






