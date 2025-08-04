"""
WSGI entry point for Vercel deployment
"""
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app
from api.app import app

# For Vercel deployment
if __name__ == "__main__":
    app.run() 