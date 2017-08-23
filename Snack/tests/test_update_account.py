from django.test import TestCase
from django.contrib.auth.models import User, Permission

from Snack.models import Profil


class TestConnectLogout(TestCase):

    # Set up the database
    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        admin = Permission.objects.get(codename='admin_account')
        self.user.user_permissions.add(admin)
        self.user.set_password('test')
        self.user.save()
        self.client.force_login(self.user)

        user2 = User.objects.create(username='user2', password='test')
        user2.set_password('test')
        user2.first_name = 'first'
        user2.last_name = 'last'
        user2.save()
        profil2 = Profil(user=user2)
        profil2.save()

    def test_update_success(self):
        response = self.client.post(
            '/update_account/',
            {
                'id_user': '2',
                'username': 'user3',
                'first_name': 'first3',
                'last_name': 'last3',
                'debt': '3',
                'card_number': 'aefd78'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/permissions/')
        profil = Profil.objects.get(user__id=2)
        self.assertEqual('user3', profil.user.username)
        self.assertEqual('first3', profil.user.first_name)
        self.assertEqual('last3', profil.user.last_name)
        self.assertEqual(3, profil.debt)
        self.assertEqual('aefd78', profil.card_number)

    def test_update_username_already_exist(self):
        response = self.client.post(
            '/update_account/',
            {
                'id_user': '2',
                'username': 'user',
                'first_name': 'first3',
                'last_name': 'last3',
                'debt': '3',
                'card_number': 'aefd78'
            }
        )
        self.assertEqual(response.status_code, 302)
