"""
CLI commands for backtesting TradingAgents strategies.
"""

import typer
from pathlib import Path
import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box
from dotenv import load_dotenv

from tradingagents.backtesting import BacktestEngine, MultiTickerBacktestEngine, BacktestConfig
from tradingagents.default_config import DEFAULT_CONFIG
from cli.utils import (
    select_analysts,
    select_research_depth,
    select_llm_provider,
    select_shallow_thinking_agent,
    select_deep_thinking_agent,
)

# Load environment variables
load_dotenv()

console = Console()
app = typer.Typer(help="Backtesting commands for TradingAgents")


def get_backtest_config():
    """Interactive prompts to configure backtest parameters."""
    console.print(Panel.fit(
        "[bold green]Backtesting Configuration[/bold green]",
        border_style="green"
    ))
    
    # Ticker(s)
    console.print("\n[bold]Step 1: Ticker Selection[/bold]")
    ticker_input = Prompt.ask(
        "Enter ticker symbol(s) (comma-separated for multiple)",
        default="AAPL"
    )
    tickers = [t.strip().upper() for t in ticker_input.split(',')]
    
    # Date range
    console.print("\n[bold]Step 2: Date Range[/bold]")
    default_end = datetime.datetime.now().strftime("%Y-%m-%d")
    default_start = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    
    start_date = Prompt.ask("Start date (YYYY-MM-DD)", default=default_start)
    end_date = Prompt.ask("End date (YYYY-MM-DD)", default=default_end)
    
    # Initial capital
    console.print("\n[bold]Step 3: Capital Settings[/bold]")
    initial_cash = float(Prompt.ask("Initial capital ($)", default="100000"))
    
    # Position sizing
    console.print("\n[bold]Step 4: Position Sizing[/bold]")
    sizing_options = {
        "1": ("percentage", "Percentage of portfolio (e.g., 95%)"),
        "2": ("fixed", "Fixed dollar amount per trade"),
        "3": ("all_in", "All-in (100% of capital)"),
    }
    
    console.print("Position sizing strategy:")
    for key, (_, desc) in sizing_options.items():
        console.print(f"  {key}. {desc}")
    
    sizing_choice = Prompt.ask("Select option", choices=["1", "2", "3"], default="1")
    position_sizing = sizing_options[sizing_choice][0]
    
    if position_sizing == "percentage":
        position_size_value = float(Prompt.ask("Percentage (0-100)", default="95")) / 100
    elif position_sizing == "fixed":
        position_size_value = float(Prompt.ask("Fixed amount ($)", default="10000"))
    else:
        position_size_value = 1.0
    
    # Trading costs
    console.print("\n[bold]Step 5: Trading Costs[/bold]")
    commission = float(Prompt.ask("Commission (%)", default="0.1")) / 100
    
    # Risk management
    console.print("\n[bold]Step 6: Risk Management[/bold]")
    use_stop_loss = Confirm.ask("Enable stop loss?", default=False)
    stop_loss = None
    if use_stop_loss:
        stop_loss = float(Prompt.ask("Stop loss (%)", default="10")) / 100
    
    use_take_profit = Confirm.ask("Enable take profit?", default=False)
    take_profit = None
    if use_take_profit:
        take_profit = float(Prompt.ask("Take profit (%)", default="20")) / 100
    
    # Learning
    console.print("\n[bold]Step 7: Agent Learning[/bold]")
    enable_reflection = Confirm.ask("Enable agent learning (reflection)?", default=True)
    
    # Analyst selection
    console.print("\n[bold]Step 8: Analyst Configuration[/bold]")
    selected_analysts = select_analysts()
    
    # Research depth
    console.print("\n[bold]Step 9: Research Depth[/bold]")
    research_depth = select_research_depth()
    
    # LLM configuration
    console.print("\n[bold]Step 10: LLM Configuration[/bold]")
    llm_provider, backend_url = select_llm_provider()
    shallow_thinker = select_shallow_thinking_agent(llm_provider)
    deep_thinker = select_deep_thinking_agent(llm_provider)
    
    # Create configs
    backtest_config = BacktestConfig(
        initial_cash=initial_cash,
        commission=commission,
        position_sizing=position_sizing,
        position_size_value=position_size_value,
        stop_loss=stop_loss,
        take_profit=take_profit,
        enable_reflection=enable_reflection,
    )
    
    ta_config = DEFAULT_CONFIG.copy()
    ta_config["quick_think_llm"] = shallow_thinker
    ta_config["deep_think_llm"] = deep_thinker
    ta_config["max_debate_rounds"] = research_depth
    ta_config["max_risk_discuss_rounds"] = research_depth
    ta_config["llm_provider"] = llm_provider.lower()
    ta_config["backend_url"] = backend_url
    
    return {
        'tickers': tickers,
        'start_date': start_date,
        'end_date': end_date,
        'backtest_config': backtest_config,
        'ta_config': ta_config,
        'selected_analysts': [analyst.value for analyst in selected_analysts],
    }


@app.command()
def run(
    ticker: str = typer.Option(None, "--ticker", "-t", help="Stock ticker symbol"),
    start_date: str = typer.Option(None, "--start", "-s", help="Start date (YYYY-MM-DD)"),
    end_date: str = typer.Option(None, "--end", "-e", help="End date (YYYY-MM-DD)"),
    initial_cash: float = typer.Option(100000, "--cash", "-c", help="Initial capital"),
    output_dir: str = typer.Option(None, "--output", "-o", help="Output directory for results"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Use interactive mode"),
):
    """
    Run a backtest for TradingAgents strategy.
    
    Examples:
        # Interactive mode (default)
        tradingagents backtest run
        
        # Command line mode
        tradingagents backtest run -t AAPL -s 2023-01-01 -e 2024-01-01 -c 100000
    """
    if interactive or not all([ticker, start_date, end_date]):
        # Interactive mode
        config = get_backtest_config()
        
        # Show summary
        console.print("\n" + "="*60)
        console.print("[bold green]Backtest Configuration Summary[/bold green]")
        console.print("="*60)
        
        summary_table = Table(show_header=False, box=box.SIMPLE)
        summary_table.add_column("Parameter", style="cyan")
        summary_table.add_column("Value", style="yellow")
        
        summary_table.add_row("Ticker(s)", ", ".join(config['tickers']))
        summary_table.add_row("Period", f"{config['start_date']} to {config['end_date']}")
        summary_table.add_row("Initial Capital", f"${config['backtest_config'].initial_cash:,.2f}")
        summary_table.add_row("Position Sizing", config['backtest_config'].position_sizing)
        summary_table.add_row("Commission", f"{config['backtest_config'].commission:.2%}")
        summary_table.add_row("Analysts", ", ".join(config['selected_analysts']))
        summary_table.add_row("Reflection", "Enabled" if config['backtest_config'].enable_reflection else "Disabled")
        
        console.print(summary_table)
        console.print("="*60 + "\n")
        
        if not Confirm.ask("Proceed with backtest?", default=True):
            console.print("[yellow]Backtest cancelled.[/yellow]")
            return
        
        # Determine output directory
        if output_dir is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            ticker_str = "_".join(config['tickers'])
            output_dir = f"results/backtests/{ticker_str}_{timestamp}"
        
        # Run backtest
        if len(config['tickers']) == 1:
            # Single ticker
            engine = BacktestEngine(
                ticker=config['tickers'][0],
                start_date=config['start_date'],
                end_date=config['end_date'],
                initial_cash=config['backtest_config'].initial_cash,
                config=config['backtest_config'],
                ta_config=config['ta_config'],
                selected_analysts=config['selected_analysts'],
                debug=False,
            )
            
            results = engine.run()
            
            # Print metrics
            results.print_metrics()
            
            # Save results
            engine.save_results(output_dir)
            engine.plot(output_dir + '/plots')
            
            console.print(f"\n[bold green]✓ Backtest complete! Results saved to {output_dir}[/bold green]")
            
        else:
            # Multiple tickers
            engine = MultiTickerBacktestEngine(
                tickers=config['tickers'],
                start_date=config['start_date'],
                end_date=config['end_date'],
                initial_cash=config['backtest_config'].initial_cash,
                config=config['backtest_config'],
                ta_config=config['ta_config'],
                selected_analysts=config['selected_analysts'],
                debug=False,
            )
            
            results = engine.run()
            engine.save_all_results(output_dir)
            
            console.print(f"\n[bold green]✓ Multi-ticker backtest complete! Results saved to {output_dir}[/bold green]")
    
    else:
        # Command-line mode (non-interactive)
        if output_dir is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"results/backtests/{ticker}_{timestamp}"
        
        console.print(f"[bold]Running backtest for {ticker}[/bold]")
        console.print(f"Period: {start_date} to {end_date}")
        console.print(f"Initial capital: ${initial_cash:,.2f}\n")
        
        config = BacktestConfig(initial_cash=initial_cash)
        
        engine = BacktestEngine(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            initial_cash=initial_cash,
            config=config,
            debug=False,
        )
        
        results = engine.run()
        results.print_metrics()
        
        engine.save_results(output_dir)
        engine.plot(output_dir + '/plots')
        
        console.print(f"\n[bold green]✓ Backtest complete! Results saved to {output_dir}[/bold green]")


@app.command()
def compare(
    tickers: str = typer.Argument(..., help="Comma-separated list of tickers to compare"),
    start_date: str = typer.Option(None, "--start", "-s", help="Start date (YYYY-MM-DD)"),
    end_date: str = typer.Option(None, "--end", "-e", help="End date (YYYY-MM-DD)"),
    initial_cash: float = typer.Option(100000, "--cash", "-c", help="Initial capital per ticker"),
):
    """
    Compare backtest results across multiple tickers.
    
    Example:
        tradingagents backtest compare "AAPL,GOOGL,MSFT" -s 2023-01-01 -e 2024-01-01
    """
    ticker_list = [t.strip().upper() for t in tickers.split(',')]
    
    if not start_date:
        start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    console.print(f"\n[bold]Comparing {len(ticker_list)} tickers[/bold]")
    console.print(f"Period: {start_date} to {end_date}\n")
    
    config = BacktestConfig(initial_cash=initial_cash)
    
    engine = MultiTickerBacktestEngine(
        tickers=ticker_list,
        start_date=start_date,
        end_date=end_date,
        initial_cash=initial_cash * len(ticker_list),
        cash_per_ticker=initial_cash,
        config=config,
        debug=False,
    )
    
    results = engine.run()
    
    # Create comparison table
    console.print("\n[bold]Comparison Results[/bold]\n")
    
    comparison_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    comparison_table.add_column("Ticker", style="cyan", justify="center")
    comparison_table.add_column("Return", style="green", justify="right")
    comparison_table.add_column("Sharpe", style="yellow", justify="right")
    comparison_table.add_column("Max DD", style="red", justify="right")
    comparison_table.add_column("Trades", style="blue", justify="right")
    comparison_table.add_column("Win Rate", style="magenta", justify="right")
    
    for ticker, result in results.items():
        comparison_table.add_row(
            ticker,
            f"{result.total_return:.2%}",
            f"{result.sharpe_ratio:.2f}",
            f"{result.max_drawdown_pct:.2%}",
            str(result.num_trades),
            f"{result.win_rate:.2%}",
        )
    
    console.print(comparison_table)
    
    # Save results
    output_dir = f"results/backtests/comparison_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    engine.save_all_results(output_dir)
    
    console.print(f"\n[bold green]✓ Comparison complete! Results saved to {output_dir}[/bold green]")


if __name__ == "__main__":
    app()

