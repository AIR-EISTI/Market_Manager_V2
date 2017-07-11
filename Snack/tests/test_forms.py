from django.test import TestCase
from django.contrib.auth.models import User

from Snack.forms import ConnectForm


class Setup_Class(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="user@mp.com", password="user")


class Connect_Form_Test(TestCase):

    # coverage run manage.py test -v 2 --cover-html
    # Valid Form Data
    def test_ConnectForm_valid(self):
        form = ConnectForm(data={'username': "user@mp.com", 'password': "user"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_ConnectForm_invalid(self):
        form = ConnectForm(data={'email': "", 'password': "mp"})
        self.assertFalse(form.is_valid())
