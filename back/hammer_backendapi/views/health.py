from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import datetime

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for monitoring"""
    return JsonResponse({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "service": "hammer-portfolio-backend"
    })

@csrf_exempt
@require_http_methods(["GET"])
def api_info(request):
    """API information endpoint"""
    return JsonResponse({
        "name": "Hammer Portfolio API",
        "version": "1.0.0",
        "description": "API for managing student portfolios and generating certificates",
        "endpoints": {
            "students": "/api/students/",
            "login": "/api/login/",
            "certificates": "/api/generate/",
            "details": "/api/details/",
            "health": "/api/health/",
        }
    })
