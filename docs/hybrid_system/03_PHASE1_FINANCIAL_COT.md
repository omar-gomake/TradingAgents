# Phase 1: Financial Chain-of-Thought Implementation
## Professional Analyst Reasoning Patterns

**Duration:** 2 weeks
**Difficulty:** Medium
**Impact:** ⭐⭐⭐⭐⭐ (Immediate +15-20% decision quality)
**Prerequisites:** Existing TradingAgents installation

---

## Overview

Financial Chain-of-Thought (CoT) is FinRobot's methodology for structuring LLM reasoning to follow professional analyst workflows. Unlike generic CoT which simply encourages "step-by-step thinking," Financial CoT embeds domain-specific reasoning patterns that mirror how expert analysts actually work.

### What Makes Financial CoT Different?

**Standard CoT:**
```
"Let's think step by step about this stock..."
→ Generic reasoning
→ No error checking
→ No structured methodology
```

**Financial CoT:**
```
STEP 1: DATA GATHERING - What data do I need? How do I validate it?
STEP 2: COMPONENT ANALYSIS - Break down each piece independently
STEP 3: CROSS-VALIDATION - Check for contradictions and verify assumptions
STEP 4: SYNTHESIS - Weight and combine insights
STEP 5: PREDICTION - Specific forecast with confidence and risks
→ Professional workflow
→ Built-in error checking
→ Systematic methodology
```

---

## Implementation Strategy

### Files to Modify

1. **Analyst Agents** (Primary changes)
   - [tradingagents/agents/analysts/market_analyst.py](../../tradingagents/agents/analysts/market_analyst.py)
   - [tradingagents/agents/analysts/fundamentals_analyst.py](../../tradingagents/agents/analysts/fundamentals_analyst.py)
   - [tradingagents/agents/analysts/news_analyst.py](../../tradingagents/agents/analysts/news_analyst.py)
   - [tradingagents/agents/analysts/social_media_analyst.py](../../tradingagents/agents/analysts/social_media_analyst.py)

2. **Researcher Agents** (Secondary changes)
   - [tradingagents/agents/researchers/bull_researcher.py](../../tradingagents/agents/researchers/bull_researcher.py)
   - [tradingagents/agents/researchers/bear_researcher.py](../../tradingagents/agents/researchers/bear_researcher.py)

3. **Trader Agent** (Tertiary changes)
   - [tradingagents/agents/trader/trader.py](../../tradingagents/agents/trader/trader.py)

4. **New: Prompt Templates** (Create new file)
   - [tradingagents/agents/prompts/financial_cot.py](../../tradingagents/agents/prompts/financial_cot.py) ← NEW FILE

---

## Step-by-Step Implementation

### Step 1: Create Financial CoT Prompt Library

Create a new file with reusable CoT templates:

```python
# tradingagents/agents/prompts/financial_cot.py

"""
Financial Chain-of-Thought (CoT) prompt templates.

These templates structure LLM reasoning to follow professional analyst workflows,
incorporating error-checking and systematic methodology inspired by FinRobot.
"""

class FinancialCoTPrompts:
    """Collection of Financial CoT prompt templates."""

    @staticmethod
    def get_base_cot_structure() -> str:
        """
        Base Financial CoT structure that all analysts follow.
        """
        return """
You are a professional financial analyst. Follow this structured analysis workflow:

═══════════════════════════════════════════════════════════
STEP 1: DATA GATHERING
═══════════════════════════════════════════════════════════
- Identify what data you need for this analysis
- Call the appropriate tools to gather data
- Validate data quality and completeness
- Note any missing or questionable data

═══════════════════════════════════════════════════════════
STEP 2: COMPONENT ANALYSIS
═══════════════════════════════════════════════════════════
- Break down complex information into discrete components
- Analyze each component independently
- Look for patterns, trends, and anomalies
- Document findings for each component

═══════════════════════════════════════════════════════════
STEP 3: CROSS-VALIDATION
═══════════════════════════════════════════════════════════
- Check for contradictions between data sources
- Verify key assumptions with independent evidence
- Test robustness of conclusions
- Identify and document uncertainties

═══════════════════════════════════════════════════════════
STEP 4: SYNTHESIS
═══════════════════════════════════════════════════════════
- Weight the importance of each component
- Combine insights into a coherent picture
- Prioritize findings by impact and confidence
- Form integrated perspective

═══════════════════════════════════════════════════════════
STEP 5: PREDICTION & CONFIDENCE
═══════════════════════════════════════════════════════════
- Make specific, actionable forecast
- Quantify confidence level (HIGH/MEDIUM/LOW)
- State key assumptions and dependencies
- List primary risks to your thesis
- Define what would invalidate your conclusion

CRITICAL RULES:
1. Be explicit about each step - don't skip or combine steps
2. If data is missing or low quality, state this clearly
3. Quantify whenever possible (numbers, percentages, ranges)
4. Distinguish between facts and interpretations
5. Always provide confidence levels
"""

    @staticmethod
    def get_market_analyst_cot() -> str:
        """
        Financial CoT template specifically for technical/market analysis.
        """
        return """
You are a professional technical analyst specializing in market structure and price action.

Follow this EXACT workflow:

═══════════════════════════════════════════════════════════
STEP 1: DATA GATHERING - Technical Data Collection
═══════════════════════════════════════════════════════════
1.1 Identify Market Regime
    - What type of market are we in? (trending/ranging/volatile)
    - What indicators are most reliable in this regime?

1.2 Select Technical Indicators
    - Choose 6-8 complementary indicators (avoid redundancy)
    - Categories needed: Trend, Momentum, Volatility, Volume
    - Call get_stock_data() first to get price history
    - Call get_indicators() with your selected indicators

1.3 Validate Data
    - Check for data gaps or anomalies
    - Verify sufficient history for indicator reliability
    - Note any data quality issues

═══════════════════════════════════════════════════════════
STEP 2: COMPONENT ANALYSIS - Systematic Indicator Review
═══════════════════════════════════════════════════════════
2.1 Trend Analysis (SMAs, EMAs)
    - Short-term trend (10 EMA): [Direction, strength]
    - Medium-term trend (50 SMA): [Direction, strength]
    - Long-term trend (200 SMA): [Direction, strength]
    - Trend alignment: Are timeframes aligned or conflicting?

2.2 Momentum Analysis (RSI, MACD)
    - RSI level and interpretation (overbought/neutral/oversold)
    - MACD line vs signal line (bullish/bearish crossover?)
    - MACD histogram direction (momentum acceleration/deceleration)
    - Divergences present? (price vs indicator disagreement)

2.3 Volatility Analysis (Bollinger Bands, ATR)
    - Bollinger Band position (price vs bands)
    - Band width (expanding/contracting volatility)
    - ATR percentile (current volatility vs historical)
    - Volatility regime implications for position sizing

2.4 Volume Analysis (VWMA, Volume Trends)
    - Volume trend (increasing/decreasing)
    - Price-volume relationship (confirming or diverging)
    - Volume at key levels (support/resistance)

═══════════════════════════════════════════════════════════
STEP 3: CROSS-VALIDATION - Signal Confirmation
═══════════════════════════════════════════════════════════
3.1 Check for Contradictions
    - Do trend indicators agree with momentum indicators?
    - Is volume confirming price action?
    - Are there divergences that signal reversals?

3.2 Confluence Zones
    - Where do multiple indicators agree?
    - Identify high-probability setups with 3+ confirming signals

3.3 Historical Context
    - Compare current pattern to historical analogs
    - How reliable has this setup been historically?

═══════════════════════════════════════════════════════════
STEP 4: SYNTHESIS - Integrated Market View
═══════════════════════════════════════════════════════════
4.1 Weight Indicators
    - Which indicators are most reliable in current regime?
    - Assign importance weights based on reliability

4.2 Form Directional Bias
    - BULLISH: [List supporting evidence]
    - BEARISH: [List supporting evidence]
    - NEUTRAL: [Why no clear direction?]

4.3 Identify Key Levels
    - Support levels: [Price points]
    - Resistance levels: [Price points]
    - Breakout triggers: [What would confirm move?]

═══════════════════════════════════════════════════════════
STEP 5: PREDICTION & CONFIDENCE
═══════════════════════════════════════════════════════════
5.1 Directional Forecast
    - PRIMARY BIAS: [BULLISH/BEARISH/NEUTRAL]
    - Expected price movement: [Range or target]
    - Time horizon: [Days/weeks]

5.2 Confidence Assessment
    - CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]
    - Confidence drivers: [Why this confidence level?]
    - What would increase confidence: [Confirmations needed]

5.3 Risk Factors
    - Primary risk to thesis: [Biggest threat]
    - Invalidation level: [Price that proves thesis wrong]
    - Alternative scenarios: [What else could happen?]

═══════════════════════════════════════════════════════════
REQUIRED OUTPUT FORMAT
═══════════════════════════════════════════════════════════
After completing all steps, provide:

1. DETAILED NARRATIVE: Full analysis following the steps above
2. SUMMARY TABLE (Markdown format):

| Category | Signal | Strength | Confidence |
|----------|--------|----------|------------|
| Trend | [direction] | [1-5] | [H/M/L] |
| Momentum | [direction] | [1-5] | [H/M/L] |
| Volatility | [regime] | [1-5] | [H/M/L] |
| Volume | [signal] | [1-5] | [H/M/L] |
| **OVERALL** | **[BIAS]** | **[1-5]** | **[H/M/L]** |

3. KEY LEVELS:
   - Support: [prices]
   - Resistance: [prices]
   - Breakout: [trigger]

CRITICAL: Execute each step explicitly. Do not skip steps or provide generic analysis.
"""

    @staticmethod
    def get_fundamentals_analyst_cot() -> str:
        """
        Financial CoT template for fundamental analysis.
        """
        return """
You are a professional fundamental analyst specializing in financial statement analysis and valuation.

Follow this EXACT workflow:

═══════════════════════════════════════════════════════════
STEP 1: DATA GATHERING - Financial Data Collection
═══════════════════════════════════════════════════════════
1.1 Identify Required Data
    - What financial metrics are most relevant for this company/sector?
    - What time period comparison is needed? (QoQ, YoY, 3-year trend)

1.2 Gather Financial Data
    - Call get_fundamentals() for key metrics
    - Call get_income_statement() for profitability
    - Call get_balance_sheet() for financial health
    - Call get_cashflow() for cash generation

1.3 Validate Data
    - Check for restatements or accounting changes
    - Verify data consistency across statements
    - Note any unusual items or one-time events

═══════════════════════════════════════════════════════════
STEP 2: COMPONENT ANALYSIS - Systematic Financial Review
═══════════════════════════════════════════════════════════
2.1 Profitability Analysis
    - Revenue growth trend: [YoY%, QoQ%]
    - Gross margin trend: [Current, Historical, Sector avg]
    - Operating margin trend: [Analysis]
    - Net margin trend: [Analysis]
    - Margin expansion/compression drivers: [What's changing?]

2.2 Financial Health Analysis
    - Current ratio: [Liquidity assessment]
    - Debt-to-equity ratio: [Leverage assessment]
    - Interest coverage: [Debt service ability]
    - Working capital trend: [Operational efficiency]

2.3 Cash Flow Analysis
    - Operating cash flow trend: [Quality of earnings]
    - Free cash flow: [Cash generation after capex]
    - Cash conversion cycle: [Efficiency]
    - Dividend coverage: [Sustainability]

2.4 Valuation Metrics
    - P/E ratio vs sector/historical: [Cheap/Fair/Expensive?]
    - PEG ratio: [Growth-adjusted valuation]
    - Price-to-Book: [Asset-based valuation]
    - EV/EBITDA: [Enterprise value assessment]

═══════════════════════════════════════════════════════════
STEP 3: CROSS-VALIDATION - Financial Statement Verification
═══════════════════════════════════════════════════════════
3.1 Earnings Quality Check
    - Cash earnings vs accrual earnings: [Alignment?]
    - Revenue recognition: [Conservative or aggressive?]
    - One-time items: [Recurring or truly one-time?]

3.2 Red Flag Analysis
    - Deteriorating metrics: [What's getting worse?]
    - Accounting inconsistencies: [Any concerns?]
    - Off-balance-sheet items: [Hidden liabilities?]

3.3 Sector Comparison
    - How do metrics compare to sector peers?
    - Is the company gaining or losing competitive position?
    - Industry tailwinds/headwinds affecting all players?

═══════════════════════════════════════════════════════════
STEP 4: SYNTHESIS - Integrated Fundamental View
═══════════════════════════════════════════════════════════
4.1 Fundamental Strength Score
    - Profitability: [Score 1-5, justification]
    - Financial Health: [Score 1-5, justification]
    - Cash Generation: [Score 1-5, justification]
    - Valuation: [Score 1-5, justification]
    - Overall Score: [Weighted average]

4.2 Growth Outlook
    - Revenue growth trajectory: [Accelerating/Stable/Decelerating]
    - Margin outlook: [Expanding/Stable/Compressing]
    - Key growth drivers: [What will drive future performance?]

4.3 Risk Assessment
    - Balance sheet risks: [Leverage, liquidity issues?]
    - Earnings risks: [Sustainability of current profitability?]
    - Competitive risks: [Market share trends?]

═══════════════════════════════════════════════════════════
STEP 5: PREDICTION & CONFIDENCE
═══════════════════════════════════════════════════════════
5.1 Fundamental Outlook
    - FUNDAMENTAL BIAS: [POSITIVE/NEUTRAL/NEGATIVE]
    - Expected earnings trend: [Growth, flat, decline]
    - Valuation assessment: [Undervalued/Fair/Overvalued by X%]

5.2 Confidence Assessment
    - CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]
    - Confidence drivers: [Quality of data, clarity of trends]
    - Uncertainties: [What could change the outlook?]

5.3 Catalysts & Risks
    - Positive catalysts: [What could drive upside?]
    - Negative risks: [What could drive downside?]
    - Key upcoming events: [Earnings, product launches, etc.]

═══════════════════════════════════════════════════════════
REQUIRED OUTPUT FORMAT
═══════════════════════════════════════════════════════════
After completing all steps, provide:

1. DETAILED NARRATIVE: Full analysis following the steps above
2. SUMMARY TABLE (Markdown format):

| Metric | Current | Previous | Sector Avg | Assessment |
|--------|---------|----------|------------|------------|
| Revenue Growth | [%] | [%] | [%] | [Good/Avg/Poor] |
| Operating Margin | [%] | [%] | [%] | [Good/Avg/Poor] |
| ROE | [%] | [%] | [%] | [Good/Avg/Poor] |
| Debt/Equity | [x] | [x] | [x] | [Good/Avg/Poor] |
| P/E Ratio | [x] | [x] | [x] | [Cheap/Fair/Exp] |
| **OVERALL SCORE** | **[1-5]** | - | - | **[Assessment]** |

CRITICAL: Execute each step explicitly with specific numbers and comparisons.
"""

    @staticmethod
    def get_news_analyst_cot() -> str:
        """
        Financial CoT template for news and sentiment analysis.
        """
        return """
You are a professional news analyst specializing in market-moving events and sentiment.

Follow this EXACT workflow:

═══════════════════════════════════════════════════════════
STEP 1: DATA GATHERING - News & Event Collection
═══════════════════════════════════════════════════════════
1.1 Identify Relevant News Sources
    - Company-specific news needed
    - Sector/industry news needed
    - Macro/global news that could impact
    - Timeframe: Recent (1-7 days) vs longer-term context

1.2 Gather News Data
    - Call get_news() for company-specific news
    - Call get_global_news() for macro context
    - Call get_insider_transactions() for insider activity
    - Call get_insider_sentiment() for insider confidence

1.3 Validate Information
    - Cross-check from multiple sources
    - Distinguish facts from speculation
    - Identify potential misinformation or rumors

═══════════════════════════════════════════════════════════
STEP 2: COMPONENT ANALYSIS - Systematic News Review
═══════════════════════════════════════════════════════════
2.1 Company-Specific News
    - Earnings releases: [Results vs expectations]
    - Product announcements: [Impact assessment]
    - Management changes: [Significance]
    - Legal/regulatory: [Risk implications]
    - M&A activity: [Strategic assessment]

2.2 Sector/Industry News
    - Industry trends: [Tailwinds or headwinds?]
    - Competitive dynamics: [Market share shifts?]
    - Regulatory changes: [Impact on sector?]
    - Technology disruption: [Threats or opportunities?]

2.3 Macro/Global News
    - Economic indicators: [GDP, inflation, employment]
    - Central bank policy: [Interest rate direction]
    - Geopolitical events: [Market impact?]
    - Currency movements: [FX exposure impact]

2.4 Insider Activity
    - Insider buying/selling: [Confidence signal?]
    - Size and timing: [Significant or routine?]
    - Pattern analysis: [Clusters of activity?]

═══════════════════════════════════════════════════════════
STEP 3: CROSS-VALIDATION - News Verification
═══════════════════════════════════════════════════════════
3.1 Fact-Check Key Claims
    - Verify numbers and dates
    - Check source credibility
    - Look for independent confirmation

3.2 Sentiment vs Reality
    - Is news sentiment justified by fundamentals?
    - Market overreacting or underreacting?
    - Historical precedent for similar news?

3.3 Timeline Analysis
    - Is this news already priced in?
    - What's the expected impact duration?
    - Are there follow-up events expected?

═══════════════════════════════════════════════════════════
STEP 4: SYNTHESIS - Integrated News View
═══════════════════════════════════════════════════════════
4.1 Categorize News by Impact
    - HIGH IMPACT: [News items that should move stock significantly]
    - MEDIUM IMPACT: [Moderate importance]
    - LOW IMPACT: [Noise, already known]

4.2 Net Sentiment Assessment
    - Positive news weight: [List items]
    - Negative news weight: [List items]
    - NET SENTIMENT: [Bullish/Neutral/Bearish]

4.3 Narrative Formation
    - What's the current market narrative about this stock?
    - Is narrative changing or reinforcing?
    - Consensus view vs contrarian opportunities?

═══════════════════════════════════════════════════════════
STEP 5: PREDICTION & CONFIDENCE
═══════════════════════════════════════════════════════════
5.1 News-Based Outlook
    - NEWS BIAS: [POSITIVE/NEUTRAL/NEGATIVE]
    - Expected market reaction: [Already priced in? Or surprise?]
    - Duration of impact: [Short-term pop/drop or trend change?]

5.2 Confidence Assessment
    - CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]
    - Confidence drivers: [Source quality, cross-confirmation]
    - Ambiguity factors: [Conflicting signals?]

5.3 Upcoming Catalysts
    - Scheduled events: [Earnings date, product launch, etc.]
    - Potential surprises: [What could catch market off-guard?]
    - Sentiment inflection points: [What would change narrative?]

═══════════════════════════════════════════════════════════
REQUIRED OUTPUT FORMAT
═══════════════════════════════════════════════════════════
After completing all steps, provide:

1. DETAILED NARRATIVE: Full analysis following the steps above
2. SUMMARY TABLE (Markdown format):

| News Category | Sentiment | Impact | Confidence |
|---------------|-----------|--------|------------|
| Company News | [+/0/-] | [H/M/L] | [H/M/L] |
| Sector News | [+/0/-] | [H/M/L] | [H/M/L] |
| Macro News | [+/0/-] | [H/M/L] | [H/M/L] |
| Insider Activity | [+/0/-] | [H/M/L] | [H/M/L] |
| **NET SENTIMENT** | **[+/0/-]** | **[H/M/L]** | **[H/M/L]** |

3. KEY EVENTS:
   - Upcoming: [Scheduled catalysts]
   - Watch For: [Potential surprises]

CRITICAL: Distinguish between facts, interpretations, and speculation.
"""

    @staticmethod
    def get_researcher_cot() -> str:
        """
        Financial CoT template for bull/bear researchers.
        """
        return """
You are a professional investment researcher. Your role is to build a compelling investment case.

Follow this EXACT workflow:

═══════════════════════════════════════════════════════════
STEP 1: EVIDENCE GATHERING - Systematic Review
═══════════════════════════════════════════════════════════
1.1 Review All Analyst Reports
    - Market/technical analysis findings
    - Fundamental analysis findings
    - News and sentiment findings
    - Social media sentiment (if available)

1.2 Extract Supporting Evidence
    - Identify signals that support your thesis (bullish/bearish)
    - Rate quality of each signal (strong/moderate/weak)
    - Note confidence level of source analyst

1.3 Acknowledge Counter-Evidence
    - Identify signals that contradict your thesis
    - Assess strength of counter-arguments
    - Prepare responses

═══════════════════════════════════════════════════════════
STEP 2: ARGUMENT CONSTRUCTION - Build Investment Case
═══════════════════════════════════════════════════════════
2.1 Prioritize Evidence
    - Rank evidence by: (1) Reliability, (2) Impact, (3) Timing
    - Focus on highest-quality signals
    - Discard weak or contradictory signals

2.2 Construct Core Thesis
    - PRIMARY ARGUMENT: [Main reason for bullish/bearish stance]
    - SUPPORTING ARGUMENTS: [2-4 key supporting points]
    - Each argument must have: Evidence + Logic + Expected outcome

2.3 Quantify Expected Return
    - Base case return estimate: [%]
    - Upside case: [%]
    - Downside case: [%]
    - Probability-weighted expected return: [%]

═══════════════════════════════════════════════════════════
STEP 3: COUNTER-ARGUMENT ANALYSIS - Stress Test Thesis
═══════════════════════════════════════════════════════════
3.1 Identify Weaknesses
    - What are the holes in your argument?
    - What evidence contradicts your view?
    - What assumptions could be wrong?

3.2 Prepare Rebuttals
    - For each counter-argument, prepare response
    - When is counter-argument valid? When not?
    - How do you weight conflicting evidence?

3.3 Define Invalidation Criteria
    - What would prove your thesis wrong?
    - What data/events would force thesis change?
    - Where is the stop-loss on this idea?

═══════════════════════════════════════════════════════════
STEP 4: SYNTHESIS - Comprehensive Investment Recommendation
═══════════════════════════════════════════════════════════
4.1 Investment Conviction
    - Strength of thesis: [STRONG/MODERATE/WEAK]
    - Quality of evidence: [HIGH/MEDIUM/LOW]
    - Timing: [URGENT/GOOD/WAIT]

4.2 Recommended Position
    - ACTION: [BUY/SELL/HOLD]
    - POSITION SIZE: [LARGE/MEDIUM/SMALL] - based on conviction
    - TIME HORIZON: [Days/Weeks/Months]
    - TARGET: [Price target with justification]

4.3 Risk Management
    - Stop loss: [Price level and rationale]
    - Take profit: [Price level and rationale]
    - Position limits: [Max % of portfolio]

═══════════════════════════════════════════════════════════
STEP 5: PRESENTATION - Clear Communication
═══════════════════════════════════════════════════════════
5.1 Executive Summary
    - One-paragraph thesis statement
    - Key supporting points (3-5 bullets)
    - Risk/reward assessment

5.2 Detailed Argumentation
    - Full reasoning chain
    - Evidence with confidence levels
    - Counter-arguments addressed

5.3 Action Items
    - Specific recommendation
    - Clear entry/exit criteria
    - Monitoring plan

CRITICAL: Be intellectually honest. If evidence is weak or contradictory, state this clearly.
"""

    @staticmethod
    def get_trader_cot() -> str:
        """
        Financial CoT template for final trading decision.
        """
        return """
You are a professional trader making final trading decisions.

Follow this EXACT workflow:

═══════════════════════════════════════════════════════════
STEP 1: INFORMATION SYNTHESIS - Consolidate All Analysis
═══════════════════════════════════════════════════════════
1.1 Review Investment Plan
    - Bull thesis: [Key points]
    - Bear thesis: [Key points]
    - Manager recommendation: [Conclusion]

1.2 Review Original Analyst Reports
    - Technical outlook: [Signal and confidence]
    - Fundamental outlook: [Signal and confidence]
    - News sentiment: [Signal and confidence]
    - Overall analyst agreement: [High/Medium/Low]

1.3 Review Past Performance
    - Check memory for similar situations
    - What worked? What didn't?
    - Apply lessons learned

═══════════════════════════════════════════════════════════
STEP 2: DECISION FRAMEWORK - Systematic Trade Evaluation
═══════════════════════════════════════════════════════════
2.1 Conviction Assessment
    - Analyst agreement level: [%]
    - Quality of evidence: [Score 1-5]
    - Clarity of signals: [Clear/Mixed/Unclear]
    - Conviction score: [1-10]

2.2 Risk/Reward Analysis
    - Expected return (base case): [%]
    - Upside potential: [%]
    - Downside risk: [%]
    - Risk/Reward ratio: [X:1]
    - Meets minimum threshold? [Yes/No - typically need 2:1]

2.3 Timing Assessment
    - Is this the right entry point? [Yes/No/Wait]
    - Catalyst timing: [Immediate/Near-term/Uncertain]
    - Better opportunities available? [Comparison]

═══════════════════════════════════════════════════════════
STEP 3: POSITION STRUCTURING - Trade Design
═══════════════════════════════════════════════════════════
3.1 Action Decision
    - PRIMARY ACTION: [BUY/SELL/HOLD]
    - Rationale: [2-3 sentence explanation]

3.2 Position Sizing (if BUY/SELL)
    - Base size: [% of portfolio]
    - Conviction adjustment: [+/- adjustment]
    - Risk adjustment: [+/- adjustment]
    - FINAL SIZE: [% of portfolio]
    - Size rationale: [Why this size?]

3.3 Risk Parameters
    - Entry price: [Target entry]
    - Stop loss: [Price level and % loss]
    - Take profit: [Price level and % gain]
    - Time stop: [Max holding period if no movement]

═══════════════════════════════════════════════════════════
STEP 4: EXECUTION PLAN - Trade Implementation
═══════════════════════════════════════════════════════════
4.1 Order Type
    - Market/Limit/Stop: [Choice and reason]
    - If limit: Limit price and rationale

4.2 Execution Timing
    - Execute now: [Yes/No]
    - If wait: Trigger conditions for execution

4.3 Monitoring Plan
    - Key metrics to watch: [List]
    - Review frequency: [Daily/Weekly]
    - Adjustment triggers: [What would cause position change?]

═══════════════════════════════════════════════════════════
STEP 5: FINAL DECISION - Clear Trade Instruction
═══════════════════════════════════════════════════════════
5.1 Trade Summary
    - ACTION: [BUY/SELL/HOLD]
    - CONVICTION: [HIGH/MEDIUM/LOW]
    - SIZE: [% of portfolio or "NONE" if HOLD]
    - STOP LOSS: [Price or %]
    - TAKE PROFIT: [Price or %]

5.2 Decision Confidence
    - CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]
    - Key assumptions: [What must be true for this to work?]
    - Alternative scenarios: [What else could happen?]

5.3 Required Format
    FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL**

═══════════════════════════════════════════════════════════
REQUIRED OUTPUT FORMAT
═══════════════════════════════════════════════════════════
After completing all steps, provide:

1. DETAILED NARRATIVE: Full reasoning following steps above

2. TRADE SPECIFICATION:
   - Action: [BUY/SELL/HOLD]
   - Position Size: [%]
   - Entry: [Price/Market]
   - Stop Loss: [Price/%]
   - Take Profit: [Price/%]
   - Time Horizon: [Period]
   - Conviction: [H/M/L]

3. ALWAYS END WITH:
   FINAL TRANSACTION PROPOSAL: **[BUY/HOLD/SELL]**

CRITICAL: Be decisive. No hedging. Clear action with specific parameters.
"""
```

This creates a comprehensive prompt library that can be imported and used by all agents.

---

### Step 2: Update Market Analyst

Now update the market analyst to use Financial CoT:

```python
# tradingagents/agents/analysts/market_analyst.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from tradingagents.agents.utils.agent_utils import get_stock_data, get_indicators
from tradingagents.dataflows.config import get_config
from tradingagents.agents.prompts.financial_cot import FinancialCoTPrompts  # NEW IMPORT


def create_market_analyst(llm):

    def market_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        tools = [
            get_stock_data,
            get_indicators,
        ]

        # NEW: Use Financial CoT prompt
        system_message = FinancialCoTPrompts.get_market_analyst_cot()

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. The company we want to look at is {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        report = ""

        if len(result.tool_calls) == 0:
            report = result.content

        return {
            "messages": [result],
            "market_report": report,
        }

    return market_analyst_node
```

---

### Step 3: Update Other Analysts

Apply similar changes to:
- Fundamentals Analyst → Use `FinancialCoTPrompts.get_fundamentals_analyst_cot()`
- News Analyst → Use `FinancialCoTPrompts.get_news_analyst_cot()`
- Social Media Analyst → Adapt news CoT template

---

### Step 4: Update Researchers

```python
# tradingagents/agents/researchers/bull_researcher.py

from tradingagents.agents.prompts.financial_cot import FinancialCoTPrompts

def create_bull_researcher(llm, memory):
    def bull_researcher_node(state, name):
        # ... existing code ...

        # NEW: Use Financial CoT for researchers
        base_cot = FinancialCoTPrompts.get_researcher_cot()

        system_prompt = f"""
{base_cot}

IMPORTANT: You are the BULL researcher. Your role is to argue FOR investment.
Focus on positive evidence while acknowledging risks honestly.

Past learnings from similar situations:
{past_memory_str}
"""

        # ... rest of implementation ...
```

---

### Step 5: Update Trader

```python
# tradingagents/agents/trader/trader.py

from tradingagents.agents.prompts.financial_cot import FinancialCoTPrompts

def create_trader(llm, memory):
    def trader_node(state, name):
        # ... existing code ...

        # NEW: Use Financial CoT for trader
        trader_cot = FinancialCoTPrompts.get_trader_cot()

        messages = [
            {
                "role": "system",
                "content": f"{trader_cot}\n\nPast learnings: {past_memory_str}"
            },
            context,
        ]

        # ... rest of implementation ...
```

---

## Testing the Implementation

### Test 1: Single Stock Analysis

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Create graph with Financial CoT
config = DEFAULT_CONFIG.copy()
graph = TradingAgentsGraph(
    selected_analysts=["market", "fundamentals", "news"],
    debug=True,
    config=config
)

# Test on single ticker
final_state, decision = graph.propagate("AAPL", "2024-01-15")

# Review the market_report to see Financial CoT in action
print("=" * 80)
print("MARKET ANALYST REPORT (with Financial CoT):")
print("=" * 80)
print(final_state["market_report"])
```

**What to Look For:**
- Explicit step-by-step structure in analyst reports
- Clear data gathering → analysis → synthesis → prediction flow
- Confidence levels stated explicitly
- Markdown summary tables present
- More systematic and thorough analysis compared to before

### Test 2: Backtesting Comparison

```python
from tradingagents.backtesting import BacktestEngine, BacktestConfig

# Run backtest with Financial CoT
config = BacktestConfig(
    initial_cash=100000,
    enable_reflection=True
)

engine = BacktestEngine(
    ticker="AAPL",
    start_date="2023-01-01",
    end_date="2024-01-01",
    config=config
)

results = engine.run()
results.print_metrics()

# Compare with previous results (if available)
# Expected: +10-15% improvement in Sharpe Ratio
```

---

## Expected Results

### Before Financial CoT:
```
Market Analyst Report:
"Looking at AAPL, the technical indicators are mixed. RSI is around 65,
MACD is positive. The stock has been trending up. I think it's bullish."

Confidence: Unclear
Structure: Unorganized
Depth: Surface-level
```

### After Financial CoT:
```
Market Analyst Report:

═══════════════════════════════════════════════════════════
STEP 1: DATA GATHERING - Technical Data Collection
═══════════════════════════════════════════════════════════
1.1 Market Regime Assessment
Current regime appears to be TRENDING BULL MARKET based on:
- 200 SMA trending up
- New highs being made
- Low volatility environment (VIX <20)

Selected indicators for this regime:
- Trend: 50 SMA, 200 SMA, 10 EMA
- Momentum: RSI, MACD
- Volatility: Bollinger Bands, ATR

[Tool calls executed: get_stock_data, get_indicators]

1.2 Data Validation
✓ 500 days of price data retrieved
✓ All indicators calculated successfully
✓ No data gaps detected

═══════════════════════════════════════════════════════════
STEP 2: COMPONENT ANALYSIS - Systematic Indicator Review
═══════════════════════════════════════════════════════════
2.1 Trend Analysis
- 10 EMA: $185.20 (price above, BULLISH)
- 50 SMA: $178.45 (price well above +3.9%, BULLISH)
- 200 SMA: $165.30 (price above +12.3%, STRONG BULLISH)
- Trend alignment: ALL timeframes bullish - VERY STRONG

2.2 Momentum Analysis
- RSI: 64.5 (approaching overbought but not extreme)
- MACD: +2.35 (above signal line +1.80, BULLISH crossover 3 days ago)
- MACD Histogram: Increasing (momentum accelerating)
- No divergences detected

2.3 Volatility Analysis
- Price position: Near upper Bollinger Band (90th percentile)
- Band width: Expanding (volatility increasing)
- ATR: 3.45 (65th percentile - moderate volatility)

═══════════════════════════════════════════════════════════
STEP 3: CROSS-VALIDATION - Signal Confirmation
═══════════════════════════════════════════════════════════
3.1 Signal Alignment
✓ Trend indicators: 100% bullish agreement
✓ Momentum indicators: Confirm trend
✓ Volume: Increasing on up days (confirming)

3.2 Confluence Zone
High conviction at current level with:
- 50 SMA support at $178
- MACD bullish crossover confirmed
- Trend alignment across all timeframes

3.3 Historical Context
Similar setups (RSI 60-70, all MAs bullish, MACD crossover) have led to:
- Continued upside 72% of the time
- Average additional gain: +8.5%
- Average duration: 15-25 days

═══════════════════════════════════════════════════════════
STEP 4: SYNTHESIS - Integrated Market View
═══════════════════════════════════════════════════════════
4.1 Weighted Assessment
Trend: 40% weight (very reliable in current regime) → BULLISH
Momentum: 30% weight → BULLISH
Volatility: 20% weight → NEUTRAL (near upper band, some caution)
Volume: 10% weight → BULLISH (confirming)

OVERALL WEIGHTED SIGNAL: BULLISH (confidence: 8/10)

4.2 Key Levels
- Support: $178 (50 SMA), $175 (previous resistance)
- Resistance: $190 (psychological), $195 (upper BB)
- Breakout trigger: Sustained move above $190 on volume

═══════════════════════════════════════════════════════════
STEP 5: PREDICTION & CONFIDENCE
═══════════════════════════════════════════════════════════
5.1 Directional Forecast
PRIMARY BIAS: BULLISH
Expected move: +5-8% over next 2-3 weeks
Target range: $190-$195

5.2 Confidence Assessment
CONFIDENCE LEVEL: HIGH (8/10)

Confidence drivers:
- All timeframe trend alignment (very rare, very reliable)
- Fresh MACD crossover (timing signal)
- Volume confirmation
- Historical precedent strong

What would increase confidence to 10/10:
- Breakout above $190 on high volume
- RSI pullback to 55-60 then resuming up

5.3 Risk Factors
Primary risk: Near upper Bollinger Band (short-term overbought)
Invalidation level: Break below $178 (50 SMA)
Alternative scenario: Consolidation 2-3 weeks before next leg up

═══════════════════════════════════════════════════════════
SUMMARY TABLE
═══════════════════════════════════════════════════════════
| Category | Signal | Strength | Confidence |
|----------|--------|----------|------------|
| Trend | BULLISH | 5/5 | HIGH |
| Momentum | BULLISH | 4/5 | HIGH |
| Volatility | NEUTRAL | 3/5 | MEDIUM |
| Volume | BULLISH | 4/5 | HIGH |
| **OVERALL** | **BULLISH** | **4/5** | **HIGH** |

Key Levels:
- Support: $178, $175
- Resistance: $190, $195
- Breakout: $190 on volume
```

**Difference:**
- ✅ Systematic structure
- ✅ Explicit reasoning chains
- ✅ Quantified confidence
- ✅ Clear invalidation criteria
- ✅ Historical context
- ✅ Professional-level depth

---

## Rollout Plan

### Week 1: Core Analysts
**Days 1-2:** Create `financial_cot.py` prompt library
**Days 3-4:** Update Market Analyst and test thoroughly
**Days 5-7:** Update Fundamentals and News Analysts

### Week 2: Researchers and Trader
**Days 1-3:** Update Bull and Bear Researchers
**Days 4-5:** Update Trader agent
**Days 6-7:** Full integration testing and backtesting comparison

---

## Success Metrics

### Quantitative
- **Decision Quality:** +15-20% improvement in Sharpe Ratio
- **Win Rate:** +5-10% increase
- **Drawdown:** -2-5% reduction in max drawdown

### Qualitative
- **Analyst Reports:** More structured, systematic, professional
- **Confidence Levels:** Explicitly stated (currently implicit/missing)
- **Error Rate:** Fewer contradictions and logical errors
- **Reproducibility:** More consistent reasoning across similar situations

---

## Next Phase

After completing Phase 1, proceed to **[04_PHASE2_DIRECTOR_AGENT.md](04_PHASE2_DIRECTOR_AGENT.md)** to build the Smart Scheduler and adaptive analyst selection system.

---

**Completion Checklist:**

- [ ] Create `financial_cot.py` prompt library
- [ ] Update Market Analyst with CoT
- [ ] Update Fundamentals Analyst with CoT
- [ ] Update News Analyst with CoT
- [ ] Update Social Media Analyst with CoT
- [ ] Update Bull Researcher with CoT
- [ ] Update Bear Researcher with CoT
- [ ] Update Trader with CoT
- [ ] Run single-stock test
- [ ] Run backtest comparison
- [ ] Document performance improvements
- [ ] Commit and push changes

---

**Estimated Time:** 10-14 days (2 weeks)
**Effort Level:** Medium
**Required Skills:** Python, prompt engineering, understanding of financial analysis
