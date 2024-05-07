from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    GenerateForgotPasswordOTPView,
    OTPVerifyView,
    UpdatePasswordView,
)

urlpatterns = [
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
    path(
        "token/verify/",
        jwt_views.TokenVerifyView.as_view(),
        name="token_verify",
    ),
    path(
        "generate-otp/",
        GenerateForgotPasswordOTPView.as_view(),
        name="generate_forgot_password_otp",
    ),
    path(
        "verify-otp/",
        OTPVerifyView.as_view(),
        name="verify_forgot_password_otp",
    ),
    path(
        "update-password/",
        UpdatePasswordView.as_view(),
        name="update_password",
    ),
]
