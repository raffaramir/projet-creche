from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class MoodChoice(models.TextChoices):
    HAPPY = "happy", _("Joyeux")
    CALM = "calm", _("Calme")
    TIRED = "tired", _("Fatigué")
    SAD = "sad", _("Triste")
    UPSET = "upset", _("Agité")


class DailyEvaluation(models.Model):
    """Daily evaluation written by educators about a child."""

    child = models.ForeignKey(
        "children.Child",
        verbose_name=_("Enfant"),
        on_delete=models.CASCADE,
        related_name="evaluations",
    )
    educator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Éducateur"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="evaluations_made",
    )
    date = models.DateField(_("Date"))

    mood = models.CharField(_("Humeur"), max_length=20, choices=MoodChoice.choices, default=MoodChoice.HAPPY)
    appetite_score = models.PositiveSmallIntegerField(_("Appétit (1-5)"), default=3)
    sleep_minutes = models.PositiveIntegerField(_("Sommeil (minutes)"), default=0)
    behavior_score = models.PositiveSmallIntegerField(_("Comportement (1-5)"), default=3)
    learning_score = models.PositiveSmallIntegerField(_("Apprentissage (1-5)"), default=3)

    activities = models.TextField(_("Activités du jour"), blank=True)
    incidents = models.TextField(_("Incidents / remarques"), blank=True)
    educator_note = models.TextField(_("Note de l'éducateur"), blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Évaluation quotidienne")
        verbose_name_plural = _("Évaluations quotidiennes")
        ordering = ("-date",)
        unique_together = ("child", "date")

    def __str__(self):
        return f"{self.child.full_name} — {self.date}"


class WeeklyReport(models.Model):
    """Aggregated weekly summary for parents."""

    child = models.ForeignKey(
        "children.Child",
        verbose_name=_("Enfant"),
        on_delete=models.CASCADE,
        related_name="weekly_reports",
    )
    week_start = models.DateField(_("Début de semaine"))
    summary = models.TextField(_("Résumé de la semaine"), blank=True)
    progress_score = models.PositiveSmallIntegerField(_("Progrès global (1-10)"), default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Rapport hebdomadaire")
        verbose_name_plural = _("Rapports hebdomadaires")
        ordering = ("-week_start",)
        unique_together = ("child", "week_start")

    def __str__(self):
        return f"{self.child.full_name} — semaine du {self.week_start}"
