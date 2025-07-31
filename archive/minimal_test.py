"""
Minimal test to isolate the navigation issue
"""
import streamlit as st
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

st.set_page_config(page_title="Minimal Navigation Test", layout="wide")

def test_basic_navigation():
    """Test basic navigation without complex components"""
    
    st.title("Minimal Navigation Test")
    
    if "test_page" not in st.session_state:
        st.session_state.test_page = "home"
    
    st.write(f"Current page: **{st.session_state.test_page}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Go to Home", key="home_btn"):
            st.session_state.test_page = "home"
            st.rerun()
    
    with col2:
        if st.button("Go to Input Page", key="input_btn"):
            st.session_state.test_page = "input"
            st.rerun()
    
    st.markdown("---")
    
    # Display content based on current page
    if st.session_state.test_page == "home":
        show_home_page()
    elif st.session_state.test_page == "input":
        show_input_page()

def show_home_page():
    """Simple home page"""
    st.subheader("🏠 Home Page")
    st.info("This is the home page - navigation is working!")
    
    if st.button("Quick Navigate to Input", key="quick_nav"):
        st.session_state.test_page = "input"
        st.rerun()

def show_input_page():
    """Simple input page to test if the navigation issue is here"""
    st.subheader("📊 Input Page")
    st.success("SUCCESS: Navigation to input page is working!")
    
    # Test basic file upload
    uploaded_file = st.file_uploader(
        "Test File Upload",
        type=['xlsx', 'xls'],
        key="test_uploader"
    )
    
    if uploaded_file:
        st.success(f"File uploaded: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size} bytes")
    
    # Test calling the actual unified input function
    st.markdown("---")
    st.subheader("Test Real Unified Input Function")
    
    if st.button("Load Real Unified Input Page", key="load_real"):
        try:
            import unified_input_page_fixed
            st.markdown("**Output from unified_input_page_fixed.show_unified_input_page():**")
            unified_input_page_fixed.show_unified_input_page()
        except Exception as e:
            st.error(f"Error loading real page: {e}")
            import traceback
            st.code(traceback.format_exc())

if __name__ == "__main__":
    test_basic_navigation()