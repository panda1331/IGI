from django.contrib import admin
from .models import Payment, PromoCode

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order__code' ,'payment_method', 'status', 'amount')
    list_filter = ('status',)

admin.site.register(Payment, PaymentAdmin)
admin.site.register(PromoCode)