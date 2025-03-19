"""
  APPLICATION MODELS
"""
import uuid
from django.db import models


PRODUCT_CATEGORIES = (
        ('Vegetable', 'Vegetable'),
        ('Fruits', 'Fruits')
)
class Product(models.Model):
    """Products table"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_image = models.ImageField(blank=True, null=True, upload_to='products/')
    product_price = models.CharField(max_length=10, blank=True, null=True)
    product_weight = models.CharField(max_length=10, blank=True, null=True)
    product_origin = models.CharField(max_length=50, blank=True, null=True)
    product_quality = models.CharField(max_length=20, blank=True, null=True)
    product_check = models.CharField(max_length=20, blank=True, null=True, default='Healthy')
    product_min_weight = models.CharField(max_length=10, blank=True, null=True)
    product_category = models.CharField(max_length=255,
                                          blank=True,
                                          null=True,
                                          choices=PRODUCT_CATEGORIES
                                        )
    product_description = models.TextField(blank=True, null=True)
    product_detail_description = models.TextField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.product_name
