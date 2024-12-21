import base64
import io
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from django.core.paginator import Paginator

from datetime import MAXYEAR, MINYEAR, date, datetime
from users.models import Client
from .models import *
from .forms import AccrualForm, BankCardForm, EditCarForm, PaymentForm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 

@login_required
def personal_cabinet(request):
    if request.user.is_staff:
        return redirect('staff-cabinet')
    payments = Payment.objects.filter(client=request.user.client)
    accruals = Accrual.objects.filter(client=request.user.client)
    coupons = CouponClient.objects.filter(
        coupon__start_date__lte=timezone.now().date(),
        coupon__end_date__gte=timezone.now().date(),
        client=request.user.client,
        is_used=False
    ).all()
    data = {
        'payments': payments,
        'accruals': accruals,
        'coupons': coupons,
        'balance': get_balance(request.user.client)
    }
    return render(request, 'system/personal_cabinet.html', data)

@login_required
def staff_cabinet(request):
    if not request.user.is_staff:
        return redirect('no-access')
    payments = Payment.objects.all()
    number_amount = {}
    for payment in payments:
        if payment.number_parking_space in number_amount:
            number_amount[payment.number_parking_space] += payment.total_cost
        else:
            number_amount[payment.number_parking_space] = payment.total_cost
    
    x, y = number_amount.keys(), number_amount.values()
    x_range = range(1, len(x) + 1)
    
    fig, ax = plt.subplots()
    
    ax.bar(x_range, y, width=0.5)
    ax.set_xticks(x_range)
    ax.set_xticklabels(x)

    ax.set_xlabel('Номер парковочного места')
    ax.set_ylabel('Количество денег')
    ax.set_title('Сколько денег приносят парковочные места')

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    
    image = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()
    return render(request, 'system/staff_cabinet.html', {'image': image})


@login_required
def cars(request):
    if request.user.is_staff:
        return redirect('no-access')
    cars = request.user.client.cars.all()
    return render(request, 'system/cars.html', {'cars': cars})


@login_required
def add_car(request, car_id):
    if request.user.is_staff:
        return redirect('no-access')
    
    car = Car.objects.filter(id=car_id).first()
    if request.method == 'POST':
        form = EditCarForm(request.POST)
        if form.is_valid():
            cur_car = form.save(commit=False)
            exist_car = Car.objects.filter(number=cur_car.number).first()
            if exist_car:
                if not car or car.number == exist_car.number:
                    exist_car.name = cur_car.name
                    exist_car.brand = cur_car.brand
                    exist_car.model = cur_car.model
                    exist_car.save()
                    exist_car.clients.add(request.user.client)
                else:
                    return render(request, 'system/add_car.html', {'form': form, 'is_number': True})
            else:
                if not car:
                    cur_car.save()
                    request.user.client.cars.add(cur_car)
                else:
                    car.name = cur_car.name
                    car.brand = cur_car.brand
                    car.model = cur_car.model
                    car.number = cur_car.number
                    car.save()

            return redirect('cars')
    else:
        form = EditCarForm(instance=car) if car else EditCarForm()
    return render(request, 'system/add_car.html', {'form': form})


@login_required
def delete_car(request, car_id):
    if request.user.is_staff or not request.user.client.cars.filter(id=car_id).exists():
        return redirect('no-access')
    car = Car.objects.filter(id=car_id).first()
    car.delete()
    return redirect('cars')


def parking_spaces(request):
    order = request.GET.get('order')
    if order == 'ascending_order':
        parking_spaces = ParkingSpace.objects.all().order_by('cost_per_day')
    elif order == 'descending_order':
        parking_spaces = ParkingSpace.objects.all().order_by('-cost_per_day')
    else:
        parking_spaces = ParkingSpace.objects.all()
        
    paginator = Paginator(parking_spaces, 3) 
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1 
    page_parking_spaces = paginator.get_page(page_number)
    return render(request, 'system/parking_spaces.html', 
                  {'page_parking_spaces': page_parking_spaces, 'number_empty': range(3 - len(page_parking_spaces))})


@login_required
def parking_space(request, number):
    if request.user.is_staff:
        return render(request, 'system/parking_space.html', {'parking_space': parking_space})
    parking_space = ParkingSpace.objects.filter(number=number).first()
    
    new_total_cost = None
    total_cost = None
    coupon_cost = None

    if not parking_space:
        raise Http404()
    if request.method == 'POST':
        action = request.POST.get('action')

        form = PaymentForm(request.user.client, data=request.POST)
        payment = form.save(commit=False)
        days = (payment.reservation_end_date - payment.reservation_start_date).days + 1
        total_cost = days * parking_space.cost_per_day
        new_total_cost = total_cost

        id_coupon_client = request.POST.get('coupon_client')
        if id_coupon_client:
            coupon_client = CouponClient.objects.get(id=id_coupon_client)
        else:
            coupon_client = None
        is_valid_coupon = coupon_client and coupon_client.coupon.min_amount <= total_cost
        if is_valid_coupon:
            coupon = coupon_client.coupon
            if coupon.discount_type == 'percent':
                new_total_cost *= (1 - coupon.discount_value / 100)
            else:
                new_total_cost = max(0, total_cost - coupon.discount_value)
        
        if action == 'calculate':
            coupon_cost = new_total_cost - total_cost
        elif action == 'pay':
            if is_valid_coupon:
                coupon_client.is_used = True
                coupon_client.save()
            else:
                payment.coupon_client = None
            payment.total_cost = new_total_cost
            payment.client = request.user.client
            payment.number_parking_space = parking_space.number
            payment.save()
            parking_space.client = request.user.client
            parking_space.save()
            return redirect('parking-spaces')
    else:
        form = PaymentForm(request.user.client)
    
    data = {
        'parking_space': parking_space,
        'form': form,
        'total_cost': total_cost,
        'new_total_cost': new_total_cost,
        'coupon_cost': coupon_cost
    }
    return render(request, 'system/parking_space.html', data)


@login_required
def accrual(request):
    if request.user.is_staff:
        return redirect('no-access')
    if request.method == 'POST':
        form = AccrualForm(request.user.client, data=request.POST)
        if form.is_valid():
            accrual = form.save(commit=False)
            accrual.client = request.user.client	
            accrual.save()
            return render(request, 'system/success_accrual.html')
    else:
        form = AccrualForm(request.user.client)
    return render(request, 'system/accrual.html', {'form': form})


def client_balance(request):
    if not request.user.is_staff:
        return redirect('no-access')
    
    if request.method == 'POST':
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()

        clients = Client.objects.all()
        client_balance = []
        
        for client in clients:
            accruals = Accrual.objects.filter(client=client, date__gte=start_date, date__lte=end_date)
            payments = Payment.objects.filter(client=client, payment_date__gte=start_date, payment_date__lte=end_date)
            
            total_accruals = _sum(accruals, lambda x: x.amount)
            total_payments = _sum(payments, lambda x: x.total_cost)
            
            total = round(total_accruals - total_payments, 2)
            
            client_balance.append({
                'client': client,
                'total': total
            })
    else:
        start_date = None
        end_date = None
        client_balance = []
    
    return render(request, 'system/client_balance.html', {
        'start_date': start_date,
        'end_date': end_date,
        'client_balance': client_balance
    })


def client_payments(request, client_id):
    if not request.user.is_staff:
        return redirect('no-access')
    
    client = Client.objects.get(id=client_id)
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = date(MINYEAR, 1, 1)

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = date(MAXYEAR, 12, 31)
    
    payments = Payment.objects.filter(client=client, payment_date__gte=start_date, payment_date__lte=end_date)
    data = {
        'payments': payments,
        'client': client,
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'system/client_payments.html', data)



def get_balance(client: Client):
    try:
        payments = client.payment_set.all()
    except Exception:
        payments = []
    try:
        accruals = client.accrual_set.all()
    except Exception:
        accruals = []
    return round(_sum(accruals, lambda x: x.amount) - _sum(payments, lambda x: x.total_cost), 2)


@login_required
def get_coupon(request, coupon_id: int):
    if request.user.is_staff:
        return redirect('no-access')
    coupon = Coupon.objects.get(id=coupon_id)
    
    if not coupon or coupon.price != 0:
        raise Http404()
    coupon_client, created = CouponClient.objects.get_or_create(
        client=request.user.client,
        coupon=coupon,
        #defaults={'is_used': False}
    )
    if created:
        coupon.clients.add(request.user.client)
        return render(request, 'system/success_coupon_add.html', {'coupon': coupon})
    return render(request, 'system/error_coupon_add.html', {'coupon': coupon})

def _sum(arr, func):
    return round(sum(map(func, arr)), 2)



@login_required
def bank_cards(request):
    if request.user.is_staff:
        return redirect('no-access')
    cards = BankCard.objects.filter(client=request.user.client)
    return render(request, 'system/bank_cards.html', {'cards': cards})


@login_required
def add_bank_card(request):
    if request.user.is_staff:
        return redirect('no-access')
    if request.method == 'POST':
        form = BankCardForm(request.POST)
        if form.is_valid():
            bank_card = form.save(commit=False)
            bank_card.client = request.user.client
            bank_card.save()
            return redirect('bank-cards')
    else:
        form = BankCardForm()
    return render(request, 'system/add_bank_card.html', {'form': form})


@login_required
def edit_bank_card(request, card_id):
    if request.user.is_staff:
        return redirect('no-access')
    card = get_object_or_404(BankCard, id=card_id, client=request.user.client)
    if request.method == 'POST':
        form = BankCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect('bank-cards')
    else:
        form = BankCardForm(instance=card)
    return render(request, 'system/edit_bank_card.html', {'form': form})


@login_required
def delete_bank_card(request, card_id):
    if request.user.is_staff:
        return redirect('no-access')
    card = get_object_or_404(BankCard, id=card_id, client=request.user.client)
    if request.method == 'POST':
        card.delete()
        return redirect('bank-cards')
    return render(request, 'system/delete_bank_card.html')