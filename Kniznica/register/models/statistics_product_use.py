from django.db import models
from register.models import Book, Product


class StatisticsProductUse(models.Model):
    class Meta:
        db_table = 'statistics_product_use'
        app_label = 'register'
        default_permissions = ()

    counter = models.IntegerField()
    user = models.ForeignKey(Book, null=False, on_delete=models.CASCADE, related_name='used')
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, related_name='used')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
