from django.db import models

from apps.user.models import User


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


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="product_images", default="", null=True, blank=True
    )

    def __str__(self):
        return self.product.name + " - " + str(self.id)


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


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_cart"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_cart"
    )
    size = models.CharField(
        blank=True, default="", verbose_name="cart_item_size"
    )
    quantity = models.IntegerField(default=1, null=True, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created_at"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")

    def __str__(self):
        return self.product.name + " - " + self.user.email
