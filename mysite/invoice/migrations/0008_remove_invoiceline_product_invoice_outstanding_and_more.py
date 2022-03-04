# Generated by Django 4.0.2 on 2022-03-02 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_rename_purchase_product_cost'),
        ('partner', '0001_initial'),
        ('invoice', '0007_invoiceline_status_invoiceline_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceline',
            name='product',
        ),
        migrations.AddField(
            model_name='invoice',
            name='outstanding',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='invoice',
            name='pay_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('partial', 'Partial'), ('complete', 'Complete'), ('overdue', 'Overdue')], default='pending', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='qty_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('partial', 'Partial'), ('complete', 'Complete')], default='pending', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_line_item', to='product.product'),
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='qty_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('partial', 'Partial'), ('complete', 'Complete')], default='pending', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='type',
            field=models.CharField(choices=[('sell', 'Sell'), ('purchase', 'Purchase')], default='', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_partner', to='partner.partner'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_line_parent', to='invoice.invoice'),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='qty',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]