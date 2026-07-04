import uuid

from django.db import models
from django.conf import settings

from merchants.models import MerchantBusiness
from customers.models import Customer
from payments.models import Payment


class Transaction(models.Model):

    TRANSACTION_STATUS = (
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("REFUND", "Refund"),
    )

    PAYMENT_GATEWAYS = (
        ("INTERNAL", "Internal"),
        ("MOBILE_MONEY", "Mobile Money"),
        ("CARD", "Card"),
        ("BANK", "Bank"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    merchant = models.ForeignKey(
        MerchantBusiness,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions"
    )

    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        related_name="transaction"
    )

    reference = models.CharField(
        max_length=120,
        unique=True
    )

    gateway_reference = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    gross_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    net_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default="TZS"
    )

    status = models.CharField(
        max_length=20,
        choices=TRANSACTION_STATUS,
        default="SUCCESS"
    )

    gateway = models.CharField(
        max_length=20,
        choices=PAYMENT_GATEWAYS,
        default="INTERNAL"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference} - {self.status}"