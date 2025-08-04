"""
Quick Supabase connection test
"""
from supabase import create_client

# Your Supabase URL (this should be correct)
SUPABASE_URL = "https://apsgqpqeksqviariaetm.supabase.co"

def test_connection():
    """Test Supabase connection"""
    print("🔧 Testing Supabase Connection")
    print("=" * 40)
    print(f"URL: {SUPABASE_URL}")
    
    # You need to get the correct anon key from your Supabase dashboard
    print("\n❌ You need to get the correct anon key from your Supabase dashboard:")
    print("1. Go to https://supabase.com")
    print("2. Sign in and open your project")
    print("3. Go to Settings → API")
    print("4. Copy the 'anon public' key (starts with eyJ...)")
    print("5. Replace the key in this script and run again")
    
    # Example of what the key should look like
    print("\n📝 Your anon key should look like this:")
    print("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6...")
    
    return False

if __name__ == "__main__":
    test_connection() 