from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class UserTests(TestCase):
    def test_user_registration(self):
        user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass'))

    def test_user_registration_duplicate_username(self):
        User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
        with self.assertRaises(Exception):
            User.objects.create_user(username='testuser', password='testpass2', email='test2@example.com')

    def test_user_registration_invalid_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username='testuser2', password='testpass', email='invalid-email')

    def test_user_authentication_success(self):
        User.objects.create_user(username='authuser', password='authpass', email='auth@example.com')
        user = User.objects.get(username='authuser')
        self.assertTrue(user.check_password('authpass'))

    def test_user_authentication_failure(self):
        User.objects.create_user(username='authuser2', password='authpass2', email='auth2@example.com')
        user = User.objects.get(username='authuser2')
        self.assertFalse(user.check_password('wrongpass'))

    def test_user_update(self):
        user = User.objects.create_user(username='updateuser', password='updatepass', email='update@example.com')
        user.email = 'newemail@example.com'
        user.save()
        updated_user = User.objects.get(username='updateuser')
        self.assertEqual(updated_user.email, 'newemail@example.com')

    def test_user_delete(self):
        user = User.objects.create_user(username='deleteuser', password='deletepass', email='delete@example.com')
        user.delete()
        self.assertEqual(User.objects.filter(username='deleteuser').count(), 0)

class SecurityTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass1', email='user1@test.com')
        self.user2 = User.objects.create_user(username='user2', password='pass2', email='user2@test.com')

    def test_access_protected_endpoint_without_auth(self):
        url = reverse('users-detail', args=[self.user1.id])
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_user_cannot_access_other_user_data(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('users-detail', args=[self.user2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_access_own_data(self):
        self.client.login(username='user1', password='pass1')
        url = reverse('users-detail', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
