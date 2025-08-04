#!/usr/bin/env python3
"""
Test to check main page functionality
"""
import requests
import json

def test_main_page():
    domain = "https://www.smartbudgetnow.com"
    
    print("🔍 Testing Main Page")
    print("=" * 25)
    
    try:
        # Test 1: Check main page
        print("1. Testing main page...")
        response = requests.get(f"{domain}/", timeout=10)
        print(f"   📊 Main page response: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Main page loads (Length: {len(response.text)} chars)")
            
            # Check for error messages in the content
            if "An error occurred loading the dashboard" in response.text:
                print("   ❌ Found dashboard error message on main page")
            elif "error" in response.text.lower():
                print("   ⚠️ Found error-related text on main page")
            else:
                print("   ✅ No error messages found on main page")
                
            # Check for flash messages
            if "alert" in response.text.lower():
                print("   ⚠️ Found alert/flash messages on main page")
            else:
                print("   ✅ No flash messages found")
        else:
            print(f"   ❌ Main page failed: {response.status_code}")
        
        # Test 2: Check if there are any redirects
        print("2. Testing for redirects...")
        response = requests.get(f"{domain}/", timeout=10, allow_redirects=False)
        print(f"   📊 Response without redirects: {response.status_code}")
        
        if response.status_code == 302:
            print("   ⚠️ Main page is redirecting somewhere")
            if 'Location' in response.headers:
                print(f"   📍 Redirecting to: {response.headers['Location']}")
        else:
            print("   ✅ No redirects on main page")
        
        # Test 3: Check session state
        print("3. Testing session state...")
        response = requests.get(f"{domain}/test-session", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   📊 Session data: {data.get('session_data', {})}")
            print(f"   📊 Users count: {data.get('users_count', 0)}")
        
        print("\n📋 Summary:")
        print("If you see 'An error occurred loading the dashboard' on the main page,")
        print("it might be a leftover flash message from a previous session.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_main_page() 