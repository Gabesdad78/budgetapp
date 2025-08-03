#!/usr/bin/env python3
"""
Simple ML Budget App Starter
This script starts the web app cleanly without freezing
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_header():
    print("=" * 50)
    print("ML Budget App - Simple Starter")
    print("=" * 50)

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'pandas', 'numpy', 'scikit-learn', 
        'flask-sqlalchemy', 'flask-login', 'werkzeug'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        for package in missing_packages:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         capture_output=True)
    
    return len(missing_packages) == 0

def start_web_app():
    """Start the Flask web app"""
    print("\n🚀 Starting ML Budget App...")
    print("📱 Web App will be available at: http://localhost:5000")
    print("📱 Mobile App will be available as desktop app")
    print("\n⏳ Starting in 3 seconds...")
    
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🎉 Starting applications...")
    
    # Start web app in background
    web_process = subprocess.Popen([sys.executable, 'app.py'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
    
    # Wait a moment for web app to start
    time.sleep(3)
    
    # Try to open browser
    try:
        webbrowser.open('http://localhost:5000')
        print("✅ Opened web app in browser")
    except:
        print("📱 Please open: http://localhost:5000")
    
    print("\n📋 Available Options:")
    print("1. 🌐 Web App: http://localhost:5000 (Recommended)")
    print("2. 🖥️  Desktop Mobile: python mobile_app.py")
    print("3. 📱 Mobile on Phone: Use browser on your phone")
    print("4. 🛑 Stop: Press Ctrl+C")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping applications...")
        web_process.terminate()
        print("✅ Applications stopped")

def main():
    """Main function"""
    print_header()
    
    if check_dependencies():
        print("\n✅ All dependencies are ready!")
        start_web_app()
    else:
        print("\n❌ Some dependencies failed to install")
        print("💡 Try running: python -m pip install --upgrade pip")

if __name__ == "__main__":
    main() 