import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

logger = logging.getLogger(__name__)

@csrf_exempt
def generate_all_certificates(request):
    """Temporary: PDF generation disabled due to library issues"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)
        
    return JsonResponse({
        "error": "PDF generation temporarily unavailable",
        "message": "Certificate generation is being updated. Please try again later.",
        "status": "maintenance"
    }, status=503)
