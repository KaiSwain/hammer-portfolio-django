# hammer_backendapi/views/ai_summary_view.py
"""
Django view for AI Summary generation endpoint - with PDF support
"""
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from hammer_backendapi.models import Student
from .ai_summary_fixed import generate_long_summary_html
from io import BytesIO
import re
from html import unescape

logger = logging.getLogger(__name__)

def html_to_pdf_reportlab(html_content: str, student_name: str) -> bytes:
    """
    Convert HTML to PDF using ReportLab - Railway compatible
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.colors import HexColor
    except ImportError as e:
        raise Exception(f"ReportLab not available: {e}")
    
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles for the personality summary
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center
        textColor=HexColor('#2563eb')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=HexColor('#1f2937')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        alignment=0  # Left
    )
    
    # Create story (content)
    story = []
    
    # Add title
    story.append(Paragraph("🏗️ PERSONALITY SUMMARY 🏗️", title_style))
    story.append(Paragraph(f"<b>{student_name}</b>", heading_style))
    
    # Add generation date
    from datetime import datetime
    story.append(Paragraph(f"<i>Generated on {datetime.now().strftime('%m/%d/%Y')}</i>", normal_style))
    story.append(Spacer(1, 20))
    
    # Parse and add content
    lines = html_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a heading (contains <h2> tags)
        if '<h2>' in line and '</h2>' in line:
            section_title = re.sub(r'<[^>]+>', '', line)
            section_title = unescape(section_title)
            story.append(Spacer(1, 15))
            story.append(Paragraph(section_title, heading_style))
        elif '<p>' in line:
            # This is a paragraph
            paragraph_text = re.sub(r'<[^>]+>', '', line)
            paragraph_text = unescape(paragraph_text)
            if paragraph_text:
                story.append(Paragraph(paragraph_text, normal_style))
                story.append(Spacer(1, 5))
        elif '<li>' in line:
            # This is a list item
            item_text = re.sub(r'<[^>]+>', '', line)
            item_text = unescape(item_text)
            if item_text:
                story.append(Paragraph(f"• {item_text}", normal_style))
    
    # Build PDF
    doc.build(story)
    
    # Get the PDF bytes
    buffer.seek(0)
    return buffer.getvalue()

@csrf_exempt
@require_http_methods(["POST"])
def generate_ai_summary(request):
    """
    Generate AI personality summary PDF for a student.
    
    Expected POST data:
    {
        "student_id": 123
    }
    
    Returns:
    PDF file download with filename based on student name
    """
    try:
        # Parse request data
        data = json.loads(request.body)
        student_id = data.get("student_id")
        
        if not student_id:
            return JsonResponse({
                "success": False,
                "error": "student_id is required"
            }, status=400)
        
        # Get student
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return JsonResponse({
                "success": False,
                "error": f"Student with ID {student_id} not found"
            }, status=404)
        
        logger.info(f"Generating AI summary PDF for student: {student.full_name}")
        
        # Generate HTML summary
        html_content = generate_long_summary_html(student)
        
        # Check if generation was successful
        if "AI Summary Generation Issue" in html_content:
            # Return error as JSON
            return JsonResponse({
                "success": False,
                "error": "AI summary generation failed",
                "html": html_content,
                "student_name": student.full_name
            }, status=500)

        # Generate PDF from HTML using Railway-compatible ReportLab
        try:
            logger.info("Starting PDF generation with ReportLab...")
            pdf_bytes = html_to_pdf_reportlab(html_content, student.full_name)
            logger.info(f"PDF generated successfully, size: {len(pdf_bytes)} bytes")
            
            # Create filename based on student name
            safe_name = "".join(c for c in student.full_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            filename = f"personality_summary_{safe_name}.pdf"
            
            # Return PDF as download
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = len(pdf_bytes)
            
            logger.info(f"AI summary PDF generated successfully for {student.full_name}")
            return response
            
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}", exc_info=True)
            # Fall back to JSON response for debugging
            return JsonResponse({
                "success": True,
                "html_content": html_content,
                "student_name": student.full_name,
                "student_id": student_id,
                "error": f"PDF generation failed: {str(e)}",
                "note": "Returning HTML content as fallback"
            })
        
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "error": "Invalid JSON in request body"
        }, status=400)
    
    except Exception as e:
        logger.error(f"Error generating AI summary: {str(e)}", exc_info=True)
        return JsonResponse({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def test_ai_connection(request):
    """
    Test endpoint to verify OpenAI connection works.
    """
    try:
        from .ai_summary_fixed import test_openai_connection
        
        success, message = test_openai_connection()
        
        return JsonResponse({
            "success": success,
            "message": message,
            "endpoint": "AI connection test"
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e),
            "endpoint": "AI connection test"
        }, status=500)