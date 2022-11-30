from django.db import models
from product.models import Product
from store.models import Store

class Material(models.Model):
    class Meta:
        verbose_name = "material"
        verbose_name_plural = "materials"
        db_table = "Material"
        ordering = ['pk']
        unique_together = ['material_name', 'store']

    material_name = models.CharField(max_length = 100, blank = False, null = False)
    product = models.ManyToManyField(Product, through = "MaterialQuantity")
    price = models.DecimalField(max_digits = 100, decimal_places = 2, null = False)
    store = models.ForeignKey(Store, on_delete = models.CASCADE, null = False, blank = False, related_name = "material_entries")
    max_capacity = models.PositiveBigIntegerField(null = False, default = 0)
    current_capacity = models.PositiveBigIntegerField(null = False, default = 0)

    def __str__(self):
        return (
            f"""[
                material_name: {self.material_name}, 
                price: {self.price}, 
                product: {self.product},
                store: {self.store}
                ]
            """)

class MaterialQuantity(models.Model):
    class Meta:
        verbose_name = "material_quantity"
        verbose_name_plural = "material_quantities"
        db_table = "Material Quantity"
        ordering = ['pk']
        unique_together = ['material', 'product']

    def __str__(self):
        return f"[material: {self.material}, product: {self.product}, quantity: {self.quantity}]"

    material = models.ForeignKey(Material, on_delete = models.CASCADE, related_name = "material_entries")
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = "product_entries")
    quantity = models.PositiveBigIntegerField()

