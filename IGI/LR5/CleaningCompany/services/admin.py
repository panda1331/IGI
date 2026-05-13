from django.contrib import admin

from .models import Category, Service

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')

admin.site.register(Category)
admin.site.register(Service, ServiceAdmin)