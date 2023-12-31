# Generated by Django 4.2.3 on 2023-07-26 21:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('quotations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_date', models.DateField(default=django.utils.timezone.now)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('tax', models.DecimalField(decimal_places=2, default=18, max_digits=3)),
                ('payment_status', models.CharField(default='Pending', max_length=20)),
                ('invoice_notes', models.CharField(default='Payment by deposit to company account only', max_length=300)),
                ('invoice_reference', models.CharField(default='INV<django.db.models.fields.related.ForeignKey>2307', max_length=50)),
                ('quotation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotations.quotation')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.invoice')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
