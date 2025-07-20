import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Kite API Configuration
    KITE_API_KEY = os.getenv('KITE_API_KEY')
    KITE_API_SECRET = os.getenv('KITE_API_SECRET')  
    KITE_ACCESS_TOKEN = os.getenv('KITE_ACCESS_TOKEN')
    
    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # User Preferences
    INVESTMENT_PROFILE = os.getenv('INVESTMENT_PROFILE', 'moderate_risk_long_term')
    REPORT_FORMAT = os.getenv('REPORT_FORMAT', 'markdown')
    
    # Validation
    REQUIRED_VARS = [
        'KITE_API_KEY', 'KITE_API_SECRET', 
        'KITE_ACCESS_TOKEN', 'GEMINI_API_KEY'
    ]

def check_config():
    """Validate that all required environment variables are set"""
    missing = []
    config = Config()
    
    for var in Config.REQUIRED_VARS:
        if not getattr(config, var):
            missing.append(var)
    
    if missing:
        raise ValueError(f"Missing required environment variables: {missing}")
    
    print("✅ All required environment variables are configured!")
    return True
