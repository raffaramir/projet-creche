from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ConversationType(models.TextChoices):
    PARENT_NURSERY = "parent_nursery", _("Parent ↔ Crèche")
    MEDICAL = "medical", _("Conseil médical")
    GROUP = "group", _("Groupe")


class Conversation(models.Model):
    """A conversation between two or more users."""

    title = models.CharField(_("Titre"), max_length=150, blank=True)
    type = models.CharField(
        _("Type"),
        max_length=30,
        choices=ConversationType.choices,
        default=ConversationType.PARENT_NURSERY,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Participants"),
        related_name="conversations",
    )
    nursery = models.ForeignKey(
        "nurseries.Nursery",
        verbose_name=_("Crèche"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conversations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")
        ordering = ("-updated_at",)

    def __str__(self):
        return self.title or f"Conversation #{self.pk}"


class Message(models.Model):
    """A single chat message."""

    conversation = models.ForeignKey(
        Conversation,
        verbose_name=_("Conversation"),
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Expéditeur"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="messages_sent",
    )
    content = models.TextField(_("Message"))
    attachment = models.FileField(_("Pièce jointe"), upload_to="chat/", null=True, blank=True)

    is_flagged = models.BooleanField(_("Signalé"), default=False)
    is_deleted = models.BooleanField(_("Supprimé"), default=False)
    read_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Lu par"),
        related_name="messages_read",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.sender} — {self.content[:30]}"
