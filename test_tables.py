"""
Test if database tables are accessible
"""
from supabase import create_client

# Your Supabase credentials
SUPABASE_URL = "https://apsgqpqeksqviariaetm.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFwc2dxcHFla3NxdmlhcmlhZXRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQyNzAzMDEsImV4cCI6MjA2OTg0NjMwMX0.kOgm3q7hwtmoiNpQKnW9ihLJ7s5kLQ5TwUdQ_lt5fNA"

def test_tables():
    """Test if all tables are accessible"""
    try:
        print("🔧 Testing Database Tables")
        print("=" * 40)
        
        # Create client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        
        # Test each table
        tables = ['users', 'transactions', 'budgets', 'goals']
        
        for table in tables:
            try:
                result = supabase.table(table).select('count').execute()
                print(f"✅ {table} table is accessible")
            except Exception as e:
                print(f"❌ {table} table error: {e}")
        
        print("\n🎉 Database setup test complete!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    test_tables() 