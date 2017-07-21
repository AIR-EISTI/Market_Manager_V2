from django.test import TestCase
from django.contrib.auth.models import User
from Snack.models import Profil, Type, Product, Purchase


class ProfilTest(TestCase):

    def setUp(self):
        self.type = Type.objects.create(name="Barre chocolatée")
        self.user = User.objects.create(username="user", password="user")
        self.product = Product.objects.create(
            name="Twix", type=self.type,
            price=0.6, quantity=10
        )

    def test_profil_str(self):
        self.profil = Profil.objects.create(user=self.user, card_number="123456")
        self.assertTrue(isinstance(self.profil, Profil))
        self.assertEqual(self.profil.__str__(), str(self.profil.user))

    def test_type_str(self):
        self.assertTrue(isinstance(self.type, Type))
        self.assertEqual(self.type.__str__(), str(self.type.name))

    def test_product_str(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(self.product.__str__(), str(self.product.name))

    def test_purchase_str(self):
        self.purchase = Purchase.objects.create(
            user=self.user, product=self.product, debt=False)
        self.assertTrue(isinstance(self.purchase, Purchase))
        self.assertEqual(self.purchase.__str__(), str(self.purchase.user))
