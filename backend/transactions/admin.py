from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        "reference",
        "merchant",
        "customer",
        "gross_amount",
        "fee",
        "net_amount",
        "currency",
        "status",
        "gateway",
        "created_at",
    )

    search_fields = (
        "reference",
        "gateway_reference",
        "merchant__business_name",
        "customer__email",
    )

    list_filter = (
        "status",
        "gateway",
        "currency",
        "created_at",
    )

    readonly_fields = (
        "id",
        "reference",
        "created_at",
    )

    ordering = ("-created_at",)