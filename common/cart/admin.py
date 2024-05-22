from django.contrib import admin

from common.cart.models import Cart, CartProduct


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity']

    def name(self, obj):
        return obj.product.name
