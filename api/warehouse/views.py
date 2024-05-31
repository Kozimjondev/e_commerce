from django.db.models import Prefetch
from rest_framework import viewsets, permissions

from api.warehouse.serializers import WarehouseCreateSerializer, \
    WarehouseProductCreateSerializer, WarehouseIncomeProductCreateSerializer, WarehouseListSerializer
from common.warehouse.models import Warehouse, WarehouseProduct, WarehouseIncomeProduct


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.prefetch_related('staff')
    serializer_class = WarehouseCreateSerializer
    # permission_classes = [permissions.IsAdminUser]
    lookup_field = 'guid'

    def list(self, request, *args, **kwargs):
        self.serializer_class = WarehouseListSerializer
        return super().list(request, *args, **kwargs)


class WarehouseProductViewSet(viewsets.ModelViewSet):
    queryset = WarehouseProduct.objects.all().select_related('warehouse', 'product')
    serializer_class = WarehouseProductCreateSerializer
    lookup_field = 'guid'
    permission_classes = [permissions.IsAdminUser]


class WarehouseIncomeProductViewSet(viewsets.ModelViewSet):
    queryset = WarehouseIncomeProduct.objects.all().select_related('warehouseProduct', 'uom')
    serializer_class = WarehouseIncomeProductCreateSerializer
    lookup_field = 'guid'
    permission_classes = [permissions.IsAdminUser]
