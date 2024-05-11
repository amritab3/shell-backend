from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer
from apps.product.models import ProductSize


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        products = request.data["products"]

        product_ids = [product["product"] for product in products]
        request.data["products"] = product_ids

        for product in products:
            product_size = ProductSize.objects.get(
                product=product["product"], size=product["size"]
            )

            if product_size.size_inventory < product["quantity"]:
                return Response(
                    {
                        "message": f"Quantity exceeded the inventory size for {product['product']}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            remaining_quantity = (
                product_size.size_inventory - product["quantity"]
            )

            product_size.size_inventory = remaining_quantity
            product_size.save()

        order = super(OrderViewSet, self).create(request, *args, **kwargs)
        delivery_charge = 100

        payment_form_data = {
            "amount": int(order.data["amount"]),
            "product_service_charge": 0,
            "product_delivery_charge": 100,
            "tax_amount": 0,
            "total_amount": int(order.data["amount"]) + delivery_charge,
            "transaction_uuid": order.data["id"],
            "product_code": "EPAYTEST",
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "success_url": "http://localhost:3000/user/order/payment-success",
            "failure_url": "http://localhost:3000/user/order/payment-failed",
        }

        response_data = {
            "order": order.data,
            "paymentFormData": payment_form_data,
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)
