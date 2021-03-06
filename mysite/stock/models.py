from django.urls import reverse
from django.db import models
from product.models import Product
from invoice.models import Invoice, InvoiceLine
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from main.models import NamingSeries as NS

ENTRY_STATUS = [
    ('draft', 'Draft'),
    ('submitted', 'Submitted'),
    ('cancelled', 'Cancelled'),
]
ENTRY_TYPE = [
    ('transfer', 'Transfer'),
    ('issue', 'Issue'),
    ('delivery', 'Delivery'),
    ('receipt', 'Receipt'),
]

class StockEntry(models.Model):
    code = models.CharField(max_length=10, null=True)
    date = models.DateField(null=True)
    type = models.CharField(choices=ENTRY_TYPE, default='', null=True, max_length=10)
    status = models.CharField(choices=ENTRY_STATUS, default='draft', null=True, max_length=10)
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=12)
    parent = models.ForeignKey(Invoice, related_name='ste_parent', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-code']

    def __str__(self):
        return self.code

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            if self.type == 'transfer':
                self.code = NS.get_series(serie='TSTE')
            if self.type == 'issue':
                self.code = NS.get_series(serie='ISTE')
            if self.type == 'delivery':
                self.code = NS.get_series(serie='DSTE')
            if self.type == 'receipt':
                self.code = NS.get_series(serie='RSTE')
        
        # FIXME dont calculate total fom post_save
        # when ste create from invoice only from save method

        else:
            total = 0
            lines = StockEntryLine.objects.filter(parent=self.id)
            for line in lines:
                total += line.total
            self.total = total
        return super().save(force_insert, force_update, using, update_fields)

    @classmethod
    def submit_stock_entry(cls, id=None):
        if id:
            ste = cls.objects.get(pk=id)
            if StockEntryLine.submit_stock_lines(ste):
                ste.status = 'submitted'
                ste.save()

    @classmethod
    def cancel_stock_entry(cls, id=None):
        if id:
            ste = cls.objects.get(pk=id)
            ste.status = 'cancelled'
            ste.save()

    @classmethod
    def calculate_total(cls, id=None):
        if id:
            total = 0
            lines = StockEntryLine.objects.filter(parent=id)
            for line in lines:
                total += line.total
            ste = cls.objects.get(pk=id)
            ste.total = total
            ste.save()
            

class StockEntryLine(models.Model):
    item = models.ForeignKey(Product, related_name='str_line_item', on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey(StockEntry, related_name='ste_line_parent', on_delete=models.SET_NULL, null=True)
    qty = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    status = models.CharField(choices=ENTRY_STATUS, default='draft', null=True, max_length=10)
    total = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    invo_line = models.ForeignKey(InvoiceLine, related_name='invo_line_parent', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.total = self.qty * self.price
        return super().save(force_insert, force_update, using, update_fields)

    @classmethod
    def submit_stock_lines(cls, parent=None):
        lines = cls.objects.all().filter(parent=parent.id)
        if lines: 
            for line in lines:
                if line.item.type == 'stockable':
                    if line.invo_line:
                        line.invo_line.qty_stock = line.invo_line.qty_stock - line.qty
                        line.invo_line.save()
                        line.invo_line.update_qty_status(line.invo_line)
                    if parent.type == 'receipt':
                        if line.item.update_product_stock(line, type='in'):
                            line.status = 'submitted'
                            line.save()
                    if parent.type == 'delivery':
                        if line.item.update_product_stock(line, type='out'):
                            line.status = 'submitted'
                            line.save()
            return True
        else:
            return False


    @classmethod
    def cancel_stock_lines(cls, parent=None):
        lines = cls.objects.all().filter(parent=parent)
        if lines:
            for line in lines:
                line.status = 'cancelled'
                line.save()
            return True
        else:
            return False

@receiver(post_save, sender=StockEntryLine)
def save_calculate_ste_lines(sender, instance, **kwargs):
    # FIXME dont calculate when create from invoice
    instance.parent.calculate_total(instance.parent.id)

@receiver(post_delete, sender=StockEntryLine)
def delete_calculate_ste_lines(sender, instance, **kwargs):
    instance.parent.calculate_total(instance.parent.id)
