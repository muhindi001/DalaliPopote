from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsMerchant
from merchants.models import MerchantBusiness
from .models import MerchantProduct
from .serializers import MerchantProductSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication, JWTAuthentication)
    serializer_class = MerchantProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsMerchant()]

    def _get_merchant_business(self):
        if not self.request.user.is_authenticated:
            return None

        try:
            return self.request.user.merchant_business
        except ObjectDoesNotExist:
            pass

        role = getattr(self.request.user, "role", None)
        if isinstance(role, str):
            role = role.lower()

        if role not in {"merchant", "merchant_user", "seller", "vendor"}:
            return None

        business_name = self.request.user.get_full_name() or self.request.user.username or "Merchant Business"
        merchant_business = MerchantBusiness.objects.create(
            merchant=self.request.user,
            business_name=business_name,
            business_email=self.request.user.email or f"{self.request.user.username}@example.com",
            phone=getattr(self.request.user, "phone", "") or "0000000000",
            category="other",
            registration_number=f"auto-{self.request.user.pk}",
            tax_number=f"auto-{self.request.user.pk}",
            annual_revenue="0.00",
            address="To be updated",
            city="Unknown",
            country="Tanzania",
        )
        return merchant_business

    def get_queryset(self):
        merchant_business = self._get_merchant_business()
        if self.request.user.is_authenticated and merchant_business:
            return MerchantProduct.objects.filter(merchant=merchant_business)
        return MerchantProduct.objects.all()

    def perform_create(self, serializer):
        merchant_business = self._get_merchant_business()
        if not merchant_business:
            raise PermissionError("Merchant profile could not be initialized.")
        serializer.save(merchant=merchant_business)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication, JWTAuthentication)
    serializer_class = MerchantProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsMerchant()]

    def _get_merchant_business(self):
        if not self.request.user.is_authenticated:
            return None

        try:
            return self.request.user.merchant_business
        except ObjectDoesNotExist:
            pass

        role = getattr(self.request.user, "role", None)
        if isinstance(role, str):
            role = role.lower()

        if role not in {"merchant", "merchant_user", "seller", "vendor"}:
            return None

        business_name = self.request.user.get_full_name() or self.request.user.username or "Merchant Business"
        merchant_business = MerchantBusiness.objects.create(
            merchant=self.request.user,
            business_name=business_name,
            business_email=self.request.user.email or f"{self.request.user.username}@example.com",
            phone=getattr(self.request.user, "phone", "") or "0000000000",
            category="other",
            registration_number=f"auto-{self.request.user.pk}",
            tax_number=f"auto-{self.request.user.pk}",
            annual_revenue="0.00",
            address="To be updated",
            city="Unknown",
            country="Tanzania",
        )
        return merchant_business

    def get_queryset(self):
        merchant_business = self._get_merchant_business()
        if self.request.user.is_authenticated and merchant_business:
            return MerchantProduct.objects.filter(merchant=merchant_business)
        return MerchantProduct.objects.all()