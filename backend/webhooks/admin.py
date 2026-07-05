from django.contrib import admin

from .models import Webhook


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):

    list_display = (
        "merchant",
        "event",
        "url",
        "status",
        "last_response_code",
        "last_attempt_at",
        "created_at",
    )

    list_filter = (
        "event",
        "status",
        "created_at",
    )

    search_fields = (
        "url",
        "merchant__business_name",
    )

    readonly_fields = (
        "last_response_code",
        "last_attempt_at",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)