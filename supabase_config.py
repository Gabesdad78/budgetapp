"""
Supabase Configuration and Database Manager
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SupabaseManager:
    def __init__(self):
        """Initialize Supabase client"""
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_ANON_KEY')
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        
        self.client: Client = create_client(self.url, self.key)
    
    def create_user_profile(self, user_id: str, email: str, username: str, income: float = 0):
        """Create user profile in database"""
        try:
            data = {
                'id': user_id,
                'email': email,
                'username': username,
                'income': income
            }
            result = self.client.table('users').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating user profile: {e}")
            return None
    
    def get_user_profile(self, user_id: str):
        """Get user profile by user ID"""
        try:
            result = self.client.table('users').select('*').eq('id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    def get_user_profile_by_username(self, username: str):
        """Get user profile by username"""
        try:
            result = self.client.table('users').select('*').eq('username', username).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting user profile by username: {e}")
            return None
    
    def get_user_transactions(self, user_id: str):
        """Get all transactions for a user"""
        try:
            result = self.client.table('transactions').select('*').eq('user_id', user_id).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting user transactions: {e}")
            return []
    
    def get_user_budgets(self, user_id: str):
        """Get all budgets for a user"""
        try:
            result = self.client.table('budgets').select('*').eq('user_id', user_id).execute()
            budgets = {}
            for budget in result.data:
                budgets[budget['category']] = budget['amount']
            return budgets
        except Exception as e:
            print(f"Error getting user budgets: {e}")
            return {}
    
    def get_user_goals(self, user_id: str):
        """Get all goals for a user"""
        try:
            result = self.client.table('goals').select('*').eq('user_id', user_id).execute()
            return result.data if result.data else []
        except Exception as e:
            print(f"Error getting user goals: {e}")
            return []
    
    def add_transaction(self, user_id: str, description: str, amount: float, category: str, date: str):
        """Add a new transaction"""
        try:
            data = {
                'user_id': user_id,
                'description': description,
                'amount': amount,
                'category': category,
                'date': date
            }
            result = self.client.table('transactions').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error adding transaction: {e}")
            return None
    
    def set_user_budgets(self, user_id: str, budgets: dict):
        """Set budgets for a user"""
        try:
            # Delete existing budgets
            self.client.table('budgets').delete().eq('user_id', user_id).execute()
            
            # Insert new budgets
            budget_data = []
            for category, amount in budgets.items():
                if amount > 0:
                    budget_data.append({
                        'user_id': user_id,
                        'category': category,
                        'amount': amount
                    })
            
            if budget_data:
                result = self.client.table('budgets').insert(budget_data).execute()
                return result.data if result.data else []
            return []
        except Exception as e:
            print(f"Error setting user budgets: {e}")
            return []
    
    def add_goal(self, user_id: str, title: str, target_amount: float, deadline: str, category: str = None):
        """Add a new goal"""
        try:
            data = {
                'user_id': user_id,
                'title': title,
                'target_amount': target_amount,
                'deadline': deadline,
                'category': category
            }
            result = self.client.table('goals').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error adding goal: {e}")
            return None
    
    def update_goal_progress(self, goal_id: str, current_amount: float):
        """Update goal progress"""
        try:
            data = {'current_amount': current_amount}
            result = self.client.table('goals').update(data).eq('id', goal_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error updating goal progress: {e}")
            return None
    
    def get_spending_analytics(self, user_id: str):
        """Get spending analytics for a user"""
        try:
            transactions = self.get_user_transactions(user_id)
            if not transactions:
                return {}
            
            total_spent = sum(t['amount'] for t in transactions)
            category_spending = {}
            
            for transaction in transactions:
                category = transaction['category']
                amount = transaction['amount']
                category_spending[category] = category_spending.get(category, 0) + amount
            
            return {
                'total_spent': total_spent,
                'category_spending': category_spending,
                'transaction_count': len(transactions)
            }
        except Exception as e:
            print(f"Error getting spending analytics: {e}")
            return {}

# Global instance
_supabase_manager = None

def get_supabase_manager():
    """Get or create Supabase manager instance"""
    global _supabase_manager
    if _supabase_manager is None:
        try:
            _supabase_manager = SupabaseManager()
        except Exception as e:
            print(f"Error initializing Supabase manager: {e}")
            # Return a mock manager for development
            return MockSupabaseManager()
    return _supabase_manager

class MockSupabaseManager:
    """Mock Supabase manager for development/testing"""
    def __init__(self):
        self.users = {}
        self.transactions = []
        self.budgets = {}
        self.goals = []
    
    def create_user_profile(self, user_id: str, email: str, username: str, income: float = 0):
        user = {'id': user_id, 'email': email, 'username': username, 'income': income}
        self.users[user_id] = user
        return user
    
    def get_user_profile(self, user_id: str):
        return self.users.get(user_id)
    
    def get_user_profile_by_username(self, username: str):
        for user in self.users.values():
            if user.get('username') == username:
                return user
        return None
    
    def get_user_transactions(self, user_id: str):
        return [t for t in self.transactions if t.get('user_id') == user_id]
    
    def get_user_budgets(self, user_id: str):
        return self.budgets.get(user_id, {})
    
    def get_user_goals(self, user_id: str):
        return [g for g in self.goals if g.get('user_id') == user_id]
    
    def add_transaction(self, user_id: str, description: str, amount: float, category: str, date: str):
        transaction = {
            'id': str(len(self.transactions) + 1),
            'user_id': user_id,
            'description': description,
            'amount': amount,
            'category': category,
            'date': date
        }
        self.transactions.append(transaction)
        return transaction
    
    def set_user_budgets(self, user_id: str, budgets: dict):
        self.budgets[user_id] = budgets
        return [{'category': k, 'amount': v} for k, v in budgets.items()]
    
    def add_goal(self, user_id: str, title: str, target_amount: float, deadline: str, category: str = None):
        goal = {
            'id': str(len(self.goals) + 1),
            'user_id': user_id,
            'title': title,
            'target_amount': target_amount,
            'current_amount': 0,
            'deadline': deadline,
            'category': category
        }
        self.goals.append(goal)
        return goal
    
    def update_goal_progress(self, goal_id: str, current_amount: float):
        for goal in self.goals:
            if goal.get('id') == goal_id:
                goal['current_amount'] = current_amount
                return goal
        return None
    
    def get_spending_analytics(self, user_id: str):
        transactions = self.get_user_transactions(user_id)
        if not transactions:
            return {}
        
        total_spent = sum(t['amount'] for t in transactions)
        category_spending = {}
        
        for transaction in transactions:
            category = transaction['category']
            amount = transaction['amount']
            category_spending[category] = category_spending.get(category, 0) + amount
        
        return {
            'total_spent': total_spent,
            'category_spending': category_spending,
            'transaction_count': len(transactions)
        } 