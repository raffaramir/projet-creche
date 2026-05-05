from django.contrib import admin

from .models import Nursery, NurseryService


class NurseryServiceInline(admin.TabularInline):
    model = NurseryService
    extra = 0


@admin.register(Nursery)
class NurseryAdmin(admin.ModelAdmin):
    list_display = ("name", "manager", "city", "capacity", "is_active")
    list_filter = ("is_active", "city")
    search_fields = ("name", "city", "postal_code", "manager__email")
    inlines = [NurseryServiceInline]
