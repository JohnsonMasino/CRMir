from django.db import models
from django import forms


class CompanySettings(models.Model):
    company_name = models.CharField(max_length=100, default='Empire DHV')
    invoice_prefix = models.CharField(max_length=10, default='INV')
    quotation_prefix = models.CharField(max_length=10, default='QUO')
    client_prefix = models.CharField(max_length=10, default='CUS')
    product_prefix = models.CharField(max_length=10, default='PRD')
    default_tax = models.FloatField(max_length=10, default=18)
    default_discount = models.FloatField(max_length=10, default=0)
    payment_terms = models.CharField(max_length=500, default='Payment by deposit to company account only')
    contract_prefix = models.CharField(max_length=10, default='CTR')
    date_format = models.CharField(max_length=10, default='%Y-%m-%d')
    company_account = models.CharField(max_length=100, default='0100123012021')
    company_bank_name = models.CharField(max_length=100, default='BANK ACCOUNT NAME')
    company_address = models.TextField(default='Accra, Ghana')
    company_logo = models.FileField(upload_to='logo/', default='icon.svg')

    user_identifier = models.CharField(max_length=20, default='estate')  # send email via our emailer api
    invoice_theme = models.CharField(max_length=20, default='estate', choices=[
        ('estate', 'estate'),
        ('business', 'business'),
        ('hosting', 'hosting'),
    ])

    def __str__(self):
        return self.company_name


class Role(models.Model):
    name = models.CharField(max_length=40, default='')
    description = models.CharField(max_length=400, default='')

    def __str__(self):
        return self.name
