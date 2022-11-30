from django.db import models
from store.models import Store

# Create your models here.
class Product(models.Model):
    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        db_table = "Product"
        ordering = ['pk']
        unique_together = ['product_name', 'store']

    product_name = models.CharField(max_length = 100, null = False)
    store = models.ForeignKey(
        Store, on_delete = models.CASCADE, 
        null = False, blank = False,
        related_name = "product_entries")