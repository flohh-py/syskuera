from django.db import models
from django.urls import reverse

PROD_TYPE = [
    ('stock', 'Stockable'),
    ('service', 'Service'),
]

class Product(models.Model):
    code = models.CharField(max_length=50, null=True)
    type = models.CharField(choices=PROD_TYPE, default='stock', null=True, max_length=10)
    price = models.FloatField(default=0.0)
    purchase = models.FloatField(default=0.0)
    descrip = models.CharField(max_length=120)
    qty = models.FloatField(default=0.0)

    def __str__(self):
        return self.code
    
    def get_absolute_url(self):
        # return 'prduct:list', (), {'slug': self.slug}
        return reverse('product:detail', args=[self.id])

    class Meta:
        ordering = ['code']