from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        "invoice_number",
        "merchant",
        "customer",
        "total",
        "currency",
        "status",
        "issued_at",
    )

    search_fields = (
        "invoice_number",
        "merchant__business_name",
        "customer__email",
    )

    list_filter = (
        "status",
        "currency",
        "issued_at",
    )

    readonly_fields = (
        "id",
        "invoice_number",
        "created_at",
    )

    ordering = ("-created_at",)