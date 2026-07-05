from rest_framework import serializers

from .models import Webhook


class WebhookSerializer(serializers.ModelSerializer):

    merchant = serializers.ReadOnlyField()

    class Meta:
        model = Webhook
        fields = "__all__"
        read_only_fields = (
            "merchant",
            "last_response_code",
            "last_attempt_at",
            "created_at",
            "updated_at",
        )