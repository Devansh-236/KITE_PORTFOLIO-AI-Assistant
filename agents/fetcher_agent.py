# agents/fetcher_agent.py
import logging
from typing import Dict, Any
from kite_api.connector import kite_connector
import time

logger = logging.getLogger(__name__)

class PortfolioFetcherAgent:
    """Enhanced agent for fetching comprehensive portfolio data from Kite API"""
    
    def __init__(self, name: str = "PortfolioFetcherAgent"):
        self.name = name
        self.connector = kite_connector
    
    def execute(self) -> Dict[str, Any]:
        """Fetch comprehensive portfolio data with enhanced error handling"""
        logger.info(f"{self.name}: Starting comprehensive portfolio data fetch...")
        
        try:
            # Fetch all required data with retry mechanism
            data_sources = {
                'profile': self._fetch_with_retry(self.connector.get_profile),
                'holdings': self._fetch_with_retry(self.connector.get_holdings),
                'positions': self._fetch_with_retry(self.connector.get_positions),
                'margins': self._fetch_with_retry(self.connector.get_margins)
            }
            
            # Validate critical data
            if not data_sources['holdings']:
                logger.warning("No holdings data retrieved")
            
            # Compile comprehensive portfolio data
            portfolio_data = {
                **data_sources,
                'timestamp': self._get_timestamp(),
                'data_quality': self._assess_data_quality(data_sources),
                'status': 'success'
            }
            
            logger.info(f"{self.name}: Successfully fetched portfolio data")
            logger.info(f"Holdings: {len(data_sources['holdings'])}, "
                       f"Net Positions: {len(data_sources['positions'].get('net', []))}")
            
            return portfolio_data
            
        except Exception as e:
            logger.error(f"{self.name}: Error fetching portfolio data: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
    
    def _fetch_with_retry(self, fetch_function, max_retries: int = 3) -> Any:
        """Fetch data with retry mechanism"""
        for attempt in range(max_retries):
            try:
                return fetch_function()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                logger.warning(f"Fetch attempt {attempt + 1} failed: {e}")
                time.sleep(1)  # Wait before retry
        return {}
    
    def _assess_data_quality(self, data_sources: Dict) -> Dict[str, str]:
        """Assess quality of fetched data"""
        quality = {}
        
        # Check holdings data
        holdings = data_sources.get('holdings', [])
        quality['holdings'] = 'Good' if len(holdings) > 0 else 'Poor'
        
        # Check positions data
        positions = data_sources.get('positions', {})
        quality['positions'] = 'Good' if positions.get('net') else 'Poor'
        
        # Check profile data
        profile = data_sources.get('profile', {})
        quality['profile'] = 'Good' if profile.get('user_name') else 'Poor'
        
        # Check margins data
        margins = data_sources.get('margins', {})
        quality['margins'] = 'Good' if margins.get('equity') else 'Poor'
        
        return quality
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
