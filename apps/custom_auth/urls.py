from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import GenerateForgotPasswordOTPView, OTPVerifyView

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
        "generate-otp/",
        GenerateForgotPasswordOTPView.as_view(),
        name="generate_forgot_password_otp",
    ),
    path(
        "verify-otp/",
        OTPVerifyView.as_view(),
        name="verify_forgot_password_otp",
    ),
]
