from django.contrib import admin

from .models import Refund


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):

    list_display = (
        "refund_reference",
        "merchant",
        "payment",
        "transaction",
        "amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "refund_reference",
        "gateway_reference",
        "payment__payment_reference",
        "transaction__reference",
    )

    readonly_fields = (
        "refund_reference",
        "gateway_reference",
        "processed_at",
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )