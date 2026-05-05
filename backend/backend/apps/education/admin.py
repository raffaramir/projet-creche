from django.contrib import admin

from .models import Course, CourseProgress, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "is_3d", "order")
    list_filter = ("category", "is_published", "is_3d")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("course", "title", "order", "duration_minutes")
    list_filter = ("course",)


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ("child", "course", "completion_percent", "score", "updated_at")
    list_filter = ("course",)
