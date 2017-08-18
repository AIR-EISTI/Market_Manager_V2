from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.connect, name='connect'),
    url(r'^purchase/$', views.purchase, name='purchase'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.sign_up, name='signup'),
    url(r'^change_theme/$', views.change_theme, name='change_theme'),
    url(r'^history/$', views.history, name='history'),
    url(r'^sale/$', views.sale, name='sale'),
    url(r'^permissions/$', views.permissions, name='permissions'),
    url(r'^account/$', views.account, name='account'),
    url(r'^update_account/$', views.update_account, name='update_account'),
    url(r'^stock/$', views.stock, name='stock'),
    url(r'^debt/$', views.debt, name='debt'),
]
