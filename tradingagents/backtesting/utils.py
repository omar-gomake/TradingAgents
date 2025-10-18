"""
Utility functions for backtesting.
"""

import pandas as pd
import backtrader as bt
from datetime import datetime, timedelta
from typing import List, Tuple


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime object."""
    if isinstance(date_str, datetime):
        return date_str
    
    formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Could not parse date: {date_str}")


def get_trading_days(start_date: str, end_date: str) -> List[str]:
    """Get list of trading days between start and end date."""
    start = parse_date(start_date)
    end = parse_date(end_date)
    
    # Generate all days
    days = []
    current = start
    while current <= end:
        # Skip weekends (5=Saturday, 6=Sunday)
        if current.weekday() < 5:
            days.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=1)
    
    return days


def create_data_feed(ticker: str, start_date: str, end_date: str) -> bt.feeds.PandasData:
    """
    Create a backtrader data feed from yfinance data.
    
    Args:
        ticker: Stock ticker symbol
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        Backtrader data feed
    """
    import yfinance as yf
    
    # Download data with some buffer for technical indicators
    start = parse_date(start_date) - timedelta(days=365)  # Extra year for indicators
    end = parse_date(end_date)
    
    df = yf.download(ticker, start=start, end=end, progress=False)
    
    if df.empty:
        raise ValueError(f"No data found for {ticker} between {start_date} and {end_date}")
    
    # Ensure proper column names for backtrader
    # Handle both single-level and multi-level column indexes
    if isinstance(df.columns, pd.MultiIndex):
        # For MultiIndex, take the first level (the actual column names)
        df.columns = [col[0].lower() if isinstance(col, tuple) else col.lower() for col in df.columns]
    else:
        # For regular Index
        df.columns = [str(col).lower() for col in df.columns]
    
    # Create the data feed
    data = bt.feeds.PandasData(
        dataname=df,
        fromdate=parse_date(start_date),
        todate=end,
    )
    
    return data


def calculate_position_size(
    current_value: float,
    price: float,
    sizing_method: str,
    sizing_value: float,
    max_position: float = None
) -> int:
    """
    Calculate the number of shares to buy based on position sizing strategy.
    
    Args:
        current_value: Current portfolio value
        price: Current price per share
        sizing_method: Position sizing method ('percentage', 'fixed', 'all_in')
        sizing_value: Value for the sizing method
        max_position: Maximum position size as percentage of portfolio
        
    Returns:
        Number of shares to buy
    """
    if sizing_method == "all_in":
        target_value = current_value
    elif sizing_method == "percentage":
        target_value = current_value * sizing_value
    elif sizing_method == "fixed":
        target_value = min(sizing_value, current_value)
    else:
        raise ValueError(f"Unknown sizing method: {sizing_method}")
    
    # Apply maximum position size limit if specified
    if max_position is not None:
        max_value = current_value * max_position
        target_value = min(target_value, max_value)
    
    # Calculate number of shares (integer)
    shares = int(target_value / price)
    
    return max(shares, 0)


def format_currency(value: float) -> str:
    """Format value as currency string."""
    return f"${value:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format value as percentage string."""
    return f"{value * 100:.{decimals}f}%"

