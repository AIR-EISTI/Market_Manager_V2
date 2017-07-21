import json

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from Snack.forms import ConnectForm, SignUpForm
from Snack.models import Product, Purchase, Profil


def connect(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = ConnectForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.data['username'],
                    password=form.data['password']
                )
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('purchase'))
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'Wrong username or password'
                    )
                    return HttpResponseRedirect(reverse('connect'))
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Wrong username or password'
                )
                return HttpResponseRedirect(reverse('connect'))
        else:
            form = ConnectForm()
        return render(request, 'Snack/login.html', locals())
    else:
        return HttpResponseRedirect(reverse('purchase'))


@csrf_exempt
@login_required
def purchase(request):
    if request.method == 'POST' and request.user.profil.available:
        post = request.POST['products']
        products = json.loads(post)
        if len(products) <= 0:
            messages.add_message(
                request,
                messages.WARNING,
                'Hum... There is no product selected :('
            )
            json_data = json.dumps({'return': False})
        else:
            for product in products:
                if Product.objects.filter(name=product).exists():
                    product_object = Product.objects.get(name=product)
                    nb = products[product]
                    if nb > 0 and nb < product_object.quantity:
                        price = product_object.price * nb
                        Purchase.objects.create(
                            user=request.user,
                            product=product_object,
                            number=nb,
                            price=round(price)).save()
                    elif nb < 0 or nb > product_object.quantity:
                        messages.add_message(
                            request,
                            messages.WARNING,
                            'Good try but it\'s not so simple, try again ! ;)'
                        )
            json_data = json.dumps({'return': True})
        return HttpResponse(json_data)
    else:
        products = Product.objects.all()
        return render(request, 'Snack/purchase.html', {'products': products})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('connect'))


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            if form.data['password'] == form.data['password_verif']:
                user = User.objects.create_user(
                    username=form.data['username'],
                    password=form.data['password'],
                )
                user.last_name = form.data['last_name']
                user.first_name = form.data['first_name'],
                user.save()
                if form.data['card_number']:
                    Profil(
                        user=user,
                        card_number=form.data['card_number']
                    ).save()
                else:
                    Profil(user=user).save()
                login(request, user)
                return HttpResponseRedirect(reverse('purchase'))
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Password and validation password are not the same'
                )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Sign Up Failed'
            )
    else:
        form = SignUpForm()
    return render(request, 'Snack/signup.html', {'form': form})
