from django.test import TestCase
from django.contrib.auth.models import User

from Snack.models import Profil, Type, Product, Purchase


class TestSale(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)
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

    def test_form_valid(self):
        response = self.client.post(
            '/sale/?page=1&datepicker_start=11/22/2017&datepicker_end=11/22/2018',
        )
        self.assertEqual(response.status_code, 200)

    def test_date1_sup_date2(self):
        response = self.client.post(
            '/sale/?page=1&datepicker_start=11/22/2018&datepicker_end=11/22/2017',
        )
        self.assertEqual(response.status_code, 200)

    def test_form_invalid(self):
        response = self.client.post(
            '/sale/?page=1&datepicker_start=&datepicker_end=',
        )
        self.assertEqual(response.status_code, 200)

    def test_empty_page(self):
        response = self.client.post(
            '/sale/?page=2',
        )
        self.assertEqual(response.status_code, 200)

    def test_page_not_integer(self):
        response = self.client.post(
            '/sale/?page=a',
        )
        self.assertEqual(response.status_code, 200)
