import os

from django.core.mail import EmailMultiAlternatives
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.template.loader import render_to_string

from .models import Order, OrderPayment, OrderItem
from .serializers import OrderSerializer
from apps.product.models import ProductSize, Product
from apps.user.models import Cart, CartItem


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        cart_items = request.data["cart_items"]

        order_amount = 0
        for cart_item_id in cart_items:
            try:
                cart_item_instance = CartItem.objects.get(id=cart_item_id)
                product_size_instance = ProductSize.objects.get(
                    product=cart_item_instance.product,
                    size=cart_item_instance.size,
                )
                if (
                    product_size_instance.size_inventory
                    < cart_item_instance.quantity
                ):
                    return Response(
                        {
                            "message": f"Order quantity exceeded the in stock quantity for {cart_item_instance.product.name}, size {cart_item_instance.size}"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                order_amount += (
                    cart_item_instance.quantity
                    * cart_item_instance.product.price
                )
            except CartItem.DoesNotExist:
                return Response(
                    {"detail": "CartItem does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        request.data["order_amount"] = order_amount
        order = super(OrderViewSet, self).create(request, *args, **kwargs)

        payment_form_data = {
            "amount": int(order.data["order_amount"]),
            "product_service_charge": 0,
            "product_delivery_charge": 100,
            "tax_amount": 0,
            "total_amount": int(order.data["order_amount"])
            + int(order.data["delivery_charge"]),
            "transaction_uuid": order.data["id"],
            "product_code": "EPAYTEST",
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "success_url": "http://localhost:3000/user/payments/payment-success",
            "failure_url": "http://localhost:3000/user/payments/payment-failed",
        }

        response_data = {
            "order": order.data,
            "paymentFormData": payment_form_data,
        }

        merge_data = {
            "ORDER_ID": order.data["id"],
            "CUSTOMER_NAME": request.user.first_name + request.user.last_name,
            "TOTAL_AMOUNT": order.data["order_amount"],
            "ORDER_DATE": order.data["created_at"],
        }
        html_data = render_to_string(
            "order_confirmation_email.html", merge_data
        )
        message = EmailMultiAlternatives(
            subject="Order Confirmation",
            body="order confirmation email",
            from_email=os.environ.get("FROM_EMAIL"),
            to=[request.user.email],
        )
        message.attach_alternative(html_data, "text/html")
        message.send(fail_silently=False)

        return Response(data=response_data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["GET"],
        url_path="order-data",
        url_name="order_data",
    )
    def order_data(self, request, pk=None):
        order = self.get_object()

        response_data = {
            "order_id": order.id,
            "user_email": order.user.email,
            "user_phone": order.user.mobile_no,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["POST"],
        url_path="payment-success",
        url_name="payment-success",
    )
    def payment_success(self, request, pk=None):
        order = self.get_object()

        order.status = "paid"

        order_payment = OrderPayment.objects.get(order_id=order.id)
        order_payment.payment_status = "completed"

        order.save()
        order_payment.save()

        return Response(
            data={"message": "Payment details updated"},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["POST"],
        url_path="payment-failed",
        url_name="payment-failed",
    )
    def payment_failed(self, request, pk=None):
        order = self.get_object()

        order.status = "payment_pending"

        order_payment = OrderPayment.objects.get(order_id=order.id)
        order_payment.payment_status = "failed"

        order.save()
        order_payment.save()

        return Response(
            data={"message": "Payment details updated"},
            status=status.HTTP_200_OK,
        )
