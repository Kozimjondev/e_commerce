from django.contrib.auth import get_user_model
from django.db import models
from common.base import BaseModel
from common.product.models import Product

User = get_user_model()


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="userCart", blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class CartProduct(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             related_name="cartCartProduct", blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="productCartProduct")
    quantity = models.DecimalField(default=0, max_digits=20, decimal_places=6)

    def __str__(self):
        return f"{self.id}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
