import logging
from datetime import date
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import OrderCreateForm
from .models import Order, OrderItem
from payments.models import Payment, PromoCode
from users.models import User

logger = logging.getLogger(__name__)

@login_required
def orders(request):
    logger.info('Making order')
    now_local = timezone.localtime(timezone.now())
    now_utc = timezone.now()

    user = request.user
    if user.user_type == 'client':
        all_orders = user.orders_as_client.all()
    elif user.user_type == 'employee':
        all_orders = user.orders_as_employee.all()
    else:
        all_orders = Order.objects.all()
    return render(request, 'orders/orders.html', {'orders': all_orders, 'now_local': now_local, 'now_utc': now_utc})

@login_required
def create_order(request):
    logger.info('Creating order')
    if request.user.user_type not in ['client', 'admin'] and not request.user.is_superuser:
        return redirect('profile')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            client = request.user
            if request.user.is_superuser or request.user.user_type == 'admin':
                client_id = request.POST.get('client')
                client = User.objects.get(pk=client_id) if client_id else request.user

            order = Order.objects.create(
                client=client,
                address=form.cleaned_data['address'],
                work_date=form.cleaned_data['work_date'],
                employee=form.cleaned_data['employee'],
            )
            for service, quantity in form.get_services_with_quantity():
                OrderItem.objects.create(
                    order=order,
                    service=service,
                    quantity=quantity,
                    price=service.price,
                )
            promo_code = form.cleaned_data.get('promo_code')
            today = date.today()
            active_promo = PromoCode.objects.filter(
                code=promo_code,
                valid_from__lte=today,
            ).first()

            total = order.total_price
            if active_promo:
                discount = Decimal(active_promo.discount_percentage)
                total = order.total_price * (Decimal('1') - discount / Decimal('100'))
                order.save()

            print("Total:", order.total_price)
            Payment.objects.create(
                order=order,
                amount=total,
                status='waiting',
            )
            return redirect('payment', order_id=order.id)
        else:
            return render(request, 'orders/create_order.html', {'form': form})
    else:
        form = OrderCreateForm()
        clients = User.objects.filter(user_type='client') if (request.user.is_superuser or request.user.user_type == 'admin') else None
        return render(request, 'orders/create_order.html', {'form': form, 'clients': clients})

@user_passes_test(lambda u: u.is_superuser)
def edit_order(request, pk):
    logger.info('Editing order')
    try:
        order = Order.objects.get(pk=pk)
        if request.method == 'POST':
            order.address = request.POST.get('address')
            order.work_date = datetime.strptime(request.POST.get('work_date'), '%Y-%m-%d').date()
            employee_id = request.POST.get('employee')
            order.employee = User.objects.get(pk=employee_id) if employee_id else None
            order.status = request.POST.get('status')
            order.save()
            return redirect('order_list')
        else:
            employees = User.objects.filter(user_type='employee')
            return render(request, 'orders/edit_order.html', {'order': order, 'employees': employees})
    except Order.DoesNotExist:
        logger.error('Order does not exist')
        return HttpResponseNotFound('Order does not exist')

@user_passes_test(lambda u: u.is_superuser)
def delete_order(request, pk):
    logger.info('Deleting order')
    try:
        order = Order.objects.get(pk=pk)
        order.delete()
        print('Order deleted')
        return redirect('order_list')
    except Order.DoesNotExist:
        logger.error('Order does not exist')
        return HttpResponseNotFound('Order does not exist')