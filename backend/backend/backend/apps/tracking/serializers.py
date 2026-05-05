from rest_framework import serializers

from .models import DailyEvaluation, WeeklyReport


class DailyEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyEvaluation
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "educator")


class WeeklyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyReport
        fields = "__all__"
        read_only_fields = ("created_at",)
