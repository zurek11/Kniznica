from django.db import models


class Product(models.Model):
    category = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    name = models.CharField(max_length=254)
    publisher = models.CharField(max_length=254)
    author = models.CharField(max_length=150)
    notes = models.CharField(max_length=500)
    date_added = models.DateField
    rating = models.FloatField
    language = models.CharField(max_length=30)
    source = models.CharField(max_length=100)
    used = models.PositiveIntegerField


class Book(models.Model):
    product_id = models.ForeignKey(Product, on_delete=True)
    isbn = models.CharField(max_length=30)
    edition = models.CharField(max_length=50)
    borrowed = models.BooleanField
    published_year = models.PositiveIntegerField
    range = models.CharField(max_length=100)
