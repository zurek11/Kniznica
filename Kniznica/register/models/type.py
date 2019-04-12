from django.db import models


class Type(models.Model):
    class Meta:
        db_table = 'types'
        app_label = 'register'
        default_permissions = ()

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
