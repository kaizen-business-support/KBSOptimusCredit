"""
Page de saisie unifiée - Version 1.0
Utilise session_manager pour la gestion d'état
Développé par Kaizen Business Support
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

# Import the session manager (used by original main.py)
try:
    from session_manager import SessionManager
except ImportError as e:
    st.error(f"❌ Impossible d'importer session_manager: {e}")
    st.stop()

def show_unified_input_page():
    """Page de saisie unifiée compatible avec le système original"""
    
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
    """Gestion de l'import Excel simple et stable"""
    
    st.subheader("📤 Import de fichier Excel")
    st.info("Importez vos états financiers au format Excel conforme BCEAO")
    
    # File uploader simple et stable
    uploaded_file = st.file_uploader(
        "Choisir un fichier Excel (.xlsx, .xls)",
        type=['xlsx', 'xls'],
        key="excel_uploader_stable_main"  # Clé unique et stable
    )
    
    if uploaded_file is not None:
        process_excel_file(uploaded_file)

def process_excel_file(uploaded_file):
    """Traite le fichier Excel uploadé"""
    
    try:
        st.success(f"✅ Fichier **{uploaded_file.name}** prêt pour l'analyse")
        
        # Afficher les informations du fichier
        file_size = len(uploaded_file.getvalue())
        st.info(f"📁 Taille: {file_size:,} octets")
        
        # Prévisualisation du fichier
        try:
            # Lire le fichier Excel
            df = pd.read_excel(uploaded_file, sheet_name=None)  # Lire toutes les feuilles
            
            st.subheader("📋 Aperçu du fichier")
            
            # Afficher les feuilles disponibles
            if len(df) > 1:
                st.write(f"**Feuilles trouvées:** {', '.join(df.keys())}")
                
                # Afficher chaque feuille
                for sheet_name, sheet_df in df.items():
                    with st.expander(f"Feuille: {sheet_name}"):
                        st.dataframe(sheet_df.head(10), use_container_width=True)
            else:
                # Une seule feuille
                sheet_name = list(df.keys())[0]
                sheet_df = df[sheet_name]
                st.dataframe(sheet_df.head(10), use_container_width=True)
                
        except Exception as e:
            st.warning(f"⚠️ Impossible de prévisualiser le fichier: {e}")
        
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
                key="secteur_select_main_stable"  # Clé stable
            )
        
        with col2:
            st.info("Le secteur permet une comparaison avec les normes sectorielles")
        
        # Check if analysis was already completed
        if st.session_state.get('analysis_completed_excel', False):
            # Show completed analysis state
            st.success("🎉 Analyse terminée avec succès!")
            st.info("🎯 Analyse terminée ! Vous pouvez maintenant consulter les résultats détaillés.")
            
            if st.button("📊 Voir les Résultats", key="view_results_main_stable", type="primary"):
                # Use direct navigation like the sidebar
                st.session_state['current_page'] = 'analysis'
                st.query_params.page = 'analysis'
                st.rerun()
        else:
            # Bouton d'analyse
            if st.button(
                "🚀 Lancer l'Analyse Financière",
                key="launch_analysis_main_stable",  # Clé stable
                type="primary"
            ):
                launch_financial_analysis(uploaded_file, secteur)
    
    except Exception as e:
        st.error(f"❌ Erreur traitement fichier: {e}")
        st.code(traceback.format_exc())

def launch_financial_analysis(uploaded_file, secteur):
    """Lance l'analyse financière"""
    
    try:
        with st.spinner("🔄 Analyse en cours..."):
            
            # Import sécurisé de l'analyseur
            try:
                from modules.core.analyzer import FinancialAnalyzer
                
                # Créer l'analyseur
                analyzer = FinancialAnalyzer()
                
                # Créer un fichier temporaire pour l'analyse
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_file_path = tmp_file.name
                
                # Lancer l'analyse
                analysis_result = analyzer.analyze_excel_file(temp_file_path, secteur)
                
                # Nettoyer le fichier temporaire
                os.unlink(temp_file_path)
                
                if analysis_result.get('success', False):
                    # Stocker les résultats dans le format attendu par SessionManager
                    analysis_results = {
                        'data': analysis_result['data'],
                        'ratios': analysis_result['ratios'],
                        'scores': analysis_result['scores'],
                        'metadata': {
                            'source': 'Excel Import',
                            'file_name': uploaded_file.name,
                            'secteur': secteur,
                            'timestamp': datetime.now().isoformat()
                        }
                    }
                    st.session_state['analysis_results'] = analysis_results
                    
                    # Mark analysis as completed to preserve state across reruns
                    st.session_state['analysis_completed_excel'] = True
                    
                    # Afficher le succès
                    st.success("🎉 Analyse terminée avec succès!")
                    
                    # Navigation automatique vers les résultats
                    st.info("🎯 Analyse terminée ! Vous pouvez maintenant consulter les résultats détaillés.")
                    
                    if st.button("📊 Voir les Résultats", key="view_results_main_stable", type="primary"):
                        # Use direct navigation like the sidebar
                        st.session_state['current_page'] = 'analysis'
                        st.query_params.page = 'analysis'
                        st.rerun()
                
                else:
                    st.error(f"❌ Erreur d'analyse: {analysis_result.get('error', 'Erreur inconnue')}")
                    
            except ImportError:
                st.error("❌ Module d'analyse non disponible")
                st.info("Vérifiez que le module modules.core.analyzer est présent")
            
    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse: {e}")
        st.code(traceback.format_exc())

def handle_manual_input():
    """Gestion de la saisie manuelle"""
    
    st.subheader("✏️ Saisie Manuelle des Données")
    st.info("Saisissez vos données financières directement dans l'interface")
    
    # Formulaire de saisie manuelle
    with st.form(key="manual_input_form_main_stable"):  # Clé stable
        st.markdown("### 📊 Données du Bilan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**ACTIF**")
            immobilisations = st.number_input(
                "Immobilisations nettes", 
                min_value=0.0,
                key="immobilisations_main_stable"
            )
            stocks = st.number_input(
                "Stocks",
                min_value=0.0, 
                key="stocks_main_stable"
            )
            creances = st.number_input(
                "Créances clients",
                min_value=0.0,
                key="creances_main_stable"
            )
            tresorerie = st.number_input(
                "Trésorerie",
                min_value=0.0,
                key="tresorerie_main_stable"
            )
        
        with col2:
            st.markdown("**PASSIF**")
            capitaux_propres = st.number_input(
                "Capitaux propres",
                key="capitaux_propres_main_stable"
            )
            dettes_financieres = st.number_input(
                "Dettes financières",
                min_value=0.0,
                key="dettes_financieres_main_stable"
            )
            dettes_court_terme = st.number_input(
                "Dettes court terme",
                min_value=0.0,
                key="dettes_ct_main_stable"
            )
        
        st.markdown("### 💰 Données du Compte de Résultat")
        
        col3, col4 = st.columns(2)
        
        with col3:
            chiffre_affaires = st.number_input(
                "Chiffre d'affaires",
                min_value=0.0,
                key="ca_main_stable"
            )
            resultat_exploitation = st.number_input(
                "Résultat d'exploitation", 
                key="resultat_exploit_main_stable"
            )
        
        with col4:
            resultat_net = st.number_input(
                "Résultat net",
                key="resultat_net_main_stable"
            )
            charges_personnel = st.number_input(
                "Charges de personnel",
                min_value=0.0,
                key="charges_personnel_main_stable"
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
            key="secteur_manual_main_stable"
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
            
            try:
                # Import sécurisé des modules
                from modules.core.analyzer import FinancialAnalyzer
                from modules.core.ratios import RatiosCalculator
                
                # Calculer les ratios
                ratios_calc = RatiosCalculator()
                ratios = ratios_calc.calculate_all_ratios(data)
                
                # Calculer les scores
                analyzer = FinancialAnalyzer()
                scores = analyzer.calculate_score(ratios, secteur)
                
                # Stocker les résultats dans le format attendu par SessionManager
                analysis_results = {
                    'data': data,
                    'ratios': ratios,
                    'scores': scores,
                    'metadata': {
                        'source': 'Saisie Manuelle',
                        'secteur': secteur,
                        'timestamp': datetime.now().isoformat()
                    }
                }
                st.session_state['analysis_results'] = analysis_results
                
                # Mark analysis as completed to preserve state across reruns
                st.session_state['analysis_completed_manual'] = True
                
                st.success("🎉 Analyse terminée avec succès!")
                
                # Navigation vers les résultats
                st.info("🎯 Analyse terminée ! Vous pouvez maintenant consulter les résultats détaillés.")
                
                if st.button("📊 Voir les Résultats", key="manual_view_results_main_stable", type="primary"):
                    # Use direct navigation like the sidebar
                    st.session_state['current_page'] = 'analysis'
                    st.query_params.page = 'analysis'
                    st.rerun()
                    
            except ImportError:
                st.error("❌ Modules d'analyse non disponibles")
                st.info("Vérifiez que les modules modules.core.analyzer et modules.core.ratios sont présents")
    
    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse: {e}")
        st.code(traceback.format_exc())

def handle_ocr_input():
    """Gestion de l'input OCR (fonctionnalité future)"""
    
    st.subheader("🤖 Reconnaissance Optique (OCR)")
    st.info("🚧 Fonctionnalité en développement - Disponible dans une prochaine version")
    
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
        key="ocr_email_main_stable"
    )
    
    if st.button("📧 M'alerter", key="ocr_notify_main_stable"):
        if email:
            st.success(f"✅ Nous vous notifierons à {email} dès que l'OCR sera disponible!")
        else:
            st.warning("⚠️ Veuillez saisir une adresse email valide")

# Point d'entrée de la page
if __name__ == "__main__":
    show_unified_input_page()