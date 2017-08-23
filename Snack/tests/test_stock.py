import json

from django.test import TestCase
from django.contrib.auth.models import User, Permission

from Snack.models import Profil, Type, Product


class TestHistory(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        treasurer = Permission.objects.get(codename='treasurer_account')
        self.user.user_permissions.add(treasurer)
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)
        type = Type(name='barre')
        type.save()
        self.twix = Product(name='twix', type=type, price=0.1, quantity=0)
        self.twix.save()

    def test_set_number_product(self):
        response = self.client.post(
            '/stock/',
            {'type': '"number"', 'productName': '"twix"', 'quantity': '5'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(5, Product.objects.get(name='twix').quantity)
        self.assertEqual(True, json.loads(response.content)['res'])

    def test_set_price(self):
        response = self.client.post(
            '/stock/',
            {'type': '"price"', 'productName': '"twix"', 'price': 0.6}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0.6, Product.objects.get(name='twix').price)
        self.assertEqual(True, json.loads(response.content)['res'])

    def test_get_all_product(self):
        response = self.client.get('/stock/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.twix, response.context['products'])
