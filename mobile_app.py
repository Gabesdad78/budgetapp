#!/usr/bin/env python3
"""
ML Budget App - Mobile Version
Built with Kivy for Android compatibility
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.lang import Builder
import json
import os
from datetime import datetime, timedelta
import sqlite3
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import threading

# Set window size for desktop testing
Window.size = (400, 700)

# KV Language string for UI
KV = '''
#:import utils kivy.utils

<CustomButton@Button>:
    background_color: 0, 0, 0, 0
    canvas.before:
        Color:
            rgba: (0.4, 0.6, 0.9, 1) if self.state == 'normal' else (0.3, 0.5, 0.8, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]

<TransactionCard@BoxLayout>:
    orientation: 'vertical'
    size_hint_y: None
    height: dp(80)
    padding: dp(10)
    spacing: dp(5)
    canvas.before:
        Color:
            rgba: 0.95, 0.95, 0.95, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [8,]
    
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.7
        
        Label:
            text: root.description
            size_hint_x: 0.6
            halign: 'left'
            valign: 'middle'
            text_size: self.size
            color: 0.2, 0.2, 0.2, 1
            font_size: dp(16)
        
        Label:
            text: root.amount_text
            size_hint_x: 0.4
            halign: 'right'
            valign: 'middle'
            text_size: self.size
            color: root.amount_color
            font_size: dp(16)
            bold: True
    
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.3
        
        Label:
            text: root.category
            size_hint_x: 0.5
            halign: 'left'
            valign: 'middle'
            text_size: self.size
            color: 0.5, 0.5, 0.5, 1
            font_size: dp(12)
        
        Label:
            text: root.date
            size_hint_x: 0.5
            halign: 'right'
            valign: 'middle'
            text_size: self.size
            color: 0.5, 0.5, 0.5, 1
            font_size: dp(12)

<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        
        # Header
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.3
            
            Label:
                text: 'ML Budget App'
                font_size: dp(32)
                bold: True
                color: 0.4, 0.6, 0.9, 1
            
            Label:
                text: 'Smart Financial Management'
                font_size: dp(16)
                color: 0.6, 0.6, 0.6, 1
        
        # Login Form
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.4
            spacing: dp(15)
            
            TextInput:
                id: username
                hint_text: 'Username'
                multiline: False
                size_hint_y: None
                height: dp(50)
                font_size: dp(16)
                padding: dp(15)
                background_color: 1, 1, 1, 1
                foreground_color: 0.2, 0.2, 0.2, 1
                canvas.before:
                    Color:
                        rgba: 0.9, 0.9, 0.9, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [8,]
            
            TextInput:
                id: password
                hint_text: 'Password'
                multiline: False
                password: True
                size_hint_y: None
                height: dp(50)
                font_size: dp(16)
                padding: dp(15)
                background_color: 1, 1, 1, 1
                foreground_color: 0.2, 0.2, 0.2, 1
                canvas.before:
                    Color:
                        rgba: 0.9, 0.9, 0.9, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [8,]
            
            CustomButton:
                text: 'Login'
                size_hint_y: None
                height: dp(50)
                font_size: dp(18)
                bold: True
                on_press: root.login()
            
            CustomButton:
                text: 'Register'
                size_hint_y: None
                height: dp(50)
                font_size: dp(18)
                bold: True
                on_press: root.register()

<DashboardScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        
        # Header
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(60)
            
            Label:
                text: 'Dashboard'
                font_size: dp(24)
                bold: True
                color: 0.4, 0.6, 0.9, 1
            
            Button:
                text: 'Add'
                size_hint_x: 0.3
                on_press: root.show_add_transaction()
                background_color: 0.4, 0.6, 0.9, 1
        
        # Stats Cards
        GridLayout:
            cols: 2
            size_hint_y: None
            height: dp(200)
            spacing: dp(10)
            
            BoxLayout:
                orientation: 'vertical'
                canvas.before:
                    Color:
                        rgba: 0.4, 0.8, 0.4, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10,]
                padding: dp(15)
                
                Label:
                    text: 'Income'
                    font_size: dp(14)
                    color: 1, 1, 1, 1
                
                Label:
                    text: root.income_text
                    font_size: dp(20)
                    bold: True
                    color: 1, 1, 1, 1
            
            BoxLayout:
                orientation: 'vertical'
                canvas.before:
                    Color:
                        rgba: 0.9, 0.4, 0.4, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10,]
                padding: dp(15)
                
                Label:
                    text: 'Expenses'
                    font_size: dp(14)
                    color: 1, 1, 1, 1
                
                Label:
                    text: root.expenses_text
                    font_size: dp(20)
                    bold: True
                    color: 1, 1, 1, 1
            
            BoxLayout:
                orientation: 'vertical'
                canvas.before:
                    Color:
                        rgba: 0.4, 0.6, 0.9, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10,]
                padding: dp(15)
                
                Label:
                    text: 'Remaining'
                    font_size: dp(14)
                    color: 1, 1, 1, 1
                
                Label:
                    text: root.remaining_text
                    font_size: dp(20)
                    bold: True
                    color: 1, 1, 1, 1
            
            BoxLayout:
                orientation: 'vertical'
                canvas.before:
                    Color:
                        rgba: 0.9, 0.6, 0.4, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10,]
                padding: dp(15)
                
                Label:
                    text: 'Budget Used'
                    font_size: dp(14)
                    color: 1, 1, 1, 1
                
                Label:
                    text: root.budget_used_text
                    font_size: dp(20)
                    bold: True
                    color: 1, 1, 1, 1
        
        # Progress Bar
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(60)
            padding: dp(10)
            
            Label:
                text: 'Budget Progress'
                font_size: dp(16)
                bold: True
                color: 0.4, 0.6, 0.9, 1
            
            ProgressBar:
                id: budget_progress
                max: 100
                value: root.budget_percentage
        
        # Transactions List
        Label:
            text: 'Recent Transactions'
            font_size: dp(18)
            bold: True
            color: 0.4, 0.6, 0.9, 1
            size_hint_y: None
            height: dp(30)
        
        ScrollView:
            GridLayout:
                id: transactions_list
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(5)
                padding: dp(5)

<AddTransactionScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)
        
        Label:
            text: 'Add Transaction'
            font_size: dp(24)
            bold: True
            color: 0.4, 0.6, 0.9, 1
            size_hint_y: None
            height: dp(40)
        
        TextInput:
            id: description
            hint_text: 'Description'
            multiline: False
            size_hint_y: None
            height: dp(50)
            font_size: dp(16)
            padding: dp(15)
        
        TextInput:
            id: amount
            hint_text: 'Amount'
            multiline: False
            input_filter: 'float'
            size_hint_y: None
            height: dp(50)
            font_size: dp(16)
            padding: dp(15)
        
        Spinner:
            id: category
            text: 'Select Category'
            values: ['Food & Dining', 'Transportation', 'Entertainment', 'Shopping', 'Bills & Utilities', 'Healthcare', 'Education', 'Other']
            size_hint_y: None
            height: dp(50)
            font_size: dp(16)
        
        Spinner:
            id: transaction_type
            text: 'Expense'
            values: ['Expense', 'Income']
            size_hint_y: None
            height: dp(50)
            font_size: dp(16)
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            
            CustomButton:
                text: 'Cancel'
                on_press: root.cancel()
            
            CustomButton:
                text: 'Save'
                on_press: root.save_transaction()
'''

class TransactionCard(BoxLayout):
    description = StringProperty('')
    amount_text = StringProperty('')
    amount_color = StringProperty('0.4, 0.8, 0.4, 1')
    category = StringProperty('')
    date = StringProperty('')

class LoginScreen(Screen):
    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        
        if username and password:
            # Simple authentication for demo
            if username == 'demo' and password == 'demo':
                self.manager.current = 'dashboard'
            else:
                self.show_error('Invalid credentials')
        else:
            self.show_error('Please enter username and password')
    
    def register(self):
        username = self.ids.username.text
        password = self.ids.password.text
        
        if username and password:
            # Simple registration for demo
            self.manager.current = 'dashboard'
        else:
            self.show_error('Please enter username and password')
    
    def show_error(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()

class DashboardScreen(Screen):
    income_text = StringProperty('$0.00')
    expenses_text = StringProperty('$0.00')
    remaining_text = StringProperty('$0.00')
    budget_used_text = StringProperty('0%')
    budget_percentage = NumericProperty(0)
    
    def on_enter(self):
        self.load_data()
        self.update_transactions()
    
    def load_data(self):
        # Load data from storage
        store = JsonStore('budget_data.json')
        if store.exists('transactions'):
            transactions = store.get('transactions')['data']
            
            income = sum(t['amount'] for t in transactions if t['type'] == 'Income')
            expenses = sum(t['amount'] for t in transactions if t['type'] == 'Expense')
            remaining = income - expenses
            budget_used = (expenses / income * 100) if income > 0 else 0
            
            self.income_text = f'${income:.2f}'
            self.expenses_text = f'${expenses:.2f}'
            self.remaining_text = f'${remaining:.2f}'
            self.budget_used_text = f'{budget_used:.1f}%'
            self.budget_percentage = budget_used
    
    def update_transactions(self):
        transactions_list = self.ids.transactions_list
        transactions_list.clear_widgets()
        
        store = JsonStore('budget_data.json')
        if store.exists('transactions'):
            transactions = store.get('transactions')['data']
            
            for transaction in transactions[-5:]:  # Show last 5 transactions
                card = TransactionCard()
                card.description = transaction['description']
                card.amount_text = f"${transaction['amount']:.2f}"
                card.amount_color = '0.4, 0.8, 0.4, 1' if transaction['type'] == 'Income' else '0.9, 0.4, 0.4, 1'
                card.category = transaction['category']
                card.date = transaction['date']
                transactions_list.add_widget(card)
    
    def show_add_transaction(self):
        self.manager.current = 'add_transaction'

class AddTransactionScreen(Screen):
    def save_transaction(self):
        description = self.ids.description.text
        amount = self.ids.amount.text
        category = self.ids.category.text
        transaction_type = self.ids.transaction_type.text
        
        if description and amount and category != 'Select Category':
            try:
                amount = float(amount)
                
                # Save transaction
                store = JsonStore('budget_data.json')
                transactions = store.get('transactions')['data'] if store.exists('transactions') else []
                
                transaction = {
                    'description': description,
                    'amount': amount,
                    'category': category,
                    'type': transaction_type,
                    'date': datetime.now().strftime('%Y-%m-%d')
                }
                
                transactions.append(transaction)
                store.put('transactions', data=transactions)
                
                # Clear form
                self.ids.description.text = ''
                self.ids.amount.text = ''
                self.ids.category.text = 'Select Category'
                self.ids.transaction_type.text = 'Expense'
                
                # Go back to dashboard
                self.manager.current = 'dashboard'
                
            except ValueError:
                self.show_error('Please enter a valid amount')
        else:
            self.show_error('Please fill all fields')
    
    def cancel(self):
        self.manager.current = 'dashboard'
    
    def show_error(self, message):
        popup = Popup(title='Error', content=Label(text=message), size_hint=(None, None), size=(300, 200))
        popup.open()

class MLBudgetApp(App):
    def build(self):
        Builder.load_string(KV)
        
        # Create screen manager
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(AddTransactionScreen(name='add_transaction'))
        
        return sm

if __name__ == '__main__':
    MLBudgetApp().run() 