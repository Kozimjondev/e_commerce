from django.db import models

from common.base import BaseModel


class Category(BaseModel):
    title = models.CharField(max_length=250)
    photo = models.ImageField(upload_to='categoryImage', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 blank=True, null=True, related_name='categorySubCategory')
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"
