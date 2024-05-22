from rest_framework import viewsets

from api.category.serializers import CategoryCreateSerializer, SubCategoryCreateSerializer, CategoryListSerializer, \
    SubCategoryListSerializer
from common.category.models import Category, SubCategory


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer
    lookup_field = 'guid'

    def list(self, request, *args, **kwargs):
        self.serializer_class = CategoryListSerializer
        return super().list(request, *args, **kwargs)


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all().select_related('category')
    serializer_class = SubCategoryCreateSerializer
    lookup_field = 'guid'

    def list(self, request, *args, **kwargs):
        self.serializer_class = SubCategoryListSerializer
        return super().list(request, *args, **kwargs)

