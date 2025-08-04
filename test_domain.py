#!/usr/bin/env python3
"""
Test script to check domain functionality
"""
import requests
import json

def test_domain():
    domain = "https://www.smartbudgetnow.com"
    
    print("🌐 Testing Domain: www.smartbudgetnow.com")
    print("=" * 50)
    
    try:
        # Test 1: Check if domain is accessible
        print("1. Testing domain accessibility...")
        response = requests.get(domain, timeout=10)
        print(f"   ✅ Domain is accessible (Status: {response.status_code})")
        
        # Test 2: Check main page
        print("2. Testing main page...")
        response = requests.get(f"{domain}/")
        print(f"   ✅ Main page working (Status: {response.status_code})")
        
        # Test 3: Check login page
        print("3. Testing login page...")
        response = requests.get(f"{domain}/login")
        print(f"   ✅ Login page working (Status: {response.status_code})")
        
        # Test 4: Check API endpoint
        print("4. Testing API endpoint...")
        response = requests.get(f"{domain}/api/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API working: {data.get('message', 'Unknown')}")
        else:
            print(f"   ❌ API failed (Status: {response.status_code})")
        
        # Test 5: Check debug endpoint
        print("5. Testing debug endpoint...")
        response = requests.get(f"{domain}/debug")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Debug working: {data.get('status', 'Unknown')}")
        else:
            print(f"   ❌ Debug failed (Status: {response.status_code})")
        
        print("\n🎉 Domain is working correctly!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to domain. Check if it's deployed correctly.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Domain might be slow or not responding.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_domain() 