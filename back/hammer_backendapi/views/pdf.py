import os
import json
from io import BytesIO
from decimal import Decimal
from django.conf import settings
from django.http import FileResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from borb.pdf import PDF
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.geometry.rectangle import Rectangle

@csrf_exempt
def generate_certificate(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=405)

    try:
        data = json.loads(request.body)
        student = data.get("student", {})
        certificates = data.get("certificates", [])

        if not student or not certificates:
            return JsonResponse({"error": "Missing student data or certificates"}, status=400)

        template_path = os.path.join(settings.BASE_DIR, "static", "Certificates_Master.pdf")
        with open(template_path, "rb") as pdf_file:
            result = PDF.loads(pdf_file)
            doc = result[0] if isinstance(result, tuple) else result

        if doc is None:
            return JsonResponse({"error": "Failed to load PDF"}, status=500)

        # ✅ Coordinates for fields
        CERTIFICATE_COORDS = {
            "osha": {
                "page": 2,
                "fields": {
                    "full_name": Rectangle(Decimal(200), Decimal(400), Decimal(200), Decimal(30)),
                    "osha_completion_date": Rectangle(Decimal(200), Decimal(370), Decimal(200), Decimal(30)),
                },
            },
            "hammerMath": {
                "page": 4,
                "fields": {
                    "full_name": Rectangle(Decimal(200), Decimal(400), Decimal(200), Decimal(30)),
                    "posttest_score": Rectangle(Decimal(200), Decimal(370), Decimal(200), Decimal(30)),
                },
            },
        }

        for cert in certificates:
            if cert in CERTIFICATE_COORDS:
                page_index = CERTIFICATE_COORDS[cert]["page"]
                page = doc.get_page(page_index)
                layout = SingleColumnLayout(page)

                for field, rect in CERTIFICATE_COORDS[cert]["fields"].items():
                    value = str(student.get(field, ""))
                    p = Paragraph(value, font_size=14)
                    p._bounding_box = rect  # ✅ Hack for absolute positioning
                    layout.add(p)

        buffer = BytesIO()
        PDF.dumps(buffer, doc)
        buffer.seek(0)

        return FileResponse(buffer, content_type="application/pdf", as_attachment=True, filename="certificates.pdf")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
    