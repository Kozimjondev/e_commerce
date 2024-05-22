from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action

from common.product.models import Product
from .serializers import CartCreateSerializer, \
    CartProductListSerializer
from rest_framework.response import Response
from common.cart.models import Cart, CartProduct
from ..product.serializers import ProductListSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartCreateSerializer
    http_method_names = ['get']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartProducts = CartProduct.objects.select_related('product').filter(cart=cart)
        categoryProduct = CartProduct.objects.filter(cart=cart).values('product__category').distinct()
        products = CartProduct.objects.filter(cart=cart).values('product')
        print(products)
        print(categoryProduct)
        similarProducts = Product.objects.filter(category__in=categoryProduct).exclude(pk__in=products).order_by("?")
        response = {
            'data': CartProductListSerializer(cartProducts, many=True).data,
            'similarProducts': ProductListSerializer(similarProducts, many=True).data,
        }
        # return Response(CartProductListSerializer(cartProducts, many=True).data)
        return Response(response)

    @action(methods=['GET'], detail=False)
    def add(self, request, *args, **kwargs):
        product = request.query_params.get('product')
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartProduct = CartProduct.objects.filter(cart=cart, product_id=product).first()
        if cartProduct is None:
            cartProduct = CartProduct.objects.create(cart=cart, product_id=product, quantity=1)
        else:
            cartProduct.quantity += 1
            cartProduct.save()
        return Response({'quantity': cartProduct.quantity})

    @action(methods=['GET'], detail=False)
    def sub(self, request, *args, **kwargs):
        product = request.query_params.get('product')
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartProduct = CartProduct.objects.filter(cart=cart, product_id=product).first()
        if cartProduct is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif cartProduct.quantity == 1:
            cartProduct.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            cartProduct.quantity -= 1
            cartProduct.save()
            return Response({'quantity': cartProduct.quantity})

