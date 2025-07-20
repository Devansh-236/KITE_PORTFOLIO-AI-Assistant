#!/usr/bin/env python3
"""
Portfolio Analysis Multi-Agent System
Main orchestration script for running the complete analysis pipeline
"""

import logging
import sys
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table

from config.settings import check_config
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
    """Main orchestrator for the multi-agent portfolio analysis system"""
    
    def __init__(self):
        self.fetcher = PortfolioFetcherAgent()
        self.analyzer = DataAnalyzerAgent()
        self.suggester = SuggestionEngineAgent()
        self.reporter = ReportGeneratorAgent()
    
    def run_analysis(self):
        """Execute complete portfolio analysis workflow"""
        console.print(Panel.fit("🚀 Portfolio Analysis Multi-Agent System", style="bold blue"))
        
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
            
            # Step 3: Generate Suggestions
            task3 = progress.add_task("Generating investment suggestions...", total=None)
            suggestions_result = self.suggester.execute(analysis_result)
            progress.update(task3, completed=True)
            
            if suggestions_result.get('status') != 'success':
                console.print("❌ Suggestion generation failed", style="bold red")
                return False
            
            # Step 4: Generate Report
            task4 = progress.add_task("Generating comprehensive report...", total=None)
            report_result = self.reporter.execute(analysis_result, suggestions_result)
            progress.update(task4, completed=True)
            
            if report_result.get('status') != 'success':
                console.print("❌ Report generation failed", style="bold red")
                return False
            
            self._display_completion_summary(report_result)
            return True
    
    def _display_portfolio_summary(self, portfolio_data):
        """Display portfolio fetch summary"""
        holdings_count = len(portfolio_data.get('holdings', []))
        positions_count = len(portfolio_data.get('positions', {}).get('net', []))
        
        console.print(f"✅ Portfolio data fetched: {holdings_count} holdings, {positions_count} positions")
    
    def _display_analysis_summary(self, analysis_result):
        """Display analysis summary"""
        analysis = analysis_result.get('analysis', {})
        summary = analysis.get('summary', {})
        
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
    
    def _display_completion_summary(self, report_result):
        """Display completion summary"""
        filename = report_result.get('filename', 'Unknown')
        
        console.print(Panel(
            f"📊 Analysis Complete!\n\n"
            f"Report saved as: [bold green]{filename}[/bold green]\n"
            f"Location: [cyan]reports/{filename}[/cyan]\n\n"
            f"Open the file to view your complete portfolio analysis and recommendations.",
            title="🎉 Success",
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
            console.print("\n🎯 Portfolio analysis completed successfully!")
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
