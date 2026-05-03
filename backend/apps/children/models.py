from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    BOY = "boy", _("Garçon")
    GIRL = "girl", _("Fille")
    OTHER = "other", _("Autre")


class Child(models.Model):
    """A child enrolled (or being enrolled) at a nursery."""

    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Parent"),
        on_delete=models.CASCADE,
        related_name="children",
    )
    nursery = models.ForeignKey(
        "nurseries.Nursery",
        verbose_name=_("Crèche"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enrolled_children",
    )

    first_name = models.CharField(_("Prénom"), max_length=80)
    last_name = models.CharField(_("Nom"), max_length=80)
    date_of_birth = models.DateField(_("Date de naissance"))
    gender = models.CharField(
        _("Genre"),
        max_length=20,
        choices=Gender.choices,
        default=Gender.OTHER,
    )

    school = models.CharField(_("École / établissement"), max_length=150, blank=True)
    photo = models.ImageField(_("Photo"), upload_to="children/", null=True, blank=True)
    notes = models.TextField(_("Notes"), blank=True)

    enrolled_on = models.DateField(_("Date d'inscription"), null=True, blank=True)
    is_active = models.BooleanField(_("Actif"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Enfant")
        verbose_name_plural = _("Enfants")
        ordering = ("last_name", "first_name")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
