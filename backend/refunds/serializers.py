from decimal import Decimal
from rest_framework import serializers
from django.db.models import Sum
from .models import Refund


class RefundSerializer(serializers.ModelSerializer):

    refund_reference = serializers.ReadOnlyField()
    merchant = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.ReadOnlyField()

    class Meta:
        model = Refund
        fields = [
            "id",
            "merchant",
            "payment",
            "transaction",
            "refund_reference",
            "gateway_reference",
            "amount",
            "reason",
            "notes",
            "status",
            "processed_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "merchant",
            "refund_reference",
            "gateway_reference",
            "status",
            "processed_at",
            "created_at",
            "updated_at",
        )

    def validate_amount(self, value):
        if value <= Decimal("0.00"):
            raise serializers.ValidationError(
                "Refund amount must be greater than zero."
            )
        return value
    


    def validate(self, attrs):

        payment = attrs.get("payment")
        transaction = attrs.get("transaction")
        amount = attrs.get("amount")

        # Payment must exist
        if payment is None:
            raise serializers.ValidationError({
                "payment": "Payment is required."
            })

        # Transaction must belong to payment
        if transaction.payment != payment:
            raise serializers.ValidationError({
                "transaction":
                "Transaction does not belong to the selected payment."
            })

        # Only successful payments can be refunded
        if payment.status != "SUCCESS":
            raise serializers.ValidationError(
                "Only successful payments can be refunded."
            )

        # Transaction must also be successful
        if transaction.status != "SUCCESS":
            raise serializers.ValidationError(
                "Only successful transactions can be refunded."
            )

        # Total refunded so far
        total_refunded = (
            payment.refunds
            .filter(status__in=[
                "PENDING",
                "APPROVED",
                "PROCESSING",
                "SUCCESS"
            ])
            .exclude(pk=getattr(self.instance, "pk", None))
                .aggregate(
                total=Sum("amount")
            )["total"]
            or Decimal("0.00")
        )

        remaining = payment.amount - total_refunded

        if amount > remaining:
            raise serializers.ValidationError(
                f"Refund exceeds remaining refundable amount ({remaining})."
            )

        return attrs