from rest_framework import viewsets

from apps.accounts.permissions import IsApproved
from apps.accounts.models import Role

from .models import Child
from .serializers import ChildSerializer


class ChildViewSet(viewsets.ModelViewSet):
    """Children scoped by user role: parents see their children; managers see their nursery's."""

    serializer_class = ChildSerializer
    permission_classes = [IsApproved]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == Role.ADMIN:
            return Child.objects.all()
        if user.role == Role.PARENT:
            return Child.objects.filter(parent=user)
        if user.role == Role.NURSERY_MANAGER:
            return Child.objects.filter(nursery__manager=user)
        return Child.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role == Role.PARENT:
            serializer.save(parent=self.request.user)
        else:
            serializer.save()
