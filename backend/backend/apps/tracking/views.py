from rest_framework import viewsets

from apps.accounts.models import Role
from apps.accounts.permissions import IsApproved

from .models import DailyEvaluation, WeeklyReport
from .serializers import DailyEvaluationSerializer, WeeklyReportSerializer


class DailyEvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = DailyEvaluationSerializer
    permission_classes = [IsApproved]

    def get_queryset(self):
        user = self.request.user
        qs = DailyEvaluation.objects.all()
        if user.is_superuser or user.role == Role.ADMIN:
            return qs
        if user.role == Role.PARENT:
            return qs.filter(child__parent=user)
        if user.role in (Role.NURSERY_MANAGER, Role.EDUCATOR):
            return qs.filter(child__nursery__manager=user) if user.role == Role.NURSERY_MANAGER else qs.filter(educator=user)
        return qs.none()

    def perform_create(self, serializer):
        serializer.save(educator=self.request.user)


class WeeklyReportViewSet(viewsets.ModelViewSet):
    serializer_class = WeeklyReportSerializer
    permission_classes = [IsApproved]

    def get_queryset(self):
        user = self.request.user
        qs = WeeklyReport.objects.all()
        if user.is_superuser or user.role == Role.ADMIN:
            return qs
        if user.role == Role.PARENT:
            return qs.filter(child__parent=user)
        if user.role == Role.NURSERY_MANAGER:
            return qs.filter(child__nursery__manager=user)
        return qs.none()
