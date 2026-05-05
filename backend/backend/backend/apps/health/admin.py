from django.contrib import admin

from .models import (
    Allergy,
    DietRestriction,
    Disease,
    HealthRecord,
    Medication,
    VaccinationRecord,
)


class AllergyInline(admin.TabularInline):
    model = Allergy
    extra = 0


class DiseaseInline(admin.TabularInline):
    model = Disease
    extra = 0


class MedicationInline(admin.TabularInline):
    model = Medication
    extra = 0


class DietRestrictionInline(admin.TabularInline):
    model = DietRestriction
    extra = 0


class VaccinationInline(admin.TabularInline):
    model = VaccinationRecord
    extra = 0


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ("child", "blood_type", "doctor_name", "updated_at")
    search_fields = ("child__first_name", "child__last_name", "doctor_name")
    inlines = [AllergyInline, DiseaseInline, MedicationInline, DietRestrictionInline, VaccinationInline]


admin.site.register([Allergy, Disease, Medication, DietRestriction, VaccinationRecord])
