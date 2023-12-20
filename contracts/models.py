# contracts/models.py
from django.db import models
from invoices.models import Invoice


class Contract(models.Model):
    contract_reference = models.CharField(max_length=100, unique=True)
    contract_expiration_date = models.DateField()
    contract_status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired')
    ])
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='contracts')

    def __str__(self):
        return self.contract_reference
