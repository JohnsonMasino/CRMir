# Generated by Django 4.2.3 on 2023-07-27 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_clientcredits_date_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
