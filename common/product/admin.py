from django.contrib import admin
from .models import Product, ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    list_filter = ['category']
    exclude = ['created_at', 'updated_at']

    save_on_top = True


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
