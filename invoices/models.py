import datetime

import django
from django.db import models
from django.utils import timezone
from products.models import Product
from quotations.models import Quotation
from quotations.models import QuotationItem
from settings.models import CompanySettings


class Invoice(models.Model):
    settings = CompanySettings()  # () #.objects.first()

    invoice_date = models.DateField(default=django.utils.timezone.now)
    discount = models.DecimalField(default=settings.default_discount, max_digits=3, decimal_places=2)
    tax = models.DecimalField(default=settings.default_tax, max_digits=3, decimal_places=2)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20, default='Pending')
    invoice_notes = models.CharField(max_length=300, default=settings.payment_terms)
    # print(quotation)
    invoice_reference = models.CharField(max_length=50,
                                         default=f'{settings.invoice_prefix}{quotation}{datetime.datetime.now().strftime("%y%m")}')

    def __str__(self):
        return self.invoice_reference


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Reference the Product model directly
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} - {self.quantity}"
