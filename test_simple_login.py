#!/usr/bin/env python3
"""
Simple test to check if login fix worked
"""
import requests
import json

def test_simple_login():
    domain = "https://www.smartbudgetnow.com"
    
    print("🔍 Testing Simple Login Fix")
    print("=" * 35)
    
    try:
        # Test 1: Check if we can access the simple dashboard test
        print("1. Testing simple dashboard route...")
        response = requests.get(f"{domain}/dashboard-simple", timeout=10)
        print(f"   📊 Simple dashboard response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Simple dashboard works: {data.get('message', 'Unknown')}")
        else:
            print(f"   ❌ Simple dashboard failed: {response.status_code}")
        
        # Test 2: Check if we can access the test session route
        print("2. Testing session route...")
        response = requests.get(f"{domain}/test-session", timeout=10)
        print(f"   📊 Session test response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Session test works: {data.get('status', 'Unknown')}")
        else:
            print(f"   ❌ Session test failed: {response.status_code}")
        
        # Test 3: Try a simple login
        print("3. Testing simple login...")
        login_data = {
            'email': 'test123@example.com',
            'password': 'testpass123'
        }
        
        response = requests.post(f"{domain}/login", data=login_data, timeout=10)
        print(f"   📊 Login response: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Login successful (redirect)")
        elif response.status_code == 200:
            print("   ⚠️ Login returned 200 (might be showing form)")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
        
        print("\n📋 Summary:")
        print("If the simple dashboard and session tests work,")
        print("the issue was with the template rendering.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_simple_login() 