from django.db import models
from accounts.models import User


class MerchantBusiness(models.Model):

    CATEGORY_CHOICES = (
        ("retail", "Retail"),
        ("restaurant", "Restaurant"),
        ("pharmacy", "Pharmacy"),
        ("electronics", "Electronics"),
        ("services", "Services"),
        ("other", "Other"),
    )

    merchant = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="merchant_business",
        null=True,
        blank=True,
    )

    business_name = models.CharField(max_length=255)

    business_email = models.EmailField()

    phone = models.CharField(max_length=20)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    registration_number = models.CharField(max_length=100)

    tax_number = models.CharField(max_length=100)

    annual_revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    address = models.TextField()

    city = models.CharField(max_length=100)

    country = models.CharField(max_length=100)

    website = models.URLField(blank=True)

    kyc_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


class MerchantKYC(models.Model):

    STATUS = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    merchant = models.OneToOneField(
        MerchantBusiness,
        on_delete=models.CASCADE,
        related_name="kyc"
    )

    owner_name = models.CharField(max_length=255)

    national_id = models.CharField(max_length=100)

    id_front = models.ImageField(upload_to="kyc/front/")

    id_back = models.ImageField(upload_to="kyc/back/")

    business_license = models.FileField(upload_to="kyc/license/")

    tin_certificate = models.FileField(upload_to="kyc/tin/")

    selfie = models.ImageField(upload_to="kyc/selfie/")

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="pending"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    verified_at = models.DateTimeField(
        null=True,
        blank=True
    )