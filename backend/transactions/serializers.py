from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = [
            "id",
            "merchant",
            "customer",
            "payment",
            "reference",
            "gateway_reference",
            "gross_amount",
            "fee",
            "net_amount",
            "currency",
            "status",
            "gateway",
            "created_at",
        ]

        read_only_fields = fields