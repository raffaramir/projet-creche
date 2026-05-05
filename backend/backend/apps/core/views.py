import json

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.children.models import Child
from apps.education.models import Course, CourseProgress


def home(request):
    return render(request, "pages/home.html")


@require_POST
def session_login(request):
    """Authenticate user and create a Django session (for @login_required views)."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"detail": "Données invalides."}, status=400)

    email = data.get("email", "").strip()
    password = data.get("password", "")

    user = authenticate(request, email=email, password=password)
    if user is None:
        return JsonResponse({"detail": "Email ou mot de passe incorrect."}, status=401)

    if not user.is_approved and not user.is_superuser:
        return JsonResponse(
            {"detail": "Votre compte est en attente de validation par un administrateur."},
            status=403,
        )

    auth_login(request, user)
    return JsonResponse({
        "ok": True,
        "role": user.role,
        "email": user.email,
        "full_name": user.full_name,
    })


def session_logout(request):
    """Log out and redirect to home."""
    auth_logout(request)
    return redirect("home")


def login_page(request):
    return render(request, "pages/login.html")


def register_page(request):
    return render(request, "pages/register_choice.html")


def register_parent_page(request):
    return render(request, "pages/register_parent.html")


def register_manager_page(request):
    return render(request, "pages/register_manager.html")


@login_required
def dashboard(request):
    return render(request, "pages/dashboard.html", {"user_obj": request.user})


def about(request):
    return render(request, "pages/about.html")


def team(request):
    return render(request, "pages/team.html")


def security(request):
    return render(request, "pages/security.html")


def faq(request):
    return render(request, "pages/faq.html")


def course_catalog(request):
    courses = Course.objects.filter(is_published=True)
    return render(request, "pages/course_catalog.html", {"courses": courses})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    return render(request, "pages/course_detail.html", {"course": course})


@login_required
def child_progress_3d(request, child_id):
    """3D parent tracking dashboard for a single child."""
    user = request.user
    qs = Child.objects.all()
    if not user.is_superuser and getattr(user, "role", "") != "admin":
        qs = qs.filter(parent=user)
    child = get_object_or_404(qs, pk=child_id)
    progress = CourseProgress.objects.filter(child=child).select_related("course")
    return render(
        request,
        "pages/child_progress_3d.html",
        {"child": child, "progress": progress},
    )
