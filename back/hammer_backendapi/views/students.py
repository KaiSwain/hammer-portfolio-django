from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from hammer_backendapi.models import (
    Student,
    Teacher,
    GenderIdentity,
    DiscAssessment,
    SixteenTypeAssessment,
    EnneagramResult,
    OshaType

)

# -----------------------------
# Student Serializer
# -----------------------------
class StudentSerializer(serializers.ModelSerializer):
    # WRITE: accept FK ids
    gender_identity_id = serializers.PrimaryKeyRelatedField(
        source="gender_identity", queryset=GenderIdentity.objects.all(),
        required=False, allow_null=True, write_only=True
    )
    disc_assessment_type_id = serializers.PrimaryKeyRelatedField(
        source="disc_assessment_type", queryset=DiscAssessment.objects.all(),
        required=False, allow_null=True, write_only=True
    )
    sixteen_types_assessment_id = serializers.PrimaryKeyRelatedField(
        source="sixteen_types_assessment", queryset=SixteenTypeAssessment.objects.all(),
        required=False, allow_null=True, write_only=True
    )
    enneagram_result_id = serializers.PrimaryKeyRelatedField(
        source="enneagram_result", queryset=EnneagramResult.objects.all(),
        required=False, allow_null=True, write_only=True
    )
    osha_type_id = serializers.PrimaryKeyRelatedField(
        source="osha_type", queryset=OshaType.objects.all(),
        required=False, allow_null=True, write_only=True
    )

    class Meta:
        model = Student
        # Explicitly list fields so we can include the *_id write-only fields
        fields = (
            "id",
            "teacher",  # keep teacher read-only; you set it in view on create
            "full_name",
            "start_date", "end_date",
            "complete_50_hour_training", "passed_osha_10_exam",
            "osha_completion_date", "hammer_math", "employability_skills",
            "passed_ruler_assessment", "pretest_score", "posttest_score",
            "created_at",
            # READ: nested FKs (depth=1 will expand these)
            "gender_identity", "disc_assessment_type", "sixteen_types_assessment",
            "enneagram_result", "osha_type",
            # WRITE: id inputs
            "gender_identity_id", "disc_assessment_type_id",
            "sixteen_types_assessment_id", "enneagram_result_id", "osha_type_id",
        )
        read_only_fields = ("id", "teacher", "created_at")
        depth = 1  # expands the read fields above

# -----------------------------
# Student ViewSet
# -----------------------------
class StudentView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            teacher = Teacher.objects.get(user=request.user)
            students = Student.objects.filter(teacher=teacher)
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        # get teacher bound to the logged-in user
        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        # do NOT put teacher in data; it's read-only and will be ignored
        # normalize/remap if needed (same as your update path)
        # data = self._remap_and_normalize(data)  # if you have this helper

        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save(teacher=teacher)  # <-- set teacher here
            
            return Response(StudentSerializer(instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()

        # pull out FK fields so DRF doesn't try to validate them as nested (depth=1)
        fk_fields = [
            ("gender_identity", GenderIdentity),
            ("disc_assessment_type", DiscAssessment),
            ("sixteen_types_assessment", SixteenTypeAssessment),
            ("enneagram_result", EnneagramResult),
            ("osha_type", OshaType),
        ]
        fk_updates = {}
        for name, _ in fk_fields:
            if name in data:
                fk_updates[name] = data.pop(name)

        # let serializer handle simple fields (partial or full — your call)
        ser = StudentSerializer(student, data=data, partial=True)
        if not ser.is_valid():
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        # apply simple field updates
        ser.save()

        # now handle the foreign keys manually from the payload
        def coerce_to_id(val):
            # supports number, "", None, {"id": X}
            if val in ("", None):
                return None
            if isinstance(val, dict):
                return val.get("id")
            return val  # assume it's already an ID

        from django.core.exceptions import ObjectDoesNotExist
        for name, model in fk_fields:
            if name not in fk_updates:
                continue  # not being updated
            raw = fk_updates[name]
            fk_id = coerce_to_id(raw)
            if fk_id is None:
                setattr(student, name, None)
            else:
                try:
                    obj = model.objects.get(pk=fk_id)
                except ObjectDoesNotExist:
                    return Response({name: [f"Invalid id: {fk_id}"]}, status=status.HTTP_400_BAD_REQUEST)
                setattr(student, name, obj)

        student.save()
        student.refresh_from_db()

        # return depth=1
        return Response(StudentSerializer(student).data, status=status.HTTP_200_OK)
    