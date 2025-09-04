# hammer_backendapi/views/generate_all.py
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Remove module-level PDF import to avoid WeasyPrint startup issues
# from hammer_backendapi.views.utils import generate_master_pdf_pymupdf

def _get_master_pdf_generator():
    """Lazy import of master PDF generator to avoid WeasyPrint startup issues"""
    try:
        from hammer_backendapi.views.utils import generate_master_pdf_pymupdf
        return generate_master_pdf_pymupdf
    except ImportError as e:
        raise RuntimeError(f"PDF generation not available: {e}")

TEMPLATE_PATH = "static/Certificates_Master.pdf"

@csrf_exempt
def generate_all_certificates(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        data = json.loads(request.body or "{}")
        student = data.get("student", {}) or {}

        full_name = student.get("full_name") or "Unnamed Student"
        end_date = student.get("end_date") or "N/A"
        osha_date = student.get("osha_completion_date") or "N/A"

        disc_text = (student.get("disc_assessment_type") or {}).get("type_name") or "N/A"
        sixteen_text = (student.get("sixteen_types_assessment") or {}).get("type_name") or "N/A"
        enneagram_text = (student.get("enneagram_result") or {}).get("result_name") or "N/A"

        # Build the map of page -> fields (1-based page numbers!)
        page_fields_map = {
    3: [  # Employment Portfolio Overview (was index=2)
        {"text": disc_text,      "coords": (510, 560), "align": "center", "fontsize": 8, "color": (0,0,0)},
        {"text": sixteen_text,   "coords": (510, 620), "align": "center", "fontsize": 8, "color": (0,0,0)},
        {"text": enneagram_text, "coords": (510, 675), "align": "center", "fontsize": 8, "color": (0,0,0)},
    ],
    5: [  # NCCER (was index=4)
        {"text": full_name, "coords": (400, 275), "align": "center", "fontsize": 30, "color": (1,0,0)},
        {"text": end_date,  "coords": (392, 440), "align": "center", "fontsize": 14, "color": (0,0,0)},
    ],
    6: [  # OSHA (was index=5)
        {"text": full_name, "coords": (450, 290), "align": "center", "fontsize": 40, "color": (1,0,0)},
        {"text": osha_date, "coords": (650, 470), "align": "center", "fontsize": 14, "color": (0,0,0)},
    ],
    7: [  # HammerMath (was index=6)
        {"text": full_name, "coords": (385, 375), "align": "center", "fontsize": 30, "color": (1,0,0)},
        {"text": end_date,  "coords": (560, 545), "align": "center", "fontsize": 14, "color": (0,0,0)},
    ],
    8: [  # Employability (was index=7)
        {"text": full_name, "coords": (390, 350), "align": "center", "fontsize": 30, "color": (1,0,0)},
        {"text": end_date,  "coords": (555, 500), "align": "center", "fontsize": 14, "color": (0,0,0)},
    ],
    9: [  # Workforce (was index=8)
        {"text": full_name, "coords": (450, 360), "align": "center", "fontsize": 40, "color": (1,0,0)},
        {"text": end_date,  "coords": (550, 475), "align": "center", "fontsize": 14, "color": (0,0,0)},
    ],
}

        generate_master_pdf_pymupdf = _get_master_pdf_generator()
        return generate_master_pdf_pymupdf(
            TEMPLATE_PATH,
            page_fields_map,
            filename=f"Certificates_Master_{full_name.replace(' ', '_')}.pdf"
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
