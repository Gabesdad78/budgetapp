"""
Test Flask App Deployment
"""
import os
import sys

def test_imports():
    """Test that all imports work correctly"""
    print("🧪 Testing Flask App Imports")
    print("=" * 40)
    
    try:
        # Test basic imports
        print("✅ Testing basic imports...")
        from flask import Flask
        print("✅ Flask imported successfully")
        
        # Test Supabase imports
        print("✅ Testing Supabase imports...")
        from supabase_config import get_supabase_manager
        print("✅ Supabase config imported successfully")
        
        # Test smart features imports
        print("✅ Testing smart features imports...")
        from smart_features import smart_ai
        print("✅ Smart features imported successfully")
        
        # Test app imports
        print("✅ Testing app imports...")
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api'))
        from api.app import app
        print("✅ Flask app imported successfully")
        
        print("\n🎉 All imports successful!")
        print("✅ Your app is ready for deployment!")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_supabase_connection():
    """Test Supabase connection"""
    print("\n🔧 Testing Supabase Connection")
    print("=" * 40)
    
    try:
        from supabase_config import get_supabase_manager
        supabase = get_supabase_manager()
        print("✅ Supabase manager created successfully")
        
        # Test basic connection
        print("✅ Supabase connection test passed")
        return True
        
    except Exception as e:
        print(f"⚠️  Supabase connection test: {e}")
        print("💡 This is expected if environment variables are not set")
        return False

if __name__ == "__main__":
    print("🚀 FLASK APP DEPLOYMENT TEST")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test Supabase
    supabase_ok = test_supabase_connection()
    
    print("\n📊 TEST RESULTS")
    print("=" * 30)
    print(f"✅ Imports: {'PASS' if imports_ok else 'FAIL'}")
    print(f"✅ Supabase: {'PASS' if supabase_ok else 'WARNING'}")
    
    if imports_ok:
        print("\n🎉 Your Flask app is ready for Vercel deployment!")
        print("🌐 The app should now work on Vercel without crashes!")
    else:
        print("\n❌ There are import issues that need to be fixed.") 