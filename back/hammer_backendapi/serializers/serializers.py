from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from hammer_backendapi.models import (
    Student,
    GenderIdentity,
    DiscAssessment,
    SixteenTypeAssessment,
    EnneagramResult,
    OshaType,
)

# ---- Nested serializers (read-only) ----
class GenderIdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GenderIdentity
        fields = ("id", "gender")


class DiscAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscAssessment
        fields = ("id", "type_name")


class SixteenTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SixteenTypeAssessment
        fields = ("id", "type_name")


class EnneagramResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnneagramResult
        fields = ("id", "result_name")


class OshaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OshaType
        fields = ("id", "name")


# ---- Main serializer ----
class StudentSerializer(serializers.ModelSerializer):
    # READ: nested related objects (safe, explicit)
    gender_identity = GenderIdentitySerializer(read_only=True)
    disc_assessment_type = DiscAssessmentSerializer(read_only=True)
    sixteen_types_assessment = SixteenTypeSerializer(read_only=True)
    enneagram_result = EnneagramResultSerializer(read_only=True)
    osha_type = OshaTypeSerializer(read_only=True)

    # WRITE: accept IDs for FKs
    gender_identity_id = serializers.PrimaryKeyRelatedField(
        source="gender_identity",
        queryset=GenderIdentity.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    disc_assessment_type_id = serializers.PrimaryKeyRelatedField(
        source="disc_assessment_type",
        queryset=DiscAssessment.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    sixteen_types_assessment_id = serializers.PrimaryKeyRelatedField(
        source="sixteen_types_assessment",
        queryset=SixteenTypeAssessment.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    enneagram_result_id = serializers.PrimaryKeyRelatedField(
        source="enneagram_result",
        queryset=EnneagramResult.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )
    osha_type_id = serializers.PrimaryKeyRelatedField(
        source="osha_type",
        queryset=OshaType.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )

    # OPTIONAL: quick validation on scores
    pretest_score = serializers.IntegerField(
        required=False, allow_null=True, min_value=0, max_value=100
    )
    posttest_score = serializers.IntegerField(
        required=False, allow_null=True, min_value=0, max_value=100
    )

    class Meta:
        model = Student
        read_only_fields = ("id", "teacher", "created_at")
        fields = (
            "id",
            "teacher",
            "full_name",
            "start_date",
            "end_date",
            "complete_50_hour_training",
            "passed_osha_10_exam",
            "osha_completion_date",
            "hammer_math",
            "employability_skills",
            "passed_ruler_assessment",
            "pretest_score",
            "posttest_score",
            "created_at",
            # nested read-only
            "gender_identity",
            "disc_assessment_type",
            "sixteen_types_assessment",
            "enneagram_result",
            "osha_type",
            # write-only ids
            "gender_identity_id",
            "disc_assessment_type_id",
            "sixteen_types_assessment_id",
            "enneagram_result_id",
            "osha_type_id",
        )

    def validate(self, attrs):
        """Business rules: end_date after start_date; OSHA fields if passed."""
        start = attrs.get("start_date") or getattr(self.instance, "start_date", None)
        end = attrs.get("end_date") or getattr(self.instance, "end_date", None)
        if start and end and end < start:
            raise serializers.ValidationError({"end_date": "Must be on/after start_date."})

        passed_osha = attrs.get("passed_osha_10_exam")
        # When updating, if flag not present, fall back to instance value
        if passed_osha is None:
            passed_osha = getattr(self.instance, "passed_osha_10_exam", False)

        if passed_osha:
            osha_date = attrs.get("osha_completion_date") or getattr(
                self.instance, "osha_completion_date", None
            )
            osha_type = attrs.get("osha_type") or getattr(self.instance, "osha_type", None)
            if not osha_date:
                raise serializers.ValidationError({"osha_completion_date": "Required if OSHA exam passed."})
            if not osha_type:
                raise serializers.ValidationError({"osha_type_id": "Required if OSHA exam passed."})

        return attrs
