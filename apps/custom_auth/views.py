import os

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from rest_framework import views
from rest_framework import status
from rest_framework.response import Response

import random

from apps.user.models import User
from .models import ForgotPasswordOTP
from .serializers import OTPModelSerializer


# Create your views here.
class GenerateForgotPasswordOTPView(views.APIView):
    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            otp_instance = ForgotPasswordOTP.objects.get(user=user)
            if otp_instance.is_expired():
                otp_instance.delete()  # Delete expired instance
            else:
                return Response(
                    {"message": "OTP already generated for this user."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ForgotPasswordOTP.DoesNotExist:
            pass  # No OTP instance found, continue to generate a new OTP

        # Generate a 6-digit OTP
        otp_code = "".join([str(random.randint(0, 9)) for _ in range(6)])

        # Save the OTP to the database
        otp_instance = ForgotPasswordOTP.objects.create(
            user=user, otp_code=otp_code
        )

        if otp_instance:
            merge_data = {"OTP_CODE": otp_code}
            html_body = render_to_string(
                "forgot_password_otp.html", merge_data
            )
            message = EmailMultiAlternatives(
                subject="Password reset OTP",
                body="password reset otp",
                from_email=os.environ.get("FROM_EMAIL"),
                to=[email],
            )
            message.attach_alternative(html_body, "text/html")
            message.send(fail_silently=False)

        serializer = OTPModelSerializer(otp_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OTPVerifyView(views.APIView):
    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("otp_code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            otp_instance = ForgotPasswordOTP.objects.get(
                user=user, otp_code=otp_code
            )
        except ForgotPasswordOTP.DoesNotExist:
            return Response(
                {"message": "Invalid OTP code."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ForgotPasswordOTP.MultipleObjectsReturned:
            return Response(
                {"message": "Multiple OTP instances found for the user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if otp_instance.is_expired():
            return Response(
                {"message": "OTP has expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If OTP is found and matches, you can perform additional actions here if needed.
        # For simplicity, let's just delete the OTP instance after verification.
        otp_instance.delete()

        return Response(
            {"message": "OTP verified successfully."},
            status=status.HTTP_200_OK,
        )


class UpdatePasswordView(views.APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_new_password")

        # Check if password and confirm_password match
        if password != confirm_password:
            return Response(
                {"message": "Passwords do not match."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return Response(
                {"message": "Password updated successfully."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
