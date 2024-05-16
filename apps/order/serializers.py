from rest_framework import serializers
from datetime import date, timedelta

from .models import Order, OrderItem, OrderPayment
from apps.product.models import ProductSize
from apps.user.models import CartItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "amount"]
        extra_kwargs = {"order": {"write_only": True}}


class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = [
            "id",
            "order",
            "payment_method",
            "payment_status",
            "total_payment_amount",
        ]
        extra_kwargs = {"order": {"write_only": True}}


class OrderSerializer(serializers.ModelSerializer):
    payment = OrderPaymentSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    cart_items = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "order_amount",
            "status",
            "payment",
            "items",
            "delivery_charge",
            "delivery_date",
            "cart_items",
        ]

    def create(self, validated_data):
        cart_items = validated_data.pop("cart_items")
        validated_data["delivery_date"] = date.today() + timedelta(days=2)

        order = Order.objects.create(**validated_data)

        for cart_item_id in cart_items:
            try:
                cart_item_instance = CartItem.objects.get(id=cart_item_id)
                product_size_instance = ProductSize.objects.get(
                    product=cart_item_instance.product,
                    size=cart_item_instance.size,
                )

                remaining_quantity = (
                    product_size_instance.size_inventory
                    - cart_item_instance.quantity
                )
                product_size_instance.size_inventory = remaining_quantity
                product_size_instance.save()

                cart_item_instance.delete()

                order_item_price = (
                    cart_item_instance.quantity
                    * cart_item_instance.product.price
                )
                OrderItem.objects.create(
                    order=order,
                    product=cart_item_instance.product,
                    quantity=cart_item_instance.quantity,
                    amount=order_item_price,
                )
            except CartItem.DoesNotExist:
                raise serializers.FieldDoesNotExist("Cart item does not exist")
            except ProductSize.DoesNotExist:
                raise serializers.FieldDoesNotExist(
                    "Product size does not exist"
                )

        OrderPayment.objects.create(
            order=order,
            total_payment_amount=validated_data.get("order_amount"),
        )

        return order
