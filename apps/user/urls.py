from uuid import UUID
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter


from .views import (
    CreateUserView,
    ListUserView,
    RetrieveUpdateDeleteUser,
    UserAdminViewSet,
    CartViewSet,
    RolesViewSet,
)

router1 = DefaultRouter()
router2 = DefaultRouter()

router1.register(r"user", UserAdminViewSet)
router1.register(r"roles", RolesViewSet)
router2.register("", CartViewSet, basename="user_cart")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create_user"),
    path("admin/", include(router1.urls)),
    path("<str:userId>/cart/", include(router2.urls)),
    path("", ListUserView.as_view(), name="list_user"),
    path("<str:pk>/", RetrieveUpdateDeleteUser.as_view(), name="user-detail"),
]
