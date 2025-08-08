import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from hammer_backendapi.views.utils.pdf_utils import generate_certificate_pdf

TEMPLATE_PATH = "static/Certificates_Master.pdf"


# ===============================
# 1. Employment Portfolio Overview (Page 2)
# ===============================
@csrf_exempt
def generate_portfolio_certificate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        # 1) Get the posted data safely
        data = json.loads(request.body)
        student = data.get("student", {}) or {}

        # 2) Pull the three values we want. Because of depth=1,
        #    these are nested objects like:
        #    - disc_assessment_type: { "id": 1, "type_name": "Disc Type" }
        #    - sixteen_types_assessment: { "id": 1, "type_name": "16 Type" }
        #    - enneagram_result: { "id": 1, "result_name": "Enneagram Result" }

        disc_obj = student.get("disc_assessment_type")  # dict or None
        sixteen_obj = student.get("sixteen_types_assessment")  # dict or None
        enneagram_obj = student.get("enneagram_result")  # dict or None

        # 3) Safely convert to plain strings
        if isinstance(disc_obj, dict):
            disc_text = disc_obj.get("type_name") or "N/A"
        else:
            disc_text = "N/A"

        if isinstance(sixteen_obj, dict):
            sixteen_text = sixteen_obj.get("type_name") or "N/A"
        else:
            sixteen_text = "N/A"

        if isinstance(enneagram_obj, dict):
            enneagram_text = enneagram_obj.get("result_name") or "N/A"
        else:
            enneagram_text = "N/A"

        # 4) Build the fields list for your PDF drawer
        fields = [
            {"text": disc_text,     "coords": (510, 560), "align": "center", "fontsize": 16, "color": (0, 0, 0)},
            {"text": sixteen_text,  "coords": (510, 620), "align": "center", "fontsize": 16, "color": (0, 0, 0)},
            {"text": enneagram_text,"coords": (510, 675), "align": "center", "fontsize": 16, "color": (0, 0, 0)},
        ]

        # 5) Generate and return the PDF
        return generate_certificate_pdf(TEMPLATE_PATH, 2, fields, "portfolio_certificate.pdf")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ===============================
# 2. NCCER (Page 4)
# ===============================
@csrf_exempt
def generate_nccer_certificate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        data = json.loads(request.body)
        student = data.get("student", {})
        full_name = student.get("full_name", "")
        date = student.get("date", "")

        fields = [
            {
                "text": full_name,
                "coords": (400, 275),
                "align": "center",
                "fontsize": 18,
                "color": (1, 0, 0),
            },  # red
            {
                "text": date,
                "coords": (392, 440),
                "align": "center",
                "fontsize": 14,
                "color": (0, 0, 0),
            },
        ]

        return generate_certificate_pdf(
            TEMPLATE_PATH, 4, fields, "nccer_certificate.pdf"
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ===============================
# 3. OSHA (Page 5)
# ===============================
@csrf_exempt
def generate_osha_certificate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)
        student = data.get("student", {})
        full_name = student.get("full_name") or "Unnamed Student"
        date = student.get("osha_completion_date") or "N/A"

        fields = [
            {
                "text": full_name,
                "coords": (450, 290),
                "align": "center",
                "fontsize": 18,
                "color": (1, 0, 0),
            },
            {
                "text": date,
                "coords": (650, 470),
                "align": "center",
                "fontsize": 14,
                "color": (0, 0, 0),
            },
        ]

        return generate_certificate_pdf(
            TEMPLATE_PATH, 5, fields, "osha_certificate.pdf"
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ===============================
# 4. HammerMath (Page 6)
# ===============================
@csrf_exempt
def generate_hammermath_certificate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        data = json.loads(request.body)
        student = data.get("student", {})
        full_name = student.get("full_name", "")
        date = student.get("date", "")

        fields = [
            {
                "text": full_name,
                "coords": (385, 375),
                "align": "center",
                "fontsize": 18,
                "color": (1, 0, 0),
            },
            {
                "text": date,
                "coords": (560, 545),
                "align": "center",
                "fontsize": 14,
                "color": (0, 0, 0),
            },
        ]

        return generate_certificate_pdf(
            TEMPLATE_PATH, 6, fields, "hammermath_certificate.pdf"
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ===============================
# 5. Employability (Page 7)
# ===============================
@csrf_exempt
def generate_employability_certificate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        data = json.loads(request.body)
        student = data.get("student", {})
        full_name = student.get("full_name", "")
        date = student.get("date", "")

        fields = [
            {
                "text": full_name,
                "coords": (390, 350),
                "align": "center",
                "fontsize": 18,
                "color": (1, 0, 0),
            },
            {
                "text": date,
                "coords": (555, 500),
                "align": "center",
                "fontsize": 14,
                "color": (0, 0, 0),
            },
        ]

        return generate_certificate_pdf(
            TEMPLATE_PATH, 7, fields, "employability_certificate.pdf"
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ===============================
# 6. Workforce Development (Page 8)
# ===============================
@csrf_exempt
def generate_workforce_certificate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
    try:
        data = json.loads(request.body)
        student = data.get("student", {})
        full_name = student.get("full_name", "")
        date = student.get("date", "")

        fields = [
            {
                "text": full_name,
                "coords": (450, 360),
                "align": "center",
                "fontsize": 18,
                "color": (1, 0, 0),
            },
            {
                "text": date,
                "coords": (550, 475),
                "align": "center",
                "fontsize": 14,
                "color": (0, 0, 0),
            },
        ]

        return generate_certificate_pdf(
            TEMPLATE_PATH, 8, fields, "workforce_certificate.pdf"
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


