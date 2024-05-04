from django.db import models

from apps.product.models import Product
from apps.user.models import User

PAYMENT_METHOD_CHOICES = (
    ("esewa", "ESewa"),
    ("card", "Card"),
)

ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("cancelled", "Cancelled"),
    ("shipping", "Shipping"),
    ("delivered", "Delivered"),
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=20, default="esewa", choices=PAYMENT_METHOD_CHOICES
    )
    amount = models.FloatField(default=0.0, verbose_name="order_amount")
    status = models.CharField(
        max_length=20, default="created", choices=ORDER_STATUS_CHOICES
    )
    products = models.ManyToManyField(Product)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email + " - " + str(self.id)
