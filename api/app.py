from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Simple in-memory storage for demo
users = {}
transactions = {}
budgets = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        income = float(request.form['income'])
        
        if username in users:
            flash('Username already exists')
            return redirect(url_for('register'))
            
        users[username] = {
            'email': email,
            'password': password,  # In real app, hash this
            'income': income,
            'id': len(users) + 1
        }
        
        flash('Registration successful!')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            # In real app, use proper session management
            return redirect(url_for('dashboard', username=username))
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    username = request.args.get('username', 'demo')
    user = users.get(username, {'income': 5000, 'id': 1})
    
    user_transactions = [t for t in transactions.values() if t.get('user_id') == user['id']]
    user_budgets = [b for b in budgets.values() if b.get('user_id') == user['id']]
    
    category_spending = {}
    total_spent = 0
    
    for transaction in user_transactions:
        if transaction.get('transaction_type') == 'expense':
            category = transaction.get('category', 'Other')
            if category not in category_spending:
                category_spending[category] = 0
            category_spending[category] += transaction.get('amount', 0)
            total_spent += transaction.get('amount', 0)
    
    return render_template('dashboard.html', 
                         transactions=user_transactions[:10],
                         category_spending=category_spending,
                         total_spent=total_spent,
                         budgets=user_budgets,
                         income=user['income'])

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    username = request.args.get('username', 'demo')
    user = users.get(username, {'id': 1})
    
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form['description']
    transaction_type = request.form['transaction_type']
    
    transaction_id = len(transactions) + 1
    transactions[transaction_id] = {
        'user_id': user['id'],
        'amount': amount,
        'category': category,
        'description': description,
        'transaction_type': transaction_type,
        'date': datetime.now().isoformat()
    }
    
    flash('Transaction added successfully!')
    return redirect(url_for('dashboard', username=username))

@app.route('/set_budget', methods=['POST'])
def set_budget():
    username = request.args.get('username', 'demo')
    user = users.get(username, {'id': 1})
    
    category = request.form['category']
    amount = float(request.form['amount'])
    current_month = datetime.now().strftime('%Y-%m')
    
    budget_id = len(budgets) + 1
    budgets[budget_id] = {
        'user_id': user['id'],
        'category': category,
        'amount': amount,
        'month': current_month
    }
    
    flash('Budget set successfully!')
    return redirect(url_for('dashboard', username=username))

@app.route('/ml_recommendations')
def ml_recommendations():
    username = request.args.get('username', 'demo')
    user = users.get(username, {'id': 1})
    
    user_transactions = [t for t in transactions.values() if t.get('user_id') == user['id']]
    
    if len(user_transactions) < 3:
        return jsonify({'error': 'Not enough transaction data for recommendations'})
    
    # Simple recommendations based on averages
    categories = list(set(t.get('category', 'Other') for t in user_transactions if t.get('transaction_type') == 'expense'))
    
    recommendations = {}
    for category in categories:
        category_transactions = [t for t in user_transactions 
                               if t.get('category') == category and t.get('transaction_type') == 'expense']
        
        if category_transactions:
            total = sum(t.get('amount', 0) for t in category_transactions)
            avg = total / len(category_transactions)
            recommendations[category] = {
                'predicted_spending': round(avg, 2),
                'recommended_budget': round(avg * 1.1, 2)
            }
    
    return jsonify(recommendations)

@app.route('/spending_analysis')
def spending_analysis():
    username = request.args.get('username', 'demo')
    user = users.get(username, {'id': 1})
    
    user_transactions = [t for t in transactions.values() if t.get('user_id') == user['id']]
    
    if len(user_transactions) == 0:
        return jsonify({'error': 'No transaction data available'})
    
    expenses = [t for t in user_transactions if t.get('transaction_type') == 'expense']
    
    if not expenses:
        return jsonify({'error': 'No expense data available'})
    
    total_spent = sum(t.get('amount', 0) for t in expenses)
    avg_transaction = total_spent / len(expenses)
    
    # Calculate top categories
    category_totals = {}
    for transaction in expenses:
        category = transaction.get('category', 'Other')
        if category not in category_totals:
            category_totals[category] = 0
        category_totals[category] += transaction.get('amount', 0)
    
    top_categories = dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5])
    
    analysis = {
        'total_spent': float(total_spent),
        'avg_transaction': float(avg_transaction),
        'top_categories': top_categories,
        'monthly_trend': {'2024-01': total_spent}  # Simplified
    }
    
    return jsonify(analysis)

@app.route('/test')
def test():
    return jsonify({"message": "App is working!", "status": "success"})

if __name__ == '__main__':
    app.run(debug=True) 