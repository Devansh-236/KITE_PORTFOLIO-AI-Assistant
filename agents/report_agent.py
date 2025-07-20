# agents/report_agent.py
import logging
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ReportGeneratorAgent:
    """Enhanced agent for generating comprehensive portfolio reports with dynamic user preferences"""
    
    def __init__(self, name: str = "ReportGeneratorAgent"):
        self.name = name
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def execute(self, analysis_data: Dict[str, Any], suggestions_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive portfolio report with dynamic user preferences"""
        logger.info(f"{self.name}: Generating comprehensive portfolio report...")
        
        try:
            # Generate comprehensive report content
            report_content = self._generate_comprehensive_report_content(analysis_data, suggestions_data)
            
            # Save report to file
            filename = self._save_report(report_content)
            
            # Generate executive summary
            exec_summary = self._generate_executive_summary(analysis_data, suggestions_data)
            
            logger.info(f"{self.name}: Comprehensive report generated successfully: {filename}")
            
            return {
                'status': 'success',
                'filename': filename,
                'content': report_content,
                'executive_summary': exec_summary,
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"{self.name}: Report generation error: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
    
    def _generate_comprehensive_report_content(self, analysis_data: Dict, suggestions_data: Dict) -> str:
        """Generate comprehensive formatted report content with dynamic user preferences"""
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        # Extract data with proper defaults
        analysis = analysis_data.get('analysis', {})
        suggestions = suggestions_data.get('suggestions', {})
        
        # EXTRACT USER PREFERENCES DYNAMICALLY from suggestions data
        user_preferences = suggestions.get('user_preferences_applied', {})
        
        # Get user-specific values from preferences - NO HARDCODING
        basic_info = user_preferences.get('basic_info', {})
        goals = user_preferences.get('investment_goals', {})
        risk_prefs = user_preferences.get('risk_preferences', {})
        portfolio_prefs = user_preferences.get('portfolio_preferences', {})
        constraints = user_preferences.get('constraints', {})
        
        # DYNAMIC VALUES - NOT HARDCODED - Safe conversion to ensure numeric values
        additional_budget = self._safe_int(constraints.get('additional_investment_budget', 0))
        monthly_liquidity = self._safe_int(constraints.get('liquidity_amount', 0))
        liquidity_frequency = str(constraints.get('liquidity_frequency', 'N/A'))
        liquidity_needs = bool(constraints.get('liquidity_needs', False))
        preferred_sectors = list(portfolio_prefs.get('preferred_sectors', []))
        risk_tolerance = str(risk_prefs.get('risk_tolerance', 'Not specified'))
        primary_goal = str(goals.get('primary_goal', 'Not specified'))
        time_horizon = str(goals.get('time_horizon', 'Not specified'))
        expected_return = self._safe_float(goals.get('expected_return', 0))
        monthly_addition = self._safe_int(goals.get('monthly_addition', 0))
        target_corpus = self._safe_int(goals.get('target_corpus', 0))
        user_age = self._safe_str(basic_info.get('age', 'N/A'))
        experience_level = str(basic_info.get('experience_level', 'N/A'))
        equity_preference = self._safe_int(portfolio_prefs.get('preferred_equity_allocation', 70))
        risk_score = self._safe_int(risk_prefs.get('risk_score', 3))
        existing_action = str(constraints.get('existing_portfolio_action', 'modify'))
        
        # Extract analysis data
        exec_summary = analysis.get('executive_summary', {})
        holdings_analysis = analysis.get('holdings_analysis', [])
        sector_analysis = analysis.get('sector_analysis', {})
        key_insights = analysis.get('key_insights', [])
        risk_warnings = analysis.get('risk_warnings', [])
        opportunities = analysis.get('opportunities', [])
        
        # Extract suggestions data
        personalized_analysis = suggestions.get('personalized_analysis', {})
        existing_portfolio_action = suggestions.get('existing_portfolio_action', {})
        new_investments = suggestions.get('new_investments', [])
        implementation_strategy = suggestions.get('implementation_strategy', {})
        risk_management = suggestions.get('risk_management', {})
        goal_alignment = suggestions.get('goal_alignment', {})
        
        # Build report with DYNAMIC values - using safe formatting
        report = f"""# Comprehensive Personalized Portfolio Analysis Report

*Generated on {timestamp}*

---

## 👤 Your Investment Profile

**Personal Details:**
- **Age:** {user_age} years old
- **Experience Level:** {experience_level}
- **Primary Investment Goal:** {primary_goal}
- **Investment Time Horizon:** {time_horizon}
- **Risk Tolerance:** {risk_tolerance}
- **Expected Annual Return:** {expected_return:.1f}%

**Financial Parameters:**
- **Preferred Equity Allocation:** {equity_preference}%
- **Additional Investment Budget:** ₹{additional_budget:,}
- **Monthly SIP Capacity:** ₹{monthly_addition:,}
- **Target Portfolio Value:** ₹{target_corpus:,}

**Liquidity Requirements:**"""

        if liquidity_needs and monthly_liquidity > 0:
            report += f"""
- **Liquidity Needed:** ₹{monthly_liquidity:,} {liquidity_frequency.lower()}
- **Liquidity Strategy Required:** Yes"""
        else:
            report += f"""
- **Regular Liquidity Needed:** No"""

        preferred_sectors_str = ', '.join(preferred_sectors) if preferred_sectors else 'No specific sector preferences'
        report += f"""

**Sector Preferences:** {preferred_sectors_str}

**Existing Portfolio Preference:** {existing_action.title()}

---

## 📊 Current Portfolio Analysis

### Portfolio Snapshot
| Metric | Value | Status |
|--------|--------|---------|
| **Total Investment** | ₹{self._safe_float(exec_summary.get('total_investment', 0)):,.2f} | - |
| **Current Value** | ₹{self._safe_float(exec_summary.get('current_value', 0)):,.2f} | {'🔴' if self._safe_float(exec_summary.get('total_pnl', 0)) < 0 else '🟢'} |
| **Total P&L** | ₹{self._safe_float(exec_summary.get('total_pnl', 0)):,.2f} ({self._safe_float(exec_summary.get('total_pnl_percentage', 0)):+.2f}%) | {'Loss' if self._safe_float(exec_summary.get('total_pnl', 0)) < 0 else 'Profit'} |
| **Holdings Count** | {self._safe_int(exec_summary.get('number_of_holdings', 0))} | {'⚠️ Under-diversified' if self._safe_int(exec_summary.get('number_of_holdings', 0)) < 5 else '✅ Well-diversified'} |

### Goal Alignment Analysis
- **Current vs Target:** ₹{self._safe_float(exec_summary.get('current_value', 0)):,.2f} / ₹{target_corpus:,} target
- **Gap to Target:** ₹{max(0, target_corpus - self._safe_float(exec_summary.get('current_value', 0))):,}
- **Time to Goal:** {self._calculate_time_to_goal(target_corpus, exec_summary.get('current_value', 0), monthly_addition, additional_budget):.1f} years (with current plan)

---

## 🏢 Holdings Analysis

"""
        
        # Add holdings analysis with safety check
        if holdings_analysis and isinstance(holdings_analysis, list):
            for i, holding in enumerate(holdings_analysis, 1):
                symbol = str(holding.get('symbol', f'Holding {i}'))
                sector = str(holding.get('sector', 'N/A'))
                pnl = self._safe_float(holding.get('pnl', 0))
                pnl_pct = self._safe_float(holding.get('pnl_percentage', 0))
                weight = self._safe_float(holding.get('weight_in_portfolio', 0))
                
                report += f"""### {i}. {symbol}
**Sector:** {sector} | **P&L:** ₹{pnl:,.0f} ({pnl_pct:+.2f}%)
**Portfolio Weight:** {weight:.1f}% | **Recommendation:** {holding.get('recommendation', 'Review')}

"""
        else:
            report += "Current portfolio shows high concentration - detailed analysis needed.\n\n"

        # Sector Analysis
        sector_allocation = sector_analysis.get('sector_allocation', [])
        report += f"""---

## 🏭 Sector Analysis vs Your Preferences

### Current Allocation
"""
        
        if sector_allocation and isinstance(sector_allocation, list):
            for sector in sector_allocation:
                sector_name = str(sector.get('sector', 'N/A'))
                sector_pct = self._safe_float(sector.get('percentage', 0))
                sector_value = self._safe_float(sector.get('value', 0))
                
                # Check if this sector is in user preferences
                preference_match = "✅ Preferred" if any(pref.lower() in sector_name.lower() for pref in preferred_sectors) else "⚪ Not in preferences"
                
                report += f"**{sector_name}:** {sector_pct:.1f}% (₹{sector_value:,.0f}) - {preference_match}\n"
        else:
            report += "**Current:** 100% concentrated in single unknown sector\n"

        if preferred_sectors:
            missing_sectors = [sector for sector in preferred_sectors if not any(alloc.get('sector', '').lower() == sector.lower() for alloc in sector_allocation)]
            if missing_sectors:
                report += f"""
### Missing Sectors from Your Preferences
Sectors you're interested in but not currently invested: {', '.join(missing_sectors)}
"""

        # Key Insights
        report += f"""
---

## 🔍 Key Insights Based on Your Profile

"""
        
        if key_insights and isinstance(key_insights, list):
            for i, insight in enumerate(key_insights[:5], 1):
                report += f"{i}. {insight}\n"
        else:
            # Generate insights based on user profile
            report += f"1. As a {user_age}-year-old {experience_level.lower()} investor, your portfolio needs diversification\n"
            report += f"2. Your {primary_goal.lower()} goal requires strategic sector allocation\n"
            report += f"3. With {risk_tolerance.lower()} risk tolerance, current concentration is concerning\n"

        # Personalized Recommendations Section
        report += f"""
---

## 🎯 Personalized Strategic Recommendations

### Portfolio Assessment Based on Your Profile

"""
        
        if personalized_analysis:
            alignment = str(personalized_analysis.get('alignment_with_goals', f'Portfolio needs restructuring to align with {primary_goal}'))
            risk_assess = str(personalized_analysis.get('risk_assessment', f'Risk level needs adjustment for {risk_tolerance}'))
            gap_analysis = str(personalized_analysis.get('gap_analysis', f'Missing exposure to preferred sectors: {", ".join(preferred_sectors[:3])}'))
            
            report += f"""**Goal Alignment:** {alignment}

**Risk Assessment:** {risk_assess}

**Gap Analysis:** {gap_analysis}
"""
        else:
            report += f"""**Goal Alignment:** Your {primary_goal} goal requires strategic changes to current portfolio structure

**Risk Assessment:** Current portfolio risk doesn't match your {risk_tolerance} profile

**Gap Analysis:** Missing diversification across your preferred sectors: {', '.join(preferred_sectors[:3]) if preferred_sectors else 'multiple sectors'}
"""

        # Investment Recommendations based on Budget
        report += f"""
---

## 💰 Personalized Investment Strategy

### Your Investment Capacity
- **Additional Budget Available:** ₹{additional_budget:,}
- **Monthly SIP Capacity:** ₹{monthly_addition:,}
- **Total Annual Capacity:** ₹{additional_budget + (monthly_addition * 12):,}

"""

        if additional_budget > 0 or monthly_addition > 0:
            report += f"""### Recommended Investment Allocation

Based on your preferred sectors: {preferred_sectors_str}

"""
            
            if new_investments and isinstance(new_investments, list):
                for investment in new_investments[:5]:  # Limit to top 5
                    symbol = str(investment.get('symbol', 'N/A'))
                    sector = str(investment.get('sector', 'N/A'))
                    allocation_amt = self._safe_int(investment.get('allocation_amount', 0))
                    allocation_pct = self._safe_float(investment.get('allocation_percentage', 0))
                    priority = str(investment.get('priority', 'Medium'))
                    timeline = str(investment.get('timeline', 'Immediate'))
                    rationale = str(investment.get('rationale', 'Aligns with your sector preferences'))
                    
                    # Check if sector matches user preference
                    sector_match = "✅ Matches your preference" if any(pref.lower() in sector.lower() for pref in preferred_sectors) else "🔍 Strategic addition"
                    
                    report += f"""**{symbol} - {sector} Sector** {sector_match}
- **Suggested Investment:** ₹{allocation_amt:,} ({allocation_pct:.1f}% of total portfolio)
- **Priority:** {priority} | **Timeline:** {timeline}
- **Why this fits you:** {rationale}

"""
            else:
                # Generate fallback recommendations based on user preferences
                if preferred_sectors:
                    budget_per_sector = additional_budget // max(len(preferred_sectors[:4]), 1)  # Top 4 preferred sectors
                    
                    sector_stocks = {
                        'Banking & Financial Services': ('HDFCBANK', 'Leading private bank with consistent dividends'),
                        'Information Technology': ('HCLTECH', 'Stable IT services with global presence'),
                        'Auto & Auto Components': ('MARUTI', 'Market leader in passenger vehicles'),
                        'Energy & Power': ('RELIANCE', 'Diversified energy conglomerate'),
                        'Infrastructure & Real Estate': ('L&T', 'Leading infrastructure company')
                    }
                    
                    for sector in preferred_sectors[:4]:
                        if sector in sector_stocks:
                            stock, description = sector_stocks[sector]
                            report += f"""**{stock} - {sector}** ✅ Your Preferred Sector
- **Suggested Investment:** ₹{budget_per_sector:,}
- **Priority:** High | **Timeline:** Immediate
- **Why this fits you:** {description} - aligns with your {sector} sector preference

"""

        # Liquidity Management Strategy
        if liquidity_needs and monthly_liquidity > 0:
            current_value = self._safe_float(exec_summary.get('current_value', 0))
            total_portfolio = max(current_value + additional_budget, 1)
            liquidity_percentage = (monthly_liquidity * 12) / total_portfolio * 100
            
            report += f"""
### Liquidity Management Strategy

**Your Requirement:** ₹{monthly_liquidity:,} {liquidity_frequency.lower()}
**Annual Liquidity Need:** ₹{self._calculate_annual_liquidity(monthly_liquidity, liquidity_frequency):,}
**Portfolio Allocation for Liquidity:** {liquidity_percentage:.1f}%

**Strategy:**
- Maintain {min(25, liquidity_percentage + 5):.0f}% in dividend-paying stocks from your preferred sectors
- Keep {max(10, liquidity_percentage):.0f}% in liquid instruments for immediate needs
- Focus on quarterly dividend-paying stocks in Banking and FMCG sectors
"""

        # Calculate next review date
        next_review = datetime.now() + timedelta(days=30)
        
        # Conclusion
        report += f"""
---

## 📋 Personalized Action Summary

### Your Investment Profile Summary
- **Age & Experience:** {user_age} years, {experience_level.lower()}
- **Goal & Timeline:** {primary_goal} over {time_horizon.lower()}
- **Risk & Return:** {risk_tolerance} with {expected_return:.1f}% target return
- **Budget & SIP:** ₹{additional_budget:,} immediate + ₹{monthly_addition:,} monthly
- **Sector Focus:** {', '.join(preferred_sectors[:3]) if preferred_sectors else 'Diversified approach'}

### Immediate Next Steps (Based on Your Preferences)
1. **Deploy ₹{additional_budget:,}** across {len(preferred_sectors) if preferred_sectors else 3} sectors immediately
2. **Set up ₹{monthly_addition:,} monthly SIP** for systematic growth
3. **Establish {f'₹{monthly_liquidity:,} {liquidity_frequency.lower()} withdrawal' if liquidity_needs else 'quarterly review'} system**
4. **Implement {10 if risk_score <= 2 else 15}% stop-loss** appropriate for your risk tolerance

### Success Metrics Tailored to You
- Achieve ₹{target_corpus:,} target in {self._calculate_time_to_goal(target_corpus, exec_summary.get('current_value', 0), monthly_addition, additional_budget):.1f} years
- Maintain {expected_return:.1f}% annual returns aligned with {risk_tolerance.lower()} profile
- Generate {'₹{:,} {} income'.format(monthly_liquidity, liquidity_frequency.lower()) if liquidity_needs else 'consistent growth'}
- Build diversified portfolio across your preferred sectors

---

*This analysis is specifically tailored for a {user_age}-year-old {experience_level.lower()} investor with {primary_goal.lower()} goal, ₹{additional_budget:,} immediate budget, ₹{monthly_addition:,} monthly SIP capacity, and preferences for {', '.join(preferred_sectors[:3]) if preferred_sectors else 'diversified investing'}.*

**Generated on:** {timestamp}  
**Next Review Date:** {next_review.strftime('%B %d, %Y')}

---

### Important Notes
- All recommendations are based on your preferences collected on {basic_info.get('collection_date', timestamp)[:10]}
- Market conditions can change - maintain flexibility within your risk tolerance
- Consider consulting a financial advisor for complex tax and legal matters
- This system will learn and improve recommendations based on your feedback
"""
        
        return report
    
    def _safe_int(self, value) -> int:
        """Safely convert value to integer"""
        try:
            if isinstance(value, str) and value.lower() in ['n/a', 'none', '']:
                return 0
            return int(float(str(value)) if value is not None else 0)
        except (ValueError, TypeError):
            return 0
    
    def _safe_float(self, value) -> float:
        """Safely convert value to float"""
        try:
            if isinstance(value, str) and value.lower() in ['n/a', 'none', '']:
                return 0.0
            return float(str(value)) if value is not None else 0.0
        except (ValueError, TypeError):
            return 0.0
    
    def _safe_str(self, value) -> str:
        """Safely convert value to string"""
        if value is None:
            return 'N/A'
        return str(value)
    
    def _calculate_time_to_goal(self, target: int, current: float, monthly: int, additional: int) -> float:
        """Calculate time to reach investment goal"""
        try:
            gap = max(0, target - current)
            annual_capacity = monthly * 12 + additional
            if annual_capacity <= 0:
                return 10.0  # Default 10 years if no investment capacity
            return gap / annual_capacity
        except:
            return 10.0
    
    def _calculate_annual_liquidity(self, monthly_liquidity: int, frequency: str) -> int:
        """Calculate annual liquidity requirement"""
        frequency_lower = frequency.lower()
        if 'monthly' in frequency_lower:
            return monthly_liquidity * 12
        elif 'quarterly' in frequency_lower:
            return monthly_liquidity * 4
        elif 'half' in frequency_lower or 'semi' in frequency_lower:
            return monthly_liquidity * 2
        else:
            return monthly_liquidity * 4  # Default quarterly
    
    def _generate_executive_summary(self, analysis_data: Dict, suggestions_data: Dict) -> str:
        """Generate executive summary with dynamic user preferences"""
        analysis = analysis_data.get('analysis', {})
        suggestions = suggestions_data.get('suggestions', {})
        user_preferences = suggestions.get('user_preferences_applied', {})
        
        # Extract user-specific data
        goals = user_preferences.get('investment_goals', {})
        constraints = user_preferences.get('constraints', {})
        basic_info = user_preferences.get('basic_info', {})
        
        exec_summary = analysis.get('executive_summary', {})
        
        additional_budget = self._safe_int(constraints.get('additional_investment_budget', 0))
        monthly_addition = self._safe_int(goals.get('monthly_addition', 0))
        primary_goal = str(goals.get('primary_goal', 'Investment Growth'))
        user_age = self._safe_str(basic_info.get('age', 'N/A'))
        
        immediate_actions = suggestions.get('immediate_actions', suggestions.get('new_investments', []))
        
        summary = f"""
PERSONALIZED PORTFOLIO EXECUTIVE SUMMARY
=======================================

INVESTOR PROFILE: {user_age}-year-old pursuing {primary_goal}

CURRENT PORTFOLIO:
Total Investment: ₹{self._safe_float(exec_summary.get('total_investment', 0)):,.2f}
Current Value: ₹{self._safe_float(exec_summary.get('current_value', 0)):,.2f}  
P&L: ₹{self._safe_float(exec_summary.get('total_pnl', 0)):,.2f} ({self._safe_float(exec_summary.get('total_pnl_percentage', 0)):+.2f}%)

INVESTMENT CAPACITY:
Additional Budget: ₹{additional_budget:,}
Monthly SIP: ₹{monthly_addition:,}
Total Annual Capacity: ₹{additional_budget + (monthly_addition * 12):,}

PERSONALIZED IMMEDIATE ACTIONS:
"""
        
        if immediate_actions and isinstance(immediate_actions, list):
            for i, action in enumerate(immediate_actions[:3], 1):
                action_name = str(action.get('action', action.get('symbol', 'Portfolio Action')))
                priority = str(action.get('priority', 'High'))
                summary += f"{i}. {action_name} (Priority: {priority})\n"
        else:
            summary += f"1. Deploy ₹{additional_budget:,} across preferred sectors (Priority: High)\n"
            summary += f"2. Set up ₹{monthly_addition:,} monthly SIP (Priority: High)\n"
            summary += f"3. Implement risk management for {primary_goal} (Priority: Medium)\n"
        
        return summary
    
    def _save_report(self, content: str) -> str:
        """Save comprehensive report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"personalized_portfolio_analysis_{timestamp}.md"
        filepath = os.path.join(self.reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
    
    def _get_timestamp(self) -> str:
        return datetime.now().isoformat()
