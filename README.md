# 💰 ML Budget App

A powerful machine learning budget management application that helps you control spending, allocate funds, and predict future expenses using AI.

![ML Budget App](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--learn-orange.svg)
![Deploy](https://img.shields.io/badge/Deploy-Vercel-purple.svg)

## 🚀 Live Demo

**[Deployed on Vercel](https://your-app-name.vercel.app)** *(Replace with your actual Vercel URL)*

## ✨ Features

### 💡 Core Features
- **Budget Management**: Set and track monthly budgets by category
- **Transaction Tracking**: Record income and expenses with detailed categorization
- **User Authentication**: Secure registration and login system
- **Real-time Analytics**: Interactive charts and spending insights

### 🤖 Machine Learning Features
- **Spending Predictions**: AI-powered forecasting of future expenses
- **Budget Recommendations**: Smart suggestions based on spending patterns
- **Pattern Analysis**: Identify spending trends and anomalies
- **Category Insights**: Understand your spending behavior

### 📊 Analytics & Visualization
- **Interactive Charts**: Doughnut charts for category breakdown
- **Monthly Trends**: Line charts showing spending over time
- **Budget Progress**: Visual progress bars for budget tracking
- **Real-time Updates**: Instant data visualization

### 📱 Multi-Platform Access
- **Web App**: Responsive design works on any device
- **Mobile Web**: Optimized for smartphone browsers
- **Desktop App**: Native-like experience on desktop

## 🛠️ Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (local), PostgreSQL (production)
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Charts**: Chart.js
- **Deployment**: Vercel

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ml-budget-app.git
   cd ml-budget-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the app**
   - Open your browser to `http://localhost:5000`
   - Register a new account and start managing your budget!

### Vercel Deployment

1. **Fork this repository** to your GitHub account

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign up/Login with GitHub
   - Click "New Project"
   - Import your forked repository

3. **Deploy**
   - Vercel will automatically detect the Flask app
   - Click "Deploy"
   - Your app will be live in minutes!

## 📱 Mobile Access

### Option 1: Direct Browser Access
- Open your phone's browser
- Go to your Vercel URL
- The app is fully responsive and mobile-optimized

### Option 2: Mobile Web Wrapper
- Copy `mobile_web_wrapper.html` to your phone
- Open it in your browser
- It will connect to your deployed app

## 🎯 Key Features Explained

### Budget Management
- Set monthly budgets for different categories (Food, Transport, Entertainment, etc.)
- Track spending against budgets in real-time
- Visual progress bars show budget utilization

### Transaction Tracking
- Add income and expenses with detailed descriptions
- Categorize transactions for better organization
- Search and filter transaction history

### Machine Learning Insights
- **Spending Predictions**: AI analyzes your spending patterns to predict future expenses
- **Budget Recommendations**: Get smart suggestions for budget allocation
- **Pattern Recognition**: Identify unusual spending patterns

### Interactive Analytics
- **Category Breakdown**: See where your money goes with interactive charts
- **Monthly Trends**: Track spending patterns over time
- **Budget vs Actual**: Compare planned vs actual spending

## ��️ Project Structure

```
ml-budget-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
├── runtime.txt           # Python runtime version
├── templates/            # HTML templates
│   ├── base.html        # Base template with styling
│   ├── index.html       # Landing page
│   ├── dashboard.html   # Main dashboard
│   ├── login.html       # Login page
│   └── register.html    # Registration page
├── static/              # Static files (CSS, JS, images)
├── mobile_web_wrapper.html  # Mobile web wrapper
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for local development:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///budget.db
```

### Database
The app uses SQLite for local development and automatically switches to PostgreSQL on Vercel.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask community for the excellent web framework
- Scikit-learn for machine learning capabilities
- Bootstrap for responsive design
- Chart.js for beautiful visualizations
- Vercel for seamless deployment

## 📞 Support

If you have any questions or need help:
- Open an issue on GitHub
- Check the [documentation](docs/)
- Contact: your-email@example.com

---

**Made with ❤️ for better financial management** 