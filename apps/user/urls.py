from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import CreateUserView, ListUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create_user"),
    path(
        "login/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("list/", ListUserView.as_view(), name="list_user"),
]
