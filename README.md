# 🚀 Personalized Portfolio Analysis Multi-Agent System

A comprehensive AI-powered portfolio analysis system that provides personalized investment recommendations using the Kite Connect API and Google Gemini AI. The system employs multiple specialized AI agents to analyze your portfolio and generate tailored investment strategies based on your personal preferences, risk tolerance, and financial goals.

**Portfolio Demo Analysis**
- **Interactive Preference Collection**: Comprehensive questionnaire covering age, experience, goals, risk tolerance, sector preferences, and budget constraints
- **Dynamic Recommendations**: All suggestions tailored to your specific financial profile and preferences
- **Goal-Oriented Strategy**: Aligned with your investment objectives (wealth creation, income generation, retirement planning, etc.)

### 🤖 **Multi-Agent Architecture**
- **UserPreferenceAgent**: Collects and manages user investment preferences
- **PortfolioFetcherAgent**: Retrieves real-time portfolio data from Kite Connect API
- **DataAnalyzerAgent**: Performs comprehensive portfolio analysis using AI
- **SuggestionEngineAgent**: Generates personalized investment recommendations
- **ReportGeneratorAgent**: Creates detailed, professional investment reports

### 📊 **Comprehensive Analysis**
- **Real-time Data**: Live portfolio data from Zerodha Kite Connect API
- **AI-Powered Insights**: Advanced analysis using Google Gemini AI
- **Risk Assessment**: Detailed risk metrics and concentration analysis
- **Sector Analysis**: Portfolio allocation vs. your preferred sectors
- **Performance Attribution**: Detailed P&L analysis and performance tracking

### 📋 **Professional Reporting**
- **Detailed Reports**: Investment-grade analysis reports in Markdown format
- **Personalized Recommendations**: Budget-specific investment suggestions
- **Implementation Roadmap**: Step-by-step action plans with timelines
- **Risk Management**: Tailored risk controls based on your risk tolerance

## 🏗️ Project Structure

```
portfolio-analyzer/
├── 📁 agents/                          # AI Agent modules
│   ├── __init__.py                     # Package initialization
│   ├── preference_agent.py             # User preference collection agent
│   ├── fetcher_agent.py               # Portfolio data fetching agent
│   ├── analyzer_agent.py              # Portfolio analysis agent
│   ├── suggestion_agent.py            # Investment suggestion agent
│   └── report_agent.py                # Report generation agent
├── 📁 config/                          # Configuration management
│   └── settings.py                     # Environment and settings configuration
├── 📁 kite_api/                        # Kite Connect API integration
│   └── connector.py                    # Kite API connector and utilities
├── 📁 utils/                           # Utility modules
│   ├── __init__.py                     # Package initialization
│   └── api_handler.py                  # Rate-limited Gemini API handler
├── 📁 reports/                         # Generated portfolio reports
│   └── (auto-generated .md files)     # Timestamped analysis reports
├── 📁 user_preferences/                # Saved user preferences
│   └── (auto-generated .json files)   # User preference data
├── 📄 main.py                          # Main orchestrator and entry point
├── 📄 Makefile                         # Automation and setup commands
├── 📄 requirements.txt                 # Python dependencies
├── 📄 .env.example                     # Environment variables template
├── 📄 .env                            # Your environment variables (create this)
├── 📄 .gitignore                      # Git ignore patterns
└── 📄 README.md                        # This file
```

## 🚀 Quick Start

### 1. **Prerequisites**

- **Python 3.8+** installed on your system
- **Zerodha Kite Connect API** credentials ([Get them here](https://developers.kite.trade/))
- **Google Gemini API** key ([Get it here](https://aistudio.google.com/))
- **Active Zerodha trading account** with portfolio data

### 2. **Clone and Setup**

```bash
# Clone the repository
git clone  portfolio-analyzer
cd portfolio-analyzer

# Complete project setup (creates venv, installs dependencies, creates directories)
make dev-setup
```

### 3. **Configure Environment**

```bash
# Copy the environment template
cp .env.example .env

# Edit .env file with your credentials
nano .env  # or use your preferred editor
```

**Required Environment Variables:**
```bash
# Kite Connect API Credentials
KITE_API_KEY=your_api_key_here
KITE_API_SECRET=your_api_secret_here
KITE_ACCESS_TOKEN=your_access_token_here

# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: User Preferences (will be collected interactively)
INVESTMENT_PROFILE=moderate_risk_long_term
REPORT_FORMAT=markdown
```

### 4. **First-Time Authentication** (If needed)

```bash
# If you need to set up Kite API authentication
python utils/auth.py
```

### 5. **Test Your Setup**

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Test Kite API connection
make test-connection

# Check if all configurations are correct
make check-env
```

### 6. **Run Complete Analysis**

```bash
# Run the full personalized portfolio analysis
make run
```

## 🎮 Available Commands

### **Setup & Installation**
```bash
make help                    # Show all available commands
make setup                   # Create virtual environment and install dependencies
make dev-setup              # Complete development setup with .env template
make install                # Install/update dependencies only
make clean                  # Remove virtual environment and cache files
```

### **Testing & Validation**
```bash
make test-connection        # Test Kite API connection
make check-env             # Validate environment variables
make run                   # Run complete portfolio analysis
```

### **Preference Management**
```bash
make collect-preferences   # Collect user preferences only
make show-preferences     # Display current saved preferences
```

### **Development & Maintenance**
```bash
make lint                 # Run code linting (flake8)
make format              # Format code with black
make freeze              # Update requirements.txt from current environment
```

### **System Information**
```bash
make install-system-deps  # Install system dependencies (Ubuntu/Debian)
```

## 💡 How It Works

### **Step 1: Preference Collection** 🎯
The system starts by collecting your investment preferences through an interactive questionnaire:

- **Personal Info**: Age, experience level, income range
- **Investment Goals**: Primary objectives, time horizon, expected returns
- **Risk Profile**: Risk tolerance, maximum acceptable drawdown
- **Portfolio Preferences**: Equity allocation, sector preferences, number of holdings
- **Constraints**: Budget, liquidity needs, sector restrictions

### **Step 2: Portfolio Data Fetching** 📊
- Connects to Zerodha Kite Connect API
- Retrieves real-time portfolio holdings, positions, and account information
- Validates and processes the data for analysis

### **Step 3: AI-Powered Analysis** 🤖
- Uses Google Gemini AI to analyze portfolio data
- Calculates risk metrics, concentration analysis, and performance attribution
- Identifies gaps between current portfolio and your preferences

### **Step 4: Personalized Recommendations** 🎪
- Generates investment suggestions tailored to your specific profile
- Considers your budget, sector preferences, and risk tolerance
- Creates implementation strategies with specific timelines

### **Step 5: Professional Reporting** 📋
- Compiles comprehensive analysis into professional Markdown reports
- Includes executive summaries, detailed recommendations, and action plans
- Saves timestamped reports for historical tracking

## 🔧 Configuration Options

### **Investment Profiles**
The system supports various investment profiles:
- `conservative_income_focused`: Low risk, income generation
- `moderate_risk_long_term`: Balanced growth and risk
- `aggressive_growth_young`: High risk, maximum growth
- `retirement_planning`: Long-term wealth building
- `custom`: Fully customized based on your preferences

### **Report Formats**
- `markdown`: Detailed Markdown reports (default)
- `pdf`: PDF generation (future enhancement)
- `html`: Web-friendly reports (future enhancement)

### **API Configuration**
- **Rate Limiting**: Automatic rate limiting for both Kite and Gemini APIs
- **Error Handling**: Robust error handling with graceful fallbacks
- **Retry Logic**: Automatic retry mechanisms for API failures

## 📊 Sample Output

### **Terminal Output**
```
🚀 Portfolio Analysis Multi-Agent System

🎯 Step 1: Collecting Your Investment Preferences
✅ User preferences collected successfully!

⠋ Fetching portfolio data...
✅ Portfolio data fetched: 5 holdings, 2 positions

⠋ Analyzing portfolio data...
        Portfolio Summary        
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Metric           ┃ Value      ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ Total Investment │ ₹2,50,000  │
│ Current Value    │ ₹2,85,750  │
│ Total P&L        │ ₹35,750    │
│ P&L %            │ +14.30%    │
└──────────────────┴────────────┘

⠋ Generating personalized suggestions...
⠋ Generating personalized report...

🎉 Personalized Success
📊 Analysis Complete!

🎯 Tailored for your goal: Regular Income Generation
📋 Report saved as: personalized_portfolio_analysis_20250720_143022.md
📂 Location: reports/personalized_portfolio_analysis_20250720_143022.md

🎯 Portfolio analysis completed successfully!
```

### **Generated Report Structure**
```markdown
# Comprehensive Personalized Portfolio Analysis Report

## 👤 Your Investment Profile
- Age: 25 years | Experience: Intermediate
- Goal: Wealth Creation | Risk: Aggressive
- Budget: ₹1,00,000 additional + ₹15,000 monthly SIP

## 📊 Current Portfolio Analysis
- Portfolio snapshot with P&L analysis
- Goal alignment assessment
- Risk concentration analysis

## 🎯 Personalized Strategic Recommendations
- Investment suggestions based on your preferred sectors
- Budget-specific allocation strategies
- Implementation timeline and action steps

## 💰 Personalized Investment Strategy
- Specific stock recommendations with rationale
- Risk management framework
- Expected timelines and success metrics
```

## 🔐 Security & Privacy

### **API Security**
- **Environment Variables**: All sensitive credentials stored in `.env` file
- **Rate Limiting**: Automatic API rate limiting to prevent quota exhaustion
- **Error Handling**: Secure error messages without credential exposure

### **Data Privacy**
- **Local Storage**: All preferences and reports stored locally
- **No Cloud Storage**: Your financial data never leaves your machine
- **Secure APIs**: Uses official APIs with proper authentication

### **Best Practices**
- Never commit `.env` file to version control
- Regularly rotate API keys
- Keep access tokens updated
- Monitor API usage and quotas

## 🚨 Troubleshooting

### **Common Issues**

#### **1. API Connection Failures**
```bash
# Test your Kite API connection
make test-connection

# Common fixes:
# - Verify API credentials in .env file
# - Check if access token is expired
# - Ensure market hours for live data
```

#### **2. Gemini API Rate Limits**
```bash
# The system handles rate limiting automatically
# If you hit limits frequently:
# - Reduce analysis frequency
# - Consider upgrading to Gemini Pro
# - Check your API quota usage
```

#### **3. Environment Setup Issues**
```bash
# Clean setup
make clean
make dev-setup

# Verify Python version
python --version  # Should be 3.8+

# Check virtual environment
source venv/bin/activate
python -c "import sys; print(sys.prefix)"
```

#### **4. Missing Dependencies**
```bash
# Reinstall all dependencies
make install

# For system-level dependencies (Ubuntu/Debian):
make install-system-deps
```

### **Error Codes**

| Error | Description | Solution |
|-------|-------------|----------|
| `Config validation failed` | Missing environment variables | Check `.env` file configuration |
| `Kite API connection failed` | API credentials or network issue | Verify credentials and connection |
| `Portfolio analysis failed` | AI API issue or data parsing error | Check Gemini API quota and key |
| `Report generation failed` | File system or formatting issue | Check directory permissions |

## 🤝 Contributing

### **Development Setup**
```bash
# Clone and set up development environment
git clone 
cd portfolio-analyzer
make dev-setup

# Install development dependencies
pip install -r requirements-dev.txt

# Run code quality checks
make lint
make format
```

### **Code Structure Guidelines**
- **Agent Pattern**: Each agent should have a single responsibility
- **Error Handling**: Comprehensive error handling with graceful fallbacks
- **Documentation**: Clear docstrings and type hints
- **Testing**: Unit tests for core functionality

### **Adding New Features**
1. **New Agents**: Create new agent classes following existing patterns
2. **API Integrations**: Add new API connectors in dedicated modules
3. **Report Formats**: Extend report generation with new output formats
4. **Preference Types**: Add new user preference categories

## 🚀 Future Enhancements

### **Planned Features**
- [ ] **PDF Report Generation**: Professional PDF reports with charts
- [ ] **Portfolio Backtesting**: Historical performance analysis
- [ ] **Real-time Alerts**: Notifications for portfolio changes
- [ ] **Web Dashboard**: Browser-based portfolio monitoring
- [ ] **Mobile App**: React Native mobile application
- [ ] **Advanced Analytics**: Machine learning-based predictions

### **API Integrations**
- [ ] **NSE/BSE Data**: Direct market data integration
- [ ] **Mutual Fund APIs**: MF portfolio analysis
- [ ] **International Markets**: Global portfolio support
- [ ] **Crypto Integration**: Cryptocurrency portfolio analysis

### **AI Enhancements**
- [ ] **GPT-4 Integration**: Alternative AI models for analysis
- [ ] **Custom Models**: Fine-tuned models for Indian markets
- [ ] **Sentiment Analysis**: News and social sentiment integration
- [ ] **Technical Analysis**: Advanced chart pattern recognition

## ⚠️ Disclaimer

**Important Notice:**

This software is designed for educational and informational purposes. It provides portfolio analysis and investment suggestions based on AI algorithms and market data.

### **Investment Risks**
- **Market Risk**: All investments carry market risk and potential for loss
- **AI Limitations**: AI recommendations are not guaranteed to be accurate
- **Personal Responsibility**: Always consult qualified financial advisors
- **No Guarantees**: Past performance doesn't indicate future results

### **Usage Responsibility**
- Verify all recommendations with independent research
- Consider your personal financial situation
- Understand the risks associated with your investments
- Keep your API credentials secure and private

### **Compliance**
- Ensure compliance with local financial regulations
- Understand tax implications of your investments
- Follow proper KYC and investment guidelines
- Maintain appropriate documentation for your investments

### **Contact**
- *Email*:  devanshvarshney.ai@gmail.com
- *LinkedIn*:  https://www.linkedin.com/in/devansh-varshney-3911a027a/

*Empowering retail investors with professional-grade portfolio analysis tools*
