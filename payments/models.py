from django.db import models

from clients.models import Client
from invoices.models import Invoice
from django.utils import timezone


class PaymentStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Payment Statuses"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, default=None)

    def __str__(self):
        return self.name


class Payment(models.Model):
    # Your existing fields and methods for the Payment model

    RECONCILED_CHOICES = (
        ('unreconciled', 'Unreconciled'),
        ('reconciled', 'Reconciled'),
    )

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(default=timezone.now)
    reconciled_status = models.CharField(max_length=20, choices=RECONCILED_CHOICES, default='unreconciled')

    def __str__(self):
        return f"Payment for Invoice #{self.invoice.id}"


class ClientCredits(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_paid = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Client Credits for {self.client}"
