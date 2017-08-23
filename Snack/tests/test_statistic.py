import datetime

from django.test import TestCase
from django.contrib.auth.models import User, Permission

from Snack.models import Profil, Type, Product, Purchase


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
        self.purchase1.save()

    def test_statistic_purchase_by_date(self):
        response = self.client.post(
            '/statistic/',
            {'username': '"user2"', 'type': '"basic"', 'state': '1'}
        )
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [{'x': self.purchase1.date.strftime('%Y-%m-%d'), 'y': 1}],
            response.context['purchase_by_date']
        )
        self.assertEqual(today, response.context['start_purchase'])
        self.assertEqual(today, response.context['end'])

    def test_statistic_purchase_by_product(self):
        self.purchase1 = Purchase(
            user=self.user,
            product=self.twix,
            number=2,
            price=1.2
        )
        self.purchase1.save()
        response = self.client.get('/statistic/purchase_by_snack.png?days=7')
        self.assertEqual(response.status_code, 200)
