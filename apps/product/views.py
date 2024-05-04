from rest_framework import viewsets, status
import json

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartSerializer
from rest_framework.parsers import MultiPartParser, FormParser

from backend.permissions import IsOwner


# Create your views here.
class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        uploaded_sizes = json.loads(request.data.get("uploaded_sizes"))
        request.data["uploaded_sizes"] = uploaded_sizes

        return super(ProductsViewSet, self).create(request, *args, **kwargs)


class MenProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(gender="Men")
    serializer_class = ProductSerializer


class WomenProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(gender="Women")
    serializer_class = ProductSerializer


class KidsProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(gender="Kids")
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        return super(CartViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user)
        return queryset

    def get_object(self):
        obj = Cart.objects.get(user=self.request.user)
        return obj

    @action(
        methods=["post"],
        detail=False,
        url_path="add-item",
        url_name="add-item",
    )
    def add_item_to_cart(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        cart, created = Cart.objects.get_or_create(user=user)

        try:
            product = Product.objects.get(id=data["product"])
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not created:
            cart_item = CartItem.objects.get(
                product=product, cart=cart, size=data["size"]
            )
            cart_item.quantity = data["quantity"]
            cart_item.save()

        else:
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=data["quantity"],
                size=data["size"],
            )

        serializer = CartSerializer(cart)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path="user-cart",
        url_name="user-cart",
    )
    def get_user_cart(self, request, *args, **kwargs):
        user = request.user

        cart = get_object_or_404(Cart, user=user)
        serializer = CartSerializer(cart)

        return Response(
            status=status.HTTP_200_OK, data=serializer.data["cart_items"]
        )
