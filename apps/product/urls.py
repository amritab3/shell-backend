from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductsViewSet,
    InstoreMenProductsViewSet,
    InstoreWomenProductsViewSet,
    InstoreKidsProductsViewSet,
    ThriftProductsViewSet,
    ProductCommentsViewSet,
)

router = DefaultRouter()

router.register(r"men", InstoreMenProductsViewSet)
router.register(r"women", InstoreWomenProductsViewSet)
router.register(r"kids", InstoreKidsProductsViewSet)

router.register(r"thrift", ThriftProductsViewSet)

router.register(r"", ProductsViewSet)

router2 = DefaultRouter()
router2.register(r"comments", ProductCommentsViewSet)

urlpatterns = [
    path("<str:product_id>/feedback/", include(router2.urls)),
    path("", include(router.urls)),
]
