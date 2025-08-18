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
from typing import Any, Dict
from openai import OpenAI

# Prints once at server start so you know this file is being used
print("[AI] ai_summary loaded from:", __file__)

client = OpenAI()  # reads OPENAI_API_KEY from env
MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")  # default; we also support a fallback

# ======== Prompt (Option A: JSON with "html") ========
INSTR = (
  "You write one-page, employer-facing personality summaries for construction pre-apprenticeship students.\n"
  "Use ONLY the provided assessments (DISC, 16 Types, Enneagram). If any are null/unknown, omit them—do not guess.\n"
  "Style: clear, professional, 9th–11th grade; concrete behaviors, not vague traits. No filler.\n\n"

  "Return VALID JSON ONLY with a single key \"html\" whose value is CLEAN BODY HTML "
  "(no <html>, <head>, or <body> tags). Use semantic headings/lists only—no inline CSS.\n\n"

  "Distinctiveness rules (CRITICAL):\n"
  "• Explicitly tailor content to the actual types. Avoid generic boilerplate.\n"
  "• If DISC is present: reflect the PRIMARY/SECONDARY blend (e.g., D/I vs I/D) in tone and behaviors on site.\n"
  "• If 16 Types is present: use the E–I, S–N, T–F, J–P axes to shape workstyle (e.g., E=toolbox-talk energy; I=focus blocks; "
  "S=hands-on detail; N=pattern/optimization; T=objective metrics; F=people impact; J=checklists; P=adaptation).\n"
  "• If Enneagram is present: ground motivations (1=standards/principle, 2=support, 3=results, 4=authentic craft, 5=analysis, "
  "6=safety/contingency, 7=energy/variety, 8=decisive ownership, 9=harmony/steady pace).\n"
  

  "Structure EXACTLY:\n"
  "- Short <p> intro tying NAME to provided assessments (only those present).\n"
  "<h2>Natural Workstyle & Communication Strengths</h2>\n"
  "  <p>2–3 sentences tailored to types.</p>\n"
  "  <ul><li>3–5 bullets of concrete behaviors on a jobsite; vary verbs; type-specific.</li></ul>\n"
  "<h2>Motivators & Growth Mindset Indicators</h2>\n"
  "  <p>1–2 sentences about what energizes NAME, grounded in types.</p>\n"
  "  <ul><li>3–5 bullets (goals, feedback style, learning loops) tied to types.</li></ul>\n"
  "<h2>Best-Fit Environments & Learning Styles</h2>\n"
  "  <p>1–2 sentences about ideal crew/pace/process.</p>\n"
  "  <ul><li>3–5 bullets (tools, checklists, pairing, autonomy vs structure) tied to types.</li></ul>\n"
  "<h2>How to Support NAME as a New Hire</h2>\n"
  "  <p>4–6 employer tips with specificity (handoff rituals, metric cadence, coaching cues) aligned to types.</p>\n\n"

  "Length: ~350–450 words. No <h1> or dates. No speculation. Avoid generic phrases like "
  "\"detail-oriented,\" \"team player,\" \"strong communication\" unless qualified with type-specific context."
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
    The Responses API exposes text via resp.output_text.
    """
    try:
        raw = (resp.output_text or "").strip()
        data = json.loads(raw)
        html = data.get("html")
        if isinstance(html, str) and html.strip():
            return html
        print("[AI] JSON missing 'html' or empty. Raw:", raw[:300])
    except Exception as e:
        print("[AI] JSON parse error:", e)
    # Minimal fallback so you still return a usable PDF
    return "<h2>Summary Unavailable</h2><p>The AI response was not in the expected JSON format.</p>"

def _call_model(payload: Dict[str, Any], model_id: str):
    """
    Call the Responses API. Some models (e.g., gpt-5-mini) may reject 'temperature',
    so we conditionally include it and also retry without it on specific errors.
    """
    base_args = dict(
        model=model_id,
        instructions=INSTR,
        input=json.dumps(payload),
        max_output_tokens=3000,  # room for multi-page HTML if needed
    )

    # If the chosen model is known to reject temperature, skip it
    if model_id in {"gpt-5-mini", "gpt-5-nano"}:
        return client.responses.create(**base_args)

    # Otherwise, include a light temperature
    try:
        return client.responses.create(**base_args, temperature=0.2)
    except Exception as e:
        # Auto-retry without temperature if the model complains about it
        msg = str(e)
        if "Unsupported parameter" in msg and "temperature" in msg:
            print("[AI] Retrying without temperature for model:", model_id)
            return client.responses.create(**base_args)
        raise

def generate_long_summary_html(student) -> str:
    """
    Public helper:
      html = generate_long_summary_html(student)
    Returns a single HTML string (no <html>/<body>) suitable for direct insertion into your template.
    """
    payload = {"name": student.full_name, "meta": build_meta(student)}
    print("[AI] Model:", MODEL)
    print("[AI] Payload:", payload)

    try:
        resp = _call_model(payload, MODEL)
    except Exception as e:
        print("[AI] Primary model failed:", e)
        # Fallback to a widely-available model
        resp = _call_model(payload, "gpt-4o-mini")

    html = _safe_extract_html(resp)
    print("[AI] HTML length:", len(html))
    return html


