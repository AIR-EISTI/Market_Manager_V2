import json

from django.test import TestCase
from django.contrib.auth.models import User, Permission

from Snack.models import Profil


class TestHistory(TestCase):

    def setUp(self):
        admin = Permission.objects.get(codename='admin_account')

        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        self.basic = Permission.objects.get(codename='basic_account')
        self.user.user_permissions.add(admin)
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)

        self.user2 = User.objects.create(username='user2', password='test')
        self.user2.first_name = 'first'
        self.user2.last_name = 'last'
        self.user2.set_password('test')
        self.user2.save()
        self.profil2 = Profil(user=self.user2)
        self.profil2.save()

    def test_add_permissions(self):
        response = self.client.post(
            '/account/',
            {'username': '"user2"'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual('user2', json.loads(response.content)['username'])
        self.assertEqual('first', json.loads(response.content)['first_name'])
        self.assertEqual('last', json.loads(response.content)['last_name'])
        self.assertEqual(0.0, json.loads(response.content)['debt'])
        self.assertEqual('', json.loads(response.content)['card_number'])
        self.assertEqual(2, json.loads(response.content)['id_user'])
