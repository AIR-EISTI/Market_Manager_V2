import json

from django.test import TestCase
from django.contrib.auth.models import User

from Snack.models import Profil


class TestTheme(TestCase):

    def test_ajax_request(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)
        response = self.client.post(
            '/change_theme/',
            {'color': '"def"'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, json.loads(response.content)['return'])
