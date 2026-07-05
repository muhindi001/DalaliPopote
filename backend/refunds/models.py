import uuid

from django.db import models

from merchants.models import MerchantBusiness
from payments.models import Payment
from transactions.models import Transaction


class Refund(models.Model):

    REFUND_STATUS = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("PROCESSING", "Processing"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("CANCELLED", "Cancelled"),
    )

    merchant = models.ForeignKey(
        MerchantBusiness,
        on_delete=models.CASCADE,
        related_name="refunds"
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="refunds"
    )

    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="refunds"
    )

    refund_reference = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    gateway_reference = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=REFUND_STATUS,
        default="PENDING"
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "refunds"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.refund_reference} ({self.status})"

    @property
    def is_successful(self):
        return self.status == "SUCCESS"

    @property
    def is_pending(self):
        return self.status == "PENDING"

    @property
    def is_failed(self):
        return self.status == "FAILED"

    @property
    def is_cancelled(self):
        return self.status == "CANCELLED"