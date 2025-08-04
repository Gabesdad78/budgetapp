"""
Test script to verify Supabase connection
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Your Supabase credentials
SUPABASE_URL = "https://apsgqpqeksqviariaetm.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFwc2dxcHFlazNxdmlhcmlhZXRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQyNzAzMDEsImV4cCI6MjA2OTg0NjMwMX0.kOgm3q7hwtmoiNpQKnW9ihLJ7s5kLQ5TwUdQ_lt5fNA"

def test_supabase_connection():
    """Test Supabase connection"""
    try:
        from supabase import create_client
        
        # Create client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        
        # Test connection by trying to access a table
        result = supabase.table('users').select('count').execute()
        
        print("✅ Supabase connection successful!")
        print(f"URL: {SUPABASE_URL}")
        print(f"Key: {SUPABASE_ANON_KEY[:20]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Supabase connection...")
    test_supabase_connection() 