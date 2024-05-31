from decimal import Decimal

from rest_framework import serializers

from common.uom.models import Uom, UomGroup


class UomGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UomGroup
        fields = ['id', 'guid', 'title']


class UomShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uom
        fields = ['id', 'guid', 'title', 'baseQuantity', 'quantity']


class UomListSerializer(serializers.ModelSerializer):
    uomGroup = UomGroupCreateSerializer()

    class Meta:
        model = Uom
        fields = ['id', 'guid', 'title', 'uomGroup', 'baseQuantity', 'quantity']


class UomCreateSerializer(serializers.ModelSerializer):
    uomGroup = serializers.PrimaryKeyRelatedField(queryset=UomGroup.objects.all(), required=True)

    def validate_baseQuantity(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError('Quantity must be greater than 0.')
        return round(Decimal(value), 6)

    def validate_quantity(self, value):
        if value <= 0 or value is None:
            raise serializers.ValidationError('Quantity must be greater than 0.')
        return round(Decimal(value), 6)

    class Meta:
        model = Uom
        fields = ['id', 'guid', 'title', 'uomGroup', 'baseQuantity', 'quantity']
