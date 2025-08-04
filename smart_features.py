"""
Smart AI Features for Budget App
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json

class SmartBudgetAI:
    def __init__(self):
        """Initialize Smart Budget AI"""
        self.spending_patterns = {}
        self.category_insights = {}
        self.predictions = {}
    
    def analyze_spending_patterns(self, transactions: List[Dict]) -> Dict:
        """Analyze spending patterns using AI"""
        if not transactions:
            return {"message": "No transactions to analyze"}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Calculate spending patterns
        patterns = {
            'total_spent': float(df['amount'].sum()),
            'avg_transaction': float(df['amount'].mean()),
            'total_transactions': len(df),
            'spending_by_category': df.groupby('category')['amount'].sum().to_dict(),
            'spending_by_month': df.groupby(df['date'].dt.to_period('M'))['amount'].sum().to_dict(),
            'top_categories': df.groupby('category')['amount'].sum().nlargest(5).to_dict(),
            'spending_trend': self._calculate_trend(df),
            'anomalies': self._detect_anomalies(df)
        }
        
        return patterns
    
    def _calculate_trend(self, df: pd.DataFrame) -> str:
        """Calculate spending trend"""
        monthly_spending = df.groupby(df['date'].dt.to_period('M'))['amount'].sum()
        if len(monthly_spending) < 2:
            return "Insufficient data for trend analysis"
        
        # Simple trend calculation
        recent_months = monthly_spending.tail(3)
        if len(recent_months) >= 2:
            trend = recent_months.iloc[-1] - recent_months.iloc[-2]
            if trend > 0:
                return f"Increasing by ${trend:.2f} per month"
            elif trend < 0:
                return f"Decreasing by ${abs(trend):.2f} per month"
            else:
                return "Stable spending"
        return "Stable spending"
    
    def _detect_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """Detect spending anomalies"""
        anomalies = []
        
        # Detect high-value transactions (above 2 standard deviations)
        mean_amount = df['amount'].mean()
        std_amount = df['amount'].std()
        threshold = mean_amount + (2 * std_amount)
        
        high_value = df[df['amount'] > threshold]
        for _, row in high_value.iterrows():
            anomalies.append({
                'type': 'high_value',
                'amount': float(row['amount']),
                'category': row['category'],
                'date': str(row['date']),
                'description': row['description']
            })
        
        return anomalies
    
    def predict_future_spending(self, transactions: List[Dict], months_ahead: int = 3) -> Dict:
        """Predict future spending based on patterns"""
        if not transactions:
            return {"message": "No data for predictions"}
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Calculate monthly averages
        monthly_avg = df.groupby(df['date'].dt.to_period('M'))['amount'].sum().mean()
        
        predictions = {
            'next_month': float(monthly_avg),
            'next_3_months': float(monthly_avg * 3),
            'category_predictions': self._predict_category_spending(df),
            'confidence': self._calculate_confidence(df)
        }
        
        return predictions
    
    def _predict_category_spending(self, df: pd.DataFrame) -> Dict:
        """Predict spending by category"""
        category_avg = df.groupby('category')['amount'].mean()
        return category_avg.to_dict()
    
    def _calculate_confidence(self, df: pd.DataFrame) -> float:
        """Calculate prediction confidence based on data consistency"""
        if len(df) < 10:
            return 0.3  # Low confidence with little data
        elif len(df) < 30:
            return 0.6  # Medium confidence
        else:
            return 0.8  # High confidence with lots of data
    
    def generate_smart_recommendations(self, transactions: List[Dict], budgets: Dict) -> List[Dict]:
        """Generate AI-powered recommendations"""
        recommendations = []
        
        if not transactions:
            return [{"type": "no_data", "message": "Start adding transactions to get personalized recommendations"}]
        
        df = pd.DataFrame(transactions)
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Analyze spending patterns
        total_spent = df['amount'].sum()
        category_spending = df.groupby('category')['amount'].sum()
        
        # Recommendation 1: Budget optimization
        if budgets:
            for category, budget in budgets.items():
                if category in category_spending:
                    spent = category_spending[category]
                    percentage = (spent / budget) * 100
                    
                    if percentage > 90:
                        recommendations.append({
                            "type": "budget_warning",
                            "category": category,
                            "message": f"You're at {percentage:.1f}% of your {category} budget",
                            "suggestion": "Consider reducing spending in this category"
                        })
                    elif percentage < 30:
                        recommendations.append({
                            "type": "budget_opportunity",
                            "category": category,
                            "message": f"You're only using {percentage:.1f}% of your {category} budget",
                            "suggestion": "You could reallocate some budget to other categories"
                        })
        
        # Recommendation 2: Savings opportunities
        top_categories = category_spending.nlargest(3)
        for category, amount in top_categories.items():
            if amount > total_spent * 0.3:  # If category is >30% of total spending
                recommendations.append({
                    "type": "savings_opportunity",
                    "category": category,
                    "message": f"{category} represents {((amount/total_spent)*100):.1f}% of your spending",
                    "suggestion": f"Consider reducing {category} expenses to save more"
                })
        
        # Recommendation 3: Spending pattern insights
        if len(df) >= 10:
            avg_transaction = df['amount'].mean()
            if avg_transaction > 100:
                recommendations.append({
                    "type": "spending_insight",
                    "message": f"Your average transaction is ${avg_transaction:.2f}",
                    "suggestion": "Consider smaller, more frequent purchases to better track spending"
                })
        
        return recommendations
    
    def optimize_budget_allocation(self, income: float, goals: List[Dict]) -> Dict:
        """AI-powered budget optimization"""
        if income <= 0:
            return {"message": "Please set your income to get budget recommendations"}
        
        # 50/30/20 rule with AI adjustments
        essential_categories = ['Housing', 'Food', 'Transportation', 'Healthcare']
        lifestyle_categories = ['Entertainment', 'Shopping', 'Dining']
        savings_categories = ['Savings', 'Investments', 'Emergency Fund']
        
        # Calculate goal requirements
        total_goal_amount = sum(goal.get('target_amount', 0) for goal in goals)
        monthly_goal_savings = total_goal_amount / 12 if total_goal_amount > 0 else income * 0.2
        
        # Smart allocation
        essential_budget = income * 0.5
        lifestyle_budget = income * 0.3
        savings_budget = max(monthly_goal_savings, income * 0.2)
        
        # Adjust if savings needs exceed 20%
        if savings_budget > income * 0.2:
            excess = savings_budget - (income * 0.2)
            lifestyle_budget -= excess * 0.7
            essential_budget -= excess * 0.3
        
        return {
            "essential_budget": float(essential_budget),
            "lifestyle_budget": float(lifestyle_budget),
            "savings_budget": float(savings_budget),
            "essential_categories": essential_categories,
            "lifestyle_categories": lifestyle_categories,
            "savings_categories": savings_categories,
            "recommendation": "This allocation prioritizes your financial goals while maintaining essential needs"
        }
    
    def generate_goal_insights(self, goals: List[Dict], transactions: List[Dict]) -> Dict:
        """Generate insights about financial goals"""
        insights = {}
        
        for goal in goals:
            target_amount = goal.get('target_amount', 0)
            current_amount = goal.get('current_amount', 0)
            deadline = goal.get('deadline')
            
            if target_amount > 0 and deadline:
                # Calculate progress
                progress_percentage = (current_amount / target_amount) * 100
                
                # Calculate time remaining
                deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
                days_remaining = (deadline_date - datetime.now()).days
                
                # Calculate required monthly savings
                remaining_amount = target_amount - current_amount
                monthly_required = remaining_amount / max(days_remaining / 30, 1)
                
                insights[goal.get('title', 'Unknown Goal')] = {
                    "progress_percentage": progress_percentage,
                    "days_remaining": days_remaining,
                    "monthly_required": monthly_required,
                    "on_track": progress_percentage >= (100 - (days_remaining / 365) * 100),
                    "recommendation": self._get_goal_recommendation(progress_percentage, days_remaining, monthly_required)
                }
        
        return insights
    
    def _get_goal_recommendation(self, progress: float, days_remaining: int, monthly_required: float) -> str:
        """Get personalized goal recommendations"""
        if days_remaining <= 0:
            return "Goal deadline has passed. Consider extending the deadline or adjusting the target."
        elif progress >= 100:
            return "Congratulations! You've reached your goal!"
        elif progress >= 75:
            return f"You're very close! Just ${monthly_required:.2f} more needed per month."
        elif progress >= 50:
            return f"Good progress! You need ${monthly_required:.2f} per month to stay on track."
        elif progress >= 25:
            return f"Keep going! You need ${monthly_required:.2f} per month to reach your goal."
        else:
            return f"Getting started! You need ${monthly_required:.2f} per month to reach your goal."

# Global instance
smart_ai = SmartBudgetAI() 