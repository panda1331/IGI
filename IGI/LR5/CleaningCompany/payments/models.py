import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from orders.models import Order
from services.models import Service

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Status(models.TextChoices):
        WAITING = "waiting"
        PAID = "paid"
        CANCELED = "canceled"

    status = models.CharField(choices=Status.choices, default=Status.WAITING, max_length=10)

    class PaymentMethod(models.TextChoices):
        CARD = "card"
        CASH = "cash"
        ONLINE = "online"

    payment_method = models.CharField(choices=PaymentMethod.choices, default=PaymentMethod.CARD, max_length=10)
    paid_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Payment order: {self.order.code} - {self.amount} rub."

class PromoCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    discount_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)
    services = models.ManyToManyField(Service, blank=True)

    @property
    def is_active(self):
        return (self.valid_until is None or self.valid_until >= datetime.date.today()) and \
                (self.valid_from is None or self.valid_from <= datetime.date.today())

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}%)"