from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import IsMerchant

from .models import Settlement
from .serializers import SettlementSerializer
from .services import SettlementService


class SettlementListView(generics.ListAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [
        IsAuthenticated,
        IsMerchant
    ]

    serializer_class = SettlementSerializer

    def get_queryset(self):
        return Settlement.objects.filter(
            merchant=self.request.user.merchant_business
        ).order_by("-created_at")


class SettlementDetailView(generics.RetrieveAPIView):

    authentication_classes = (JWTAuthentication,)
    permission_classes = [
        IsAuthenticated,
        IsMerchant
    ]

    serializer_class = SettlementSerializer

    def get_queryset(self):
        return Settlement.objects.filter(
            merchant=self.request.user.merchant_business
        )


class SettlementProcessView(generics.GenericAPIView):

    """
    Manually trigger settlement payout (testing / admin use)
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = [
        IsAuthenticated,
        IsMerchant
    ]

    serializer_class = SettlementSerializer

    def post(self, request, pk):

        try:
            settlement = Settlement.objects.get(
                pk=pk,
                merchant=request.user.merchant_business
            )
        except Settlement.DoesNotExist:
            return Response(
                {"detail": "Settlement not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        settlement = SettlementService.process_settlement(settlement)

        return Response(
            SettlementSerializer(settlement).data,
            status=status.HTTP_200_OK
        )