from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import IsMerchant
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionListView(generics.ListAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsMerchant]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(
            merchant=self.request.user.merchant_business
        ).order_by("-created_at")


class TransactionDetailView(generics.RetrieveAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsMerchant]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(
            merchant=self.request.user.merchant_business
        )