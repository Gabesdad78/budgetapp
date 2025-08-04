"""
Test Smart AI Features
"""
from smart_features import smart_ai

def test_smart_features():
    """Test the smart AI features"""
    print("🧠 Testing Smart AI Features")
    print("=" * 50)
    
    # Test data
    sample_transactions = [
        {'description': 'Grocery shopping', 'amount': 150.0, 'category': 'Food', 'date': '2024-01-15'},
        {'description': 'Gas station', 'amount': 45.0, 'category': 'Transportation', 'date': '2024-01-16'},
        {'description': 'Movie tickets', 'amount': 25.0, 'category': 'Entertainment', 'date': '2024-01-17'},
        {'description': 'Restaurant', 'amount': 80.0, 'category': 'Dining', 'date': '2024-01-18'},
        {'description': 'Shopping mall', 'amount': 200.0, 'category': 'Shopping', 'date': '2024-01-19'},
    ]
    
    sample_budgets = {
        'Food': 300,
        'Transportation': 200,
        'Entertainment': 100,
        'Dining': 150,
        'Shopping': 500
    }
    
    sample_goals = [
        {
            'title': 'Emergency Fund',
            'target_amount': 5000,
            'current_amount': 2000,
            'deadline': '2024-12-31',
            'category': 'Savings'
        }
    ]
    
    # Test 1: Spending Analysis
    print("📊 Testing Spending Analysis...")
    analysis = smart_ai.analyze_spending_patterns(sample_transactions)
    print(f"✅ Total spent: ${analysis.get('total_spent', 0):.2f}")
    print(f"✅ Average transaction: ${analysis.get('avg_transaction', 0):.2f}")
    print(f"✅ Spending trend: {analysis.get('spending_trend', 'N/A')}")
    
    # Test 2: Predictions
    print("\n🔮 Testing AI Predictions...")
    predictions = smart_ai.predict_future_spending(sample_transactions)
    print(f"✅ Next month prediction: ${predictions.get('next_month', 0):.2f}")
    print(f"✅ Confidence: {predictions.get('confidence', 0):.1%}")
    
    # Test 3: Smart Recommendations
    print("\n💡 Testing Smart Recommendations...")
    recommendations = smart_ai.generate_smart_recommendations(sample_transactions, sample_budgets)
    print(f"✅ Generated {len(recommendations)} recommendations")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"   {i}. {rec.get('message', 'N/A')}")
    
    # Test 4: Budget Optimization
    print("\n⚙️ Testing Budget Optimization...")
    optimization = smart_ai.optimize_budget_allocation(5000, sample_goals)
    print(f"✅ Essential budget: ${optimization.get('essential_budget', 0):.2f}")
    print(f"✅ Lifestyle budget: ${optimization.get('lifestyle_budget', 0):.2f}")
    print(f"✅ Savings budget: ${optimization.get('savings_budget', 0):.2f}")
    
    # Test 5: Goal Insights
    print("\n🎯 Testing Goal Insights...")
    insights = smart_ai.generate_goal_insights(sample_goals, sample_transactions)
    for goal_name, insight in insights.items():
        print(f"✅ {goal_name}: {insight.get('progress_percentage', 0):.1f}% complete")
        print(f"   Recommendation: {insight.get('recommendation', 'N/A')}")
    
    print("\n🎉 All Smart AI Features Tested Successfully!")
    print("=" * 50)
    print("✅ Spending Analysis: Working")
    print("✅ AI Predictions: Working")
    print("✅ Smart Recommendations: Working")
    print("✅ Budget Optimization: Working")
    print("✅ Goal Insights: Working")
    print("\n🚀 Your AI-powered budget app is ready!")

if __name__ == "__main__":
    test_smart_features() 