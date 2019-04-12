from django.contrib.auth.models import User
from django.db import models
from register.models import CopyBook


class Borrow(models.Model):
    class Meta:
        db_table = 'borrow'
        app_label = 'register'
        default_permissions = ()

    copy_book = models.ForeignKey(CopyBook, null=False, on_delete=models.CASCADE, related_name='borrows')
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='borrows')
    expires_at = models.DateTimeField(null=False)
    borrow_at = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
