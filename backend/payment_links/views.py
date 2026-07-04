from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import IsMerchant

from .models import PaymentLink
from .serializers import PaymentLinkSerializer


class PaymentLinkListCreateView(generics.ListCreateAPIView):
    authentication_classes = (JWTAuthentication,)
    serializer_class = PaymentLinkSerializer
    permission_classes = [IsAuthenticated, IsMerchant]

    def get_queryset(self):
        return PaymentLink.objects.filter(
            merchant=self.request.user.merchant_business
        )

    def perform_create(self, serializer):
        serializer.save(
            merchant=self.request.user.merchant_business
        )


class PaymentLinkDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (JWTAuthentication,)
    serializer_class = PaymentLinkSerializer
    permission_classes = [IsAuthenticated, IsMerchant]

    def get_queryset(self):
        return PaymentLink.objects.filter(
            merchant=self.request.user.merchant_business
        )