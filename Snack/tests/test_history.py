from django.test import TestCase
from django.contrib.auth.models import User

from Snack.models import Profil, Type, Product, Purchase


class TestHistory(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)

    def test_render(self):
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 200)

    def test_empty_page(self):
        self.type = Type(name="Barre")
        self.type.save()
        self.twix = Product(name="Twix", type=self.type, price=0.6, quantity=10)
        self.twix.save()
        self.purchase1 = Purchase(
            user=self.user,
            product=self.twix,
            number=2,
            price=1.2
        )
        response = self.client.post(
            '/history/?page=2',
        )
        self.assertEqual(response.status_code, 200)
