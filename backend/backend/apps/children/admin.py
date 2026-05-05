from django.contrib import admin

from .models import Child


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ("full_name", "parent", "nursery", "date_of_birth", "is_active")
    list_filter = ("is_active", "gender", "nursery")
    search_fields = ("first_name", "last_name", "parent__email")
