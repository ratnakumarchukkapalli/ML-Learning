#!/bin/bash

# ML Learning Day 1 Setup Script for macOS
# This script creates a virtual environment and launches the notebook

echo "🚀 Setting up your Day 1 ML Learning Environment..."
echo "=" * 60

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.7+ first."
    echo "💡 Install with: brew install python"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "ml_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv ml_env
    echo "✅ Virtual environment created!"
else
    echo "✅ Virtual environment already exists!"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ml_env/bin/activate

# Upgrade pip
echo "📈 Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
echo "📚 Installing required packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ All packages installed successfully!"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

# Check if notebook exists
if [ ! -f "day1_data_loading_and_eda.ipynb" ]; then
    echo "❌ Day 1 notebook not found!"
    exit 1
fi

echo ""
echo "📚 Day 1 Learning Tips:"
echo "   • Read each markdown section carefully"
echo "   • Run cells one by one to understand the output"
echo "   • Experiment with the code - try changing parameters!"
echo "   • Take notes on concepts you find challenging"
echo "   • Don't rush - understanding is more important than speed"

echo ""
echo "🎯 Today's Goal: Complete thorough EDA of the Titanic dataset"
echo "⏱️  Estimated time: 1.5-2 hours"
echo "📈 What's next: Tomorrow we'll clean data and engineer features"

echo ""
echo "🌐 Launching Jupyter Notebook..."
echo "📝 Opening day1_data_loading_and_eda.ipynb"
echo ""
echo "=" * 60
echo "✨ Happy Learning! Press Ctrl+C to stop Jupyter when done."
echo "=" * 60

# Launch Jupyter notebook
jupyter notebook day1_data_loading_and_eda.ipynb

# Deactivate virtual environment when done
deactivate
