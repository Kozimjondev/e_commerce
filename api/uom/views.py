from rest_framework import viewsets

from api.uom.serializers import UomCreateSerializer, UomListSerializer, UomGroupCreateSerializer
from common.uom.models import Uom, UomGroup


class UomGroupViewSet(viewsets.ModelViewSet):
    queryset = UomGroup.objects.all()
    serializer_class = UomGroupCreateSerializer
    lookup_field = 'guid'


class UomViewSet(viewsets.ModelViewSet):
    queryset = Uom.objects.select_related('UomGroup')
    serializer_class = UomCreateSerializer
    lookup_field = 'guid'

    def list(self, request, *args, **kwargs):
        self.serializer_class = UomListSerializer
        return super(UomViewSet, self).list(request, *args, **kwargs)
