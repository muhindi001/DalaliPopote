import uuid
from django.db import models
from merchants.models import MerchantBusiness


class PaymentLink(models.Model):

    merchant = models.ForeignKey(
        MerchantBusiness,
        on_delete=models.CASCADE,
        related_name="payment_links"
    )

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default="TZS"
    )

    active = models.BooleanField(default=True)

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title