# main.py - Updated version with preference agent
#!/usr/bin/env python3
"""
Portfolio Analysis Multi-Agent System with User Preference Collection
"""

import logging
import sys
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

from config.settings import check_config
from agents.preference_agent import UserPreferenceAgent
from agents.fetcher_agent import PortfolioFetcherAgent
from agents.analyzer_agent import DataAnalyzerAgent  
from agents.suggestion_agent import SuggestionEngineAgent
from agents.report_agent import ReportGeneratorAgent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('portfolio_analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Setup rich console
console = Console()

class PortfolioAnalysisOrchestrator:
    """Main orchestrator with user preference collection"""
    
    def __init__(self):
        self.preference_agent = UserPreferenceAgent()
        self.fetcher = PortfolioFetcherAgent()
        self.analyzer = DataAnalyzerAgent()
        self.suggester = SuggestionEngineAgent()
        self.reporter = ReportGeneratorAgent()
    
    def run_analysis(self):
        """Execute complete portfolio analysis workflow with preference collection"""
        console.print(Panel.fit("🚀 Personalized Portfolio Analysis Multi-Agent System", style="bold blue"))
        
        # Step 0: Collect User Preferences (New!)
        console.print("\n🎯 Step 1: Collecting Your Investment Preferences", style="bold yellow")
        user_preferences = self.preference_agent.execute()
        
        if user_preferences.get('status') != 'success':
            console.print("❌ Preference collection failed or was cancelled", style="bold red")
            return False
        
        console.print("✅ User preferences collected successfully!")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            
            # Step 1: Fetch Portfolio Data
            task1 = progress.add_task("Fetching portfolio data...", total=None)
            portfolio_data = self.fetcher.execute()
            progress.update(task1, completed=True)
            
            if portfolio_data.get('status') != 'success':
                console.print("❌ Failed to fetch portfolio data", style="bold red")
                return False
            
            self._display_portfolio_summary(portfolio_data)
            
            # Step 2: Analyze Data
            task2 = progress.add_task("Analyzing portfolio data...", total=None)
            analysis_result = self.analyzer.execute(portfolio_data)
            progress.update(task2, completed=True)
            
            if analysis_result.get('status') != 'success':
                console.print("❌ Portfolio analysis failed", style="bold red")
                return False
            
            self._display_analysis_summary(analysis_result)
            
            # Step 3: Generate Personalized Suggestions
            task3 = progress.add_task("Generating personalized suggestions...", total=None)
            suggestions_result = self.suggester.execute(analysis_result, user_preferences)
            progress.update(task3, completed=True)

            if suggestions_result.get('status') != 'success':
                console.print("❌ Suggestion generation failed", style="bold red")
                # Print debug info to see what went wrong
                console.print(f"Debug: Suggestions error - {suggestions_result.get('error', 'Unknown error')}")
                return False

            # Debug: Check if suggestions were generated
            console.print(f"🔍 Debug: Suggestions status - {suggestions_result.get('status')}")

            # Step 4: Generate Report
            task4 = progress.add_task("Generating personalized report...", total=None)
            try:
                report_result = self.reporter.execute(analysis_result, suggestions_result)
                progress.update(task4, completed=True)
                
                if report_result.get('status') != 'success':
                    console.print("❌ Report generation failed", style="bold red")
                    console.print(f"Debug: Report error - {report_result.get('error', 'Unknown error')}")
                    return False
                    
            except Exception as e:
                console.print(f"❌ Report generation exception: {e}", style="bold red")
                logger.exception("Report generation failed")
                return False

            self._display_completion_summary(report_result, user_preferences)
            return True

    
    def _display_portfolio_summary(self, portfolio_data):
        """Display portfolio fetch summary"""
        holdings_count = len(portfolio_data.get('holdings', []))
        positions_count = len(portfolio_data.get('positions', {}).get('net', []))
        
        console.print(f"✅ Portfolio data fetched: {holdings_count} holdings, {positions_count} positions")
    
    def _display_analysis_summary(self, analysis_result):
        """Display analysis summary"""
        analysis = analysis_result.get('analysis', {})
        summary = analysis.get('executive_summary', {})
        
        if summary:
            table = Table(title="Portfolio Summary")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Total Investment", f"₹{summary.get('total_investment', 0):,.2f}")
            table.add_row("Current Value", f"₹{summary.get('current_value', 0):,.2f}")
            table.add_row("Total P&L", f"₹{summary.get('total_pnl', 0):,.2f}")
            table.add_row("P&L %", f"{summary.get('total_pnl_percentage', 0):.2f}%")
            
            console.print(table)
        
        console.print("✅ Portfolio analysis completed")
    
    def _display_completion_summary(self, report_result, user_preferences):
        """Display completion summary with personalization info"""
        filename = report_result.get('filename', 'Unknown')
        
        # Display user goal alignment
        goals = user_preferences.get('investment_goals', {})
        primary_goal = goals.get('primary_goal', 'Wealth Creation')
        
        console.print(Panel(
            f"📊 Personalized Analysis Complete!\n\n"
            f"🎯 **Tailored for your goal:** {primary_goal}\n"
            f"📋 **Report saved as:** [bold green]{filename}[/bold green]\n"
            f"📂 **Location:** [cyan]reports/{filename}[/cyan]\n"
            f"⚙️ **Preferences saved** for future analysis\n\n"
            f"Your recommendations are specifically customized based on:\n"
            f"• Your risk tolerance and investment horizon\n"
            f"• Sector preferences and constraints\n" 
            f"• Budget and corpus addition plans\n"
            f"• Existing portfolio handling preference\n\n"
            f"Open the report to view your personalized portfolio strategy!",
            title="🎉 Personalized Success",
            style="bold green"
        ))

def main():
    """Main entry point"""
    try:
        # Check configuration
        console.print("🔧 Checking configuration...")
        check_config()
        console.print("✅ Configuration validated")
        
        # Initialize and run orchestrator
        orchestrator = PortfolioAnalysisOrchestrator()
        success = orchestrator.run_analysis()
        
        if success:
            console.print("\n🎯 Personalized portfolio analysis completed successfully!")
            return 0
        else:
            console.print("\n❌ Portfolio analysis failed!")
            return 1
            
    except KeyboardInterrupt:
        console.print("\n🛑 Analysis interrupted by user")
        return 1
    except Exception as e:
        console.print(f"\n💥 Unexpected error: {e}", style="bold red")
        logger.exception("Unexpected error in main execution")
        return 1

if __name__ == "__main__":
    sys.exit(main())
