from django.db.models import Prefetch
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action

from common.product.models import Product
from .permissions import IsOwnerOrAdmin
from .serializers import CartCreateSerializer, \
    CartProductListSerializer, WishlistCreateSerializer, WishlistProductCreateSerializer
from rest_framework.response import Response
from common.cart.models import Cart, CartProduct, Wishlist, WishlistProducts
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


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all().select_related('user')
    serializer_class = WishlistCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'guid'
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        self.queryset = Wishlist.objects.prefetch_related(
            Prefetch(
                lookup='wishlistWishlistProducts',
                queryset=WishlistProducts.objects.select_related('product')
            )
        )
        return super().list(request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def add(self, request, *args, **kwargs):
        product = request.query_params.get('product')
        print(product)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlistProduct = WishlistProducts.objects.filter(wishlist=wishlist, product_id=product).first()
        if wishlistProduct is None:
            wishlistProduct = WishlistProducts.objects.create(wishlist=wishlist, product_id=product)
            print(wishlist)
            wishlistProduct.save()
        else:
            wishlistProduct.delete()
            return Response({"data": "Removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"data": "Added to wishlist"}, status=status.HTTP_201_CREATED)

