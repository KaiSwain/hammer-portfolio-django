#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to Python path
sys.path.append('/home/kaifer/workspace/hammer/hammer-portfolio-django/back')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hammer_backendproject.settings')
django.setup()

from hammer_backendapi.models import Student
from back.not_in_use.ai_summary import generate_long_summary_html
from hammer_backendapi.views.utils.pdf_utils import html_to_pdf_bytes
from django.template.loader import render_to_string
from django.utils import timezone

print("Testing PDF Generation for AI Summary...")
print("=" * 50)

try:
    # Get a student
    student = Student.objects.first()
    if not student:
        print("❌ No students found")
        exit(1)
    
    print(f"Testing with student: {student.full_name}")
    
    # Step 1: Generate AI HTML
    print("Step 1: Generating AI summary HTML...")
    summary_html = generate_long_summary_html(student)
    print(f"✅ AI HTML generated: {len(summary_html)} characters")
    
    # Step 2: Render Django template
    print("Step 2: Rendering Django template...")
    context = {
        "name": student.full_name,
        "generated_at": timezone.now().strftime("%B %d, %Y"),
        "summary_html": summary_html,
    }
    full_html = render_to_string("personality_summary.html", context)
    print(f"✅ Full HTML rendered: {len(full_html)} characters")
    
    # Step 3: Convert to PDF
    print("Step 3: Converting HTML to PDF...")
    pdf_bytes = html_to_pdf_bytes(full_html)
    print(f"✅ PDF generated: {len(pdf_bytes)} bytes")
    
    # Save to file for testing
    with open("/tmp/test_ai_summary.pdf", "wb") as f:
        f.write(pdf_bytes)
    print("✅ PDF saved to /tmp/test_ai_summary.pdf")
    
    print("\n✅ All steps successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("=" * 50)
