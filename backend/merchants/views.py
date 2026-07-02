from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import MerchantBusinessSerializer
from accounts.permissions import IsMerchant


class MerchantBusinessCreateView(generics.CreateAPIView):
    serializer_class = MerchantBusinessSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        merchant_user = self.request.user if getattr(self.request, 'user', None) and self.request.user.is_authenticated else None
        serializer.save(merchant=merchant_user)


class MerchantProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication, JWTAuthentication)
    serializer_class = MerchantBusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.merchant_business    