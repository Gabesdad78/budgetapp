#!/usr/bin/env python3
"""
Sample Data Generator for ML Budget App
Adds sample transactions to demonstrate ML features
"""

from app import app, db, User, Transaction
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample transaction data for demonstration"""
    
    with app.app_context():
        # Check if we have any users
        user = User.query.first()
        if not user:
            print("❌ No users found. Please register an account first.")
            return
        
        print(f"📊 Adding sample data for user: {user.username}")
        
        # Sample categories and their typical spending patterns
        categories = {
            'Food & Dining': {'min': 20, 'max': 150, 'frequency': 0.3},
            'Transportation': {'min': 15, 'max': 80, 'frequency': 0.2},
            'Housing': {'min': 800, 'max': 2000, 'frequency': 0.05},
            'Utilities': {'min': 50, 'max': 200, 'frequency': 0.1},
            'Entertainment': {'min': 30, 'max': 120, 'frequency': 0.15},
            'Healthcare': {'min': 25, 'max': 300, 'frequency': 0.08},
            'Shopping': {'min': 40, 'max': 200, 'frequency': 0.12},
            'Education': {'min': 100, 'max': 500, 'frequency': 0.03},
            'Insurance': {'min': 100, 'max': 400, 'frequency': 0.05},
            'Other': {'min': 10, 'max': 100, 'frequency': 0.1}
        }
        
        # Generate transactions for the last 3 months
        start_date = datetime.now() - timedelta(days=90)
        end_date = datetime.now()
        
        transactions_created = 0
        
        current_date = start_date
        while current_date <= end_date:
            # Add some income transactions
            if current_date.day == 1:  # Monthly income
                income_transaction = Transaction(
                    user_id=user.id,
                    amount=user.income,
                    category='Income',
                    description='Monthly Salary',
                    transaction_type='income',
                    date=current_date
                )
                db.session.add(income_transaction)
                transactions_created += 1
            
            # Add expense transactions based on category patterns
            for category, pattern in categories.items():
                if random.random() < pattern['frequency']:
                    # Adjust frequency based on day of week
                    day_of_week = current_date.weekday()
                    
                    # Higher frequency on weekends for entertainment and shopping
                    if category in ['Entertainment', 'Shopping'] and day_of_week in [5, 6]:
                        if random.random() < 0.7:  # 70% chance on weekends
                            amount = random.uniform(pattern['min'], pattern['max'])
                            transaction = Transaction(
                                user_id=user.id,
                                amount=round(amount, 2),
                                category=category,
                                description=f'Sample {category} transaction',
                                transaction_type='expense',
                                date=current_date
                            )
                            db.session.add(transaction)
                            transactions_created += 1
                    
                    # Regular frequency for other categories
                    elif category not in ['Entertainment', 'Shopping']:
                        amount = random.uniform(pattern['min'], pattern['max'])
                        transaction = Transaction(
                            user_id=user.id,
                            amount=round(amount, 2),
                            category=category,
                            description=f'Sample {category} transaction',
                            transaction_type='expense',
                            date=current_date
                        )
                        db.session.add(transaction)
                        transactions_created += 1
            
            current_date += timedelta(days=1)
        
        # Commit all transactions
        db.session.commit()
        
        print(f"✅ Created {transactions_created} sample transactions")
        print("🎯 The ML model will now be able to provide recommendations!")
        print("📊 Check the dashboard to see your spending analysis and ML recommendations")

if __name__ == "__main__":
    print("🚀 ML Budget App - Sample Data Generator")
    print("=" * 50)
    print("This script will add sample transaction data to demonstrate ML features.")
    print("Make sure you have registered an account first.")
    print("=" * 50)
    
    response = input("Continue? (y/n): ")
    if response.lower() in ['y', 'yes']:
        create_sample_data()
    else:
        print("❌ Sample data generation cancelled.") 