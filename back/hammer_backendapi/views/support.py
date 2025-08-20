from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def support_request(request):
    """
    Handle support requests from the frontend
    """
    try:
        data = json.loads(request.body)
        name = data.get('name', '')
        email = data.get('email', '')
        issue = data.get('issue', '')
        
        # Log the support request
        logger.info("Support Request - Name: %s, Email: %s, Issue: %s", name, email, issue)
        
        # In a real implementation, you might:
        # - Save to database
        # - Send email notification
        # - Create a ticket in a support system
        
        return JsonResponse({
            'success': True,
            'message': 'Support request received successfully. We will contact you soon.'
        })
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON in support request")
        return JsonResponse({
            'success': False,
            'message': 'Invalid request format.'
        }, status=400)
    except Exception as e:
        logger.error("Error processing support request: %s", str(e))
        return JsonResponse({
            'success': False,
            'message': 'Error processing support request. Please try again.'
        }, status=500)
