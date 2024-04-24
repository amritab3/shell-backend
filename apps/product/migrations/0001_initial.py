# Generated by Django 4.2.6 on 2024-04-24 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=300,
                        verbose_name="product_name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default="",
                        verbose_name="product_description",
                    ),
                ),
                (
                    "price",
                    models.FloatField(
                        default=100.0, verbose_name="product_price"
                    ),
                ),
                (
                    "inventory",
                    models.IntegerField(
                        default=0, verbose_name="product_inventory"
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=50,
                        verbose_name="product_color",
                    ),
                ),
                (
                    "style",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=50,
                        verbose_name="product_style",
                    ),
                ),
                (
                    "material",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=50,
                        verbose_name="product_material",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=30,
                        verbose_name="product_category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductSize",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        blank=True, default="", verbose_name="product_size"
                    ),
                ),
                (
                    "size_inventory",
                    models.IntegerField(
                        default=0, verbose_name="product_size_inventory"
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_sizes",
                        to="product.product",
                    ),
                ),
            ],
        ),
    ]