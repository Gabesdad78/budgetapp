@echo off
echo ========================================
echo ML Budget App - Setup Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found! Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo Failed to install dependencies
    echo Please run: pip install -r requirements.txt manually
    pause
    exit /b 1
)

echo.
echo Dependencies installed successfully!
echo.
echo To start the application:
echo 1. Run: python app.py
echo 2. Open browser to: http://localhost:5000
echo 3. Register an account and start using the app
echo.
echo For sample data (optional):
echo Run: python sample_data.py
echo.
pause 