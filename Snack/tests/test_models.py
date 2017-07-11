from django.test import TestCase
from Snack.models import Profil
from django.contrib.auth.models import User


class ProfilTest(TestCase):

    def create_profil(self):
        self.user = User.objects.create(username="user", password="user")
        return Profil.objects.create(user=self.user, card_number="123456")

    def test_profil_creation(self):
        w = self.create_profil()
        self.assertTrue(isinstance(w, Profil))
        self.assertEqual(w.__str__(), str(w.user))
