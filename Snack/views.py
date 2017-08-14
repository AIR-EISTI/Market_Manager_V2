import json
import datetime

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Permission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType

from Snack.forms import ConnectForm, SignUpForm, SaleForm
from Snack.models import Product, Purchase, Profil


def connect(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = ConnectForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
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
        debt = json.loads(request.POST['debt'])
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
                    if nb is not None:
                        if nb > 0 and nb <= product_object.quantity:
                            price = product_object.price * nb
                            Purchase.objects.create(
                                user=request.user,
                                product=product_object,
                                number=nb,
                                price=round(price, 2),
                                debt=debt).save()
                            product_object.quantity -= nb
                            product_object.save()
                            if debt:
                                request.user.profil.debt = round(
                                    price + request.user.profil.debt, 2)
                                request.user.profil.save()
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
            if form.cleaned_data['password'] == form.cleaned_data['password_verif']:
                try:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'],
                    )
                    user.last_name = form.cleaned_data['last_name']
                    user.first_name = form.cleaned_data['first_name'],
                    content_type = ContentType.objects.get_for_model(Profil)
                    permission_address = Permission.objects.get(
                        content_type=content_type,
                        codename='basic_account'
                    )
                    user.save()
                    user.user_permissions.add(permission_address)
                    if form.cleaned_data['card_number']:
                        Profil(
                            user=user,
                            card_number=form.cleaned_data['card_number']
                        ).save()
                    else:
                        Profil(user=user).save()
                    login(request, user)
                    return HttpResponseRedirect(reverse('purchase'))
                except IntegrityError:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        "This username already exist... :'("
                    )
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


@csrf_exempt
@login_required
def change_theme(request):
    if request.method == 'POST':
        post = request.POST['color']
        color = json.loads(post)
        request.user.profil.color = color
        request.user.profil.save()
        json_data = json.dumps({'return': True})
        return HttpResponse(json_data)


@login_required
def history(request):
    purchases_all = Purchase.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(purchases_all, 10)
    page = request.GET.get('page')
    try:
        purchases = paginator.page(page)
    except PageNotAnInteger:
        purchases = paginator.page(1)
    except EmptyPage:
        purchases = paginator.page(paginator.num_pages)
    return render(request, 'Snack/history.html', {'purchases': purchases})


@login_required
@permission_required('Snack.treasurer_account')
def sale(request):
    start = ""
    end = ""
    form = SaleForm(request.GET)
    if form.is_valid():
        start = form.cleaned_data['datepicker_start']
        end = form.cleaned_data['datepicker_end']
        try:
            date1 = datetime.datetime.strptime(start, "%m/%d/%Y").date()
            date2 = datetime.datetime.strptime(end, "%m/%d/%Y").date()
            if date1 < date2:
                purchases_all = Purchase.objects.filter(
                    date__date__range=[date1, date2]
                )
            else:
                messages.add_message(
                    request,
                    messages.INFO,
                    'The start date is greater than the end date'
                )
                purchases_all = Purchase.objects.all().order_by('-date')
                date1 = ""
                date2 = ""
        except ValueError:
            messages.add_message(
                request,
                messages.INFO,
                'What have you done...'
            )
            purchases_all = Purchase.objects.all().order_by('-date')
            date1 = ""
            date2 = ""
    else:
        purchases_all = Purchase.objects.all().order_by('-date')
    if purchases_all:
        total = round(purchases_all.aggregate(Sum('price'))['price__sum'], 2)
    else:
        total = 0
    paginator = Paginator(purchases_all, 10)
    page = request.GET.get('page')
    try:
        purchases = paginator.page(page)
    except PageNotAnInteger:
        purchases = paginator.page(1)
    except EmptyPage:
        purchases = paginator.page(paginator.num_pages)
    return render(
        request,
        'Snack/sale.html',
        {'purchases': purchases, 'total': total, 'form': form, 'start': start,
            'end': end}
    )


@csrf_exempt
@login_required
@permission_required('Snack.admin_account')
def permissions(request):
    if request.method == 'POST':
        username = json.loads(request.POST['username'])
        account_type = json.loads(request.POST['type'])
        state = json.loads(request.POST['state'])
        user = User.objects.get(username=username)
        content_type = ContentType.objects.get_for_model(Profil)
        permission_address = Permission.objects.get(
            content_type=content_type,
            codename=account_type + '_account'
        )
        if state:
            user.user_permissions.add(permission_address)
        else:
            user.user_permissions.remove(permission_address)
        user.save()
        json_data = json.dumps({'return': True})
        return HttpResponse(json_data)
    else:
        profils = Profil.objects.all().order_by('user__username')
        return render(request, 'Snack/permissions.html', {'profils': profils})
#
#
#  @csrf_exempt
#  @login_required
#  @permission_required('Snack.admin_account')
#  def account(request):
#      if request.method == 'POST':
#
