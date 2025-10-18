# API Keys Setup Guide

## Quick Setup (30 seconds)

```bash
cd /Users/omarsabbah/Desktop/TradingAgents

# Create .env file
cat > .env << 'EOF'
OPENAI_API_KEY=your_openai_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
EOF

# Edit with your actual keys
nano .env  # or: code .env
```

## Where to Get API Keys

### 1. OpenAI API Key (REQUIRED)

**Get it here**: https://platform.openai.com/api-keys

**Steps**:

1. Create OpenAI account (if you don't have one)
2. Go to API keys page
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)
5. Paste into `.env` file

**Cost**: ~$0.01-0.10 per backtest day (using gpt-4o-mini)

### 2. Alpha Vantage API Key (OPTIONAL)

**Get it here**: https://www.alphavantage.co/support/#api-key

**Steps**:

1. Enter your email
2. Check your email for the free API key
3. Copy the key
4. Paste into `.env` file

**Free Tier**: 60 requests/minute (plenty for testing)
**Used for**: Fundamental data, news, insider transactions

## Verify Setup

After creating `.env` file, verify it's loaded:

```bash
cd /Users/omarsabbah/Desktop/TradingAgents
source venv/bin/activate
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OpenAI key set:', bool(os.getenv('OPENAI_API_KEY'))); print('Alpha Vantage key set:', bool(os.getenv('ALPHA_VANTAGE_API_KEY')))"
```

Should output:

```
OpenAI key set: True
Alpha Vantage key set: True
```

## Test the Backtest

Once keys are set, run:

```bash
python examples/one_day_test.py
```

This will complete in ~2-3 minutes and validate everything works!

## Troubleshooting

### Error: "api_key client option must be set"

- Your `.env` file doesn't exist or keys are not set
- Make sure file is named exactly `.env` (not `.env.txt`)
- Make sure you replaced `your_openai_api_key_here` with actual key

### Error: "Invalid API key"

- Check for extra spaces or quotes around the key
- Key should be plain text: `OPENAI_API_KEY=sk-abc123...`
- No quotes needed

### Want to test without Alpha Vantage?

- You can skip Alpha Vantage temporarily
- Only use market analyst (technical analysis only)
- Set in config: `fundamental_data: yfinance` and `news_data: yfinance`

## Security

✅ `.env` is in `.gitignore` - your keys won't be committed
✅ Never share your `.env` file
✅ Rotate keys if accidentally exposed
