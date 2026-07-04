from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    payment_reference = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    class Meta:
        model = Payment
        fields = [
            "id",
            "merchant",
            "customer",
            "payment_link",
            "payment_reference",
            "gateway_reference",
            "amount",
            "currency",
            "payment_method",
            "status",
            "description",
            "customer_email",
            "customer_phone",
            "paid_at",
            "expires_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "merchant",
            "payment_reference",
            "status",
            "paid_at",
            "created_at",
            "updated_at",
        ]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate(self, data):
        payment_link = data.get("payment_link")

        # If payment link exists, enforce amount consistency
        if payment_link:
            if data.get("amount") and payment_link.amount != data["amount"]:
                raise serializers.ValidationError(
                    "Amount must match payment link amount."
                )

        return data