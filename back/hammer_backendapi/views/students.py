from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from hammer_backendapi.models import Student, Teacher
from hammer_backendapi.serializers import StudentSerializer


class StudentViewSet(ModelViewSet):
    """
    CRUD for the current teacher's students.
    - Reads include nested related objects (explicit serializers).
    - Writes accept *_id fields for FKs.
    - All queries are scoped to request.user's Teacher.
    """
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def _get_teacher(self):
        try:
            return Teacher.objects.get(user=self.request.user)
        except Teacher.DoesNotExist:
            # Consistent 404 if a non-teacher hits the endpoint
            raise NotFound("Teacher not found")

    def get_queryset(self):
        teacher = self._get_teacher()
        return (
            Student.objects.filter(teacher=teacher)
            .select_related(
                "gender_identity",
                "disc_assessment_type",
                "sixteen_types_assessment",
                "enneagram_result",
                "osha_type",
            )
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(teacher=self._get_teacher())
