# Generated by Django 4.2.15 on 2024-08-22 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
    ]
