#!/usr/bin/env python

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hammer_backendproject.settings')
django.setup()

from hammer_backendapi.models import Student
from django.contrib.auth.models import User

def create_test_data():
    """Create test student data for API testing"""
    
    print("🎯 Creating test student data...")
    
    # Create admin user if not exists
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Admin user created (username: admin, password: admin123)")
    else:
        print("ℹ️  Admin user already exists")
    
    # Get or create a default teacher
    from hammer_backendapi.models import Teacher, Organization
    
    # Create organization if not exists
    org, _ = Organization.objects.get_or_create(
        name="Test Organization",
        defaults={'address': '123 Test St, Test City, TC 12345'}
    )
    
    # Create teacher if not exists
    teacher, _ = Teacher.objects.get_or_create(
        email='teacher@example.com',
        defaults={
            'full_name': 'Test Teacher',
            'password': 'temp_password',
            'organization': org
        }
    )
    
    # Create test students with the actual model fields
    test_students = [
        {
            'full_name': 'John Doe',
            'teacher': teacher,
            'complete_50_hour_training': True,
            'hammer_math': True,
            'employability_skills': True,
        },
        {
            'full_name': 'Jane Smith',
            'teacher': teacher,
            'passed_osha_10_exam': True,
            'employability_skills': True,
        },
        {
            'full_name': 'Mike Johnson',
            'teacher': teacher,
            'hammer_math': True,
            'passed_ruler_assessment': True,
        }
    ]
    
    students_created = 0
    for student_data in test_students:
        # Check if student already exists by full_name
        if not Student.objects.filter(full_name=student_data['full_name']).exists():
            student = Student.objects.create(**student_data)
            print(f"✅ Created student: {student.full_name}")
            students_created += 1
        else:
            print(f"ℹ️  Student already exists: {student_data['full_name']}")
    
    total_students = Student.objects.count()
    print(f"\n📊 Total students in database: {total_students}")
    print(f"🆕 New students created: {students_created}")
    
    # List all students
    print("\n👥 All students:")
    for student in Student.objects.all():
        print(f"   • {student.id}: {student.full_name} (Teacher: {student.teacher.full_name})")
    
    return total_students

if __name__ == "__main__":
    try:
        count = create_test_data()
        print(f"\n🎉 Test data setup complete! {count} students available for API testing.")
        print("\n🧪 Test your API now:")
        print("   curl http://localhost:8000/api/students/")
        print("   or visit: http://localhost:8000/admin/")
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        import traceback
        traceback.print_exc()
