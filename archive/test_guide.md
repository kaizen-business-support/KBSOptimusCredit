# 🧪 Complete Testing Guide - OptCred Fixed Version

## 📋 Pre-Testing Setup

### 1. Backup Your Current Version
```bash
# Create backup of your current OptCred
cp -r C:\Developper\OptCred C:\Developper\OptCred_backup_$(date +%Y%m%d)
```

### 2. File Structure Verification
Ensure you have these new files in your OptCred directory:

```
C:\Developper\OptCred\
├── app_controller.py                 ✅ NEW - Core controller
├── main_fixed.py                     ✅ NEW - Fixed main app
├── unified_input_page_fixed.py       ✅ NEW - Fixed input page
├── components\
│   └── stable_file_upload.py         ✅ NEW - Stable file upload
├── utils\
│   └── import_manager.py              ✅ NEW - Import manager
├── main.py                           📁 ORIGINAL - Keep as backup
├── session_manager.py                📁 ORIGINAL - Keep as backup
└── unified_input_page.py             📁 ORIGINAL - Keep as backup
```

### 3. Dependencies Check
```bash
# Verify all required packages
pip list | grep -E "(streamlit|pandas|numpy|openpyxl|plotly)"
```

## 🎯 Phase 1: Basic Functionality Tests

### Test 1.1: Application Startup
```bash
cd C:\Developper\OptCred
streamlit run main_fixed.py
```

**Expected Results:**
- ✅ App starts without errors
- ✅ HomePage displays correctly
- ✅ Sidebar navigation appears
- ✅ No import error messages

**If Issues:**
- Check Python path includes OptCred directory
- Verify all required files exist
- Check console for detailed error messages

### Test 1.2: Controller Initialization
**Steps:**
1. Open the app
2. Check sidebar "🔧 Diagnostic Système"
3. Expand to view system health

**Expected Values:**
```
version: 2.1.2-STABLE
session_id: [8-character ID]
current_page: home
app_state: ready
has_analysis: False
initialization_done: True
widget_counter: [incremental number]
```

## 🔄 Phase 2: Session State Management Tests

### Test 2.1: Navigation Stability
**Steps:**
1. Navigate: Home → Saisie des Données → Home → Saisie des Données
2. Repeat 5 times rapidly
3. Check sidebar diagnostic after each navigation

**Expected Results:**
- ✅ Session ID remains constant
- ✅ Widget counter increments predictably
- ✅ No error messages in console
- ✅ Page content loads consistently

**Test Script:**
```python
# Add this to test_navigation.py for automated testing
import streamlit as st
from app_controller import get_app_controller, Page

def test_navigation_stability():
    app = get_app_controller()
    
    # Record initial state
    initial_session_id = app.session_id
    
    # Navigate multiple times
    for _ in range(10):
        app.navigate_to(Page.UNIFIED_INPUT)
        app.navigate_to(Page.HOME)
        
        # Verify session stability
        assert app.session_id == initial_session_id
        
    print("✅ Navigation stability test PASSED")
```

### Test 2.2: Widget Key Stability
**Steps:**
1. Go to "Saisie des Données" page
2. Click "📤 Import Excel" tab
3. Note the file uploader widget
4. Navigate to Home and back
5. Check if uploader widget resets

**Expected Results:**
- ✅ Uploader widget maintains state
- ✅ No "DuplicateWidgetID" errors
- ✅ Upload progress preserved during navigation

## 📁 Phase 3: File Upload Tests

### Test 3.1: Stable File Upload
**Preparation:**
Create a test Excel file with sample data:

```python
# create_test_file.py
import pandas as pd
import openpyxl

# Create sample financial data
data = {
    'Compte': ['Total Actif', 'Capitaux Propres', 'Chiffre Affaires'],
    'Montant': [1000000, 400000, 800000]
}

df = pd.DataFrame(data)
df.to_excel('C:\Developper\OptCred\test_data.xlsx', index=False)
print("✅ Test file created: test_data.xlsx")
```

**Test Steps:**
1. Go to "📊 Saisie des Données"
2. Click "📤 Import Excel" tab
3. Upload `test_data.xlsx`
4. Verify file appears as "✅ Fichier chargé"
5. Navigate to Home page
6. Return to "📊 Saisie des Données"
7. Check if file is still loaded

**Expected Results:**
- ✅ File upload succeeds
- ✅ File preview displays correctly
- ✅ File persists after navigation
- ✅ "🔄 Remplacer" and "🗑️ Supprimer" buttons work

### Test 3.2: File Upload Edge Cases
**Test different scenarios:**

**Large File Test:**
```python
# Create 45MB test file (within limit)
import pandas as pd
import numpy as np

large_data = pd.DataFrame(np.random.randn(100000, 20))
large_data.to_excel('large_test.xlsx')
```

**Corrupted File Test:**
```python
# Create invalid Excel file
with open('corrupted.xlsx', 'w') as f:
    f.write('This is not Excel data')
```

**Test Steps:**
1. Try uploading large file → Should succeed with warning
2. Try uploading corrupted file → Should show error message
3. Try uploading unsupported format → Should be rejected

## 🧮 Phase 4: Analysis Workflow Tests

### Test 4.1: Complete Excel Analysis Workflow
**Steps:**
1. Upload valid Excel file with financial data
2. Select sector: "industrie_manufacturiere"
3. Click "🚀 Lancer l'Analyse Financière"
4. Wait for analysis completion
5. Click "📊 Voir les Résultats"
6. Navigate through all analysis sections

**Expected Results:**
- ✅ Analysis completes without errors
- ✅ Score displayed (0-100)
- ✅ Financial class assigned (A+ to E)
- ✅ Ratios calculated and displayed
- ✅ Recommendations provided

### Test 4.2: Manual Input Analysis
**Steps:**
1. Go to "✏️ Saisie Manuelle" tab
2. Fill in sample data:
   ```
   Immobilisations: 500000
   Stocks: 200000
   Créances: 150000
   Trésorerie: 50000
   Capitaux propres: 400000
   Dettes financières: 300000
   Dettes CT: 200000
   CA: 1000000
   Résultat exploitation: 80000
   Résultat net: 60000
   Charges personnel: 200000
   ```
3. Click "🚀 Analyser les Données"
4. Verify analysis results

**Expected Results:**
- ✅ Form accepts all inputs
- ✅ Analysis launches successfully
- ✅ Results match Excel analysis logic
- ✅ Navigation to results works

## 🔍 Phase 5: Module Import Tests

### Test 5.1: Import Manager Functionality
**Test Script:**
```python
# test_imports.py
from utils.import_manager import get_import_manager

def test_import_manager():
    im = get_import_manager()
    
    # Test successful import
    session_manager = im.safe_import('session_manager')
    assert session_manager is not None
    
    # Test failed import with fallback
    fake_module = im.safe_import('non_existent_module')
    assert fake_module is None
    
    # Test diagnostics
    diagnostics = im.get_import_diagnostics()
    print("Import Diagnostics:", diagnostics)
    
    print("✅ Import manager tests PASSED")

if __name__ == "__main__":
    test_import_manager()
```

### Test 5.2: Module Fallback Behavior
**Steps:**
1. Temporarily rename `modules/core/analyzer.py` to `analyzer.py.bak`
2. Try to perform analysis
3. Check if fallback error handling works
4. Restore the file
5. Verify analysis works again

**Expected Results:**
- ✅ Graceful error message when module missing
- ✅ App doesn't crash
- ✅ Analysis works after restoration

## ⚡ Phase 6: Stress Tests

### Test 6.1: Rapid Navigation Stress Test
**Test Script:**
```python
# stress_test_navigation.py
import time
from app_controller import get_app_controller, Page

def stress_test_navigation():
    app = get_app_controller()
    
    pages = [Page.HOME, Page.UNIFIED_INPUT, Page.HOME, Page.UNIFIED_INPUT]
    
    start_time = time.time()
    
    for i in range(50):  # 50 rapid navigations
        for page in pages:
            app.navigate_to(page)
            time.sleep(0.1)  # Brief pause
        
        if i % 10 == 0:
            print(f"Completed {i} navigation cycles")
    
    end_time = time.time()
    print(f"✅ Stress test completed in {end_time - start_time:.2f} seconds")
    
    # Verify app state
    health = app.get_health_status()
    print("Final health status:", health)

if __name__ == "__main__":
    stress_test_navigation()
```

### Test 6.2: Multiple File Upload Test
**Steps:**
1. Upload a file
2. Navigate away and back
3. Upload a different file
4. Check if both operations work correctly
5. Repeat with 5 different files

**Expected Results:**
- ✅ Each file upload works independently
- ✅ File replacement works correctly
- ✅ Memory usage stays reasonable
- ✅ No accumulated errors

## 🐛 Phase 7: Error Scenarios

### Test 7.1: Intentional Error Injection
**Create problematic scenarios:**

**Corrupted Session Test:**
```python
# Manually corrupt session state
import streamlit as st
st.session_state['optcred_v2_analysis_data'] = "corrupted_data"
```

**Memory Pressure Test:**
```python
# Create large objects in session
import numpy as np
st.session_state['large_object'] = np.random.randn(1000000)
```

**Expected Results:**
- ✅ App detects corruption and recovers
- ✅ Error messages are user-friendly
- ✅ Reset functionality works
- ✅ No data loss in normal operations

## 📊 Phase 8: Performance Tests

### Test 8.1: Load Time Measurement
**Test Script:**
```python
# performance_test.py
import time
import psutil
import os

def measure_performance():
    process = psutil.Process(os.getpid())
    
    # Measure startup time
    start_time = time.time()
    from app_controller import get_app_controller
    app = get_app_controller()
    startup_time = time.time() - start_time
    
    # Measure memory usage
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"Startup time: {startup_time:.3f}s")
    print(f"Memory usage: {memory_usage:.2f}MB")
    
    return startup_time < 2.0 and memory_usage < 100  # Acceptable thresholds

if __name__ == "__main__":
    success = measure_performance()
    print("✅ Performance test PASSED" if success else "❌ Performance test FAILED")
```

## 🔧 Phase 9: Production Readiness

### Test 9.1: Error Logging Verification
**Steps:**
1. Check if errors are properly logged
2. Verify user-friendly error messages
3. Test error recovery mechanisms

**Log Locations:**
- Streamlit console output
- Browser console (F12)
- Application diagnostic panel

### Test 9.2: Multi-User Simulation
**Steps:**
1. Open app in multiple browser tabs
2. Perform different actions in each tab
3. Verify sessions don't interfere
4. Check performance with multiple sessions

## 📝 Test Results Documentation

### Create Test Report Template:
```markdown
# OptCred Testing Report - [Date]

## Environment
- OS: Windows 10/11
- Python: 3.x
- Streamlit: 1.x
- Browser: Chrome/Firefox/Edge

## Test Results Summary
- [ ] Phase 1: Basic Functionality
- [ ] Phase 2: Session Management
- [ ] Phase 3: File Upload
- [ ] Phase 4: Analysis Workflow
- [ ] Phase 5: Module Imports
- [ ] Phase 6: Stress Tests
- [ ] Phase 7: Error Scenarios
- [ ] Phase 8: Performance
- [ ] Phase 9: Production Readiness

## Issues Found
1. [Issue description]
   - Severity: High/Medium/Low
   - Steps to reproduce:
   - Expected vs Actual behavior:
   - Fix applied: Yes/No

## Performance Metrics
- Startup time: [X]s
- Memory usage: [X]MB
- Navigation response: [X]ms
- Analysis time: [X]s

## Recommendations
- [ ] Ready for production
- [ ] Needs additional fixes
- [ ] Requires performance optimization

## Sign-off
Tested by: [Name]
Date: [Date]
Status: PASSED/FAILED
```

## 🚀 Quick Test Commands

For rapid testing, use these commands:

```bash
# Basic functionality test
streamlit run main_fixed.py

# Run all automated tests
python test_navigation.py
python test_imports.py
python stress_test_navigation.py
python performance_test.py

# Check file structure
ls -la C:\Developper\OptCred\
```

## ✅ Success Criteria

Your testing is successful when:

1. **Zero widget reset errors** during navigation
2. **Consistent session IDs** across page changes
3. **File uploads persist** through navigation
4. **Analysis completes** without import errors
5. **Navigation response time** < 1 second
6. **Memory usage stable** during extended use
7. **Error recovery works** in all scenarios
8. **Multi-tab operation** without conflicts

## 🆘 Troubleshooting Common Issues

### Issue: "Module not found" errors
**Solution:**
```python
# Check Python path
import sys
print(sys.path)

# Add OptCred to path manually
sys.path.insert(0, r'C:\Developper\OptCred')
```

### Issue: Widget key conflicts
**Solution:**
- Clear browser cache
- Delete `.streamlit` folder
- Restart Streamlit server

### Issue: Session state corruption
**Solution:**
```python
# Reset session state
for key in list(st.session_state.keys()):
    del st.session_state[key]
st.rerun()
```

---

**Follow this guide systematically and you'll have a bulletproof OptCred application!** 🎯