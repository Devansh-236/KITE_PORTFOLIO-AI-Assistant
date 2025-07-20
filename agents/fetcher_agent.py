import logging
from typing import Dict, Any
from kite_api.connector import kite_connector

logger = logging.getLogger(__name__)

class PortfolioFetcherAgent:
    """Agent responsible for fetching portfolio data from Kite API"""
    
    def __init__(self, name: str = "PortfolioFetcherAgent"):
        self.name = name
        self.connector = kite_connector
    
    def execute(self) -> Dict[str, Any]:
        """Fetch complete portfolio data"""
        logger.info(f"{self.name}: Starting portfolio data fetch...")
        
        try:
            # Fetch all required data
            profile = self.connector.get_profile()
            holdings = self.connector.get_holdings()
            positions = self.connector.get_positions()
            margins = self.connector.get_margins()
            
            # Compile portfolio data
            portfolio_data = {
                'profile': profile,
                'holdings': holdings,
                'positions': positions,
                'margins': margins,
                'timestamp': self._get_timestamp(),
                'status': 'success'
            }
            
            logger.info(f"{self.name}: Successfully fetched portfolio data")
            logger.info(f"Holdings: {len(holdings)}, Net Positions: {len(positions.get('net', []))}")
            
            return portfolio_data
            
        except Exception as e:
            logger.error(f"{self.name}: Error fetching portfolio data: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
