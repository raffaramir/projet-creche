from rest_framework import serializers

from .models import Child


class ChildSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Child
        fields = (
            "id", "parent", "nursery",
            "first_name", "last_name", "full_name",
            "date_of_birth", "gender", "school", "photo",
            "notes", "enrolled_on", "is_active",
            "created_at", "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "parent")
