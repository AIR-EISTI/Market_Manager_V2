from django.test import TestCase
from django.contrib.auth.models import User

from Snack.models import Profil


class TestSignUp(TestCase):

    def test_signup_method_get(self):
        response = self.client.get('/signup/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_form_valid(self):
        response = self.client.post(
            '/signup/',
            {
                'username': 'user',
                'password': 'pass',
                'password_verif': 'pass',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': ''
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/purchase/')

    def test_signup_form_invalid(self):
        response = self.client.post(
            '/signup/',
            {
                'username': 'user',
                'password': 'pass',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': ''
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_signup_different_password(self):
        response = self.client.post(
            '/signup/',
            {
                'username': 'user',
                'password': 'pass',
                'password_verif': 'pass2',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': ''
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_signup_card_number(self):
        response = self.client.post(
            '/signup/',
            {
                'username': 'user',
                'password': 'pass',
                'password_verif': 'pass',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': 'e8e6e9e1'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/purchase/')

    def test_username_already_exist(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        response = self.client.post(
            '/signup/',
            {
                'username': 'user',
                'password': 'test',
                'password_verif': 'test',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': ''
            }
        )
        self.assertEqual(response.status_code, 200)
