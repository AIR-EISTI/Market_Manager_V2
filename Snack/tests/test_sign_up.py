from django.test import TestCase
from django.contrib.auth.models import User, Permission

from Snack.models import Profil
from Snack.forms import SignUpForm


class TestSignUp(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        admin = Permission.objects.get(codename='admin_account')
        self.user.user_permissions.add(admin)
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)

    def test_signup_sucess(self):
        response = self.client.post(
            '/signup/',
            {
                'username': 'user2',
                'password': 'pass',
                'password_verif': 'pass',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': ''
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/permissions/')

    def test_signup_username_already_exist(self):
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
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual('This username already exist... :\'(', message.message)
            self.assertEqual('error', message.tags)

    def test_signup_password_verifpassword_different(self):
        response = self.client.post(
            '/signup/',
            {
                'username': 'user2',
                'password': 'pass',
                'password_verif': 'pass2',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': ''
            }
        )
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual(
                'Password and validation password are not the same',
                message.message
            )
            self.assertEqual('error', message.tags)

    def test_signup_fail(self):
        response = self.client.post(
            '/signup/',
            {
                'username': '',
                'password': 'pass',
                'password_verif': 'pass2',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': ''
            }
        )
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual('Sign Up Failed', message.message)
            self.assertEqual('error', message.tags)

    def test_signup_card_number(self):
        response = self.client.post(
            '/signup/',
            {
                'username': 'user2',
                'password': 'pass',
                'password_verif': 'pass',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': 'aer56'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/permissions/')

    def test_get(self):
        response = self.client.get('/signup/')
        form = SignUpForm()
        self.assertEqual(
            [x for x in response.context['form'].fields],
            [x for x in form.fields]
        )
