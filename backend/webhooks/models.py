import uuid
from django.db import models

from merchants.models import MerchantBusiness


class Webhook(models.Model):

    EVENT_CHOICES = (
        ("payment.created", "Payment Created"),
        ("payment.success", "Payment Success"),
        ("payment.failed", "Payment Failed"),
        ("payment.refunded", "Payment Refunded"),
        ("refund.created", "Refund Created"),
        ("refund.success", "Refund Success"),
        ("settlement.completed", "Settlement Completed"),
        ("invoice.created", "Invoice Created"),
    )

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("DISABLED", "Disabled"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    merchant = models.ForeignKey(
        MerchantBusiness,
        on_delete=models.CASCADE,
        related_name="webhooks",
    )

    url = models.URLField()

    event = models.CharField(
        max_length=50,
        choices=EVENT_CHOICES,
    )

    secret = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE",
    )

    last_response_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )

    last_attempt_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "webhooks"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event} -> {self.url}"