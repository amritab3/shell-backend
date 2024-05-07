# serializers.py
import json

from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import ForgotPasswordOTP


class OTPModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgotPasswordOTP
        fields = ["otp_code"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        user_data = {
            "id": str(user.id),
            "email": user.email,
            "roles": [role.name for role in user.roles.all()],
        }
        data["user"] = json.dumps(user_data)

        return data
