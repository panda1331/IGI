import datetime
import os
import statistics
from collections import defaultdict, Counter

import django.conf.global_settings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.conf import settings

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.shortcuts import render
from services.models import Service
from users.models import User, EmployeeProfile
from orders.models import Order, OrderItem
from payments.models import Payment

@user_passes_test(lambda u: u.is_superuser)
def get_statistics(request):
    services = Service.objects.all().order_by('name')
    clients = User.objects.filter(user_type='client').order_by('last_name', 'first_name')
    employees = EmployeeProfile.objects.select_related('user').order_by('user__last_name', 'user__first_name')
    paid_payments = Payment.objects.filter(status='paid')
    total_income = paid_payments.aggregate(total=Sum('amount'))['total']

    amounts = list(paid_payments.values_list('amount', flat=True))
    payments_mean = statistics.mean(amounts)
    payments_mode = statistics.mode(amounts)
    payments_median = statistics.median(amounts)

    clients_ages = list(datetime.date.today().year - y for y in  clients.values_list('date_of_birth__year', flat=True) if y is not None)
    age_mean = statistics.mean(clients_ages)
    age_median = statistics.median(clients_ages)

    paid_order_items = OrderItem.objects.filter(order__payment__status='paid')
    orders_services = [order_item.service for order_item in paid_order_items]
    popular_service = statistics.mode(orders_services)

    revenues = defaultdict(lambda: 0)
    for item in paid_order_items:
        revenues[item.service] += item.price * item.quantity
    profitable_service = max(revenues, key=revenues.get)

    services_counts = Counter(item.service.name for item in paid_order_items)
    services_names = list(services_counts.keys())
    quantities = list(services_counts.values())
    chart_path = draw_statistics(services_names, quantities)
    return render(request, 'stats/statistics.html', {'services': services, 'clients': clients, 'employees': employees, 'total_income': total_income, 'payments_mean': payments_mean, 'payments_mode': payments_mode, 'payments_median': payments_median, 'age_mean': age_mean, 'age_median': age_median, 'popular_service': popular_service, 'profitable_service': profitable_service, 'chart_path': chart_path})

def draw_statistics(services, quantities):
    plt.figure(figsize=(8, 6))
    plt.pie(quantities, labels=services, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
    plt.title('Distribution of Services')
    plt.axis('equal')

    relative_path = 'charts/service_distribution.png'
    full_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    plt.savefig(full_path)
    plt.close()
    return django.conf.global_settings.MEDIA_URL + relative_path


@user_passes_test(lambda u: u.is_superuser)
def show_planned_works(request):
    orders = Order.objects.filter(status__in=['paid', 'processing']).select_related('client').order_by('work_date')
    grouped = {}
    for order in orders:
        grouped.setdefault(order.client, []).append(order)
    return render(request, 'stats/show_planned_works.html', {'grouped': grouped})

@user_passes_test(lambda u: u.is_superuser)
def client_cost(request):
    clients = User.objects.filter(user_type='client')
    total = None
    if request.method == 'GET' and request.GET.get('client_id'):
        client_id = request.GET.get('client_id')
        start = request.GET.get('start')
        end = request.GET.get('end')
        orders = Order.objects.filter(client=client_id)
        if start:
            orders = orders.filter(work_date__gte=start)
        if end:
            orders = orders.filter(work_date__lte=end)
        total = sum(order.total_price for order in orders)
    return render(request, 'stats/client_cost.html', {'clients': clients, 'total': total})

@user_passes_test(lambda u: u.is_superuser)
def employee_clients(request):
    employees = User.objects.filter(user_type='employee')
    clients = None
    if request.GET.get('employee_id'):
        employee_id = request.GET.get('employee_id')
        client_ids = Order.objects.filter(employee_id=employee_id).values_list('client', flat=True).distinct()
        clients = User.objects.filter(id__in=client_ids)
    return render(request, 'stats/employee_clients.html', {'employees': employees, 'clients': clients})

def examples_view(request):
    return render(request, 'stats/examples.html')