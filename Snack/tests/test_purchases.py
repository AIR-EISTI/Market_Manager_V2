import json

from django.test import TestCase
from django.contrib.auth.models import User, Permission

from Snack.models import Profil, Type, Product


class TestPurchase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        basic = Permission.objects.get(codename='basic_account')
        member = Permission.objects.get(codename='member_account')
        self.user.user_permissions.add(basic)
        self.user.user_permissions.add(member)
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)
        self.type = Type(name="Barre")
        self.type.save()
        self.twix = Product(name="Twix", type=self.type, price=0.6, quantity=10)
        self.twix.save()
        self.mars = Product(name="Mars", type=self.type, price=0.6, quantity=10)
        self.mars.save()

    def test_no_product_selected(self):
        response = self.client.post(
            '/purchase/',
            {'products': '{}', 'debt': '"false"'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(False, json.loads(response.content)['return'])

    def test_product_selected_sup_0(self):
        response = self.client.post(
            '/purchase/',
            {'products': '{"Twix":2, "Mars":1}', 'debt': '"False"'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, json.loads(response.content)['return'])

    def test_product_selected_range_invalid(self):
        response = self.client.post(
            '/purchase/',
            {'products': '{"Twix":2, "Mars":-1}', 'debt': '"False"'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(True, json.loads(response.content)['return'])
