from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from apps.children.models import Child
from apps.education.models import Course, CourseProgress


def home(request):
    return render(request, "pages/home.html")


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
