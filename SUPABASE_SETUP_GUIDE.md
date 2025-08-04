# 🚀 Supabase Setup Guide for Budget App

## 📋 Step-by-Step Instructions

### **Step 1: Access Your Supabase Project**

1. **Go to Supabase Dashboard**
   - Visit: https://supabase.com
   - Sign in with your GitHub account
   - Click on your project: `budget-app-backend`

### **Step 2: Get Your API Credentials**

1. **Navigate to API Settings**
   - In your Supabase dashboard, go to **Settings** → **API**
   - You'll see two important pieces of information:

2. **Copy Your Credentials**
   - **Project URL**: `https://apsgqpqeksqviariaetm.supabase.co`
   - **anon public key**: Copy the key that starts with `eyJ...`

### **Step 3: Set Up Database Schema**

1. **Open SQL Editor**
   - In your Supabase dashboard, click **SQL Editor** in the left sidebar

2. **Run Database Setup**
   - Copy the entire content from `database_setup.sql`
   - Paste it into the SQL Editor
   - Click **Run** to execute the SQL

3. **Verify Tables Created**
   - Go to **Table Editor** in the left sidebar
   - You should see these tables:
     - `users`
     - `transactions`
     - `budgets`
     - `goals`

### **Step 4: Test Your Connection**

1. **Run the verification script**
   ```bash
   python verify_supabase.py
   ```

2. **Enter your credentials when prompted**
   - Project URL: `https://apsgqpqeksqviariaetm.supabase.co`
   - Anon Key: Your copied key

### **Step 5: Update Environment Variables**

1. **Create `.env` file** (if it doesn't exist)
   ```
   SUPABASE_URL=https://apsgqpqeksqviariaetm.supabase.co
   SUPABASE_ANON_KEY=your-actual-anon-key-here
   ```

2. **Add to Vercel** (for deployment)
   - Go to your Vercel project settings
   - Add environment variables:
     - `SUPABASE_URL`
     - `SUPABASE_ANON_KEY`

### **Step 6: Test the App**

1. **Run the Flask app locally**
   ```bash
   python api/app.py
   ```

2. **Test registration and login**
   - Visit: http://localhost:5000
   - Try registering a new user
   - Try logging in

## 🔍 Troubleshooting

### **If connection fails:**
- ✅ Check that you copied the correct anon key (not service role key)
- ✅ Verify the project URL is correct
- ✅ Make sure you ran the database setup SQL
- ✅ Check that all tables were created successfully

### **If registration fails:**
- ✅ Verify the `users` table was created
- ✅ Check that Row Level Security policies are in place
- ✅ Ensure the database schema matches exactly

### **If login fails:**
- ✅ Check that user profiles are being created
- ✅ Verify authentication is working
- ✅ Check browser console for errors

## 🎯 Next Steps

Once everything is working:

1. **Deploy to Vercel**
   - Push changes to GitHub
   - Vercel will auto-deploy
   - Add environment variables in Vercel dashboard

2. **Test the deployed app**
   - Visit your Vercel URL
   - Test all features: registration, login, transactions, budgets, goals

3. **Monitor the app**
   - Check Supabase logs for any issues
   - Monitor Vercel deployment logs

## 📞 Need Help?

If you encounter any issues:
1. Check the error messages carefully
2. Verify your credentials are correct
3. Make sure the database schema was created properly
4. Test the connection with the verification script

**Your app will have:**
- ✅ Persistent data storage
- ✅ Real-time updates
- ✅ Secure authentication
- ✅ Professional backend
- ✅ Scalable architecture 