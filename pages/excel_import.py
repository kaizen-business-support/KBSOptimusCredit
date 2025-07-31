"""
Page d'import Excel pour OptimusCredit
Version complète avec gestion anti-réinitialisation
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
    """Affiche la page d'import Excel - Version anti-réinitialisation"""
    
    st.title("📤 Import et Analyse de Fichier Excel")
    st.markdown("---")
    
    # Initialiser les variables de session pour la persistance
    if 'uploaded_file_content' not in st.session_state:
        st.session_state['uploaded_file_content'] = None
    if 'uploaded_file_name' not in st.session_state:
        st.session_state['uploaded_file_name'] = None
    if 'analysis_in_progress' not in st.session_state:
        st.session_state['analysis_in_progress'] = False
    if 'show_sectoral' not in st.session_state:
        st.session_state['show_sectoral'] = False
    if 'show_charts' not in st.session_state:
        st.session_state['show_charts'] = False
    
    # Gérer le message de réinitialisation
    if st.session_state.get('complete_reset', False):
        st.success("🔄 Application complètement réinitialisée! Vous pouvez maintenant importer un nouveau fichier.")
        # Nettoyer les variables spécifiques à cette page
        st.session_state['uploaded_file_content'] = None
        st.session_state['uploaded_file_name'] = None
        st.session_state['analysis_in_progress'] = False
        st.session_state['show_sectoral'] = False
        st.session_state['show_charts'] = False
        # Supprimer le flag APRÈS avoir nettoyé
        del st.session_state['complete_reset']
        st.rerun()
    
    # Gérer l'état du fichier uploadé de manière persistante
    file_uploaded = st.session_state['uploaded_file_content'] is not None
    
    # Section de sélection du fichier SEULEMENT si pas déjà uploadé
    if not file_uploaded:
        st.header("📁 Sélection du Fichier")
        
        # Clé unique qui change après reset
        reset_counter = SessionManager.get_reset_counter()
        uploader_key = f"file_uploader_main_{reset_counter}"
        
        uploaded_file = st.file_uploader(
            "Sélectionnez votre fichier Excel",
            type=['xlsx', 'xls'],
            help="Le fichier doit contenir les feuilles : Bilan, CR (Compte de Résultat)",
            key=uploader_key
        )
        
        # Stocker immédiatement le fichier en session_state
        if uploaded_file is not None:
            st.session_state['uploaded_file_content'] = uploaded_file.getbuffer()
            st.session_state['uploaded_file_name'] = uploaded_file.name
            st.session_state['uploaded_file_type'] = uploaded_file.type
            st.rerun()
    
    else:
        # Afficher les infos du fichier depuis la session
        st.header("📁 Fichier Sélectionné")
        
        with st.expander("📋 Détails du fichier", expanded=True):
            st.write(f"**Nom du fichier:** {st.session_state['uploaded_file_name']}")
            st.write(f"**Taille:** {len(st.session_state['uploaded_file_content']) / 1024:.1f} KB")
            st.write(f"**Type:** {st.session_state.get('uploaded_file_type', 'Excel')}")
            st.success("✅ Fichier en mémoire - Prêt pour l'analyse")
        
        # Sélection du secteur (PERSISTENT)
        st.header("🏭 Secteur d'Activité")
        
        reset_counter = SessionManager.get_reset_counter()
        secteur_key = f"secteur_selector_{reset_counter}"
        
        secteur = st.selectbox(
            "Sélectionnez votre secteur pour la comparaison :",
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
            key=secteur_key
        )
        
        # Analyse SEULEMENT si pas déjà faite
        analysis_done = SessionManager.has_analysis_data()
        
        if not analysis_done and not st.session_state['analysis_in_progress']:
            analyze_key = f"analyze_btn_{reset_counter}"
            if st.button("🔍 Analyser le fichier", type="primary", use_container_width=True, key=analyze_key):
                st.session_state['analysis_in_progress'] = True
                analyze_uploaded_file(
                    st.session_state['uploaded_file_content'], 
                    st.session_state['uploaded_file_name'], 
                    secteur
                )
        
        elif st.session_state['analysis_in_progress'] and not analysis_done:
            st.info("🔄 Analyse en cours... Veuillez patienter.")
        
        elif analysis_done:
            show_persistent_analysis_summary()
        
        # Boutons d'action
        st.markdown("---")
        
        if analysis_done:
            st.info("💡 **Analyse complète disponible** : Utilisez le menu de navigation dans la barre latérale pour accéder aux détails complets, graphiques interactifs et recommandations.")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                new_file_key = f"new_file_btn_{reset_counter}"
                if st.button("📄 Nouveau Fichier", use_container_width=True, key=new_file_key):
                    reset_app()
                    st.rerun()
            
            with col2:
                compare_key = f"compare_sector_btn_{reset_counter}"
                if st.button("🔄 Comparer Secteur", use_container_width=True, key=compare_key):
                    st.session_state['show_sectoral'] = not st.session_state['show_sectoral']
            
            with col3:
                charts_key = f"show_charts_btn_{reset_counter}"
                if st.button("📈 Graphiques", use_container_width=True, key=charts_key):
                    st.session_state['show_charts'] = not st.session_state['show_charts']
            
            with col4:
                goto_key = f"goto_analysis_btn_{reset_counter}"
                if st.button("📊 Analyse Complète", use_container_width=True, key=goto_key, type="primary"):
                    SessionManager.set_current_page('analysis')
                    st.rerun()
            
            # Affichage conditionnel
            if st.session_state.get('show_sectoral', False):
                st.markdown("---")
                st.subheader(f"🔄 Comparaison Sectorielle - {secteur.replace('_', ' ').title()}")
                show_sectoral_comparison_persistent()
            
            if st.session_state.get('show_charts', False):
                st.markdown("---")
                st.subheader("📈 Graphiques Rapides")
                show_quick_charts_persistent()
        
        else:
            st.info("📊 Cliquez sur 'Analyser le fichier' pour commencer l'analyse")
    
    # Afficher les instructions si aucun fichier ET aucune analyse
    if not file_uploaded and not SessionManager.has_analysis_data():
        show_instructions()

def analyze_uploaded_file(file_content, filename, secteur):
    """Analyse le fichier uploadé stocké en mémoire"""
    
    with st.spinner("📊 Extraction et analyse des données en cours..."):
        temp_file_path = None
        
        try:
            # Créer un fichier temporaire depuis le contenu en mémoire
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(file_content)
                temp_file_path = tmp_file.name
            
            # Importer l'analyseur
            try:
                from modules.core.analyzer import FinancialAnalyzer
            except ImportError as e:
                st.error(f"❌ Impossible d'importer FinancialAnalyzer: {e}")
                st.session_state['analysis_in_progress'] = False
                return
            
            # Créer l'analyseur et analyser
            analyzer = FinancialAnalyzer()
            data = analyzer.load_excel_template(temp_file_path)
            
            if data is None:
                st.error("❌ Erreur lors du chargement du fichier Excel")
                st.error("Vérifiez que le fichier contient les feuilles 'Bilan' et 'CR' avec les données aux bonnes positions")
                st.session_state['analysis_in_progress'] = False
                return
            
            # Calculer les ratios et scores
            ratios = analyzer.calculate_ratios(data)
            scores = analyzer.calculate_score(ratios, secteur)
            
            # Stockage via SessionManager
            metadata = {
                'secteur': secteur,
                'fichier_nom': filename,
                'source': 'excel_import'
            }
            
            store_analysis(data, ratios, scores, metadata)
            
            st.session_state['analysis_in_progress'] = False
            st.success("✅ Fichier analysé avec succès!")
            st.rerun()
                
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement: {str(e)}")
            st.session_state['analysis_in_progress'] = False
            
        finally:
            # Nettoyer le fichier temporaire
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except:
                    pass

def show_persistent_analysis_summary():
    """Affiche un résumé persistant des résultats"""
    
    analysis_data = SessionManager.get_analysis_data()
    if not analysis_data:
        return
    
    data = analysis_data['data']
    ratios = analysis_data['ratios']
    scores = analysis_data['scores']
    metadata = analysis_data['metadata']
    
    st.markdown("---")
    st.header("📊 Résumé de l'Analyse")
    
    # Afficher le nom du fichier
    filename = metadata.get('fichier_nom', 'Fichier analysé')
    st.info(f"📄 **Fichier analysé:** {filename}")
    
    # Score global
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        score_global = scores.get('global', 0)
        interpretation, color = SessionManager.get_interpretation(score_global)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: {color}20; border: 2px solid {color};">
            <h2 style="color: {color}; margin: 0;">Score Global BCEAO</h2>
            <h1 style="color: {color}; margin: 10px 0;">{score_global}/100</h1>
            <p style="color: {color}; margin: 0; font-weight: bold;">{interpretation}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Scores détaillés
    st.subheader("📈 Scores par Catégorie")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    categories = [
        ("💧 Liquidité", scores.get('liquidite', 0), 40),
        ("🏛️ Solvabilité", scores.get('solvabilite', 0), 40),
        ("📈 Rentabilité", scores.get('rentabilite', 0), 30),
        ("⚡ Activité", scores.get('activite', 0), 15),
        ("🔧 Gestion", scores.get('gestion', 0), 15)
    ]
    
    for i, (label, score, max_score) in enumerate(categories):
        with [col1, col2, col3, col4, col5][i]:
            percentage = (score / max_score) * 100
            st.metric(label, f"{score}/{max_score}", f"{percentage:.0f}%")
    
    # Indicateurs financiers clés
    st.subheader("💰 Indicateurs Financiers Clés")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ca_value = data.get('chiffre_affaires', 0)
        ta_value = data.get('total_actif', 0)
        st.metric("Chiffre d'Affaires", f"{ca_value:,.0f}".replace(',', ' ') + " FCFA")
        st.metric("Total Actif", f"{ta_value:,.0f}".replace(',', ' ') + " FCFA")
    
    with col2:
        rn_value = data.get('resultat_net', 0)
        cp_value = data.get('capitaux_propres', 0)
        st.metric("Résultat Net", f"{rn_value:,.0f}".replace(',', ' ') + " FCFA")
        st.metric("Capitaux Propres", f"{cp_value:,.0f}".replace(',', ' ') + " FCFA")
    
    # Ratios clés
    st.subheader("📊 Ratios Clés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        liquidite = ratios.get('ratio_liquidite_generale', 0)
        status = get_ratio_status(liquidite, 1.5, higher_is_better=True)
        st.metric("Liquidité Générale", f"{liquidite:.2f}", status)
    
    with col2:
        autonomie = ratios.get('ratio_autonomie_financiere', 0)
        status = get_ratio_status(autonomie, 30, higher_is_better=True)
        st.metric("Autonomie Financière", f"{autonomie:.1f}%", status)
    
    with col3:
        roe = ratios.get('roe', 0)
        status = get_ratio_status(roe, 10, higher_is_better=True)
        st.metric("ROE", f"{roe:.1f}%", status)
    
    with col4:
        marge_nette = ratios.get('marge_nette', 0)
        status = get_ratio_status(marge_nette, 5, higher_is_better=True)
        st.metric("Marge Nette", f"{marge_nette:.1f}%", status)

def show_sectoral_comparison_persistent():
    """Affiche la comparaison sectorielle de manière persistante"""
    
    analysis_data = SessionManager.get_analysis_data()
    if not analysis_data:
        return
    
    ratios = analysis_data['ratios']
    secteur = analysis_data['metadata'].get('secteur')
    
    if not secteur:
        st.warning("Secteur non spécifié")
        return
    
    # Données sectorielles simplifiées
    sectoral_benchmarks = {
        'industrie_manufacturiere': {
            'ratio_liquidite_generale': {'q1': 1.2, 'median': 1.8, 'q3': 2.5},
            'ratio_autonomie_financiere': {'q1': 25, 'median': 40, 'q3': 55},
            'roe': {'q1': 8, 'median': 15, 'q3': 22},
            'marge_nette': {'q1': 2, 'median': 4.5, 'q3': 8}
        }
    }
    
    if secteur not in sectoral_benchmarks:
        st.info("Données sectorielles non disponibles pour ce secteur")
        return
    
    benchmarks = sectoral_benchmarks[secteur]
    comparison_data = []
    
    key_ratios = {
        'ratio_liquidite_generale': 'Liquidité Générale',
        'ratio_autonomie_financiere': 'Autonomie Financière (%)',
        'roe': 'ROE (%)',
        'marge_nette': 'Marge Nette (%)'
    }
    
    for ratio_key, ratio_name in key_ratios.items():
        if ratio_key in ratios and ratio_key in benchmarks:
            entreprise_val = ratios[ratio_key]
            benchmark = benchmarks[ratio_key]
            
            # Déterminer la position
            if entreprise_val >= benchmark['q3']:
                position = "🟢 Top 25%"
            elif entreprise_val >= benchmark['median']:
                position = "🟡 Au-dessus médiane"
            elif entreprise_val >= benchmark['q1']:
                position = "🟠 Sous médiane"
            else:
                position = "🔴 Bottom 25%"
            
            comparison_data.append({
                'Ratio': ratio_name,
                'Votre Valeur': f"{entreprise_val:.2f}",
                'Médiane Secteur': f"{benchmark['median']:.2f}",
                'Votre Position': position
            })
    
    if comparison_data:
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, hide_index=True, use_container_width=True)

def show_quick_charts_persistent():
    """Affiche des graphiques rapides de manière persistante"""
    
    analysis_data = SessionManager.get_analysis_data()
    if not analysis_data:
        return
    
    data = analysis_data['data']
    ratios = analysis_data['ratios']
    scores = analysis_data['scores']
    
    # Version simplifiée sans plotly pour éviter les erreurs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Liquidité**")
        st.metric("Générale", f"{ratios.get('ratio_liquidite_generale', 0):.2f}")
        st.metric("Immédiate", f"{ratios.get('ratio_liquidite_immediate', 0):.2f}")
    
    with col2:
        st.markdown("**Rentabilité**")
        st.metric("ROE", f"{ratios.get('roe', 0):.1f}%")
        st.metric("Marge Nette", f"{ratios.get('marge_nette', 0):.1f}%")
    
    with col3:
        st.markdown("**Performance**")
        st.metric("Score Global", f"{scores.get('global', 0)}/100")
        st.metric("Classe", SessionManager.get_financial_class(scores.get('global', 0)))

def get_ratio_status(value, threshold, higher_is_better=True):
    """Retourne le statut d'un ratio"""
    if higher_is_better:
        if value >= threshold * 1.2:
            return "✅ Excellent"
        elif value >= threshold:
            return "✅ Bon"
        elif value >= threshold * 0.8:
            return "⚠️ Acceptable"
        else:
            return "❌ Faible"
    else:
        if value <= threshold * 0.8:
            return "✅ Excellent"
        elif value <= threshold:
            return "✅ Bon"
        elif value <= threshold * 1.2:
            return "⚠️ Acceptable"
        else:
            return "❌ Faible"

def show_instructions():
    """Affiche les instructions d'utilisation"""
    
    st.markdown("---")
    st.header("📋 Instructions d'Utilisation")
    
    with st.expander("💡 Comment utiliser cette page", expanded=True):
        st.markdown("""
        ### 📤 **Étapes d'Import et d'Analyse**
        
        1. **Préparez votre fichier Excel** au format BCEAO
           - Feuille "Bilan" avec les postes d'actif et passif
           - Feuille "CR" avec le compte de résultat
           - Feuille "TFT" (optionnelle) pour les flux de trésorerie
        
        2. **Uploadez votre fichier**
           - Cliquez sur "Browse files" ou glissez-déposez
           - Formats acceptés : .xlsx, .xls
           - Le fichier sera automatiquement sauvegardé en mémoire
        
        3. **Sélectionnez votre secteur d'activité**
           - Choisissez le secteur le plus proche de votre activité
           - Cela permettra une comparaison sectorielle
        
        4. **Lancez l'analyse**
           - Cliquez sur "Analyser le fichier"
           - L'analyse prend généralement 5-10 secondes
        
        5. **Consultez les résultats**
           - Score global et détaillé
           - Ratios financiers calculés
           - Options d'affichage : comparaison sectorielle, graphiques
        
        ### 🔒 **Avantages de cette version :**
        
        - **Persistance totale** : Le fichier reste en mémoire
        - **Pas de réinitialisation** : Les boutons ne font plus perdre le fichier
        - **Navigation sûre** : Vous pouvez naviguer entre les pages
        - **Reset contrôlé** : Seul "Nouveau Fichier" remet à zéro
        """)