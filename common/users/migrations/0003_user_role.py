# Generated by Django 4.2.13 on 2024-05-15 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_birthday_user_created_at_user_guid_user_photo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'Client'), (3, 'Manager')], default=2),
        ),
    ]
