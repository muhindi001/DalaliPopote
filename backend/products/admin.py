from django.contrib import admin
from .models import MerchantProduct


@admin.register(MerchantProduct)
class MerchantProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "merchant",
        "sku",
        "price",
        "stock",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "sku",
        "merchant__business_name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        (
            "Product Information",
            {
                "fields": (
                    "merchant",
                    "name",
                    "sku",
                    "description",
                    "image",
                )
            },
        ),
        (
            "Pricing & Inventory",
            {
                "fields": (
                    "price",
                    "stock",
                    "status",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )