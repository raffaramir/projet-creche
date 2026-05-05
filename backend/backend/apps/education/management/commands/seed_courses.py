from django.core.management.base import BaseCommand

from apps.education.models import Course, CourseCategory, Lesson


SEED = [
    {
        "title": "L'alphabet enchanté",
        "slug": "alphabet-enchante",
        "category": CourseCategory.LETTERS,
        "description": "Apprends les 26 lettres de l'alphabet en 3D, avec des animations magiques et la lecture audio.",
        "age_min_months": 30,
        "age_max_months": 72,
        "lessons": [
            ("Les voyelles A E I O U Y", "Découverte des voyelles avec sons et formes en 3D.", 8),
            ("Les consonnes (1/3) : B → H", "Première vague de consonnes.", 10),
            ("Les consonnes (2/3) : J → P", "Deuxième vague de consonnes.", 10),
            ("Les consonnes (3/3) : Q → Z", "Dernière vague de consonnes.", 10),
        ],
    },
    {
        "title": "Les chiffres magiques",
        "slug": "chiffres-magiques",
        "category": CourseCategory.NUMBERS,
        "description": "Compte de 0 à 9 dans un univers 3D. Chaque chiffre devient un personnage attachant.",
        "age_min_months": 24,
        "age_max_months": 60,
        "lessons": [
            ("De 0 à 4", "Apprivoise les premiers chiffres.", 7),
            ("De 5 à 9", "Termine la troupe des chiffres.", 7),
            ("Compter ensemble", "Petits jeux de comptage interactifs.", 10),
        ],
    },
    {
        "title": "Bonjour le monde !",
        "slug": "bonjour-le-monde",
        "category": CourseCategory.LANGUAGES,
        "description": "Dis bonjour en français, en anglais, en arabe et en espagnol.",
        "age_min_months": 36,
        "age_max_months": 72,
        "lessons": [
            ("Bonjour 🇫🇷", "La langue de la maison.", 5),
            ("Hello 🇬🇧", "La première langue étrangère.", 5),
            ("Marhaba 🌙", "Salutation arabe.", 5),
            ("Hola 🇪🇸", "Salutation espagnole.", 5),
        ],
    },
    {
        "title": "Histoires des prophètes",
        "slug": "histoires-prophetes",
        "category": CourseCategory.ISLAMIC,
        "description": "Découvre en douceur les grandes figures spirituelles : Nouh, Moussa, Aïssa, Mohamed ﷺ.",
        "age_min_months": 48,
        "age_max_months": 84,
        "lessons": [
            ("L'arche de Nouh (Noé)", "L'histoire de Nouh et l'arche.", 12),
            ("Moussa (Moïse) et la mer", "Le passage de la mer.", 12),
            ("Aïssa (Jésus) et la sagesse", "Les enseignements d'Aïssa.", 12),
            ("Mohamed ﷺ, le messager", "La vie du Prophète, racontée aux enfants.", 12),
        ],
    },
    {
        "title": "Petits explorateurs",
        "slug": "petits-explorateurs",
        "category": CourseCategory.SCIENCE,
        "description": "La Terre, les volcans, les molécules : une introduction joyeuse aux sciences.",
        "age_min_months": 42,
        "age_max_months": 72,
        "lessons": [
            ("La planète Terre", "Notre belle planète bleue.", 8),
            ("Les volcans", "Pourquoi les volcans grondent.", 8),
            ("La matière magique", "Les molécules pour les petits.", 8),
        ],
    },
    {
        "title": "Atelier d'art créatif",
        "slug": "atelier-art-creatif",
        "category": CourseCategory.ART,
        "description": "Formes, couleurs, symétrie : l'éveil artistique en 3D.",
        "age_min_months": 24,
        "age_max_months": 72,
        "lessons": [
            ("Les couleurs primaires", "Rouge, jaune, bleu.", 6),
            ("Les formes magiques", "Cercles, triangles, étoiles.", 6),
            ("La symétrie", "Le miroir des formes.", 6),
        ],
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample 3D courses and lessons."

    def handle(self, *args, **options):
        created_courses = 0
        created_lessons = 0
        for idx, data in enumerate(SEED):
            course, created = Course.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "category": data["category"],
                    "description": data["description"],
                    "age_min_months": data["age_min_months"],
                    "age_max_months": data["age_max_months"],
                    "is_3d": True,
                    "is_published": True,
                    "order": idx,
                },
            )
            if created:
                created_courses += 1
            for order, (title, content, duration) in enumerate(data["lessons"]):
                _, l_created = Lesson.objects.update_or_create(
                    course=course, title=title,
                    defaults={
                        "content": content,
                        "duration_minutes": duration,
                        "order": order,
                    },
                )
                if l_created:
                    created_lessons += 1
        self.stdout.write(self.style.SUCCESS(
            f"OK — {created_courses} cours créés, {created_lessons} leçons créées."
        ))
