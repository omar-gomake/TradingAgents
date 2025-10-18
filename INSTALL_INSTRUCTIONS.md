# Installation Instructions for Backtesting Framework

## Quick Fix

The backtesting framework is fully implemented, but you need to install the missing dependencies:

```bash
# Install the missing packages
pip install typer numpy matplotlib python-dotenv

# OR reinstall all dependencies from requirements.txt
pip install -r requirements.txt
```

## Verify Installation

After installing, verify it works:

```bash
python -m cli.main --help
```

You should see `backtest` listed as a command.

## Then Try

```bash
# Interactive backtesting
python -m cli.main backtest run

# Or run an example
python examples/simple_backtest.py
```

## Full Setup (If Starting Fresh)

If you're setting up from scratch or having issues:

```bash
# 1. Navigate to project directory
cd /Users/omarsabbah/Desktop/TradingAgents

# 2. Install all dependencies
pip install -r requirements.txt

# 3. Set up environment variables
export OPENAI_API_KEY="your-openai-key"
export ALPHA_VANTAGE_API_KEY="your-alpha-vantage-key"

# Or create a .env file:
echo "OPENAI_API_KEY=your-openai-key" > .env
echo "ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key" >> .env

# 4. Verify installation
python -m cli.main --help
```

## What's Installed

The backtesting framework includes:

✅ **Core Module** (`tradingagents/backtesting/`)

- BacktestEngine - Main backtesting engine
- BacktestConfig - Configuration class
- BacktestResults - Performance analytics
- BacktestVisualizer - Charting and visualization
- TradingAgentsStrategy - Backtrader integration

✅ **CLI Commands** (`cli/backtest.py`)

- `python -m cli.main backtest run` - Interactive backtesting
- `python -m cli.main backtest compare` - Compare tickers

✅ **Examples** (`examples/`)

- `simple_backtest.py` - Basic example
- `portfolio_backtest.py` - Multi-ticker portfolio
- `advanced_backtest.py` - Advanced analysis

✅ **Documentation**

- `README.md` - Updated with backtesting section
- `docs/BACKTESTING.md` - Complete guide
- `BACKTESTING_QUICKSTART.md` - Quick start
- `IMPLEMENTATION_SUMMARY.md` - Technical details

## Troubleshooting

### Error: "No module named 'typer'"

**Fix:** `pip install typer`

### Error: "No module named 'numpy'"

**Fix:** `pip install numpy`

### Error: "No module named 'matplotlib'"

**Fix:** `pip install matplotlib`

### Install All at Once

**Fix:** `pip install -r requirements.txt`

### Still Having Issues?

Check your Python version:

```bash
python --version  # Should be 3.10 or higher
```

Check which pip is being used:

```bash
which pip
which python
```

Make sure you're using the same Python environment for installation and running.

## Next Steps After Installation

1. **Verify it works:**

   ```bash
   python -m cli.main --help
   ```

2. **Try the simple example:**

   ```bash
   python examples/simple_backtest.py
   ```

3. **Read the guides:**

   - Quick start: `BACKTESTING_QUICKSTART.md`
   - Full guide: `docs/BACKTESTING.md`

4. **Run your first backtest:**
   ```bash
   python -m cli.main backtest run
   ```

---

**The framework is ready - you just need to install the dependencies!** 🚀
