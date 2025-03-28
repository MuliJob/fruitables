# Generated by Django 5.1.7 on 2025-03-27 15:27

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_name', models.CharField(blank=True, max_length=255, null=True)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='products/')),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_weight', models.CharField(blank=True, max_length=10, null=True)),
                ('product_origin', models.CharField(blank=True, max_length=50, null=True)),
                ('product_quality', models.CharField(blank=True, max_length=20, null=True)),
                ('product_check', models.CharField(blank=True, default='Healthy', max_length=20, null=True)),
                ('product_min_weight', models.CharField(blank=True, max_length=10, null=True)),
                ('product_category', models.CharField(blank=True, choices=[('Vegetable', 'Vegetable'), ('Fruits', 'Fruits')], max_length=255, null=True)),
                ('product_description', models.TextField(blank=True, null=True)),
                ('product_detail_description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total', models.DecimalField(decimal_places=2, max_digits=9)),
                ('quantity', models.IntegerField()),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_quantity', models.IntegerField(default=1)),
                ('shipping_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.cart')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='web.product')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('description', models.CharField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_product', to='web.product')),
            ],
        ),
    ]
