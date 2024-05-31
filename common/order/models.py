from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

from common.base import BaseModel
from common.product.models import Product

User = get_user_model()

phone_number_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
)


class Payment(models.IntegerChoices):
    CASH = 1, 'CASH'
    CLICK = 2, 'CLICK'
    PAYME = 3, 'PAYME'


class OrderStatus(models.IntegerChoices):
    PIN = 1, 'Pin'
    WAITING = 2, 'Waiting'
    ON_WAY = 3, 'On way'
    DELIVERED = 4, 'Delivered'


class Address(BaseModel):
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.country} {self.city} {self.street}"


class Order(BaseModel):
    user = models.ForeignKey(User, related_name="userOrder", on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(Address, related_name="addressOrder", on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True, validators=[phone_number_validator])
    comment = models.TextField(null=True, blank=True)
    paymentType = models.IntegerField(choices=Payment.choices, default=Payment.CASH)
    status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.PIN)

    def __str__(self):
        return str(self.id)


class OrderProduct(BaseModel):
    order = models.ForeignKey(Order, related_name="orderOrderProduct", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="productOrderProduct", on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    unitPrice = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    totalAmount = models.DecimalField(max_digits=20, decimal_places=6, default=0)

    def __str__(self):
        return str(self.id)

    # def calculate_total(self):
    #     self.totalAmount = self.quantity * self.unitPrice
    #     return self.totalAmount
    #
    # def save(self, *args, **kwargs):
    #     self.calculate_total()
    #     super().save(*args, **kwargs)

