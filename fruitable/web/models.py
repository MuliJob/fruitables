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
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
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
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        """Returns the string representation of the product"""
        return self.product_name or "Unnamed Product"


class Cart(models.Model):
    """Cart products"""
    cart_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total = models.DecimalField(max_digits=9,decimal_places=2)
    quantity = models.IntegerField()
    # user = models.OneToOneField(User)

    objects = models.Manager()

class CartItem(models.Model):
    """Cart Items"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=1)
    shipping_fee = models.DecimalField(max_digits=9,decimal_places=2, default=50.00)
    # user = models.OneToOneField(User)

    objects = models.Manager()

    @property
    def total_price(self):
        """Getting total price"""
        return (self.product.product_price * self.product_quantity) + self.shipping_fee
