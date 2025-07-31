"""
Setup Script for OptCred Fixes
Prepares your environment and verifies everything is ready
Version STABLE - Kaizen Business Support
"""

import os
import sys
import shutil
from datetime import datetime

def setup_optcred_fixes():
    """Setup the OptCred fixes environment"""
    
    print("🔧 OptCred Fixes Setup")
    print("=" * 50)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Step 1: Backup original files
    print("📋 Step 1: Backing up original files...")
    backup_files(current_dir)
    
    # Step 2: Create required directories
    print("📋 Step 2: Creating required directories...")
    create_directories(current_dir)
    
    # Step 3: Verify file structure
    print("📋 Step 3: Verifying file structure...")
    verify_structure(current_dir)
    
    # Step 4: Check dependencies
    print("📋 Step 4: Checking dependencies...")
    check_dependencies()
    
    # Step 5: Create launch scripts
    print("📋 Step 5: Creating convenience scripts...")
    create_launch_scripts(current_dir)
    
    print("\n✅ Setup completed successfully!")
    print_next_steps()

def backup_files(base_dir):
    """Backup original files"""
    
    backup_dir = os.path.join(base_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    files_to_backup = [
        'main.py',
        'session_manager.py', 
        'unified_input_page.py'
    ]
    
    existing_files = [f for f in files_to_backup if os.path.exists(os.path.join(base_dir, f))]
    
    if existing_files:
        os.makedirs(backup_dir, exist_ok=True)
        
        for file_name in existing_files:
            src = os.path.join(base_dir, file_name)
            dst = os.path.join(backup_dir, file_name)
            shutil.copy2(src, dst)
            print(f"  ✅ Backed up: {file_name}")
        
        print(f"  📁 Backup location: {backup_dir}")
    else:
        print("  ℹ️  No existing files to backup")

def create_directories(base_dir):
    """Create required directories"""
    
    directories = [
        'components',
        'utils',
        'tests',
        'logs'
    ]
    
    for dir_name in directories:
        dir_path = os.path.join(base_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        
        # Create __init__.py files for Python packages
        if dir_name in ['components', 'utils']:
            init_file = os.path.join(dir_path, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write(f'"""{dir_name.title()} package for OptCred"""\n')
        
        print(f"  ✅ Directory: {dir_name}")

def verify_structure(base_dir):
    """Verify the file structure is correct"""
    
    required_files = {
        'app_controller.py': 'Core application controller',
        'main_fixed.py': 'Fixed main application',
        'unified_input_page_fixed.py': 'Fixed input page',
        'components/stable_file_upload.py': 'Stable file upload component',
        'utils/import_manager.py': 'Import manager utility',
        'run_tests.py': 'Test suite runner',
        'test_guide.md': 'Testing guide'
    }
    
    missing_files = []
    
    for file_path, description in required_files.items():
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"  ✅ {file_path} - {description}")
        else:
            missing_files.append(file_path)
            print(f"  ❌ {file_path} - MISSING")
    
    if missing_files:
        print(f"\n⚠️  Missing files: {missing_files}")
        print("Please ensure all files from the fix are present.")
        return False
    
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    
    required_packages = [
        ('streamlit', 'Main framework'),
        ('pandas', 'Data manipulation'),
        ('numpy', 'Numerical computing'),  
        ('openpyxl', 'Excel file handling'),
        ('plotly', 'Interactive charts'),
        ('datetime', 'Date/time utilities (built-in)'),
        ('hashlib', 'Hashing utilities (built-in)'),
        ('threading', 'Thread management (built-in)')
    ]
    
    missing_packages = []
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package} - {description}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package} - MISSING - {description}")
    
    if missing_packages:
        print(f"\n📦 Install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def create_launch_scripts(base_dir):
    """Create convenience scripts for launching the app"""
    
    # Windows batch file
    batch_content = """@echo off
echo Starting OptCred Fixed Version...
cd /d "%~dp0"
streamlit run main_fixed.py
pause"""
    
    batch_path = os.path.join(base_dir, 'start_optcred.bat')
    with open(batch_path, 'w') as f:
        f.write(batch_content)
    
    # Python launch script
    python_content = """#!/usr/bin/env python3
\"\"\"
Launch script for OptCred Fixed Version
\"\"\"

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
        print("\\n👋 OptCred stopped by user")
    except Exception as e:
        print(f"❌ Error starting OptCred: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()"""
    
    python_path = os.path.join(base_dir, 'start_optcred.py')
    with open(python_path, 'w') as f:
        f.write(python_content)
    
    # Test runner script
    test_content = """#!/usr/bin/env python3
\"\"\"Quick test runner\"\"\"

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
    main()"""
    
    test_path = os.path.join(base_dir, 'quick_test.py')
    with open(test_path, 'w') as f:
        f.write(test_content)
    
    print(f"  ✅ start_optcred.bat - Windows launcher")
    print(f"  ✅ start_optcred.py - Python launcher") 
    print(f"  ✅ quick_test.py - Quick test runner")

def print_next_steps():
    """Print next steps for the user"""
    
    print("\n🎯 NEXT STEPS:")
    print("=" * 50)
    print("1. 🧪 Run tests to verify everything works:")
    print("   python run_tests.py")
    print()
    print("2. 🚀 Launch the fixed application:")
    print("   python start_optcred.py")
    print("   OR")
    print("   streamlit run main_fixed.py")
    print()
    print("3. 📖 Follow the comprehensive test guide:")
    print("   Open test_guide.md for detailed testing instructions")
    print()
    print("4. 🎉 If all tests pass, your OptCred is now STABLE!")
    print()
    print("🆘 Need help?")
    print("- Check test_guide.md for troubleshooting")
    print("- Run quick_test.py for rapid diagnostics")
    print("- Contact: support@kaizen-corporation.com")

def main():
    """Main setup function"""
    
    try:
        setup_optcred_fixes()
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("Please check the error and try again.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()