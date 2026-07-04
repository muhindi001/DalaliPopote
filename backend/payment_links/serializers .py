from rest_framework import serializers
from .models import PaymentLink


class PaymentLinkSerializer(serializers.ModelSerializer):

    payment_url = serializers.SerializerMethodField(read_only=True)

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
            "payment_url",
        ]

        read_only_fields = (
            "merchant",
            "uuid",
            "created_at",
            "payment_url",
        )

    def get_payment_url(self, obj):
        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(
                f"/pay/{obj.uuid}/"
            )

        return f"/pay/{obj.uuid}/"