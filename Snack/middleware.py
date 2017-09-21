import datetime
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LocaleMiddleware(MiddlewareMixin):

    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        today = datetime.datetime.today()
        if request.user.is_authenticated:
            print("----------------------------------------")
            print((today - request.user.last_login).seconds)
            print("----------------------------------------")   
            if (today - request.user.last_login).seconds > 120:
                logout(request)
                return HttpResponseRedirect(reverse('connect'))
            else:
                request.user.last_login = today
                request.user.save()
                print((today - request.user.last_login).seconds)
