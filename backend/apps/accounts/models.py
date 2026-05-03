from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    ADMIN = "admin", _("Administrateur")
    PARENT = "parent", _("Parent")
    NURSERY_MANAGER = "manager", _("Responsable de crèche")
    EDUCATOR = "educator", _("Éducateur(rice)")


class ApprovalStatus(models.TextChoices):
    PENDING = "pending", _("En attente")
    APPROVED = "approved", _("Approuvé")
    REJECTED = "rejected", _("Rejeté")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("L'adresse email est obligatoire."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.ADMIN)
        extra_fields.setdefault("approval_status", ApprovalStatus.APPROVED)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Le superutilisateur doit avoir is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Le superutilisateur doit avoir is_superuser=True."))
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model: email is the username, with role + approval flow."""

    username = None
    email = models.EmailField(_("Adresse email"), unique=True)

    role = models.CharField(
        _("Rôle"),
        max_length=20,
        choices=Role.choices,
        default=Role.PARENT,
    )
    approval_status = models.CharField(
        _("Statut de validation"),
        max_length=20,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
    )

    # Identity
    first_name = models.CharField(_("Prénom"), max_length=80, blank=True)
    last_name = models.CharField(_("Nom"), max_length=80, blank=True)
    date_of_birth = models.DateField(_("Date de naissance"), null=True, blank=True)
    place_of_birth = models.CharField(_("Lieu de naissance"), max_length=120, blank=True)
    phone = models.CharField(_("Téléphone"), max_length=30, blank=True)
    address = models.CharField(_("Adresse"), max_length=255, blank=True)
    city = models.CharField(_("Ville"), max_length=120, blank=True)
    postal_code = models.CharField(_("Code postal"), max_length=20, blank=True)
    country = models.CharField(_("Pays"), max_length=80, blank=True, default="France")

    profile_image = models.ImageField(
        _("Photo de profil"),
        upload_to="profiles/",
        null=True,
        blank=True,
    )

    # Approval workflow metadata
    approved_at = models.DateTimeField(_("Validé le"), null=True, blank=True)
    approved_by = models.ForeignKey(
        "self",
        verbose_name=_("Validé par"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approvals_made",
    )
    rejection_reason = models.TextField(_("Motif de rejet"), blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.full_name or self.email} ({self.get_role_display()})"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_approved(self) -> bool:
        return self.approval_status == ApprovalStatus.APPROVED

    @property
    def is_parent(self) -> bool:
        return self.role == Role.PARENT

    @property
    def is_nursery_manager(self) -> bool:
        return self.role == Role.NURSERY_MANAGER


class ManagerProfile(models.Model):
    """Extra fields specific to nursery managers."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="manager_profile",
        limit_choices_to={"role": Role.NURSERY_MANAGER},
    )
    professional_card = models.FileField(
        _("Carte professionnelle"),
        upload_to="manager_cards/",
        null=True,
        blank=True,
    )
    license_number = models.CharField(_("Numéro de licence"), max_length=100, blank=True)
    services_offered = models.TextField(_("Services proposés"), blank=True)

    class Meta:
        verbose_name = _("Profil responsable de crèche")
        verbose_name_plural = _("Profils responsables de crèche")

    def __str__(self):
        return f"Profil — {self.user.full_name}"
