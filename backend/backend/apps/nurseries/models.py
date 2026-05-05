from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Nursery(models.Model):
    """A daycare/nursery establishment."""

    name = models.CharField(_("Nom de la crèche"), max_length=150)
    description = models.TextField(_("Description"), blank=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Responsable"),
        on_delete=models.CASCADE,
        related_name="managed_nurseries",
    )

    # Address
    address = models.CharField(_("Adresse"), max_length=255)
    city = models.CharField(_("Ville"), max_length=120)
    postal_code = models.CharField(_("Code postal"), max_length=20)
    country = models.CharField(_("Pays"), max_length=80, default="France")

    # Contact
    phone = models.CharField(_("Téléphone"), max_length=30, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    website = models.URLField(_("Site web"), blank=True)

    # Capacity & schedule
    capacity = models.PositiveIntegerField(_("Capacité"), default=0)
    age_min_months = models.PositiveIntegerField(_("Âge minimum (mois)"), default=3)
    age_max_months = models.PositiveIntegerField(_("Âge maximum (mois)"), default=72)
    opening_hours = models.CharField(_("Horaires d'ouverture"), max_length=120, blank=True)

    # Media
    cover_image = models.ImageField(_("Image de couverture"), upload_to="nurseries/", null=True, blank=True)
    logo = models.ImageField(_("Logo"), upload_to="nurseries/logos/", null=True, blank=True)

    is_active = models.BooleanField(_("Actif"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Crèche")
        verbose_name_plural = _("Crèches")
        ordering = ("name",)

    def __str__(self):
        return self.name


class NurseryService(models.Model):
    """Services offered by a nursery (meals, sleep, activities, etc.)."""

    nursery = models.ForeignKey(
        Nursery,
        verbose_name=_("Crèche"),
        on_delete=models.CASCADE,
        related_name="services",
    )
    title = models.CharField(_("Service"), max_length=120)
    description = models.TextField(_("Description"), blank=True)
    icon = models.CharField(_("Icône"), max_length=60, blank=True)

    class Meta:
        verbose_name = _("Service de crèche")
        verbose_name_plural = _("Services de crèche")

    def __str__(self):
        return f"{self.nursery.name} — {self.title}"
