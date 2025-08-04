from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
import json
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///budget.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    income = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    budgets = db.relationship('Budget', backref='user', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_type = db.Column(db.String(20), default='expense')

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    month = db.Column(db.String(7), nullable=False)

class SimpleAnalytics:
    def __init__(self):
        pass
    
    def calculate_averages(self, transactions):
        """Calculate simple spending averages by category"""
        if not transactions:
            return {}
        
        category_totals = defaultdict(float)
        category_counts = defaultdict(int)
        
        for transaction in transactions:
            if transaction.transaction_type == 'expense':
                category_totals[transaction.category] += transaction.amount
                category_counts[transaction.category] += 1
        
        averages = {}
        for category in category_totals:
            if category_counts[category] > 0:
                averages[category] = category_totals[category] / category_counts[category]
        
        return averages
    
    def predict_simple_budget(self, transactions, category):
        """Simple budget prediction based on historical averages"""
        if not transactions:
            return 0
        
        category_transactions = [t for t in transactions 
                               if t.category == category and t.transaction_type == 'expense']
        
        if not category_transactions:
            return 0
        
        total = sum(t.amount for t in category_transactions)
        avg = total / len(category_transactions)
        
        # Simple prediction: average + 10% buffer
        return avg * 1.1
    
    def get_spending_trends(self, transactions):
        """Get simple spending trends by month"""
        if not transactions:
            return {}
        
        monthly_spending = defaultdict(float)
        
        for transaction in transactions:
            if transaction.transaction_type == 'expense':
                month_key = transaction.date.strftime('%Y-%m')
                monthly_spending[month_key] += transaction.amount
        
        return dict(monthly_spending)

# Initialize analytics
analytics = SimpleAnalytics()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        income = float(request.form['income'])
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        user = User(username=username, email=email, 
                   password_hash=generate_password_hash(password), income=income)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful!')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).limit(10).all()
    
    category_spending = {}
    total_spent = 0
    
    for transaction in Transaction.query.filter_by(user_id=current_user.id).all():
        if transaction.transaction_type == 'expense':
            category = transaction.category
            if category not in category_spending:
                category_spending[category] = 0
            category_spending[category] += transaction.amount
            total_spent += transaction.amount
    
    current_month = datetime.now().strftime('%Y-%m')
    budgets = Budget.query.filter_by(user_id=current_user.id, month=current_month).all()
    
    return render_template('dashboard.html', 
                         transactions=transactions,
                         category_spending=category_spending,
                         total_spent=total_spent,
                         budgets=budgets,
                         income=current_user.income)

@app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form['description']
    transaction_type = request.form['transaction_type']
    
    transaction = Transaction(
        user_id=current_user.id,
        amount=amount,
        category=category,
        description=description,
        transaction_type=transaction_type
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    flash('Transaction added successfully!')
    return redirect(url_for('dashboard'))

@app.route('/set_budget', methods=['POST'])
@login_required
def set_budget():
    category = request.form['category']
    amount = float(request.form['amount'])
    current_month = datetime.now().strftime('%Y-%m')
    
    existing_budget = Budget.query.filter_by(
        user_id=current_user.id,
        category=category,
        month=current_month
    ).first()
    
    if existing_budget:
        existing_budget.amount = amount
    else:
        budget = Budget(
            user_id=current_user.id,
            category=category,
            amount=amount,
            month=current_month
        )
        db.session.add(budget)
    
    db.session.commit()
    flash('Budget set successfully!')
    return redirect(url_for('dashboard'))

@app.route('/ml_recommendations')
@login_required
def ml_recommendations():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    
    if len(transactions) < 3:
        return jsonify({'error': 'Not enough transaction data for recommendations'})
    
    # Get unique categories
    categories = list(set(t.category for t in transactions if t.transaction_type == 'expense'))
    
    recommendations = {}
    for category in categories:
        predicted_budget = analytics.predict_simple_budget(transactions, category)
        recommendations[category] = {
            'predicted_spending': round(predicted_budget, 2),
            'recommended_budget': round(predicted_budget * 1.1, 2)
        }
    
    return jsonify(recommendations)

@app.route('/spending_analysis')
@login_required
def spending_analysis():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    
    if len(transactions) == 0:
        return jsonify({'error': 'No transaction data available'})
    
    expenses = [t for t in transactions if t.transaction_type == 'expense']
    
    if not expenses:
        return jsonify({'error': 'No expense data available'})
    
    total_spent = sum(t.amount for t in expenses)
    avg_transaction = total_spent / len(expenses)
    
    # Calculate top categories
    category_totals = defaultdict(float)
    for transaction in expenses:
        category_totals[transaction.category] += transaction.amount
    
    top_categories = dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5])
    
    # Calculate monthly trends
    monthly_trends = analytics.get_spending_trends(expenses)
    
    analysis = {
        'total_spent': float(total_spent),
        'avg_transaction': float(avg_transaction),
        'top_categories': top_categories,
        'monthly_trend': monthly_trends
    }
    
    return jsonify(analysis)

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 