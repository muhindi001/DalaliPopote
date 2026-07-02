from django.contrib import admin
from .models import PaymentLink


@admin.register(PaymentLink)
class PaymentLinkAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "merchant",
        "amount",
        "currency",
        "active",
        "expires_at",
        "created_at",
    )

    list_filter = (
        "active",
        "currency",
        "created_at",
        "merchant",
    )

    search_fields = (
        "title",
        "merchant__business_name",
        "uuid",
    )

    readonly_fields = (
        "uuid",
        "created_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        (
            "Payment Information",
            {
                "fields": (
                    "merchant",
                    "title",
                    "description",
                    "amount",
                    "currency",
                )
            },
        ),
        (
            "Link Settings",
            {
                "fields": (
                    "uuid",
                    "active",
                    "expires_at",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )