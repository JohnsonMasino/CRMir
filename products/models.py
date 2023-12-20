from django.db import models


class Product(models.Model):
    product_reference = models.CharField(max_length=10, null=False)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name
