# Generated by Django 2.1.8 on 2019-04-04 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_products_add_image_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]