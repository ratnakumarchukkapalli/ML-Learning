#!/usr/bin/env python3
"""
Quick launcher for Day 1 ML Learning Notebook
Run this script to launch Jupyter and open the Day 1 notebook automatically
"""

import subprocess
import sys
import os
import webbrowser
import time

def check_requirements():
    """Check if required packages are installed"""
    required_packages = ['jupyter', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'scikit-learn']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Please install them with: pip install -r requirements.txt")
        return False
    return True

def launch_notebook():
    """Launch Jupyter notebook and open Day 1 notebook"""
    print("🚀 Starting your Day 1 ML Learning Journey!")
    print("=" * 50)
    
    if not check_requirements():
        return
    
    # Check if the notebook exists
    notebook_path = "day1_data_loading_and_eda.ipynb"
    if not os.path.exists(notebook_path):
        print(f"❌ Notebook not found: {notebook_path}")
        return
    
    print("✅ All requirements satisfied!")
    print("🔧 Launching Jupyter Notebook...")
    
    # Launch Jupyter notebook
    try:
        # Start Jupyter in the background
        jupyter_process = subprocess.Popen([
            sys.executable, "-m", "jupyter", "notebook", 
            "--notebook-dir=.", 
            "--browser=false"  # We'll open browser manually
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for Jupyter to start
        time.sleep(3)
        
        # Open the specific notebook
        notebook_url = f"http://localhost:8888/notebooks/{notebook_path}"
        print(f"🌐 Opening notebook: {notebook_url}")
        webbrowser.open(notebook_url)
        
        print("\n📚 Day 1 Learning Tips:")
        print("   • Read each markdown section carefully")
        print("   • Run cells one by one to understand the output")
        print("   • Experiment with the code - try changing parameters!")
        print("   • Take notes on concepts you find challenging")
        print("   • Don't rush - understanding is more important than speed")
        
        print(f"\n🎯 Today's Goal: Complete thorough EDA of the Titanic dataset")
        print(f"⏱️  Estimated time: 1.5-2 hours")
        print(f"📈 What's next: Tomorrow we'll clean data and engineer features")
        
        print("\n" + "=" * 50)
        print("✨ Happy Learning! Press Ctrl+C to stop Jupyter when done.")
        print("=" * 50)
        
        # Keep the script running until user stops it
        try:
            jupyter_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping Jupyter...")
            jupyter_process.terminate()
            
    except Exception as e:
        print(f"❌ Error launching Jupyter: {e}")
        print("💡 Try running manually: jupyter notebook")

if __name__ == "__main__":
    launch_notebook()
