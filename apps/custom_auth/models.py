import uuid

from django.db import models
from django.utils import timezone

from apps.user.models import User


# Create your models here.
class ForgotPasswordOTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    otp_code = models.CharField(max_length=6)
    user = models.ForeignKey(
        User, related_name="forgot_password_otp", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        verbose_name="created_at", auto_now_add=True
    )
    expires_at = models.DateTimeField(
        verbose_name="expires_at", null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        """
        Check if the record has expired.
        """
        return (
            self.expires_at is not None and self.expires_at <= timezone.now()
        )

    def __str__(self):
        return self.user.email
