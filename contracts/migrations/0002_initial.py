# Generated by Django 4.2.3 on 2023-07-26 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contracts', '0001_initial'),
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='invoices.invoice'),
        ),
    ]
