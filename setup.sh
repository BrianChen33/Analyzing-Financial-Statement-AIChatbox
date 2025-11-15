#!/bin/bash

# Quick start script for Financial Statement AI Chatbox

echo "========================================"
echo "Financial Statement AI Chatbox Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check for .env file
echo ""
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✓ Created .env file. Please edit it and add your OpenAI API key."
    echo ""
    echo "To add your API key:"
    echo "  1. Get your key from: https://platform.openai.com/api-keys"
    echo "  2. Edit .env file and replace 'your-api-key-here' with your actual key"
else
    echo "✓ .env file exists"
fi

# Create uploads directory
mkdir -p uploads
echo "✓ Uploads directory ready"

# Run tests
echo ""
echo "Running tests..."
python -m pytest tests/ -v

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "✓ Setup complete!"
    echo "========================================"
    echo ""
    echo "Quick Start Options:"
    echo ""
    echo "1. Web Interface (Recommended):"
    echo "   streamlit run app.py"
    echo ""
    echo "2. Command Line:"
    echo "   python src/chatbot.py <path-to-pdf>"
    echo ""
    echo "3. Run Examples:"
    echo "   python examples/basic_usage.py"
    echo "   python examples/advanced_analysis.py"
    echo ""
    echo "4. Run Tests:"
    echo "   pytest tests/ -v"
    echo ""
else
    echo "❌ Tests failed. Please check the error messages above."
    exit 1
fi
