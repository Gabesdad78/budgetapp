from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session
from datetime import datetime
from collections import defaultdict
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Simple in-memory storage
users = {}
transactions = {}
budgets = {}

# Sample data for demo
if not users:
    users['demo'] = {
        'email': 'demo@example.com',
        'password': 'password',
        'income': 5000,
        'id': 1
    }

if not transactions:
    transactions['demo'] = [
        {'id': 1, 'description': 'Grocery Shopping', 'amount': 120.50, 'category': 'Food', 'date': '2025-08-01'},
        {'id': 2, 'description': 'Gas Station', 'amount': 45.00, 'category': 'Transportation', 'date': '2025-08-02'},
        {'id': 3, 'description': 'Netflix Subscription', 'amount': 15.99, 'category': 'Entertainment', 'date': '2025-08-03'}
    ]

if not budgets:
    budgets['demo'] = {
        'Food': 300,
        'Transportation': 200,
        'Entertainment': 100,
        'Utilities': 150,
        'Shopping': 200
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username', 'demo')
        email = data.get('email', 'demo@example.com')
        password = data.get('password', 'password')
        income = float(data.get('income', 5000))

        users[username] = {
            'email': email,
            'password': password,
            'income': income,
            'id': len(users) + 1
        }
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username', 'demo')
        password = data.get('password', 'password')
        
        if username in users and users[username]['password'] == password:
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Try demo/demo', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    user_transactions = transactions.get(user, [])
    user_budgets = budgets.get(user, {})
    
    total_spent = sum(t['amount'] for t in user_transactions)
    total_budget = sum(user_budgets.values())
    
    return render_template('dashboard.html', 
                         transactions=user_transactions,
                         budgets=user_budgets,
                         total_spent=total_spent,
                         total_budget=total_budget,
                         income=users[user]['income'])

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
            'date': data.get('date', datetime.now().strftime('%Y-%m-%d'))
        }
        
        if user not in transactions:
            transactions[user] = []
        transactions[user].append(new_transaction)
        
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
            'Shopping': float(data.get('shopping', 0))
        }
        
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
    
    return render_template('spending_analysis.html', 
                         category_spending=dict(category_spending),
                         transactions=user_transactions)

@app.route('/ml_recommendations')
def ml_recommendations():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    user_transactions = transactions.get(user, [])
    user_budgets = budgets.get(user, {})
    
    # Simple analytics
    total_spent = sum(t['amount'] for t in user_transactions)
    income = users[user]['income']
    
    recommendations = []
    
    if total_spent > income * 0.8:
        recommendations.append("⚠️ You're spending more than 80% of your income. Consider reducing expenses.")
    
    if user_transactions:
        avg_daily = total_spent / len(user_transactions)
        if avg_daily > 50:
            recommendations.append("💰 Your average daily spending is high. Try to reduce daily expenses.")
    
    # Category recommendations
    category_spending = defaultdict(float)
    for transaction in user_transactions:
        category_spending[transaction['category']] += transaction['amount']
    
    for category, budget in user_budgets.items():
        spent = category_spending.get(category, 0)
        if spent > budget * 0.9:
            recommendations.append(f"📊 {category} spending is approaching budget limit.")
    
    return render_template('ml_recommendations.html', 
                         recommendations=recommendations,
                         total_spent=total_spent,
                         income=income)

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
            "spending_analysis": "/spending_analysis"
        }
    })

if __name__ == '__main__':
    app.run(debug=True) 