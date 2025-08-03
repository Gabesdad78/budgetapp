from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
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

class MLModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
    def prepare_data(self, transactions_df):
        """Prepare transaction data for ML model"""
        transactions_df['month'] = pd.to_datetime(transactions_df['date']).dt.month
        transactions_df['day_of_week'] = pd.to_datetime(transactions_df['date']).dt.dayofweek
        transactions_df['day_of_month'] = pd.to_datetime(transactions_df['date']).dt.day
        transactions_df['category_encoded'] = self.label_encoder.fit_transform(transactions_df['category'])
        transactions_df['is_weekend'] = transactions_df['day_of_week'].isin([5, 6]).astype(int)
        transactions_df['is_month_start'] = (transactions_df['day_of_month'] <= 5).astype(int)
        transactions_df['is_month_end'] = (transactions_df['day_of_month'] >= 25).astype(int)
        return transactions_df
    
    def train_model(self, transactions_df):
        """Train the ML model on transaction data"""
        if len(transactions_df) < 10:
            return False
            
        df = self.prepare_data(transactions_df)
        features = ['month', 'day_of_week', 'day_of_month', 'category_encoded', 
                   'is_weekend', 'is_month_start', 'is_month_end']
        
        X = df[features]
        y = df['amount']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)
        
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.is_trained = True
        return True
    
    def predict_spending(self, category, date):
        """Predict spending for a given category and date"""
        if not self.is_trained:
            return None
            
        input_data = pd.DataFrame({
            'month': [date.month],
            'day_of_week': [date.weekday()],
            'day_of_month': [date.day],
            'category_encoded': [self.label_encoder.transform([category])[0]],
            'is_weekend': [1 if date.weekday() in [5, 6] else 0],
            'is_month_start': [1 if date.day <= 5 else 0],
            'is_month_end': [1 if date.day >= 25 else 0]
        })
        
        input_scaled = self.scaler.transform(input_data)
        prediction = self.model.predict(input_scaled)[0]
        
        return max(0, prediction)

# Initialize ML model
ml_model = MLModel()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    
    transactions_df = pd.read_sql(
        Transaction.query.filter_by(user_id=current_user.id).statement,
        db.engine
    )
    if len(transactions_df) > 0:
        ml_model.train_model(transactions_df)
    
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
    transactions_df = pd.read_sql(
        Transaction.query.filter_by(user_id=current_user.id).statement,
        db.engine
    )
    
    if len(transactions_df) < 10:
        return jsonify({'error': 'Not enough transaction data for ML recommendations'})
    
    if not ml_model.is_trained:
        ml_model.train_model(transactions_df)
    
    recommendations = {}
    categories = transactions_df['category'].unique()
    
    for category in categories:
        next_month = datetime.now() + timedelta(days=30)
        predicted_spending = ml_model.predict_spending(category, next_month)
        
        if predicted_spending:
            recommendations[category] = {
                'predicted_spending': round(predicted_spending, 2),
                'recommended_budget': round(predicted_spending * 1.1, 2)
            }
    
    return jsonify(recommendations)

@app.route('/spending_analysis')
@login_required
def spending_analysis():
    transactions_df = pd.read_sql(
        Transaction.query.filter_by(user_id=current_user.id).statement,
        db.engine
    )
    
    if len(transactions_df) == 0:
        return jsonify({'error': 'No transaction data available'})
    
    expenses_df = transactions_df[transactions_df['transaction_type'] == 'expense']
    
    analysis = {
        'total_spent': float(expenses_df['amount'].sum()),
        'avg_transaction': float(expenses_df['amount'].mean()),
        'top_categories': expenses_df.groupby('category')['amount'].sum().nlargest(5).to_dict(),
        'monthly_trend': expenses_df.groupby(pd.to_datetime(expenses_df['date']).dt.to_period('M'))['amount'].sum().to_dict()
    }
    
    return jsonify(analysis)

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 