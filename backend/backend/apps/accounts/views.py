from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import ApprovalStatus
from .permissions import IsAdminRole
from .serializers import (
    ApprovalActionSerializer,
    LittleFutureTokenSerializer,
    ManagerRegistrationSerializer,
    ParentRegistrationSerializer,
    UserPublicSerializer,
)

User = get_user_model()


class ParentRegistrationView(generics.CreateAPIView):
    """POST /api/v1/auth/register/parent/"""

    permission_classes = [AllowAny]
    serializer_class = ParentRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "Inscription enregistrée. Votre compte sera activé après validation par l'administrateur.",
            "user": response.data,
        }
        return response


class ManagerRegistrationView(generics.CreateAPIView):
    """POST /api/v1/auth/register/manager/"""

    permission_classes = [AllowAny]
    serializer_class = ManagerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "Inscription de la crèche enregistrée. Validation administrateur requise.",
            "user": response.data,
        }
        return response


class LittleFutureTokenView(TokenObtainPairView):
    """POST /api/v1/auth/login/"""

    serializer_class = LittleFutureTokenSerializer


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """GET/PATCH /api/v1/auth/me/"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserPublicSerializer

    def get_object(self):
        return self.request.user


class UserAdminViewSet(viewsets.ModelViewSet):
    """Admin endpoint for listing and moderating users."""

    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserPublicSerializer
    permission_classes = [IsAdminRole]
    search_fields = ("email", "first_name", "last_name", "phone")
    ordering_fields = ("created_at", "approval_status", "role")

    def get_queryset(self):
        qs = super().get_queryset()
        role = self.request.query_params.get("role")
        approval = self.request.query_params.get("approval_status")
        if role:
            qs = qs.filter(role=role)
        if approval:
            qs = qs.filter(approval_status=approval)
        return qs

    @action(detail=True, methods=["post"], serializer_class=ApprovalActionSerializer)
    def approve(self, request, pk=None):
        user = self.get_object()
        user.approval_status = ApprovalStatus.APPROVED
        user.approved_at = timezone.now()
        user.approved_by = request.user
        user.rejection_reason = ""
        user.is_active = True
        user.save(update_fields=[
            "approval_status", "approved_at", "approved_by",
            "rejection_reason", "is_active",
        ])
        return Response({"message": "Compte approuvé.", "user": UserPublicSerializer(user).data})

    @action(detail=True, methods=["post"], serializer_class=ApprovalActionSerializer)
    def reject(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.approval_status = ApprovalStatus.REJECTED
        user.rejection_reason = serializer.validated_data.get("rejection_reason", "")
        user.is_active = False
        user.save(update_fields=["approval_status", "rejection_reason", "is_active"])
        return Response({"message": "Compte rejeté.", "user": UserPublicSerializer(user).data})

    @action(detail=False, methods=["get"])
    def pending(self, request):
        qs = self.get_queryset().filter(approval_status=ApprovalStatus.PENDING)
        page = self.paginate_queryset(qs)
        serializer = self.get_serializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
