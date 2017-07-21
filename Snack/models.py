from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, default=1)
    card_number = models.CharField(max_length=30, blank=True)
    debt = models.FloatField(default=0)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        permissions = (
            ("basic_account", "Extern User"),
            ("member_account", "Air-Eisti members"),
            ("admin_account", "Administrator"),
        )


class Type(models.Model):
    name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    type = models.ForeignKey(Type, null=False)
    price = models.FloatField()
    quantity = models.IntegerField()
    barcode = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return str(self.name)


class Purchase(models.Model):
    user = models.ForeignKey(User, null=False)
    product = models.ForeignKey(Product, null=False)
    number = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    date = models.DateField(auto_now=True)
    debt = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
