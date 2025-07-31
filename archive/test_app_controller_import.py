"""
Test app_controller import functionality specifically
"""
import streamlit as st
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

st.set_page_config(page_title="App Controller Import Test", layout="wide")

def test_app_controller_import():
    """Test the app_controller import system"""
    
    st.title("App Controller Import Test")
    
    try:
        from app_controller import get_app_controller
        st.success("✅ app_controller imported successfully")
        
        app = get_app_controller()
        st.success(f"✅ AppController initialized - Session ID: {app.session_id}")
        
        # Test the safe_import method directly
        st.subheader("Testing safe_import method")
        
        if st.button("Test import 'unified_input_page_fixed'", key="test_import"):
            with st.spinner("Testing import..."):
                try:
                    unified_module = app.safe_import('unified_input_page_fixed')
                    if unified_module:
                        st.success("✅ unified_input_page_fixed imported successfully via safe_import")
                        if hasattr(unified_module, 'show_unified_input_page'):
                            st.success("✅ show_unified_input_page function found")
                        else:
                            st.error("❌ show_unified_input_page function NOT found")
                    else:
                        st.error("❌ safe_import returned None")
                except Exception as e:
                    st.error(f"❌ safe_import failed: {e}")
                    import traceback
                    st.code(traceback.format_exc())
        
        # Test the _show_unified_input_page method directly
        st.subheader("Testing _show_unified_input_page method")
        
        if st.button("Test _show_unified_input_page method", key="test_method"):
            with st.spinner("Testing method..."):
                try:
                    st.markdown("**Output from app._show_unified_input_page():**")
                    app._show_unified_input_page()
                except Exception as e:
                    st.error(f"❌ _show_unified_input_page failed: {e}")
                    import traceback
                    st.code(traceback.format_exc())
                    
    except Exception as e:
        st.error(f"❌ Failed to import app_controller: {e}")
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    test_app_controller_import()