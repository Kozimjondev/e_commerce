from django.contrib import admin

from common.cart.models import Cart, CartProduct, Wishlist, WishlistProducts


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity']

    def name(self, obj):
        return obj.product.name


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    pass


@admin.register(WishlistProducts)
class WishlistProductsAdmin(admin.ModelAdmin):
    list_display = ['name', 'products']

    def name(self, obj):
        return obj.wishlist

    def products(self, obj):
        return obj.product.id
