from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "payment_reference",
        "merchant",
        "customer",
        "amount",
        "currency",
        "payment_method",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "currency",
        "created_at",
    )

    search_fields = (
        "payment_reference",
        "gateway_reference",
        "customer_email",
        "customer_phone",
        "merchant__business_name",
    )

    readonly_fields = (
        "payment_reference",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)