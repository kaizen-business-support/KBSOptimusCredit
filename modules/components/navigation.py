import streamlit as st

def show_navigation():
    """Affiche le menu de navigation principal"""
    
    # Menu horizontal
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Accueil", use_container_width=True):
            st.session_state.current_page = 'home'
    
    with col2:
        if st.button("📤 Import Excel", use_container_width=True):
            st.session_state.current_page = 'excel_import'
    
    with col3:
        if st.button("✏️ Saisie Manuelle", use_container_width=True):
            st.session_state.current_page = 'manual_input'
    
    with col4:
        if st.button("📊 Analyse", use_container_width=True):
            st.session_state.current_page = 'analysis'
    
    with col5:
        if st.button("📋 Rapports", use_container_width=True):
            st.session_state.current_page = 'reports'
    
    return st.session_state.get('current_page', 'home')