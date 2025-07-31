"""
Page d'import Excel - Version corrigée sans réinitialisation
"""

import streamlit as st
import tempfile
import os
from datetime import datetime

# Import du gestionnaire de session centralisé
try:
    from session_manager import SessionManager, store_analysis, reset_app
except ImportError:
    st.error("❌ Impossible d'importer session_manager.py")
    st.stop()

def show_excel_import_page():
    """Affiche la page d'import Excel - Version stable"""
    
    st.title("📤 Import et Analyse de Fichier Excel")
    st.markdown("---")
    
    # ÉTAPE 1: Vérifier s'il y a déjà une analyse complète
    if SessionManager.has_analysis_data():
        show_analysis_completed()
        return
    
    # ÉTAPE 2: Initialiser les variables de session
    if 'file_uploaded' not in st.session_state:
        st.session_state['file_uploaded'] = False
    if 'file_content' not in st.session_state:
        st.session_state['file_content'] = None
    if 'file_name' not in st.session_state:
        st.session_state['file_name'] = None
    if 'analysis_running' not in st.session_state:
        st.session_state['analysis_running'] = False
    
    # ÉTAPE 3: Gérer le reset si nécessaire
    if st.session_state.get('complete_reset', False):
        st.success("🔄 Application réinitialisée! Vous pouvez importer un nouveau fichier.")
        # Nettoyer les variables locales
        st.session_state['file_uploaded'] = False
        st.session_state['file_content'] = None
        st.session_state['file_name'] = None
        st.session_state['analysis_running'] = False
        del st.session_state['complete_reset']
        st.rerun()
    
    # ÉTAPE 4: Interface d'upload
    if not st.session_state['file_uploaded']:
        show_file_upload_interface()
    else:
        show_analysis_interface()

def show_file_upload_interface():
    """Interface d'upload de fichier"""
    
    st.header("📁 Sélection du Fichier Excel")
    
    uploaded_file = st.file_uploader(
        "Sélectionnez votre fichier Excel BCEAO",
        type=['xlsx', 'xls'],
        help="Le fichier doit contenir les feuilles : Bilan, CR (Compte de Résultat)",
        key=f"file_uploader_{SessionManager.get_reset_counter()}"
    )
    
    if uploaded_file is not None:
        # Stocker le fichier immédiatement
        st.session_state['file_content'] = uploaded_file.getbuffer()
        st.session_state['file_name'] = uploaded_file.name
        st.session_state['file_uploaded'] = True
        st.success(f"✅ Fichier '{uploaded_file.name}' chargé avec succès!")
        st.rerun()
    
    # Instructions
    show_upload_instructions()

def show_analysis_interface():
    """Interface d'analyse du fichier"""
    
    st.header("📁 Fichier Sélectionné")
    
    # Détails du fichier
    with st.expander("📋 Informations du fichier", expanded=True):
        st.write(f"**Nom :** {st.session_state['file_name']}")
        st.write(f"**Taille :** {len(st.session_state['file_content']) / 1024:.1f} KB")
        st.success("✅ Fichier prêt pour l'analyse")
    
    # Sélection du secteur
    st.header("🏭 Secteur d'Activité")
    
    secteur = st.selectbox(
        "Sélectionnez votre secteur :",
        options=[
            "industrie_manufacturiere",
            "commerce_detail", 
            "services_professionnels",
            "construction_btp",
            "agriculture",
            "commerce_gros"
        ],
        format_func=lambda x: {
            "industrie_manufacturiere": "Industrie Manufacturière",
            "commerce_detail": "Commerce de Détail",
            "services_professionnels": "Services Professionnels", 
            "construction_btp": "Construction / BTP",
            "agriculture": "Agriculture",
            "commerce_gros": "Commerce de Gros"
        }.get(x, x),
        key=f"secteur_{SessionManager.get_reset_counter()}"
    )
    
    # Bouton d'analyse
    if not st.session_state['analysis_running']:
        if st.button("🔍 Analyser le Fichier", type="primary", use_container_width=True):
            st.session_state['analysis_running'] = True
            analyze_file(st.session_state['file_content'], st.session_state['file_name'], secteur)
    else:
        st.info("🔄 Analyse en cours... Veuillez patienter.")
    
    # Options supplémentaires
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Nouveau Fichier", key="new_file"):
            st.session_state['file_uploaded'] = False
            st.session_state['file_content'] = None
            st.session_state['file_name'] = None
            st.session_state['analysis_running'] = False
            st.rerun()
    
    with col2:
        if st.button("🏠 Retour Accueil", key="go_home"):
            SessionManager.set_current_page('home')
            st.rerun()

def analyze_file(file_content, filename, secteur):
    """Analyse le fichier Excel"""
    
    try:
        with st.spinner("📊 Analyse du fichier en cours..."):
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(file_content)
                temp_path = tmp_file.name
            
            try:
                # Importer l'analyseur
                from modules.core.analyzer import FinancialAnalyzer
                
                # Analyser le fichier
                analyzer = FinancialAnalyzer()
                data = analyzer.load_excel_template(temp_path)
                
                if data is None:
                    st.error("❌ Erreur lors du chargement du fichier")
                    st.error("Vérifiez que le fichier contient les feuilles 'Bilan' et 'CR'")
                    st.session_state['analysis_running'] = False
                    return
                
                # Calculer les ratios et scores
                ratios = analyzer.calculate_ratios(data)
                scores = analyzer.calculate_score(ratios, secteur)
                
                # Métadonnées
                metadata = {
                    'secteur': secteur,
                    'fichier_nom': filename,
                    'source': 'excel_import'
                }
                
                # Stocker l'analyse
                store_analysis(data, ratios, scores, metadata)
                
                st.success("✅ Analyse terminée avec succès!")
                st.balloons()
                
                # Réinitialiser le flag
                st.session_state['analysis_running'] = False
                
                # Rediriger vers l'analyse
                st.rerun()
                
            finally:
                # Nettoyer le fichier temporaire
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
    
    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse : {str(e)}")
        st.session_state['analysis_running'] = False

def show_analysis_completed():
    """Affiche l'interface quand l'analyse est terminée"""
    
    st.title("📊 Analyse Terminée")
    
    # Récupérer les données
    analysis_data = SessionManager.get_analysis_data()
    if not analysis_data:
        st.error("Erreur: données d'analyse non trouvées")
        return
    
    data = analysis_data['data']
    scores = analysis_data['scores']
    metadata = analysis_data['metadata']
    
    # Afficher un résumé
    st.success(f"✅ Fichier '{metadata.get('fichier_nom', 'Inconnu')}' analysé avec succès!")
    
    # Score global
    score_global = scores.get('global', 0)
    interpretation, color = SessionManager.get_interpretation(score_global)
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: {color}20; border: 2px solid {color};">
        <h2 style="color: {color}; margin: 0;">Score Global BCEAO</h2>
        <h1 style="color: {color}; margin: 10px 0;">{score_global}/100</h1>
        <p style="color: {color}; margin: 0; font-weight: bold;">{interpretation}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Résumé financier
    st.markdown("### 📊 Résumé Financier")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ca = data.get('chiffre_affaires', 0)
        st.metric("Chiffre d'Affaires", f"{ca:,.0f} FCFA")
    
    with col2:
        rn = data.get('resultat_net', 0)
        st.metric("Résultat Net", f"{rn:,.0f} FCFA")
    
    with col3:
        actif = data.get('total_actif', 0)
        st.metric("Total Actif", f"{actif:,.0f} FCFA")
    
    with col4:
        secteur = metadata.get('secteur', '').replace('_', ' ').title()
        st.metric("Secteur", secteur)
    
    # Actions disponibles
    st.markdown("---")
    st.markdown("### 🎯 Actions Disponibles")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Analyse Complète", type="primary", use_container_width=True):
            SessionManager.set_current_page('analysis')
            st.rerun()
    
    with col2:
        if st.button("📋 Générer Rapport", use_container_width=True):
            SessionManager.set_current_page('reports')
            st.rerun()
    
    with col3:
        if st.button("📄 Nouveau Fichier", use_container_width=True):
            reset_app()
            st.rerun()
    
    with col4:
        if st.button("🏠 Accueil", use_container_width=True):
            SessionManager.set_current_page('home')
            st.rerun()

def show_upload_instructions():
    """Affiche les instructions d'upload"""
    
    with st.expander("💡 Instructions d'utilisation", expanded=False):
        st.markdown("""
        ### 📋 Format de Fichier Requis
        
        **Extensions acceptées :** .xlsx, .xls
        
        **Feuilles obligatoires :**
        - **Bilan** : Actif et Passif avec montants
        - **CR** : Compte de Résultat détaillé
        
        **Feuille optionnelle :**
        - **TFT** : Tableau des Flux de Trésorerie
        
        ### 📊 Structure Attendue
        
        **Feuille "Bilan" :**
        - Colonne E : Montants de l'actif (lignes 6-35)
        - Colonne I : Montants du passif (lignes 5-35)
        
        **Feuille "CR" :**
        - Colonne E : Montants du compte de résultat (lignes 5-46)
        
        ### ⚠️ Points d'Attention
        
        - Respecter les positions des cellules
        - Saisir uniquement des valeurs numériques
        - Éviter les cellules fusionnées
        - Vérifier l'équilibre du bilan
        
        ### 🔧 En cas de problème
        
        - Vérifiez les noms des feuilles (exactement "Bilan" et "CR")
        - Contrôlez que les cellules contiennent des nombres
        - Assurez-vous que le fichier n'est pas protégé
        """)