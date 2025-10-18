"""
Fast Backtest Configuration
Optimized for quick testing with minimal LLM calls
"""
import os

FAST_BACKTEST_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    
    # Fast LLM settings - use cheapest/fastest models
    "llm_provider": "openai",
    "deep_think_llm": "gpt-4o-mini",  # Use fast model instead of o4-mini
    "quick_think_llm": "gpt-4o-mini",
    "backend_url": "https://api.openai.com/v1",
    
    # Minimal debate - skip debates entirely for speed
    "max_debate_rounds": 0,  # Skip researcher debates
    "max_risk_discuss_rounds": 0,  # Skip risk team debates
    "max_recur_limit": 100,
    
    # Data vendor configuration
    "data_vendors": {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",  # Use yfinance instead of API calls
        "news_data": "yfinance",  # Use yfinance instead of news APIs
    },
    
    # Tool-level configuration
    "tool_vendors": {},
}

