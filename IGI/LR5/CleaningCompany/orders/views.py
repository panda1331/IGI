import logging
from datetime import date
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils import timezone
from services.models import Service

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

# @login_required
# def create_order(request):
#     logger.info('Creating order')
#     if request.user.user_type not in ['client', 'admin'] and not request.user.is_superuser:
#         return redirect('profile')

#     cart = request.session.get('cart', {})
#     if not cart:
#         return redirect('catalog')

#     services = Service.objects.filter(pk__in=cart.keys())
#     cart_items = []
#     total_price = Decimal('0.00')

#     for service in services:
#         quantity = cart.get(str(service.id), 0)
#         item_total = service.price * quantity
#         total_price += item_total
#         cart_items.append({
#             'service': service,
#             'quantity': quantity,
#             'total_price': item_total,
#         })
    
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             client = request.user
#             if request.user.is_superuser or request.user.user_type == 'admin':
#                 client_id = request.POST.get('client')
#                 client = User.objects.get(pk=client_id) if client_id else request.user

#             order = Order.objects.create(
#                 client=client,
#                 address=form.cleaned_data['address'],
#                 work_date=form.cleaned_data['work_date'],
#                 employee=form.cleaned_data['employee'],
#             )

#             order_items = [
#                 OrderItem(
#                     order=order,
#                     service=item['service'],
#                     quantity=item['quantity'],
#                     price=item['service'].price,
#                 )
#                 for item in cart_items
#             ]
#             OrderItem.objects.bulk_create(order_items)

#             # for service_id, quantity in cart.items():
#             #     try:
#             #         service = Service.objects.get(pk=service_id)
#             #         OrderItem.objects.create(
#             #             order=order,
#             #             service=service,
#             #             quantity=quantity,
#             #             price=service.price,
#             #         )
#             #     except Service.DoesNotExist:
#             #         continue

#             # for service, quantity in form.get_services_with_quantity():
#             #     OrderItem.objects.create(
#             #         order=order,
#             #         service=service,
#             #         quantity=quantity,
#             #         price=service.price,
#             #     )
#             promo_code = form.cleaned_data.get('promo_code')
#             today = date.today()
#             active_promo = PromoCode.objects.filter(
#                 code=promo_code,
#                 valid_from__lte=today,
#             ).first()

#             total = order.total_price
#             if active_promo:
#                 discount = Decimal(active_promo.discount_percentage)
#                 total = order.total_price * (Decimal('1') - discount / Decimal('100'))
#                 order.save()

#             print("Total:", order.total_price)
#             Payment.objects.create(
#                 order=order,
#                 amount=total,
#                 status='waiting',
#             )

#             request.session['cart'] = {}
#             request.session.modified = True

#             return redirect('payment', order_id=order.id)
#         else:
#             return render(request, 'orders/create_order.html', {'form': form})
#     else:
#         form = OrderCreateForm()
#         clients = User.objects.filter(user_type='client') if (request.user.is_superuser or request.user.user_type == 'admin') else None
#         return render(request, 'orders/create_order.html', {'form': form, 'clients': clients})

@login_required
def create_order(request):
    logger.info('Creating order')
    if request.user.user_type not in ['client', 'admin'] and not request.user.is_superuser:
        return redirect('profile')

    cart = request.session.get('cart', {})
    if not cart:
        return redirect('catalog')

    services = Service.objects.filter(pk__in=cart.keys())
    cart_items = []
    total_price = Decimal('0.00')

    for service in services:
        quantity = cart.get(str(service.id), 0)
        item_total = service.price * quantity
        total_price += item_total
        cart_items.append({
            'service': service,
            'quantity': quantity,
            'total_price': item_total,
        })

    clients = User.objects.filter(user_type='client') if (request.user.is_superuser or request.user.user_type == 'admin') else None

    if request.method == 'POST':
        form = OrderCreateForm(request.POST, cart = cart)
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

            order_items = []
            total_price = Decimal('0.00')
            for service, quantity in form.get_services_with_quantity():
                order_items.append(
                    OrderItem(
                        order=order,
                        service=service,
                        quantity=quantity,
                        price=service.price,
                    )
                )
                total_price += service.price * quantity

            OrderItem.objects.bulk_create(order_items)

            promo_code = form.cleaned_data.get('promo_code')
            today = date.today()
            active_promo = PromoCode.objects.filter(
                code=promo_code,
                valid_from__lte=today,
            ).first()

            total = total_price
            if active_promo:
                discount = Decimal(active_promo.discount_percentage)
                total = total_price * (Decimal('1') - discount / Decimal('100'))

            Payment.objects.create(
                order=order,
                amount=total,
                status='waiting',
            )

            request.session['cart'] = {}
            request.session.modified = True

            return redirect('payment', order_id=order.id)
    else:
        form = OrderCreateForm(cart=cart)

    context = {
        'form': form,
        'clients': clients,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'orders/create_order.html', context)

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