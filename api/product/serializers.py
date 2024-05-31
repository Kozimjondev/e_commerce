from rest_framework import serializers
from drf_base64.serializers import Base64ImageField
# from api.warehouse.serializers import WarehouseProductShortSerializer
from api.comment.serializers import CommentListSerializer
from common.product.models import Product, ProductImage
from common.warehouse.models import Warehouse, WarehouseProduct
from config.settings.base import env


class WarehouseProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseProduct
        fields = ['id', 'quantity', ]


class ProductShortSerializer(serializers.ModelSerializer):
    totalQuantity = serializers.SerializerMethodField()
    warehouse_product_quantity = serializers.SerializerMethodField()
    # warehouseProducts = WarehouseProductShortSerializer(many=True)

    def get_warehouse_product_quantity(self, obj):
        warehouses = self.context['warehouses']
        data = {}
        for warehouse in warehouses:
            warehouse_product = obj.warehouseproducts.filter(warehouse=warehouse.id).first()
            data[warehouse.id] = warehouse_product.quantity if warehouse_product else 0
        return data

    def get_totalQuantity(self, obj):
        if hasattr(obj, 'totalQuantity'):
            return obj.totalQuantity or 0
        return 0

    class Meta:
        model = Product
        fields = ['id', 'guid', 'name', 'warehouse_product_quantity', 'totalQuantity',]# 'warehouseProducts']


class ProductImageListSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, product):
        if product.photo:
            return env.str("BASE_URL") + product.photo.url
        return ''

    class Meta:
        model = ProductImage
        fields = ['id', 'guid', 'photo', 'isMain']


class ProductImageCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)
    id = serializers.IntegerField(read_only=True)
    guid = serializers.CharField(read_only=True)
    isMain = serializers.BooleanField(required=False)

    class Meta:
        model = ProductImage
        fields = ['id', 'guid', 'product', 'photo', 'isMain']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'guid', 'category', 'name', 'price', 'description', 'quantity']


class ProductListSerializer(serializers.ModelSerializer):
    productImages = serializers.SerializerMethodField()

    def get_productImages(self, product):
        if hasattr(product, 'productImages'):
            return ProductImageListSerializer(product.productImages, many=True).data
        return []

    total_comments = serializers.IntegerField(read_only=True)

    # def get_total_comments(self, obj):
    #     return obj.productComment.count() # todo: bu yo`lda duplicate boldi.

    class Meta:
        model = Product
        fields = ['id', 'guid', 'category', 'name', 'price', 'productImages', 'total_comments']


class ProductDetailSerializer(serializers.ModelSerializer):
    productImages = serializers.SerializerMethodField()

    def get_productImages(self, product):
        if hasattr(product, 'productImages'):
            return ProductImageListSerializer(product.productImages, many=True).data
        return []

    productComment = CommentListSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'category', 'name', 'price', 'description', 'quantity',
                  'productImages', 'productComment']
