from rest_framework import viewsets

from apps.accounts.models import Role
from apps.accounts.permissions import IsApproved

from .models import (
    Allergy,
    DietRestriction,
    Disease,
    HealthRecord,
    Medication,
    VaccinationRecord,
)
from .serializers import (
    AllergySerializer,
    DietRestrictionSerializer,
    DiseaseSerializer,
    HealthRecordSerializer,
    MedicationSerializer,
    VaccinationRecordSerializer,
)


class HealthRecordViewSet(viewsets.ModelViewSet):
    serializer_class = HealthRecordSerializer
    permission_classes = [IsApproved]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == Role.ADMIN:
            return HealthRecord.objects.all()
        if user.role == Role.PARENT:
            return HealthRecord.objects.filter(child__parent=user)
        if user.role == Role.NURSERY_MANAGER:
            return HealthRecord.objects.filter(child__nursery__manager=user)
        return HealthRecord.objects.none()


class _ScopedHealthChildViewSet(viewsets.ModelViewSet):
    """Shared scoping logic for objects attached to a HealthRecord."""

    permission_classes = [IsApproved]
    model = None

    def get_queryset(self):
        user = self.request.user
        qs = self.model.objects.all()
        if user.is_superuser or user.role == Role.ADMIN:
            return qs
        if user.role == Role.PARENT:
            return qs.filter(health_record__child__parent=user)
        if user.role == Role.NURSERY_MANAGER:
            return qs.filter(health_record__child__nursery__manager=user)
        return qs.none()


class AllergyViewSet(_ScopedHealthChildViewSet):
    serializer_class = AllergySerializer
    model = Allergy
    queryset = Allergy.objects.all()


class DiseaseViewSet(_ScopedHealthChildViewSet):
    serializer_class = DiseaseSerializer
    model = Disease
    queryset = Disease.objects.all()


class MedicationViewSet(_ScopedHealthChildViewSet):
    serializer_class = MedicationSerializer
    model = Medication
    queryset = Medication.objects.all()


class DietRestrictionViewSet(_ScopedHealthChildViewSet):
    serializer_class = DietRestrictionSerializer
    model = DietRestriction
    queryset = DietRestriction.objects.all()


class VaccinationViewSet(_ScopedHealthChildViewSet):
    serializer_class = VaccinationRecordSerializer
    model = VaccinationRecord
    queryset = VaccinationRecord.objects.all()
