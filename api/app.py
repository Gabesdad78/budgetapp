from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session, send_file
from datetime import datetime, timedelta
from collections import defaultdict
import json
import os
import csv
import io
import uuid
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Supabase configuration
from supabase_config import get_supabase_manager

# Import smart routes - use absolute import
import smart_routes
smart_bp = smart_routes.smart_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Register smart blueprint
app.register_blueprint(smart_bp, url_prefix='/smart')

# Initialize Supabase manager
supabase = get_supabase_manager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        income = float(data.get('income', 0))
        
        if not username or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('register.html')
        
        try:
            # Check if user already exists
            existing_user = supabase.get_user_profile_by_username(username)
            if existing_user:
                flash('Username already exists!', 'error')
                return render_template('register.html')
            
            # Create user in Supabase auth
            auth_response = supabase.client.auth.sign_up({
                'email': email,
                'password': password
            })
            
            if auth_response.user:
                user_id = auth_response.user.id
                
                # Create user profile
                user_profile = supabase.create_user_profile(
                    user_id=user_id,
                    email=email,
                    username=username,
                    income=income
                )
                
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Registration failed. Please try again.', 'error')
                return render_template('register.html')
                
        except Exception as e:
            print(f"Registration error: {e}")
            flash('Registration failed. Please try again.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        
        try:
            # Authenticate with Supabase
            auth_response = supabase.client.auth.sign_in_with_password({
                'email': email,
                'password': password
            })
            
            if auth_response.user:
                # Get user profile
                user_profile = supabase.get_user_profile(auth_response.user.id)
                if user_profile:
                    session['user_id'] = auth_response.user.id
                    session['username'] = user_profile['username']
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('User profile not found!', 'error')
            else:
                flash('Invalid email or password!', 'error')
                
        except Exception as e:
            print(f"Login error: {e}")
            flash('Login failed. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        # Get user data from Supabase
        user_profile = supabase.get_user_profile(user_id)
        if not user_profile:
            flash('User profile not found. Please register again.', 'error')
            session.clear()
            return redirect(url_for('login'))
        
        user_transactions = supabase.get_user_transactions(user_id)
        user_budgets = supabase.get_user_budgets(user_id)
        user_goals = supabase.get_user_goals(user_id)
        
        # Calculate analytics
        total_spent = sum(t['amount'] for t in user_transactions)
        total_budget = sum(user_budgets.values())
        
        # Calculate spending trends
        recent_transactions = user_transactions[-7:] if len(user_transactions) >= 7 else user_transactions
        weekly_spending = sum(t['amount'] for t in recent_transactions)
        
        # Category breakdown
        category_spending = defaultdict(float)
        for transaction in user_transactions:
            category_spending[transaction['category']] += transaction['amount']
        
        # Budget progress
        budget_progress = {}
        for category, budget_amount in user_budgets.items():
            spent = category_spending.get(category, 0)
            progress = (spent / budget_amount * 100) if budget_amount > 0 else 0
            budget_progress[category] = {
                'spent': spent,
                'budget': budget_amount,
                'progress': min(progress, 100),
                'remaining': max(budget_amount - spent, 0)
            }
        
        return render_template('dashboard.html', 
                             transactions=user_transactions,
                             budgets=user_budgets,
                             goals=user_goals,
                             total_spent=total_spent,
                             total_budget=total_budget,
                             weekly_spending=weekly_spending,
                             income=user_profile.get('income', 0),
                             category_spending=dict(category_spending),
                             budget_progress=budget_progress)
    
    except Exception as e:
        print(f"Dashboard error: {e}")
        flash('There was an error loading your dashboard. Please try again.', 'error')
        return render_template('dashboard.html', 
                             transactions=[],
                             budgets={},
                             goals=[],
                             total_spent=0,
                             total_budget=0,
                             weekly_spending=0,
                             income=0,
                             category_spending={},
                             budget_progress={})

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.form
        user_id = session['user_id']
        
        try:
            new_transaction = supabase.add_transaction(
                user_id=user_id,
                description=data.get('description'),
                amount=float(data.get('amount')),
                category=data.get('category'),
                transaction_date=data.get('date', datetime.now().strftime('%Y-%m-%d'))
            )
            
            if new_transaction:
                flash('Transaction added successfully!', 'success')
            else:
                flash('Failed to add transaction. Please try again.', 'error')
                
        except Exception as e:
            print(f"Add transaction error: {e}")
            flash('Failed to add transaction. Please try again.', 'error')
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_transaction.html')

@app.route('/set_budget', methods=['GET', 'POST'])
def set_budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.form
        user_id = session['user_id']
        
        try:
            budgets = {
                'Food': float(data.get('food', 0)),
                'Transportation': float(data.get('transportation', 0)),
                'Entertainment': float(data.get('entertainment', 0)),
                'Utilities': float(data.get('utilities', 0)),
                'Shopping': float(data.get('shopping', 0)),
                'Healthcare': float(data.get('healthcare', 0)),
                'Education': float(data.get('education', 0)),
                'Other': float(data.get('other', 0))
            }
            
            success = supabase.set_user_budgets(user_id, budgets)
            if success:
                flash('Budget updated successfully!', 'success')
            else:
                flash('Failed to update budget. Please try again.', 'error')
                
        except Exception as e:
            print(f"Set budget error: {e}")
            flash('Failed to update budget. Please try again.', 'error')
        
        return redirect(url_for('dashboard'))
    
    return render_template('set_budget.html')

@app.route('/spending_analysis')
def spending_analysis():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        analytics = supabase.get_spending_analytics(user_id)
        user_transactions = supabase.get_user_transactions(user_id)
        
        return render_template('spending_analysis.html', 
                             category_spending=analytics['category_spending'],
                             monthly_spending=analytics['monthly_spending'],
                             top_categories=sorted(analytics['category_spending'].items(), key=lambda x: x[1], reverse=True)[:5],
                             transactions=user_transactions)
    
    except Exception as e:
        print(f"Spending analysis error: {e}")
        flash('There was an error loading spending analysis. Please try again.', 'error')
        return render_template('spending_analysis.html', 
                             category_spending={},
                             monthly_spending={},
                             top_categories=[],
                             transactions=[])

@app.route('/ml_recommendations')
def ml_recommendations():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        user_profile = supabase.get_user_profile(user_id)
        user_transactions = supabase.get_user_transactions(user_id)
        user_budgets = supabase.get_user_budgets(user_id)
        
        # Advanced analytics
        total_spent = sum(t['amount'] for t in user_transactions)
        income = user_profile.get('income', 0)
        
        recommendations = []
        
        # Spending ratio analysis
        spending_ratio = (total_spent / income * 100) if income > 0 else 0
        if spending_ratio > 80:
            recommendations.append("⚠️ You're spending more than 80% of your income. Consider reducing expenses.")
        elif spending_ratio > 60:
            recommendations.append("💰 You're spending 60-80% of your income. Monitor your spending closely.")
        
        # Category analysis
        category_spending = defaultdict(float)
        for transaction in user_transactions:
            category_spending[transaction['category']] += transaction['amount']
        
        for category, budget in user_budgets.items():
            spent = category_spending.get(category, 0)
            if spent > budget * 0.9:
                recommendations.append(f"📊 {category} spending is approaching budget limit.")
            elif spent > budget * 0.7:
                recommendations.append(f"⚠️ {category} spending is at 70% of budget.")
        
        # Spending pattern analysis
        if user_transactions:
            avg_daily = total_spent / len(user_transactions)
            if avg_daily > 50:
                recommendations.append("💰 Your average daily spending is high. Try to reduce daily expenses.")
            
            # Identify highest spending category
            if category_spending:
                highest_category = max(category_spending.items(), key=lambda x: x[1])
                recommendations.append(f"🎯 Your highest spending category is {highest_category[0]} (${highest_category[1]:.2f}). Consider setting a specific budget for this category.")
        
        # Savings recommendations
        if income > 0:
            savings_rate = ((income - total_spent) / income * 100)
            if savings_rate < 10:
                recommendations.append("💡 Consider increasing your savings rate. Aim for at least 10-20% of your income.")
            elif savings_rate > 30:
                recommendations.append("🎉 Excellent savings rate! You're on track for financial success.")
        
        return render_template('ml_recommendations.html', 
                             recommendations=recommendations,
                             total_spent=total_spent,
                             income=income,
                             spending_ratio=spending_ratio)
    
    except Exception as e:
        print(f"ML recommendations error: {e}")
        flash('There was an error loading recommendations. Please try again.', 'error')
        return render_template('ml_recommendations.html', 
                             recommendations=["💡 Start by adding some transactions to get personalized recommendations!"],
                             total_spent=0,
                             income=0,
                             spending_ratio=0)

@app.route('/goals')
def goals_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        user_goals = supabase.get_user_goals(user_id)
        return render_template('goals.html', goals=user_goals)
    except Exception as e:
        print(f"Goals error: {e}")
        flash('There was an error loading goals. Please try again.', 'error')
        return render_template('goals.html', goals=[])

@app.route('/add_goal', methods=['POST'])
def add_goal():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    data = request.form
    
    try:
        new_goal = supabase.add_goal(
            user_id=user_id,
            title=data.get('title'),
            target_amount=float(data.get('target_amount')),
            deadline=data.get('deadline'),
            category=data.get('category')
        )
        
        if new_goal:
            flash('Goal added successfully!', 'success')
        else:
            flash('Failed to add goal. Please try again.', 'error')
            
    except Exception as e:
        print(f"Add goal error: {e}")
        flash('Failed to add goal. Please try again.', 'error')
    
    return redirect(url_for('goals_page'))

@app.route('/update_goal_progress', methods=['POST'])
def update_goal_progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = request.form
    goal_id = data.get('goal_id')
    amount = float(data.get('amount'))
    
    try:
        success = supabase.update_goal_progress(goal_id, amount)
        if success:
            flash('Goal progress updated!', 'success')
        else:
            flash('Failed to update goal progress. Please try again.', 'error')
            
    except Exception as e:
        print(f"Update goal progress error: {e}")
        flash('Failed to update goal progress. Please try again.', 'error')
    
    return redirect(url_for('goals_page'))

@app.route('/export_data')
def export_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        user_transactions = supabase.get_user_transactions(user_id)
        
        # Create CSV data
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Date', 'Description', 'Category', 'Amount'])
        
        for transaction in user_transactions:
            writer.writerow([
                transaction['date'],
                transaction['description'],
                transaction['category'],
                transaction['amount']
            ])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'budget_data_{session["username"]}_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    except Exception as e:
        print(f"Export data error: {e}")
        flash('Failed to export data. Please try again.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# API endpoints for JSON responses
@app.route('/api/')
def api_index():
    return jsonify({
        "message": "Budget App API is running!",
        "status": "success",
        "endpoints": {
            "register": "/register",
            "login": "/login",
            "dashboard": "/dashboard",
            "add_transaction": "/add_transaction",
            "set_budget": "/set_budget",
            "ml_recommendations": "/ml_recommendations",
            "spending_analysis": "/spending_analysis",
            "goals": "/goals",
            "export_data": "/export_data"
        }
    })

@app.route('/health')
def health_check():
    try:
        # Test Supabase connection
        if supabase:
            return jsonify({
                "status": "healthy",
                "message": "Budget App is running successfully with Supabase",
                "timestamp": datetime.now().isoformat(),
                "supabase_connected": True
            })
        else:
            return jsonify({
                "status": "degraded",
                "message": "Budget App is running but Supabase connection failed",
                "timestamp": datetime.now().isoformat(),
                "supabase_connected": False
            })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "message": f"Budget App error: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "supabase_connected": False
        })

if __name__ == '__main__':
    app.run(debug=True) 