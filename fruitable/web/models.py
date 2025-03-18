"""
  APPLICATION MODELS
"""
from django.db import models


PRODUCT_CATEGORIES = (
        ('APPLES', 'Apples'),
        ('ORANGES', 'Oranges'),
        ('STRAWBERRY', 'Strawberry'),
        ('BANANA', 'Banana'),
        ('PUMPKIN', 'Pumpkin'),
        ('VEGETABLE', 'Vegetable')
)
class Product(models.Model):
    """Products table"""
    product_name = models.CharField(max_length=255, blank=True, null=True)
    product_image = models.ImageField(blank=True, null=True, upload_to='products/')
    product_category = models.CharField(max_length=255,
                                          blank=True,
                                          null=True,
                                          choices=PRODUCT_CATEGORIES
                                        )
    product_description = models.TextField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.product_name
