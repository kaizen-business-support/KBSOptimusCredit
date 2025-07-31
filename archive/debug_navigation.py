"""
Debug script to test navigation functionality
"""
import streamlit as st
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

st.set_page_config(page_title="Navigation Debug", layout="wide")

def test_imports():
    """Test all imports"""
    st.subheader("Import Tests")
    
    try:
        from app_controller import get_app_controller, Page
        st.success("app_controller imported successfully")
        
        app = get_app_controller()
        st.success(f"AppController initialized - Session ID: {app.session_id}")
        
        # Test navigation
        st.write(f"Current page: {app.current_page}")
        
        if st.button("Test Navigate to UNIFIED_INPUT"):
            try:
                app.navigate_to(Page.UNIFIED_INPUT)
                st.success("Navigation command executed")
                st.write(f"New current page: {app.current_page}")
            except Exception as e:
                st.error(f"Navigation failed: {e}")
                
    except Exception as e:
        st.error(f"Import failed: {e}")
        import traceback
        st.code(traceback.format_exc())

def test_unified_input_import():
    """Test unified input page import"""
    st.subheader("Unified Input Page Import Test")
    
    try:
        import unified_input_page_fixed
        st.success("unified_input_page_fixed imported successfully")
        
        if hasattr(unified_input_page_fixed, 'show_unified_input_page'):
            st.success("show_unified_input_page function found")
            
            if st.button("Test Call show_unified_input_page"):
                try:
                    st.markdown("---")
                    st.markdown("**Output of show_unified_input_page:**")
                    unified_input_page_fixed.show_unified_input_page()
                except Exception as e:
                    st.error(f"Function call failed: {e}")
                    import traceback
                    st.code(traceback.format_exc())
        else:
            st.error("show_unified_input_page function not found")
            
    except Exception as e:
        st.error(f"Import failed: {e}")
        import traceback
        st.code(traceback.format_exc())

def test_app_display_page():
    """Test app display_page method"""
    st.subheader("App display_page Test")
    
    try:
        from app_controller import get_app_controller, Page
        app = get_app_controller()
        
        if st.button("Force navigate to UNIFIED_INPUT and display"):
            app.navigate_to(Page.UNIFIED_INPUT)
            st.write(f"Page set to: {app.current_page}")
            
            st.markdown("---")
            st.markdown("**Output of app.display_page():**")
            try:
                app.display_page()
            except Exception as e:
                st.error(f"display_page failed: {e}")
                import traceback
                st.code(traceback.format_exc())
                
    except Exception as e:
        st.error(f"Test failed: {e}")
        import traceback
        st.code(traceback.format_exc())

def main():
    st.title("OptCred Navigation Debug Tool")
    st.markdown("This tool tests the navigation functionality step by step.")
    
    tab1, tab2, tab3 = st.tabs(["Import Tests", "Unified Input Test", "Display Page Test"])
    
    with tab1:
        test_imports()
    
    with tab2:
        test_unified_input_import()
        
    with tab3:
        test_app_display_page()

if __name__ == "__main__":
    main()