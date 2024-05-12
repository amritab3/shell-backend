import json

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend


from .models import (
    Product,
    PRODUCT_GENDER_CHOICES,
    PRODUCT_CATEGORY_CHOICES,
    PRODUCT_SIZES_CHOICES,
)
from .serializers import ProductSerializer, ThriftProductSerializer
from backend.pagination import CustomPageNumberPagination


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(type="instore").order_by("-created_at")
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["category"]
    ordering_fields = ["name", "price"]
    search_fields = ["name"]

    def create(self, request, *args, **kwargs):
        uploaded_sizes = json.loads(request.data.get("uploaded_sizes"))

        if not uploaded_sizes:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Please  provide the sizes"},
            )

        request.data._mutable = True
        request.data["uploaded_sizes"] = uploaded_sizes
        request.data["type"] = "instore"
        request.data._mutable = False

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

    @action(
        detail=False,
        methods=["GET"],
        url_path="product-size-choice",
        url_name="product-size-choice",
    )
    def product_size_choice(self, request):
        product_size_list = [
            {"label": label, "value": value}
            for value, label in PRODUCT_SIZES_CHOICES
        ]
        return Response(product_size_list)


class InstoreMenProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(type="instore", gender="men")
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["category"]
    ordering_fields = ["name", "price"]
    search_fields = ["name"]


class InstoreWomenProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(type="instore", gender="women").order_by(
        "-created_at"
    )
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["category"]
    ordering_fields = ["name", "price"]
    search_fields = ["name"]


class InstoreKidsProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(type="instore", gender="kids")
    serializer_class = ProductSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["category"]
    ordering_fields = ["name", "price"]
    search_fields = ["name"]


class ThriftProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(type="thrift").order_by("-created_at")
    serializer_class = ThriftProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["category"]
    ordering_fields = ["name", "price"]
    search_fields = ["name"]

    def create(self, request, *args, **kwargs):
        uploaded_sizes = json.loads(request.data.get("uploaded_sizes"))

        if not uploaded_sizes:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Please  provide the sizes"},
            )

        request.data._mutable = True
        request.data["uploaded_sizes"] = uploaded_sizes
        request.data["type"] = "thrift"
        request.data._mutable = False

        print("GGG", request.data)

        return super(ThriftProductsViewSet, self).create(
            request, *args, **kwargs
        )
