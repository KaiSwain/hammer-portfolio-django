# hammer_backendapi/views/ai_summary_fixed.py
"""
AI Summary helper - FIXED VERSION
---------------------------------
This module asks the OpenAI API for a one-page, employer-facing personality summary
and returns a SINGLE HTML string (no <html>/<body> wrapper), ready to drop into your
Django template.

• Input:  a Student model instance
• Output: HTML string via generate_long_summary_html(student)

Implementation notes:
- Clean OpenAI client initialization without proxy issues
- Uses gpt-4o-mini by default (configurable via OPENAI_MODEL)
- Proper error handling with fallbacks
- No proxy-related code that causes conflicts
"""

import os
import json
from django.conf import settings
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Student
from typing import Any, Dict
from django.conf import settings
import re
from html import unescape
from io import BytesIO

# Initialize OpenAI client safely - will be initialized when first needed
client = None

def get_openai_client():
    """Get or initialize OpenAI client lazily"""
    global client
    if client is not None:
        print("[AI] Returning existing client")
        return client
        
    try:
        print("[AI] Starting client initialization...")
        
        # Try multiple ways to get the API key
        api_key = None
        
        # Method 1: Direct environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"[AI] Method 1 - env var: {'Found' if api_key else 'Not found'}")
        
        # Method 2: Django settings (if available)
        if not api_key:
            try:
                api_key = getattr(settings, 'OPENAI_API_KEY', None)
                print(f"[AI] Method 2 - Django settings: {'Found' if api_key else 'Not found'}")
            except Exception as e:
                print(f"[AI] Method 2 failed: {e}")
        
        # Method 3: Python-decouple config
        if not api_key:
            try:
                from decouple import config
                api_key = config('OPENAI_API_KEY', default=None)
                print(f"[AI] Method 3 - decouple: {'Found' if api_key else 'Not found'}")
            except Exception as e:
                print(f"[AI] Method 3 failed: {e}")
        
        print(f"[AI] Final API key check: {'Yes' if api_key else 'No'}")
        if api_key:
            print(f"[AI] API key starts with: {api_key[:10]}...")
            print(f"[AI] API key length: {len(api_key)}")
        
        if api_key:
            print("[AI] Attempting to import OpenAI...")
            try:
                from openai import OpenAI
                print("[AI] OpenAI import successful")
                
                print("[AI] Creating OpenAI client...")
                # Clean initialization - newer OpenAI version should handle proxies correctly
                client = OpenAI(api_key=api_key)
                print("[AI] OpenAI client created successfully")
                print(f"[AI] Client type: {type(client)}")
                
                # Test if client has required attributes
                if hasattr(client, 'chat'):
                    print("[AI] Client has chat attribute")
                else:
                    print("[AI] WARNING: Client missing chat attribute")
                
                return client
                
            except ImportError as e:
                print(f"[AI] OpenAI import failed: {e}")
                return None
            except Exception as e:
                print(f"[AI] Client creation failed: {e}")
                import traceback
                traceback.print_exc()
                return None
        else:
            print("[AI] Warning: OPENAI_API_KEY not found in any source")
            return None
            
    except Exception as e:
        print(f"[AI] OpenAI initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return None

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Prompt for generating personality summaries
INSTR = (
    "You MUST return ONLY valid JSON with exactly this format: {\"html\": \"your_html_content_here\"}\n\n"
    
    "You write engaging, one-page personality summaries for construction pre-apprenticeship students.\n"
    "Use ONLY the provided assessments (DISC, 16 Types, Enneagram). If any are null/unknown, omit them—do not guess.\n"
    
    "Style: clear, professional yet engaging, 9th–11th grade; concrete behaviors, not vague traits. Make it interesting!\n\n"

    "The \"html\" value must be CLEAN BODY HTML (no <html>, <head>, or <body> tags). Use semantic headings/lists only—no inline CSS.\n\n"

    "Structure EXACTLY (make each section substantial and engaging):\n"
    "- Detailed <p> intro (2-3 sentences) highlighting their unique personality blend from assessments present.\n"
    "<h2>Workstyle & Communication</h2>\n"
    "  <p>2-3 sentences about their natural work approach and communication style with specific examples.</p>\n"
    "  <ul><li>4-5 bullets of specific on-site behaviors and strengths with concrete examples.</li></ul>\n"
    "<h2>Motivators & Learning Style</h2>\n"
    "  <p>2-3 sentences about what energizes and drives them with specific details.</p>\n"
    "  <ul><li>4-5 bullets about feedback preferences and learning approaches with examples.</li></ul>\n"
    "<h2>Best-Fit Environment</h2>\n"
    "  <p>2-3 sentences about their ideal work setting and team dynamics with specifics.</p>\n"
    "  <ul><li>4-5 bullets about tools, structure, and support that helps them thrive.</li></ul>\n"
    "<h2>Management Tips</h2>\n"
    "  <p>5-7 specific, actionable employer recommendations based on their assessment types with concrete examples.</p>\n\n"

    "Length: 500-550 words MAX (strictly enforced). Use dynamic, positive language while staying professional. "
    "Be specific to their actual assessment results. Make it feel personal and valuable to employers.\n\n"
    
    "CRITICAL: Your response must be ONLY the JSON object, nothing else. No explanations, no markdown, just the JSON."
)

def build_meta(student) -> Dict[str, Any]:
    """Collect the fields we pass to the model (omit/None for unknowns)."""
    return {
        "disc": getattr(student.disc_assessment_type, "type_name", None),
        "sixteen": getattr(student.sixteen_types_assessment, "type_name", None),
        "enneagram": getattr(student.enneagram_result, "result_name", None),
        "osha": getattr(student.osha_type, "name", None),
        "gender": getattr(student.gender_identity, "gender", None),
    }

def _safe_extract_html(response_content: str) -> str:
    """
    Parse the model's JSON response safely and extract HTML content.
    """
    try:
        # Clean the response
        content = response_content.strip()
        print(f"[AI] Raw response (first 200 chars): {content[:200]}...")
        
        # Try to extract JSON
        if '{' in content and '}' in content:
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            
            # Parse JSON
            data = json.loads(json_str)
            html = data.get("html")
            
            if isinstance(html, str) and html.strip():
                print(f"[AI] Successfully extracted HTML, length: {len(html)}")
                return html.strip()
                
        print("[AI] JSON missing 'html' key or empty")
        
    except json.JSONDecodeError as e:
        print(f"[AI] JSON parse error: {e}")
    except Exception as e:
        print(f"[AI] Unexpected error: {e}")
        
    # Fallback content
    return """
    <p>This student's personality assessment data is being processed. Please try generating the summary again.</p>
    <h2>Workstyle & Communication</h2>
    <p>Individual assessment data will be available upon regeneration.</p>
    <h2>Management Tips</h2>
    <p>Please contact your administrator if this issue persists.</p>
    """

def _create_error_content(error_msg: str, student_name: str) -> str:
    """Create a helpful error message in HTML format."""
    return f"""
    <p><strong>AI Summary Generation Issue for {student_name}</strong></p>
    <p>Error: {error_msg}</p>
    <h2>Troubleshooting</h2>
    <ul>
        <li>Check OpenAI API key configuration</li>
        <li>Verify network connectivity</li>
        <li>Contact system administrator if issue persists</li>
    </ul>
    """

def _validate_content_length(html: str, student_name: str) -> str:
    """Ensure the content is appropriate length for one page."""
    if len(html) > 4000:  # Rough estimate for one page
        print(f"[AI] Content too long ({len(html)} chars), truncating...")
        # Find a good place to truncate
        sentences = html.split('.</p>')
        truncated = ""
        for sentence in sentences:
            if len(truncated + sentence) < 3500:
                truncated += sentence + '.</p>'
            else:
                break
        return truncated + "\n<p><em>Summary truncated for length.</em></p>"
    return html

def _call_openai_api(payload: dict, model_id: str = None) -> str:
    """
    Make a clean call to OpenAI API without any proxy complications.
    """
    client = get_openai_client()
    if client is None:
        raise Exception("OpenAI client is not initialized. Check OPENAI_API_KEY.")
    
    if model_id is None:
        model_id = MODEL
    
    # Format messages
    messages = [
        {"role": "system", "content": INSTR},
        {"role": "user", "content": json.dumps(payload)}
    ]
    
    try:
        # Clean API call with minimal parameters
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=3000,
            temperature=0.7
        )
        
        # Extract content
        content = response.choices[0].message.content
        return content
        
    except Exception as e:
        print(f"[AI] OpenAI API call failed: {type(e).__name__}: {str(e)}")
        raise

def generate_long_summary_html(student) -> str:
    """
    Public helper that generates AI personality summary for a student.
    Returns HTML string suitable for direct insertion into templates.
    """
    print(f"[AI] Generating summary for student: {student.full_name}")
    
    # Check API key availability
    api_key = os.getenv("OPENAI_API_KEY") or getattr(settings, 'OPENAI_API_KEY', None)
    if not api_key:
        error_msg = "OpenAI API key not configured"
        print(f"[AI] Error: {error_msg}")
        return _create_error_content(error_msg, student.full_name)
    
    # Check client initialization
    client = get_openai_client()
    if client is None:
        error_msg = "OpenAI client failed to initialize"
        print(f"[AI] Error: {error_msg}")
        return _create_error_content(error_msg, student.full_name)
    
    # Build payload
    payload = {
        "name": student.full_name,
        "meta": build_meta(student)
    }
    
    print(f"[AI] Using model: {MODEL}")
    print(f"[AI] Payload: {payload}")
    
    # Try primary model
    try:
        print(f"[AI] Attempting primary model call: {MODEL}")
        response_content = _call_openai_api(payload, MODEL)
        html = _safe_extract_html(response_content)
        
        # Check if we got a real response
        if "personality assessment data is being processed" not in html:
            validated_html = _validate_content_length(html, student.full_name)
            print("[AI] Primary model successful")
            return validated_html
            
    except Exception as e:
        print(f"[AI] Primary model failed: {type(e).__name__}: {str(e)}")
        
        # Check for specific error types
        error_str = str(e).lower()
        if "authentication" in error_str or "api_key" in error_str:
            return _create_error_content(f"OpenAI API key authentication failed: {str(e)}", student.full_name)
        elif "rate_limit" in error_str or "quota" in error_str:
            return _create_error_content(f"OpenAI API rate limit exceeded: {str(e)}", student.full_name)
    
    # Try fallback model
    try:
        print("[AI] Trying fallback model: gpt-4o-mini")
        response_content = _call_openai_api(payload, "gpt-4o-mini")
        html = _safe_extract_html(response_content)
        
        if "personality assessment data is being processed" not in html:
            validated_html = _validate_content_length(html, student.full_name)
            print("[AI] Fallback model successful")
            return validated_html
            
    except Exception as e:
        print(f"[AI] Fallback model also failed: {type(e).__name__}: {str(e)}")
    
    # Final fallback
    print("[AI] All attempts failed - returning error message")
    return _create_error_content(
        "AI summary generation temporarily unavailable. Please try again later or contact support.",
        student.full_name
    )

def convert_html_to_pdf_reportlab(html_content: str, student_name: str) -> bytes:
    """
    Convert HTML to PDF using ReportLab - Modern, clean, friendly design
    One-page format with professional styling
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.colors import HexColor, Color
        from reportlab.lib.units import inch
        from reportlab.lib import colors
    except ImportError as e:
        raise Exception(f"ReportLab not available: {e}")
    
    buffer = BytesIO()
    
    # Create PDF document with optimized margins
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=35,
        bottomMargin=35
    )
    
    # Modern color palette
    primary_blue = HexColor('#3B82F6')      # Modern blue
    secondary_blue = HexColor('#1E40AF')    # Darker blue
    accent_orange = HexColor('#F59E0B')     # Warm orange
    text_dark = HexColor('#1F2937')         # Dark gray
    text_medium = HexColor('#6B7280')       # Medium gray
    text_light = HexColor('#9CA3AF')        # Light gray
    success_green = HexColor('#10B981')     # Success green
    
    # Get base styles
    styles = getSampleStyleSheet()
    
    # Custom modern styles
    header_style = ParagraphStyle(
        'ModernHeader',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=8,
        alignment=1,  # Center
        textColor=primary_blue,
        fontName='Helvetica-Bold'
    )
    
    name_style = ParagraphStyle(
        'ModernName',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=5,
        spaceBefore=2,
        alignment=1,  # Center
        textColor=text_dark,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'ModernSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=20,
        alignment=1,  # Center
        textColor=text_medium,
        fontName='Helvetica-Oblique'
    )
    
    section_header_style = ParagraphStyle(
        'ModernSectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        spaceAfter=8,
        spaceBefore=15,
        textColor=secondary_blue,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderColor=primary_blue,
        borderPadding=0,
        leftIndent=0
    )
    
    body_style = ParagraphStyle(
        'ModernBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=0,  # Left
        textColor=text_dark,
        fontName='Helvetica',
        leftIndent=10,
        rightIndent=10,
        leading=12
    )
    
    bullet_style = ParagraphStyle(
        'ModernBullet',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
        alignment=0,  # Left
        textColor=text_dark,
        fontName='Helvetica',
        leftIndent=20,
        bulletIndent=10,
        leading=12
    )
    
    # Create story (content)
    story = []
    
    # Modern header with emoji and styling
    story.append(Paragraph("✨ PERSONALITY INSIGHTS ✨", header_style))
    story.append(Paragraph(f"{student_name}", name_style))
    
    # Add generation date with modern styling
    from datetime import datetime
    story.append(Paragraph(f"Generated {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    
    # Add a subtle separator line using a table
    separator_data = [['', '', '']]
    separator_table = Table(separator_data, colWidths=[2*inch, 1*inch, 2*inch])
    separator_table.setStyle(TableStyle([
        ('LINEBELOW', (1, 0), (1, 0), 2, primary_blue),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(separator_table)
    story.append(Spacer(1, 10))
    
    # Parse and add content with modern styling
    lines = html_content.split('\n')
    section_icons = {
        'personality': '🎯',
        'strengths': '💪',
        'communication': '💬',
        'leadership': '👑',
        'teamwork': '🤝',
        'work': '⚡',
        'career': '🚀',
        'development': '📈',
        'growth': '🌱',
        'skills': '🔧',
        'traits': '✨',
        'summary': '📋',
        'overview': '🔍',
        'profile': '👤'
    }
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a heading (contains <h2> tags)
        if '<h2>' in line and '</h2>' in line:
            section_title = re.sub(r'<[^>]+>', '', line)
            section_title = unescape(section_title)
            
            # Add appropriate icon based on section content
            icon = '🔸'  # Default icon
            section_lower = section_title.lower()
            for keyword, emoji in section_icons.items():
                if keyword in section_lower:
                    icon = emoji
                    break
            
            formatted_title = f"{icon} {section_title}"
            story.append(Paragraph(formatted_title, section_header_style))
            
        elif '<p>' in line:
            # This is a paragraph
            paragraph_text = re.sub(r'<[^>]+>', '', line)
            paragraph_text = unescape(paragraph_text)
            if paragraph_text:
                story.append(Paragraph(paragraph_text, body_style))
                
        elif '<li>' in line:
            # This is a list item with modern bullet styling
            item_text = re.sub(r'<[^>]+>', '', line)
            item_text = unescape(item_text)
            if item_text:
                # Use modern bullet point
                story.append(Paragraph(f"▸ {item_text}", bullet_style))
    
    # Add a footer with a motivational note
    story.append(Spacer(1, 15))
    
    footer_table = Table([['', '🌟 Embrace your unique strengths and continue growing! 🌟', '']], 
                        colWidths=[1*inch, 4*inch, 1*inch])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Oblique'),
        ('FONTSIZE', (1, 0), (1, 0), 9),
        ('TEXTCOLOR', (1, 0), (1, 0), accent_orange),
        ('LINEABOVE', (1, 0), (1, 0), 1, text_light),
        ('TOPPADDING', (1, 0), (1, 0), 8),
    ]))
    story.append(footer_table)
    
    # Build PDF
    doc.build(story)
    
    # Get the PDF bytes
    buffer.seek(0)
    return buffer.getvalue()

# Test function for debugging
def test_openai_connection():
    """Test function to verify OpenAI connection works."""
    try:
        client = get_openai_client()
        if client is None:
            return False, "Client not initialized"
            
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'test successful'"}],
            max_tokens=10
        )
        
        return True, response.choices[0].message.content
        
    except Exception as e:
        return False, str(e)

# Django REST API Views

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def generate_ai_summary(request):
    """Generate AI summary PDF for a student"""
    try:
        student_id = request.data.get('student_id')
        if not student_id:
            return Response({
                'success': False,
                'error': 'student_id is required'
            }, status=400)
            
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Student not found'
            }, status=404)
            
        # Generate the AI summary HTML
        html_content = generate_long_summary_html(student)
        
        # Check if HTML generation failed
        if "AI Summary Generation Issue" in html_content:
            return Response({
                'success': False,
                'error': 'AI summary generation failed',
                'html_content': html_content
            }, status=500)
        
        # Convert HTML to PDF using ReportLab (Railway compatible)
        try:
            pdf_bytes = convert_html_to_pdf_reportlab(html_content, student.full_name)
            
            # Create filename
            safe_name = "".join(c for c in student.full_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')
            filename = f"personality_summary_{safe_name}.pdf"
            
            # Return PDF as download
            from django.http import HttpResponse
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = len(pdf_bytes)
            
            return response
            
        except Exception as pdf_error:
            # PDF generation failed - return JSON with HTML content as fallback
            return Response({
                'success': True,
                'html_content': html_content,
                'student_name': student.full_name,
                'error': f'PDF generation failed: {str(pdf_error)}',
                'note': 'Returning HTML content as fallback'
            })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_ai_connection_api(request):
    """Test OpenAI API connection endpoint"""
    try:
        success, message = test_openai_connection()
        return Response({
            'success': success,
            'message': message
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_environment(request):
    """Debug endpoint to check environment variables"""
    try:
        import os
        debug_info = {}
        
        # Check for OpenAI key in various ways
        debug_info['openai_key_env'] = 'OPENAI_API_KEY' in os.environ
        debug_info['openai_key_length'] = len(os.getenv("OPENAI_API_KEY", "")) if os.getenv("OPENAI_API_KEY") else 0
        
        # Check Django settings
        try:
            debug_info['openai_key_settings'] = hasattr(settings, 'OPENAI_API_KEY')
        except:
            debug_info['openai_key_settings'] = False
        
        # List some environment variables (safely)
        env_keys = [key for key in os.environ.keys() if 'OPENAI' in key.upper()]
        debug_info['openai_env_keys'] = env_keys
        
        # Check for proxy environment variables
        proxy_keys = [key for key in os.environ.keys() if 'PROXY' in key.upper()]
        debug_info['proxy_env_keys'] = proxy_keys
        
        # Check specific proxy variables
        debug_info['http_proxy'] = os.getenv('HTTP_PROXY') is not None
        debug_info['https_proxy'] = os.getenv('HTTPS_PROXY') is not None
        debug_info['no_proxy'] = os.getenv('NO_PROXY') is not None
        
        # Check if we're in production
        debug_info['environment'] = os.getenv('DJANGO_DEBUG', 'unknown')
        debug_info['railway_env'] = os.getenv('RAILWAY_ENVIRONMENT', 'unknown')
        
        return Response({
            'success': True,
            'debug_info': debug_info
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        })