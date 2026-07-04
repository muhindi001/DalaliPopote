from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import IsMerchant
from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceListView(generics.ListAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsMerchant]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.filter(
            merchant=self.request.user.merchant_business
        )


class InvoiceDetailView(generics.RetrieveAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsMerchant]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.filter(
            merchant=self.request.user.merchant_business
        )