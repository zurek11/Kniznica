# Generated by Django 2.1.8 on 2019-04-04 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_product_publisher_author_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='', upload_to='static/source/image'),
            preserve_default=False,
        ),
    ]