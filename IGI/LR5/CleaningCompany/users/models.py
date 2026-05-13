from datetime import date
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


def validate_age(value: date):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError("Must be at least 18 years old")

class User(AbstractUser):
    middle_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=19, validators=[RegexValidator(r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$', 'Format: +375 (29) XXX-XX-XX')], blank=True)
    date_of_birth = models.DateField(null=True, blank=True, validators=[validate_age])

    class UserType(models.TextChoices):
        EMPLOYEE = 'employee'
        CLIENT = 'client'
        ADMIN = 'admin'

    class ClientType(models.TextChoices):
        INDIVIDUAL = 'individual'
        LEGAL = 'legal'


    user_type = models.CharField(choices=UserType.choices, max_length=15, default=UserType.CLIENT)
    client_type = models.CharField(choices=ClientType.choices, max_length=15, default=ClientType.INDIVIDUAL)
    company_name = models.CharField(max_length=150, blank=True)

class Specialization(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'employee_profile')
    specializations = models.ManyToManyField(Specialization)

    hire_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='employee_photos')

    def display_specializations(self):
        return ', '.join([specialization.name for specialization in self.specializations.all()])

    def __str__(self):
        return self.user.get_full_name()