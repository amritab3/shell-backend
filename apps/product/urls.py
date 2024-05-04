from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductsViewSet,
    MenProductsViewSet,
    WomenProductsViewSet,
    KidsProductsViewSet,
    CartViewSet,
)

router = DefaultRouter()

router.register(r"men", MenProductsViewSet)
router.register(r"women", WomenProductsViewSet)
router.register(r"kids", KidsProductsViewSet)
router.register(r"cart", CartViewSet)
router.register(r"", ProductsViewSet)

urlpatterns = [path("", include(router.urls))]
