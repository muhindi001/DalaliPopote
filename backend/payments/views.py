from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import IsMerchant
from .models import Payment
from .serializers import PaymentSerializer


class PaymentListCreateView(generics.ListCreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsMerchant]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(
            merchant=self.request.user.merchant_business
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(
            merchant=self.request.user.merchant_business,
            status="PENDING"
        )


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsMerchant]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(
            merchant=self.request.user.merchant_business
        )