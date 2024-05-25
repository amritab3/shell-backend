# Generated by Django 4.2.6 on 2024-05-25 14:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0012_instoreproduct_thriftproduct"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("pants", "Pants"),
                    ("shirts", "Shirts"),
                    ("tshirts", "TShirts"),
                    ("dresses", "Dresses"),
                    ("sweaters", "Sweaters"),
                    ("blazers", "Blazers"),
                    ("jackets", "Jackets"),
                    ("others", "Others"),
                ],
                default="",
                max_length=30,
                verbose_name="product_category",
            ),
        ),
    ]
