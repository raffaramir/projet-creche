from django.contrib import admin

from .models import DailyEvaluation, WeeklyReport


@admin.register(DailyEvaluation)
class DailyEvaluationAdmin(admin.ModelAdmin):
    list_display = ("child", "date", "mood", "appetite_score", "sleep_minutes", "behavior_score")
    list_filter = ("date", "mood")
    search_fields = ("child__first_name", "child__last_name")


@admin.register(WeeklyReport)
class WeeklyReportAdmin(admin.ModelAdmin):
    list_display = ("child", "week_start", "progress_score")
    list_filter = ("week_start",)
