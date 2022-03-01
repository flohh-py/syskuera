# Generated by Django 4.0.1 on 2022-01-17 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_alter_invoiceline_invoice_alter_invoiceline_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='type',
            field=models.CharField(choices=[('sell', 'Sell'), ('purchase', 'Purchase')], default='sell', max_length=10, null=True),
        ),
    ]
