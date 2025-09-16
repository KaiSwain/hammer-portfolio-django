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
    
    "PRONOUNS & GENDER: Check the 'gender' field in the data:\n"
    "- If gender is 'Female' or 'Woman': Use she/her pronouns throughout\n"
    "- If gender is 'Male' or 'Man': Use he/him pronouns throughout\n" 
    "- If gender is null/None/empty: Use they/them pronouns throughout\n"
    "- For any other gender identity: Use they/them pronouns\n"
    "Be consistent with pronoun usage throughout the entire summary.\n"
    
    "Style: clear, professional yet engaging, 9th–11th grade; concrete behaviors, not vague traits. Make it interesting!\n\n"

    "The \"html\" value must be CLEAN BODY HTML (no <html>, <head>, or <body> tags). Use semantic headings/lists only—no inline CSS.\n\n"

    "Structure EXACTLY (make each section concise and engaging):\n"
    "- Brief <p> intro (1-2 sentences) highlighting their unique personality blend.\n"
    "<h2>Workstyle & Communication</h2>\n"
    "  <p>1-2 sentences about their work approach and communication style.</p>\n"
    "  <ul><li>3-4 bullets of specific behaviors and strengths.</li></ul>\n"
    "<h2>Motivators & Learning Style</h2>\n"
    "  <p>1-2 sentences about what energizes them.</p>\n"
    "  <ul><li>3-4 bullets about feedback preferences and learning approaches.</li></ul>\n"
    "<h2>Best-Fit Environment</h2>\n"
    "  <p>1-2 sentences about their ideal work setting.</p>\n"
    "  <ul><li>3-4 bullets about tools and support that helps them thrive.</li></ul>\n"
    "<h2>Management Tips</h2>\n"
    "  <p>4-5 specific, actionable employer recommendations in paragraph form.</p>\n\n"

    "Length: 400-450 words MAX (strictly enforced - count carefully). Use dynamic, positive language while staying professional. "
    "Be specific to their actual assessment results. MUST fit on one page.\n\n"
    
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
        print(f"[AI] Raw response (last 200 chars): ...{content[-200:]}")
        
        # Try to parse as JSON
        try:
            data = json.loads(content)
            if isinstance(data, dict) and "html" in data:
                html_content = data["html"]
                print(f"[AI] Extracted HTML (first 300 chars): {html_content[:300]}...")
                return html_content
            else:
                print(f"[AI] JSON parsed but no 'html' key found. Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                return _create_error_content("Invalid JSON structure - missing 'html' key", "Student")
        except json.JSONDecodeError as e:
            print(f"[AI] JSON decode error: {e}")
            print(f"[AI] Attempting to extract HTML from malformed response...")
            # Try to find HTML content even if JSON is malformed
            import re
            html_match = re.search(r'"html":\s*"([^"]*(?:\\.[^"]*)*)"', content)
            if html_match:
                html_content = html_match.group(1).replace('\\"', '"').replace('\\n', '\n')
                print(f"[AI] Extracted HTML via regex (first 300 chars): {html_content[:300]}...")
                return html_content
            else:
                print(f"[AI] Could not extract HTML from malformed JSON")
                return _create_error_content(f"JSON parsing failed: {str(e)}", "Student")
    except Exception as e:
        print(f"[AI] Unexpected error in _safe_extract_html: {e}")
        return _create_error_content(f"Unexpected error: {str(e)}", "Student")

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
    """
    Ensure content fits on one page - silently trim if needed without showing truncation message.
    """
    print(f"[AI] Content length: {len(html)} characters")
    
    # If content is too long, silently trim it at natural breaking points
    if len(html) > 4500:  # Conservative limit for one page
        print(f"[AI] Content too long ({len(html)} chars), silently trimming...")
        
        # Try to find a good natural breaking point (end of a section)
        sections = html.split('<h2>')
        if len(sections) > 1:
            # Keep intro + first 3 sections maximum
            trimmed = sections[0]  # intro
            section_count = 0
            for section in sections[1:]:
                if section_count < 3 and len(trimmed + '<h2>' + section) < 4200:
                    trimmed += '<h2>' + section
                    section_count += 1
                else:
                    break
            
            print(f"[AI] Trimmed to {len(trimmed)} characters, {section_count + 1} sections")
            return trimmed
        else:
            # If no sections to split, trim at sentence boundaries
            sentences = html.split('.</p>')
            trimmed = ""
            for sentence in sentences:
                if len(trimmed + sentence + '.</p>') < 4200:
                    trimmed += sentence + '.</p>'
                else:
                    break
            print(f"[AI] Trimmed to {len(trimmed)} characters at sentence boundary")
            return trimmed
    
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
    Convert HTML to PDF using ReportLab - Clean, minimal design matching Cameron Hall PDF
    Single page format with simple, readable styling
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.colors import HexColor
    except ImportError as e:
        raise Exception(f"ReportLab not available: {e}")
    
    buffer = BytesIO()
    
    # Create PDF document with minimal margins for maximum content space
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=30,
        bottomMargin=30
    )
    
    # Simple, clean colors - minimal palette
    dark_text = HexColor('#1a202c')      # Rich dark gray
    medium_text = HexColor('#2d3748')    # Medium gray  
    light_text = HexColor('#718096')     # Light gray for dates
    section_text = HexColor('#2c5282')   # Subtle blue for headings
    
    # Get base styles
    styles = getSampleStyleSheet()
    
    # Clean, elegant styles matching Cameron Hall PDF
    title_style = ParagraphStyle(
        'CleanTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=6,
        spaceBefore=0,
        alignment=1,  # Center
        textColor=dark_text,
        fontName='Helvetica-Bold'
    )
    
    name_style = ParagraphStyle(
        'CleanName',
        parent=styles['Heading2'],
        fontSize=15,
        spaceAfter=4,
        spaceBefore=2,
        alignment=1,  # Center
        textColor=section_text,
        fontName='Helvetica-Bold'
    )
    
    date_style = ParagraphStyle(
        'CleanDate',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=18,
        alignment=1,  # Center
        textColor=light_text,
        fontName='Helvetica-Oblique'
    )
    
    section_style = ParagraphStyle(
        'CleanSection',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=5,
        spaceBefore=12,
        textColor=section_text,
        fontName='Helvetica-Bold',
        leftIndent=0
    )
    
    body_style = ParagraphStyle(
        'CleanBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
        spaceBefore=1,
        alignment=0,  # Left
        textColor=dark_text,
        fontName='Helvetica',
        leftIndent=0,
        rightIndent=0,
        leading=12
    )
    
    bullet_style = ParagraphStyle(
        'CleanBullet',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=3,
        alignment=0,
        textColor=dark_text,
        fontName='Helvetica',
        leftIndent=15,
        leading=12
    )
    
    # Create story (content)
    story = []
    
    # Simple, clean header
    story.append(Paragraph("Personality Summary", title_style))
    story.append(Paragraph(student_name, name_style))
    
    # Add generation date
    from datetime import datetime
    story.append(Paragraph(datetime.now().strftime('%B %d, %Y'), date_style))
    
    # Parse and add content with minimal styling
    lines = html_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a heading (contains <h2> tags)
        if '<h2>' in line and '</h2>' in line:
            section_title = re.sub(r'<[^>]+>', '', line)
            section_title = unescape(section_title)
            story.append(Paragraph(section_title, section_style))
            
        elif '<p>' in line:
            # This is a paragraph
            paragraph_text = re.sub(r'<[^>]+>', '', line)
            paragraph_text = unescape(paragraph_text)
            if paragraph_text:
                # Only fix spacing issues, don't mess with regular spaces
                paragraph_text = re.sub(r'\.([A-Z][a-z])', r'. \1', paragraph_text)  # Fix "word.Another" but not "Jr."
                paragraph_text = re.sub(r'!([A-Z][a-z])', r'! \1', paragraph_text)  # Fix "great!This" 
                paragraph_text = re.sub(r'\?([A-Z][a-z])', r'? \1', paragraph_text)  # Fix "why?Because"
                # Clean up double spaces that might be created
                paragraph_text = re.sub(r'  +', ' ', paragraph_text)  # Multiple spaces to single space
                story.append(Paragraph(paragraph_text, body_style))
                
        elif '<li>' in line:
            # This is a list item - simple bullet
            item_text = re.sub(r'<[^>]+>', '', line)
            item_text = unescape(item_text)
            if item_text:
                # Same gentle spacing fixes for list items
                item_text = re.sub(r'\.([A-Z][a-z])', r'. \1', item_text)
                item_text = re.sub(r'!([A-Z][a-z])', r'! \1', item_text)
                item_text = re.sub(r'\?([A-Z][a-z])', r'? \1', item_text)
                item_text = re.sub(r'  +', ' ', item_text)  # Clean up multiple spaces
                story.append(Paragraph(f"• {item_text}", bullet_style))
    
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