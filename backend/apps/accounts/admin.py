from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import ManagerProfile, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("-created_at",)
    list_display = ("email", "full_name", "role", "approval_status", "is_active", "created_at")
    list_filter = ("role", "approval_status", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name", "phone")
    readonly_fields = ("created_at", "updated_at", "last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Identité"), {"fields": (
            "first_name", "last_name", "date_of_birth", "place_of_birth",
            "phone", "address", "city", "postal_code", "country", "profile_image",
        )}),
        (_("Rôle & validation"), {"fields": (
            "role", "approval_status", "approved_at", "approved_by", "rejection_reason",
        )}),
        (_("Permissions"), {"fields": (
            "is_active", "is_staff", "is_superuser", "groups", "user_permissions",
        )}),
        (_("Dates"), {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role"),
        }),
    )


@admin.register(ManagerProfile)
class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "license_number")
    search_fields = ("user__email", "license_number")
