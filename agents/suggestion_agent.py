# agents/suggestion_agent.py
import logging
import json
import re
from typing import Dict, Any
from config.settings import Config
from utils.api_handler import gemini_handler

logger = logging.getLogger(__name__)

class SuggestionEngineAgent:
    """Enhanced suggestion agent with robust JSON parsing"""
    
    def __init__(self, name: str = "SuggestionEngineAgent"):
        self.name = name
        self.config = Config()
    
    def execute(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate investment suggestions with robust parsing"""
        logger.info(f"{self.name}: Generating investment suggestions...")
        
        if analysis_data.get('status') != 'success':
            return {
                'status': 'error',
                'error': 'Invalid analysis data provided'
            }
        
        try:
            analysis = analysis_data.get('analysis', {})
            investment_profile = self.config.INVESTMENT_PROFILE
            
            # Create simplified suggestion prompt
            prompt = self._create_robust_suggestion_prompt(analysis, investment_profile)
            
            # Generate suggestions using rate-limited handler
            suggestions_text = gemini_handler.generate_content_with_retry(prompt)
            
            if not suggestions_text:
                return self._create_fallback_suggestions_response(analysis, "No API response")
            
            # Parse suggestions with robust error handling
            suggestions_result = self._robust_suggestions_parse(suggestions_text, analysis)
            
            logger.info(f"{self.name}: Suggestions generated successfully")
            
            return {
                'status': 'success',
                'suggestions': suggestions_result,
                'raw_suggestions': suggestions_text[:500],  # Truncate for logs
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"{self.name}: Suggestion generation error: {e}")
            analysis = analysis_data.get('analysis', {})
            return self._create_fallback_suggestions_response(analysis, str(e))
    
    def _create_robust_suggestion_prompt(self, analysis: dict, investment_profile: str) -> str:
        """Create robust suggestion prompt with clear structure"""
        exec_summary = analysis.get('executive_summary', {})
        
        total_investment = exec_summary.get('total_investment', 0)
        pnl_pct = exec_summary.get('total_pnl_percentage', 0)
        holdings_count = exec_summary.get('number_of_holdings', 0)
        
        return f"""
You are an investment advisor. Provide suggestions in ONLY valid JSON format with no additional text.

PORTFOLIO STATUS:
Investment: ₹{total_investment:.0f}
P&L: {pnl_pct:+.2f}%
Holdings: {holdings_count}
Profile: {investment_profile}

Main Issues: {'High concentration risk' if holdings_count < 3 else 'Portfolio needs optimization'}

Return ONLY this JSON structure:

{{
  "immediate_actions": [
    {{
      "action": "Reduce concentration risk",
      "priority": "High",
      "timeframe": "2 weeks",
      "reason": "Portfolio concentrated in single holding"
    }}
  ],
  "new_investment_ideas": [
    {{
      "symbol": "HDFCBANK",
      "sector": "Banking",
      "suggested_allocation": 15.0,
      "rationale": "Strong fundamentals and sector diversification"
    }},
    {{
      "symbol": "RELIANCE",
      "sector": "Energy",
      "suggested_allocation": 12.0,
      "rationale": "Large cap stability with diversification benefits"
    }},
    {{
      "symbol": "HINDUNILVR",
      "sector": "FMCG",
      "suggested_allocation": 10.0,
      "rationale": "Defensive play for portfolio stability"
    }}
  ],
  "risk_management": [
    "Limit any single position to 20% of portfolio",
    "Diversify across at least 5-6 different sectors",
    "Set stop-loss at 15% below average cost",
    "Review and rebalance monthly"
  ],
  "target_allocation": {{
    "current_holding": 25,
    "banking": 20,
    "energy": 15,
    "fmcg": 15,
    "technology": 15,
    "cash": 10
  }}
}}
"""
    
    def _robust_suggestions_parse(self, text: str, analysis: Dict) -> Dict:
        """Robust parsing of suggestions with fallback strategies"""
        try:
            # Strategy 1: Clean and parse
            cleaned_text = self._clean_json_text(text)
            if cleaned_text:
                return json.loads(cleaned_text)
                
        except json.JSONDecodeError as e:
            logger.warning(f"Suggestions JSON parse attempt 1 failed: {e}")
        
        try:
            # Strategy 2: Extract from code blocks
            json_match = re.search(r'``````', text, re.DOTALL)
            if json_match:
                return json.loads(self._clean_json_text(json_match.group(1)))
                
        except json.JSONDecodeError as e:
            logger.warning(f"Suggestions JSON parse attempt 2 failed: {e}")
        
        # Fallback: Create structured suggestions
        return self._create_structured_suggestions_fallback(analysis, text)
    
    def _clean_json_text(self, text: str) -> str:
        """Clean text for JSON parsing"""
        if not text:
            return ""
            
        # Remove markdown code blocks
        text = re.sub(r'```', '', text)
        
        start = text.find('{')
        end = text.rfind('}')
        
        if start == -1 or end == -1 or end <= start:
            return ""
            
        json_text = text[start:end+1]
        json_text = re.sub(r'//.*?\n', '\n', json_text)
        json_text = re.sub(r',\s*}', '}', json_text)
        json_text = re.sub(r',\s*]', ']', json_text)
        
        return json_text.strip()
    
    def _create_structured_suggestions_fallback(self, analysis: Dict, raw_text: str) -> Dict:
        """Create structured suggestions from analysis data"""
        exec_summary = analysis.get('executive_summary', {})
        holdings_count = exec_summary.get('number_of_holdings', 0)
        
        return {
            "immediate_actions": [
                {
                    "action": "Diversify portfolio immediately",
                    "priority": "High",
                    "timeframe": "1-2 weeks",
                    "reason": f"Portfolio has only {holdings_count} holding(s) creating excessive risk"
                },
                {
                    "action": "Implement risk management framework",
                    "priority": "High", 
                    "timeframe": "1 week",
                    "reason": "No systematic risk controls in place"
                }
            ],
            "new_investment_ideas": [
                {
                    "symbol": "HDFCBANK",
                    "sector": "Banking & Financial Services",
                    "suggested_allocation": 15.0,
                    "rationale": "Market leader in private banking with strong fundamentals"
                },
                {
                    "symbol": "RELIANCE",
                    "sector": "Energy & Petrochemicals",
                    "suggested_allocation": 12.0,
                    "rationale": "Diversified conglomerate providing stability and growth"
                },
                {
                    "symbol": "HINDUNILVR",
                    "sector": "FMCG",
                    "suggested_allocation": 10.0,
                    "rationale": "Defensive consumer goods for portfolio stability"
                },
                {
                    "symbol": "HCLTECH",
                    "sector": "Information Technology",
                    "suggested_allocation": 8.0,
                    "rationale": "Technology exposure for growth potential"
                }
            ],
            "risk_management": [
                "Reduce any single position to maximum 20% of portfolio",
                "Diversify across minimum 5-6 different sectors",
                "Set stop-loss orders at 15% below purchase price",
                "Implement monthly portfolio review and rebalancing",
                "Maintain 10% cash allocation for opportunities"
            ],
            "target_allocation": {
                "existing_holdings": 25,
                "banking_financial": 20,
                "energy_materials": 15,
                "fmcg_consumer": 15,
                "technology": 15,
                "cash_liquid": 10
            },
            "implementation_timeline": {
                "week_1": "Set up risk management rules and stop-losses",
                "week_2": "Begin diversification with banking sector addition",
                "month_1": "Add energy and FMCG positions",
                "month_2": "Complete technology sector addition",
                "ongoing": "Monthly review and rebalancing"
            },
            "fallback_note": "Structured recommendations based on portfolio analysis"
        }
    
    def _create_fallback_suggestions_response(self, analysis: Dict, error_msg: str) -> Dict[str, Any]:
        """Create fallback suggestions response"""
        suggestions = self._create_structured_suggestions_fallback(analysis, error_msg)
        
        return {
            'status': 'success',
            'suggestions': suggestions,
            'raw_suggestions': f'Fallback suggestions due to: {error_msg}',
            'timestamp': self._get_timestamp(),
            'fallback_used': True
        }
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()
