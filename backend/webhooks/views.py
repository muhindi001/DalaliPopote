from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import IsMerchant

from .models import Webhook
from .serializers import WebhookSerializer


class WebhookListCreateView(generics.ListCreateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsMerchant]
    serializer_class = WebhookSerializer

    def get_queryset(self):
        return Webhook.objects.filter(
            merchant=self.request.user.merchant_business
        )

    def perform_create(self, serializer):
        serializer.save(
            merchant=self.request.user.merchant_business
        )


class WebhookDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated, IsMerchant]
    serializer_class = WebhookSerializer

    def get_queryset(self):
        return Webhook.objects.filter(
            merchant=self.request.user.merchant_business
        )