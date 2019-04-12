from django.db import models
from register.models import Category
from register.models import Language
from register.models import Type


class Product(models.Model):
    class Meta:
        db_table = 'products'
        app_label = 'register'
        default_permissions = ()

    title = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=100, null=True)
    notes = models.TextField()
    rating = models.FloatField()
    source = models.CharField(max_length=100)
    url_address = models.CharField(max_length=100)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE, related_name='products')
    type = models.ForeignKey(Type, null=False, on_delete=models.CASCADE, related_name='products')
    language = models.ForeignKey(Language, null=False, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
