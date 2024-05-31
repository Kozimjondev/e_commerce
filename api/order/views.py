from decimal import Decimal
from django.db.models import Prefetch, Count, Sum
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from api.order.serializers import OrderCreateSerializer, OrderProductCreateSerializer, OrderListSerializer
from common.order.models import Order, OrderProduct
from common.product.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related(
        Prefetch(
            'orderOrderProduct', queryset=OrderProduct.objects.select_related('product'),
            to_attr='order_products',
        )
    )
    serializer_class = OrderCreateSerializer
    lookup_field = 'guid'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.query_params.get('user', None)
        if user:
            queryset = queryset.filter(user_id=user)
        queryset = queryset.annotate(quantity=Count('orderOrderProduct'),
                                     orderProductQuantity=Sum('orderOrderProduct__quantity'))
        return queryset

    def list(self, request, *args, **kwargs):
        # self.queryset = self.queryset.annotate(product_count=Count('orderOrderProduct')
        #                                        ).annotate(total_product_amount=Sum('orderOrderProduct__quantity'))
        self.serializer_class = OrderListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.queryset.annotate(product_count=Count('orderOrderProduct')
                                               ).annotate(total_product_amount=Sum('orderOrderProduct__quantity'))
        self.serializer_class = OrderCreateSerializer
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        orderProducts = request.data.get('orderProducts')
        createOrderProducts = []
        validation_messages = []

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        if orderProducts is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for orderProduct in orderProducts:

            product = Product.objects.filter(id=orderProduct.get('product')).first()
            if product is None:
                validation_messages.append(f'Product {orderProduct.get("product")} not found')
                continue

            quantity = orderProduct.get('quantity')
            if quantity is None:
                validation_messages.append(f'Quantity {orderProduct.get("product")} not found')
                continue

            orderProduct['order'] = order.id
            orderProduct['unitPrice'] = product.price
            orderProduct['totalAmount'] = product.price * Decimal(quantity)

            serializer = OrderProductCreateSerializer(data=orderProduct)
            if not serializer.is_valid():
                validation_messages.append(serializer.errors)
                continue

            orderProduct = OrderProduct(**serializer.validated_data)
            createOrderProducts.append(orderProduct)

        if validation_messages:
            order = Order.objects.get(id=order.id)
            order.delete()
            return Response(validation_messages, status=status.HTTP_400_BAD_REQUEST)

        if createOrderProducts:
            OrderProduct.objects.bulk_create(createOrderProducts)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        orderProducts = request.data.get('orderProducts')
        updateOrderProducts = []
        createOrderProducts = []
        validation_messages = []

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if orderProducts is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for orderProduct in orderProducts:
            product = Product.objects.filter(id=orderProduct.get('product')).first()
            if product is None:
                validation_messages.append(f'Product {orderProduct.get("product")} not found')

            quantity = orderProduct.get('quantity')

            if quantity is None:
                validation_messages.append(f'Quantity {orderProduct.get("product")} not found')

            orderProduct['order'] = instance.id
            orderProduct['unitPrice'] = product.price
            orderProduct['totalAmount'] = product.price * Decimal(quantity)

            existing_order_product = OrderProduct.objects.filter(order=instance, product=orderProduct.get('product')
                                                                 ).first()

            if existing_order_product:
                serializer = OrderProductCreateSerializer(existing_order_product, data=orderProduct)
                if not serializer.is_valid():
                    validation_messages.append(serializer.errors)
                    continue
                existing_order_product.save()
                updateOrderProducts.append(existing_order_product)
            else:
                serializer = OrderProductCreateSerializer(data=orderProduct)
                if not serializer.is_valid():
                    validation_messages.append(serializer.errors)
                    continue
                orderProduct = OrderProduct(**serializer.validated_data)
                createOrderProducts.append(orderProduct)

        if validation_messages:
            return Response(validation_messages, status=status.HTTP_400_BAD_REQUEST)

        print(serializer)
        serializer.save()
        print(serializer)
        if updateOrderProducts:
            OrderProduct.objects.bulk_update(updateOrderProducts, ['quantity'])

        if createOrderProducts:
            OrderProduct.objects.bulk_create(createOrderProducts)

        product_ids = [orderProduct['product'] for orderProduct in orderProducts]
        removed_orderProduct = OrderProduct.objects.filter(order=instance).exclude(product__in=product_ids)
        if removed_orderProduct:
            removed_orderProduct.delete()

        return Response({'data': "updated"}, status=status.HTTP_201_CREATED)

    def update1(self, request, *args, **kwargs):
        instance = self.get_object()
        orderProducts = request.data.get('orderProducts')
        updateOrderProducts = []
        createOrderProducts = []
        validation_messages = []

        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        if orderProducts is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for orderProduct in orderProducts:
            product = Product.objects.filter(id=orderProduct.get('product')).first()
            if product is None:
                validation_messages.append(f'Product {orderProduct.get("product")} not found')

            quantity = orderProduct.get('quantity')

            if quantity is None:
                validation_messages.append(f'Quantity {orderProduct.get("product")} not found')

            orderProduct['order'] = instance.id
            orderProduct['unitPrice'] = product.price
            orderProduct['totalAmount'] = product.price * Decimal(quantity)

            obj = OrderProduct.objects.filter(id=orderProduct.get('id'), guid=orderProduct.get('guid')).first()
            if obj is None:
                order_product_serializer = OrderProductCreateSerializer(data=orderProduct)
                if not order_product_serializer.is_valid():
                    validation_messages.append(order_product_serializer.errors)
                    continue

                orderProduct = OrderProduct(**order_product_serializer.validated_data)
                createOrderProducts.append(orderProduct)
                # continue
            else:
                order_product_serializer = OrderProductCreateSerializer(instance=obj, data=orderProduct, partial=True)
                if not order_product_serializer.is_valid():
                    validation_messages.append(order_product_serializer.errors)
                    continue
                orderProduct = order_product_serializer.save()
                updateOrderProducts.append(orderProduct)

        if validation_messages:
            return Response(validation_messages, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        print(updateOrderProducts)
        if updateOrderProducts:
            OrderProduct.objects.bulk_update(updateOrderProducts, ['quantity'])

        if createOrderProducts:
            OrderProduct.objects.bulk_create(createOrderProducts)

        return Response({'data': "updated"}, status=status.HTTP_201_CREATED)
