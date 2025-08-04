from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session, send_file
from datetime import datetime, timedelta
import json
import os
import csv
import io
import uuid
import hashlib
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Data storage files - use absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(current_dir, 'users.json')
TRANSACTIONS_FILE = os.path.join(current_dir, 'transactions.json')
BUDGETS_FILE = os.path.join(current_dir, 'budgets.json')
GOALS_FILE = os.path.join(current_dir, 'goals.json')

# Global data storage
users = {}
transactions = []
budgets = {}
goals = []

# Load data from files
def load_data():
    global users, transactions, budgets, goals
    
    # Initialize with empty data
    users = {}
    transactions = []
    budgets = {}
    goals = []
    
    # Load users
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
            users = {}
    
    # Load transactions
    if os.path.exists(TRANSACTIONS_FILE):
        try:
            with open(TRANSACTIONS_FILE, 'r', encoding='utf-8') as f:
                transactions = json.load(f)
        except Exception as e:
            print(f"Error loading transactions: {e}")
            transactions = []
    
    # Load budgets
    if os.path.exists(BUDGETS_FILE):
        try:
            with open(BUDGETS_FILE, 'r', encoding='utf-8') as f:
                budgets = json.load(f)
        except Exception as e:
            print(f"Error loading budgets: {e}")
            budgets = {}
    
    # Load goals
    if os.path.exists(GOALS_FILE):
        try:
            with open(GOALS_FILE, 'r', encoding='utf-8') as f:
                goals = json.load(f)
        except Exception as e:
            print(f"Error loading goals: {e}")
            goals = []

# Save data to files
def save_data():
    try:
        # For Vercel deployment, we'll use in-memory storage only
        # Vercel has a read-only filesystem, so we can't write files
        if os.environ.get('VERCEL'):
            print("Running on Vercel - using in-memory storage only")
            return
            
        # Only try to save files if not on Vercel
        os.makedirs(current_dir, exist_ok=True)
        
        # Save users
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        
        # Save transactions
        with open(TRANSACTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(transactions, f, indent=2, ensure_ascii=False)
        
        # Save budgets
        with open(BUDGETS_FILE, 'w', encoding='utf-8') as f:
            json.dump(budgets, f, indent=2, ensure_ascii=False)
        
        # Save goals
        with open(GOALS_FILE, 'w', encoding='utf-8') as f:
            json.dump(goals, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Error saving data: {e}")
        # Continue with in-memory storage

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Initialize data
load_data()

# Error handler
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error",
        "message": "Something went wrong. Please try again.",
        "details": str(error)
    }), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "error": "Page Not Found",
        "message": "The page you're looking for doesn't exist."
    }), 404

@app.route('/debug')
def debug_info():
    """Debug endpoint to check app status"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "users_count": len(users),
        "transactions_count": len(transactions),
        "budgets_count": len(budgets),
        "goals_count": len(goals),
        "current_dir": current_dir,
        "files_exist": {
            "users": os.path.exists(USERS_FILE),
            "transactions": os.path.exists(TRANSACTIONS_FILE),
            "budgets": os.path.exists(BUDGETS_FILE),
            "goals": os.path.exists(GOALS_FILE)
        },
        "vercel": os.environ.get('VERCEL', False),
        "environment": os.environ.get('FLASK_ENV', 'development')
    })

@app.route('/test')
def test_route():
    """Simple test route to check if app is working"""
    return jsonify({
        "message": "App is working!",
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    })

@app.route('/test-error')
def test_error():
    """Test route to simulate an error"""
    try:
        # This will cause an error
        result = 1 / 0
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({
            "error": "Test error",
            "message": str(e),
            "type": type(e).__name__
        }), 500

@app.route('/test-session')
def test_session():
    """Test route to check session functionality"""
    try:
        return jsonify({
            "session_data": dict(session),
            "users_count": len(users),
            "user_ids": [user.get('id') for user in users.values()],
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Index error: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Template rendering failed", "details": str(e)}), 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
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
    except Exception as e:
        print(f"Registration error: {e}")
        print(traceback.format_exc())
        flash('An error occurred during registration. Please try again.', 'error')
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            data = request.form
            email = data.get('email')
            password = data.get('password')
            
            print(f"Login attempt for email: {email}")
            print(f"Users available: {list(users.keys())}")
            
            # Simple credential check
            user_found = None
            for username, user in users.items():
                print(f"Checking user: {username}")
                if user.get('email') == email:
                    print(f"Email match found for: {username}")
                    if user.get('password') == hash_password(password):
                        print(f"Password match for: {username}")
                        user_found = user
                        break
                    else:
                        print(f"Password mismatch for: {username}")
            
            if user_found:
                print(f"Login successful for: {user_found.get('username')}")
                # Set minimal session data
                session['user_id'] = user_found.get('id')
                session['username'] = user_found.get('username')
                print(f"Session data set: {dict(session)}")
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                print("No matching user found")
                flash('Invalid email or password!', 'error')
        
        return render_template('login.html')
    except Exception as e:
        print(f"Login error: {e}")
        print(traceback.format_exc())
        flash('An error occurred during login. Please try again.', 'error')
        return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    try:
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
    except Exception as e:
        print(f"Forgot password error: {e}")
        print(traceback.format_exc())
        flash('An error occurred. Please try again.', 'error')
        return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
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
    except Exception as e:
        print(f"Reset password error: {e}")
        print(traceback.format_exc())
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('forgot_password'))

@app.route('/dashboard')
def dashboard():
    try:
        print(f"Dashboard access - session: {dict(session)}")
        
        if 'user_id' not in session:
            print("No user_id in session, redirecting to login")
            return redirect(url_for('login'))
        
        user_id = session['user_id']
        print(f"User ID from session: {user_id}")
        
        # Find user data
        user_data = None
        for username, user in users.items():
            if user.get('id') == user_id:
                user_data = user
                break
        
        if not user_data:
            print(f"User not found for ID: {user_id}")
            session.clear()
            flash('User session expired. Please login again.', 'error')
            return redirect(url_for('login'))
        
        print(f"User data found: {user_data.get('username')}")
        
        user_transactions = [t for t in transactions if t.get('user_id') == user_id]
        user_budgets = budgets.get(user_id, {})
        user_goals = [g for g in goals if g.get('user_id') == user_id]
        
        # Calculate basic stats
        total_spent = sum(t.get('amount', 0) for t in user_transactions)
        total_budget = sum(user_budgets.values())
        
        # Calculate weekly spending (last 7 days)
        from datetime import datetime, timedelta
        week_ago = datetime.now() - timedelta(days=7)
        weekly_transactions = [t for t in user_transactions if datetime.fromisoformat(t.get('date', '2023-01-01')) >= week_ago]
        weekly_spending = sum(t.get('amount', 0) for t in weekly_transactions)
        
        # Get user income
        income = user_data.get('income', 0)
        
        print(f"Dashboard data - transactions: {len(user_transactions)}, budgets: {len(user_budgets)}, goals: {len(user_goals)}")
        print(f"Stats - income: {income}, total_spent: {total_spent}, weekly_spending: {weekly_spending}")
        
        return render_template('dashboard.html', 
                             transactions=user_transactions[-5:],
                             budgets=user_budgets,
                             goals=user_goals,
                             total_spent=total_spent,
                             total_budget=total_budget,
                             income=income,
                             weekly_spending=weekly_spending)
    except Exception as e:
        print(f"Dashboard error: {e}")
        print(traceback.format_exc())
        flash('An error occurred loading the dashboard. Please try again.', 'error')
        return render_template('dashboard.html', 
                             transactions=[],
                             budgets={},
                             goals=[],
                             total_spent=0,
                             total_budget=0,
                             income=0,
                             weekly_spending=0)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    try:
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
    except Exception as e:
        print(f"Add transaction error: {e}")
        print(traceback.format_exc())
        flash('An error occurred adding the transaction. Please try again.', 'error')
        return render_template('add_transaction.html')

@app.route('/set_budget', methods=['GET', 'POST'])
def set_budget():
    try:
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
    except Exception as e:
        print(f"Set budget error: {e}")
        print(traceback.format_exc())
        flash('An error occurred setting the budget. Please try again.', 'error')
        return render_template('set_budget.html')

@app.route('/spending_analysis')
def spending_analysis():
    try:
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
    except Exception as e:
        print(f"Spending analysis error: {e}")
        print(traceback.format_exc())
        flash('An error occurred loading spending analysis. Please try again.', 'error')
        return render_template('spending_analysis.html', 
                             category_spending={},
                             transactions=[])

@app.route('/ml_recommendations')
def ml_recommendations():
    try:
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
    except Exception as e:
        print(f"ML recommendations error: {e}")
        print(traceback.format_exc())
        flash('An error occurred loading recommendations. Please try again.', 'error')
        return render_template('ml_recommendations.html', recommendations=[])

@app.route('/goals')
def goals_page():
    try:
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user_id = session['user_id']
        user_goals = [g for g in goals if g.get('user_id') == user_id]
        
        return render_template('goals.html', goals=user_goals)
    except Exception as e:
        print(f"Goals error: {e}")
        print(traceback.format_exc())
        flash('An error occurred loading goals. Please try again.', 'error')
        return render_template('goals.html', goals=[])

@app.route('/add_goal', methods=['POST'])
def add_goal():
    try:
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
    except Exception as e:
        print(f"Add goal error: {e}")
        print(traceback.format_exc())
        flash('An error occurred adding the goal. Please try again.', 'error')
        return redirect(url_for('goals_page'))

@app.route('/update_goal_progress', methods=['POST'])
def update_goal_progress():
    try:
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
    except Exception as e:
        print(f"Update goal progress error: {e}")
        print(traceback.format_exc())
        flash('An error occurred updating goal progress. Please try again.', 'error')
        return redirect(url_for('goals_page'))

@app.route('/export_data')
def export_data():
    try:
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
    except Exception as e:
        print(f"Export data error: {e}")
        print(traceback.format_exc())
        flash('An error occurred exporting data. Please try again.', 'error')
        return redirect(url_for('dashboard'))

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

@app.route('/dashboard-simple')
def dashboard_simple():
    """Simple dashboard test without template"""
    try:
        if 'user_id' not in session:
            return jsonify({"error": "No user session", "redirect": "login"})
        
        user_id = session['user_id']
        username = session.get('username', 'Unknown')
        
        return jsonify({
            "status": "success",
            "user_id": user_id,
            "username": username,
            "message": "Dashboard access successful"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 