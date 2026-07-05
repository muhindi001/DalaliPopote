from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import IsMerchant

from .models import Refund
from .serializers import RefundSerializer
from .services import RefundService


class RefundListCreateView(generics.ListCreateAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [
        IsAuthenticated,
        IsMerchant
    ]

    serializer_class = RefundSerializer

    def get_queryset(self):
        return Refund.objects.filter(
            merchant=self.request.user.merchant_business
        ).order_by("-created_at")

    def perform_create(self, serializer):

        refund = serializer.save(
            merchant=self.request.user.merchant_business
        )

        RefundService.process_refund(refund)


class RefundDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [
        IsAuthenticated,
        IsMerchant
    ]

    serializer_class = RefundSerializer

    def get_queryset(self):
        return Refund.objects.filter(
            merchant=self.request.user.merchant_business
        )

    def patch(self, request, *args, **kwargs):

        refund = self.get_object()

        if refund.status == "SUCCESS":
            return Response(
                {
                    "detail":
                    "Processed refunds cannot be modified."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):

        refund = self.get_object()

        if refund.status == "SUCCESS":
            return Response(
                {
                    "detail":
                    "Processed refunds cannot be deleted."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        RefundService.cancel_refund(refund)

        refund.delete()

        return Response(
            {
                "message":
                "Refund deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )