from django.db import models
from merchants.models import MerchantBusiness


class MerchantProduct(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    merchant = models.ForeignKey(
        MerchantBusiness,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=255)

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name