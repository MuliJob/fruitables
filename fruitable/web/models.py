"""
  APPLICATION MODELS
"""
import uuid
from django.db import models


PRODUCT_CATEGORIES = (
        ('Apples', 'Apples'),
        ('Oranges', 'Oranges'),
        ('Strawberries', 'Strawberries'),
        ('Bananas', 'Bananas'),
        ('Pumpkins', 'Pumpkins'),
        ('Vegetables', 'Vegetables')
)
class Product(models.Model):
    """Products table"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_image = models.ImageField(blank=True, null=True, upload_to='products/')
    product_price = models.CharField(max_length=10, blank=True, null=True)
    product_category = models.CharField(max_length=255,
                                          blank=True,
                                          null=True,
                                          choices=PRODUCT_CATEGORIES
                                        )
    product_description = models.TextField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.product_name
