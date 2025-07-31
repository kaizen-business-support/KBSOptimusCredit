"""
Page de saisie unifiée CORRIGÉE - Sans problèmes de widgets
Résout tous les problèmes d'upload, session state et navigation
Version STABLE - Kaizen Business Support
"""

import streamlit as st
import pandas as pd
import io
import traceback
from datetime import datetime
import sys
import os

# Ensure proper path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Imports sécurisés
try:
    from app_controller import get_app_controller
    from components.stable_file_upload import StableFileUpload
    from utils.import_manager import safe_import
    app = get_app_controller()
except ImportError as e:
    st.error(f"❌ Erreur d'import: {e}")
    st.error("Vérification des chemins...")
    st.code(f"Current dir: {current_dir}")
    st.code(f"Python path: {sys.path[:3]}")
    st.stop()

def show_unified_input_page():
    """Page de saisie unifiée avec tous les correctifs"""
    
    st.title("📊 Saisie des Données Financières")
    st.markdown("Interface unifiée pour l'import Excel, la saisie manuelle et l'OCR")
    
    # Onglets avec clés stables
    tab1, tab2, tab3 = st.tabs([
        "📤 Import Excel", 
        "✏️ Saisie Manuelle", 
        "🤖 OCR (Futur)"
    ])
    
    with tab1:
        handle_excel_import()
    
    with tab2:
        handle_manual_input()
    
    with tab3:
        handle_ocr_input()

def handle_excel_import():
    """Gestion de l'import Excel avec upload stable"""
    
    st.subheader("📤 Import de fichier Excel")
    st.info("Importez vos états financiers au format Excel conforme BCEAO")
    
    # Composant d'upload stable avec clé fixe
    file_uploader = StableFileUpload("excel_import")
    
    # Afficher l'upload avec clé stable fixe
    file_info = file_uploader.render(
        label="Choisir un fichier Excel (.xlsx, .xls)",
        accepted_types=['xlsx', 'xls'],
        max_size_mb=50,
        widget_key="excel_uploader_stable"  # Clé fixe au lieu de génération dynamique
    )
    
    if file_info:
        process_excel_file(file_info, file_uploader)

def process_excel_file(file_info: dict, uploader: StableFileUpload):
    """Traite le fichier Excel uploadé"""
    
    try:
        st.success(f"✅ Fichier **{file_info['name']}** prêt pour l'analyse")
        
        # Afficher l'aperçu
        uploader.display_file_preview(max_rows=10)
        
        # Options d'analyse
        st.subheader("⚙️ Options d'Analyse")
        
        col1, col2 = st.columns(2)
        
        with col1:
            secteur = st.selectbox(
                "Secteur d'activité",
                [
                    "industrie_manufacturiere",
                    "commerce_detail", 
                    "services_professionnels",
                    "construction_btp",
                    "agriculture",
                    "commerce_gros"
                ],
                key="secteur_select_stable"  # Clé fixe
            )
        
        with col2:
            st.info("Le secteur permet une comparaison avec les normes sectorielles")
        
        # Bouton d'analyse
        if st.button(
            "🚀 Lancer l'Analyse Financière",
            key="launch_analysis_stable",  # Clé fixe
            type="primary"
        ):
            launch_financial_analysis(file_info, secteur, uploader)
    
    except Exception as e:
        st.error(f"❌ Erreur traitement fichier: {e}")
        st.code(traceback.format_exc())

def launch_financial_analysis(file_info: dict, secteur: str, uploader: StableFileUpload):
    """Lance l'analyse financière"""
    
    try:
        with st.spinner("🔄 Analyse en cours..."):
            
            # Import sécurisé de l'analyseur
            analyzer_module = safe_import('modules.core.analyzer', ['analyzer'])
            
            if not analyzer_module:
                st.error("❌ Module d'analyse non disponible")
                return
            
            # Créer l'analyseur
            analyzer = analyzer_module.FinancialAnalyzer()
            
            # Créer un fichier temporaire pour l'analyse
            temp_file_path = create_temp_excel_file(file_info['content'])
            
            # Lancer l'analyse
            analysis_result = analyzer.analyze_excel_file(temp_file_path, secteur)
            
            if analysis_result.get('success', False):
                # Stocker les résultats
                app.store_analysis(
                    data=analysis_result['data'],
                    ratios=analysis_result['ratios'], 
                    scores=analysis_result['scores'],
                    metadata={
                        'source': 'Excel Import',
                        'file_name': file_info['name'],
                        'secteur': secteur,
                        'file_size': file_info['size'],
                        'upload_timestamp': file_info['timestamp']
                    }
                )
                
                # Marquer le traitement comme terminé
                uploader.mark_processing_complete()
                
                # Afficher le succès
                st.success("🎉 Analyse terminée avec succès!")
                
                # Navigation automatique vers les résultats
                if st.button("📊 Voir les Résultats", 
                           key="view_results_stable"):  # Clé fixe
                    from app_controller import Page
                    app.navigate_to(Page.ANALYSIS)
                    st.rerun()
            
            else:
                st.error(f"❌ Erreur d'analyse: {analysis_result.get('error', 'Erreur inconnue')}")
            
    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse: {e}")
        st.code(traceback.format_exc())

def create_temp_excel_file(file_content: bytes) -> str:
    """Crée un fichier temporaire pour l'analyse"""
    import tempfile
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
        tmp_file.write(file_content)
        return tmp_file.name

def handle_manual_input():
    """Gestion de la saisie manuelle"""
    
    st.subheader("✏️ Saisie Manuelle des Données")
    st.info("Saisissez vos données financières directement dans l'interface")
    
    # Formulaire de saisie manuelle
    with st.form(key="manual_input_form_stable"):  # Clé fixe
        st.markdown("### 📊 Données du Bilan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**ACTIF**")
            immobilisations = st.number_input(
                "Immobilisations nettes", 
                min_value=0.0,
                key="immobilisations_stable"  # Clé fixe
            )
            stocks = st.number_input(
                "Stocks",
                min_value=0.0, 
                key="stocks_stable"  # Clé fixe
            )
            creances = st.number_input(
                "Créances clients",
                min_value=0.0,
                key="creances_stable"  # Clé fixe
            )
            tresorerie = st.number_input(
                "Trésorerie",
                min_value=0.0,
                key="tresorerie_stable"  # Clé fixe
            )
        
        with col2:
            st.markdown("**PASSIF**")
            capitaux_propres = st.number_input(
                "Capitaux propres",
                key="capitaux_propres_stable"  # Clé fixe
            )
            dettes_financieres = st.number_input(
                "Dettes financières",
                min_value=0.0,
                key="dettes_financieres_stable"  # Clé fixe
            )
            dettes_court_terme = st.number_input(
                "Dettes court terme",
                min_value=0.0,
                key="dettes_ct_stable"  # Clé fixe
            )
        
        st.markdown("### 💰 Données du Compte de Résultat")
        
        col3, col4 = st.columns(2)
        
        with col3:
            chiffre_affaires = st.number_input(
                "Chiffre d'affaires",
                min_value=0.0,
                key="ca_stable"  # Clé fixe
            )
            resultat_exploitation = st.number_input(
                "Résultat d'exploitation", 
                key="resultat_exploit_stable"  # Clé fixe
            )
        
        with col4:
            resultat_net = st.number_input(
                "Résultat net",
                key="resultat_net_stable"  # Clé fixe
            )
            charges_personnel = st.number_input(
                "Charges de personnel",
                min_value=0.0,
                key="charges_personnel_stable"  # Clé fixe
            )
        
        # Secteur
        secteur_manual = st.selectbox(
            "Secteur d'activité",
            [
                "industrie_manufacturiere",
                "commerce_detail",
                "services_professionnels", 
                "construction_btp",
                "agriculture",
                "commerce_gros"
            ],
            key="secteur_manual_stable"  # Clé fixe
        )
        
        # Bouton de soumission
        submitted = st.form_submit_button(
            "🚀 Analyser les Données",
            type="primary"
        )
        
        if submitted:
            process_manual_input({
                'immobilisations_nettes': immobilisations,
                'stocks': stocks,
                'creances_clients': creances,
                'tresorerie': tresorerie,
                'capitaux_propres': capitaux_propres,
                'dettes_financieres': dettes_financieres,
                'dettes_court_terme': dettes_court_terme,
                'chiffre_affaires': chiffre_affaires,
                'resultat_exploitation': resultat_exploitation,
                'resultat_net': resultat_net,
                'charges_personnel': charges_personnel,
                'total_actif': immobilisations + stocks + creances + tresorerie
            }, secteur_manual)

def process_manual_input(data: dict, secteur: str):
    """Traite les données saisies manuellement"""
    
    try:
        # Validation des données
        if data['total_actif'] <= 0:
            st.error("❌ Le total actif doit être supérieur à zéro")
            return
        
        if data['chiffre_affaires'] <= 0:
            st.error("❌ Le chiffre d'affaires doit être supérieur à zéro")
            return
        
        with st.spinner("🔄 Analyse en cours..."):
            
            # Import sécurisé de l'analyseur
            analyzer_module = safe_import('modules.core.analyzer', ['analyzer'])
            ratios_module = safe_import('modules.core.ratios', ['ratios'])
            
            if not analyzer_module or not ratios_module:
                st.error("❌ Modules d'analyse non disponibles")
                return
            
            # Calculer les ratios
            ratios_calc = ratios_module.RatiosCalculator()
            ratios = ratios_calc.calculate_all_ratios(data)
            
            # Calculer les scores
            analyzer = analyzer_module.FinancialAnalyzer()
            scores = analyzer.calculate_score(ratios, secteur)
            
            # Stocker les résultats
            app.store_analysis(
                data=data,
                ratios=ratios,
                scores=scores,
                metadata={
                    'source': 'Saisie Manuelle',
                    'secteur': secteur,
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            st.success("🎉 Analyse terminée avec succès!")
            
            # Navigation vers les résultats
            if st.button("📊 Voir les Résultats", 
                       key="manual_view_results_stable"):  # Clé fixe
                from app_controller import Page
                app.navigate_to(Page.ANALYSIS)
                st.rerun()
    
    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse: {e}")
        st.code(traceback.format_exc())

def handle_ocr_input():
    """Gestion de l'input OCR (fonctionnalité future)"""
    
    st.subheader("🤖 Reconnaissance Optique (OCR)")
    st.info("🚧 Fonctionnalité en développement - Disponible dans la version 2.2")
    
    st.markdown("""
    ### 🔮 Fonctionnalités Prévues
    
    - **📸 Upload d'images** : PDF, PNG, JPG des états financiers
    - **🧠 IA de reconnaissance** : Extraction automatique des données
    - **✅ Validation assistée** : Vérification et correction des données extraites
    - **🔄 Traitement par lots** : Analyse de plusieurs documents simultanément
    
    ### 📧 Notifications
    
    Vous souhaitez être notifié de la disponibilité de cette fonctionnalité ?
    """)
    
    email = st.text_input(
        "Adresse email pour notification",
        key="ocr_email_stable"  # Clé fixe
    )
    
    if st.button("📧 M'alerter", key="ocr_notify_stable"):  # Clé fixe
        if email:
            st.success(f"✅ Nous vous notifierons à {email} dès que l'OCR sera disponible!")
        else:
            st.warning("⚠️ Veuillez saisir une adresse email valide")

# Point d'entrée de la page
if __name__ == "__main__":
    show_unified_input_page()