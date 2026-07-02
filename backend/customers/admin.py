from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "merchant",
        "linked_user",
        "created_at",
    )

    list_filter = (
        "created_at",
        "merchant",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
        "merchant__business_name",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = ("-created_at",)

    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "merchant",
                    "linked_user",
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "address",
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