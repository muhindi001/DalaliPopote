import uuid

from django.db import models

from merchants.models import MerchantBusiness
from customers.models import Customer
from payment_links.models import PaymentLink


class Payment(models.Model):

    PAYMENT_METHODS = (
        ("CARD", "Card"),
        ("MOBILE_MONEY", "Mobile Money"),
        ("BANK_TRANSFER", "Bank Transfer"),
        ("WALLET", "Wallet"),
        ("QR_CODE", "QR Code"),
        ("CASH", "Cash"),
    )

    PAYMENT_STATUS = (
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("CANCELLED", "Cancelled"),
        ("EXPIRED", "Expired"),
        ("REFUNDED", "Refunded"),
    )

    merchant = models.ForeignKey(
        MerchantBusiness,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )

    payment_link = models.ForeignKey(
        PaymentLink,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )

    payment_reference = models.UUIDField(
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

    currency = models.CharField(
        max_length=10,
        default="TZS"
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHODS,
        default="CARD"
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="PENDING"
    )

    description = models.TextField(
        blank=True
    )

    customer_email = models.EmailField(
        blank=True,
        null=True
    )

    customer_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    expires_at = models.DateTimeField(
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
        db_table = "payments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.payment_reference} - {self.status}"