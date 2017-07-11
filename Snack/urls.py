from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.connect, name='connect'),
    url(r'^purchase/$', views.purchase, name='purchase'),
]
