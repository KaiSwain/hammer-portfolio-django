#!/usr/bin/env python3
"""
Test script for Student Files API endpoints
"""

import requests
import json
import sys
import os

# API Configuration
BASE_URL = "http://localhost:8000/api"

def test_health_check():
    """Test if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health/")
        if response.status_code == 200:
            print("✅ API Health Check: PASSED")
            return True
        else:
            print(f"❌ API Health Check: FAILED (Status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API Health Check: FAILED (Connection Error)")
        return False

def get_auth_token():
    """Get authentication token (you'll need to create a user first)"""
    # This would require a test user - for now just return None
    # In a real test, you would login and get a token
    return None

def test_student_files_endpoints():
    """Test student file endpoints (without authentication for now)"""
    
    print("\n🧪 Testing Student Files API Endpoints")
    
    # Test list files for student (should require auth)
    try:
        response = requests.get(f"{BASE_URL}/students/1/files/")
        print(f"📂 List Student Files: Status {response.status_code}")
        
        if response.status_code == 401:
            print("   ✅ Authentication required (expected)")
        elif response.status_code == 200:
            print("   ✅ Endpoint accessible")
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    print("🔧 Testing Hammer Portfolio Student Files API")
    print("=" * 50)
    
    # Test basic health
    if not test_health_check():
        print("\n❌ API is not running. Please start the Django server first:")
        print("   cd back && source venv/bin/activate && python manage.py runserver")
        sys.exit(1)
    
    # Test student files endpoints
    test_student_files_endpoints()
    
    print("\n✅ Basic API endpoint tests completed!")
    print("\nNext steps:")
    print("1. Create a test user and get authentication token")
    print("2. Test file upload functionality")
    print("3. Test file download and deletion")

if __name__ == "__main__":
    main()