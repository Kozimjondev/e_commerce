from django.contrib import admin

from common.uom.models import Uom, UomGroup


@admin.register(Uom)
class UomAdmin(admin.ModelAdmin):
    pass


@admin.register(UomGroup)
class UomGroupAdmin(admin.ModelAdmin):
    pass

