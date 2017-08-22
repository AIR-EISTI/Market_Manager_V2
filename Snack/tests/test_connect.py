from django.test import TestCase
from django.contrib.auth.models import User, Permission


class TestConnectLogout(TestCase):

    # Set up the database
    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        basic = Permission.objects.get(codename='basic_account')
        self.user.user_permissions.add(basic)
        self.user.set_password('test')
        self.user.save()

    def test_connect_success(self):
        response = self.client.post(
            '/',
            {'username': 'user', 'password': 'test'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/purchase/')

    def test_connect_fail(self):
        response = self.client.post(
            '/',
            {'username': 'user', 'password': 'false'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_wrong_information(self):
        response = self.client.post(
            '/',
            {'username': '', 'password': 'aaa'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_user_already_connect(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/purchase/')

    def test_logout_redirect(self):
        self.client.force_login(self.user)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
