from rest_framework import serializers

from .models import Nursery, NurseryService


class NurseryServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseryService
        fields = ("id", "title", "description", "icon")


class NurserySerializer(serializers.ModelSerializer):
    services = NurseryServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Nursery
        fields = (
            "id", "name", "description", "manager",
            "address", "city", "postal_code", "country",
            "phone", "email", "website",
            "capacity", "age_min_months", "age_max_months", "opening_hours",
            "cover_image", "logo", "is_active", "services",
            "created_at", "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "manager")
