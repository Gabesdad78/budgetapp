"""
Complete Supabase Setup for Budget App
"""
import os
import webbrowser
from datetime import datetime

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🚀 COMPLETE SUPABASE SETUP FOR BUDGET APP")
    print("=" * 60)

def setup_database_schema():
    """Guide user through database schema setup"""
    print("\n📋 STEP 1: SET UP DATABASE SCHEMA")
    print("-" * 40)
    
    print("1. Go to your Supabase dashboard:")
    print("   https://supabase.com")
    print("   (Sign in with GitHub)")
    
    print("\n2. Click on your project: budget-app-backend")
    
    print("\n3. Open SQL Editor:")
    print("   - Click 'SQL Editor' in the left sidebar")
    
    print("\n4. Copy and paste this SQL script:")
    print("   (I'll show you the script below)")
    
    # Read and display the database setup SQL
    try:
        with open('database_setup.sql', 'r') as f:
            sql_content = f.read()
        
        print("\n" + "=" * 60)
        print("📄 DATABASE SETUP SQL SCRIPT")
        print("=" * 60)
        print(sql_content)
        print("=" * 60)
        
        # Save to a file for easy copying
        with open('database_setup_ready.sql', 'w') as f:
            f.write(sql_content)
        
        print("\n✅ SQL script saved to 'database_setup_ready.sql'")
        print("   You can copy from this file to paste in Supabase")
        
    except FileNotFoundError:
        print("❌ database_setup.sql not found")
        return False
    
    print("\n5. Click 'Run' to execute the SQL")
    print("\n6. Verify tables were created:")
    print("   - Go to 'Table Editor' in the left sidebar")
    print("   - You should see: users, transactions, budgets, goals")
    
    return True

def setup_environment_variables():
    """Set up environment variables"""
    print("\n📋 STEP 2: ENVIRONMENT VARIABLES")
    print("-" * 40)
    
    # Your Supabase credentials
    SUPABASE_URL = "https://apsgqpqeksqviariaetm.supabase.co"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFwc2dxcHFla3NxdmlhcmlhZXRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQyNzAzMDEsImV4cCI6MjA2OTg0NjMwMX0.kOgm3q7hwtmoiNpQKnW9ihLJ7s5kLQ5TwUdQ_lt5fNA"
    
    # Create .env file
    env_content = f"""# Supabase Configuration
SUPABASE_URL={SUPABASE_URL}
SUPABASE_ANON_KEY={SUPABASE_ANON_KEY}

# Flask Configuration
SECRET_KEY=your-secret-key-here-{datetime.now().strftime('%Y%m%d%H%M%S')}
FLASK_ENV=production
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with your Supabase credentials")
    
    print("\n📋 For Vercel deployment, add these environment variables:")
    print(f"SUPABASE_URL = {SUPABASE_URL}")
    print(f"SUPABASE_ANON_KEY = {SUPABASE_ANON_KEY}")
    
    return True

def test_integration():
    """Test the complete integration"""
    print("\n📋 STEP 3: TEST INTEGRATION")
    print("-" * 40)
    
    try:
        from supabase_config import get_supabase_manager
        
        # Get Supabase manager
        supabase = get_supabase_manager()
        
        if supabase is None:
            print("❌ Failed to initialize Supabase manager")
            return False
        
        print("✅ Supabase manager initialized successfully")
        
        # Test table access
        try:
            result = supabase.client.table('users').select('count').execute()
            print("✅ Database tables are accessible!")
            print("🎉 Your Supabase integration is working perfectly!")
            return True
        except Exception as e:
            print(f"⚠️  Database tables not ready yet: {e}")
            print("💡 Please complete Step 1 (database schema setup) first")
            return False
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def deploy_to_vercel():
    """Guide user through Vercel deployment"""
    print("\n📋 STEP 4: DEPLOY TO VERCEL")
    print("-" * 40)
    
    print("1. Go to your Vercel dashboard:")
    print("   https://vercel.com/dashboard")
    
    print("\n2. Find your budget app project")
    
    print("\n3. Go to Settings → Environment Variables")
    
    print("\n4. Add these environment variables:")
    print("   SUPABASE_URL = https://apsgqpqeksqviariaetm.supabase.co")
    print("   SUPABASE_ANON_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFwc2dxcHFla3NxdmlhcmlhZXRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQyNzAzMDEsImV4cCI6MjA2OTg0NjMwMX0.kOgm3q7hwtmoiNpQKnW9ihLJ7s5kLQ5TwUdQ_lt5fNA")
    
    print("\n5. Save the environment variables")
    
    print("\n6. Redeploy your app:")
    print("   - Go to Deployments tab")
    print("   - Click 'Redeploy' on the latest deployment")
    
    return True

def main():
    """Main setup function"""
    print_banner()
    
    print("\n🎯 This script will help you complete the Supabase setup!")
    print("   Follow each step carefully.")
    
    # Step 1: Database Schema
    if not setup_database_schema():
        print("\n❌ Failed to set up database schema")
        return
    
    print("\n⏳ After you've completed Step 1 in your Supabase dashboard,")
    print("   press Enter to continue with the next steps...")
    input()
    
    # Step 2: Environment Variables
    if not setup_environment_variables():
        print("\n❌ Failed to set up environment variables")
        return
    
    # Step 3: Test Integration
    if not test_integration():
        print("\n❌ Integration test failed")
        print("   Please complete the database schema setup first")
        return
    
    # Step 4: Deploy to Vercel
    deploy_to_vercel()
    
    print("\n🎉 SETUP COMPLETE!")
    print("=" * 60)
    print("✅ Your Budget App now has:")
    print("   - Persistent Supabase database")
    print("   - Real-time data synchronization")
    print("   - Secure user authentication")
    print("   - Professional cloud backend")
    print("   - Advanced analytics and goals tracking")
    
    print("\n🌐 Your app is ready to use!")
    print("   Local: http://localhost:5000")
    print("   Vercel: Check your Vercel dashboard for the URL")

if __name__ == "__main__":
    main() 