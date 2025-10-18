#!/bin/bash
# TradingAgents Environment Setup Helper

echo "=========================================="
echo "TradingAgents API Keys Setup"
echo "=========================================="
echo ""

# Check if .env exists
if [ -f ".env" ]; then
    echo "✅ .env file already exists"
    echo ""
    echo "Current keys status:"
    source venv/bin/activate 2>/dev/null
    python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
openai = os.getenv('OPENAI_API_KEY', '')
alpha = os.getenv('ALPHA_VANTAGE_API_KEY', '')
print(f'  OpenAI: {"✅ Set" if openai and openai != "your_openai_api_key_here" else "❌ Not set"}')
print(f'  Alpha Vantage: {"✅ Set" if alpha and alpha != "your_alpha_vantage_key_here" else "❌ Not set"}')
" 2>/dev/null || echo "  (Install python-dotenv to check: pip install python-dotenv)"
    echo ""
    echo "To edit: nano .env  (or: code .env)"
    exit 0
fi

echo "Creating .env file..."
cat > .env << 'EOF'
# TradingAgents API Keys
# Get OpenAI key: https://platform.openai.com/api-keys
# Get Alpha Vantage key: https://www.alphavantage.co/support/#api-key

OPENAI_API_KEY=your_openai_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
EOF

echo "✅ Created .env file"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Get your API keys:"
echo "   OpenAI: https://platform.openai.com/api-keys"
echo "   Alpha Vantage: https://www.alphavantage.co/support/#api-key"
echo ""
echo "2. Edit .env file:"
echo "   nano .env"
echo "   (or: code .env if using VS Code)"
echo ""
echo "3. Replace 'your_xxx_key_here' with actual keys"
echo ""
echo "4. Run test:"
echo "   source venv/bin/activate"
echo "   python examples/one_day_test.py"
echo ""
echo "=========================================="
echo "Need help? See SETUP_API_KEYS.md"
echo "=========================================="

