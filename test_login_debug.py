#!/usr/bin/env python3
"""
Test script to debug login issues
"""
import requests
import json

def test_login_debug():
    domain = "https://www.smartbudgetnow.com"
    
    print("🔍 Debugging Login Issue")
    print("=" * 40)
    
    try:
        # Test 1: Check if we can register a new account
        print("1. Testing account registration...")
        register_data = {
            'username': 'testuser123',
            'email': 'test123@example.com',
            'password': 'testpass123',
            'income': '5000'
        }
        
        response = requests.post(f"{domain}/register", data=register_data, timeout=10)
        print(f"   📊 Register response: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Registration successful (redirect)")
        elif response.status_code == 200:
            print("   ⚠️ Registration returned 200 (might be showing form again)")
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
        
        # Test 2: Try to login with the account
        print("2. Testing login with new account...")
        login_data = {
            'email': 'test123@example.com',
            'password': 'testpass123'
        }
        
        response = requests.post(f"{domain}/login", data=login_data, timeout=10)
        print(f"   📊 Login response: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Login successful (redirect)")
            # Follow the redirect to see if dashboard loads
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
        else:
            print(f"   ❌ Login failed: {response.status_code}")
        
        # Test 3: Check debug info
        print("3. Checking debug info...")
        response = requests.get(f"{domain}/debug", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Users count: {data.get('users_count', 0)}")
            print(f"   📊 Environment: {data.get('environment', 'unknown')}")
            print(f"   📊 Vercel: {data.get('vercel', 'unknown')}")
        
        print("\n📋 Summary:")
        print("If registration works but login fails with 500 error,")
        print("the issue is likely in the session handling or dashboard template.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_login_debug() 