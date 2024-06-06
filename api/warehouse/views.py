from decimal import Decimal

from django.db.models import Avg, Prefetch, OuterRef, Sum, Subquery, Q
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from api.warehouse.serializers import WarehouseCreateSerializer, \
    WarehouseProductCreateSerializer, WarehouseIncomeProductCreateSerializer, WarehouseListSerializer, \
    ReceiptCreateSerializer, ReceiptProductCreateSerializer, ReceiptListSerializer, WarehouseDetailSerializer, \
    ReceiptDetailSerializer
from common.product.models import Product
from common.uom.models import Uom
from common.warehouse.models import Warehouse, WarehouseProduct, WarehouseIncomeProduct, ReceiptProduct, Receipt


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = (Warehouse.objects.prefetch_related('staff')
                .prefetch_related('warehouseWarehouseProduct', ))
    serializer_class = WarehouseCreateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'guid'

    def list(self, request, *args, **kwargs):
        self.serializer_class = WarehouseListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Annotate and aggregate ReceiptProduct totals for each WarehouseProduct
        warehouse_products = WarehouseProduct.objects.filter(warehouse=instance
                                                             ).annotate(
            total_amount=Sum('product__productReceiptProduct__totalAmount',
                             filter=Q(product__productReceiptProduct__warehouse=instance)),
            total_quantity=Sum('product__productReceiptProduct__quantity',
                               filter=Q(product__productReceiptProduct__warehouse=instance))
        )

        for wp in warehouse_products:
            if wp.total_amount > 0 and wp.total_quantity > 0:
                wp.costPrice = wp.total_amount / wp.total_quantity
            else:
                wp.costPrice = 0
            wp.save()

        self.serializer_class = WarehouseDetailSerializer
        return super().retrieve(request, *args, **kwargs)


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.select_related('staff').all()
    serializer_class = ReceiptCreateSerializer
    lookup_field = 'guid'

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            Prefetch(
                lookup='receiptReceiptProduct',
                queryset=ReceiptProduct.objects.select_related('product', 'warehouse'),
                to_attr='products'
            )
        )
        return queryset

    def list(self, request, *args, **kwargs):
        self.serializer_class = ReceiptListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ReceiptDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        receipt_products = request.data.get('products')
        validation_messages = []

        if receipt_products is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        receipt = serializer.save()

        create_receipt_products = []
        warehouse_products = []

        for receipt_product in receipt_products:
            receipt_product['receipt'] = receipt.id
            receipt_product_serializer = ReceiptProductCreateSerializer(data=receipt_product)
            if not receipt_product_serializer.is_valid():
                validation_messages.append(receipt_product_serializer.errors)
                continue

            warehouseProduct = WarehouseProduct.objects.filter(warehouse_id=receipt_product.get("warehouse"),
                                                               product_id=receipt_product.get("product")).first()
            if not warehouseProduct:
                warehouseProduct = WarehouseProduct.objects.create(warehouse_id=receipt_product.get('warehouse'),
                                                                   product_id=receipt_product.get('product'))

            obj = WarehouseProduct(id=warehouseProduct.id,
                                   **dict(quantity=warehouseProduct.quantity + receipt_product.get('quantity')))

            warehouse_products.append(obj)

            receipt_product = ReceiptProduct(**receipt_product_serializer.validated_data)
            create_receipt_products.append(receipt_product)

        if validation_messages:
            receipt.delete()
            return Response(validation_messages, status=status.HTTP_400_BAD_REQUEST)

        if create_receipt_products:
            ReceiptProduct.objects.bulk_create(create_receipt_products)

        if warehouse_products:
            WarehouseProduct.objects.bulk_update(warehouse_products, fields=['quantity'])

        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        receipt_products = request.data.get('products')
        validation_messages = []

        if receipt_products is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        create_receipt_products = []
        update_receipt_products = []
        warehouse_products = []

        for receipt_product in receipt_products:
            receipt_product['receipt'] = instance.id

            obj = ReceiptProduct.objects.filter(id=receipt_product.get("id"), guid=receipt_product.get("guid")).first()

            warehouseProduct = WarehouseProduct.objects.filter(warehouse_id=receipt_product.get("warehouse"),
                                                               product_id=receipt_product.get("product")).first()
            if warehouseProduct is None:
                warehouseProduct = WarehouseProduct.objects.create(warehouse_id=receipt_product.get('warehouse'),
                                                                   product_id=receipt_product.get('product'))

            if obj is None:
                receipt_product_serializer = ReceiptProductCreateSerializer(data=receipt_product)

                if not receipt_product_serializer.is_valid():
                    validation_messages.append(receipt_product_serializer.errors)
                    continue

                p = ReceiptProduct(**receipt_product_serializer.validated_data)
                create_receipt_products.append(p)
                diff = receipt_product.get('quantity')
            else:
                diff = round(Decimal(receipt_product.get('quantity', 0)) - obj.quantity, 6)
                receipt_product_serializer = ReceiptProductCreateSerializer(instance=obj, data=receipt_product, partial=True)
                if not receipt_product_serializer.is_valid():
                    validation_messages.append(receipt_product_serializer.errors)
                    continue
                p = ReceiptProduct(id=obj.id, **receipt_product_serializer.validated_data)
                update_receipt_products.append(p)

            data = WarehouseProduct(id=warehouseProduct.id,
                                    **dict(quantity=warehouseProduct.quantity + diff))
            warehouse_products.append(data)

        if validation_messages:
            return Response(validation_messages, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        if update_receipt_products:
            WarehouseProduct.objects.bulk_update(update_receipt_products, fields=['quantity'])

        if warehouse_products:
            WarehouseProduct.objects.bulk_update(warehouse_products, fields=['quantity'])

        if create_receipt_products:
            ReceiptProduct.objects.bulk_create(create_receipt_products)

        return Response(status=status.HTTP_200_OK)









    def create1(self, request, *args, **kwargs):
        receipt_products = request.data.get('receiptReceiptProduct', None)
        create_receipt_products = []
        validation_messages = []

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receipt = serializer.save()

        if receipt_products is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for receipt_product in receipt_products:
            product = Product.objects.filter(id=receipt_product['product']).first()
            warehouse = Warehouse.objects.filter(id=receipt_product['warehouse']).first()
            uom = Uom.objects.filter(id=receipt_product['uom']).first()

            if product is None:
                validation_messages.append(f'Product {receipt_product.get("product")} not found')
                continue

            if warehouse is None:
                validation_messages.append(f"Warehouse {receipt_product['warehouse']} not found")
                continue

            quantity = receipt_product.get('quantity')
            unitPrice = receipt_product.get("unitPrice")

            if quantity is None or unitPrice is None:
                validation_messages.append(f'Quantity {receipt_product.get("quantity")} or '
                                           f'{receipt_product.get("unitPrice")} not valid')

            receipt_product['receipt'] = receipt.id
            receipt_product['uom'] = uom.id
            receipt_product['product'] = product.id
            receipt_product['warehouse'] = warehouse.id

            totalAmount = quantity * unitPrice
            receipt_product_data = {
                'warehouse': receipt_product['warehouse'],
                'receipt': receipt_product['receipt'],
                'product': receipt_product['product'],
                'uom': receipt_product['uom'],
                'quantity': quantity,
                'unitPrice': unitPrice,
                'totalAmount': totalAmount
            }

            receipt_product_serializer = ReceiptProductCreateSerializer(data=receipt_product_data)
            if not receipt_product_serializer.is_valid():
                validation_messages.append(receipt_product_serializer.errors)
                continue

            receipt_product = ReceiptProduct(**receipt_product_serializer.validated_data)
            create_receipt_products.append(receipt_product)

            warehouse_product, created = WarehouseProduct.objects.get_or_create(
                warehouse=warehouse,
                product=product,
                defaults={
                    'uom': uom,
                    'quantity': quantity,
                }
            )
            if not created:
                warehouse_product.quantity += quantity
                warehouse_product.save()

            WarehouseIncomeProduct.objects.create(
                warehouse=warehouse,
                product=product,
                uom=uom,
                quantity=quantity,
                unitPrice=unitPrice,
                totalAmount=totalAmount
            )

        if validation_messages:
            receipt.delete()
            return Response(validation_messages, status=status.HTTP_400_BAD_REQUEST)

        if create_receipt_products:
            ReceiptProduct.objects.bulk_create(create_receipt_products)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update1(self, request, *args, **kwargs):
        instance = self.get_object()
        receipt_products = request.data.get('receiptReceiptProduct')

        create_receipt_products = []
        update_receipt_products = []
        validation_messages = []

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        if receipt_products is None:
            return Response({'receiptReceiptProduct': ['This field is required.']},
                            status=status.HTTP_400_BAD_REQUEST)

        for receipt_product in receipt_products:
            product = Product.objects.filter(id=receipt_product['product']).first()
            warehouse = Warehouse.objects.filter(id=receipt_product['warehouse']).first()
            uom = Uom.objects.filter(id=receipt_product['uom']).first()

            if product is None:
                validation_messages.append(f'Product {receipt_product.get("product")} not found')
            if warehouse is None:
                validation_messages.append(f'Warehouse {receipt_product.get("warehouse")} not found')
            if uom is None:
                continue

            quantity = receipt_product.get('quantity')
            unitPrice = receipt_product.get('unitPrice')

            if quantity is None or unitPrice is None:
                validation_messages.append(f'Quantity {receipt_product.get("quantity")} or '
                                           f'{receipt_product.get("unitPrice")} not valid')

            receipt_product['receipt'] = instance.id
            receipt_product['uom'] = uom.id
            receipt_product['product'] = product.id
            receipt_product['warehouse'] = warehouse.id
            receipt_product['totalAmount'] = Decimal(quantity) * Decimal(unitPrice)
            totalAmount = Decimal(quantity) * Decimal(unitPrice)

            obj = ReceiptProduct.objects.filter(id=receipt_product.get('id'), guid=receipt_product.get('guid')).first()
            if obj is None:
                receipt_product_serializer = ReceiptProductCreateSerializer(data=receipt_product)
                if not receipt_product_serializer.is_valid():
                    validation_messages.append(receipt_product_serializer.errors)
                    continue
                receipt_product = ReceiptProduct(**receipt_product_serializer.validated_data)
                create_receipt_products.append(receipt_product)
            else:
                receipt_product_serializer = ReceiptProductCreateSerializer(instance=obj, data=receipt_product,
                                                                            partial=True)
                if not receipt_product_serializer.is_valid():
                    validation_messages.append(receipt_product_serializer.errors)
                    continue
                receipt_product = receipt_product_serializer.save()
                update_receipt_products.append(receipt_product)

            warehouse_income_product, create = WarehouseIncomeProduct.objects.update_or_create(
                warehouse=warehouse,
                product=product,
                uom=uom,
                quantity=quantity,
                unitPrice=unitPrice,
                totalAmount=totalAmount
            )

            warehouse_product, created = WarehouseProduct.objects.get_or_create(
                warehouse=warehouse,
                product=product,
                defaults={
                    'uom': uom,
                    'quantity': quantity,
                }
            )

            if not created:
                warehouse_product.quantity += warehouse_income_product.quantity
                warehouse_product.save()

        if validation_messages:
            return Response(validation_messages, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        if update_receipt_products:
            ReceiptProduct.objects.bulk_update(update_receipt_products, fields=['quantity', 'unitPrice', ])

        if create_receipt_products:
            ReceiptProduct.objects.bulk_create(create_receipt_products)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReceiptViewSet1(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
