from django.test import TestCase
from django.contrib.auth.models import User

from Snack.models import Profil, Type, Product


class TestPurchase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)

    def test_method_post(self):
        response = self.client.post(
            '/purchase/',
            {'products': '{"Twix":0, "Mars":1}', 'debt': '"false"'}
        )
        self.assertEqual(response.status_code, 200)

    def test_product_exists(self):
        self.type = Type(name="Barre")
        self.type.save()
        self.twix = Product(name="Twix", type=self.type, price=0.6, quantity=10)
        self.twix.save()
        self.mars = Product(name="Mars", type=self.type, price=0.6, quantity=10)
        self.mars.save()
        response = self.client.post(
            '/purchase/',
            {'products': '{"Twix":0, "Mars":1}', 'debt': '"False"'}
        )
        self.assertEqual(response.status_code, 200)

    def test_no_product(self):
        response = self.client.post(
            '/purchase/',
            {'products': '{}', 'debt': '"false"'}
        )
        self.assertEqual(response.status_code, 200)

    def test_range_product_invalid(self):
        self.type = Type(name="Barre")
        self.type.save()
        self.twix = Product(name="Twix", type=self.type, price=0.6, quantity=10)
        self.twix.save()
        response = self.client.post(
            '/purchase/',
            {'products': '{"Twix":-1}', 'debt': '"false"'}
        )
        self.assertEqual(response.status_code, 200)

    def test_debt(self):
        self.type = Type(name="Barre")
        self.type.save()
        self.twix = Product(name="Twix", type=self.type, price=0.6, quantity=10)
        self.twix.save()
        self.mars = Product(name="Mars", type=self.type, price=0.6, quantity=10)
        self.mars.save()
        response = self.client.post(
            '/purchase/',
            {'products': '{"Twix":0, "Mars":1}', 'debt': '"True"'}
        )
        self.assertEqual(response.status_code, 200)
