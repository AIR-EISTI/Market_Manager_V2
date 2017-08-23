import json

from django.test import TestCase
from django.contrib.auth.models import User, Permission

from Snack.models import Profil


class TestHistory(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        admin = Permission.objects.get(codename='admin_account')
        self.basic = Permission.objects.get(codename='basic_account')
        self.user.user_permissions.add(admin)
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)
        self.user2 = User.objects.create(username='user2', password='test')
        self.user2.set_password('test')
        self.user.save()

    def test_add_permissions(self):
        response = self.client.post(
            '/permissions/',
            {'username': '"user2"', 'type': '"basic"', 'state': '1'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.basic, self.user2.user_permissions.all())
        self.assertEqual(True, json.loads(response.content)['return'])

    def test_remove_permissions(self):
        self.user2.user_permissions.add(self.basic)
        response = self.client.post(
            '/permissions/',
            {'username': '"user2"', 'type': '"basic"', 'state': '0'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, json.loads(response.content)['return'])
        self.assertNotIn(self.basic, self.user2.user_permissions.all())
