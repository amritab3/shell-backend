import json

from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend


from .models import Product, PRODUCT_GENDER_CHOICES, PRODUCT_CATEGORY_CHOICES
from .serializers import ProductSerializer
from backend.pagination import CustomPageNumberPagination


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        uploaded_sizes = json.loads(request.data.get("uploaded_sizes"))
        request.data["uploaded_sizes"] = uploaded_sizes

        return super(ProductsViewSet, self).create(request, *args, **kwargs)

    @action(
        detail=False,
        methods=["GET"],
        url_path="product-gender-choice",
        url_name="product-gender-choice",
    )
    def product_gender_choice(self, request):
        gender_choices_list = [
            {"label": label, "value": value}
            for value, label in PRODUCT_GENDER_CHOICES
        ]
        return Response(gender_choices_list)

    @action(
        detail=False,
        methods=["GET"],
        url_path="product-category-choice",
        url_name="product-category-choice",
    )
    def product_category_choice(self, request):
        product_category_list = [
            {"label": label, "value": value}
            for value, label in PRODUCT_CATEGORY_CHOICES
        ]
        return Response(product_category_list)


class InstoreMenProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(type="instore", gender="men")
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["category"]
    ordering_fields = ["name", "price"]


class InstoreWomenProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(type="instore", gender="women").order_by(
        "-created_at"
    )
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["category"]
    ordering_fields = ["name", "price"]


class InstoreKidsProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(type="instore", gender="kids")
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["category"]
    ordering_fields = ["name", "price"]


class ThriftProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(type="thrift")
    serializer_class = ProductSerializer
