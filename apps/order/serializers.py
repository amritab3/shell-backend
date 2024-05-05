from rest_framework import serializers

from .models import Order
from apps.product.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "payment_method",
            "amount",
            "status",
            "products",
        ]

    def create(self, validated_data):
        products = validated_data.pop("products")
        order = Order.objects.create(**validated_data)
        order.products.set(products)
        return order
