from kiteconnect import KiteConnect
import logging
from config.settings import Config
from typing import Dict, List, Optional
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KiteAPIConnector:
    """Direct Kite Connect API connector replacing MCP server approach"""
    
    def __init__(self):
        self.config = Config()
        self.kite = KiteConnect(api_key=self.config.KITE_API_KEY)
        
        # Set access token if available
        if self.config.KITE_ACCESS_TOKEN:
            self.kite.set_access_token(self.config.KITE_ACCESS_TOKEN)
        else:
            logger.warning("No access token found. Login flow required.")
    
    def get_login_url(self) -> str:
        """Get login URL for authentication"""
        return self.kite.login_url()
    
    def generate_session(self, request_token: str) -> Dict:
        """Generate session using request token"""
        try:
            data = self.kite.generate_session(request_token, self.config.KITE_API_SECRET)
            logger.info("Session generated successfully")
            return data
        except Exception as e:
            logger.error(f"Session generation failed: {e}")
            raise
    
    def get_profile(self) -> Dict:
        """Get user profile information"""
        try:
            return self.kite.profile()
        except Exception as e:
            logger.error(f"Error fetching profile: {e}")
            return {}
    
    def get_holdings(self) -> List[Dict]:
        """Fetch portfolio holdings"""
        try:
            holdings = self.kite.holdings()
            logger.info(f"Retrieved {len(holdings)} holdings")
            return holdings
        except Exception as e:
            logger.error(f"Error fetching holdings: {e}")
            return []
    
    def get_positions(self) -> Dict:
        """Fetch current positions"""
        try:
            positions = self.kite.positions()
            logger.info("Retrieved positions data")
            return positions
        except Exception as e:
            logger.error(f"Error fetching positions: {e}")
            return {'net': [], 'day': []}
    
    def get_margins(self) -> Dict:
        """Fetch account margins"""
        try:
            return self.kite.margins()
        except Exception as e:
            logger.error(f"Error fetching margins: {e}")
            return {}
    
    def get_instruments(self, exchange: str = "NSE") -> List[Dict]:
        """Fetch instruments list"""
        try:
            return self.kite.instruments(exchange)
        except Exception as e:
            logger.error(f"Error fetching instruments: {e}")
            return []
    
    def get_quote(self, instruments: List[str]) -> Dict:
        """Get live quotes for instruments"""
        try:
            return self.kite.quote(instruments)
        except Exception as e:
            logger.error(f"Error fetching quotes: {e}")
            return {}

def test_connection():
    """Test Kite API connection"""
    try:
        connector = KiteAPIConnector()
        profile = connector.get_profile()
        if profile:
            print(f"✅ Connected successfully! User: {profile.get('user_name', 'Unknown')}")
            return True
        else:
            print("❌ Connection failed - check your credentials")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

# Singleton instance
kite_connector = KiteAPIConnector()
