# Generated by Django 5.1.7 on 2025-03-25 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_alter_product_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='shipping_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
