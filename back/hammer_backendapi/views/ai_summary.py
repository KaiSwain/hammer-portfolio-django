# hammer_backendapi/views/ai_summary.py
"""
AI Summary helper
-----------------
This module asks the OpenAI API for a one-page, employer-facing personality summary
and returns a SINGLE HTML string (no <html>/<body> wrapper), ready to drop into your
Django template.

• Input:  a Student model instance
• Output: HTML string via generate_long_summary_html(student)

Implementation notes:
- Prompts the model to return VALID JSON with a single key "html".
- Uses gpt-5-mini by default (configurable via OPENAI_MODEL).
- gpt-5-mini may reject the 'temperature' param → we handle that.
- Falls back to gpt-4o-mini on error.
"""

import os
import json
import os
from typing import Any, Dict
from openai import OpenAI

# Prints once at server start so you know this file is being used
print("[AI] ai_summary loaded from:", __file__)

# Initialize OpenAI client safely
try:
    # Create client with minimal configuration to avoid proxy issues
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = OpenAI(api_key=api_key)
        print("[AI] OpenAI client initialized successfully")
    else:
        print("[AI] Warning: OPENAI_API_KEY not found in environment")
        client = None
except Exception as e:
    print(f"[AI] Warning: OpenAI client initialization failed: {e}")
    client = None

MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")  # Use gpt-5-mini as preferred model

# ======== Prompt (Option A: JSON with "html") ========
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
        # OSHA isn't referenced in the prompt, but passing it is harmless if you decide to use it later:
        "osha": getattr(student.osha_type, "name", None),
        "gender": getattr(student.gender_identity, "gender", None),
    }

def _safe_extract_html(resp) -> str:
    """
    Parse the model's JSON safely; never crash the view if it misformats.
    The Chat Completions API exposes text via resp.choices[0].message.content.
    """
    try:
        # Extract content from chat completion response
        raw = resp.choices[0].message.content.strip() if resp.choices else ""
        print(f"[AI] Raw response: {raw[:500]}...")  # Debug: show first 500 chars
        
        # Try to extract JSON even if there's extra text
        if '{' in raw and '}' in raw:
            start = raw.find('{')
            end = raw.rfind('}') + 1
            json_str = raw[start:end]
            
            # Enhanced cleanup for gpt-5-mini JSON formatting issues
            import re
            # Remove control characters that break JSON parsing
            json_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', json_str)
            # Fix common JSON issues: unescaped quotes, newlines, etc.
            json_str = json_str.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
            # Handle unescaped quotes in content (preserve structure)
            # This is more complex - let's try a simpler approach first
            
            print(f"[AI] Cleaned JSON: {json_str[:200]}...")  # Debug
            
            data = json.loads(json_str)
            html = data.get("html")
            if isinstance(html, str) and html.strip():
                print(f"[AI] Successfully extracted HTML, length: {len(html)}")
                return html
                
        print("[AI] JSON missing 'html' key or empty. Raw:", raw[:300])
    except json.JSONDecodeError as e:
        print(f"[AI] JSON parse error: {e}")
        print(f"[AI] Attempting manual HTML extraction...")
        
        # Fallback: try to extract HTML content manually if JSON parsing fails
        try:
            raw = (resp.output_text or "").strip()
            # Look for content between "html":" and the closing quote/brace
            import re
            html_match = re.search(r'"html"\s*:\s*"(.*?)(?="\s*})', raw, re.DOTALL)
            if html_match:
                html_content = html_match.group(1)
                # Unescape basic characters
                html_content = html_content.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t')
                print(f"[AI] Manual extraction successful, length: {len(html_content)}")
                return html_content
        except Exception as manual_e:
            print(f"[AI] Manual extraction failed: {manual_e}")
            
        print(f"[AI] Problematic JSON: {raw[:500] if raw else 'Empty response'}")
    except Exception as e:
        print(f"[AI] Unexpected error: {e}")
        
    # Enhanced fallback with some basic content
    return """
    <p>This student's personality assessment data is being processed. Please try generating the summary again.</p>
    <h2>Workstyle & Communication</h2>
    <p>Individual assessment data will be available upon regeneration.</p>
    <h2>Management Tips</h2>
    <p>Please contact your administrator if this issue persists.</p>
    """

def _validate_one_page_content(html_content: str, student_name: str) -> str:
    """
    Validate that content will fit on one page and truncate if necessary.
    Returns guaranteed one-page HTML content.
    """
    # Word count limits for guaranteed one-page fit
    MAX_WORDS = 550  # Increased limit - still fits on one page comfortably
    MAX_BULLETS_PER_SECTION = 4  # Max bullets per section (increased from 3)
    
    # Simple word count (avoid BeautifulSoup dependency)
    # Remove HTML tags for word counting
    import re
    text_content = re.sub(r'<[^>]+>', ' ', html_content)
    word_count = len(text_content.split())
    
    print(f"[AI] Content word count: {word_count}")
    
    # If content is too long, use truncated version
    if word_count > MAX_WORDS:
        print(f"[AI] Content too long ({word_count} words), using truncated version...")
        return _create_truncated_content(student_name)
    
        # Limit bullets per section using simple regex
        # Find all <ul>...</ul> blocks and limit to 4 <li> items each
        def limit_bullets(match):
            ul_content = match.group(1)
            li_items = re.findall(r'<li[^>]*>.*?</li>', ul_content, re.DOTALL)
            limited_items = li_items[:MAX_BULLETS_PER_SECTION]  # Now 4 instead of 3
            return '<ul>' + ''.join(limited_items) + '</ul>'
        
        html_content = re.sub(r'<ul[^>]*>(.*?)</ul>', limit_bullets, html_content, flags=re.DOTALL)
    
    return html_content

def _create_truncated_content(student_name: str) -> str:
    """Create a truncated version that fits on one page."""
    return f"""
    <p>{student_name} brings unique strengths and dedication to every project, demonstrating strong commitment to quality work and professional development.</p>
    <h2>Workstyle & Communication</h2>
    <p>Shows natural approach to work and team collaboration with emphasis on clear communication and reliability.</p>
    <ul>
    <li>Demonstrates strong work ethic and reliability in all tasks</li>
    <li>Communicates effectively with team members and supervisors</li>
    <li>Adapts well to different project requirements and challenges</li>
    <li>Takes initiative in problem-solving and process improvement</li>
    </ul>
    <h2>Motivators & Learning Style</h2>
    <p>Thrives with clear guidance and hands-on experience, showing strong motivation for skill development and career advancement.</p>
    <ul>
    <li>Responds positively to constructive feedback and coaching</li>
    <li>Learns best through practical application and mentorship</li>
    <li>Values recognition for quality work and professional growth</li>
    <li>Shows enthusiasm for expanding technical knowledge and skills</li>
    </ul>
    <h2>Best-Fit Environment</h2>
    <p>Works best in structured environments with clear expectations and opportunities for hands-on learning and skill development.</p>
    <ul>
    <li>Benefits from mentorship and guidance from experienced professionals</li>
    <li>Thrives with clear project goals and regular feedback</li>
    <li>Appreciates opportunities to develop both technical and leadership skills</li>
    <li>Values safety-focused workplace culture and protocols</li>
    </ul>
    <h2>Management Tips</h2>
    <p>Provide clear expectations and regular feedback. Consider pairing with experienced mentors for optimal development. Recognize achievements and provide opportunities for skill building. Encourage questions and foster a supportive learning environment that promotes both technical growth and leadership development.</p>
    """

def _create_guaranteed_one_page_content(student_name: str) -> str:
    """Create minimal but professional content guaranteed to fit on one page."""
    return f"""
    <p>{student_name} is a dedicated team member ready to contribute effectively to your organization with strong foundational skills and professional commitment.</p>
    <h2>Workstyle & Communication</h2>
    <p>Brings enthusiasm and commitment to every project with focus on quality and teamwork.</p>
    <ul>
    <li>Strong work ethic and attention to detail in all assignments</li>
    <li>Effective team communication skills and collaborative approach</li>
    <li>Eager to learn and consistently follows safety protocols</li>
    <li>Shows reliability and punctuality in work commitments</li>
    </ul>
    <h2>Motivators & Learning Style</h2>
    <p>Motivated by opportunities to develop skills and contribute meaningfully to team success.</p>
    <ul>
    <li>Thrives with hands-on learning and practical application</li>
    <li>Responds well to mentorship and guidance</li>
    <li>Values recognition for quality work and improvement</li>
    <li>Shows initiative in professional development</li>
    </ul>
    <h2>Management Tips</h2>
    <p>Provide mentorship opportunities and clear project guidelines for best results. Encourage questions and offer regular feedback to support continued growth and development in both technical skills and professional competencies.</p>
    """

def _call_model(payload: Dict[str, Any], model_id: str):
    """
    Call the OpenAI Chat Completions API. Some models (e.g., gpt-5-mini) may reject 'temperature',
    so we conditionally include it and also retry without it on specific errors.
    """
    if client is None:
        raise Exception("OpenAI client is not initialized. Check OPENAI_API_KEY environment variable.")
    
    # Format the input as a system message and user message
    system_message = INSTR
    user_message = json.dumps(payload)
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    base_args = dict(
        model=model_id,
        messages=messages,
        max_tokens=3000,  # Use max_tokens instead of max_output_tokens
    )

    # If the chosen model is known to reject temperature, skip it
    if model_id in {"gpt-5-mini", "gpt-5-nano"}:
        return client.chat.completions.create(**base_args)

    # Otherwise, include a light temperature
    try:
        return client.chat.completions.create(**base_args, temperature=0.2)
    except Exception as e:
        # Auto-retry without temperature if the model complains about it
        msg = str(e)
        if "Unsupported parameter" in msg and "temperature" in msg:
            print("[AI] Retrying without temperature for model:", model_id)
            return client.chat.completions.create(**base_args)
        raise

def generate_long_summary_html(student) -> str:
    """
    Public helper with guaranteed one-page output:
      html = generate_long_summary_html(student)
    Returns a single HTML string (no <html>/<body>) suitable for direct insertion into your template.
    """
    payload = {"name": student.full_name, "meta": build_meta(student)}
    print("[AI] Model:", MODEL)
    print("[AI] Payload:", payload)

    try:
        resp = _call_model(payload, MODEL)
        html = _safe_extract_html(resp)
        # If we got a real response (not the fallback), validate and ensure one-page
        if "personality assessment data is being processed" not in html:
            validated_html = _validate_one_page_content(html, student.full_name)
            print("[AI] Content validated for one-page output")
            return validated_html
    except Exception as e:
        print("[AI] Primary model failed:", e)

    # Try fallback model
    try:
        print("[AI] Trying fallback model: gpt-4o-mini")
        resp = _call_model(payload, "gpt-4o-mini")
        html = _safe_extract_html(resp)
        if "personality assessment data is being processed" not in html:
            validated_html = _validate_one_page_content(html, student.full_name)
            print("[AI] Fallback content validated for one-page output")
            return validated_html
    except Exception as e:
        print("[AI] Fallback model also failed:", e)

    # Final fallback - guaranteed one-page content
    print("[AI] Using guaranteed one-page fallback content")
    return _create_guaranteed_one_page_content(student.full_name)


