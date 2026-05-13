from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmployeeProfile, Specialization

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional info',
         {'fields': ('middle_name', 'phone_number', 'date_of_birth', 'user_type', 'client_type', 'company_name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional info',
         {'fields': ('middle_name', 'phone_number', 'date_of_birth', 'user_type', 'client_type', 'company_name')}),
    )
    list_display = ('first_name', 'last_name', 'date_of_birth', 'user_type', 'client_type', 'company_name')
    list_filter = ('user_type',)

class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_specializations')

admin.site.register(User, CustomUserAdmin)
admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
admin.site.register(Specialization)