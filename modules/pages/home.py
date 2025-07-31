"""
Page d'accueil de l'application d'analyse financière BCEAO
Version complète avec SessionManager intégré
"""

import streamlit as st
from datetime import datetime

# Import du gestionnaire de session centralisé
try:
    from session_manager import SessionManager, store_analysis
except ImportError:
    st.error("❌ Impossible d'importer session_manager.py")
    st.stop()

def show_home_page():
    """Affiche la page d'accueil avec présentation de l'outil"""
    
    st.title("🏦 Outil d'Analyse Financière BCEAO")
    st.markdown("### *Analyse conforme aux normes prudentielles de la Banque Centrale des États de l'Afrique de l'Ouest*")
    
    # Hero section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 🎯 **Analyse Financière Professionnelle**
        
        Cet outil vous permet d'analyser la santé financière de votre entreprise selon les **normes BCEAO** 
        avec un scoring automatique, des comparaisons sectorielles et des recommandations personnalisées.
        
        ### ✨ **Fonctionnalités Principales**
        
        🔹 **Import Excel** : Compatible avec les modèles BCEAO standard  
        🔹 **Scoring sur 100** : Évaluation selon 5 catégories (liquidité, solvabilité, rentabilité, activité, gestion)  
        🔹 **25+ Ratios** : Calculs automatiques avec interprétation  
        🔹 **Comparaisons sectorielles** : Benchmarks par quartiles pour 6 secteurs  
        🔹 **Recommandations** : Plan d'action personnalisé sur 6 mois  
        🔹 **Rapports professionnels** : Export PDF, Excel et JSON  
        """)
    
    with col2:
        # Affichage du statut de l'analyse actuelle
        if SessionManager.has_analysis_data():
            score, metadata = SessionManager.get_analysis_info()
            interpretation, color = SessionManager.get_interpretation(score)
            
            st.markdown(f"""
            <div style="
                text-align: center; 
                padding: 20px; 
                border-radius: 10px; 
                background-color: {color}20; 
                border: 2px solid {color};
                margin-bottom: 20px;
            ">
                <h3 style="color: {color}; margin: 0;">📊 Analyse Actuelle</h3>
                <h2 style="color: {color}; margin: 10px 0;">{score}/100</h2>
                <p style="color: {color}; margin: 0; font-weight: bold;">{interpretation}</p>
                <p style="color: {color}; margin: 5px 0; font-size: 0.9em;">
                    Secteur: {metadata.get('secteur', 'N/A').replace('_', ' ').title()}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("💡 **Analyse disponible** - Utilisez la navigation pour consulter les détails complets.")
        else:
            st.markdown("""
            <div style="
                text-align: center; 
                padding: 20px; 
                border-radius: 10px; 
                background-color: #e3f2fd; 
                border: 2px solid #2196f3;
                margin-bottom: 20px;
            ">
                <h3 style="color: #1976d2; margin: 0;">🚀 Commencer l'Analyse</h3>
                <p style="color: #1976d2; margin: 10px 0;">
                    Importez votre fichier Excel ou saisissez manuellement vos données
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Actions rapides
    st.markdown("---")
    st.subheader("🚀 Actions Rapides")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📤 Import Excel", use_container_width=True, type="primary"):
            SessionManager.set_current_page('excel_import')
            st.rerun()
    
    with col2:
        if st.button("✏️ Saisie Manuelle", use_container_width=True):
            SessionManager.set_current_page('manual_input')
            st.rerun()
    
    with col3:
        if SessionManager.has_analysis_data():
            if st.button("📊 Voir Analyse", use_container_width=True):
                SessionManager.set_current_page('analysis')
                st.rerun()
        else:
            st.button("📊 Voir Analyse", use_container_width=True, disabled=True, help="Aucune analyse disponible")
    
    with col4:
        if st.button("📚 Démonstration", use_container_width=True):
            launch_demo()
    
    # Guide d'utilisation
    st.markdown("---")
    st.subheader("📋 Guide d'Utilisation")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Vue d'ensemble", "📤 Import Excel", "✏️ Saisie Manuelle", "📊 Analyse"])
    
    with tab1:
        show_overview_guide()
    
    with tab2:
        show_excel_guide()
    
    with tab3:
        show_manual_guide()
    
    with tab4:
        show_analysis_guide()
    
    # Informations sur les normes BCEAO
    show_bceao_info()

def launch_demo():
    """Lance une démonstration avec des données d'exemple"""
    
    with st.spinner("🚀 Chargement de la démonstration..."):
        # Données d'exemple d'une PME industrielle
        demo_data = {
            'total_actif': 1400000,
            'immobilisations_nettes': 800000,
            'stocks': 150000,
            'creances_clients': 200000,
            'autres_creances': 50000,
            'tresorerie': 200000,
            'capitaux_propres': 600000,
            'dettes_financieres': 400000,
            'dettes_court_terme': 250000,
            'tresorerie_passif': 50000,
            'fournisseurs_exploitation': 120000,
            'dettes_sociales_fiscales': 80000,
            'autres_dettes': 50000,
            'chiffre_affaires': 1500000,
            'valeur_ajoutee': 600000,
            'excedent_brut': 200000,
            'resultat_exploitation': 120000,
            'resultat_net': 80000,
            'charges_personnel': 400000,
            'dotations_amortissements': 80000,
            'frais_financiers': 30000,
            'charges_exploitation': 900000,
            'cafg': 160000,
            # Détails du bilan
            'terrains': 200000,
            'batiments': 400000,
            'materiel_mobilier': 200000,
            'capital': 200000,
            'reserves': 320000,
            'emprunts_dettes_financieres': 400000,
            'total_actif_circulant': 400000,
            'ressources_stables': 1000000,
            # Données du compte de résultat
            'achats_matieres_premieres': 600000,
            'autres_charges': 200000,
            'revenus_financiers': 10000,
            'impots_resultat': 20000,
            'resultat_financier': -20000,
            # Flux de trésorerie
            'flux_activites_operationnelles': 100000,
            'flux_activites_investissement': -50000,
            'flux_activites_financement': -30000,
            'variation_tresorerie': 20000
        }
        
        try:
            # Importer l'analyseur
            from modules.core.analyzer import FinancialAnalyzer
            
            # Créer l'analyseur
            analyzer = FinancialAnalyzer()
            
            # Calculer les ratios
            ratios = analyzer.calculate_ratios(demo_data)
            
            # Calculer les scores
            scores = analyzer.calculate_score(ratios, 'industrie_manufacturiere')
            
            # Métadonnées de la démonstration
            metadata = {
                'secteur': 'industrie_manufacturiere',
                'fichier_nom': 'Démonstration - PME Industrielle',
                'source': 'demonstration',
                'mode_saisie': 'demo'
            }
            
            # Stocker l'analyse via SessionManager
            store_analysis(demo_data, ratios, scores, metadata)
            
            st.success("✅ Démonstration chargée avec succès!")
            st.info("🎯 **PME Industrielle** - Données d'exemple pour découvrir l'outil")
            
            # Afficher un aperçu rapide
            score_global = scores.get('global', 0)
            interpretation, color = SessionManager.get_interpretation(score_global)
            
            st.markdown(f"""
            ### 📊 Aperçu de la Démonstration
            
            **Entreprise fictive :** PME dans l'industrie manufacturière  
            **Score BCEAO :** {score_global}/100 - {interpretation}  
            **Classe :** {SessionManager.get_financial_class(score_global)}
            """)
            
            # Boutons d'action
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Voir l'Analyse Complète", key="demo_goto_analysis", type="primary"):
                    SessionManager.set_current_page('analysis')
                    st.rerun()
            
            with col2:
                if st.button("📋 Générer Rapport", key="demo_goto_reports"):
                    SessionManager.set_current_page('reports')
                    st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement de la démonstration: {str(e)}")
            st.error("Assurez-vous que le module analyzer est disponible.")

def show_overview_guide():
    """Affiche le guide de vue d'ensemble"""
    
    st.markdown("""
    ### 🎯 Vue d'Ensemble de l'Outil
    
    **Objectif :** Analyser la santé financière d'une entreprise selon les normes BCEAO
    
    **Processus en 4 étapes :**
    
    1. **📤 Import des données**
       - Fichier Excel au format BCEAO
       - Saisie manuelle détaillée
    
    2. **⚙️ Calculs automatiques**
       - 25+ ratios financiers
       - Score global sur 100 points
       - Classification en 5 catégories
    
    3. **📊 Analyse comparative**
       - Benchmarks sectoriels
       - Normes prudentielles BCEAO
       - Identification des forces/faiblesses
    
    4. **📋 Recommandations**
       - Plan d'action personnalisé
       - Priorités par urgence
       - Indicateurs de suivi
    
    **Secteurs supportés :**
    - Industrie manufacturière
    - Commerce (détail/gros)
    - Services professionnels
    - Construction/BTP
    - Agriculture
    """)

def show_excel_guide():
    """Affiche le guide d'import Excel"""
    
    st.markdown("""
    ### 📤 Guide d'Import Excel
    
    **Format requis :**
    - Extension : .xlsx ou .xls
    - Feuilles obligatoires : "Bilan", "CR" (Compte de Résultat)
    - Feuille optionnelle : "TFT" (Tableau de Flux de Trésorerie)
    
    **Structure du fichier :**
    
    **Feuille "Bilan" :**
    - Colonnes E : Montants de l'actif
    - Colonnes I : Montants du passif
    - Postes détaillés : immobilisations, stocks, créances, dettes...
    
    **Feuille "CR" :**
    - Soldes intermédiaires de gestion
    - Chiffre d'affaires, charges, résultats
    - Structure conforme au plan comptable OHADA
    
    **Conseils :**
    - Utilisez le modèle BCEAO fourni
    - Vérifiez l'équilibre du bilan
    - Contrôlez la cohérence des montants
    - Sauvegardez en format Excel (.xlsx)
    """)

def show_manual_guide():
    """Affiche le guide de saisie manuelle"""
    
    st.markdown("""
    ### ✏️ Guide de Saisie Manuelle
    
    **Avantages :**
    - Contrôle total des données
    - Validation en temps réel
    - Aide contextuelle
    - Calculs automatiques
    
    **Étapes de saisie :**
    
    1. **Bilan - Actif :**
       - Immobilisations nettes
       - Stocks et en-cours
       - Créances clients
       - Trésorerie
    
    2. **Bilan - Passif :**
       - Capitaux propres
       - Dettes financières
       - Dettes d'exploitation
       - Découverts bancaires
    
    3. **Compte de Résultat :**
       - Chiffre d'affaires
       - Charges d'exploitation
       - Charges financières
       - Résultat net
    
    **Validations automatiques :**
    - Équilibre du bilan (Actif = Passif)
    - Cohérence résultat net
    - Vérification des montants
    """)

def show_analysis_guide():
    """Affiche le guide d'analyse"""
    
    st.markdown("""
    ### 📊 Guide d'Analyse des Résultats
    
    **Score Global BCEAO (sur 100) :**
    - 85-100 : Excellence financière (Classe A+)
    - 70-84 : Très bonne situation (Classe A)
    - 55-69 : Bonne situation (Classe B)
    - 40-54 : Situation moyenne (Classe C)
    - 25-39 : Situation faible (Classe D)
    - 0-24 : Situation critique (Classe E)
    
    **Catégories d'évaluation :**
    
    **💧 Liquidité (40 points) :**
    - Capacité à honorer les engagements à court terme
    - Ratios : liquidité générale, immédiate, BFR
    
    **🏛️ Solvabilité (40 points) :**
    - Solidité de la structure financière
    - Ratios : autonomie, endettement, couverture
    
    **📈 Rentabilité (30 points) :**
    - Performance économique et financière
    - Ratios : ROE, ROA, marges
    
    **⚡ Activité (15 points) :**
    - Efficacité d'utilisation des actifs
    - Ratios : rotation, délais de recouvrement
    
    **🔧 Gestion (15 points) :**
    - Efficacité de la gestion opérationnelle
    - Ratios : productivité, charges/VA
    """)

def show_bceao_info():
    """Affiche les informations sur les normes BCEAO"""
    
    st.markdown("---")
    st.subheader("📚 Normes et Références BCEAO")
    
    with st.expander("🏛️ À propos de la BCEAO"):
        st.markdown("""
        ### Banque Centrale des États de l'Afrique de l'Ouest
        
        La BCEAO est l'institution d'émission monétaire commune aux huit États membres de l'UEMOA :
        - Bénin
        - Burkina Faso
        - Côte d'Ivoire
        - Guinée-Bissau
        - Mali
        - Niger
        - Sénégal
        - Togo
        
        **Mission :** Définir et conduire la politique monétaire de l'Union, superviser le système bancaire
        et veiller à la stabilité financière.
        """)
    
    with st.expander("📋 Normes Prudentielles"):
        st.markdown("""
        ### Principales Normes Prudentielles BCEAO
        
        **Solvabilité :**
        - Ratio de fonds propres de base : ≥ 5% (objectif 7%)
        - Ratio de fonds propres Tier 1 : ≥ 6,625% (objectif 8,5%)
        - Ratio de solvabilité global : ≥ 8,625% (objectif 11,5%)
        
        **Liquidité :**
        - Ratio de liquidité court terme : ≥ 75%
        - Coefficient de couverture des emplois MLT : ≥ 100%
        - Ratio de transformation : ≤ 100%
        
        **Division des risques :**
        - Division des risques : ≤ 65% des fonds propres
        - Limite des grands risques : ≤ 8 fois les fonds propres
        - Engagements sur apparentés : ≤ 20%
        """)
    
    with st.expander("🔗 Ressources Utiles"):
        st.markdown("""
        ### Liens et Documentation
        
        - **Site officiel BCEAO :** https://www.bceao.int
        - **Réglementation prudentielle :** Instruction n°001-01-2017
        - **Plan comptable OHADA :** Acte uniforme du 23 mars 2000
        - **Guide méthodologique :** Manuel d'analyse financière BCEAO
        
        ### Support Technique
        
        Pour toute question sur l'utilisation de cet outil :
        - **Email :** contact@kaizen-corporation.com
        - **Téléphone :** +221 75 645 45 00
        - **Horaires :** Lundi-Vendredi 8h-17h (GMT)
        """)
    
    # Statistiques d'utilisation (fictives pour la démonstration)
    st.markdown("---")
    st.subheader("📊 Statistiques d'Utilisation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Entreprises Analysées", "2,847", "↗️ +12%")
    
    with col2:
        st.metric("Analyses ce Mois", "184", "↗️ +8%")
    
    with col3:
        st.metric("Score Moyen Secteur", "67/100", "↗️ +3pts")
    
    with col4:
        st.metric("Taux de Conformité", "78%", "↗️ +5%")