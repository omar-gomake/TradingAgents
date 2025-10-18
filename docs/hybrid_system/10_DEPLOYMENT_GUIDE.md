# Production Deployment Guide
## Running Your Autonomous Trading System 24/7

**Last Updated:** 2025-10-18

---

## Overview

This guide covers deploying the complete hybrid trading system to production for fully autonomous operation.

---

## Architecture for Production

```
┌─────────────────────────────────────────────────────────────┐
│                   LOAD BALANCER / NGINX                      │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    FASTAPI REST API                          │
│  - Trading endpoints                                         │
│  - Portfolio status                                          │
│  - Performance metrics                                       │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  CELERY TASK QUEUE                           │
│  - Daily screening (6:00 AM)                                 │
│  - Analysis pipeline (7:00-9:00 AM)                          │
│  - Portfolio optimization (9:15 AM)                          │
│  - Trade execution (9:30 AM)                                 │
│  - Continuous monitoring                                     │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌────────────────────┴────────────────────┐
        ▼                                         ▼
┌──────────────────┐                    ┌──────────────────┐
│  REDIS BROKER    │                    │  POSTGRESQL DB   │
│  - Message queue │                    │  - Decisions     │
│  - Caching       │                    │  - Outcomes      │
└──────────────────┘                    │  - Performance   │
                                        └──────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  TRADINGAGENTS CORE                          │
│  - Director Agent                                            │
│  - Analyst Pipeline                                          │
│  - Portfolio Manager                                         │
│  - Risk Monitor                                              │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│               BROKER INTEGRATION                             │
│  - Interactive Brokers / Alpaca / Paper Trading             │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│               MONITORING & ALERTS                            │
│  - Grafana dashboards                                        │
│  - Prometheus metrics                                        │
│  - Email/Slack notifications                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start: Docker Deployment

### Step 1: Create docker-compose.yml

```yaml
# docker-compose.yml

version: '3.8'

services:
  # Redis for message broker and caching
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # PostgreSQL for performance tracking
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: tradingagents
      POSTGRES_USER: trading
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # FastAPI application
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ALPHA_VANTAGE_API_KEY=${ALPHA_VANTAGE_API_KEY}
      - DATABASE_URL=postgresql://trading:${DB_PASSWORD}@postgres:5432/tradingagents
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
      - postgres
    volumes:
      - ./tradingagents:/app/tradingagents
      - ./results:/app/results

  # Celery worker for background tasks
  celery_worker:
    build: .
    command: celery -A tradingagents.tasks worker --loglevel=info
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ALPHA_VANTAGE_API_KEY=${ALPHA_VANTAGE_API_KEY}
      - DATABASE_URL=postgresql://trading:${DB_PASSWORD}@postgres:5432/tradingagents
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
      - postgres
    volumes:
      - ./tradingagents:/app/tradingagents
      - ./results:/app/results

  # Celery beat for scheduled tasks
  celery_beat:
    build: .
    command: celery -A tradingagents.tasks beat --loglevel=info
    environment:
      - DATABASE_URL=postgresql://trading:${DB_PASSWORD}@postgres:5432/tradingagents
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
      - postgres

  # Grafana for monitoring
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - postgres

volumes:
  redis_data:
  postgres_data:
  grafana_data:
```

### Step 2: Create .env file

```bash
# .env

# API Keys
OPENAI_API_KEY=sk-...
ALPHA_VANTAGE_API_KEY=...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DB_PASSWORD=secure_password_here

# Grafana
GRAFANA_PASSWORD=admin

# Broker (if using real trading)
IBKR_USERNAME=...
IBKR_PASSWORD=...

# Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
EMAIL_FROM=trading@yourdomain.com
EMAIL_TO=you@yourdomain.com
```

### Step 3: Create Celery Tasks

```python
# tradingagents/tasks.py

from celery import Celery
from celery.schedules import crontab
import os

# Initialize Celery
app = Celery('tradingagents')
app.config_from_object({
    'broker_url': os.getenv('REDIS_URL', 'redis://localhost:6379'),
    'result_backend': os.getenv('REDIS_URL', 'redis://localhost:6379'),
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json',
    'timezone': 'America/New_York',
    'enable_utc': True,
})

# Scheduled tasks
app.conf.beat_schedule = {
    # Daily 6:00 AM - Regime detection
    'detect-market-regime': {
        'task': 'tradingagents.tasks.detect_regime',
        'schedule': crontab(hour=6, minute=0),
    },
    # Daily 6:30 AM - Universe screening
    'screen-universe': {
        'task': 'tradingagents.tasks.screen_universe',
        'schedule': crontab(hour=6, minute=30),
    },
    # Daily 7:00 AM - Start analysis pipeline
    'analyze-opportunities': {
        'task': 'tradingagents.tasks.analyze_opportunities',
        'schedule': crontab(hour=7, minute=0),
    },
    # Daily 9:15 AM - Portfolio optimization
    'optimize-portfolio': {
        'task': 'tradingagents.tasks.optimize_portfolio',
        'schedule': crontab(hour=9, minute=15),
    },
    # Daily 9:30 AM - Execute trades
    'execute-trades': {
        'task': 'tradingagents.tasks.execute_trades',
        'schedule': crontab(hour=9, minute=30),
    },
    # Every 5 minutes during trading hours - Monitor positions
    'monitor-positions': {
        'task': 'tradingagents.tasks.monitor_positions',
        'schedule': crontab(minute='*/5', hour='9-16', day_of_week='mon-fri'),
    },
    # Daily 4:00 PM - Daily reflection
    'daily-reflection': {
        'task': 'tradingagents.tasks.daily_reflection',
        'schedule': crontab(hour=16, minute=0),
    },
}

@app.task
def detect_regime():
    """Detect current market regime."""
    from tradingagents.portfolio.regime_detector import MarketRegimeDetector
    detector = MarketRegimeDetector()
    regime = detector.detect_regime("SPY", date="today")
    # Store in cache
    return regime

@app.task
def screen_universe():
    """Screen universe for opportunities."""
    from tradingagents.portfolio.universe_screener import UniverseScreener
    screener = UniverseScreener()
    candidates = screener.screen(
        universe=get_sp500_tickers(),
        top_n=50
    )
    # Store in cache
    return candidates

@app.task
def analyze_opportunities():
    """Analyze screened opportunities."""
    from tradingagents.graph.trading_graph import TradingAgentsGraph
    # Get candidates from cache
    # For each candidate, run analysis
    # Store results
    pass

@app.task
def optimize_portfolio():
    """Optimize portfolio weights."""
    from tradingagents.portfolio.optimizer import PortfolioOptimizer
    # Get analyzed opportunities
    # Run optimization
    # Return target portfolio
    pass

@app.task
def execute_trades():
    """Execute trading decisions."""
    from tradingagents.execution.executor import TradeExecutor
    # Get target portfolio
    # Generate trades
    # Execute via broker
    pass

@app.task
def monitor_positions():
    """Monitor positions for stop-loss/take-profit."""
    from tradingagents.portfolio.risk_monitor import PortfolioRiskMonitor
    monitor = PortfolioRiskMonitor()
    # Check all positions
    # Trigger actions if needed
    pass

@app.task
def daily_reflection():
    """Daily performance reflection and learning."""
    from tradingagents.graph.reflection import EnhancedReflector
    reflector = EnhancedReflector()
    # Analyze day's performance
    # Update agent memories
    # Update meta-learner
    pass
```

### Step 4: Launch

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check Celery worker is running
docker-compose logs celery_worker

# Check scheduled tasks
docker-compose exec celery_worker celery -A tradingagents.tasks inspect scheduled

# Access Grafana dashboard
# → http://localhost:3000 (admin / <GRAFANA_PASSWORD>)
```

---

## Monitoring & Alerts

### Grafana Dashboards

Create dashboards for:
1. **Portfolio Performance**
   - Equity curve
   - Daily returns
   - Sharpe ratio
   - Max drawdown

2. **Trading Activity**
   - Trades per day
   - Win rate
   - Average profit/loss
   - Position counts

3. **System Health**
   - Task completion times
   - Error rates
   - API call counts
   - Cost tracking

4. **Risk Metrics**
   - Portfolio VaR
   - Beta to SPY
   - Sector exposure
   - Correlation matrix

### Alerts

```python
# tradingagents/notifications/alerter.py

class Alerter:
    """Send alerts for critical events."""

    def send_alert(self, alert_type: str, message: str, severity: str = "medium"):
        """
        Send multi-channel alerts.

        Channels:
        - Email for HIGH severity
        - Slack for ALL severities
        - SMS for CRITICAL (via Twilio)
        """
        if severity == "critical":
            self._send_sms(message)
            self._send_email(message)
            self._send_slack(message, color="danger")
        elif severity == "high":
            self._send_email(message)
            self._send_slack(message, color="warning")
        else:
            self._send_slack(message, color="good")

    def alert_on_large_loss(self, loss_pct: float):
        """Alert if position loss exceeds threshold."""
        if loss_pct > 0.10:  # 10% loss
            self.send_alert(
                "position_loss",
                f"Large position loss detected: {loss_pct:.2%}",
                severity="high"
            )

    def alert_on_system_error(self, error: Exception):
        """Alert on system errors."""
        self.send_alert(
            "system_error",
            f"System error: {str(error)}",
            severity="critical"
        )
```

---

## Security Considerations

### 1. API Key Management
- **Never commit API keys to git**
- Use environment variables or secrets manager
- Rotate keys regularly
- Use separate keys for dev/staging/prod

### 2. Brokerage Security
- Enable two-factor authentication
- Use read-only API keys for monitoring
- Implement trade size limits
- Require manual approval for large trades (optional)

### 3. Code Validation
- If using Text2Code (Phase 4), strict sandboxing
- No eval/exec in production
- Validate all generated code
- Whitelist allowed imports

### 4. Database Security
- Strong passwords
- No direct external access
- Regular backups
- Encrypted at rest

---

## Cost Management

### LLM API Costs

**Estimated Daily Costs:**
- Screening 50 stocks: $0.50
- Deep analysis 10 positions: $2.00
- Portfolio optimization: $0.30
- Risk monitoring: $0.20
- **Total daily: ~$3.00**
- **Monthly: ~$60-90**

**Cost Optimization:**
- Use gpt-4o-mini for routine tasks
- Cache analyst reports (don't re-analyze same stock same day)
- Use Director Agent to reduce unnecessary analyses
- Batch API calls where possible

### Data API Costs

**Alpha Vantage:**
- Free tier: 25 req/day (not enough)
- Premium: $50/mo for 1200 req/day (sufficient)

**Alternative: yfinance (free) for most data**

---

## Backup & Recovery

### Daily Backups

```bash
# Backup database
docker-compose exec postgres pg_dump -U trading tradingagents > backup_$(date +%Y%m%d).sql

# Backup results
tar -czf results_backup_$(date +%Y%m%d).tar.gz results/

# Upload to S3 (optional)
aws s3 cp backup_$(date +%Y%m%d).sql s3://my-trading-backups/
```

### Disaster Recovery

1. **Database corruption:** Restore from latest backup
2. **Bad trades:** Emergency stop-all script
3. **API outage:** Fallback to cached data + hold positions
4. **System crash:** Automatic restart via Docker

---

## Performance Tuning

### 1. Caching Strategy

```python
# tradingagents/cache.py

import redis
import json

class CacheManager:
    """Manage Redis caching for performance."""

    def __init__(self):
        self.redis_client = redis.from_url(os.getenv('REDIS_URL'))

    def cache_analyst_report(
        self,
        ticker: str,
        analyst_type: str,
        report: str,
        ttl: int = 3600  # 1 hour
    ):
        """Cache analyst reports to avoid redundant analysis."""
        key = f"report:{ticker}:{analyst_type}:{date.today()}"
        self.redis_client.setex(key, ttl, json.dumps(report))

    def get_cached_report(self, ticker: str, analyst_type: str) -> str:
        """Retrieve cached report if fresh."""
        key = f"report:{ticker}:{analyst_type}:{date.today()}"
        cached = self.redis_client.get(key)
        return json.loads(cached) if cached else None
```

### 2. Parallel Processing

```python
# Use asyncio for parallel analyst execution

import asyncio

async def run_analysts_parallel(analysts, state):
    """Run multiple analysts in parallel."""
    tasks = [analyst.run_async(state) for analyst in analysts]
    results = await asyncio.gather(*tasks)
    return results
```

---

## Testing in Production

### Paper Trading First

**Always test with paper trading before live money:**

```python
# tradingagents/execution/executor.py

class TradeExecutor:
    def __init__(self, mode: str = "paper"):
        """
        Modes:
        - paper: Simulated trading (no real money)
        - live: Real trading

        Start with 'paper' for at least 1 month!
        """
        self.mode = mode

    def place_order(self, order):
        if self.mode == "paper":
            # Simulate order execution
            return self._simulate_order(order)
        else:
            # Real broker execution
            return self._real_order(order)
```

**Paper Trading Checklist:**
- [ ] Run for minimum 1 month
- [ ] Verify positive returns
- [ ] Check Sharpe ratio > 1.5
- [ ] Max drawdown < 15%
- [ ] No system errors
- [ ] Cost projections reasonable
- [ ] All alerts working

---

## Going Live

### Pre-Launch Checklist

- [ ] Phases 1-6 fully implemented and tested
- [ ] 1+ months successful paper trading
- [ ] All monitoring and alerts configured
- [ ] Backup and recovery tested
- [ ] Cost budget approved
- [ ] Start with small capital (10-20% of total)
- [ ] Manual kill switch tested
- [ ] Email/Slack notifications working
- [ ] Brokerage API limits verified
- [ ] Tax reporting plan in place

### Launch Day

1. **Fund account** with initial capital (start small!)
2. **Enable live mode** in configuration
3. **Monitor closely** for first 2 weeks
4. **Gradually increase** capital allocation
5. **Review weekly** performance and costs

---

## Ongoing Maintenance

### Daily
- [ ] Check morning screening completed
- [ ] Verify trades executed as expected
- [ ] Monitor for alerts

### Weekly
- [ ] Review performance metrics
- [ ] Check cost tracking
- [ ] Review any errors in logs

### Monthly
- [ ] Full performance review
- [ ] Meta-learner insights review
- [ ] Update agent configurations based on learnings
- [ ] Database maintenance

### Quarterly
- [ ] Comprehensive backtest with new data
- [ ] Review and update risk parameters
- [ ] Evaluate adding new phases/features
- [ ] Tax preparation

---

## Troubleshooting

### Common Issues

**1. API Rate Limits**
```
Solution: Implement exponential backoff, use caching, upgrade API tier
```

**2. LLM Timeouts**
```
Solution: Increase timeout, retry with exponential backoff, use faster model
```

**3. Database Lock**
```
Solution: Use connection pooling, reduce concurrent writes
```

**4. Celery Tasks Not Running**
```bash
# Check beat scheduler is running
docker-compose logs celery_beat

# Check worker is processing
docker-compose exec celery_worker celery -A tradingagents.tasks inspect active
```

**5. Positions Not Closing**
```
Solution: Check broker connection, manual override if needed
```

---

## Emergency Procedures

### Emergency Stop

```python
# tradingagents/emergency_stop.py

def emergency_stop_all():
    """
    EMERGENCY: Close all positions immediately.

    Use when:
    - System malfunction detected
    - Market crash (>5% down)
    - Critical bug discovered
    """
    from tradingagents.execution.executor import TradeExecutor

    executor = TradeExecutor(mode="live")

    # Get all positions
    positions = executor.get_positions()

    # Close everything at market
    for ticker, position in positions.items():
        executor.place_order({
            'ticker': ticker,
            'action': 'SELL',
            'quantity': position.quantity,
            'type': 'MARKET',
            'reason': 'EMERGENCY_STOP'
        })

    # Send critical alert
    send_alert("ALL POSITIONS CLOSED - EMERGENCY STOP", severity="critical")

# Run with: python -m tradingagents.emergency_stop
```

---

## Conclusion

You now have a fully autonomous trading system running 24/7!

**Key Success Factors:**
1. Start with paper trading
2. Monitor closely initially
3. Scale capital gradually
4. Keep costs under control
5. Maintain backups
6. Trust the system (but verify!)

**Remember:** Even with full automation, periodic human oversight is recommended for:
- Major system upgrades
- Extreme market conditions
- Regulatory changes
- Tax planning

---

**Next:** Review [11_MONITORING_OPERATIONS.md](11_MONITORING_OPERATIONS.md) for detailed monitoring best practices.

**Last Updated:** 2025-10-18
