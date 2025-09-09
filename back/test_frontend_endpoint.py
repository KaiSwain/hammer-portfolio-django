#!/usr/bin/env python
"""
Test the exact endpoint and process the frontend uses for AI summary
"""
import requests
import json
import os

# Frontend configuration
FRONTEND_API_URL = "https://hammer-app-hk3st.ondigitalocean.app"

def test_frontend_flow():
    print("=" * 60)
    print("Testing Frontend AI Summary Flow")
    print("=" * 60)
    print(f"Frontend API URL: {FRONTEND_API_URL}")
    
    # Step 1: Health check
    print("\n1. Health Check...")
    try:
        health_response = requests.get(f'{FRONTEND_API_URL}/api/health/', timeout=10)
        print(f"   Status: {health_response.status_code}")
        print(f"   Response: {health_response.text}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return
    
    # Step 2: Login to get a token (you'll need to provide real credentials)
    print("\n2. Login to get token...")
    
    # You would typically need to login here, but for testing let's see what happens
    # when we call the personality-summary endpoint without proper auth
    
    # Step 3: Test the personality-summary endpoint
    print("\n3. Testing personality-summary endpoint...")
    
    # Try with a fake student ID to see what error we get
    test_student_id = 1
    
    try:
        # This is exactly what the frontend does
        response = requests.post(
            f'{FRONTEND_API_URL}/api/students/{test_student_id}/personality-summary/',
            headers={
                'Authorization': 'Token fake_token_for_testing',
                'Content-Type': 'application/json',
            }
        )
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Response: {response.text[:500]}...")
        
        if response.status_code == 401:
            print("   ✅ Expected 401 - auth required")
        elif response.status_code == 500:
            print("   ⚠️  Server error - this might be our OpenAI issue")
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
    
    # Step 4: Check what environment variables the production server sees
    print("\n4. Trying to diagnose environment variables...")
    
    # We can't directly check env vars, but we can look for clues in error messages
    print("   Note: To fully debug, we need to check DigitalOcean app logs")
    print("   The issue is likely that production environment variables aren't being read correctly")

if __name__ == "__main__":
    test_frontend_flow()
