from django.db.models import Prefetch, Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.product.serializers import ProductCreateSerializer, ProductListSerializer, ProductDetailSerializer, \
    ProductImageCreateSerializer
from common.comment.models import Comment
from common.product.models import Product, ProductImage


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related(
        Prefetch(
            'productComment', queryset=Comment.objects.select_related('user')
        )).annotate(total_comments=Count('productComment'))
    serializer_class = ProductCreateSerializer
    lookup_field = 'guid'

    # permission_classes = [IsAdminOrReadOnly] # todo: create permission

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.prefetch_related(
            Prefetch(
                lookup='productProductImage',
                queryset=ProductImage.objects.all(),
                to_attr='productImages',
            )
        )
        id = self.request.query_params.get('id', '')
        if id:
            queryset = queryset.filter(id__in=id.split(','))
        return queryset

    def list(self, request, *args, **kwargs):
        self.serializer_class = ProductListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # instance = self.get_object().prefetch_related(
        #     Prefetch(
        #         lookup="productComment",
        #         queryset=Comment.objects.select_related('user'),
        #     )
        # )
        self.serializer_class = ProductDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer
    lookup_field = 'guid'
    permission_classes = [IsAuthenticatedOrReadOnly, ]
