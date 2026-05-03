from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "type", "nursery", "updated_at")
    list_filter = ("type",)
    filter_horizontal = ("participants",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "is_flagged", "is_deleted", "created_at")
    list_filter = ("is_flagged", "is_deleted")
    search_fields = ("content", "sender__email")
