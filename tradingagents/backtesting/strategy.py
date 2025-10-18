"""
Backtrader strategy wrapper for TradingAgents.
"""

import backtrader as bt
from datetime import datetime
from typing import Dict, Any, Optional
from .config import BacktestConfig
from .utils import calculate_position_size


class TradingAgentsStrategy(bt.Strategy):
    """
    Backtrader strategy that wraps TradingAgentsGraph for backtesting.
    """
    
    params = (
        ('trading_agents_graph', None),  # TradingAgentsGraph instance
        ('config', None),                 # BacktestConfig instance
        ('ticker', None),                 # Stock ticker
        ('verbose', False),               # Print debug information
    )
    
    def __init__(self):
        """Initialize the strategy."""
        self.order = None
        self.buy_price = None
        self.buy_date = None
        self.trade_count = 0
        
        # Track trade history for learning
        self.trade_history = []
        
        # Track daily decisions
        self.decisions = []
        
        # Track agent states for analysis
        self.agent_states = []
        
        # Get configuration
        self.config: BacktestConfig = self.params.config
        self.ta_graph = self.params.trading_agents_graph
        self.ticker = self.params.ticker
        
        if self.ta_graph is None:
            raise ValueError("trading_agents_graph parameter is required")
        
        if self.config is None:
            raise ValueError("config parameter is required")
            
    def log(self, txt, dt=None):
        """Logging function."""
        if self.params.verbose:
            try:
                dt = dt or self.datas[0].datetime.date(0)
                print(f'{dt.isoformat()} - {txt}')
            except (IndexError, AttributeError):
                # Handle case where datetime is not available (e.g., at strategy end)
                print(f'{txt}')
    
    def notify_order(self, order):
        """Notification of order status changes."""
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}, '
                        f'Cost: {order.executed.value:.2f}, '
                        f'Comm: {order.executed.comm:.2f}')
                self.buy_price = order.executed.price
                self.buy_date = self.datas[0].datetime.date(0)
                
            else:  # Sell
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}, '
                        f'Cost: {order.executed.value:.2f}, '
                        f'Comm: {order.executed.comm:.2f}')
                
                # Calculate return for reflection
                if self.buy_price is not None:
                    returns = (order.executed.price - self.buy_price) / self.buy_price
                    
                    # Record trade
                    trade_info = {
                        'entry_date': self.buy_date,
                        'exit_date': self.datas[0].datetime.date(0),
                        'entry_price': self.buy_price,
                        'exit_price': order.executed.price,
                        'returns': returns,
                        'profit': order.executed.value - order.executed.comm,
                    }
                    self.trade_history.append(trade_info)
                    
                    # Reflection: Learn from this trade
                    if self.config.enable_reflection and self.config.reflection_on_close_only:
                        try:
                            self.ta_graph.reflect_and_remember(returns)
                            self.log(f'Reflected on trade with return: {returns:.2%}')
                        except Exception as e:
                            self.log(f'Error during reflection: {e}')
                    
                    self.buy_price = None
                    self.buy_date = None
                    
            self.trade_count += 1
            
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log(f'Order Canceled/Margin/Rejected')
        
        self.order = None
    
    def notify_trade(self, trade):
        """Notification of trade status changes."""
        if not trade.isclosed:
            return
        
        self.log(f'TRADE PROFIT, GROSS: {trade.pnl:.2f}, NET: {trade.pnlcomm:.2f}')
    
    def next(self):
        """
        Called on each bar (trading day).
        This is where we call TradingAgents to get trading decisions.
        """
        # Get current date
        current_date = self.datas[0].datetime.date(0).isoformat()
        
        # Check if there's a pending order
        if self.order:
            return
        
        # Get current price
        current_price = self.datas[0].close[0]
        
        try:
            # Get decision from TradingAgents
            self.log(f'Analyzing {self.ticker} on {current_date}...')
            
            final_state, decision = self.ta_graph.propagate(self.ticker, current_date)
            
            # Store the decision and state for later analysis
            self.decisions.append({
                'date': current_date,
                'decision': decision,
                'price': current_price,
            })
            self.agent_states.append(final_state)
            
            self.log(f'Decision: {decision}')
            
            # Execute trading logic based on decision
            if decision.upper() == 'BUY':
                if not self.position:  # Not currently in a position
                    # Calculate position size
                    size = calculate_position_size(
                        current_value=self.broker.getvalue(),
                        price=current_price,
                        sizing_method=self.config.position_sizing,
                        sizing_value=self.config.position_size_value,
                        max_position=self.config.max_position_size
                    )
                    
                    if size > 0:
                        self.log(f'BUY CREATE, Price: {current_price:.2f}, Size: {size}')
                        self.order = self.buy(size=size)
                        
            elif decision.upper() == 'SELL':
                if self.position:  # Currently in a position
                    self.log(f'SELL CREATE, Price: {current_price:.2f}')
                    self.order = self.sell(size=self.position.size)
                    
            elif decision.upper() == 'HOLD':
                self.log(f'HOLD, Current position: {self.position.size if self.position else 0}')
                
            # Apply stop loss and take profit if configured
            if self.position and self.buy_price:
                current_return = (current_price - self.buy_price) / self.buy_price
                
                if self.config.stop_loss and current_return <= -self.config.stop_loss:
                    self.log(f'STOP LOSS TRIGGERED at {current_return:.2%}')
                    self.order = self.sell(size=self.position.size)
                    
                elif self.config.take_profit and current_return >= self.config.take_profit:
                    self.log(f'TAKE PROFIT TRIGGERED at {current_return:.2%}')
                    self.order = self.sell(size=self.position.size)
                    
        except Exception as e:
            self.log(f'Error getting decision from TradingAgents: {e}')
            import traceback
            self.log(traceback.format_exc())
    
    def stop(self):
        """Called when backtest ends."""
        self.log(f'Strategy ending. Total trades: {self.trade_count}')
        self.log(f'Final Portfolio Value: {self.broker.getvalue():.2f}')

