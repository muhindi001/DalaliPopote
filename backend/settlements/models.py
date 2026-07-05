import uuid

from django.db import models

from merchants.models import MerchantBusiness
from transactions.models import Transaction


class Settlement(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    merchant = models.ForeignKey(
        MerchantBusiness,
        on_delete=models.CASCADE,
        related_name="settlements",
    )

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="settlement",
    )

    reference = models.CharField(
        max_length=100,
        unique=True,
    )

    bank_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    bank_account_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    bank_account_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    gross_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    platform_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    net_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    currency = models.CharField(
        max_length=10,
        default="TZS",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    settled_at = models.DateTimeField(
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
        db_table = "settlements"
        ordering = ["-created_at"]

    def __str__(self):
        return self.reference