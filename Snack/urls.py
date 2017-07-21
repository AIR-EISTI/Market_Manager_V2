from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.connect, name='connect'),
    url(r'^purchase/$', views.purchase, name='purchase'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.sign_up, name='signup'),
]
