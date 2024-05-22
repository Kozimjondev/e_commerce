from rest_framework import serializers
from drf_base64.fields import Base64ImageField
from common.category.models import Category, SubCategory
from config.settings.base import env


class CategoryCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = Category
        fields = ('id', 'guid', 'title', 'photo')


class CategoryListSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        if obj.photo:
            return f"{env.str('BASE_URL')}{obj.photo.url}"
        return ""

    class Meta:
        model = Category
        fields = ('id', 'guid', 'title', 'photo')


class SubCategoryCreateSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)

    def validate(self, attrs):
        category = attrs.get('category')

        # Check if the category is an instance of the Category model
        if isinstance(category, Category):
            category_id = category.id
        else:
            category_id = category

        # Validate the category ID
        if not Category.objects.filter(id=category_id).exists():
            raise serializers.ValidationError({"category": "Category should be chosen"})

        return attrs

    class Meta:
        model = SubCategory
        fields = ('id', 'guid', 'category', 'title')


class SubCategoryListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()

    class Meta:
        model = SubCategory
        fields = ('id', 'guid', 'category', 'title')
