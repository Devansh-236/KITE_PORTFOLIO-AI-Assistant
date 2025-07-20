# agents/suggestion_agent.py
import logging
import json
import re
from typing import Dict, Any, Optional
from config.settings import Config
from utils.api_handler import gemini_handler
from agents.preference_agent import UserPreferenceAgent

logger = logging.getLogger(__name__)

class SuggestionEngineAgent:
    """Enhanced suggestion agent that uses user preferences for personalized recommendations"""
    
    def __init__(self, name: str = "SuggestionEngineAgent"):
        self.name = name
        self.config = Config()
    
    def execute(self, analysis_data: Dict[str, Any], user_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate personalized investment suggestions based on analysis and preferences"""
        logger.info(f"{self.name}: Generating personalized investment suggestions...")
        
        if analysis_data.get('status') != 'success':
            return {
                'status': 'error',
                'error': 'Invalid analysis data provided'
            }
        
        try:
            analysis = analysis_data.get('analysis', {})
            
            # Load user preferences
            if not user_preferences:
                user_preferences = UserPreferenceAgent.load_latest_preferences()
                if not user_preferences:
                    logger.warning("No user preferences found, using default profile")
                    user_preferences = self._get_default_preferences()
            
            # Create personalized suggestion prompt
            prompt = self._create_personalized_suggestion_prompt(analysis, user_preferences)
            
            # Generate suggestions using rate-limited handler
            suggestions_text = gemini_handler.generate_content_with_retry(prompt)
            
            if not suggestions_text:
                return self._create_fallback_suggestions_response(analysis, user_preferences, "No API response")
            
            # Parse suggestions with robust error handling
            suggestions_result = self._robust_suggestions_parse(suggestions_text, analysis, user_preferences)
            
            # CRITICAL: Add user preferences to response for report generation
            suggestions_result['user_preferences_applied'] = user_preferences
            
            logger.info(f"{self.name}: Personalized suggestions generated successfully")
            
            return {
                'status': 'success',
                'suggestions': suggestions_result,
                'raw_suggestions': suggestions_text[:500],
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"{self.name}: Suggestion generation error: {e}")
            analysis = analysis_data.get('analysis', {})
            return self._create_fallback_suggestions_response(analysis, user_preferences or {}, str(e))
    
    def _create_personalized_suggestion_prompt(self, analysis: dict, preferences: dict) -> str:
        """Create personalized suggestion prompt based on user preferences"""
        exec_summary = analysis.get('executive_summary', {})
        
        # Extract user preferences
        goals = preferences.get('investment_goals', {})
        risk_prefs = preferences.get('risk_preferences', {})
        portfolio_prefs = preferences.get('portfolio_preferences', {})
        constraints = preferences.get('constraints', {})
        basic_info = preferences.get('basic_info', {})
        
        return f"""
You are a personalized investment advisor. Create investment suggestions based on the portfolio analysis AND the specific user preferences provided.

PORTFOLIO ANALYSIS:
- Investment: ₹{exec_summary.get('total_investment', 0):.0f}
- P&L: {exec_summary.get('total_pnl_percentage', 0):+.2f}%
- Holdings: {exec_summary.get('number_of_holdings', 0)}

USER PROFILE & PREFERENCES:
- Age: {basic_info.get('age', 'N/A')} | Experience: {basic_info.get('experience_level', 'N/A')}
- Primary Goal: {goals.get('primary_goal', 'Wealth Creation')}
- Time Horizon: {goals.get('time_horizon', 'Long-term')}
- Risk Tolerance: {risk_prefs.get('risk_tolerance', 'Moderate')}
- Expected Return: {goals.get('expected_return', 12)}%
- Equity Preference: {portfolio_prefs.get('preferred_equity_allocation', 70)}%
- Monthly Addition: ₹{goals.get('monthly_addition', 0)}
- Additional Budget: ₹{constraints.get('additional_investment_budget', 0)}
- Preferred Sectors: {', '.join(portfolio_prefs.get('preferred_sectors', []))}
- Avoid Sectors: {', '.join(constraints.get('avoid_sectors', []))}
- Portfolio Size Preference: {portfolio_prefs.get('diversification_preference', 8)} holdings
- Existing Portfolio Action: {constraints.get('existing_portfolio_action', 'modify')}

Return suggestions in JSON format that specifically address:
1. How to handle existing portfolio based on user preference
2. New investments aligned with preferred sectors and risk tolerance
3. Implementation considering monthly additions and additional budget
4. Risk management appropriate for user's risk tolerance

{{
  "personalized_analysis": {{
    "alignment_with_goals": "How current portfolio aligns with user goals",
    "risk_assessment": "Portfolio risk vs user risk tolerance",
    "gap_analysis": "What's missing based on preferences"
  }},
  "existing_portfolio_action": {{
    "recommendation": "hold/modify/partial_exit based on user preference",
    "rationale": "Why this action suits user profile",
    "specific_changes": ["Specific changes to make"]
  }},
  "new_investments": [
    {{
      "symbol": "STOCK_SYMBOL",
      "sector": "Sector from preferred list",
      "allocation_amount": "Amount in ₹",
      "allocation_percentage": "% of total portfolio",
      "rationale": "Why this fits user preferences",
      "priority": "High/Medium/Low",
      "timeline": "When to invest"
    }}
  ],
  "implementation_strategy": {{
    "phase_1_immediate": {{
      "budget_required": "₹ needed for immediate actions",
      "actions": ["Immediate steps"],
      "timeframe": "Timeline"
    }},
    "phase_2_monthly_sip": {{
      "monthly_amount": "{goals.get('monthly_addition', 0)}",
      "allocation_split": {{"sector1": "percentage", "sector2": "percentage"}},
      "duration": "How long to continue SIP"
    }},
    "phase_3_additional_corpus": {{
      "when_to_deploy": "Timing for additional ₹{constraints.get('additional_investment_budget', 0)}",
      "deployment_strategy": "How to invest additional corpus"
    }}
  }},
  "risk_management": {{
    "position_sizing": "Max % per holding based on risk tolerance",
    "stop_loss_strategy": "Appropriate for user risk profile",
    "rebalancing_frequency": "Based on user involvement preference",
    "emergency_fund": "Liquidity requirements based on user needs"
  }},
  "goal_alignment": {{
    "target_corpus": "{goals.get('target_corpus', 5000000)}",
    "expected_timeline": "Time to reach target",
    "probability_of_success": "Based on expected returns and risk",
    "adjustments_needed": "If goals seem unrealistic"
  }}
}}

Ensure all recommendations are specifically tailored to the user's preferences, constraints, and goals.
"""
    
    def _robust_suggestions_parse(self, text: str, analysis: Dict, preferences: Dict) -> Dict:
        """Parse suggestions with user preferences context"""
        try:
            # Clean and parse
            cleaned_text = self._clean_json_text(text)
            if cleaned_text:
                return json.loads(cleaned_text)
                
        except json.JSONDecodeError as e:
            logger.warning(f"Suggestions JSON parse failed: {e}")
        
        # Fallback: Create personalized structured suggestions
        return self._create_personalized_suggestions_fallback(analysis, preferences, text)
    
    def _create_personalized_suggestions_fallback(self, analysis: Dict, preferences: Dict, raw_text: str) -> Dict:
        """Create personalized suggestions fallback based on user preferences"""
        exec_summary = analysis.get('executive_summary', {})
        goals = preferences.get('investment_goals', {})
        risk_prefs = preferences.get('risk_preferences', {})
        portfolio_prefs = preferences.get('portfolio_preferences', {})
        constraints = preferences.get('constraints', {})
        
        # Determine suggestions based on preferences
        preferred_sectors = portfolio_prefs.get('preferred_sectors', [])
        avoid_sectors = constraints.get('avoid_sectors', [])
        risk_level = risk_prefs.get('risk_score', 3)
        additional_budget = constraints.get('additional_investment_budget', 0)
        monthly_addition = goals.get('monthly_addition', 0)
        
        # Create sector-appropriate suggestions
        investment_ideas = []
        
        # Conservative suggestions for lower risk tolerance
        if risk_level <= 2:
            safe_stocks = [
                {"symbol": "HDFCBANK", "sector": "Banking", "rationale": "Stable large-cap banking leader"},
                {"symbol": "HINDUNILVR", "sector": "FMCG", "rationale": "Defensive consumer goods"},
                {"symbol": "NESTLEIND", "sector": "FMCG", "rationale": "Quality consumer brand"}
            ]
            investment_ideas.extend(safe_stocks)
        
        # Moderate to aggressive suggestions
        elif risk_level >= 3:
            growth_stocks = [
                {"symbol": "RELIANCE", "sector": "Energy", "rationale": "Diversified conglomerate"},
                {"symbol": "HCLTECH", "sector": "IT", "rationale": "Technology growth potential"},
                {"symbol": "ASIANPAINT", "sector": "Consumer", "rationale": "Market leader in paints"}
            ]
            investment_ideas.extend(growth_stocks)
        
        # Filter based on sector preferences
        if preferred_sectors:
            filtered_ideas = []
            for idea in investment_ideas:
                if any(pref_sector.lower() in idea['sector'].lower() for pref_sector in preferred_sectors):
                    filtered_ideas.append(idea)
            if filtered_ideas:
                investment_ideas = filtered_ideas
        
        # Add allocation amounts based on budget
        for i, idea in enumerate(investment_ideas):
            if additional_budget > 0:
                idea['allocation_amount'] = additional_budget // max(len(investment_ideas), 1)
                idea['allocation_percentage'] = (idea['allocation_amount'] / max(exec_summary.get('current_value', 100000) + additional_budget, 1)) * 100
            else:
                idea['allocation_amount'] = monthly_addition * 3  # 3 months worth
                idea['allocation_percentage'] = 10  # Default percentage
            
            idea['priority'] = "High" if i < 2 else "Medium"
            idea['timeline'] = "Immediate" if additional_budget > 0 else "Via SIP"
        
        return {
            "personalized_analysis": {
                "alignment_with_goals": f"Current portfolio needs diversification to align with {goals.get('primary_goal', 'wealth creation')} goal",
                "risk_assessment": f"Portfolio risk level needs adjustment for {risk_prefs.get('risk_tolerance', 'moderate')} risk tolerance",
                "gap_analysis": f"Missing diversification across preferred sectors: {', '.join(preferred_sectors)}"
            },
            "existing_portfolio_action": {
                "recommendation": constraints.get('existing_portfolio_action', 'modify'),
                "rationale": f"Based on your preference to {constraints.get('existing_portfolio_action', 'modify')} existing holdings",
                "specific_changes": [
                    f"Reduce concentration to maximum {20 if risk_level <= 2 else 25}% per holding",
                    "Gradual rebalancing over 2-3 months to minimize market impact"
                ]
            },
            "new_investments": investment_ideas[:4],  # Limit to top 4 suggestions
            "implementation_strategy": {
                "phase_1_immediate": {
                    "budget_required": additional_budget,
                    "actions": [
                        "Deploy additional corpus in chosen stocks",
                        "Set up systematic investment plan"
                    ],
                    "timeframe": "Next 2 weeks"
                },
                "phase_2_monthly_sip": {
                    "monthly_amount": monthly_addition,
                    "allocation_split": {
                        "Large Cap": 60 if risk_level <= 2 else 50,
                        "Mid Cap": 30 if risk_level <= 2 else 35,
                        "Small Cap": 10 if risk_level <= 2 else 15
                    },
                    "duration": "12-24 months for full deployment"
                },
                "phase_3_additional_corpus": {
                    "when_to_deploy": "Stagger over 3-6 months" if additional_budget > 50000 else "Deploy immediately",
                    "deployment_strategy": "Dollar cost averaging to reduce timing risk"
                }
            },
            "risk_management": {
                "position_sizing": f"Maximum {20 if risk_level <= 2 else 25}% per stock",
                "stop_loss_strategy": f"{10 if risk_level <= 2 else 15}% stop loss based on risk tolerance",
                "rebalancing_frequency": "Quarterly review with annual rebalancing",
                "emergency_fund": "Maintain 6 months expenses before additional investments"
            },
            "goal_alignment": {
                "target_corpus": goals.get('target_corpus', 5000000),
                "expected_timeline": f"{((goals.get('target_corpus', 5000000) - exec_summary.get('current_value', 0)) / max(monthly_addition * 12 + additional_budget, 1)) if monthly_addition > 0 else 10:.0f} years",
                "probability_of_success": "High" if goals.get('expected_return', 12) <= 15 else "Moderate",
                "adjustments_needed": "Goals are realistic with consistent investing" if goals.get('expected_return', 12) <= 15 else "Consider more conservative return expectations"
            },
            "preferences_applied": {
                "sectors_focused": preferred_sectors,
                "sectors_avoided": avoid_sectors,
                "risk_alignment": f"Suggestions match {risk_prefs.get('risk_tolerance', 'moderate')} risk profile",
                "budget_utilization": f"₹{additional_budget:,} additional + ₹{monthly_addition:,} monthly considered"
            },
            "fallback_note": "Personalized recommendations based on user preferences and portfolio analysis"
        }
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Return default preferences if none are found"""
        return {
            'investment_goals': {
                'primary_goal': 'Wealth Creation',
                'time_horizon': 'Long-term (5-10 years)',
                'expected_return': 12.0,
                'monthly_addition': 10000,
                'target_corpus': 5000000
            },
            'risk_preferences': {
                'risk_tolerance': 'Moderate (Balanced growth)',
                'risk_score': 3,
                'max_acceptable_drawdown': 15.0
            },
            'portfolio_preferences': {
                'preferred_equity_allocation': 70,
                'preferred_sectors': [],
                'diversification_preference': 8
            },
            'constraints': {
                'additional_investment_budget': 0,
                'avoid_sectors': [],
                'existing_portfolio_action': 'modify'
            },
            'basic_info': {
                'age': 35,
                'experience_level': 'Intermediate'
            }
        }
    
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
    
    def _create_fallback_suggestions_response(self, analysis: Dict, preferences: Dict, error_msg: str) -> Dict[str, Any]:
        """Create fallback suggestions response with preferences"""
        suggestions = self._create_personalized_suggestions_fallback(analysis, preferences, error_msg)
        
        return {
            'status': 'success',
            'suggestions': suggestions,
            'raw_suggestions': f'Fallback suggestions due to: {error_msg}',
            'timestamp': self._get_timestamp(),
            'fallback_used': True,
            'user_preferences_applied': preferences  # CRITICAL: Include preferences
        }
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()
