from django.contrib import admin

from common.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

