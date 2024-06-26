# Generated by Django 4.2.13 on 2024-06-05 07:16

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        ('product', '0006_remove_productimage_unique_main_image_per_product'),
        ('warehouse', '0007_warehouseproduct_costprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarehouseExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
                ('quantity', models.DecimalField(decimal_places=6, default=0, max_digits=50)),
                ('unitPrice', models.DecimalField(decimal_places=6, default=0, max_digits=50)),
                ('totalAmount', models.DecimalField(decimal_places=6, default=0, max_digits=50)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orderWarehouseExpense', to='order.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productWarehouseExpense', to='product.product')),
                ('warehouse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='warehouseWarehouseExpense', to='warehouse.warehouse')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
