from rest_framework import serializers

from .models import (
    Allergy,
    DietRestriction,
    Disease,
    HealthRecord,
    Medication,
    VaccinationRecord,
)


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = "__all__"


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = "__all__"


class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = "__all__"


class DietRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietRestriction
        fields = "__all__"


class VaccinationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccinationRecord
        fields = "__all__"


class HealthRecordSerializer(serializers.ModelSerializer):
    allergies = AllergySerializer(many=True, read_only=True)
    diseases = DiseaseSerializer(many=True, read_only=True)
    medications = MedicationSerializer(many=True, read_only=True)
    diet_restrictions = DietRestrictionSerializer(many=True, read_only=True)
    vaccinations = VaccinationRecordSerializer(many=True, read_only=True)

    class Meta:
        model = HealthRecord
        fields = (
            "id", "child",
            "blood_type", "height_cm", "weight_kg",
            "doctor_name", "doctor_phone", "insurance_number",
            "special_needs", "updated_at",
            "allergies", "diseases", "medications", "diet_restrictions", "vaccinations",
        )
