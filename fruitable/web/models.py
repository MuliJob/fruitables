"""
  APPLICATION MODELS
"""
import uuid
from django.db import models
from django.db.models import Avg
from django.conf import settings

from django_ckeditor_5.fields import CKEditor5Field





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

    def get_average_rating(self):
        """Calculate the average rating for this product"""
        avg_rating = self.review_product.aggregate(Avg('star'))['star__avg']
        return round(avg_rating or 0, 1)


class Cart(models.Model):
    """Cart products"""
    cart_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total = models.DecimalField(max_digits=9,decimal_places=2)
    quantity = models.IntegerField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    objects = models.Manager()

class CartItem(models.Model):
    """Cart Items"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=1)
    shipping_fee = models.DecimalField(max_digits=9,decimal_places=2, default=0.00)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    objects = models.Manager()

    def __str__(self):
        """Returns the string representation of the product"""
        return self.product.product_name or "Unnamed Product"

    @property
    def total_price(self):
        """Getting total price"""
        return (self.product.product_price * self.product_quantity) + self.shipping_fee

class Order(models.Model):
    """Order history"""


class Transaction(models.Model):
    """Transaction records"""

class Review(models.Model):
    """Review model"""
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False, null=False)
    description = models.CharField(blank=False)
    star = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=1, blank=True)
    product = models.ForeignKey(Product, related_name='review_product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        """Returns the string representation of the user review"""
        return self.name or "Unnamed"


class Subscriber(models.Model):
    """Subscribed users"""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        """String representation of the email"""
        return self.email


class EmailTemplate(models.Model):
    """Email Templates Model"""
    subject = models.CharField(max_length=255)
    message = CKEditor5Field()
    recipients = models.ManyToManyField(Subscriber)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        """String representation of the subject"""
        return self.subject
