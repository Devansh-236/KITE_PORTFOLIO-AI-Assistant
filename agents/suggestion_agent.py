import logging
import json
import google.generativeai as genai
from typing import Dict, Any
from config.settings import Config

logger = logging.getLogger(__name__)

class SuggestionEngineAgent:
    """Agent for generating investment suggestions based on analysis"""
    
    def __init__(self, name: str = "SuggestionEngineAgent"):
        self.name = name
        self.config = Config()
        
        # Initialize Gemini
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def execute(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized investment suggestions"""
        logger.info(f"{self.name}: Generating investment suggestions...")
        
        if analysis_data.get('status') != 'success':
            return {
                'status': 'error',
                'error': 'Invalid analysis data provided'
            }
        
        try:
            analysis = analysis_data.get('analysis', {})
            investment_profile = self.config.INVESTMENT_PROFILE
            
            # Create suggestion prompt
            prompt = self._create_suggestion_prompt(analysis, investment_profile)
            
            # Generate suggestions using Gemini
            response = self.model.generate_content(prompt)
            suggestions_text = response.text
            
            # Parse structured suggestions
            suggestions_result = self._parse_suggestions(suggestions_text)
            
            logger.info(f"{self.name}: Suggestions generated successfully")
            
            return {
                'status': 'success',
                'suggestions': suggestions_result,
                'raw_suggestions': suggestions_text,
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"{self.name}: Suggestion generation error: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
    
    def _create_suggestion_prompt(self, analysis: dict, investment_profile: str) -> str:
        """Create personalized suggestion prompt"""
        return f"""
        Based on the following portfolio analysis and user investment profile, provide actionable investment suggestions.
        
        PORTFOLIO ANALYSIS:
        {json.dumps(analysis, indent=2)}
        
        INVESTMENT PROFILE: {investment_profile}
        
        Please provide suggestions in the following JSON structure:
        {{
            "immediate_actions": [
                {{
                    "action": "Rebalance Technology sector",
                    "reason": "Over-concentrated at 35%, should be <25%",
                    "priority": "High",
                    "timeframe": "1-2 weeks"
                }},
                ...
            ],
            "portfolio_optimization": {{
                "suggested_allocation": {{
                    "Technology": 25,
                    "Healthcare": 20,
                    "Finance": 15,
                    ...
                }},
                "rebalancing_needed": true,
                "risk_reduction_steps": [
                    "Diversify sector exposure",
                    "Consider adding defensive stocks"
                ]
            }},
            "new_investment_ideas": [
                {{
                    "symbol": "HDFCBANK",
                    "sector": "Finance",
                    "rationale": "Underweight in banking sector, strong fundamentals",
                    "suggested_allocation": 5.0
                }},
                ...
            ],
            "risk_management": [
                "Set stop-loss for positions with >20% gains",
                "Consider booking profits in over-performing stocks"
            ],
            "long_term_strategy": [
                "Maintain diversified portfolio across 8-10 sectors",
                "Regular monthly SIP for consistent investing"
            ]
        }}
        
        Tailor suggestions specifically to the investment profile: {investment_profile}
        """
    
    def _parse_suggestions(self, suggestions_text: str) -> Dict:
        """Parse suggestion response"""
        try:
            json_start = suggestions_text.find('{')
            json_end = suggestions_text.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_str = suggestions_text[json_start:json_end]
                return json.loads(json_str)
            else:
                return {
                    'immediate_actions': [],
                    'raw_suggestions': suggestions_text
                }
                
        except json.JSONDecodeError:
            return {
                'immediate_actions': [],
                'error': 'Could not parse suggestions',
                'raw_suggestions': suggestions_text
            }
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()
