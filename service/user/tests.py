from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class TestRegister(APITestCase):
    """Test case for registering new user"""
    def test_register(self):
        """Test this"""
        data = {
            'username': 'testcase',
            'email': 'testcase@gmail.com',
            'password': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestLoginLogout(APITestCase):
    """Test case for login and logout"""
    def setUp(self):
        """Set up test variables"""
        self.user = User.objects.create_user(username='testcase', password='testpassword')
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_login(self):
        """Test loging"""
        data = {
            'username': 'testcase',
            'password': 'testpassword'
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        """Test logout"""
        self.assertTrue(User.objects.filter(username='testcase').exists())
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
