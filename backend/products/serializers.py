from rest_framework import serializers
from .models import MerchantProduct


class MerchantProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantProduct
        fields = "__all__"
        read_only_fields = (
            "merchant",
            "created_at",
            "updated_at",
        )