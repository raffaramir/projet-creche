from django.db import models
from django.utils.translation import gettext_lazy as _


class CourseCategory(models.TextChoices):
    LETTERS = "letters", _("Lettres")
    NUMBERS = "numbers", _("Chiffres")
    LANGUAGES = "languages", _("Langues")
    ISLAMIC = "islamic", _("Éducation islamique")
    SCIENCE = "science", _("Sciences")
    ART = "art", _("Arts & créativité")


class Course(models.Model):
    """An interactive 3D learning course."""

    title = models.CharField(_("Titre du cours"), max_length=150)
    slug = models.SlugField(_("Identifiant"), unique=True, max_length=180)
    category = models.CharField(
        _("Catégorie"),
        max_length=20,
        choices=CourseCategory.choices,
    )
    description = models.TextField(_("Description"), blank=True)
    age_min_months = models.PositiveIntegerField(_("Âge minimum (mois)"), default=24)
    age_max_months = models.PositiveIntegerField(_("Âge maximum (mois)"), default=72)

    # 3D / asset metadata
    cover_image = models.ImageField(_("Image de couverture"), upload_to="courses/", null=True, blank=True)
    scene_url = models.URLField(_("URL de la scène 3D"), blank=True)
    is_3d = models.BooleanField(_("Contenu 3D"), default=True)

    is_published = models.BooleanField(_("Publié"), default=False)
    order = models.PositiveIntegerField(_("Ordre d'affichage"), default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Cours")
        verbose_name_plural = _("Cours")
        ordering = ("category", "order", "title")

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """A specific lesson inside a course."""

    course = models.ForeignKey(
        Course,
        verbose_name=_("Cours"),
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(_("Titre de la leçon"), max_length=150)
    content = models.TextField(_("Contenu pédagogique"), blank=True)
    media_url = models.URLField(_("Média / vidéo"), blank=True)
    duration_minutes = models.PositiveIntegerField(_("Durée (minutes)"), default=10)
    order = models.PositiveIntegerField(_("Ordre"), default=0)

    class Meta:
        verbose_name = _("Leçon")
        verbose_name_plural = _("Leçons")
        ordering = ("course", "order")

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class CourseProgress(models.Model):
    """A child's progress on a given course."""

    child = models.ForeignKey(
        "children.Child",
        verbose_name=_("Enfant"),
        on_delete=models.CASCADE,
        related_name="course_progress",
    )
    course = models.ForeignKey(
        Course,
        verbose_name=_("Cours"),
        on_delete=models.CASCADE,
        related_name="progress_entries",
    )
    completion_percent = models.PositiveIntegerField(_("Avancement (%)"), default=0)
    last_lesson = models.ForeignKey(
        Lesson,
        verbose_name=_("Dernière leçon"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    score = models.PositiveIntegerField(_("Score"), default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Progression")
        verbose_name_plural = _("Progressions")
        unique_together = ("child", "course")

    def __str__(self):
        return f"{self.child.full_name} — {self.course.title} ({self.completion_percent}%)"
