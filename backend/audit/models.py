from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("REGISTER", "Register"),
        ("PROFILE_UPDATE", "Profile Update"),
        ("KYC_SUBMITTED", "KYC Submitted"),
        ("KYC_APPROVED", "KYC Approved"),
        ("PASSWORD_RESET", "Password Reset"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )

    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
    )

    ip_address = models.GenericIPAddressField()

    user_agent = models.TextField()

    details = models.JSONField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.action}"