from rest_framework import serializers

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)

    class Meta:
        model = Message
        fields = (
            "id", "conversation", "sender", "sender_name",
            "content", "attachment",
            "is_flagged", "is_deleted",
            "created_at",
        )
        read_only_fields = ("created_at", "sender", "sender_name", "is_flagged", "is_deleted")


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = (
            "id", "title", "type", "participants", "nursery",
            "messages", "created_at", "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
