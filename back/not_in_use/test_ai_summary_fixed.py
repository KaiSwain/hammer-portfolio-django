#!/usr/bin/env python
"""
Test script for the new AI summary functionality
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/home/kaifer/workspace/hammer/hammer-portfolio-django/back')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hammer_backendproject.settings')
django.setup()

def test_ai_connection():
    """Test the basic OpenAI connection"""
    print("Testing OpenAI connection...")
    
    try:
        from hammer_backendapi.views.ai_summary_fixed import test_openai_connection
        
        success, message = test_openai_connection()
        
        if success:
            print("✅ OpenAI connection test PASSED")
            print(f"Response: {message}")
        else:
            print("❌ OpenAI connection test FAILED")
            print(f"Error: {message}")
            
        return success
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

def test_ai_summary_generation():
    """Test AI summary generation with a sample student"""
    print("\nTesting AI summary generation...")
    
    try:
        from hammer_backendapi.models import Student
        from hammer_backendapi.views.ai_summary_fixed import generate_long_summary_html
        
        # Get the first student for testing
        student = Student.objects.first()
        
        if not student:
            print("❌ No students found in database")
            return False
            
        print(f"Testing with student: {student.full_name}")
        
        # Generate summary
        html_content = generate_long_summary_html(student)
        
        if html_content and len(html_content) > 100:
            print("✅ AI summary generation PASSED")
            print(f"Generated {len(html_content)} characters of HTML content")
            print("First 200 characters:")
            print(html_content[:200] + "...")
            return True
        else:
            print("❌ AI summary generation FAILED")
            print(f"Content: {html_content}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False

def main():
    print("🧪 Testing AI Summary Functionality")
    print("=" * 50)
    
    # Test 1: Basic connection
    connection_ok = test_ai_connection()
    
    # Test 2: Summary generation (only if connection works)
    if connection_ok:
        summary_ok = test_ai_summary_generation()
        
        if summary_ok:
            print("\n🎉 All tests PASSED! AI summary functionality is working.")
        else:
            print("\n⚠️ Connection works but summary generation failed.")
    else:
        print("\n⚠️ Connection test failed. Check OpenAI API key configuration.")
    
    print("\n📋 Next steps:")
    print("1. Ensure OPENAI_API_KEY is set in your environment")
    print("2. Test the endpoint: curl -X GET http://localhost:8000/api/ai/test/")
    print("3. Deploy with: railway up")

if __name__ == "__main__":
    main()