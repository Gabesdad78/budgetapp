"""
Smart AI Routes for Budget App
"""
from flask import Blueprint, render_template, jsonify, request, session
from smart_features import smart_ai
from supabase_config import get_supabase_manager

smart_bp = Blueprint('smart', __name__)

@smart_bp.route('/ai-analysis')
def ai_analysis():
    """AI-powered spending analysis"""
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        supabase = get_supabase_manager()
        user_id = session['user_id']
        
        # Get user transactions
        transactions = supabase.get_user_transactions(user_id)
        
        # Get AI analysis
        analysis = smart_ai.analyze_spending_patterns(transactions)
        
        return render_template('ai_analysis.html', analysis=analysis)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@smart_bp.route('/ai-predictions')
def ai_predictions():
    """AI-powered spending predictions"""
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        supabase = get_supabase_manager()
        user_id = session['user_id']
        
        # Get user transactions
        transactions = supabase.get_user_transactions(user_id)
        
        # Get AI predictions
        predictions = smart_ai.predict_future_spending(transactions)
        
        return render_template('ai_predictions.html', predictions=predictions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@smart_bp.route('/smart-recommendations')
def smart_recommendations():
    """AI-powered smart recommendations"""
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        supabase = get_supabase_manager()
        user_id = session['user_id']
        
        # Get user data
        transactions = supabase.get_user_transactions(user_id)
        budgets = supabase.get_user_budgets(user_id)
        
        # Get AI recommendations
        recommendations = smart_ai.generate_smart_recommendations(transactions, budgets)
        
        return render_template('smart_recommendations.html', recommendations=recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@smart_bp.route('/budget-optimizer')
def budget_optimizer():
    """AI-powered budget optimization"""
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        supabase = get_supabase_manager()
        user_id = session['user_id']
        
        # Get user data
        user_profile = supabase.get_user_profile(user_id)
        goals = supabase.get_user_goals(user_id)
        
        income = user_profile.get('income', 0) if user_profile else 0
        
        # Get AI budget optimization
        optimization = smart_ai.optimize_budget_allocation(income, goals)
        
        return render_template('budget_optimizer.html', optimization=optimization)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@smart_bp.route('/goal-insights')
def goal_insights():
    """AI-powered goal insights"""
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        supabase = get_supabase_manager()
        user_id = session['user_id']
        
        # Get user data
        goals = supabase.get_user_goals(user_id)
        transactions = supabase.get_user_transactions(user_id)
        
        # Get AI goal insights
        insights = smart_ai.generate_goal_insights(goals, transactions)
        
        return render_template('goal_insights.html', insights=insights)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@smart_bp.route('/api/smart-analysis')
def api_smart_analysis():
    """API endpoint for smart analysis"""
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    try:
        supabase = get_supabase_manager()
        user_id = session['user_id']
        
        # Get user data
        transactions = supabase.get_user_transactions(user_id)
        budgets = supabase.get_user_budgets(user_id)
        goals = supabase.get_user_goals(user_id)
        user_profile = supabase.get_user_profile(user_id)
        
        # Comprehensive AI analysis
        analysis = smart_ai.analyze_spending_patterns(transactions)
        predictions = smart_ai.predict_future_spending(transactions)
        recommendations = smart_ai.generate_smart_recommendations(transactions, budgets)
        
        income = user_profile.get('income', 0) if user_profile else 0
        optimization = smart_ai.optimize_budget_allocation(income, goals)
        goal_insights = smart_ai.generate_goal_insights(goals, transactions)
        
        return jsonify({
            "analysis": analysis,
            "predictions": predictions,
            "recommendations": recommendations,
            "optimization": optimization,
            "goal_insights": goal_insights
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500 