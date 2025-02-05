from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class UserRegistrationTestCase(TestCase):

    def setUp(self):
        self.url = reverse('users:registration')
        User.objects.create_user(username='user11', password='password111').save()

    def test_registration_successful(self):
        """Проверяем, успешную регистрацию"""
        data = {
            'username': 'user_test',
            'password': 'password111',
            'password_check': 'password111'
        }

        response = self.client.post(self.url, data=data, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users:login'))

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('weather_app:main'))
        self.assertRedirects(response, f'{reverse("users:login")}?next={reverse("weather_app:main")}')

    def test_too_short_username(self):
        data = {
            'username': 'us',
            'password': 'password111',
            'password_check': 'password111'
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='us').exists())
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_too_long_password(self):
        data = {
            'username': 'user_test',
            'password': 'password111' * 4,
            'password_check': 'password111' * 4
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='us').exists())
        self.assertTemplateUsed(response, 'users/registration.html')