import logging
import os
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class ReportGeneratorAgent:
    """Agent for generating comprehensive portfolio reports"""
    
    def __init__(self, name: str = "ReportGeneratorAgent"):
        self.name = name
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)
    
    def execute(self, analysis_data: Dict[str, Any], suggestions_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive portfolio report"""
        logger.info(f"{self.name}: Generating portfolio report...")
        
        try:
            # Generate report content
            report_content = self._generate_report_content(analysis_data, suggestions_data)
            
            # Save report to file
            filename = self._save_report(report_content)
            
            logger.info(f"{self.name}: Report generated successfully: {filename}")
            
            return {
                'status': 'success',
                'filename': filename,
                'content': report_content,
                'timestamp': self._get_timestamp()
            }
            
        except Exception as e:
            logger.error(f"{self.name}: Report generation error: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': self._get_timestamp()
            }
    
    def _generate_report_content(self, analysis_data: Dict, suggestions_data: Dict) -> str:
        """Generate formatted report content"""
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        # Extract data
        analysis = analysis_data.get('analysis', {})
        suggestions = suggestions_data.get('suggestions', {})
        
        summary = analysis.get('summary', {})
        sector_allocation = analysis.get('sector_allocation', [])
        top_performers = analysis.get('top_performers', [])
        bottom_performers = analysis.get('bottom_performers', [])
        risk_metrics = analysis.get('risk_metrics', {})
        key_insights = analysis.get('key_insights', [])
        
        immediate_actions = suggestions.get('immediate_actions', [])
        new_investments = suggestions.get('new_investment_ideas', [])
        risk_management = suggestions.get('risk_management', [])
        
        # Generate report
        report = f"""# Portfolio Analysis Report
        
*Generated on {timestamp}*

## Executive Summary

**Portfolio Overview:**
- **Total Investment:** ₹{summary.get('total_investment', 'N/A'):,.2f}
- **Current Value:** ₹{summary.get('current_value', 'N/A'):,.2f}  
- **Total P&L:** ₹{summary.get('total_pnl', 'N/A'):,.2f} ({summary.get('total_pnl_percentage', 'N/A'):.2f}%)
- **Number of Holdings:** {summary.get('number_of_holdings', 'N/A')}

## Sector Allocation

| Sector | Allocation | Value |
|--------|------------|-------|
"""
        
        # Add sector allocation table
        for sector in sector_allocation[:10]:  # Top 10 sectors
            report += f"| {sector.get('sector', 'N/A')} | {sector.get('percentage', 0):.1f}% | ₹{sector.get('value', 0):,.0f} |\n"
        
        report += f"""
## Performance Analysis

### Top Performers 📈

| Stock | P&L | P&L % |
|-------|-----|-------|
"""
        
        # Add top performers
        for stock in top_performers[:5]:
            report += f"| {stock.get('symbol', 'N/A')} | ₹{stock.get('pnl', 0):,.0f} | {stock.get('pnl_percentage', 0):.2f}% |\n"
        
        report += f"""
### Bottom Performers 📉

| Stock | P&L | P&L % |
|-------|-----|-------|
"""
        
        # Add bottom performers  
        for stock in bottom_performers[:5]:
            report += f"| {stock.get('symbol', 'N/A')} | ₹{stock.get('pnl', 0):,.0f} | {stock.get('pnl_percentage', 0):.2f}% |\n"
        
        report += f"""
## Risk Assessment

- **Diversification Score:** {risk_metrics.get('diversification_score', 'N/A')}/10
- **Concentration Risk:** {risk_metrics.get('concentration_risk', 'N/A')}
- **Sector Concentration:** {risk_metrics.get('sector_concentration', 'N/A')}%

## Key Insights

"""
        
        # Add key insights
        for i, insight in enumerate(key_insights[:5], 1):
            report += f"{i}. {insight}\n"
        
        report += f"""
## Recommendations

### Immediate Actions Required

"""
        
        # Add immediate actions
        for i, action in enumerate(immediate_actions[:5], 1):
            report += f"""**{i}. {action.get('action', 'N/A')}**
- *Priority:* {action.get('priority', 'N/A')}
- *Timeframe:* {action.get('timeframe', 'N/A')}  
- *Reason:* {action.get('reason', 'N/A')}

"""
        
        report += f"""
### New Investment Ideas

"""
        
        # Add new investment suggestions
        for idea in new_investments[:3]:
            report += f"""**{idea.get('symbol', 'N/A')} ({idea.get('sector', 'N/A')})**
- *Suggested Allocation:* {idea.get('suggested_allocation', 0)}%
- *Rationale:* {idea.get('rationale', 'N/A')}

"""
        
        report += f"""
### Risk Management

"""
        
        # Add risk management suggestions
        for i, risk_item in enumerate(risk_management[:5], 1):
            report += f"{i}. {risk_item}\n"
        
        report += f"""

---

*This report is generated automatically by the Portfolio Analysis Multi-Agent System.*
*Please consult with a financial advisor before making investment decisions.*
"""
        
        return report
    
    def _save_report(self, content: str) -> str:
        """Save report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"portfolio_report_{timestamp}.md"
        filepath = os.path.join(self.reports_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filename
    
    def _get_timestamp(self) -> str:
        return datetime.now().isoformat()
