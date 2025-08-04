from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session, send_file
from datetime import datetime, timedelta
import json
import os
import csv
import io
import uuid
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Data storage files
USERS_FILE = 'users.json'
TRANSACTIONS_FILE = 'transactions.json'
BUDGETS_FILE = 'budgets.json'
GOALS_FILE = 'goals.json'

# Load data from files
def load_data():
    global users, transactions, budgets, goals
    users = {}
    transactions = []
    budgets = {}
    goals = []
    
    # Load users
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                users = json.load(f)
        except:
            users = {}
    
    # Load transactions
    if os.path.exists(TRANSACTIONS_FILE):
        try:
            with open(TRANSACTIONS_FILE, 'r') as f:
                transactions = json.load(f)
        except:
            transactions = []
    
    # Load budgets
    if os.path.exists(BUDGETS_FILE):
        try:
            with open(BUDGETS_FILE, 'r') as f:
                budgets = json.load(f)
        except:
            budgets = {}
    
    # Load goals
    if os.path.exists(GOALS_FILE):
        try:
            with open(GOALS_FILE, 'r') as f:
                goals = json.load(f)
        except:
            goals = []

# Save data to files
def save_data():
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        with open(TRANSACTIONS_FILE, 'w') as f:
            json.dump(transactions, f, indent=2)
        with open(BUDGETS_FILE, 'w') as f:
            json.dump(budgets, f, indent=2)
        with open(GOALS_FILE, 'w') as f:
            json.dump(goals, f, indent=2)
    except Exception as e:
        print(f"Error saving data: {e}")

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize data
load_data()

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
        
        # Create user with hashed password
        user_id = str(uuid.uuid4())
        users[username] = {
            'id': user_id,
            'email': email,
            'username': username,
            'password': hash_password(password),
            'income': income
        }
        save_data()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        
        # Check credentials
        for user in users.values():
            if user['email'] == email and user['password'] == hash_password(password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        
        flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Find user by email
        user_found = None
        for username, user in users.items():
            if user['email'] == email:
                user_found = user
                break
        
        if user_found:
            # Generate a simple reset token (in production, use proper tokens)
            reset_token = str(uuid.uuid4())
            user_found['reset_token'] = reset_token
            user_found['reset_expires'] = (datetime.now() + timedelta(hours=1)).isoformat()
            save_data()
            
            flash(f'Password reset link sent to {email}. Check your email.', 'success')
            return redirect(url_for('reset_password', token=reset_token))
        else:
            flash('Email not found. Please check your email address.', 'error')
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Find user with this token
    user_found = None
    for username, user in users.items():
        if user.get('reset_token') == token:
            # Check if token is expired
            if 'reset_expires' in user:
                expires = datetime.fromisoformat(user['reset_expires'])
                if datetime.now() < expires:
                    user_found = user
                else:
                    flash('Reset link has expired. Please request a new one.', 'error')
                    return redirect(url_for('forgot_password'))
            break
    
    if not user_found:
        flash('Invalid or expired reset link.', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not new_password or not confirm_password:
            flash('Both password fields are required!', 'error')
            return render_template('reset_password.html', token=token)
        
        if new_password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('reset_password.html', token=token)
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
            return render_template('reset_password.html', token=token)
        
        # Update password
        user_found['password'] = hash_password(new_password)
        user_found.pop('reset_token', None)
        user_found.pop('reset_expires', None)
        save_data()
        
        flash('Password reset successful! You can now login with your new password.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', token=token)

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
        save_data()
        
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
        save_data()
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
    save_data()
    
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
    
    save_data()
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