from rest_framework import serializers
from drf_base64.serializers import Base64ImageField

from api.comment.serializers import CommentListSerializer
from common.product.models import Product, ProductImage
from config.settings.base import env


class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'guid', 'name', 'price']


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
