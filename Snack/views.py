from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

from Snack.forms import ConnectForm


def connect(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = ConnectForm(request.POST)
            if form.is_valid():
                try:
                    user = authenticate(username=form.data['username'], password=form.data['password'])
                    if user is not None:
                        login(request, user)
                        return HttpResponseRedirect(reverse('connect'))
                    else:
                        messages.add_message(request, messages.ERROR, 'Wrong username or password')
                        return HttpResponseRedirect(reverse('connect'))
                except IntegrityError:
                    messages.add_message(request, messages.ERROR, 'Wrong username or password')
                    return HttpResponseRedirect(reverse('connect'))
            else:
                return HttpResponseRedirect(reverse('connect'))
        else:
            form = ConnectForm()
    return render(request, 'Snack/login.html', locals())
