from django.contrib.auth import get_user_model
from django.db import models

from common.base import BaseModel
from common.product.models import Product

User = get_user_model()


class Comment(BaseModel):
    user = models.ForeignKey(User, related_name='userComment', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='productComment', on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        ordering = ['-created_at']

