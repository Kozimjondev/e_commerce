from django.db import models
from django.db import transaction
from common.base import BaseModel
from common.category.models import Category
from config.settings.base import env


class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categoryProduct')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    description = models.TextField()
    quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='productProductImage', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='productImage', null=True, blank=True)
    isMain = models.BooleanField(default=False)

    @property
    def imageURL(self):
        if self.product.photo:
            return env.str("BASE_URL") + self.product.photo.url
        return ''

    def __str__(self):
        return f"{self.id}"

    def save(self, *args, **kwargs):
        if self.isMain:
            with transaction.atomic():
                # Set isMain=False for all other images of this product
                ProductImage.objects.filter(product=self.product, isMain=True).update(isMain=False)
        # Save the current instance
        super().save(*args, **kwargs)


