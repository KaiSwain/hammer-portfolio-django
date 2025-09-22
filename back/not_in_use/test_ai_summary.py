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

print("Testing AI Summary functionality...")
print("=" * 50)

# Test OpenAI client initialization
try:
    from back.not_in_use.ai_summary import client, MODEL
    print(f"OpenAI Client: {'✅ Initialized' if client else '❌ Not initialized'}")
    print(f"Model: {MODEL}")
    
    # Check environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key present: {'✅ Yes' if api_key else '❌ No'}")
    if api_key:
        print(f"API Key starts with: {api_key[:10]}...")
    
except Exception as e:
    print(f"❌ Error importing AI components: {e}")

print("\n" + "=" * 50)

# Test with a real student
try:
    students = Student.objects.all()[:1]
    if students:
        student = students[0]
        print(f"Testing with student: {student.full_name}")
        print("Generating AI summary...")
        
        html = generate_long_summary_html(student)
        print(f"✅ Generated HTML length: {len(html)} characters")
        print("First 200 characters:")
        print(html[:200])
        
        # Test if it's fallback content
        if "personality assessment data is being processed" in html:
            print("❌ Using fallback content - AI call failed")
        elif "dedicated team member ready to contribute" in html:
            print("❌ Using guaranteed fallback content - OpenAI not working")
        else:
            print("✅ Generated real AI content!")
            
    else:
        print("❌ No students found in database")
        
except Exception as e:
    print(f"❌ Error testing with student: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Test complete!")
