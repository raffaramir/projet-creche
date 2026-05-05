from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import ApprovalStatus, ManagerProfile, Role

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    """Public, read-only user representation."""

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "approval_status",
            "phone",
            "city",
            "country",
            "profile_image",
        )
        read_only_fields = fields


class ManagerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerProfile
        fields = ("professional_card", "license_number", "services_offered")


class ParentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            "email", "password", "password_confirm",
            "first_name", "last_name",
            "date_of_birth", "place_of_birth",
            "phone", "address", "city", "postal_code", "country",
            "profile_image",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Les mots de passe ne correspondent pas."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(role=Role.PARENT, approval_status=ApprovalStatus.PENDING, **validated_data)
        user.set_password(password)
        user.save()
        return user


class ManagerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    license_number = serializers.CharField(required=False, allow_blank=True)
    professional_card = serializers.FileField(required=False, allow_null=True)
    services_offered = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            "email", "password", "password_confirm",
            "first_name", "last_name",
            "date_of_birth", "place_of_birth",
            "phone", "address", "city", "postal_code", "country",
            "profile_image",
            "license_number", "professional_card", "services_offered",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Les mots de passe ne correspondent pas."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        manager_data = {
            "license_number": validated_data.pop("license_number", ""),
            "professional_card": validated_data.pop("professional_card", None),
            "services_offered": validated_data.pop("services_offered", ""),
        }
        user = User(
            role=Role.NURSERY_MANAGER,
            approval_status=ApprovalStatus.PENDING,
            **validated_data,
        )
        user.set_password(password)
        user.save()
        ManagerProfile.objects.create(user=user, **manager_data)
        return user


class ApprovalActionSerializer(serializers.Serializer):
    """Used by admins to approve/reject pending users."""

    rejection_reason = serializers.CharField(required=False, allow_blank=True)


class LittleFutureTokenSerializer(TokenObtainPairSerializer):
    """JWT token serializer that blocks unapproved users."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["full_name"] = user.full_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_approved and not self.user.is_superuser:
            raise serializers.ValidationError(
                "Votre compte est en attente de validation par un administrateur."
            )
        data["user"] = UserPublicSerializer(self.user).data
        return data
