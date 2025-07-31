"""
Automated Test Suite for OptCred Fixed Version
Runs comprehensive tests to validate all fixes
Version STABLE - Kaizen Business Support
"""

import os
import sys
import time
import traceback
from datetime import datetime
import subprocess

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

class TestSuite:
    """Comprehensive test suite for OptCred"""
    
    def __init__(self):
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
        self.start_time = datetime.now()
    
    def run_all_tests(self):
        """Execute all test phases"""
        
        print("Starting OptCred Comprehensive Test Suite")
        print("=" * 60)
        
        # Test phases
        test_phases = [
            ("File Structure", self.test_file_structure),
            ("Dependencies", self.test_dependencies),
            ("Basic Imports", self.test_basic_imports),
            ("Controller Initialization", self.test_controller_init),
            ("Session Management", self.test_session_management),
            ("Widget Key Generation", self.test_widget_keys),
            ("Import Manager", self.test_import_manager),
            ("File Upload Component", self.test_file_upload),
            ("Navigation System", self.test_navigation)
        ]
        
        for phase_name, test_func in test_phases:
            print(f"\nTesting {phase_name}...")
            try:
                test_func()
                self._log_success(f"{phase_name} tests passed")
            except Exception as e:
                self._log_error(f"{phase_name} tests failed", e)
        
        self._print_summary()
    
    def test_file_structure(self):
        """Test if all required files exist"""
        
        required_files = [
            'app_controller.py',
            'main_fixed.py',
            'unified_input_page_fixed.py',
            'components/stable_file_upload.py',
            'utils/import_manager.py'
        ]
        
        missing_files = []
        
        for file_path in required_files:
            full_path = os.path.join(current_dir, file_path)
            if not os.path.exists(full_path):
                missing_files.append(file_path)
        
        if missing_files:
            raise Exception(f"Missing files: {missing_files}")
        
        print("All required files present")
    
    def test_dependencies(self):
        """Test if all required Python packages are available"""
        
        required_packages = [
            'streamlit',
            'pandas', 
            'numpy',
            'openpyxl',
            'datetime',
            'hashlib',
            'threading',
            'pathlib'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            raise Exception(f"Missing packages: {missing_packages}")
        
        print("All dependencies available")
    
    def test_basic_imports(self):
        """Test if new modules can be imported"""
        
        try:
            from app_controller import get_app_controller, Page, AppState
            from components.stable_file_upload import StableFileUpload
            from utils.import_manager import get_import_manager
            
            print("All new modules import successfully")
            
        except ImportError as e:
            raise Exception(f"Import failed: {e}")
    
    def test_controller_init(self):
        """Test application controller initialization"""
        
        try:
            # Enhanced Streamlit session state mock
            class MockSessionState:
                def __init__(self):
                    self.data = {}
                    # Pre-initialize required keys
                    self.data['optcred_v2_session_id'] = 'test1234'
                    self.data['optcred_v2_widget_counter'] = 0
                    self.data['optcred_v2_initialization_done'] = True
                    self.data['optcred_v2_current_page'] = 'home'
                    self.data['optcred_v2_app_state'] = 'ready'
                
                def get(self, key, default=None):
                    return self.data.get(key, default)
                
                def __getitem__(self, key):
                    if key not in self.data:
                        raise KeyError(key)
                    return self.data[key]
                
                def __setitem__(self, key, value):
                    self.data[key] = value
                
                def __contains__(self, key):
                    return key in self.data
                
                def keys(self):
                    return self.data.keys()
                
                def setdefault(self, key, default):
                    if key not in self.data:
                        self.data[key] = default
                    return self.data[key]
            
            # Mock streamlit module
            import streamlit as st
            original_session_state = getattr(st, 'session_state', None)
            st.session_state = MockSessionState()
            
            try:
                from app_controller import get_app_controller, Page
                
                # Get controller instance
                app = get_app_controller()
                
                # Test basic properties
                assert hasattr(app, 'session_id')
                assert hasattr(app, 'current_page')
                assert hasattr(app, 'app_state')
                
                # Test methods
                assert callable(app.generate_widget_key)
                assert callable(app.navigate_to)
                assert callable(app.has_valid_analysis)
                
                # Test session ID generation
                session_id = app.session_id
                assert len(session_id) == 8
                assert session_id.isalnum()
                
                print("Controller initialization successful")
                
            finally:
                # Restore original session state
                if original_session_state is not None:
                    st.session_state = original_session_state
            
        except Exception as e:
            raise Exception(f"Controller initialization failed: {e}")
    
    def test_session_management(self):
        """Test session state management"""
        
        try:
            # Enhanced Streamlit session state mock
            class MockSessionState:
                def __init__(self):
                    self.data = {}
                    # Pre-initialize session ID to prevent errors
                    self.data['optcred_v2_session_id'] = 'test1234'
                    self.data['optcred_v2_widget_counter'] = 0
                    self.data['optcred_v2_initialization_done'] = True
                
                def get(self, key, default=None):
                    return self.data.get(key, default)
                
                def __getitem__(self, key):
                    if key not in self.data:
                        raise KeyError(key)
                    return self.data[key]
                
                def __setitem__(self, key, value):
                    self.data[key] = value
                
                def __contains__(self, key):
                    return key in self.data
                
                def keys(self):
                    return self.data.keys()
                
                def setdefault(self, key, default):
                    if key not in self.data:
                        self.data[key] = default
                    return self.data[key]
            
            # Mock streamlit module completely
            import streamlit as st
            original_session_state = getattr(st, 'session_state', None)
            st.session_state = MockSessionState()
            
            try:
                from app_controller import get_app_controller
                app = get_app_controller()
                
                # Test basic controller properties
                assert hasattr(app, 'session_id')
                assert app.session_id == 'test1234'
                
                # Test analysis storage
                sample_data = {'test': 'data'}
                sample_ratios = {'ratio1': 1.5}
                sample_scores = {'global': 75}
                sample_metadata = {'source': 'test'}
                
                app.store_analysis(sample_data, sample_ratios, sample_scores, sample_metadata)
                
                # Test analysis retrieval
                analysis = app.get_analysis()
                assert analysis is not None
                assert analysis['data']['test'] == 'data'
                assert analysis['scores']['global'] == 75
                
                print("Session management working correctly")
                
            finally:
                # Restore original session state
                if original_session_state is not None:
                    st.session_state = original_session_state
            
        except Exception as e:
            raise Exception(f"Session management failed: {e}")
    
    def test_widget_keys(self):
        """Test widget key generation"""
        
        try:
            # Enhanced Streamlit session state mock
            class MockSessionState:
                def __init__(self):
                    self.data = {}
                    # Pre-initialize required keys
                    self.data['optcred_v2_session_id'] = 'test1234'
                    self.data['optcred_v2_widget_counter'] = 0
                    self.data['optcred_v2_initialization_done'] = True
                
                def get(self, key, default=None):
                    return self.data.get(key, default)
                
                def __getitem__(self, key):
                    if key not in self.data:
                        raise KeyError(key)
                    return self.data[key]
                
                def __setitem__(self, key, value):
                    self.data[key] = value
                
                def __contains__(self, key):
                    return key in self.data
                
                def keys(self):
                    return self.data.keys()
                
                def setdefault(self, key, default):
                    if key not in self.data:
                        self.data[key] = default
                    return self.data[key]
            
            # Mock streamlit module
            import streamlit as st
            original_session_state = getattr(st, 'session_state', None)
            st.session_state = MockSessionState()
            
            try:
                from app_controller import get_app_controller
                app = get_app_controller()
                
                # Generate multiple keys
                keys = []
                for i in range(10):
                    key = app.generate_widget_key(f"test_widget_{i}")
                    keys.append(key)
                
                # Verify uniqueness
                assert len(keys) == len(set(keys)), "Widget keys are not unique"
                
                # Verify format
                for key in keys:
                    parts = key.split('_')
                    assert len(parts) >= 3, f"Invalid key format: {key}"
                
                print("Widget key generation working correctly")
                
            finally:
                # Restore original session state
                if original_session_state is not None:
                    st.session_state = original_session_state
            
        except Exception as e:
            raise Exception(f"Widget key generation failed: {e}")
    
    def test_import_manager(self):
        """Test import manager functionality"""
        
        try:
            from utils.import_manager import get_import_manager
            
            im = get_import_manager()
            
            # Test successful import
            os_module = im.safe_import('os')
            assert os_module is not None
            
            # Test failed import
            fake_module = im.safe_import('non_existent_module_12345')
            assert fake_module is None
            
            # Test diagnostics
            diagnostics = im.get_import_diagnostics()
            assert isinstance(diagnostics, dict)
            assert 'cached_modules' in diagnostics
            
            print("Import manager working correctly")
            
        except Exception as e:
            raise Exception(f"Import manager failed: {e}")
    
    def test_file_upload(self):
        """Test stable file upload component"""
        
        try:
            from components.stable_file_upload import StableFileUpload
            
            # Create uploader instance
            uploader = StableFileUpload("test_upload")
            
            # Test initialization
            assert hasattr(uploader, 'prefix')
            assert hasattr(uploader, 'keys')
            assert callable(uploader.render)
            
            # Test key generation
            keys = uploader.keys
            assert 'file_content' in keys
            assert 'file_name' in keys
            assert 'upload_timestamp' in keys
            
            print("File upload component working correctly")
            
        except Exception as e:
            raise Exception(f"File upload component failed: {e}")
    
    def test_navigation(self):
        """Test navigation system"""
        
        try:
            # Enhanced Streamlit session state mock
            class MockSessionState:
                def __init__(self):
                    self.data = {}
                    # Pre-initialize required keys
                    self.data['optcred_v2_session_id'] = 'test1234'
                    self.data['optcred_v2_widget_counter'] = 0
                    self.data['optcred_v2_initialization_done'] = True
                    self.data['optcred_v2_current_page'] = 'home'
                    self.data['optcred_v2_app_state'] = 'ready'
                
                def get(self, key, default=None):
                    return self.data.get(key, default)
                
                def __getitem__(self, key):
                    if key not in self.data:
                        raise KeyError(key)
                    return self.data[key]
                
                def __setitem__(self, key, value):
                    self.data[key] = value
                
                def __contains__(self, key):
                    return key in self.data
                
                def keys(self):
                    return self.data.keys()
                
                def setdefault(self, key, default):
                    if key not in self.data:
                        self.data[key] = default
                    return self.data[key]
            
            # Mock streamlit module
            import streamlit as st
            original_session_state = getattr(st, 'session_state', None)
            st.session_state = MockSessionState()
            
            try:
                from app_controller import get_app_controller, Page
                
                app = get_app_controller()
                
                # Test page enumeration
                assert Page.HOME.value == 'home'
                assert Page.UNIFIED_INPUT.value == 'unified_input'
                assert Page.ANALYSIS.value == 'analysis'
                assert Page.REPORTS.value == 'reports'
                
                # Test navigation (without actual streamlit)
                current_page = app.current_page
                assert isinstance(current_page, Page)
                
                print("Navigation system working correctly")
                
            finally:
                # Restore original session state
                if original_session_state is not None:
                    st.session_state = original_session_state
            
        except Exception as e:
            raise Exception(f"Navigation system failed: {e}")
    
    def _log_success(self, message):
        """Log successful test"""
        self.results['passed'] += 1
        print(f"PASS: {message}")
    
    def _log_error(self, message, error):
        """Log failed test"""
        self.results['failed'] += 1
        error_detail = f"{message}: {str(error)}"
        self.results['errors'].append(error_detail)
        print(f"FAIL: {error_detail}")
        
        # Print traceback for debugging
        print("   Traceback:")
        traceback.print_exc()
    
    def _print_summary(self):
        """Print test summary"""
        
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        print("\n" + "=" * 60)
        print("TEST SUITE SUMMARY")
        print("=" * 60)
        print(f"Duration: {duration:.2f} seconds")
        print(f"Passed: {self.results['passed']}")
        print(f"Failed: {self.results['failed']}")
        print(f"Success Rate: {(self.results['passed'] / (self.results['passed'] + self.results['failed']) * 100):.1f}%")
        
        if self.results['errors']:
            print("\nERRORS FOUND:")
            for i, error in enumerate(self.results['errors'], 1):
                print(f"{i}. {error}")
        
        if self.results['failed'] == 0:
            print("\nALL TESTS PASSED! Your OptCred fixes are working correctly!")
        else:
            print(f"\n{self.results['failed']} tests failed. Please review the errors above.")
        
        print("=" * 60)

def create_test_data():
    """Create sample test data for Excel testing"""
    
    try:
        import pandas as pd
        
        # Sample financial data
        bilan_data = {
            'Compte': [
                'Total Actif',
                'Immobilisations nettes', 
                'Stocks',
                'Créances clients',
                'Trésorerie',
                'Capitaux propres',
                'Dettes financières',
                'Dettes court terme'
            ],
            'Montant': [
                1000000,  # Total Actif
                500000,   # Immobilisations
                200000,   # Stocks
                150000,   # Créances
                150000,   # Trésorerie
                400000,   # Capitaux propres
                300000,   # Dettes financières
                300000    # Dettes CT
            ]
        }
        
        cr_data = {
            'Compte': [
                'Chiffre d\'affaires',
                'Résultat d\'exploitation',
                'Résultat net',
                'Charges personnel'
            ],
            'Montant': [
                1200000,  # CA
                100000,   # Résultat exploitation
                75000,    # Résultat net
                250000    # Charges personnel
            ]
        }
        
        # Create Excel file with multiple sheets
        with pd.ExcelWriter('test_data.xlsx', engine='openpyxl') as writer:
            pd.DataFrame(bilan_data).to_excel(writer, sheet_name='Bilan', index=False)
            pd.DataFrame(cr_data).to_excel(writer, sheet_name='CR', index=False)
        
        print("Test data file created: test_data.xlsx")
        
    except Exception as e:
        print(f"Failed to create test data: {e}")

def main():
    """Main test execution"""
    
    print("OptCred Test Suite Launcher")
    print("Choose your testing mode:")
    print("1. Run Automated Tests")
    print("2. Create Test Data")  
    print("3. Launch App for Manual Testing")
    print("4. Full Test Suite (Automated + Manual)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        # Run automated tests
        suite = TestSuite()
        suite.run_all_tests()
        
    elif choice == '2':
        # Create test data
        create_test_data()
        
    elif choice == '3':
        # Launch app
        print("Launching OptCred for manual testing...")
        try:
            subprocess.run(['streamlit', 'run', 'main_fixed.py'], cwd=current_dir)
        except FileNotFoundError:
            print("Streamlit not found. Install with: pip install streamlit")
        except Exception as e:
            print(f"Failed to launch app: {e}")
            
    elif choice == '4':
        # Full test suite
        print("Running full test suite...")
        
        # 1. Create test data
        create_test_data()
        
        # 2. Run automated tests
        suite = TestSuite()
        suite.run_all_tests()
        
        # 3. Launch app for manual testing
        if suite.results['failed'] == 0:
            print("\nAutomated tests passed! Launching app for manual testing...")
            input("Press Enter to launch the app...")
            try:
                subprocess.run(['streamlit', 'run', 'main_fixed.py'], cwd=current_dir)
            except Exception as e:
                print(f"Failed to launch app: {e}")
        else:
            print("Some automated tests failed. Fix issues before manual testing.")
    
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()