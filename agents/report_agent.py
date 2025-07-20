# agents/report_agent.py
import logging
import os
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ReportGeneratorAgent:
    """Enhanced agent for generating comprehensive portfolio reports"""
    
    def __init__(self, name: str = "ReportGeneratorAgent"):
        self.name = name
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def execute(self, analysis_data: Dict[str, Any], suggestions_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive portfolio report"""
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
        """Generate comprehensive formatted report content"""
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        # Extract data
        analysis = analysis_data.get('analysis', {})
        suggestions = suggestions_data.get('suggestions', {})
        
        exec_summary = analysis.get('executive_summary', {})
        holdings_analysis = analysis.get('holdings_analysis', [])
        sector_analysis = analysis.get('sector_analysis', {})
        key_insights = analysis.get('key_insights', [])
        risk_warnings = analysis.get('risk_warnings', [])
        opportunities = analysis.get('opportunities', [])
        
        # Suggestion sections
        immediate_actions = suggestions.get('immediate_actions', [])
        new_investments = suggestions.get('new_investment_ideas', [])
        risk_management = suggestions.get('risk_management', [])
        
        # Start building report
        report = f"""# Comprehensive Portfolio Analysis Report

*Generated on {timestamp}*

---

## 📊 Executive Summary

### Portfolio Snapshot
| Metric | Value | Status |
|--------|--------|---------|
| **Total Investment** | ₹{exec_summary.get('total_investment', 0):,.2f} | - |
| **Current Value** | ₹{exec_summary.get('current_value', 0):,.2f} | {'🔴' if exec_summary.get('total_pnl', 0) < 0 else '🟢'} |
| **Total P&L** | ₹{exec_summary.get('total_pnl', 0):,.2f} ({exec_summary.get('total_pnl_percentage', 0):+.2f}%) | {'Loss' if exec_summary.get('total_pnl', 0) < 0 else 'Profit'} |
| **Holdings Count** | {exec_summary.get('number_of_holdings', 0)} | {'⚠️ Under-diversified' if exec_summary.get('number_of_holdings', 0) < 5 else '✅ Diversified'} |

---

## 🏢 Holdings Analysis

"""
        
        # Add holdings analysis
        for i, holding in enumerate(holdings_analysis, 1):
            symbol = holding.get('symbol', f'Holding {i}')
            sector = holding.get('sector', 'N/A')
            pnl = holding.get('pnl', 0)
            pnl_pct = holding.get('pnl_percentage', 0)
            
            report += f"""### {i}. {symbol}
**Sector:** {sector} | **P&L:** ₹{pnl:,.0f} ({pnl_pct:+.2f}%)
**Weight:** {holding.get('weight_in_portfolio', 0):.1f}% | **Recommendation:** {holding.get('recommendation', 'Review')}

"""

        # Sector Analysis
        report += f"""---

## 🏭 Sector Analysis

### Current Allocation
"""
        
        sector_allocation = sector_analysis.get('sector_allocation', [])
        for sector in sector_allocation:
            report += f"**{sector.get('sector', 'N/A')}:** {sector.get('percentage', 0):.1f}% (₹{sector.get('value', 0):,.0f})\n"

        # Key Insights
        report += f"""
---

## 🔍 Key Insights

"""
        for i, insight in enumerate(key_insights[:5], 1):
            report += f"{i}. {insight}\n"

        # Risk Warnings
        if risk_warnings:
            report += f"""
### ⚠️ Critical Risk Warnings
"""
            for warning in risk_warnings[:3]:
                report += f"- 🚨 {warning}\n"

        # Opportunities
        if opportunities:
            report += f"""
### 🚀 Strategic Opportunities
"""
            for opportunity in opportunities[:3]:
                report += f"- 💡 {opportunity}\n"

        # Recommendations
        report += f"""
---

## 🎯 Strategic Recommendations

### Immediate Actions Required
"""
        
        for i, action in enumerate(immediate_actions[:3], 1):
            report += f"""
**{i}. {action.get('action', 'N/A')}**
- *Priority:* {action.get('priority', 'N/A')}
- *Timeframe:* {action.get('timeframe', 'N/A')}
- *Reason:* {action.get('reason', 'N/A')}
"""

        # New Investment Ideas
        if new_investments:
            report += f"""
### 💰 Recommended New Investments

"""
            for investment in new_investments[:3]:
                report += f"""**{investment.get('symbol', 'N/A')} ({investment.get('sector', 'N/A')})**
- *Suggested Allocation:* {investment.get('suggested_allocation', 0)}%
- *Rationale:* {investment.get('rationale', 'N/A')}

"""

        # Risk Management
        if risk_management:
            report += f"""
### Risk Management Framework

"""
            for i, rule in enumerate(risk_management[:5], 1):
                report += f"{i}. {rule}\n"

        # Calculate next review date (simple method)
        next_review = datetime.now() + timedelta(days=30)
        
        # Conclusion
        report += f"""
---

## 📋 Summary & Next Steps

### Immediate Priorities
1. **Risk Reduction:** Address high concentration risk in current portfolio
2. **Diversification:** Add quality holdings across different sectors  
3. **Risk Management:** Implement stop-loss and position sizing rules
4. **Monitoring:** Establish systematic review and rebalancing process

### Review Schedule
- **Daily:** Price monitoring and news flow
- **Weekly:** Technical analysis and sector rotation  
- **Monthly:** Portfolio rebalancing and performance review
- **Quarterly:** Strategy review and fundamental analysis update

---

*This comprehensive analysis is generated by an AI-powered multi-agent portfolio analysis system.*

**Generated on:** {timestamp}  
**Next Review Date:** {next_review.strftime('%B %d, %Y')}

---

### Disclaimer
This report is for informational purposes only and should not be considered as personalized investment advice. Please consult with a qualified financial advisor before making any investment decisions.
"""
        
        return report
    
    def _generate_executive_summary(self, analysis_data: Dict, suggestions_data: Dict) -> str:
        """Generate executive summary for quick review"""
        analysis = analysis_data.get('analysis', {})
        suggestions = suggestions_data.get('suggestions', {})
        
        exec_summary = analysis.get('executive_summary', {})
        immediate_actions = suggestions.get('immediate_actions', [])
        
        summary = f"""
PORTFOLIO EXECUTIVE SUMMARY
==========================

Total Investment: ₹{exec_summary.get('total_investment', 0):,.2f}
Current Value: ₹{exec_summary.get('current_value', 0):,.2f}
P&L: ₹{exec_summary.get('total_pnl', 0):,.2f} ({exec_summary.get('total_pnl_percentage', 0):+.2f}%)

IMMEDIATE ACTIONS REQUIRED:
"""
        
        for i, action in enumerate(immediate_actions[:3], 1):
            summary += f"{i}. {action.get('action', 'N/A')} (Priority: {action.get('priority', 'N/A')})\n"
        
        return summary
    
    def _save_report(self, content: str) -> str:
        """Save comprehensive report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"portfolio_analysis_{timestamp}.md"
        filepath = os.path.join(self.reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
    
    def _get_timestamp(self) -> str:
        return datetime.now().isoformat()
