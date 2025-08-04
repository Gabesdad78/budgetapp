#!/usr/bin/env python3
"""
Comprehensive test to debug the login issue
"""
import requests
import json

def test_comprehensive_login():
    domain = "https://www.smartbudgetnow.com"
    
    print("🔍 Comprehensive Login Debug")
    print("=" * 40)
    
    try:
        # Test 1: Check current users
        print("1. Checking current users...")
        response = requests.get(f"{domain}/test-session", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Users count: {data.get('users_count', 0)}")
            print(f"   📊 User IDs: {data.get('user_ids', [])}")
        
        # Test 2: Try to register a new account
        print("2. Registering new test account...")
        register_data = {
            'username': 'testuser456',
            'email': 'test456@example.com',
            'password': 'testpass456',
            'income': '6000'
        }
        
        response = requests.post(f"{domain}/register", data=register_data, timeout=10)
        print(f"   📊 Register response: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Registration successful (redirect)")
        elif response.status_code == 200:
            print("   ⚠️ Registration returned 200 (might be showing form again)")
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
        
        # Test 3: Try to login with the new account
        print("3. Testing login with new account...")
        login_data = {
            'email': 'test456@example.com',
            'password': 'testpass456'
        }
        
        response = requests.post(f"{domain}/login", data=login_data, timeout=10, allow_redirects=False)
        print(f"   📊 Login response: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Login successful (redirect)")
            if 'Location' in response.headers:
                dashboard_url = response.headers['Location']
                print(f"   📍 Redirecting to: {dashboard_url}")
                
                # Test dashboard access
                dashboard_response = requests.get(f"{domain}{dashboard_url}", timeout=10)
                print(f"   📊 Dashboard response: {dashboard_response.status_code}")
                
                if dashboard_response.status_code == 200:
                    print("   ✅ Dashboard loads successfully")
                else:
                    print(f"   ❌ Dashboard failed: {dashboard_response.status_code}")
        elif response.status_code == 200:
            print("   ⚠️ Login returned 200 (might be showing form again)")
            # Check if there's an error message in the response
            if "Invalid email or password" in response.text:
                print("   ❌ Login failed - invalid credentials")
            elif "error" in response.text.lower():
                print("   ❌ Login failed - error in response")
            else:
                print("   ⚠️ Login form shown again")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
        
        # Test 4: Check debug info
        print("4. Checking debug info...")
        response = requests.get(f"{domain}/debug", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Users count: {data.get('users_count', 0)}")
            print(f"   📊 Environment: {data.get('environment', 'unknown')}")
            print(f"   📊 Vercel: {data.get('vercel', 'unknown')}")
        
        print("\n📋 Summary:")
        print("If login returns 200 instead of 302, the issue is:")
        print("- Invalid credentials")
        print("- Session handling problem")
        print("- Template rendering error")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_comprehensive_login() 