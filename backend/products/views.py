from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsMerchant
from .models import MerchantProduct
from .serializers import MerchantProductSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication, JWTAuthentication)
    serializer_class = MerchantProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsMerchant()]

    def get_queryset(self):
        if self.request.user.is_authenticated and getattr(self.request.user, "merchant_business", None):
            return MerchantProduct.objects.filter(merchant=self.request.user.merchant_business)
        return MerchantProduct.objects.all()

    def perform_create(self, serializer):
        serializer.save(merchant=self.request.user.merchant_business)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication, JWTAuthentication)
    serializer_class = MerchantProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsMerchant()]

    def get_queryset(self):
        if self.request.user.is_authenticated and getattr(self.request.user, "merchant_business", None):
            return MerchantProduct.objects.filter(merchant=self.request.user.merchant_business)
        return MerchantProduct.objects.all()