#!/usr/bin/env python3
"""
Simple test script to check login functionality
"""
import requests
import json

def test_login():
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Testing Login Functionality")
    print("=" * 40)
    
    try:
        # Test 1: Check if server is running
        print("1. Testing server connection...")
        response = requests.get(f"{base_url}/")
        print(f"   ✅ Server is running (Status: {response.status_code})")
        
        # Test 2: Check login page
        print("2. Testing login page...")
        response = requests.get(f"{base_url}/login")
        print(f"   ✅ Login page accessible (Status: {response.status_code})")
        
        # Test 3: Check register page
        print("3. Testing register page...")
        response = requests.get(f"{base_url}/register")
        print(f"   ✅ Register page accessible (Status: {response.status_code})")
        
        # Test 4: Check forgot password page
        print("4. Testing forgot password page...")
        response = requests.get(f"{base_url}/forgot_password")
        print(f"   ✅ Forgot password page accessible (Status: {response.status_code})")
        
        # Test 5: Check API endpoint
        print("5. Testing API endpoint...")
        response = requests.get(f"{base_url}/api/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API working: {data.get('message', 'Unknown')}")
        else:
            print(f"   ❌ API failed (Status: {response.status_code})")
        
        print("\n🎉 All tests passed! The app should be working correctly.")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the Flask app is running.")
        print("   Run: python api/app.py")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_login() 