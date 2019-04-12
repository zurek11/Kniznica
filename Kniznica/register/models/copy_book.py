from django.db import models
from register.models import Book


class CopyBook(models.Model):
    class Meta:
        db_table = 'copy_book'
        app_label = 'register'
        default_permissions = ()

    borrowed = models.BooleanField()
    book = models.ForeignKey(Book, null=False, on_delete=models.CASCADE, related_name='copies')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
