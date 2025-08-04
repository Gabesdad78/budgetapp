"""
Set up environment variables and test Supabase integration
"""
import os
from dotenv import load_dotenv

# Your Supabase credentials
SUPABASE_URL = "https://apsgqpqeksqviariaetm.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFwc2dxcHFla3NxdmlhcmlhZXRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQyNzAzMDEsImV4cCI6MjA2OTg0NjMwMX0.kOgm3q7hwtmoiNpQKnW9ihLJ7s5kLQ5TwUdQ_lt5fNA"

def create_env_file():
    """Create .env file with Supabase credentials"""
    env_content = f"""# Supabase Configuration
SUPABASE_URL={SUPABASE_URL}
SUPABASE_ANON_KEY={SUPABASE_ANON_KEY}

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with your Supabase credentials")

def test_supabase_integration():
    """Test the complete Supabase integration"""
    try:
        from supabase_config import get_supabase_manager
        
        # Get Supabase manager
        supabase = get_supabase_manager()
        
        if supabase is None:
            print("❌ Failed to initialize Supabase manager")
            return False
        
        print("✅ Supabase manager initialized successfully")
        
        # Test basic operations
        print("🔧 Testing basic operations...")
        
        # Test table access (this will work after schema is set up)
        try:
            result = supabase.client.table('users').select('count').execute()
            print("✅ Database tables are accessible")
        except Exception as e:
            print(f"⚠️  Database tables not ready yet: {e}")
            print("💡 Run the database_setup.sql script in your Supabase dashboard")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase integration test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Supabase Integration")
    print("=" * 40)
    
    # Create .env file
    create_env_file()
    
    # Test integration
    print("\n🔧 Testing Supabase integration...")
    success = test_supabase_integration()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run database_setup.sql in your Supabase dashboard")
        print("2. Test the Flask app: python api/app.py")
        print("3. Deploy to Vercel with environment variables")
    else:
        print("\n❌ Setup failed. Please check your credentials.")

if __name__ == "__main__":
    main() 