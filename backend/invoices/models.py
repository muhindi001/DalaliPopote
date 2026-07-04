import uuid
from django.db import models

from merchants.models import MerchantBusiness
from customers.models import Customer
from transactions.models import Transaction


class Invoice(models.Model):

    INVOICE_STATUS = (
        ("DRAFT", "Draft"),
        ("SENT", "Sent"),
        ("PAID", "Paid"),
        ("VOID", "Void"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    merchant = models.ForeignKey(
        MerchantBusiness,
        on_delete=models.CASCADE,
        related_name="invoices"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices"
    )

    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="invoice"
    )

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    currency = models.CharField(max_length=10, default="TZS")

    status = models.CharField(
        max_length=20,
        choices=INVOICE_STATUS,
        default="DRAFT"
    )

    issued_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "invoices"
        ordering = ["-created_at"]

    def __str__(self):
        return self.invoice_number