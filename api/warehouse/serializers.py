from decimal import Decimal

from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.product.serializers import ProductShortSerializer
from api.staff.serializers import StaffShortSerializer
from common.product.models import Product
from common.uom.models import Uom
from common.warehouse.models import Warehouse, WarehouseProduct, WarehouseIncomeProduct

User = get_user_model()


class WarehouseProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = ['quantity']


class WarehouseProductCreateSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), required=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Quantity must be greater than 0.')
        return round(value, 6)

    class Meta:
        model = WarehouseProduct
        fields = ['id', 'guid', 'warehouse', 'product', 'quantity']


class WarehouseProductListSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)

    class Meta:
        model = WarehouseProduct
        fields = ['id', 'guid', 'product']


class WarehouseShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'guid', 'title']


class WarehouseCreateSerializer(serializers.ModelSerializer):
    staff = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Warehouse
        fields = ['id', 'guid', 'staff', 'title', ]


class WarehouseListSerializer(serializers.ModelSerializer):
    staff = StaffShortSerializer(many=True)

    class Meta:
        model = Warehouse
        fields = ['id', 'guid', 'title', 'staff']


class WarehouseIncomeProductCreateSerializer(serializers.ModelSerializer):
    warehouseProduct = serializers.PrimaryKeyRelatedField(queryset=WarehouseProduct.objects.all(), required=True)
    uom = serializers.PrimaryKeyRelatedField(queryset=Uom.objects.all(), required=True)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Quantity must be greater than 0.')
        return round(Decimal(value), 6)

    def validate_unitPrice(self, value):
        if value <= 0:
            raise serializers.ValidationError('Unit price must be greater than 0.')
        return round(Decimal(value), 6)

    class Meta:
        model = WarehouseIncomeProduct
        fields = ['id', 'guid', 'warehouseProduct', 'uom', 'quantity', 'unitPrice']
