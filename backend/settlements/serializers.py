from rest_framework import serializers

from .models import Settlement


class SettlementSerializer(serializers.ModelSerializer):

    merchant = serializers.ReadOnlyField()
    reference = serializers.ReadOnlyField()
    gross_amount = serializers.ReadOnlyField()
    platform_fee = serializers.ReadOnlyField()
    net_amount = serializers.ReadOnlyField()
    currency = serializers.ReadOnlyField()
    settled_at = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta:
        model = Settlement
        fields = [
            "id",
            "merchant",
            "transaction",
            "reference",
            "bank_name",
            "bank_account_name",
            "bank_account_number",
            "gross_amount",
            "platform_fee",
            "net_amount",
            "currency",
            "status",
            "settled_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = (
            "merchant",
            "reference",
            "gross_amount",
            "platform_fee",
            "net_amount",
            "currency",
            "settled_at",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):

        transaction = attrs.get("transaction")

        if transaction.status != "SUCCESS":
            raise serializers.ValidationError(
                "Only successful transactions can be settled."
            )

        if hasattr(transaction, "settlement"):
            raise serializers.ValidationError(
                "Settlement already exists for this transaction."
            )

        return attrs