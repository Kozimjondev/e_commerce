from decimal import Decimal

from rest_framework import serializers

from api.product.serializers import ProductShortSerializer
from api.staff.serializers import StaffShortSerializer
from common.order.models import Order, OrderProduct
from common.product.models import Product


class OrderProductCreateSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=True, write_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)

    def validate_quantity(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    def to_internal_value(self, data):
        decimal_fields = ['quantity', 'unitPrice', 'totalAmount']
        # print(data)
        for field in decimal_fields:
            if data.get(field) is not None and data.get(field) != 'null' and data.get(field) != "":
                data[field] = round(Decimal(data[field]), 6)
        # print(data)
        return super().to_internal_value(data)

    class Meta:
        model = OrderProduct
        fields = ['order', 'product', 'quantity', 'unitPrice', 'totalAmount']


class OrderProductListSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer()

    class Meta:
        model = OrderProduct
        fields = ['id', 'guid', 'product', 'quantity', 'unitPrice', 'totalAmount']


class OrderCreateSerializer(serializers.ModelSerializer):
    orderOrderProduct = OrderProductCreateSerializer(many=True, read_only=True)
    product_count = serializers.SerializerMethodField()
    total_product_amount = serializers.SerializerMethodField()

    def get_total_product_amount(self, obj):
        if obj.orderOrderProduct is not None:
            return obj.total_product_amount
        return 0

    def get_product_count(self, obj):
        if obj.orderOrderProduct is not None and hasattr(obj, 'orderOrderProduct'):
            return obj.product_count
        return 0

    class Meta:
        model = Order
        fields = ['id', 'guid', 'user', 'address', 'phone', 'comment', 'paymentType',
                  'status', 'product_count', 'total_product_amount', 'orderOrderProduct']


class OrderListSerializer(serializers.ModelSerializer):
    # orderOrderProduct = OrderProductListSerializer(many=True, read_only=True)
    # product_count = serializers.SerializerMethodField()
    # total_product_amount = serializers.SerializerMethodField()
    user = StaffShortSerializer()
    quantity = serializers.SerializerMethodField()
    orderProductQuantity = serializers.SerializerMethodField()

    order_products = serializers.SerializerMethodField()

    # def get_total_product_amount(self, obj):
    #     if obj.orderOrderProduct is not None:
    #         return obj.total_product_amount
    #     return 0

    def get_order_products(self, obj):
        return OrderProductListSerializer(obj.order_products, many=True).data

    def get_quantity(self, obj):
        if hasattr(obj, 'quantity'):
            return obj.quantity
        return 0

    def get_orderProductQuantity(self, obj):
        if hasattr(obj, 'orderProductQuantity'):
            return obj.orderProductQuantity
        return 0

    # def get_product_count(self, obj):
    #     if obj.orderOrderProduct is not None and hasattr(obj, 'orderOrderProduct'):
    #         return obj.product_count
    #     return 0

    class Meta:
        model = Order
        fields = ['id', 'guid', 'user', 'paymentType', 'quantity', 'orderProductQuantity', 'order_products']
