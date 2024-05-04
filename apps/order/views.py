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
                    {"message": "Quantity exceeded the inventory size"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            remaining_quantity = (
                product_size.size_inventory - product["quantity"]
            )

            product_size.size_inventory = remaining_quantity
            product_size.save()

        return super(OrderViewSet, self).create(request, *args, **kwargs)
