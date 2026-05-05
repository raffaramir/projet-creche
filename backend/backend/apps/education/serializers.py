from rest_framework import serializers

from .models import Course, CourseProgress, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "course", "title", "content", "media_url", "duration_minutes", "order")


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id", "title", "slug", "category", "description",
            "age_min_months", "age_max_months", "cover_image",
            "scene_url", "is_3d", "is_published", "order",
            "lessons", "created_at", "updated_at",
        )


class CourseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProgress
        fields = "__all__"
        read_only_fields = ("started_at", "updated_at")
