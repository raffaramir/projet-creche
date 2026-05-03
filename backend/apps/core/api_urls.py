from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import (
    CurrentUserView,
    LittleFutureTokenView,
    ManagerRegistrationView,
    ParentRegistrationView,
    UserAdminViewSet,
)
from apps.chat.views import ConversationViewSet, MessageViewSet
from apps.children.views import ChildViewSet
from apps.education.views import (
    CourseProgressViewSet,
    CourseViewSet,
    LessonViewSet,
)
from apps.health.views import (
    AllergyViewSet,
    DietRestrictionViewSet,
    DiseaseViewSet,
    HealthRecordViewSet,
    MedicationViewSet,
    VaccinationViewSet,
)
from apps.notifications.views import NotificationViewSet
from apps.nurseries.views import NurseryViewSet
from apps.tracking.views import DailyEvaluationViewSet, WeeklyReportViewSet

router = DefaultRouter()
router.register(r"admin/users", UserAdminViewSet, basename="admin-users")
router.register(r"children", ChildViewSet, basename="children")
router.register(r"nurseries", NurseryViewSet, basename="nurseries")
router.register(r"health/records", HealthRecordViewSet, basename="health-records")
router.register(r"health/allergies", AllergyViewSet, basename="health-allergies")
router.register(r"health/diseases", DiseaseViewSet, basename="health-diseases")
router.register(r"health/medications", MedicationViewSet, basename="health-medications")
router.register(r"health/diet", DietRestrictionViewSet, basename="health-diet")
router.register(r"health/vaccinations", VaccinationViewSet, basename="health-vaccinations")
router.register(r"education/courses", CourseViewSet, basename="education-courses")
router.register(r"education/lessons", LessonViewSet, basename="education-lessons")
router.register(r"education/progress", CourseProgressViewSet, basename="education-progress")
router.register(r"tracking/evaluations", DailyEvaluationViewSet, basename="tracking-evaluations")
router.register(r"tracking/reports", WeeklyReportViewSet, basename="tracking-reports")
router.register(r"chat/conversations", ConversationViewSet, basename="chat-conversations")
router.register(r"chat/messages", MessageViewSet, basename="chat-messages")
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    # Auth
    path("auth/register/parent/", ParentRegistrationView.as_view(), name="api_register_parent"),
    path("auth/register/manager/", ManagerRegistrationView.as_view(), name="api_register_manager"),
    path("auth/login/", LittleFutureTokenView.as_view(), name="api_login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="api_refresh"),
    path("auth/me/", CurrentUserView.as_view(), name="api_me"),
    # REST resources
    path("", include(router.urls)),
]
