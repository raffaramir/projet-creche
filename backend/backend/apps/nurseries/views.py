from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.accounts.models import Role

from .models import Nursery
from .serializers import NurserySerializer


class NurseryViewSet(viewsets.ModelViewSet):
    queryset = Nursery.objects.filter(is_active=True)
    serializer_class = NurserySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ("name", "city", "postal_code")

    def perform_create(self, serializer):
        if self.request.user.role == Role.NURSERY_MANAGER:
            serializer.save(manager=self.request.user)
        else:
            serializer.save()
