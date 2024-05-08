from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductsViewSet,
    InstoreMenProductsViewSet,
    InstoreWomenProductsViewSet,
    InstoreKidsProductsViewSet,
    ThriftProductsViewSet,
)

router = DefaultRouter()

router.register(r"men", InstoreMenProductsViewSet)
router.register(r"women", InstoreWomenProductsViewSet)
router.register(r"kids", InstoreKidsProductsViewSet)

router.register(r"thrift", ThriftProductsViewSet)

router.register(r"", ProductsViewSet)

urlpatterns = [path("", include(router.urls))]
