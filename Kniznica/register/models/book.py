from django.db import models
from register.models import Product


class Book(models.Model):
    class Meta:
        db_table = 'books'
        app_label = 'register'
        default_permissions = ()

    isbn = models.CharField(max_length=100, null=False)
    edition = models.CharField(max_length=10, null=True)
    year = models.CharField(max_length=10, null=True)
    pages = models.CharField(max_length=10, null=True)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
