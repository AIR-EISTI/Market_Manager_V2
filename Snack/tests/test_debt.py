import json

from django.test import TestCase
from django.contrib.auth.models import User, Permission

from Snack.models import Profil


class TestPurchase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        treasurer = Permission.objects.get(codename='treasurer_account')
        self.user.user_permissions.add(treasurer)
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)

    def test_set_debt(self):
        response = self.client.post(
            '/debt/',
            {'id': 1, 'debt': 5}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(5, Profil.objects.get(id=1).debt)
        self.assertEqual(True, json.loads(response.content)['res'])

    def test_get_all_user(self):
        response = self.client.get('/debt/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.profil, response.context['profils'])
