from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session, send_file
from datetime import datetime, timedelta
import json
import os
import csv
import io
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Simple in-memory storage for development
users = {}
transactions = []
budgets = {}
goals = []

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
        
        # Create user
        user_id = str(uuid.uuid4())
        users[username] = {
            'id': user_id,
            'email': email,
            'username': username,
            'income': income
        }
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        
        # Simple authentication
        for user in users.values():
            if user['email'] == email:
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        
        flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user_transactions = [t for t in transactions if t.get('user_id') == user_id]
    user_budgets = budgets.get(user_id, {})
    user_goals = [g for g in goals if g.get('user_id') == user_id]
    
    # Calculate basic stats
    total_spent = sum(t['amount'] for t in user_transactions)
    total_budget = sum(user_budgets.values())
    
    return render_template('dashboard.html', 
                         transactions=user_transactions[-5:],
                         budgets=user_budgets,
                         goals=user_goals,
                         total_spent=total_spent,
                         total_budget=total_budget)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.form
        description = data.get('description')
        amount = float(data.get('amount', 0))
        category = data.get('category')
        date = data.get('date')
        
        if not description or not amount or not category or not date:
            flash('All fields are required!', 'error')
            return render_template('add_transaction.html')
        
        transaction = {
            'id': str(uuid.uuid4()),
            'user_id': session['user_id'],
            'description': description,
            'amount': amount,
            'category': category,
            'date': date
        }
        transactions.append(transaction)
        
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_transaction.html')

@app.route('/set_budget', methods=['GET', 'POST'])
def set_budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.form
        user_id = session['user_id']
        
        budget_data = {}
        for key, value in data.items():
            if key.startswith('budget_') and value:
                category = key.replace('budget_', '')
                budget_data[category] = float(value)
        
        budgets[user_id] = budget_data
        flash('Budget set successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('set_budget.html')

@app.route('/spending_analysis')
def spending_analysis():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user_transactions = [t for t in transactions if t.get('user_id') == user_id]
    
    # Calculate spending by category
    category_spending = {}
    for transaction in user_transactions:
        category = transaction['category']
        amount = transaction['amount']
        category_spending[category] = category_spending.get(category, 0) + amount
    
    return render_template('spending_analysis.html', 
                         category_spending=category_spending,
                         transactions=user_transactions)

@app.route('/ml_recommendations')
def ml_recommendations():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user_transactions = [t for t in transactions if t.get('user_id') == user_id]
    user_budgets = budgets.get(user_id, {})
    
    # Simple recommendations
    recommendations = []
    total_spent = sum(t['amount'] for t in user_transactions)
    
    if total_spent > 0:
        # Top spending category
        category_spending = {}
        for transaction in user_transactions:
            category = transaction['category']
            amount = transaction['amount']
            category_spending[category] = category_spending.get(category, 0) + amount
        
        if category_spending:
            top_category = max(category_spending, key=category_spending.get)
            top_amount = category_spending[top_category]
            percentage = (top_amount / total_spent) * 100
            
            recommendations.append({
                'type': 'spending_insight',
                'message': f'Your top spending category is {top_category} ({percentage:.1f}% of total)',
                'suggestion': f'Consider reducing {top_category} expenses to save more'
            })
    
    return render_template('ml_recommendations.html', recommendations=recommendations)

@app.route('/goals')
def goals_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user_goals = [g for g in goals if g.get('user_id') == user_id]
    
    return render_template('goals.html', goals=user_goals)

@app.route('/add_goal', methods=['POST'])
def add_goal():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = request.form
    title = data.get('title')
    target_amount = float(data.get('target_amount', 0))
    deadline = data.get('deadline')
    category = data.get('category')
    
    if not title or not target_amount or not deadline:
        flash('Title, target amount, and deadline are required!', 'error')
        return redirect(url_for('goals_page'))
    
    goal = {
        'id': str(uuid.uuid4()),
        'user_id': session['user_id'],
        'title': title,
        'target_amount': target_amount,
        'current_amount': 0,
        'deadline': deadline,
        'category': category
    }
    goals.append(goal)
    
    flash('Goal added successfully!', 'success')
    return redirect(url_for('goals_page'))

@app.route('/update_goal_progress', methods=['POST'])
def update_goal_progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    data = request.form
    goal_id = data.get('goal_id')
    current_amount = float(data.get('current_amount', 0))
    
    for goal in goals:
        if goal['id'] == goal_id:
            goal['current_amount'] = current_amount
            break
    
    flash('Goal progress updated!', 'success')
    return redirect(url_for('goals_page'))

@app.route('/export_data')
def export_data():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user_transactions = [t for t in transactions if t.get('user_id') == user_id]
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Description', 'Amount', 'Category'])
    
    for transaction in user_transactions:
        writer.writerow([
            transaction['date'],
            transaction['description'],
            transaction['amount'],
            transaction['category']
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'transactions_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/api/')
def api_index():
    return jsonify({
        "status": "success",
        "message": "Budget App is running!",
        "endpoints": {
            "dashboard": "/dashboard",
            "add_transaction": "/add_transaction",
            "set_budget": "/set_budget",
            "spending_analysis": "/spending_analysis",
            "ml_recommendations": "/ml_recommendations",
            "goals": "/goals",
            "export_data": "/export_data"
        }
    })

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "Budget App is running successfully!"
    })

if __name__ == '__main__':
    app.run(debug=True) 