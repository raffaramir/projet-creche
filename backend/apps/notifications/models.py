from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationCategory(models.TextChoices):
    INFO = "info", _("Information")
    HEALTH = "health", _("Santé")
    EDUCATION = "education", _("Éducation")
    CHAT = "chat", _("Message")
    APPROVAL = "approval", _("Validation de compte")
    REPORT = "report", _("Rapport")


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Destinataire"),
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    category = models.CharField(
        _("Catégorie"),
        max_length=20,
        choices=NotificationCategory.choices,
        default=NotificationCategory.INFO,
    )
    title = models.CharField(_("Titre"), max_length=180)
    body = models.TextField(_("Contenu"), blank=True)
    link = models.CharField(_("Lien interne"), max_length=255, blank=True)

    is_read = models.BooleanField(_("Lue"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} — {self.title}"
