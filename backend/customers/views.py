from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.permissions import IsMerchant
from .models import Customer
from .serializers import CustomerSerializer


class CustomerListCreateView(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication, JWTAuthentication)
    serializer_class = CustomerSerializer
    permission_classes = [
        IsAuthenticated,
        IsMerchant
    ]

    def get_queryset(self):
        return Customer.objects.filter(
            merchant=self.request.user.merchant_business
        )

    def perform_create(self, serializer):
        serializer.save(
            merchant=self.request.user.merchant_business
        )


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = (TokenAuthentication, JWTAuthentication)
    serializer_class = CustomerSerializer
    permission_classes = [
        IsAuthenticated,
        IsMerchant
    ]

    def get_queryset(self):
        return Customer.objects.filter(
            merchant=self.request.user.merchant_business
        )
        