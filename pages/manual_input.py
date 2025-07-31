"""
Page de saisie manuelle pour OptimusCredit
Version complète avec validation et analyse intégrée
"""

import streamlit as st
from datetime import datetime

# Import du gestionnaire de session centralisé
try:
    from session_manager import SessionManager, store_analysis
except ImportError:
    st.error("❌ Impossible d'importer session_manager.py")
    st.stop()

def show_manual_input_page():
    """Affiche la page de saisie manuelle avec SessionManager"""
    
    st.title("✏️ Saisie Manuelle des Données Financières")
    st.markdown("---")
    
    st.info("💡 Saisissez vos données financières pour obtenir une analyse complète selon les normes BCEAO")
    
    # Sélection du secteur
    st.header("🏭 Secteur d'Activité")
    secteur = st.selectbox(
        "Sélectionnez votre secteur d'activité :",
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
        }.get(x, x)
    )
    
    # Onglets pour organiser la saisie
    tab_bilan, tab_cr, tab_flux = st.tabs([
        "📊 Bilan", "📈 Compte de Résultat", "💰 Flux de Trésorerie"
    ])
    
    # Initialiser les données
    data = {}
    
    with tab_bilan:
        st.header("📊 Bilan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("ACTIF")
            
            st.markdown("**Immobilisations (en FCFA)**")
            data['immobilisations_nettes'] = st.number_input(
                "Immobilisations nettes", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Valeur nette des immobilisations après amortissements"
            )
            
            st.markdown("**Actif Circulant (en FCFA)**")
            data['stocks'] = st.number_input(
                "Stocks", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Stocks de marchandises, matières premières et produits finis"
            )
            
            data['creances_clients'] = st.number_input(
                "Créances clients", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Montant dû par les clients"
            )
            
            data['autres_creances'] = st.number_input(
                "Autres créances", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Autres créances (TVA, avances, etc.)"
            )
            
            st.markdown("**Trésorerie (en FCFA)**")
            data['tresorerie'] = st.number_input(
                "Banques et caisses", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Disponibilités en banque et en caisse"
            )
            
            # Calcul total actif circulant
            data['total_actif_circulant'] = data['stocks'] + data['creances_clients'] + data['autres_creances']
            
            # Total actif
            data['total_actif'] = data['immobilisations_nettes'] + data['total_actif_circulant'] + data['tresorerie']
            
            st.markdown("---")
            st.metric("**TOTAL ACTIF**", f"{data['total_actif']:,.0f} FCFA")
        
        with col2:
            st.subheader("PASSIF")
            
            st.markdown("**Capitaux Propres (en FCFA)**")
            data['capital'] = st.number_input(
                "Capital social", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Capital social de l'entreprise"
            )
            
            data['reserves'] = st.number_input(
                "Réserves", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Réserves accumulées"
            )
            
            data['resultat_net'] = st.number_input(
                "Résultat net", 
                value=0.0, 
                format="%.0f",
                help="Résultat net de l'exercice (peut être négatif)"
            )
            
            # Calcul capitaux propres
            data['capitaux_propres'] = data['capital'] + data['reserves'] + data['resultat_net']
            
            st.markdown("**Dettes (en FCFA)**")
            data['dettes_financieres'] = st.number_input(
                "Dettes financières", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Emprunts bancaires et autres dettes financières"
            )
            
            data['fournisseurs_exploitation'] = st.number_input(
                "Dettes fournisseurs", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Montant dû aux fournisseurs"
            )
            
            data['dettes_sociales_fiscales'] = st.number_input(
                "Dettes sociales et fiscales", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Dettes envers l'administration (CNSS, impôts, etc.)"
            )
            
            data['autres_dettes'] = st.number_input(
                "Autres dettes", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Autres dettes à court terme"
            )
            
            data['tresorerie_passif'] = st.number_input(
                "Découverts bancaires", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Découverts et crédits de trésorerie"
            )
            
            # Calculs
            data['dettes_court_terme'] = (
                data['fournisseurs_exploitation'] + 
                data['dettes_sociales_fiscales'] + 
                data['autres_dettes']
            )
            
            total_passif = (
                data['capitaux_propres'] + 
                data['dettes_financieres'] + 
                data['dettes_court_terme'] + 
                data['tresorerie_passif']
            )
            
            st.markdown("---")
            st.metric("**TOTAL PASSIF**", f"{total_passif:,.0f} FCFA")
            
            # Vérification équilibre
            equilibre = abs(data['total_actif'] - total_passif)
            if equilibre < 1000:
                st.success(f"✅ Bilan équilibré (écart: {equilibre:,.0f})")
            else:
                st.error(f"❌ Bilan déséquilibré (écart: {equilibre:,.0f})")
    
    with tab_cr:
        st.header("📈 Compte de Résultat")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("PRODUITS")
            
            st.markdown("**Chiffre d'Affaires (en FCFA)**")
            data['chiffre_affaires'] = st.number_input(
                "Chiffre d'affaires", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Chiffre d'affaires total de l'exercice"
            )
            
            data['autres_produits'] = st.number_input(
                "Autres produits d'exploitation", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Subventions, reprises de provisions, etc."
            )
            
            st.markdown("**Produits Financiers (en FCFA)**")
            data['revenus_financiers'] = st.number_input(
                "Revenus financiers", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Intérêts, dividendes reçus, etc."
            )
        
        with col2:
            st.subheader("CHARGES")
            
            st.markdown("**Charges d'Exploitation (en FCFA)**")
            data['achats_matieres_premieres'] = st.number_input(
                "Achats matières premières", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Achats de matières premières et marchandises"
            )
            
            data['charges_personnel'] = st.number_input(
                "Charges de personnel", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Salaires, charges sociales, etc."
            )
            
            data['autres_charges'] = st.number_input(
                "Autres charges d'exploitation", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Loyers, assurances, services extérieurs, etc."
            )
            
            data['dotations_amortissements'] = st.number_input(
                "Dotations aux amortissements", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Amortissements des immobilisations"
            )
            
            st.markdown("**Charges Financières (en FCFA)**")
            data['frais_financiers'] = st.number_input(
                "Frais financiers", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Intérêts sur emprunts, frais bancaires, etc."
            )
            
            data['impots_resultat'] = st.number_input(
                "Impôts sur le résultat", 
                min_value=0.0, 
                value=0.0, 
                format="%.0f",
                help="Impôts sur les bénéfices"
            )
        
        # Calculs du compte de résultat
        total_produits = data['chiffre_affaires'] + data['autres_produits'] + data['revenus_financiers']
        
        data['charges_exploitation'] = (
            data['achats_matieres_premieres'] + 
            data['charges_personnel'] + 
            data['autres_charges'] + 
            data['dotations_amortissements']
        )
        
        total_charges = data['charges_exploitation'] + data['frais_financiers'] + data['impots_resultat']
        
        # Soldes intermédiaires
        data['valeur_ajoutee'] = data['chiffre_affaires'] - data['achats_matieres_premieres']
        data['excedent_brut'] = data['valeur_ajoutee'] - data['charges_personnel']
        data['resultat_exploitation'] = data['excedent_brut'] - data['autres_charges'] - data['dotations_amortissements']
        data['resultat_financier'] = data['revenus_financiers'] - data['frais_financiers']
        
        # Cohérence avec le résultat net du bilan
        resultat_calcule = data['resultat_exploitation'] + data['resultat_financier'] - data['impots_resultat']
        if abs(resultat_calcule - data['resultat_net']) > 1000:
            st.warning(f"⚠️ Incohérence détectée: Résultat calculé ({resultat_calcule:,.0f}) vs Résultat bilan ({data['resultat_net']:,.0f})")
        
        st.markdown("---")
        
        # Affichage des soldes
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Valeur Ajoutée", f"{data['valeur_ajoutee']:,.0f} FCFA")
        with col2:
            st.metric("EBE", f"{data['excedent_brut']:,.0f} FCFA")
        with col3:
            st.metric("Résultat d'Exploitation", f"{data['resultat_exploitation']:,.0f} FCFA")
    
    with tab_flux:
        st.header("💰 Flux de Trésorerie")
        
        st.markdown("**Capacité d'Autofinancement et Flux (en FCFA)**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            data['cafg'] = st.number_input(
                "CAFG (Capacité d'autofinancement)", 
                value=data.get('resultat_net', 0) + data.get('dotations_amortissements', 0), 
                format="%.0f",
                help="Généralement : Résultat net + Dotations aux amortissements"
            )
            
            data['flux_activites_operationnelles'] = st.number_input(
                "Flux des activités opérationnelles", 
                value=data.get('cafg', 0), 
                format="%.0f",
                help="CAFG - variation du BFR"
            )
        
        with col2:
            data['flux_activites_investissement'] = st.number_input(
                "Flux des activités d'investissement", 
                value=0.0, 
                format="%.0f",
                help="Généralement négatif (acquisitions d'immobilisations)"
            )
            
            data['flux_activites_financement'] = st.number_input(
                "Flux des activités de financement", 
                value=0.0, 
                format="%.0f",
                help="Emprunts contractés - remboursements - dividendes"
            )
    
    # Validation et analyse
    st.markdown("---")
    st.header("🔍 Validation et Analyse")
    
    # Vérifications de base
    errors, warnings = validate_financial_data(data)
    
    # Affichage des erreurs et avertissements
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    
    if warnings:
        for warning in warnings:
            st.warning(f"⚠️ {warning}")
    
    # Bouton d'analyse
    if not errors:
        if st.button("🔍 Lancer l'Analyse Financière", type="primary", use_container_width=True):
            
            with st.spinner("📊 Analyse en cours..."):
                try:
                    # Importer l'analyseur
                    from modules.core.analyzer import FinancialAnalyzer
                    
                    # Créer l'analyseur
                    analyzer = FinancialAnalyzer()
                    
                    # Calculer les ratios
                    ratios = analyzer.calculate_ratios(data)
                    
                    # Calculer les scores
                    scores = analyzer.calculate_score(ratios, secteur)
                    
                    # Utiliser SessionManager pour stocker
                    metadata = {
                        'secteur': secteur,
                        'source': 'manual_input',
                        'mode_saisie': 'manuelle'
                    }
                    
                    # Stocker via le gestionnaire centralisé
                    store_analysis(data, ratios, scores, metadata)
                    
                    st.success("✅ Analyse financière réalisée avec succès!")
                    
                    # Afficher un résumé rapide
                    score_global = scores.get('global', 0)
                    interpretation, color = SessionManager.get_interpretation(score_global)
                    
                    st.markdown(f"""
                    ### 📊 Résultat de l'Analyse
                    
                    **Score Global BCEAO:** {score_global}/100  
                    **Évaluation:** {interpretation}  
                    **Classe:** {SessionManager.get_financial_class(score_global)}
                    """)
                    
                    # Proposition de navigation
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("📊 Voir l'Analyse Complète", key="goto_analysis", type="primary"):
                            SessionManager.set_current_page('analysis')
                            st.rerun()
                    
                    with col2:
                        if st.button("📋 Générer un Rapport", key="goto_reports", type="secondary"):
                            SessionManager.set_current_page('reports')
                            st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'analyse: {str(e)}")
                    st.error("Vérifiez vos données et réessayez.")
    
    else:
        st.info("💡 Corrigez les erreurs ci-dessus avant de lancer l'analyse")
    
    # Instructions d'aide
    with st.expander("💡 Aide à la saisie", expanded=False):
        st.markdown("""
        ### 📋 Guide de Saisie
        
        **Données obligatoires :**
        - Total actif > 0
        - Chiffre d'affaires > 0
        - Equilibre du bilan (Actif = Passif)
        
        **Conseils :**
        - Saisissez les montants en FCFA sans espaces ni virgules
        - Le bilan doit être équilibré (vérification automatique)
        - La cohérence entre le résultat net du bilan et du compte de résultat est vérifiée
        - Les ratios seront calculés automatiquement
        
        **Secteurs disponibles :**
        - **Industrie Manufacturière** : Production, transformation
        - **Commerce de Détail** : Vente directe aux consommateurs
        - **Services Professionnels** : Conseil, services aux entreprises
        - **Construction/BTP** : Bâtiment, travaux publics
        - **Agriculture** : Production agricole, élevage
        - **Commerce de Gros** : Distribution, négoce
        
        **Calculs automatiques :**
        - Valeur ajoutée = CA - Achats matières premières
        - EBE = Valeur ajoutée - Charges personnel
        - Résultat d'exploitation = EBE - Autres charges - Amortissements
        - CAFG = Résultat net + Dotations amortissements
        """)

def validate_financial_data(data):
    """Valide la cohérence des données financières"""
    
    errors = []
    warnings = []
    
    # Vérifications obligatoires
    if data.get('total_actif', 0) <= 0:
        errors.append("Total actif invalide")
    
    if data.get('chiffre_affaires', 0) <= 0:
        errors.append("Chiffre d'affaires invalide")
    
    # Vérifications de cohérence
    total_passif = (
        data.get('capitaux_propres', 0) + 
        data.get('dettes_financieres', 0) + 
        data.get('dettes_court_terme', 0) + 
        data.get('tresorerie_passif', 0)
    )
    
    if abs(data.get('total_actif', 0) - total_passif) > 1000:
        errors.append("Bilan non équilibré")
    
    # Avertissements
    if data.get('capitaux_propres', 0) <= 0:
        warnings.append("Capitaux propres négatifs")
    
    if data.get('resultat_net', 0) < 0:
        warnings.append("Résultat net négatif")
    
    # Vérifications de cohérence avancées
    if data.get('immobilisations_nettes', 0) > data.get('total_actif', 0) * 0.8:
        warnings.append("Immobilisations représentent plus de 80% de l'actif")
    
    if data.get('dettes_financieres', 0) > data.get('capitaux_propres', 0) * 2:
        warnings.append("Endettement financier très élevé")
    
    if data.get('charges_personnel', 0) > data.get('chiffre_affaires', 0) * 0.7:
        warnings.append("Charges de personnel représentent plus de 70% du CA")
    
    return errors, warnings