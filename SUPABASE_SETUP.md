# 🚀 Supabase Setup Guide for Budget App

## 📋 Prerequisites
- Supabase account (free at https://supabase.com)
- Your budget app GitHub repository

## 🎯 Step 1: Create Supabase Project

### 1.1 Go to Supabase
- Visit https://supabase.com
- Click "Start your project"
- Sign in with GitHub

### 1.2 Create New Project
- Click "New Project"
- Choose your organization
- Enter project details:
  - **Name**: `budget-app-backend`
  - **Database Password**: `budgetapp2024!` (or your choice)
  - **Region**: Choose closest to you
- Click "Create new project"

### 1.3 Get Your Credentials
Once created, go to Settings → API and copy:
- **Project URL** (looks like: `https://xyz.supabase.co`)
- **Anon Key** (starts with `eyJ...`)

## 🗄️ Step 2: Database Schema

### 2.1 Create Tables
Go to SQL Editor and run this SQL:

```sql
-- Enable Row Level Security
ALTER TABLE auth.users ENABLE ROW LEVEL SECURITY;

-- Create users table (extends Supabase auth)
CREATE TABLE public.users (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    income DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create transactions table
CREATE TABLE public.transactions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category TEXT NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create budgets table
CREATE TABLE public.budgets (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, category)
);

-- Create goals table
CREATE TABLE public.goals (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    target_amount DECIMAL(10,2) NOT NULL,
    current_amount DECIMAL(10,2) DEFAULT 0,
    deadline DATE,
    category TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_transactions_user_id ON public.transactions(user_id);
CREATE INDEX idx_transactions_date ON public.transactions(date);
CREATE INDEX idx_budgets_user_id ON public.budgets(user_id);
CREATE INDEX idx_goals_user_id ON public.goals(user_id);
```

### 2.2 Enable Row Level Security
```sql
-- Enable RLS on all tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.budgets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.goals ENABLE ROW LEVEL SECURITY;

-- Create policies
-- Users can only see their own data
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON public.users
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Transactions policies
CREATE POLICY "Users can view own transactions" ON public.transactions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own transactions" ON public.transactions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own transactions" ON public.transactions
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own transactions" ON public.transactions
    FOR DELETE USING (auth.uid() = user_id);

-- Budgets policies
CREATE POLICY "Users can view own budgets" ON public.budgets
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own budgets" ON public.budgets
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own budgets" ON public.budgets
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own budgets" ON public.budgets
    FOR DELETE USING (auth.uid() = user_id);

-- Goals policies
CREATE POLICY "Users can view own goals" ON public.goals
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own goals" ON public.goals
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own goals" ON public.goals
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own goals" ON public.goals
    FOR DELETE USING (auth.uid() = user_id);
```

## 🔧 Step 3: Update Flask App

### 3.1 Install Supabase Python Client
```bash
pip install supabase
```

### 3.2 Environment Variables
Create `.env` file:
```
SUPABASE_URL=your_project_url
SUPABASE_ANON_KEY=your_anon_key
```

## 🚀 Step 4: Deploy to Vercel

### 4.1 Add Environment Variables to Vercel
- Go to your Vercel project
- Settings → Environment Variables
- Add:
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY`

### 4.2 Deploy
- Push changes to GitHub
- Vercel will auto-deploy

## ✅ Step 5: Test

1. Register a new user
2. Add transactions
3. Set budgets
4. Create goals
5. Check real-time updates

## 🎉 Success!

Your budget app now has:
- ✅ Persistent data storage
- ✅ Real-time updates
- ✅ Secure authentication
- ✅ Scalable backend
- ✅ Professional architecture

## 📞 Need Help?

If you encounter any issues:
1. Check Supabase logs
2. Verify environment variables
3. Test locally first
4. Check Vercel deployment logs 