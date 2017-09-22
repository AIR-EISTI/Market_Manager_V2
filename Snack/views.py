import json
import datetime
import numpy as np

from datetime import timedelta
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

from itertools import groupby

from Snack.forms import ConnectForm, SignUpForm, SaleForm, UpdateAccountForm
from Snack.models import Product, Purchase, Profil, Type

from .tasks import badgeuse


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
@permission_required('Snack.basic_account')
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
        if "version" in request.GET:
            if request.GET["version"] == "notouch":
                types = Type.objects.all()
                products = Product.objects.all()
                return render(request, 'Snack/purchaseNoTouch.html', {'types':types,'products':products})
            
        if "type" in request.GET:
            typeSelect = Type.objects.get(name=request.GET["type"])
            products = Product.objects.filter(type=typeSelect.id)
            types = Type.objects.all()
            return render(request, 'Snack/purchase.html', {'products': products,'types':types,'typeSelect':typeSelect})
        else:
            types = Type.objects.all()
            return render(request, 'Snack/purchaseType.html', {'types':types})
        
        


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('connect'))


@login_required
@permission_required('Snack.admin_account')
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
                    user.first_name = form.cleaned_data['first_name']
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
                    return HttpResponseRedirect(reverse('permissions'))
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
                purchase = Purchase.objects.all().order_by('-date')
                purchases_all = purchase.filter(
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
        except (ValueError, TypeError):
            messages.add_message(
                request,
                messages.info,
                'what have you done...'
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
        form = UpdateAccountForm()
        return render(
            request,
            'Snack/permissions.html',
            {'profils': profils, 'form': form}
        )


@csrf_exempt
@login_required
@permission_required('Snack.admin_account')
def account(request):
    if request.method == 'POST':
        username = json.loads(request.POST['username'])
        profil = Profil.objects.get(user__username=username)
        json_data = json.dumps({
            'username': profil.user.username,
            'first_name': profil.user.first_name,
            'last_name': profil.user.last_name,
            'debt': profil.debt,
            'card_number': profil.card_number,
            'id_user': profil.user.id
        })
        return HttpResponse(json_data)


@login_required
@permission_required('Snack.admin_account')
def update_account(request):
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id_user']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            debt = form.cleaned_data['debt']
            card_number = form.cleaned_data['card_number']
            profil = Profil.objects.get(user__id=id)
            if profil.user.username != username:
                profil.user.username = username
            if profil.user.first_name != first_name:
                profil.user.first_name = first_name
            if profil.user.last_name != last_name:
                profil.user.last_name = last_name
            if profil.debt != debt:
                profil.debt = debt
            if profil.card_number != card_number:
                profil.card_number = card_number
            try:
                profil.user.save()
                profil.save()
            except IntegrityError:
                pass
        return HttpResponseRedirect(reverse('permissions'))


@csrf_exempt
@login_required
@permission_required('Snack.treasurer_account')
def stock(request):
    if request.method == 'POST':
        type_json = json.loads(request.POST['type'])
        product_name = json.loads(request.POST['productName'])
        product = Product.objects.get(name=product_name)
        if type_json == 'number':
            quantity = json.loads(request.POST['quantity'])
            product.quantity = quantity
        elif type_json == 'price':
            price = json.loads(request.POST['price'])
            product.price = price
        product.save()
        json_data = json.dumps({'res': True})
        return HttpResponse(json_data)
    else:
        products = Product.objects.all()
        type = Type.objects.all()
        return render(
            request,
            'Snack/stock.html',
            {'products': products, 'type': type}
        )

@csrf_exempt
@login_required
def heartbeat(request):
    json_data = json.dumps({'res': True})
    return HttpResponse(json_data)


@csrf_exempt
@login_required
@permission_required('Snack.treasurer_account')
def debt(request):
    if request.method == 'POST':
        id_profil = json.loads(request.POST['id'])
        debt = json.loads(request.POST['debt'])
        profil = Profil.objects.get(id=id_profil)
        profil.debt = debt
        profil.save()
        json_data = json.dumps({'res': True})
        return HttpResponse(json_data)
    else:
        profils = Profil.objects.all()
        return render(request, 'Snack/debt.html', {'profils': profils})


def extract_date(entity):
    return entity.date.date()


@login_required
@permission_required('Snack.treasurer_account')
def statistic(request):
    entities = Purchase.objects.order_by('date')
    start = entities[0].date.strftime('%Y-%m-%d')
    end = datetime.datetime.today().strftime('%Y-%m-%d')
    purchase_by_date = []
    for date_purchase, group in groupby(entities, key=extract_date):
        nb_purchase = Purchase.objects.filter(
            date__range=[
                datetime.datetime.combine(date_purchase, datetime.time.min),
                datetime.datetime.combine(date_purchase, datetime.time.max)
            ]
        ).count()
        purchase_by_date.append(
            {
                'x': date_purchase.strftime('%Y-%m-%d'),
                'y': nb_purchase
            }
        )
    return render(
        request,
        'Snack/statistic.html',
        {
            'purchase_by_date': purchase_by_date,
            'start_purchase': start,
            'end': end
        }
    )


def purchase_by_snack(request):
    import matplotlib
    matplotlib.use('Agg')
    from pylab import figure
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    f = figure(figsize=(15, 5))
    days = request.GET['days']
    today = datetime.datetime.today()
    start = datetime.datetime.today() - timedelta(days=int(days))
    purchase = Purchase.objects.filter(date__date__range=[start, today])
    obj = []
    total = []
    products = Product.objects.all()
    for product in products:
        obj.append(product.name)
        purchase_product = purchase.filter(product=product)
        if purchase_product:
            total.append(purchase_product.aggregate(Sum('number'))['number__sum'])
        else:
            total.append(0)
    y_pos = np.arange(len(obj))
    plt.bar(y_pos, total, align='center', alpha=0.5)
    plt.xticks(y_pos, obj)
    plt.ylabel('Quantity')
    str_start = start.strftime('%d-%m-%Y')
    str_today = today.strftime('%d-%m-%Y')
    plt.suptitle('From ' + str_start + ' To ' + str_today)
    canvas = FigureCanvasAgg(f)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


@csrf_exempt
def login_by_badge(request):
    ref = badgeuse()
    user = Profil.objects.filter(card_number=ref)
    if user:
        login(request, user.first().user)
        json_data = json.dumps({'res': True})
    else:
        json_data = json.dumps({'res': False})
    return HttpResponse(json_data)


@csrf_exempt
@login_required
@permission_required('Snack.treasurer_account')
def create_product(request):
    if request.method == 'POST':
        name = json.loads(request.POST['name'])
        price = json.loads(request.POST['price'])
        number = json.loads(request.POST['quantity'])
        type = json.loads(request.POST['type'])
        object_type = Type.objects.get(id=type.split('_')[0])
        Product.objects.create(
            name=name,
            type=object_type,
            price=float(price),
            quantity=int(number)
        ).save()
        json_data = json.dumps({'res': True})
        return HttpResponse(json_data)
