#!/usr/bin/env python3
"""Quick test runner"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run_tests import TestSuite

def main():
    print("🧪 Quick Test Runner")
    suite = TestSuite()
    suite.run_all_tests()

if __name__ == "__main__":
    main()