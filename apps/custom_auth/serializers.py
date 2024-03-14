# serializers.py
from rest_framework import serializers
from .models import ForgotPasswordOTP


class OTPModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForgotPasswordOTP
        fields = ["otp_code"]
