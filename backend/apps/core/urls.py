from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("connexion/", views.login_page, name="login"),
    path("inscription/", views.register_page, name="register"),
    path("inscription/parent/", views.register_parent_page, name="register_parent"),
    path("inscription/creche/", views.register_manager_page, name="register_manager"),
    path("tableau-de-bord/", views.dashboard, name="dashboard"),
    path("a-propos/", views.about, name="about"),
    path("equipe/", views.team, name="team"),
    path("securite/", views.security, name="security"),
    path("faq/", views.faq, name="faq"),
    # 3D learning
    path("cours/", views.course_catalog, name="course_catalog"),
    path("cours/<slug:slug>/", views.course_detail, name="course_detail"),
    # 3D parent tracking
    path("suivi/<int:child_id>/", views.child_progress_3d, name="child_progress_3d"),
]
