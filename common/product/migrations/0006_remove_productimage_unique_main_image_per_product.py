# Generated by Django 4.2.13 on 2024-05-22 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_productimage_unique_main_image_per_product'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='productimage',
            name='unique_main_image_per_product',
        ),
    ]