from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from hammer_backendapi.models import (
    Student,
    StudentFile,
    GenderIdentity,
    DiscAssessment,
    SixteenTypeAssessment,
    EnneagramResult,
    OshaType,
    FundingSource,
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


class FundingSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundingSource
        fields = ("id", "name", "description")


class StudentFileSerializer(serializers.ModelSerializer):
    """Serializer for student file uploads"""
    student_name = serializers.CharField(source='student.first_name', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    file_url = serializers.SerializerMethodField()
    file_size_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentFile
        fields = [
            'id', 'student', 'student_name', 'file', 'file_url', 
            'original_filename', 'file_size', 'file_size_mb', 
            'uploaded_at', 'uploaded_by', 'uploaded_by_name'
        ]
        read_only_fields = ['id', 'uploaded_at', 'uploaded_by', 'file_size']
    
    def get_file_url(self, obj):
        """Get the file URL for download"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None
    
    def get_file_size_mb(self, obj):
        """Get file size in MB with 2 decimal places"""
        if obj.file_size:
            return round(obj.file_size / (1024 * 1024), 2)
        return 0


# ---- Main serializer ----
class StudentSerializer(serializers.ModelSerializer):
    # READ: nested related objects (safe, explicit)
    gender_identity = GenderIdentitySerializer(read_only=True)
    disc_assessment_type = DiscAssessmentSerializer(read_only=True)
    sixteen_types_assessment = SixteenTypeSerializer(read_only=True)
    enneagram_result = EnneagramResultSerializer(read_only=True)
    osha_type = OshaTypeSerializer(read_only=True)
    funding_source = FundingSourceSerializer(read_only=True)

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
    funding_source_id = serializers.PrimaryKeyRelatedField(
        source="funding_source",
        queryset=FundingSource.objects.all(),
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
            "email",
            "nccer_number",
            "start_date",
            "end_date",
            "complete_50_hour_training",
            "passed_osha_10_exam",
            "osha_completion_date",
            "hammer_math",
            "employability_skills",
            "job_interview_skills",
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
            "funding_source",
            # write-only ids
            "gender_identity_id",
            "disc_assessment_type_id",
            "sixteen_types_assessment_id",
            "enneagram_result_id",
            "osha_type_id",
            "funding_source_id",
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
