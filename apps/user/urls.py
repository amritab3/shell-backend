from uuid import UUID
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import (
    CreateUserView,
    ListUserView,
    RetrieveUpdateDeleteUser,
    UserAdminViewSet,
)

router = DefaultRouter()

router.register(r"user", UserAdminViewSet)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create_user"),
    path("admin/", include(router.urls)),
    path("", ListUserView.as_view(), name="list_user"),
    path("<str:pk>/", RetrieveUpdateDeleteUser.as_view(), name="user-detail"),
]
