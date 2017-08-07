from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profil(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        default=1
    )
    card_number = models.CharField(
        max_length=30,
        blank=True
    )
    debt = models.FloatField(
        default=0
    )
    available = models.BooleanField(
        default=True
    )
    DEFAULT = 'default'
    BLACK_TER = 'blackter'
    GREY_DARKER = 'greydarker'
    GREY_DARK = 'greydark'
    GREY = 'grey'
    GREY_LIGHT = 'greylight'
    GREY_LIGHTER = 'greylighter'
    WHITE_TER = 'whiteter'
    WHITE_BIS = 'whitebis'
    ORANGE = 'orange'
    GREEN = 'green'
    TURQUOISE = 'turquoise'
    BLUE = 'blue'
    color_choices = (
        (DEFAULT, 'default'),
        (BLACK_TER, 'black-ter'),
        (GREY_DARKER, 'grey-darker'),
        (GREY_DARK, 'grey-dark'),
        (GREY, 'grey'),
        (GREY_LIGHT, 'grey-light'),
        (GREY_LIGHTER, 'grey-lighter'),
        (WHITE_TER, 'white-ter'),
        (WHITE_BIS, 'white-bis'),
        (ORANGE, 'orange'),
        (GREEN, 'green'),
        (TURQUOISE, 'turquoise'),
        (BLUE, 'blue')
    )
    color = models.CharField(
        max_length=12,
        choices=color_choices,
        default=DEFAULT
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        permissions = (
            ("basic_account", "Extern User"),
            ("member_account", "Air-Eisti members"),
            ("admin_account", "Administrator"),
            ("treasurer_account", "Treasurer"),
        )


class Type(models.Model):
    name = models.CharField(
        max_length=30,
        null=False
    )

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True
    )
    type = models.ForeignKey(
        Type,
        null=False
    )
    price = models.FloatField()
    quantity = models.IntegerField()
    barcode = models.CharField(
        max_length=30,
        blank=True
    )

    def __str__(self):
        return str(self.name)


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        null=False
    )
    product = models.ForeignKey(
        Product,
        null=False
    )
    number = models.IntegerField(
        default=0
    )
    price = models.FloatField(
        default=0
    )
    date = models.DateTimeField(
        auto_now=True
    )
    debt = models.BooleanField(
        default=False
    )

    def __str__(self):
        return str(self.user)
