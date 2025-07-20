# agents/preference_agent.py
import logging
import json
import os 
from typing import Dict, Any, List, Optional
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich.table import Table
from rich.panel import Panel

logger = logging.getLogger(__name__)
console = Console()

class UserPreferenceAgent:
    """Agent for collecting comprehensive user preferences and investment goals"""
    
    def __init__(self, name: str = "UserPreferenceAgent"):
        self.name = name
        self.preferences = {}
    
    def execute(self) -> Dict[str, Any]:
        """Collect user preferences through interactive prompts"""
        logger.info(f"{self.name}: Starting user preference collection...")
        
        try:
            # Display welcome message
            self._display_welcome()
            
            # Collect preferences in sections
            basic_info = self._collect_basic_info()
            investment_goals = self._collect_investment_goals()
            risk_preferences = self._collect_risk_preferences()
            portfolio_preferences = self._collect_portfolio_preferences()
            constraints = self._collect_constraints()
            
            # Compile all preferences
            preferences = {
                'basic_info': basic_info,
                'investment_goals': investment_goals,
                'risk_preferences': risk_preferences,
                'portfolio_preferences': portfolio_preferences,
                'constraints': constraints,
                'timestamp': self._get_timestamp(),
                'status': 'success'
            }
            
            # Display summary
            self._display_preferences_summary(preferences)
            
            # Confirm preferences
            if Confirm.ask("\n✅ Are these preferences correct?"):
                self._save_preferences(preferences)
                logger.info(f"{self.name}: User preferences collected successfully")
                return preferences
            else:
                console.print("❌ Preferences collection cancelled. Please run again to update.")
                return {'status': 'cancelled'}
                
        except KeyboardInterrupt:
            console.print("\n⏹️ Preference collection interrupted by user")
            return {'status': 'cancelled'}
        except Exception as e:
            logger.error(f"{self.name}: Error collecting preferences: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
    
    def _display_welcome(self):
        """Display welcome message and instructions"""
        welcome_text = """
🎯 Portfolio Preference Collection

Before we analyze your portfolio and provide recommendations, 
let's understand your investment preferences, goals, and constraints.

This will help us provide personalized recommendations that align 
with your specific situation and objectives.

⏱️ This will take about 5-10 minutes.
        """
        
        console.print(Panel(welcome_text, title="Welcome", style="bold blue"))
    
    def _collect_basic_info(self) -> Dict[str, Any]:
        """Collect basic investor information"""
        console.print("\n📋 Section 1: Basic Information", style="bold green")
        
        age = IntPrompt.ask("What is your age?", default=30)
        
        experience_options = {
            1: "Beginner (0-2 years)",
            2: "Intermediate (2-5 years)", 
            3: "Experienced (5-10 years)",
            4: "Expert (10+ years)"
        }
        
        console.print("\nInvestment Experience:")
        for key, value in experience_options.items():
            console.print(f"{key}. {value}")
        
        experience = IntPrompt.ask("Select your experience level", choices=["1", "2", "3", "4"])
        
        income_ranges = {
            1: "Less than ₹5 lakhs",
            2: "₹5-15 lakhs",
            3: "₹15-30 lakhs", 
            4: "₹30-50 lakhs",
            5: "More than ₹50 lakhs"
        }
        
        console.print("\nAnnual Income Range:")
        for key, value in income_ranges.items():
            console.print(f"{key}. {value}")
        
        income_range = IntPrompt.ask("Select your income range", choices=["1", "2", "3", "4", "5"])
        
        return {
            'age': age,
            'experience_level': experience_options[experience],
            'income_range': income_ranges[income_range],
            'collection_date': datetime.now().isoformat()
        }
    
    def _collect_investment_goals(self) -> Dict[str, Any]:
        """Collect investment goals and objectives"""
        console.print("\n🎯 Section 2: Investment Goals & Objectives", style="bold green")
        
        # Primary goal
        goal_options = {
            1: "Wealth Creation (Long-term growth)",
            2: "Regular Income Generation", 
            3: "Capital Preservation",
            4: "Tax Saving",
            5: "Retirement Planning",
            6: "Child's Education/Marriage",
            7: "House Purchase",
            8: "Other specific goal"
        }
        
        console.print("\nWhat is your primary investment goal?")
        for key, value in goal_options.items():
            console.print(f"{key}. {value}")
        
        primary_goal = IntPrompt.ask("Select primary goal", choices=[str(i) for i in range(1, 9)])
        
        if primary_goal == 8:
            other_goal = Prompt.ask("Please specify your goal")
            primary_goal_text = other_goal
        else:
            primary_goal_text = goal_options[primary_goal]
        
        # Investment horizon
        horizon_options = {
            1: "Short-term (< 2 years)",
            2: "Medium-term (2-5 years)",
            3: "Long-term (5-10 years)", 
            4: "Very long-term (> 10 years)"
        }
        
        console.print("\nInvestment Time Horizon:")
        for key, value in horizon_options.items():
            console.print(f"{key}. {value}")
        
        horizon = IntPrompt.ask("Select your time horizon", choices=["1", "2", "3", "4"])
        
        # Expected returns
        expected_return = FloatPrompt.ask(
            "What annual return do you expect from your portfolio? (%)", 
            default=12.0
        )
        
        # Corpus addition
        add_corpus = Confirm.ask("Do you plan to add more money to your portfolio regularly?")
        monthly_addition = 0
        if add_corpus:
            monthly_addition = IntPrompt.ask("How much can you invest monthly? (₹)", default=10000)
        
        return {
            'primary_goal': primary_goal_text,
            'time_horizon': horizon_options[horizon],
            'expected_return': expected_return,
            'add_corpus': add_corpus,
            'monthly_addition': monthly_addition,
            'target_corpus': IntPrompt.ask("What is your target portfolio value? (₹ in lakhs)", default=50) * 100000
        }
    
    def _collect_risk_preferences(self) -> Dict[str, Any]:
        """Collect risk tolerance and preferences"""
        console.print("\n⚖️ Section 3: Risk Preferences", style="bold green")
        
        # Risk tolerance
        risk_options = {
            1: "Very Conservative (Capital protection is priority)",
            2: "Conservative (Limited fluctuations acceptable)",
            3: "Moderate (Balanced growth with reasonable risk)",
            4: "Aggressive (High growth potential, higher volatility ok)",
            5: "Very Aggressive (Maximum growth, comfortable with high risk)"
        }
        
        console.print("\nRisk Tolerance:")
        for key, value in risk_options.items():
            console.print(f"{key}. {value}")
        
        risk_tolerance = IntPrompt.ask("Select your risk tolerance", choices=["1", "2", "3", "4", "5"])
        
        # Maximum drawdown tolerance
        max_drawdown = FloatPrompt.ask(
            "Maximum portfolio decline you can tolerate? (%)", 
            default=15.0
        )
        
        # Volatility comfort
        volatility_comfort = Confirm.ask("Are you comfortable with daily portfolio fluctuations of 2-5%?")
        
        return {
            'risk_tolerance': risk_options[risk_tolerance],
            'max_acceptable_drawdown': max_drawdown,
            'volatility_comfort': volatility_comfort,
            'risk_score': risk_tolerance  # 1-5 scale
        }
    
    def _collect_portfolio_preferences(self) -> Dict[str, Any]:
        """Collect portfolio construction preferences"""
        console.print("\n💼 Section 4: Portfolio Preferences", style="bold green")
        
        # Equity allocation preference
        equity_allocation = IntPrompt.ask(
            "What percentage of equity exposure do you prefer? (%)", 
            default=70
        )
        
        # Sector preferences
        console.print("\nDo you have any sector preferences?")
        sector_preferences = []
        
        sectors = [
            "Banking & Financial Services", "Information Technology", "Healthcare & Pharma",
            "FMCG & Consumer", "Auto & Auto Components", "Energy & Power", 
            "Infrastructure & Real Estate", "Metals & Mining", "Chemicals"
        ]
        
        for sector in sectors:
            preference = Confirm.ask(f"Interested in {sector}?", default=False)
            if preference:
                sector_preferences.append(sector)
        
        # Market cap preferences
        console.print("\nMarket Cap Preferences:")
        large_cap = IntPrompt.ask("Large Cap allocation preference? (%)", default=60)
        mid_cap = IntPrompt.ask("Mid Cap allocation preference? (%)", default=25)  
        small_cap = IntPrompt.ask("Small Cap allocation preference? (%)", default=15)
        
        # International exposure
        international_exposure = Confirm.ask("Interested in international/global exposure?", default=False)
        
        # ESG preferences
        esg_focus = Confirm.ask("Do you prefer ESG (Environmental, Social, Governance) focused investments?", default=False)
        
        return {
            'preferred_equity_allocation': equity_allocation,
            'preferred_sectors': sector_preferences,
            'market_cap_preference': {
                'large_cap': large_cap,
                'mid_cap': mid_cap, 
                'small_cap': small_cap
            },
            'international_exposure': international_exposure,
            'esg_focus': esg_focus,
            'diversification_preference': IntPrompt.ask("How many stocks do you prefer in your portfolio?", default=8)
        }
    
    def _collect_constraints(self) -> Dict[str, Any]:
        """Collect investment constraints and restrictions"""
        console.print("\n🚫 Section 5: Constraints & Restrictions", style="bold green")
        
        # Budget constraints
        additional_investment_budget = IntPrompt.ask(
            "How much additional money can you invest now? (₹)", 
            default=0
        )
        
        # Liquidity needs
        liquidity_needs = Confirm.ask("Do you need regular liquidity from your portfolio?")
        liquidity_frequency = None
        liquidity_amount = None
        
        if liquidity_needs:
            liquidity_frequency = Prompt.ask("How often? (Monthly/Quarterly/Half-yearly)", default="Quarterly")
            liquidity_amount = IntPrompt.ask("How much liquidity needed? (₹)", default=10000)
        
        # Tax considerations
        tax_saving_priority = Confirm.ask("Is tax saving a priority?", default=False)
        
        # Sector restrictions
        avoid_sectors = []
        console.print("\nAny sectors you want to avoid?")
        
        sectors_to_avoid = [
            "Tobacco", "Alcohol", "Gambling", "Defense", "Pharmaceuticals", "None"
        ]
        
        for sector in sectors_to_avoid:
            if sector == "None":
                if not avoid_sectors:
                    console.print("No sector restrictions selected.")
                break
            avoid = Confirm.ask(f"Avoid {sector}?", default=False)
            if avoid:
                avoid_sectors.append(sector)
        
        # Existing portfolio changes
        existing_portfolio_change = Prompt.ask(
            "How would you like to handle your existing portfolio? (Hold/Modify/Sell)", 
            default="Modify"
        )
        
        return {
            'additional_investment_budget': additional_investment_budget,
            'liquidity_needs': liquidity_needs,
            'liquidity_frequency': liquidity_frequency,
            'liquidity_amount': liquidity_amount,
            'tax_saving_priority': tax_saving_priority,
            'avoid_sectors': avoid_sectors,
            'existing_portfolio_action': existing_portfolio_change.lower()
        }
    
    def _display_preferences_summary(self, preferences: Dict[str, Any]):
        """Display a summary of collected preferences"""
        console.print("\n📋 Preferences Summary", style="bold blue")
        
        # Basic Info
        basic = preferences['basic_info']
        console.print(f"\n👤 **Basic Info:**")
        console.print(f"   Age: {basic['age']} | Experience: {basic['experience_level']}")
        console.print(f"   Income: {basic['income_range']}")
        
        # Goals
        goals = preferences['investment_goals']
        console.print(f"\n🎯 **Investment Goals:**")
        console.print(f"   Primary Goal: {goals['primary_goal']}")
        console.print(f"   Time Horizon: {goals['time_horizon']}")
        console.print(f"   Expected Return: {goals['expected_return']}%")
        console.print(f"   Monthly Addition: ₹{goals['monthly_addition']:,}")
        
        # Risk
        risk = preferences['risk_preferences']
        console.print(f"\n⚖️ **Risk Profile:**")
        console.print(f"   Risk Tolerance: {risk['risk_tolerance']}")
        console.print(f"   Max Drawdown: {risk['max_acceptable_drawdown']}%")
        
        # Portfolio
        portfolio = preferences['portfolio_preferences']
        console.print(f"\n💼 **Portfolio Preferences:**")
        console.print(f"   Equity Allocation: {portfolio['preferred_equity_allocation']}%")
        console.print(f"   Preferred Sectors: {', '.join(portfolio['preferred_sectors']) if portfolio['preferred_sectors'] else 'No specific preference'}")
        console.print(f"   Number of Holdings: {portfolio['diversification_preference']}")
        
        # Constraints
        constraints = preferences['constraints']
        console.print(f"\n🚫 **Constraints:**")
        console.print(f"   Additional Budget: ₹{constraints['additional_investment_budget']:,}")
        console.print(f"   Existing Portfolio: {constraints['existing_portfolio_action'].title()}")
        console.print(f"   Avoid Sectors: {', '.join(constraints['avoid_sectors']) if constraints['avoid_sectors'] else 'None'}")
    
    def _save_preferences(self, preferences: Dict[str, Any]):
        """Save preferences to file"""
        preferences_dir = "user_preferences"
        os.makedirs(preferences_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"user_preferences_{timestamp}.json"
        filepath = os.path.join(preferences_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, indent=2, default=str)
        
        # Also save as latest preferences
        latest_filepath = os.path.join(preferences_dir, "latest_preferences.json")
        with open(latest_filepath, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, indent=2, default=str)
        
        console.print(f"✅ Preferences saved to: {filename}")
    
    def _get_timestamp(self) -> str:
        return datetime.now().isoformat()

    @staticmethod
    def load_latest_preferences() -> Optional[Dict[str, Any]]:
        """Load the latest saved preferences"""
        try:
            filepath = os.path.join("user_preferences", "latest_preferences.json")
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load latest preferences: {e}")
        return None
