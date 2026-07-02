from rest_framework import serializers
from .models import MerchantBusiness


class MerchantBusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = MerchantBusiness
        fields = "__all__"
        read_only_fields = (
            "merchant",
            "kyc_verified",
            "created_at",
            "updated_at",
        )