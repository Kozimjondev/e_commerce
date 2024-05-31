from django.db import models
from django.contrib.auth import get_user_model

from common.base import BaseModel
from common.product.models import Product
from common.uom.models import Uom

User = get_user_model()


class Warehouse(BaseModel):
    staff = models.ManyToManyField(User, related_name='staffWarehouse', null=True, blank=True)
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class WarehouseProduct(BaseModel):
    warehouse = models.ForeignKey(Warehouse, related_name='warehouseWarehouseProduct', on_delete=models.CASCADE,
                                  null=True, blank=True)
    product = models.ForeignKey(Product, related_name='productWarehouseProduct',
                                on_delete=models.CASCADE, null=True, blank=True)
    uom = models.ForeignKey(Uom, related_name='uomWarehouseProduct', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(default=0, max_digits=50, decimal_places=6)

    def __str__(self):
        return f'{self.product} - {self.id}'


class WarehouseIncomeProduct(BaseModel):
    # warehouseProduct = models.ForeignKey(WarehouseProduct, related_name='warehouseProductWarehouseIncomeProduct',
    #                                      on_delete=models.CASCADE, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, related_name='warehouseWarehouseIncomeProduct',
                                  on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='productWarehouseIncomeProduct',
                                on_delete=models.CASCADE, null=True, blank=True)
    uom = models.ForeignKey(Uom, related_name='uomWarehouseIncomeProduct',
                            on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(default=0, max_digits=50, decimal_places=6)
    unitPrice = models.DecimalField(default=0, max_digits=50, decimal_places=6)
    totalAmount = models.DecimalField(default=0, max_digits=50, decimal_places=6)

    def __str__(self):
        return f"{self.id}"


class Receipt(BaseModel):
    order = models.CharField(max_length=150)
    staff = models.ForeignKey(User, related_name='staffReceipt', on_delete=models.CASCADE, null=True, blank=True)
    received_date = models.DateTimeField()


class ReceiptProduct(BaseModel):
    warehouse = models.ForeignKey(Warehouse, related_name='warehouseReceiptProduct',
                                  on_delete=models.CASCADE, null=True, blank=True)
    receipt = models.ForeignKey(Receipt, related_name='receiptReceiptProduct',
                                on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='productReceiptProduct',
                                on_delete=models.CASCADE, null=True, blank=True)
    uom = models.ForeignKey(Uom, related_name='uomReceiptProduct', on_delete=models.SET_NULL, null=True, blank=True)
    totalAmount = models.DecimalField(default=0, max_digits=50, decimal_places=6)
    quantity = models.DecimalField(default=0, max_digits=50, decimal_places=6)
    unitPrice = models.DecimalField(default=0, max_digits=50, decimal_places=6)

    def __str__(self):
        return f"{self.id}"
