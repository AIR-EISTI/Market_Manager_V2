from django.test import TestCase
from django.contrib.auth.models import User


class TestConnect(TestCase):

    # Set up the database
    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        self.user.save()

    # Redirect to / if the form is not valid
    def test_connect_view_denies_anonymous(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/', follow=True)
        self.assertRedirects(response, '/')

    # Redirect to /purchase/ if the connexion is a success
    def test_connect_success(self):
        response = self.client.post('/', {'username': 'user', 'password': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/purchase/')

    # Redirect to / if the connexion fail
    def test_connect_fail(self):
        response = self.client.post('/', {'username': 'user', 'password': 'false'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    # Redirect to /purchase/ if the user is already connected
    def test_connect_redirect(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/purchase/')
