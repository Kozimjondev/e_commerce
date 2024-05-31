from django.contrib import admin
from common.warehouse.models import Warehouse, WarehouseProduct, WarehouseIncomeProduct, ReceiptProduct, Receipt


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    pass


@admin.register(WarehouseProduct)
class WarehouseProductAdmin(admin.ModelAdmin):
    pass


@admin.register(WarehouseIncomeProduct)
class WarehouseIncomeProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Receipt)
class ReceiptProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ReceiptProduct)
class ReceiptProductAdmin(admin.ModelAdmin):
    pass
