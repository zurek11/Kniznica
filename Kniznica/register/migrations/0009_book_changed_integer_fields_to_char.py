# Generated by Django 2.1.8 on 2019-04-11 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0008_create_book_copy_book_and_statistics_tables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='book',
            name='year',
            field=models.CharField(max_length=10),
        ),
    ]
