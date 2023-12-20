from datetime import datetime

from django.db import models
from clients.models import Client
from products.models import Product
from settings.models import CompanySettings


class Quotation(models.Model):
    quotation_reference = models.CharField(max_length=50, editable=False, unique=True)
    quotation_date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.quotation_reference

    def save(self, *args, **kwargs):
        if not self.quotation_reference:
            settings = CompanySettings.objects.first()
            # Generate the quotation_reference using settings, quotation id, and current date
            self.quotation_reference = f'{settings.quotation_prefix}{self.id}{datetime.datetime.now().strftime("%y%m")}'
        super(Quotation, self).save(*args, **kwargs)


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} - {self.quantity}"
