import datetime

from datetime import timedelta
from django.test import TestCase
from django.contrib.auth.models import User, Permission

from Snack.models import Profil, Type, Product, Purchase


class TestSale(TestCase):

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

    def test_page_return_correct_purchase(self):
        today = datetime.date.today() + timedelta(days=int(3))
        start = datetime.date.today() - timedelta(days=int(6))
        response = self.client.get(
            '/sale/?page=1&datepicker_start=' + start.strftime('%m/%d/%Y') +
            '&datepicker_end=' + today.strftime('%m/%d/%Y'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.purchase1, response.context['purchases'].object_list)

    def test_date1_sup_date2_page_return_message_error(self):
        today = datetime.date.today() + timedelta(days=int(1))
        start = datetime.date.today() + timedelta(days=int(6))
        response = self.client.get(
            '/sale/?page=1&datepicker_start=' + start.strftime('%m/%d/%Y') +
            '&datepicker_end=' + today.strftime('%m/%d/%Y'),
        )
        self.assertEqual(response.status_code, 200)
        for message in response.context['messages']:
            self.assertEqual('info', message.tags)
            self.assertEqual(
                'The start date is greater than the end date',
                message.message
            )

    #  def test_date_not_a_date(self):
    #      response = self.client.get(
    #          '/sale/?page=1&datepicker_start=08-21-2017&datepicker_end=08-22-2017'
    #      )
    #      self.assertEqual(response.status_code, 200)
    #      for message in response.context['messages']:
    #          self.assertIn('info', message.tags)
    #          self.assertIn(
    #              'what have you done...',
    #              message.message
    #          )

    def test_no_date(self):
        response = self.client.get(
            '/sale/?page=1&datepicker_start=&datepicker_end=',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.purchase1, response.context['purchases'].object_list)

    def test_no_purchase_selected(self):
        today = datetime.date.today() + timedelta(days=int(3))
        start = datetime.date.today() + timedelta(days=int(2))
        response = self.client.get(
            '/sale/?page=1&datepicker_start=' + start.strftime('%m/%d/%Y') +
            '&datepicker_end=' + today.strftime('%m/%d/%Y'),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, response.context['total'])

    def test_page_not_an_integer(self):
        response = self.client.get(
            '/sale/?page=a&datepicker_start=&datepicker_end=',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, response.context['purchases'].number)

    def test_page_empty(self):
        response = self.client.get(
            '/sale/?page=2&datepicker_start=&datepicker_end=',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, response.context['purchases'].number)
