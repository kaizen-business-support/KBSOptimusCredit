"""
Application principale OptimusCredit - Version Corrigée STABLE
Résout définitivement tous les problèmes de session, navigation et widgets
Version 2.1.2-STABLE - Kaizen Business Support
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Configuration de la page DOIT être la première commande Streamlit
st.set_page_config(
    page_title="OptimusCredit - Analyse Financière BCEAO",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import du contrôleur centralisé
try:
    from app_controller import get_app_controller, Page
    app = get_app_controller()
except ImportError as e:
    st.error(f"❌ Impossible d'importer app_controller.py: {e}")
    st.error("Assurez-vous que app_controller.py est présent dans le répertoire racine.")
    st.stop()

def main():
    """Fonction principale simplifiée et robuste"""
    
    # Afficher l'en-tête
    display_header()
    
    # Sidebar avec navigation
    display_sidebar()
    
    # Contenu principal via le contrôleur
    app.display_page()
    
    # Pied de page
    display_footer()

def display_header():
    """En-tête de l'application"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #1f4e79; margin-bottom: 10px;">📊 OptimusCredit</h1>
            <h3 style="color: #2e7d32; margin-top: 0;">Outil d'Analyse Financière BCEAO</h3>
            <p style="color: #666; margin-top: 10px;">Conforme aux normes prudentielles BCEAO 2024 • Version 2.1.2-STABLE</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

def display_sidebar():
    """Sidebar avec navigation centralisée"""
    
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        # Statut de l'analyse
        if app.has_valid_analysis():
            display_analysis_status()
        else:
            st.info("ℹ️ Aucune analyse en cours")
        
        st.markdown("---")
        
        # Menu de navigation
        display_navigation_menu()
        
        st.markdown("---")
        
        # Actions rapides
        display_quick_actions()
        
        st.markdown("---")
        
        # Diagnostic système
        if st.expander("🔧 Diagnostic Système"):
            health = app.get_health_status()
            for key, value in health.items():
                st.text(f"{key}: {value}")

def display_analysis_status():
    """Affichage du statut d'analyse dans la sidebar"""
    try:
        analysis = app.get_analysis()
        if not analysis:
            return
        
        scores = analysis.get('scores', {})
        global_score = scores.get('global', 0)
        
        # Déterminer la couleur et classe
        if global_score >= 70:
            color = "#22c55e"
            classe = "A" if global_score < 85 else "A+"
        elif global_score >= 40:
            color = "#f59e0b" 
            classe = "B" if global_score >= 55 else "C"
        else:
            color = "#ef4444"
            classe = "D" if global_score >= 25 else "E"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; border-radius: 10px; background-color: {color}20; border: 2px solid {color};">
            <h4 style="color: {color}; margin: 0;">✅ Analyse Disponible</h4>
            <h2 style="color: {color}; margin: 10px 0;">{global_score}/100</h2>
            <p style="color: {color}; margin: 0; font-weight: bold;">Classe {classe}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Métadonnées
        metadata = analysis.get('metadata', {})
        if metadata:
            st.markdown(f"""
            **📁 Source:** {metadata.get('source', 'N/A')}  
            **🏭 Secteur:** {metadata.get('secteur', 'N/A').replace('_', ' ').title()}  
            **📅 Analysé:** {metadata.get('timestamp', 'N/A')[:19]}  
            **🔢 Ratios:** {len(analysis.get('ratios', {}))}
            """)
            
    except Exception as e:
        st.error(f"Erreur affichage statut: {e}")

def display_navigation_menu():
    """Menu de navigation avec widgets stables"""
    
    current_page = app.current_page
    analysis_available = app.has_valid_analysis()
    
    # Définition des pages avec leurs métadonnées
    pages_config = [
        (Page.HOME, "🏠 Accueil", "Page d'accueil et présentation", False),
        (Page.UNIFIED_INPUT, "📊 Saisie des Données", "Import Excel, Saisie Manuelle ou OCR", False),
        (Page.ANALYSIS, "📊 Analyse Complète", "Analyse détaillée et ratios", True),
        (Page.REPORTS, "📋 Rapports", "Génération de rapports", True)
    ]
    
    for page, label, description, requires_analysis in pages_config:
        # Déterminer l'état du bouton
        disabled = requires_analysis and not analysis_available
        button_type = "primary" if current_page == page else "secondary"
        
        # Bouton avec clé stable
        if st.button(
            label,
            key=app.generate_widget_key(f"nav_{page.value}"),
            type=button_type,
            disabled=disabled,
            use_container_width=True,
            help=description
        ):
            if not disabled:
                app.navigate_to(page)
                st.rerun()
            else:
                st.warning("⚠️ Cette fonction nécessite une analyse")

def display_quick_actions():
    """Actions rapides dans la sidebar"""
    
    st.markdown("### ⚡ Actions Rapides")
    
    analysis_available = app.has_valid_analysis()
    
    if analysis_available:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("👁️ Voir", 
                        key=app.generate_widget_key("quick_view"),
                        use_container_width=True):
                app.navigate_to(Page.ANALYSIS)
                st.rerun()
        
        with col2:
            if st.button("📄 Rapport", 
                        key=app.generate_widget_key("quick_report"),
                        use_container_width=True):
                app.navigate_to(Page.REPORTS)
                st.rerun()
        
        # Reset avec confirmation
        if st.button("🔄 Nouvelle Analyse", 
                    key=app.generate_widget_key("quick_reset"),
                    type="secondary",
                    use_container_width=True):
            app.reset_application()
    
    else:
        if st.button("📊 Saisir Données", 
                    key=app.generate_widget_key("quick_input"),
                    type="primary",
                    use_container_width=True):
            app.navigate_to(Page.UNIFIED_INPUT)
            st.rerun()
        
        st.caption("Import Excel, Saisie Manuelle ou OCR")

def display_footer():
    """Pied de page de l'application"""
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; color: #666;">
            <p style="margin: 5px 0;">
                <strong>OptimusCredit v2.1.2-STABLE</strong> • Outil d'Analyse Financière BCEAO
            </p>
            <p style="margin: 5px 0; font-size: 12px;">
                Conforme aux normes prudentielles BCEAO 2024 • 
                Architecture stabilisée et navigation sécurisée
            </p>
            <p style="margin: 5px 0; font-size: 10px;">
                © 2024 Kaizen Business Support • Tous droits réservés • 
                <a href="mailto:contact@kaizen-corporation.com" style="color: #1f4e79;">Support Technique</a>
            </p>
        </div>
        """, unsafe_allow_html=True)

# Point d'entrée de l'application
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ Erreur critique dans l'application: {e}")
        
        # Diagnostic d'urgence
        st.markdown("### 🚨 Diagnostic d'Urgence")
        
        if st.button("🔄 Redémarrer l'application", key="emergency_restart"):
            # Nettoyer complètement la session
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        # Afficher les détails techniques
        with st.expander("🔍 Détails Techniques"):
            import traceback
            st.code(traceback.format_exc())