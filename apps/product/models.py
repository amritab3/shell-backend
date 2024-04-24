from django.db import models


class Product(models.Model):
    name = models.CharField(
        max_length=300, blank=True, default="", verbose_name="product_name"
    )
    description = models.TextField(
        blank=True, default="", verbose_name="product_description"
    )
    price = models.FloatField(default=100.000, verbose_name="product_price")
    inventory = models.IntegerField(
        default=0, verbose_name="product_inventory"
    )
    color = models.CharField(
        max_length=50, blank=True, default="", verbose_name="product_color"
    )
    style = models.CharField(
        max_length=50, blank=True, default="", verbose_name="product_style"
    )
    material = models.CharField(
        max_length=50, blank=True, default="", verbose_name="product_material"
    )
    category = models.CharField(
        max_length=30, blank=True, default="", verbose_name="product_category"
    )
    gender = models.CharField(
        max_length=30, blank=True, default="", verbose_name="product_gender"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created_at"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    size = models.CharField(
        blank=True, default="", verbose_name="product_size"
    )
    size_inventory = models.IntegerField(
        default=0, verbose_name="product_size_inventory"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sizes"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created_at"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")

    def __str__(self):
        return self.size + " - " + self.product.name
