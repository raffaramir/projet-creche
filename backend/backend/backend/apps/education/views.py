from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import Role
from apps.accounts.permissions import IsApproved

from .models import Course, CourseProgress, Lesson
from .serializers import (
    CourseProgressSerializer,
    CourseSerializer,
    LessonSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_published=True)
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ("title", "category")


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class CourseProgressViewSet(viewsets.ModelViewSet):
    serializer_class = CourseProgressSerializer
    permission_classes = [IsApproved]

    def get_queryset(self):
        user = self.request.user
        qs = CourseProgress.objects.all()
        if user.is_superuser or user.role == Role.ADMIN:
            return qs
        if user.role == Role.PARENT:
            return qs.filter(child__parent=user)
        if user.role == Role.NURSERY_MANAGER:
            return qs.filter(child__nursery__manager=user)
        return qs.none()
