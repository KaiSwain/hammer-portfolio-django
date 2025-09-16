# hammer_backendapi/views/students.py
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action

from hammer_backendapi.models import Student, Teacher
from hammer_backendapi.serializers import StudentSerializer

from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.utils import timezone

from .ai_summary_fixed import generate_long_summary_html          # << key import
# Remove module-level PDF import to avoid WeasyPrint startup issues
# from .utils import html_to_pdf_bytes                        # << pdf helper

def _get_html_to_pdf_converter():
    """Lazy import of HTML to PDF converter to avoid WeasyPrint startup issues"""
    try:
        from hammer_backendapi.views.utils import html_to_pdf_bytes
        return html_to_pdf_bytes
    except ImportError as e:
        raise RuntimeError(f"PDF generation not available: {e}")

class StudentViewSet(ModelViewSet):
    """
    CRUD for the current teacher's students.
    Queries are scoped to the authenticated teacher.
    """
    serializer_class = StudentSerializer
    
    # Always require authentication for proper teacher-student isolation
    permission_classes = [IsAuthenticated]

    def _get_teacher(self):
        try:
            return Teacher.objects.get(user=self.request.user)
        except Teacher.DoesNotExist:
            raise NotFound("Teacher not found")

    def get_queryset(self):
        # Always filter by teacher - this is essential for data isolation
        # Even in development mode, teachers should only see their own students
        teacher = self._get_teacher()
        return (
            Student.objects.filter(teacher=teacher)
            .select_related(
                "gender_identity",
                "disc_assessment_type", 
                "sixteen_types_assessment",
                "enneagram_result",
                "osha_type",
                "teacher"
            )
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(teacher=self._get_teacher())

    @action(detail=True, methods=["post"], url_path="personality-summary")
    def personality_summary(self, request, pk=None):
        # Scope to current teacher
        student = get_object_or_404(self.get_queryset(), pk=pk)

        # 1) Ask AI for the HTML body of the report
        try:
            print("[AI] calling generate_long_summary_html")
            summary_html = generate_long_summary_html(student)
        except Exception as e:
            print("[AI] ERROR:", e)
            summary_html = "<h2>Summary Unavailable</h2><p>Please try again later.</p>"

        # 2) Render that HTML inside your Django template
        context = {
            "name": student.full_name,
            "generated_at": timezone.now().strftime("%B %d, %Y"),
            "summary_html": summary_html,  # template injects this
        }
        html = render_to_string("personality_summary.html", context)

        # 3) Convert HTML to PDF and return as download
        try:
            html_to_pdf = _get_html_to_pdf_converter()
            pdf_bytes = html_to_pdf(html)
            
            # Return as PDF download
            response = HttpResponse(pdf_bytes, content_type="application/pdf")
            safe_name = student.full_name.replace(" ", "_").replace("/", "_") or "Student"
            response["Content-Disposition"] = f'attachment; filename="{safe_name}_personality_summary.pdf"'
            return response
            
        except Exception as pdf_error:
            print(f"[AI] PDF generation failed: {pdf_error}")
            # Return HTML content as fallback
            return JsonResponse({
                "success": True,
                "student_name": student.full_name,
                "generated_at": timezone.now().strftime("%B %d, %Y"),
                "summary_html": summary_html,
                "format": "html",
                "message": f"PDF generation failed: {pdf_error}. Showing HTML content.",
                "error": str(pdf_error)
            })
    

    