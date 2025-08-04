from flask import Flask, jsonify, request

app = Flask(__name__)

# Simple in-memory storage
users = {}
transactions = {}
budgets = {}

@app.route('/')
def index():
    return jsonify({
        "message": "Budget App is running!",
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() or request.form
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
        
        return jsonify({
            "message": "Registration successful!",
            "username": username,
            "status": "success"
        })
    
    return jsonify({
        "message": "Register endpoint",
        "method": "POST",
        "fields": ["username", "email", "password", "income"]
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() or request.form
        username = data.get('username', 'demo')
        password = data.get('password', 'password')
        
        if username in users and users[username]['password'] == password:
            return jsonify({
                "message": "Login successful!",
                "username": username,
                "status": "success"
            })
        else:
            return jsonify({
                "message": "Invalid username or password",
                "status": "error"
            }), 401
    
    return jsonify({
        "message": "Login endpoint",
        "method": "POST",
        "fields": ["username", "password"]
    })

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
    
    return jsonify({
        "message": "Dashboard data",
        "username": username,
        "income": user['income'],
        "total_spent": total_spent,
        "category_spending": category_spending,
        "recent_transactions": user_transactions[:5],
        "budgets": user_budgets,
        "status": "success"
    })

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.get_json() or request.form
    username = data.get('username', 'demo')
    user = users.get(username, {'id': 1})
    
    amount = float(data.get('amount', 0))
    category = data.get('category', 'Other')
    description = data.get('description', 'Transaction')
    transaction_type = data.get('transaction_type', 'expense')
    
    transaction_id = len(transactions) + 1
    transactions[transaction_id] = {
        'user_id': user['id'],
        'amount': amount,
        'category': category,
        'description': description,
        'transaction_type': transaction_type,
        'date': '2024-01-01'
    }
    
    return jsonify({
        "message": "Transaction added successfully!",
        "transaction_id": transaction_id,
        "status": "success"
    })

@app.route('/set_budget', methods=['POST'])
def set_budget():
    data = request.get_json() or request.form
    username = data.get('username', 'demo')
    user = users.get(username, {'id': 1})
    
    category = data.get('category', 'Other')
    amount = float(data.get('amount', 0))
    
    budget_id = len(budgets) + 1
    budgets[budget_id] = {
        'user_id': user['id'],
        'category': category,
        'amount': amount,
        'month': '2024-01'
    }
    
    return jsonify({
        "message": "Budget set successfully!",
        "budget_id": budget_id,
        "status": "success"
    })

@app.route('/ml_recommendations')
def ml_recommendations():
    username = request.args.get('username', 'demo')
    user = users.get(username, {'id': 1})
    
    user_transactions = [t for t in transactions.values() if t.get('user_id') == user['id']]
    
    if len(user_transactions) < 3:
        return jsonify({
            "error": "Not enough transaction data for recommendations",
            "status": "error"
        })
    
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
    
    return jsonify({
        "recommendations": recommendations,
        "status": "success"
    })

@app.route('/spending_analysis')
def spending_analysis():
    username = request.args.get('username', 'demo')
    user = users.get(username, {'id': 1})
    
    user_transactions = [t for t in transactions.values() if t.get('user_id') == user['id']]
    
    if len(user_transactions) == 0:
        return jsonify({
            "error": "No transaction data available",
            "status": "error"
        })
    
    expenses = [t for t in user_transactions if t.get('transaction_type') == 'expense']
    
    if not expenses:
        return jsonify({
            "error": "No expense data available",
            "status": "error"
        })
    
    total_spent = sum(t.get('amount', 0) for t in expenses)
    avg_transaction = total_spent / len(expenses)
    
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
        'monthly_trend': {'2024-01': total_spent}
    }
    
    return jsonify({
        "analysis": analysis,
        "status": "success"
    })

@app.route('/test')
def test():
    return jsonify({
        "message": "App is working!",
        "status": "success",
        "timestamp": "2024-01-01"
    })

if __name__ == '__main__':
    app.run(debug=True) 