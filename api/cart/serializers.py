from rest_framework import serializers

from api.product.serializers import ProductShortSerializer
from common.cart.models import Cart, CartProduct


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'guid', 'user')
        read_only_fields = ('id', 'guid')


class CartListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Cart
        fields = ('id', 'guid', 'user')
        read_only_fields = ('id', 'guid')


class CartProductCreateSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(required=False)

    class Meta:
        model = CartProduct
        fields = ['id', 'guid', 'cart', 'product', 'quantity']


class CartProductListSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer()
    totalPrice = serializers.SerializerMethodField()

    def get_totalPrice(self, obj):
        return obj.product.price * obj.quantity

    class Meta:
        model = CartProduct
        fields = ['id', 'guid', 'product', 'quantity', 'totalPrice']
