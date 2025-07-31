#!/usr/bin/env python3
"""
Launch script for OptCred Fixed Version
"""

import subprocess
import sys
import os

def main():
    try:
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        print("🚀 Starting OptCred Fixed Version...")
        
        # Launch Streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'main_fixed.py'])
        
    except KeyboardInterrupt:
        print("\n👋 OptCred stopped by user")
    except Exception as e:
        print(f"❌ Error starting OptCred: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()