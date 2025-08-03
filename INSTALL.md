# Installation Guide - ML Budget App

This guide will help you install and set up the ML Budget App on your system.

## Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **Web browser** (Chrome, Firefox, Safari, Edge)

## Installation Steps

### Step 1: Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation by opening Command Prompt and typing: `python --version`

#### macOS
1. Install using Homebrew: `brew install python`
2. Or download from [python.org](https://www.python.org/downloads/)
3. Verify installation: `python3 --version`

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Step 2: Download the Application

1. Download or clone the ML Budget App files
2. Extract to a folder on your computer
3. Open Command Prompt/Terminal in that folder

### Step 3: Install Dependencies

#### Windows (Command Prompt)
```cmd
pip install -r requirements.txt
```

#### Windows (PowerShell)
```powershell
python -m pip install -r requirements.txt
```

#### macOS/Linux
```bash
pip3 install -r requirements.txt
```

### Step 4: Run the Application

#### Windows
```cmd
python app.py
```

#### macOS/Linux
```bash
python3 app.py
```

### Step 5: Access the Application

1. Open your web browser
2. Go to: `http://localhost:5000`
3. Register a new account
4. Start using the app!

## Quick Setup Scripts

### Windows Users
1. Double-click `setup.bat` or `setup.ps1`
2. Follow the prompts
3. Run `python app.py` to start

### macOS/Linux Users
```bash
chmod +x run.py
./run.py
```

## Troubleshooting

### Python Not Found
**Problem**: `python` command not recognized
**Solution**: 
- Reinstall Python and check "Add to PATH"
- Or use `python3` instead of `python`

### Dependencies Installation Failed
**Problem**: `pip install` fails
**Solution**:
- Update pip: `python -m pip install --upgrade pip`
- Try: `python -m pip install -r requirements.txt`

### Port Already in Use
**Problem**: Port 5000 is busy
**Solution**:
- Change port in `app.py` line: `app.run(debug=True, port=5001)`
- Or kill the process using port 5000

### Database Issues
**Problem**: App won't start or data lost
**Solution**:
- Delete `budget.db` file
- Restart the application

## Sample Data (Optional)

To test ML features with sample data:

1. Start the application
2. Register an account
3. Run: `python sample_data.py`
4. Check the dashboard for ML recommendations

## File Structure

```
my-debt-app/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── run.py             # Startup script
├── sample_data.py     # Sample data generator
├── setup.bat          # Windows setup script
├── setup.ps1          # PowerShell setup script
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── README.md          # Main documentation
├── INSTALL.md         # This file
└── budget.db          # Database (created automatically)
```

## System Requirements

### Minimum Requirements
- **RAM**: 2GB
- **Storage**: 100MB free space
- **OS**: Windows 10, macOS 10.14+, Ubuntu 18.04+

### Recommended Requirements
- **RAM**: 4GB+
- **Storage**: 500MB free space
- **OS**: Latest version of your operating system

## Security Notes

- The app stores data locally on your device
- No data is sent to external servers
- Use strong passwords for your account
- Keep your system updated

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Ensure Python 3.8+ is installed
3. Verify all dependencies are installed
4. Check the console for error messages
5. Try deleting `budget.db` and restarting

## Next Steps

After successful installation:

1. **Register an account** with your monthly income
2. **Add transactions** to build the ML model
3. **Set budgets** for different categories
4. **Monitor recommendations** as the AI learns
5. **Adjust spending** based on insights

---

**Happy budgeting! 🎯** 