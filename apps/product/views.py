from rest_framework import viewsets
import json

from rest_framework.permissions import IsAuthenticated

from .models import Product, Cart
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
