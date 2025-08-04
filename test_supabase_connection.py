"""
Test Supabase connection with correct credentials
"""
from supabase import create_client

# Your Supabase credentials
SUPABASE_URL = "https://apsgqpqeksqviariaetm.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFwc2dxcHFla3NxdmlhcmlhZXRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQyNzAzMDEsImV4cCI6MjA2OTg0NjMwMX0.kOgm3q7hwtmoiNpQKnW9ihLJ7s5kLQ5TwUdQ_lt5fNA"

def test_supabase_connection():
    """Test Supabase connection with correct credentials"""
    try:
        print("🔧 Testing Supabase Connection")
        print("=" * 40)
        print(f"URL: {SUPABASE_URL}")
        print(f"Key: {SUPABASE_ANON_KEY[:20]}...")

        # Create client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

        # Test connection by trying to access a table
        result = supabase.table('users').select('count').execute()

        print("✅ Supabase connection successful!")
        print("🎉 Your credentials are working correctly!")
        
        return True

    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        print("\n💡 This might mean:")
        print("1. The database schema hasn't been set up yet")
        print("2. The 'users' table doesn't exist")
        print("3. Row Level Security policies need to be configured")
        
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Set up the database schema using database_setup.sql")
        print("2. Test the Flask app with Supabase integration")
        print("3. Deploy to Vercel with environment variables")
    else:
        print("\n🔧 Let's set up the database schema first!")
        print("1. Go to your Supabase dashboard")
        print("2. Open SQL Editor")
        print("3. Run the database_setup.sql script") 