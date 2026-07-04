from rest_framework import serializers

from .models import PaymentLink


class PaymentLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLink
        fields = [
            "id",
            "merchant",
            "uuid",
            "title",
            "description",
            "amount",
            "currency",
            "active",
            "expires_at",
            "created_at",
        ]
        read_only_fields = ("merchant", "uuid", "created_at")
