from django.db import models
from merchants.models import MerchantBusiness
from accounts.models import User


class Customer(models.Model):

    merchant = models.ForeignKey(
        MerchantBusiness,
        on_delete=models.CASCADE,
        related_name="customers"
    )

    linked_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"