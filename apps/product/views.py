from django.shortcuts import render
from rest_framework import viewsets
import json

from .models import Product
from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.
class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        uploaded_sizes = json.loads(request.data.get("uploaded_sizes"))
        request.data["uploaded_sizes"] = uploaded_sizes

        return super(ProductsViewSet, self).create(request, *args, **kwargs)
