import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from payments.models import PromoCode
from .models import Payment

def promo_codes(request):
    all_promo_codes = PromoCode.objects.all()
    return render(request, 'payments/promo_codes.html', {'promo_codes': all_promo_codes})

@login_required
def payment_check(request, order_id):
    try:
        if request.user.is_superuser:
            payment = Payment.objects.get(order_id=order_id)
        else:
            payment = Payment.objects.get(order_id=order_id, order__client=request.user)
    except Payment.DoesNotExist:
        return HttpResponseNotFound("Payment does not exist")
    return render(request, 'payments/payment.html', {'payment': payment})

@login_required
def pay_order(request, order_id):
    if request.user.is_superuser:
        payment = get_object_or_404(Payment, order_id=order_id)
    else:
        payment = get_object_or_404(Payment, order_id=order_id, order__client=request.user)
    if request.method == 'POST':
        payment.status = 'paid'
        payment.payment_method = request.POST.get('payment_method', 'card')
        payment.paid_at = datetime.datetime.now()
        payment.save()

        payment.order.status = 'processing'
        payment.order.save()
        return redirect('profile')
    return redirect('payment', order_id=order_id)