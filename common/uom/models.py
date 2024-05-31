from django.db import models

from common.base import BaseModel


class UomGroup(BaseModel):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Uom(BaseModel):
    title = models.CharField(max_length=150)
    uomGroup = models.ForeignKey(UomGroup, related_name='uomGroupUom', on_delete=models.CASCADE)
    baseQuantity = models.DecimalField(default=0, max_digits=20, decimal_places=6)
    quantity = models.DecimalField(default=0, max_digits=50, decimal_places=6)

    def __str__(self):
        return f"{self.title}"
