"""
Supabase configuration and database operations for the Budget App
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any
from datetime import datetime, date

# Load environment variables
load_dotenv()

class SupabaseManager:
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    def create_user_profile(self, user_id: str, email: str, username: str, income: float = 0) -> Dict:
        """Create a user profile in the users table"""
        try:
            data = {
                'id': user_id,
                'email': email,
                'username': username,
                'income': income
            }
            result = self.client.table('users').insert(data).execute()
            return result.data[0] if result.data else {}
        except Exception as e:
            print(f"Error creating user profile: {e}")
            return {}
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile by ID"""
        try:
            result = self.client.table('users').select('*').eq('id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    def update_user_income(self, user_id: str, income: float) -> bool:
        """Update user income"""
        try:
            self.client.table('users').update({'income': income}).eq('id', user_id).execute()
            return True
        except Exception as e:
            print(f"Error updating user income: {e}")
            return False
    
    def add_transaction(self, user_id: str, description: str, amount: float, 
                       category: str, transaction_date: str) -> Optional[Dict]:
        """Add a new transaction"""
        try:
            data = {
                'user_id': user_id,
                'description': description,
                'amount': amount,
                'category': category,
                'date': transaction_date
            }
            result = self.client.table('transactions').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return None
    
    def get_user_transactions(self, user_id: str) -> List[Dict]:
        """Get all transactions for a user"""
        try:
            result = self.client.table('transactions').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
    
    def set_user_budgets(self, user_id: str, budgets: Dict[str, float]) -> bool:
        """Set budgets for a user (replaces existing budgets)"""
        try:
            # Delete existing budgets
            self.client.table('budgets').delete().eq('user_id', user_id).execute()
            
            # Insert new budgets
            budget_data = []
            for category, amount in budgets.items():
                if amount > 0:  # Only add non-zero budgets
                    budget_data.append({
                        'user_id': user_id,
                        'category': category,
                        'amount': amount
                    })
            
            if budget_data:
                self.client.table('budgets').insert(budget_data).execute()
            return True
        except Exception as e:
            print(f"Error setting budgets: {e}")
            return False
    
    def get_user_budgets(self, user_id: str) -> Dict[str, float]:
        """Get budgets for a user"""
        try:
            result = self.client.table('budgets').select('*').eq('user_id', user_id).execute()
            budgets = {}
            for budget in result.data:
                budgets[budget['category']] = budget['amount']
            return budgets
        except Exception as e:
            print(f"Error getting budgets: {e}")
            return {}
    
    def add_goal(self, user_id: str, title: str, target_amount: float, 
                 deadline: str, category: str) -> Optional[Dict]:
        """Add a new financial goal"""
        try:
            data = {
                'user_id': user_id,
                'title': title,
                'target_amount': target_amount,
                'current_amount': 0,
                'deadline': deadline,
                'category': category
            }
            result = self.client.table('goals').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error adding goal: {e}")
            return None
    
    def get_user_goals(self, user_id: str) -> List[Dict]:
        """Get all goals for a user"""
        try:
            result = self.client.table('goals').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting goals: {e}")
            return []
    
    def update_goal_progress(self, goal_id: str, amount: float) -> bool:
        """Update goal progress by adding amount"""
        try:
            # Get current goal
            result = self.client.table('goals').select('current_amount').eq('id', goal_id).execute()
            if not result.data:
                return False
            
            current_amount = result.data[0]['current_amount']
            new_amount = current_amount + amount
            
            # Update goal
            self.client.table('goals').update({'current_amount': new_amount}).eq('id', goal_id).execute()
            return True
        except Exception as e:
            print(f"Error updating goal progress: {e}")
            return False
    
    def get_spending_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get spending analytics for a user"""
        try:
            # Get transactions
            transactions = self.get_user_transactions(user_id)
            
            # Calculate category spending
            category_spending = {}
            monthly_spending = {}
            
            for transaction in transactions:
                category = transaction['category']
                amount = transaction['amount']
                month = transaction['date'][:7]  # YYYY-MM
                
                # Category spending
                category_spending[category] = category_spending.get(category, 0) + amount
                
                # Monthly spending
                monthly_spending[month] = monthly_spending.get(month, 0) + amount
            
            return {
                'category_spending': category_spending,
                'monthly_spending': monthly_spending,
                'total_transactions': len(transactions),
                'total_spent': sum(t['amount'] for t in transactions)
            }
        except Exception as e:
            print(f"Error getting analytics: {e}")
            return {
                'category_spending': {},
                'monthly_spending': {},
                'total_transactions': 0,
                'total_spent': 0
            }

# Global instance
supabase_manager = None

def get_supabase_manager() -> SupabaseManager:
    """Get or create Supabase manager instance"""
    global supabase_manager
    if supabase_manager is None:
        try:
            supabase_manager = SupabaseManager()
        except Exception as e:
            print(f"Failed to initialize Supabase: {e}")
            return None
    return supabase_manager 