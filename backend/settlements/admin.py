from django.contrib import admin

from .models import Settlement


@admin.register(Settlement)
class SettlementAdmin(admin.ModelAdmin):

    list_display = (
        "reference",
        "merchant",
        "transaction",
        "gross_amount",
        "platform_fee",
        "net_amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "reference",
        "merchant__business_name",
        "transaction__reference",
    )

    readonly_fields = (
        "id",
        "reference",
        "gross_amount",
        "platform_fee",
        "net_amount",
        "currency",
        "settled_at",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)