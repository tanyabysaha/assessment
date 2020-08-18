from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from rest_framework.test import APITestCase, APIClient

User = get_user_model()

default_user = {
    'email': 'user@user.com',
    'first_name': 'User',
    'last_name': 'User',
    'password': '12345678',
}


class TestAccountsApi(APITestCase):
    """Unit tests for Accounts app."""

    def setUp(self):
        self.client = APIClient()
        self.user = User(**default_user)
        self.user.set_password('12345678')
        self.user.save()

    def test_register_user(self):
        new_user = {
            'email': 'user2@user.com',
            'password': '12345678'
        }

        response = self.client.post(reverse('user-register'), data=new_user)
        self.assertEqual(204, response.status_code)

    def test_try_register_user_with_invalid_email(self):
        new_user = {
            'email': 'useruser.com',
            'password': '12345678'
        }

        response = self.client.post(reverse('user-register'), data=new_user)
        self.assertEqual(400, response.status_code)

    def test_register_user_without_email(self):
        new_user = {
            'password': '12345678'
        }

        response = self.client.post(reverse('user-register'), data=new_user)
        self.assertEqual(400, response.status_code)

    def test_register_user_on_same_email(self):
        new_user = {
            'email': self.user.email,
            'password': '12345678'
        }

        response = self.client.post(reverse('user-register'), data=new_user)
        self.assertEqual(400, response.status_code)

    def test_login_user(self, password=default_user.get('password')):
        user = {
            'email': self.user.email,
            'password': password,
        }

        response = self.client.post(reverse('user-login'), data=user)
        self.assertEqual(200, response.status_code)

    def test_try_login_user_with_invalid_email(self):
        new_user = {
            'email': 'useruser.com',
            'password': '12345678'
        }

        response = self.client.post(reverse('user-login'), data=new_user)
        self.assertEqual(400, response.status_code)

    def test_try_login_user_with_invalid_password(self):
        new_user = {
            'email': self.user.email,
            'password': 'wrong'
        }

        response = self.client.post(reverse('user-login'), data=new_user)
        self.assertEqual(400, response.status_code)

    def test_try_login_user_without_password(self):
        new_user = {
            'email': self.user.email,
        }

        response = self.client.post(reverse('user-login'), data=new_user)
        self.assertEqual(400, response.status_code)

    def test_try_login_user_with_wrong_email(self):
        """Wrong email - email that does not exist in db yet"""
        new_user = {
            'email': 'test@gmail.com',
            'password': '12345678'
        }

        response = self.client.post(reverse('user-login'), data=new_user)
        self.assertEqual(400, response.status_code)
