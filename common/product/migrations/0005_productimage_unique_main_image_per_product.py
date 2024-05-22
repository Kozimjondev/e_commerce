# Generated by Django 4.2.13 on 2024-05-22 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_remove_product_photo_productimage'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='productimage',
            constraint=models.UniqueConstraint(condition=models.Q(('isMain', True)), fields=('product',), name='unique_main_image_per_product'),
        ),
    ]