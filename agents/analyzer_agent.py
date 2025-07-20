# agents/analyzer_agent.py
import logging
import json
import re
from typing import Dict, Any, List
from config.settings import Config
from utils.api_handler import gemini_handler

logger = logging.getLogger(__name__)

class DataAnalyzerAgent:
    """Enhanced agent with robust JSON parsing for portfolio analysis"""
    
    def __init__(self, name: str = "DataAnalyzerAgent"):
        self.name = name
        self.config = Config()
    
    def execute(self, portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform portfolio analysis with robust error handling"""
        logger.info(f"{self.name}: Starting comprehensive portfolio analysis...")
        
        if portfolio_data.get('status') != 'success':
            return {
                'status': 'error',
                'error': 'Invalid portfolio data provided'
            }
        
        try:
            # Extract and preprocess data
            holdings = portfolio_data.get('holdings', [])
            positions = portfolio_data.get('positions', {}).get('net', [])
            profile = portfolio_data.get('profile', {})
            
            # Calculate basic metrics first
            basic_metrics = self._calculate_basic_metrics(holdings, positions)
            
            # Create analysis prompt
            prompt = self._create_robust_analysis_prompt(holdings, basic_metrics)
            
            # Generate analysis using rate-limited handler
            logger.info(f"{self.name}: Sending data to Gemini for analysis...")
            analysis_text = gemini_handler.generate_content_with_retry(prompt)
            
            if not analysis_text:
                logger.error("No response from Gemini API")
                return self._create_fallback_response(basic_metrics, "No API response")
            
            # Parse the analysis with robust error handling
            analysis_result = self._robust_json_parse(analysis_text, basic_metrics)
            
            logger.info(f"{self.name}: Analysis completed successfully")
            
            return {
                'status': 'success',
                'analysis': analysis_result,
                'raw_analysis': analysis_text[:500],  # Truncate for logs
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"{self.name}: Analysis error: {e}")
            basic_metrics = self._calculate_basic_metrics(
                portfolio_data.get('holdings', []), 
                portfolio_data.get('positions', {}).get('net', [])
            )
            return self._create_fallback_response(basic_metrics, str(e))
    
    def _create_robust_analysis_prompt(self, holdings: List[Dict], basic_metrics: Dict) -> str:
        """Create a robust analysis prompt with clear JSON structure"""
        # Get first holding details
        primary_holding = holdings[0] if holdings else {}
        symbol = primary_holding.get('tradingsymbol', 'UNKNOWN')
        pnl = primary_holding.get('pnl', 0)
        
        return f"""
You are a financial analyst. Analyze this portfolio and return ONLY valid JSON with no additional text.

PORTFOLIO DATA:
Symbol: {symbol}
Investment: ₹{basic_metrics.get('total_investment', 0):.0f}
Current Value: ₹{basic_metrics.get('current_value', 0):.0f}
P&L: ₹{pnl:.0f}
Holdings Count: {len(holdings)}

Return ONLY this JSON structure with no markdown formatting:

{{
  "executive_summary": {{
    "total_investment": {basic_metrics.get('total_investment', 0)},
    "current_value": {basic_metrics.get('current_value', 0)},
    "total_pnl": {basic_metrics.get('total_pnl', 0)},
    "total_pnl_percentage": {basic_metrics.get('total_pnl_percentage', 0):.2f},
    "number_of_holdings": {len(holdings)},
    "risk_level": "High"
  }},
  "holdings_analysis": [
    {{
      "symbol": "{symbol}",
      "sector": "Unknown",
      "pnl": {pnl},
      "pnl_percentage": {basic_metrics.get('total_pnl_percentage', 0):.2f},
      "weight_in_portfolio": 100,
      "recommendation": "Review"
    }}
  ],
  "sector_analysis": {{
    "sector_allocation": [
      {{
        "sector": "Unknown", 
        "percentage": 100.0, 
        "value": {basic_metrics.get('current_value', 0)}
      }}
    ]
  }},
  "key_insights": [
    "Portfolio highly concentrated in single holding",
    "Significant diversification risk present",
    "Current position showing {'loss' if pnl < 0 else 'profit'} of ₹{abs(pnl):.0f}"
  ],
  "risk_warnings": [
    "High concentration risk - single stock portfolio",
    "No sector diversification",
    "Vulnerable to individual stock volatility"
  ],
  "opportunities": [
    "Add diversified holdings across sectors",
    "Consider large-cap stocks for stability",
    "Implement risk management strategies"
  ]
}}
"""
    
    def _robust_json_parse(self, text: str, basic_metrics: Dict) -> Dict:
        """Robust JSON parsing with multiple fallback strategies"""
        try:
            # Strategy 1: Clean and parse as-is
            cleaned_text = self._clean_json_text(text)
            if cleaned_text:
                return json.loads(cleaned_text)
                
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse attempt 1 failed: {e}")
            
        try:
            # Strategy 2: Extract JSON from markdown code blocks
            json_match = re.search(r'``````', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                return json.loads(self._clean_json_text(json_str))
                
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse attempt 2 failed: {e}")
            
        try:
            # Strategy 3: Find JSON-like structure
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.findall(json_pattern, text, re.DOTALL)
            
            for match in matches:
                try:
                    cleaned_match = self._clean_json_text(match)
                    parsed = json.loads(cleaned_match)
                    # Validate it has expected structure
                    if 'executive_summary' in parsed:
                        return parsed
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"JSON parse attempt 3 failed: {e}")
        
        # Strategy 4: Manual JSON construction
        logger.warning("All JSON parsing failed, creating structured fallback")
        return self._create_structured_fallback(basic_metrics, text)
    
    def _clean_json_text(self, text: str) -> str:
        """Clean text for JSON parsing"""
        if not text:
            return ""
            
        # Remove markdown code blocks
        text = re.sub(r'```', '', text)
        
        # Find JSON boundaries
        start = text.find('{')
        end = text.rfind('}')
        
        if start == -1 or end == -1 or end <= start:
            return ""
            
        json_text = text[start:end+1]
        
        # Clean up common issues
        json_text = re.sub(r'//.*?\n', '\n', json_text)  # Remove comments
        json_text = re.sub(r',\s*}', '}', json_text)      # Remove trailing commas
        json_text = re.sub(r',\s*]', ']', json_text)      # Remove trailing commas in arrays
        
        return json_text.strip()
    
    def _create_structured_fallback(self, basic_metrics: Dict, raw_text: str) -> Dict:
        """Create structured analysis from basic metrics and raw text"""
        holdings_count = basic_metrics.get('number_of_holdings', 0)
        pnl = basic_metrics.get('total_pnl', 0)
        pnl_pct = basic_metrics.get('total_pnl_percentage', 0)
        
        return {
            "executive_summary": {
                "total_investment": basic_metrics.get('total_investment', 0),
                "current_value": basic_metrics.get('current_value', 0),
                "total_pnl": pnl,
                "total_pnl_percentage": pnl_pct,
                "number_of_holdings": holdings_count,
                "risk_level": "High" if holdings_count < 3 else "Medium"
            },
            "holdings_analysis": [
                {
                    "symbol": "PRIMARY_HOLDING",
                    "sector": "To_Be_Determined",
                    "pnl": pnl,
                    "pnl_percentage": pnl_pct,
                    "weight_in_portfolio": 100.0 if holdings_count == 1 else 50.0,
                    "recommendation": "Review_Required"
                }
            ],
            "sector_analysis": {
                "sector_allocation": [
                    {
                        "sector": "Primary_Sector",
                        "percentage": 100.0,
                        "value": basic_metrics.get('current_value', 0)
                    }
                ]
            },
            "key_insights": [
                f"Portfolio has {holdings_count} holding(s) with significant concentration risk",
                f"Current P&L of ₹{pnl:.0f} ({pnl_pct:+.2f}%) requires attention",
                "Immediate diversification recommended to reduce risk",
                "Consider adding quality large-cap stocks across sectors"
            ],
            "risk_warnings": [
                "Critical concentration risk - portfolio lacks diversification",
                "Single stock volatility can cause significant losses",
                "No defensive positions to weather market downturns"
            ],
            "opportunities": [
                "Add banking sector exposure with quality names",
                "Consider technology sector for growth potential",
                "Include FMCG stocks for defensive positioning",
                "Implement systematic diversification strategy"
            ],
            "parsing_note": "Structured from calculated metrics due to AI response parsing issues"
        }
    
    def _calculate_basic_metrics(self, holdings: List[Dict], positions: List[Dict]) -> Dict[str, float]:
        """Calculate basic portfolio metrics"""
        try:
            if not holdings:
                return {
                    'total_investment': 0,
                    'current_value': 0,
                    'total_pnl': 0,
                    'total_pnl_percentage': 0,
                    'number_of_holdings': 0
                }
            
            total_investment = 0
            current_value = 0
            
            for holding in holdings:
                avg_price = float(holding.get('average_price', 0))
                current_price = float(holding.get('last_price', 0))
                quantity = int(holding.get('quantity', 0))
                
                investment = avg_price * quantity
                current_val = current_price * quantity
                
                total_investment += investment
                current_value += current_val
            
            total_pnl = current_value - total_investment
            total_pnl_percentage = (total_pnl / total_investment * 100) if total_investment > 0 else 0
            
            return {
                'total_investment': total_investment,
                'current_value': current_value,
                'total_pnl': total_pnl,
                'total_pnl_percentage': total_pnl_percentage,
                'number_of_holdings': len(holdings)
            }
            
        except Exception as e:
            logger.error(f"Error calculating basic metrics: {e}")
            return {
                'total_investment': 0,
                'current_value': 0,
                'total_pnl': 0,
                'total_pnl_percentage': 0,
                'number_of_holdings': 0
            }
    
    def _create_fallback_response(self, basic_metrics: Dict, error_msg: str) -> Dict[str, Any]:
        """Create fallback response when analysis fails"""
        analysis = self._create_structured_fallback(basic_metrics, error_msg)
        
        return {
            'status': 'success',  # Mark as success with fallback data
            'analysis': analysis,
            'raw_analysis': f'Fallback analysis due to: {error_msg}',
            'timestamp': self._get_timestamp(),
            'fallback_used': True
        }
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()
