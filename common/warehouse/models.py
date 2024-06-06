from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum

from common.base import BaseModel
from common.order.models import Order
from common.product.models import Product
from common.uom.models import Uom

User = get_user_model()


class Warehouse(BaseModel):
    staff = models.ManyToManyField(User, related_name='staffWarehouse', blank=True)
    title = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.id}"


class WarehouseProduct(BaseModel):
    warehouse = models.ForeignKey(Warehouse, related_name='warehouseWarehouseProduct', on_delete=models.CASCADE,
                                  null=True, blank=True)
    product = models.ForeignKey(Product, related_name='productWarehouseProduct',
                                on_delete=models.CASCADE, null=True, blank=True)
    uom = models.ForeignKey(Uom, related_name='uomWarehouseProduct', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(default=0, max_digits=50, decimal_places=6)
    costPrice = models.DecimalField(default=0, max_digits=50, decimal_places=6)

    def __str__(self):
        return f'{self.product} - {self.product.id}: {self.warehouse.id}-warehouse'


class WarehouseIncomeProduct(BaseModel):
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
    received_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}"


class ReceiptProduct(BaseModel):
    warehouse = models.ForeignKey(Warehouse, related_name='warehouseReceiptProduct',
                                  on_delete=models.CASCADE, null=True, blank=True)
    receipt = models.ForeignKey(Receipt, related_name='receiptReceiptProduct',
                                on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, related_name='productReceiptProduct',
                                on_delete=models.CASCADE, null=True, blank=True)
    uom = models.ForeignKey(Uom, related_name='uomReceiptProduct', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.DecimalField(default=0, max_digits=50, decimal_places=6)
    unitPrice = models.DecimalField(default=0, max_digits=50, decimal_places=6)
    totalAmount = models.DecimalField(default=0, max_digits=50, decimal_places=6)

    def calculate_total(self):
        self.totalAmount = self.quantity * self.unitPrice
        return self.totalAmount

    def save(self, *args, **kwargs):
        self.calculate_total()
        super().save(*args, **kwargs)
        # self.update_warehouse_product_cost()

    # def update_warehouse_product_cost(self):
    #     # Calculate the new cost price for the corresponding WarehouseProduct
    #     warehouse_product = WarehouseProduct.objects.get(warehouse=self.warehouse, product=self.product)
    #     total_amounts = ReceiptProduct.objects.filter(warehouse=self.warehouse, product=self.product).aggregate(Sum('totalAmount'))['totalAmount__sum']
    #     total_quantity = ReceiptProduct.objects.filter(warehouse=self.warehouse, product=self.product).aggregate(Sum('quantity'))['quantity__sum']
    #
    #     if total_quantity:
    #         new_cost_price = total_amounts / total_quantity
    #         warehouse_product.costPrice = new_cost_price
    #         warehouse_product.save()

    def __str__(self):
        return f"{self.id}"


class WarehouseExpense(BaseModel):
    warehouse = models.ForeignKey(Warehouse, related_name='warehouseWarehouseExpense', on_delete=models.SET_NULL,
                                  null=True, blank=True)
    order = models.ForeignKey(Order, related_name='orderWarehouseExpense', on_delete=models.SET_NULL,
                              null=True, blank=True)
    product = models.ForeignKey(Product, related_name='productWarehouseExpense', on_delete=models.SET_NULL,
                                null=True, blank=True)
    quantity = models.DecimalField(default=0, max_digits=50, decimal_places=6)
    unitPrice = models.DecimalField(default=0, max_digits=50, decimal_places=6)
    totalAmount = models.DecimalField(default=0, max_digits=50, decimal_places=6)

    def __str__(self):
        return f"{self.id}"
