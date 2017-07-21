from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Product, Purchase, Type, Profil


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'quantity')


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'number', 'price', 'date', 'debt')


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProfilInLine(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = 'profil'


class UserAdmin(UserAdmin):
    inlines = (ProfilInLine,)


admin.site.register(Product, ProductAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
