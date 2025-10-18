# Phase 3: SEC Document Deep Analyzer
## Extract Alpha from 10-K/10-Q Filings

**Duration:** 2 weeks (Weeks 5-6)
**Difficulty:** High
**Impact:** ⭐⭐⭐⭐⭐ (+10-15% from information edge)
**Prerequisites:** Phases 1-2 completed

---

## Overview

Add deep SEC filing analysis to extract insights others miss:
- Full 10-K/10-Q parsing and analysis
- Risk Factors tracking (what's NEW vs what's boilerplate)
- MD&A (Management Discussion & Analysis) sentiment and changes
- Accounting quality red flags
- Competitive positioning analysis

**Key Innovation:** Most traders only look at headline numbers. We analyze the full filings to find hidden risks and opportunities.

---

## Key Files to Create

1. `tradingagents/agents/analysts/sec_analyst.py` - New SEC analyst agent
2. `tradingagents/agents/utils/sec_tools.py` - SEC filing tools
3. `tradingagents/dataflows/sec_edgar.py` - SEC EDGAR data vendor
4. `tradingagents/agents/prompts/sec_cot.py` - SEC-specific Financial CoT prompts

---

## Quick Implementation

### SEC Tools

```python
# tradingagents/agents/utils/sec_tools.py

import requests
from sec_api import QueryApi, RenderApi
from langchain.tools import tool

@tool
def get_latest_10k(ticker: str) -> Dict[str, Any]:
    """Download and parse latest 10-K filing."""
    # Use sec-api.io or sec-edgar-downloader
    # Extract key sections: Risk Factors, MD&A, Financial Statements
    pass

@tool
def get_risk_factors(ticker: str, filing_type: str = "10-K") -> str:
    """Extract and analyze Risk Factors section."""
    pass

@tool
def compare_filings(ticker: str, num_filings: int = 2) -> Dict:
    """Compare consecutive filings to find changes."""
    pass
```

### SEC Analyst Agent

```python
# tradingagents/agents/analysts/sec_analyst.py

def create_sec_analyst(llm):
    """Create SEC filing analysis agent."""

    def sec_analyst_node(state):
        ticker = state["company_of_interest"]
        date = state["trade_date"]

        tools = [get_latest_10k, get_risk_factors, compare_filings]

        system_message = """
        You are an expert SEC filing analyst following Financial CoT methodology.

        STEP 1: DATA GATHERING
        - Download latest 10-K or 10-Q
        - Extract key sections
        - Validate filing completeness

        STEP 2: RISK FACTOR ANALYSIS
        - Read Risk Factors section carefully
        - Identify NEW risks (not in previous filing)
        - Classify by severity (high/medium/low)

        STEP 3: MD&A ANALYSIS  
        - Analyze management tone and outlook
        - Identify forward-looking statements
        - Compare to previous period

        STEP 4: ACCOUNTING QUALITY
        - Check for red flags (revenue recognition, off-balance sheet)
        - Analyze working capital trends
        - Review auditor notes

        STEP 5: SYNTHESIS & CONCLUSION
        - Overall filing quality score (1-5)
        - Key takeaways for investors
        - Red flags or positive catalysts
        """

        # Standard agent implementation...
        pass

    return sec_analyst_node
```

---

## Expected Results

**New Alpha Sources:**
- Early detection of emerging risks (before market realizes)
- Management sentiment shifts
- Accounting quality deterioration warnings
- Competitive position changes
- Forward guidance extraction

**Performance Impact:** +10-15% from information edge

---

## Next Phase

Continue to [06_PHASE4_STRATEGY_GENERATOR.md](06_PHASE4_STRATEGY_GENERATOR.md)
