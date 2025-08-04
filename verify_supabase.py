"""
Verify Supabase credentials and test connection
"""
from supabase import create_client

def test_supabase_credentials(url, key):
    """Test Supabase connection with provided credentials"""
    try:
        # Create client
        supabase = create_client(url, key)
        
        # Test connection by trying to access a table
        result = supabase.table('users').select('count').execute()
        
        print("✅ Supabase connection successful!")
        print(f"URL: {url}")
        print(f"Key: {key[:20]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Supabase Credential Verification")
    print("=" * 40)
    
    # Get credentials from user
    print("Please enter your Supabase credentials:")
    url = input("Project URL (e.g., https://xyz.supabase.co): ").strip()
    key = input("Anon Key (starts with eyJ...): ").strip()
    
    if not url or not key:
        print("❌ Please provide both URL and key")
        exit(1)
    
    print("\nTesting connection...")
    success = test_supabase_credentials(url, key)
    
    if success:
        print("\n🎉 Success! Your credentials are working.")
        print("Next step: Run the database setup SQL in your Supabase dashboard.")
    else:
        print("\n❌ Connection failed. Please check your credentials.")
        print("Make sure to:")
        print("1. Copy the correct Project URL from Settings → API")
        print("2. Copy the correct anon public key from Settings → API")
        print("3. Run the database setup SQL in SQL Editor") 