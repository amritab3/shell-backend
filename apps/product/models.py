import uuid

from django.db import models

PRODUCT_GENDER_CHOICES = (("men", "Men"), ("women", "Women"), ("kids", "Kids"))

PRODUCT_CATEGORY_CHOICES = (
    ("pants", "Pants"),
    ("shirts", "Shirts"),
    ("tshirts", "TShirts"),
    ("dresses", "Dresses"),
    ("sweaters", "Sweaters"),
    ("blazers", "Blazers"),
    ("jackets", "Jackets"),
    ("shoes", "Shoes"),
    ("others", "Others"),
)

PRODUCT_TYPE_CHOICES = (("instore", "Instore"), ("thrift", "Thrift"))

PRODUCT_SIZES_CHOICES = (
    ("xs", "XS"),
    ("s", "S"),
    ("m", "M"),
    ("l", "L"),
    ("xl", "XL"),
    ("xxl", "XXL"),
)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        max_length=30,
        blank=True,
        choices=PRODUCT_CATEGORY_CHOICES,
        default="",
        verbose_name="product_category",
    )
    gender = models.CharField(
        max_length=30,
        blank=True,
        choices=PRODUCT_GENDER_CHOICES,
        default="",
        verbose_name="product_gender",
    )
    type = models.CharField(
        max_length=20,
        blank=True,
        choices=PRODUCT_TYPE_CHOICES,
        default="",
        verbose_name="product_type",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created_at"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="product_images", default="", null=True, blank=True
    )

    def __str__(self):
        return self.product.name + " - " + str(self.id)


class ProductSize(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.CharField(
        blank=True,
        default="",
        verbose_name="product_size",
        choices=PRODUCT_SIZES_CHOICES,
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
