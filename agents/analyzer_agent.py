import logging
import json
import google.generativeai as genai
from typing import Dict, Any
from config.settings import Config

logger = logging.getLogger(__name__)

class DataAnalyzerAgent:
    """Agent for analyzing portfolio data using Gemini AI"""
    
    def __init__(self, name: str = "DataAnalyzerAgent"):
        self.name = name
        self.config = Config()
        
        # Initialize Gemini
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def execute(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze portfolio data and generate insights"""
        logger.info(f"{self.name}: Starting portfolio analysis...")
        
        if portfolio_data.get('status') != 'success':
            return {
                'status': 'error',
                'error': 'Invalid portfolio data provided'
            }
        
        try:
            # Extract key data for analysis
            holdings = portfolio_data.get('holdings', [])
            positions = portfolio_data.get('positions', {}).get('net', [])
            profile = portfolio_data.get('profile', {})
            
            # Create analysis prompt
            prompt = self._create_analysis_prompt(holdings, positions, profile)
            
            # Generate analysis using Gemini
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            # Parse the structured analysis
            analysis_result = self._parse_analysis(analysis_text)
            
            logger.info(f"{self.name}: Analysis completed successfully")
            
            return {
                'status': 'success',
                'analysis': analysis_result,
                'raw_analysis': analysis_text,
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"{self.name}: Analysis error: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
    
    def _create_analysis_prompt(self, holdings: list, positions: list, profile: dict) -> str:
        """Create comprehensive analysis prompt"""
        return f"""
        As a professional financial analyst, analyze the following portfolio data and provide a comprehensive analysis.
        
        PORTFOLIO HOLDINGS:
        {json.dumps(holdings, indent=2)}
        
        CURRENT POSITIONS:
        {json.dumps(positions, indent=2)}
        
        USER PROFILE:
        {json.dumps(profile, indent=2)}
        
        Please provide a detailed analysis in the following JSON structure:
        {{
            "summary": {{
                "total_investment": <float>,
                "current_value": <float>,
                "total_pnl": <float>,
                "total_pnl_percentage": <float>,
                "number_of_holdings": <int>
            }},
            "sector_allocation": [
                {{"sector": "Technology", "percentage": 25.5, "value": 50000}},
                ...
            ],
            "top_performers": [
                {{"symbol": "INFY", "pnl_percentage": 15.2, "pnl": 5000}},
                ...
            ],
            "bottom_performers": [
                {{"symbol": "XYZ", "pnl_percentage": -8.1, "pnl": -2000}},
                ...
            ],
            "risk_metrics": {{
                "diversification_score": <float 0-10>,
                "concentration_risk": "Low/Medium/High",
                "sector_concentration": <top_sector_percentage>
            }},
            "key_insights": [
                "Your portfolio shows strong diversification across sectors",
                "Technology sector is overweight at 35% of portfolio",
                ...
            ]
        }}
        
        Ensure all calculations are accurate based on the provided data. If any field cannot be calculated, use null.
        """
    
    def _parse_analysis(self, analysis_text: str) -> Dict:
        """Parse and validate analysis response"""
        try:
            # Try to extract JSON from the response
            json_start = analysis_text.find('{')
            json_end = analysis_text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = analysis_text[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback: return raw text with basic structure
                return {
                    'summary': {'error': 'Could not parse structured analysis'},
                    'raw_analysis': analysis_text
                }
                
        except json.JSONDecodeError:
            return {
                'summary': {'error': 'Invalid JSON in analysis'},
                'raw_analysis': analysis_text
            }
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()
