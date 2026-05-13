import uuid
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum, F
from services.models import Service
from users.models import User


# Create your models here.
class Order(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_as_client', limit_choices_to={'user_type': 'client'})
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_as_employee', null=True, blank=True, limit_choices_to={'user_type': 'employee'})
    address = models.CharField(max_length=120)
    work_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Status(models.TextChoices):
        ISSUED = 'issued'
        PROCESSING = 'processing'
        COMPLETED = 'completed'
        CANCELED = 'canceled'

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ISSUED)

    @property
    def total_price(self):
        result = self.items.aggregate(total=Sum(F('price') * F('quantity')))
        return result['total'] or 0

    def __str__(self):
        return f"Order: {self.code} - {self.client.get_full_name()}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.code} - {self.service.name} x {self.quantity}"