from django.contrib import admin

from .models import Order, OrderItem

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('code', 'client', 'employee', 'address', 'status', 'created_at')
    list_filter = ('status', 'work_date', 'employee')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'service', 'quantity', 'price')
    list_filter = ('service', 'quantity', 'price')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)