from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from posts.models import Post, Like

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

    def test_create_post(self):
        self.client.force_login(self.user)

        new_post = {
            'text': "text",
            }

        response = self.client.post(reverse('posts-list'), data=new_post)
        self.assertEqual(201, response.status_code)

    def test_create_post_as_non_authorised(self):

        new_post = {
            'text': "text",
        }

        response = self.client.post(reverse('posts-list'), data=new_post)
        self.assertEqual(401, response.status_code)

    def test_create_post_without_text(self):
        self.client.force_login(self.user)
        new_post = {
            'text': ''
        }

        response = self.client.post(reverse('posts-list'), data=new_post)
        self.assertEqual(400, response.status_code)

    def test_like_post(self):
        self.test_create_post()

        response = self.client.post(reverse('posts-like', kwargs={'pk': Post.objects.first().id}))
        self.assertEqual(204, response.status_code)
        self.assertEqual(1, Like.objects.count())

    def test_delete_like_post(self):
        self.test_create_post()

        response = self.client.delete(reverse('posts-like', kwargs={'pk': Post.objects.first().id}))
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Like.objects.count())

    def test_like_post_as_non_authorised(self):
        self.test_create_post()
        self.client.logout()

        response = self.client.delete(reverse('posts-like', kwargs={'pk': Post.objects.first().id}))
        self.assertEqual(401, response.status_code)

