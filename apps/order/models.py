import uuid
from django.db import models
from datetime import date, timedelta

from apps.product.models import Product
from apps.user.models import User

PAYMENT_METHOD_CHOICES = (
    ("esewa", "ESewa"),
    ("card", "Card"),
)

ORDER_STATUS_CHOICES = (
    ("created", "Created"),
    ("paid", "Paid"),
    ("payment_pending", "Payment Pending"),
    ("cancelled", "Cancelled"),
    ("shipping", "Shipping"),
    ("delivered", "Delivered"),
)

PAYMENT_STATUS_CHOICES = (
    ("pending", "Pending"),
    ("completed", "Completed"),
    ("failed", "Failed"),
)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_amount = models.FloatField(default=0.0, verbose_name="order_amount")
    status = models.CharField(
        max_length=20, default="created", choices=ORDER_STATUS_CHOICES
    )

    delivery_date = models.DateField(default="", verbose_name="delivery_date")
    delivery_charge = models.FloatField(
        default=100.0, verbose_name="delivery_charge"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email + " - " + str(self.id)


class OrderPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment_method = models.CharField(
        max_length=20, default="esewa", choices=PAYMENT_METHOD_CHOICES
    )
    payment_status = models.CharField(
        max_length=20, default="pending", choices=PAYMENT_STATUS_CHOICES
    )
    total_payment_amount = models.FloatField(
        default=0.0, verbose_name="payment_amount"
    )
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Order: " + str(self.order.id)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    amount = models.FloatField(default=0.0, verbose_name="order_amount")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name + " - " + self.order.user.email
