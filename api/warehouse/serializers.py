from decimal import Decimal

from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.product.serializers import ProductShortSerializer
from api.staff.serializers import StaffShortSerializer
from common.order.models import Order
from common.product.models import Product
from common.uom.models import Uom
from common.warehouse.models import Warehouse, WarehouseProduct, WarehouseIncomeProduct, Receipt, ReceiptProduct, \
    WarehouseExpense
from django.db import transaction

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


class WarehouseProductDetailSerializer(serializers.ModelSerializer):
    # product = ProductShortSerializer(read_only=True)

    costPrice = serializers.SerializerMethodField()

    def get_costPrice(self, obj):
        return obj.costPrice

    class Meta:
        model = WarehouseProduct
        fields = ['id', 'guid', 'product', 'uom', 'quantity', 'costPrice']


class WarehouseDetailSerializer(serializers.ModelSerializer):
    warehouseWarehouseProduct = WarehouseProductDetailSerializer(read_only=True, many=True)
    staff = StaffShortSerializer(read_only=True)

    class Meta:
        model = Warehouse
        fields = ['id', 'guid', 'title', 'staff', 'warehouseWarehouseProduct']


class WarehouseIncomeProductCreateSerializer(serializers.ModelSerializer):
    warehouseProduct = serializers.PrimaryKeyRelatedField(queryset=WarehouseProduct.objects.all(), required=True)
    uom = serializers.PrimaryKeyRelatedField(queryset=Uom.objects.all(), required=True)

    def validate_quantity(self, value):
        if value <= 0 or None:
            raise serializers.ValidationError('Quantity must be greater than 0.')
        return round(Decimal(value), 6)

    def validate_unitPrice(self, value):
        if value <= 0 or None:
            raise serializers.ValidationError('Unit price must be greater than 0.')
        return round(Decimal(value), 6)

    class Meta:
        model = WarehouseIncomeProduct
        fields = ['id', 'guid', 'warehouseProduct', 'uom', 'quantity', 'unitPrice']


class ReceiptProductCreateSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), required=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    receipt = serializers.PrimaryKeyRelatedField(queryset=Receipt.objects.all(), required=True)

    def validate_quantity(self, value):
        if value <= 0 or None:
            raise serializers.ValidationError('Quantity must be greater than 0.')
        return round(Decimal(value), 6)

    def validate_unitPrice(self, value):
        if value <= 0 or None:
            raise serializers.ValidationError('Unit price must be greater than 0.')
        return round(Decimal(value), 6)

    class Meta:
        model = ReceiptProduct
        fields = ['id', 'guid', 'warehouse', 'receipt', 'product', 'uom', 'quantity', 'unitPrice', 'totalAmount']


class ReceiptProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptProduct
        fields = ['id', 'guid', 'warehouse', 'receipt', 'product', 'uom', 'quantity', 'unitPrice', 'totalAmount']


class ReceiptCreateSerializer(serializers.ModelSerializer):
    staff = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    products = ReceiptProductCreateSerializer(many=True, read_only=True)

    class Meta:
        model = Receipt
        fields = ['id', 'guid', 'order', 'staff', 'received_date', 'products']


class ReceiptListSerializer(serializers.ModelSerializer):
    staff = StaffShortSerializer()

    class Meta:
        model = Receipt
        fields = ['id', 'guid', 'order', 'staff']


class ReceiptDetailSerializer(serializers.ModelSerializer):
    staff = StaffShortSerializer()
    products = ReceiptProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Receipt
        fields = ['id', 'guid', 'order', 'staff']


class WarehouseExpenseCreateSerializer(serializers.ModelSerializer):
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), required=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=True)

    class Meta:
        model = WarehouseExpense
        fields = ['id', 'guid', 'warehouse', 'order', 'product', 'quantity', 'unitPrice', 'totalAmount']


class ReceiptCreateSerializer1(serializers.ModelSerializer):
    staff = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    receiptReceiptProduct = ReceiptProductCreateSerializer(many=True)

    class Meta:
        model = Receipt
        fields = ['id', 'guid', 'order', 'staff', 'received_date', 'receiptReceiptProduct']
        # depth = 1

    def create(self, validated_data):
        receipt_products_data = validated_data.pop('receiptReceiptProduct')

        with transaction.atomic():
            receipt = Receipt.objects.create(**validated_data)

            for rp_data in receipt_products_data:
                rp_data['receipt'] = receipt

                # Create or update WarehouseProduct
                warehouse_product, created = WarehouseProduct.objects.get_or_create(
                    warehouse=rp_data['warehouse'],
                    product=rp_data['product'],
                    defaults={
                        'uom': rp_data['uom'],
                        'quantity': rp_data['quantity']
                    }
                )
                if not created:
                    warehouse_product.quantity += rp_data['quantity']
                    warehouse_product.save()

                # Calculate totalAmount for WarehouseIncomeProduct
                total_amount = rp_data['quantity'] * rp_data['unitPrice']

                # Create WarehouseIncomeProduct
                WarehouseIncomeProduct.objects.create(
                    warehouse=rp_data['warehouse'],
                    product=rp_data['product'],
                    uom=rp_data['uom'],
                    quantity=rp_data['quantity'],
                    unitPrice=rp_data['unitPrice'],
                    totalAmount=total_amount
                )

                ReceiptProduct.objects.create(**rp_data)

        return receipt
