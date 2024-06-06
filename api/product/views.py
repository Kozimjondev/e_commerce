from decimal import Decimal
from django.db.models import Prefetch, Count, Sum, F, DecimalField, ExpressionWrapper
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from api.product.serializers import ProductCreateSerializer, ProductListSerializer, ProductDetailSerializer, \
    ProductImageCreateSerializer, ProductShortSerializer
from api.warehouse.serializers import WarehouseShortSerializer
from common.comment.models import Comment
from common.product.models import Product, ProductImage
from common.warehouse.models import Warehouse, WarehouseProduct


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related(
        Prefetch(
            'productComment', queryset=Comment.objects.select_related('user')
        )
    ).annotate(
        total_comments=Count('productComment'),
        total_amount=Sum('productReceiptProduct__totalAmount'),
        total_quantity=Sum('productReceiptProduct__quantity')
    ).annotate(
        calculated_price=ExpressionWrapper(
            F('total_amount') / F('total_quantity'),
            output_field=DecimalField(max_digits=50, decimal_places=6)
        )
    )
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
        self.serializer_class = ProductDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer
    lookup_field = 'guid'
    permission_classes = [IsAuthenticatedOrReadOnly, ]


class RemainingProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related('productWarehouseProduct__warehouse')
    serializer_class = ProductCreateSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.annotate(totalQuantity=Sum('productWarehouseProduct__quantity'))#.prefetch_related(
        #     Prefetch(
        #         lookup='productWarehouseProduct',
        #         queryset=WarehouseProduct.objects.all(),
        #         to_attr='warehouseProduct'
        #     )
        # )
        warehouses = Warehouse.objects.all()
        # products = []
        # totalQuantity = Decimal(0)

        # for product in queryset:
        #     data = {
        #         **ProductShortSerializer(product).data
        #     }
        #     warehouseProducts = {}
        #     totalQuantity = 0

        #     for warehouse in warehouses:
        #         warehouseProducts[f"{warehouse.id}"] = 0
        #         warehouseProduct = WarehouseProduct.objects.filter(warehouse=warehouse, product=product).first()
        #         if warehouseProduct:
        #             warehouseProducts[f"{warehouse.id}"] = warehouseProduct.quantity
        #             totalQuantity += warehouseProduct.quantity
        #     data["totalQuantity"] = totalQuantity
        #     data["warehouseProducts"] = warehouseProducts
        #     products.append(data)
        # payload = {
        #     'warehouses': WarehouseShortSerializer(warehouses, many=True).data,
        #     'products': products
        # }
        serializer = ProductShortSerializer(queryset, many=True, context={"warehouses": warehouses})
        return Response(data={
            'warehouses': WarehouseShortSerializer(warehouses, many=True).data,
            'results': serializer.data,
        })
