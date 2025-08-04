from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session, send_file
from datetime import datetime, timedelta
from collections import defaultdict
import json
import os
import csv
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Data storage - in-memory for Vercel compatibility
users = {}
transactions = {}
budgets = {}
goals = {}

# Optional file storage (will fail gracefully on Vercel)
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
TRANSACTIONS_FILE = os.path.join(DATA_DIR, 'transactions.json')
BUDGETS_FILE = os.path.join(DATA_DIR, 'budgets.json')
GOALS_FILE = os.path.join(DATA_DIR, 'goals.json')

def load_data(filename, default=None):
    """Load data from JSON file - gracefully handles missing files"""
    if default is None:
        default = {}
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return default
    except:
        return default

def save_data(data, filename):
    """Save data to JSON file - gracefully handles write failures"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        # On Vercel, file writes will fail, but that's okay
        return False

# Try to load existing data, but don't fail if it doesn't exist
try:
    users = load_data(USERS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)
    budgets = load_data(BUDGETS_FILE)
    goals = load_data(GOALS_FILE)
except:
    # If loading fails, start with empty data
    pass

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
        
        if username in users:
            flash('Username already exists!', 'error')
            return render_template('register.html')

        users[username] = {
            'email': email,
            'password': password,
            'income': income,
            'id': len(users) + 1,
            'created_at': datetime.now().isoformat()
        }
        
        # Initialize user data
        transactions[username] = []
        budgets[username] = {}
        goals[username] = []
        
        # Try to save data (will fail gracefully on Vercel)
        save_data(users, USERS_FILE)
        save_data(transactions, TRANSACTIONS_FILE)
        save_data(budgets, BUDGETS_FILE)
        save_data(goals, GOALS_FILE)
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        
        if username in users and users[username]['password'] == password:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    user_transactions = transactions.get(user, [])
    user_budgets = budgets.get(user, {})
    user_goals = goals.get(user, [])
    
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
                         income=users[user]['income'],
                         category_spending=dict(category_spending),
                         budget_progress=budget_progress)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.form
        user = session['user']
        
        new_transaction = {
            'id': len(transactions.get(user, [])) + 1,
            'description': data.get('description'),
            'amount': float(data.get('amount')),
            'category': data.get('category'),
            'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
            'created_at': datetime.now().isoformat()
        }
        
        if user not in transactions:
            transactions[user] = []
        transactions[user].append(new_transaction)
        
        # Try to save data
        save_data(transactions, TRANSACTIONS_FILE)
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_transaction.html')

@app.route('/set_budget', methods=['GET', 'POST'])
def set_budget():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.form
        user = session['user']
        
        budgets[user] = {
            'Food': float(data.get('food', 0)),
            'Transportation': float(data.get('transportation', 0)),
            'Entertainment': float(data.get('entertainment', 0)),
            'Utilities': float(data.get('utilities', 0)),
            'Shopping': float(data.get('shopping', 0)),
            'Healthcare': float(data.get('healthcare', 0)),
            'Education': float(data.get('education', 0)),
            'Other': float(data.get('other', 0))
        }
        
        # Try to save data
        save_data(budgets, BUDGETS_FILE)
        flash('Budget updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('set_budget.html')

@app.route('/spending_analysis')
def spending_analysis():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    user_transactions = transactions.get(user, [])
    
    # Calculate spending by category
    category_spending = defaultdict(float)
    for transaction in user_transactions:
        category_spending[transaction['category']] += transaction['amount']
    
    # Monthly trends
    monthly_spending = defaultdict(float)
    for transaction in user_transactions:
        month = transaction['date'][:7]  # YYYY-MM
        monthly_spending[month] += transaction['amount']
    
    # Top spending categories
    top_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return render_template('spending_analysis.html', 
                         category_spending=dict(category_spending),
                         monthly_spending=dict(monthly_spending),
                         top_categories=top_categories,
                         transactions=user_transactions)

@app.route('/ml_recommendations')
def ml_recommendations():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    user_transactions = transactions.get(user, [])
    user_budgets = budgets.get(user, {})
    
    # Advanced analytics
    total_spent = sum(t['amount'] for t in user_transactions)
    income = users[user]['income']
    
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

@app.route('/goals')
def goals_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    user_goals = goals.get(user, [])
    
    return render_template('goals.html', goals=user_goals)

@app.route('/add_goal', methods=['POST'])
def add_goal():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    data = request.form
    
    new_goal = {
        'id': len(goals.get(user, [])) + 1,
        'title': data.get('title'),
        'target_amount': float(data.get('target_amount')),
        'current_amount': 0,
        'deadline': data.get('deadline'),
        'category': data.get('category'),
        'created_at': datetime.now().isoformat()
    }
    
    if user not in goals:
        goals[user] = []
    goals[user].append(new_goal)
    
    # Try to save data
    save_data(goals, GOALS_FILE)
    flash('Goal added successfully!', 'success')
    return redirect(url_for('goals_page'))

@app.route('/update_goal_progress', methods=['POST'])
def update_goal_progress():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    data = request.form
    goal_id = int(data.get('goal_id'))
    amount = float(data.get('amount'))
    
    for goal in goals.get(user, []):
        if goal['id'] == goal_id:
            goal['current_amount'] += amount
            break
    
    # Try to save data
    save_data(goals, GOALS_FILE)
    flash('Goal progress updated!', 'success')
    return redirect(url_for('goals_page'))

@app.route('/export_data')
def export_data():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    user_transactions = transactions.get(user, [])
    
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
        download_name=f'budget_data_{user}_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@app.route('/logout')
def logout():
    session.pop('user', None)
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
    return jsonify({
        "status": "healthy",
        "message": "Budget App is running successfully",
        "timestamp": datetime.now().isoformat(),
        "users_count": len(users),
        "transactions_count": sum(len(t) for t in transactions.values()),
        "budgets_count": len(budgets),
        "goals_count": sum(len(g) for g in goals.values())
    })

if __name__ == '__main__':
    app.run(debug=True) 