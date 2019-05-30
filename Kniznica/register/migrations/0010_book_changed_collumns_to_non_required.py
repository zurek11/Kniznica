# Generated by Django 2.1.8 on 2019-04-11 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0009_book_changed_integer_fields_to_char'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.CharField(max_length=10, null=True),
        ),
    ]