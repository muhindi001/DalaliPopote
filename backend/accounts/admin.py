from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id", "username","email","role","phone","is_active","is_staff","date_joined",
    )

    list_filter = (
        "role","is_active","is_staff","is_superuser",
    )

    search_fields = (
        "username","email","phone",
    )

    ordering = ("-date_joined",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "role",
                    "phone",
                    "created_at",
                )
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "date_joined",
        "last_login",
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "email",
                    "role",
                    "phone",
                ),
            },
        ),
    )