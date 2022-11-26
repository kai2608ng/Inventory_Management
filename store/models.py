from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Store(models.Model):
    class Meta:
        ordering = ['pk']
        verbose_name = "Store"
        verbose_name_plural = "Stores"
        db_table = "Store"

    store_name = models.CharField(max_length = 100, null = False, blank = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)