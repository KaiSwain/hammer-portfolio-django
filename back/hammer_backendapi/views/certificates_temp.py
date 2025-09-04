import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def generate_portfolio_certificate(request):
    """Temporary: PDF generation disabled due to library issues"""
    return JsonResponse({
        "error": "PDF generation temporarily unavailable",
        "message": "Certificate generation is being updated. Please try again later.",
        "status": "maintenance"
    }, status=503)

@csrf_exempt  
def generate_nccer_certificate(request):
    """Temporary: PDF generation disabled due to library issues"""
    return JsonResponse({
        "error": "PDF generation temporarily unavailable", 
        "message": "Certificate generation is being updated. Please try again later.",
        "status": "maintenance"
    }, status=503)

@csrf_exempt
def generate_osha_certificate(request):
    """Temporary: PDF generation disabled due to library issues"""
    return JsonResponse({
        "error": "PDF generation temporarily unavailable",
        "message": "Certificate generation is being updated. Please try again later.", 
        "status": "maintenance"
    }, status=503)

@csrf_exempt
def generate_hammermath_certificate(request):
    """Temporary: PDF generation disabled due to library issues"""
    return JsonResponse({
        "error": "PDF generation temporarily unavailable",
        "message": "Certificate generation is being updated. Please try again later.",
        "status": "maintenance"
    }, status=503)

@csrf_exempt
def generate_employability_certificate(request):
    """Temporary: PDF generation disabled due to library issues"""
    return JsonResponse({
        "error": "PDF generation temporarily unavailable",
        "message": "Certificate generation is being updated. Please try again later.",
        "status": "maintenance"
    }, status=503)

@csrf_exempt
def generate_workforce_certificate(request):
    """Temporary: PDF generation disabled due to library issues"""
    return JsonResponse({
        "error": "PDF generation temporarily unavailable",
        "message": "Certificate generation is being updated. Please try again later.",
        "status": "maintenance"
    }, status=503)
