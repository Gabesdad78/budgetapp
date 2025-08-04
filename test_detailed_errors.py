#!/usr/bin/env python3
"""
Detailed test to check specific functionality that might be causing 500 errors
"""
import requests
import json

def test_detailed_functionality():
    domain = "https://www.smartbudgetnow.com"
    
    print("🔍 Detailed Error Testing")
    print("=" * 50)
    
    try:
        # Test 1: Check if we can access the main page content
        print("1. Testing main page content...")
        response = requests.get(f"{domain}/")
        if response.status_code == 200:
            print(f"   ✅ Main page loads (Length: {len(response.text)} chars)")
            if "Smart Budget App" in response.text:
                print("   ✅ Main page contains expected content")
            else:
                print("   ⚠️ Main page content seems different")
        else:
            print(f"   ❌ Main page failed (Status: {response.status_code})")
        
        # Test 2: Check login page content
        print("2. Testing login page content...")
        response = requests.get(f"{domain}/login")
        if response.status_code == 200:
            print(f"   ✅ Login page loads (Length: {len(response.text)} chars)")
            if "login" in response.text.lower():
                print("   ✅ Login page contains expected content")
            else:
                print("   ⚠️ Login page content seems different")
        else:
            print(f"   ❌ Login page failed (Status: {response.status_code})")
        
        # Test 3: Check register page content
        print("3. Testing register page content...")
        response = requests.get(f"{domain}/register")
        if response.status_code == 200:
            print(f"   ✅ Register page loads (Length: {len(response.text)} chars)")
            if "register" in response.text.lower():
                print("   ✅ Register page contains expected content")
            else:
                print("   ⚠️ Register page content seems different")
        else:
            print(f"   ❌ Register page failed (Status: {response.status_code})")
        
        # Test 4: Check if POST requests work (this might be where the 500 error occurs)
        print("4. Testing POST request to login (this might fail)...")
        try:
            response = requests.post(f"{domain}/login", data={
                'email': 'test@example.com',
                'password': 'testpassword'
            }, timeout=10)
            print(f"   📊 Login POST response: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Login POST works")
            elif response.status_code == 302:
                print("   ✅ Login POST redirects (expected)")
            else:
                print(f"   ⚠️ Login POST returned: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Login POST failed: {e}")
        
        # Test 5: Check if we can access the dashboard (should redirect to login)
        print("5. Testing dashboard access...")
        response = requests.get(f"{domain}/dashboard", allow_redirects=False)
        if response.status_code == 302:
            print("   ✅ Dashboard redirects to login (expected)")
        elif response.status_code == 200:
            print("   ⚠️ Dashboard loads without login (unexpected)")
        else:
            print(f"   ❌ Dashboard failed (Status: {response.status_code})")
        
        # Test 6: Check debug endpoint for more details
        print("6. Testing debug endpoint for details...")
        response = requests.get(f"{domain}/debug")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Debug info: {data}")
        else:
            print(f"   ❌ Debug failed (Status: {response.status_code})")
        
        print("\n📋 Summary:")
        print("If you're getting 500 errors when trying to login or register,")
        print("the issue is likely with the form submission or data processing.")
        print("The app is running, but there might be an issue with:")
        print("- File permissions on Vercel")
        print("- Database operations")
        print("- Session handling")
        print("- Template rendering")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_detailed_functionality() 