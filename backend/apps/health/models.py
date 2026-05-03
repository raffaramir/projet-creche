from django.db import models
from django.utils.translation import gettext_lazy as _


class HealthRecord(models.Model):
    """One-to-one health profile per child."""

    child = models.OneToOneField(
        "children.Child",
        verbose_name=_("Enfant"),
        on_delete=models.CASCADE,
        related_name="health_record",
    )

    blood_type = models.CharField(_("Groupe sanguin"), max_length=10, blank=True)
    height_cm = models.PositiveIntegerField(_("Taille (cm)"), null=True, blank=True)
    weight_kg = models.DecimalField(_("Poids (kg)"), max_digits=5, decimal_places=2, null=True, blank=True)

    doctor_name = models.CharField(_("Médecin référent"), max_length=120, blank=True)
    doctor_phone = models.CharField(_("Téléphone du médecin"), max_length=30, blank=True)
    insurance_number = models.CharField(_("Numéro d'assuré"), max_length=80, blank=True)

    special_needs = models.TextField(_("Besoins particuliers"), blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Dossier médical")
        verbose_name_plural = _("Dossiers médicaux")

    def __str__(self):
        return f"Dossier — {self.child.full_name}"


class Allergy(models.Model):
    SEVERITY_CHOICES = [
        ("low", _("Faible")),
        ("medium", _("Modérée")),
        ("high", _("Élevée")),
    ]

    health_record = models.ForeignKey(
        HealthRecord,
        verbose_name=_("Dossier médical"),
        on_delete=models.CASCADE,
        related_name="allergies",
    )
    name = models.CharField(_("Allergène"), max_length=120)
    severity = models.CharField(_("Gravité"), max_length=20, choices=SEVERITY_CHOICES, default="low")
    notes = models.TextField(_("Notes"), blank=True)

    class Meta:
        verbose_name = _("Allergie")
        verbose_name_plural = _("Allergies")

    def __str__(self):
        return self.name


class Disease(models.Model):
    health_record = models.ForeignKey(
        HealthRecord,
        verbose_name=_("Dossier médical"),
        on_delete=models.CASCADE,
        related_name="diseases",
    )
    name = models.CharField(_("Maladie"), max_length=150)
    diagnosed_on = models.DateField(_("Date de diagnostic"), null=True, blank=True)
    is_chronic = models.BooleanField(_("Chronique"), default=False)
    notes = models.TextField(_("Notes"), blank=True)

    class Meta:
        verbose_name = _("Maladie")
        verbose_name_plural = _("Maladies")

    def __str__(self):
        return self.name


class Medication(models.Model):
    health_record = models.ForeignKey(
        HealthRecord,
        verbose_name=_("Dossier médical"),
        on_delete=models.CASCADE,
        related_name="medications",
    )
    name = models.CharField(_("Médicament"), max_length=150)
    dosage = models.CharField(_("Posologie"), max_length=120, blank=True)
    schedule = models.CharField(_("Fréquence"), max_length=120, blank=True)
    start_date = models.DateField(_("Début"), null=True, blank=True)
    end_date = models.DateField(_("Fin"), null=True, blank=True)
    notes = models.TextField(_("Notes"), blank=True)

    class Meta:
        verbose_name = _("Médicament")
        verbose_name_plural = _("Médicaments")

    def __str__(self):
        return self.name


class DietRestriction(models.Model):
    health_record = models.ForeignKey(
        HealthRecord,
        verbose_name=_("Dossier médical"),
        on_delete=models.CASCADE,
        related_name="diet_restrictions",
    )
    name = models.CharField(_("Restriction alimentaire"), max_length=120)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Restriction alimentaire")
        verbose_name_plural = _("Restrictions alimentaires")

    def __str__(self):
        return self.name


class VaccinationRecord(models.Model):
    health_record = models.ForeignKey(
        HealthRecord,
        verbose_name=_("Dossier médical"),
        on_delete=models.CASCADE,
        related_name="vaccinations",
    )
    vaccine = models.CharField(_("Vaccin"), max_length=150)
    administered_on = models.DateField(_("Date d'administration"))
    next_dose_on = models.DateField(_("Prochaine dose"), null=True, blank=True)
    notes = models.TextField(_("Notes"), blank=True)

    class Meta:
        verbose_name = _("Vaccination")
        verbose_name_plural = _("Vaccinations")

    def __str__(self):
        return f"{self.vaccine} — {self.administered_on}"
