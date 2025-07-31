"""
Page d'analyse avec affichage détaillé des états financiers
Grandes masses en gras selon les spécifications BCEAO
Compatible avec le main.py mis à jour
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import du gestionnaire de session centralisé
try:
    from session_manager import SessionManager
except ImportError:
    st.error("❌ Impossible d'importer session_manager.py")
    st.stop()

def show_detailed_analysis_page():
    """Affiche la page d'analyse détaillée avec états financiers complets"""
    
    # Vérifier la disponibilité des données
    if not SessionManager.has_analysis_data():
        show_no_analysis_error()
        return
    
    # Récupérer les données
    analysis_data = SessionManager.get_analysis_data()
    data = analysis_data['data']
    ratios = analysis_data['ratios']
    scores = analysis_data['scores']
    metadata = analysis_data['metadata']
    
    # En-tête de la page
    display_analysis_header(scores, metadata)
    
    # Onglets pour organiser l'affichage détaillé
    tab_overview, tab_bilan, tab_cr, tab_flux, tab_ratios, tab_sector = st.tabs([
        "📊 Vue d'Ensemble", 
        "🏦 Bilan Détaillé", 
        "📈 Compte de Résultat", 
        "💰 Flux de Trésorerie",
        "📉 Ratios Complets",
        "🔍 Comparaison Sectorielle"
    ])
    
    with tab_overview:
        show_analysis_overview(data, ratios, scores, metadata)
    
    with tab_bilan:
        show_detailed_balance_sheet(data)
    
    with tab_cr:
        show_detailed_income_statement(data)
    
    with tab_flux:
        show_detailed_cash_flow(data)
    
    with tab_ratios:
        show_complete_ratios_analysis(ratios, scores)
    
    with tab_sector:
        show_sectoral_comparison_detailed(ratios, metadata.get('secteur'))

def show_no_analysis_error():
    """Affiche une erreur si aucune analyse n'est disponible"""
    
    st.error("❌ Aucune analyse disponible")
    st.info("💡 Veuillez d'abord importer des données Excel ou effectuer une saisie manuelle.")
    
    col1, col2 = st.columns(2)
    
    reset_counter = SessionManager.get_reset_counter()
    
    with col1:
        input_key = f"goto_input_from_analysis_{reset_counter}"
        if st.button("📊 Saisir des Données", key=input_key, type="primary", use_container_width=True):
            SessionManager.set_current_page('unified_input')
            st.rerun()
    
    with col2:
        home_key = f"goto_home_from_analysis_{reset_counter}"
        if st.button("🏠 Accueil", key=home_key, use_container_width=True):
            SessionManager.set_current_page('home')
            st.rerun()

def display_analysis_header(scores, metadata):
    """Affiche l'en-tête de l'analyse"""
    
    st.title("📊 Analyse Financière Complète")
    
    # Informations générales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        source = metadata.get('source', 'inconnue').replace('_', ' ').title()
        st.info(f"**Source :** {source}")
    
    with col2:
        secteur = metadata.get('secteur', '').replace('_', ' ').title()
        st.info(f"**Secteur :** {secteur}")
    
    with col3:
        date_analyse = metadata.get('date_analyse', 'Non spécifiée')
        st.info(f"**Date :** {date_analyse}")
    
    # Score global en évidence
    score_global = scores.get('global', 0)
    interpretation, color = SessionManager.get_interpretation(score_global)
    classe = SessionManager.get_financial_class(score_global)
    
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; border-radius: 15px; background-color: {color}20; border: 3px solid {color}; margin: 20px 0;">
        <h1 style="color: {color}; margin: 0;">Score Global BCEAO</h1>
        <h1 style="color: {color}; margin: 15px 0; font-size: 3em;">{score_global}/100</h1>
        <h2 style="color: {color}; margin: 10px 0;">Classe {classe}</h2>
        <h3 style="color: {color}; margin: 0;">{interpretation}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

def show_analysis_overview(data, ratios, scores, metadata):
    """Affiche la vue d'ensemble de l'analyse"""
    
    st.header("📊 Vue d'Ensemble de la Performance")
    
    # Scores par catégorie
    st.subheader("🎯 Scores par Catégorie BCEAO")
    
    categories_data = [
        ("💧 Liquidité", scores.get('liquidite', 0), 40, "Capacité à honorer les engagements court terme"),
        ("🏛️ Solvabilité", scores.get('solvabilite', 0), 40, "Solidité de la structure financière"),
        ("📈 Rentabilité", scores.get('rentabilite', 0), 30, "Performance économique et profitabilité"),
        ("⚡ Activité", scores.get('activite', 0), 15, "Efficacité opérationnelle et rotation"),
        ("🔧 Gestion", scores.get('gestion', 0), 15, "Qualité du management et productivité")
    ]
    
    # Affichage des scores avec barres de progression
    for label, score, max_score, description in categories_data:
        col1, col2, col3 = st.columns([2, 1, 3])
        
        with col1:
            st.markdown(f"**{label}**")
            progress = score / max_score
            st.progress(progress, text=f"{score}/{max_score} ({progress*100:.0f}%)")
        
        with col2:
            if progress >= 0.8:
                st.success("Excellent")
            elif progress >= 0.6:
                st.info("Bon")
            elif progress >= 0.4:
                st.warning("Moyen")
            else:
                st.error("Faible")
        
        with col3:
            st.caption(description)
    
    st.markdown("---")
    
    # Indicateurs financiers clés
    st.subheader("💰 Indicateurs Financiers Clés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ca = data.get('chiffre_affaires', 0)
        st.metric(
            "Chiffre d'Affaires", 
            f"{ca:,.0f}".replace(',', ' ') + " FCFA",
            help="Volume d'activité de l'entreprise"
        )
    
    with col2:
        rn = data.get('resultat_net', 0)
        rn_pct = (rn / ca * 100) if ca > 0 else 0
        st.metric(
            "Résultat Net", 
            f"{rn:,.0f}".replace(',', ' ') + " FCFA",
            delta=f"{rn_pct:.1f}% du CA",
            help="Bénéfice ou perte de l'exercice"
        )
    
    with col3:
        ta = data.get('total_actif', 0)
        st.metric(
            "Total Actif", 
            f"{ta:,.0f}".replace(',', ' ') + " FCFA",
            help="Total des ressources de l'entreprise"
        )
    
    with col4:
        cp = data.get('capitaux_propres', 0)
        autonomie = (cp / ta * 100) if ta > 0 else 0
        st.metric(
            "Capitaux Propres", 
            f"{cp:,.0f}".replace(',', ' ') + " FCFA",
            delta=f"{autonomie:.1f}% de l'actif",
            help="Fonds propres de l'entreprise"
        )
    
    # Ratios de performance clés
    st.subheader("📊 Ratios de Performance Clés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        liquidite = ratios.get('ratio_liquidite_generale', 0)
        status = get_ratio_status(liquidite, 1.5, higher_is_better=True)
        st.metric("Liquidité Générale", f"{liquidite:.2f}", status)
    
    with col2:
        autonomie_ratio = ratios.get('ratio_autonomie_financiere', 0)
        status = get_ratio_status(autonomie_ratio, 30, higher_is_better=True)
        st.metric("Autonomie Financière", f"{autonomie_ratio:.1f}%", status)
    
    with col3:
        roe = ratios.get('roe', 0)
        status = get_ratio_status(roe, 10, higher_is_better=True)
        st.metric("ROE", f"{roe:.1f}%", status)
    
    with col4:
        marge_nette = ratios.get('marge_nette', 0)
        status = get_ratio_status(marge_nette, 5, higher_is_better=True)
        st.metric("Marge Nette", f"{marge_nette:.1f}%", status)
    
    # Graphique radar des performances
    st.subheader("📡 Radar de Performance")
    create_performance_radar(scores)

def show_detailed_balance_sheet(data):
    """Affiche le bilan détaillé avec grandes masses en gras - VERSION CORRIGÉE"""
    
    st.header("🏦 Bilan Détaillé")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## **ACTIF**")
        
        # Créer le DataFrame pour l'actif avec structure détaillée
        actif_data = []
        
        # IMMOBILISATIONS (Grande masse en gras)
        actif_data.append(["**IMMOBILISATIONS**", "**Montant (FCFA)**"])
        
        if data.get('terrains', 0) > 0:
            actif_data.append(["  • Terrains", f"{data.get('terrains', 0):,.0f}"])
        if data.get('batiments', 0) > 0:
            actif_data.append(["  • Bâtiments", f"{data.get('batiments', 0):,.0f}"])
        if data.get('materiel_equipement', 0) > 0:
            actif_data.append(["  • Matériel et équipements", f"{data.get('materiel_equipement', 0):,.0f}"])
        if data.get('materiel_transport', 0) > 0:
            actif_data.append(["  • Matériel de transport", f"{data.get('materiel_transport', 0):,.0f}"])
        if data.get('mobilier_bureau', 0) > 0:
            actif_data.append(["  • Mobilier de bureau", f"{data.get('mobilier_bureau', 0):,.0f}"])
        if data.get('immobilisations_financieres', 0) > 0:
            actif_data.append(["  • Immobilisations financières", f"{data.get('immobilisations_financieres', 0):,.0f}"])
        
        actif_data.append(["**TOTAL IMMOBILISATIONS**", f"**{data.get('immobilisations_nettes', 0):,.0f}**"])
        actif_data.append(["", ""])  # Ligne vide pour séparation
        
        # ACTIF CIRCULANT
        actif_data.append(["**ACTIF CIRCULANT**", ""])
        
        if data.get('stocks_matieres_premieres', 0) > 0:
            actif_data.append(["  • Stocks matières premières", f"{data.get('stocks_matieres_premieres', 0):,.0f}"])
        if data.get('stocks_produits_finis', 0) > 0:
            actif_data.append(["  • Stocks produits finis", f"{data.get('stocks_produits_finis', 0):,.0f}"])
        if data.get('stocks_marchandises', 0) > 0:
            actif_data.append(["  • Stocks marchandises", f"{data.get('stocks_marchandises', 0):,.0f}"])
        
        actif_data.append(["**TOTAL STOCKS**", f"**{data.get('stocks', 0):,.0f}**"])
        actif_data.append(["", ""])  # Ligne vide
        
        # CRÉANCES
        actif_data.append(["**CRÉANCES**", ""])
        
        if data.get('creances_clients', 0) > 0:
            actif_data.append(["  • Créances clients", f"{data.get('creances_clients', 0):,.0f}"])
        if data.get('autres_creances', 0) > 0:
            actif_data.append(["  • Autres créances", f"{data.get('autres_creances', 0):,.0f}"])
        
        total_creances = data.get('creances_clients', 0) + data.get('autres_creances', 0)
        actif_data.append(["**TOTAL CRÉANCES**", f"**{total_creances:,.0f}**"])
        actif_data.append(["", ""])  # Ligne vide
        
        # TRÉSORERIE ACTIF
        actif_data.append(["**TRÉSORERIE ACTIF**", ""])
        
        if data.get('banques_actif', 0) > 0:
            actif_data.append(["  • Banques", f"{data.get('banques_actif', 0):,.0f}"])
        if data.get('caisse', 0) > 0:
            actif_data.append(["  • Caisse", f"{data.get('caisse', 0):,.0f}"])
        if data.get('ccp', 0) > 0:
            actif_data.append(["  • CCP", f"{data.get('ccp', 0):,.0f}"])
        
        actif_data.append(["**TOTAL TRÉSORERIE ACTIF**", f"**{data.get('tresorerie', 0):,.0f}**"])
        actif_data.append(["", ""])  # Ligne vide
        
        # TOTAL GÉNÉRAL ACTIF
        total_actif = data.get('total_actif', 0)
        actif_data.append(["**TOTAL GÉNÉRAL ACTIF**", f"**{total_actif:,.0f}**"])
        
        # Affichage du tableau actif avec grandes masses en gras
        display_formatted_balance_sheet(actif_data)
    
    with col2:
        st.markdown("## **PASSIF**")
        
        # Créer le DataFrame pour le passif avec structure détaillée
        passif_data = []
        
        # CAPITAUX PROPRES (Grande masse en gras)
        passif_data.append(["**CAPITAUX PROPRES**", "**Montant (FCFA)**"])
        
        if data.get('capital', 0) > 0:
            passif_data.append(["  • Capital social", f"{data.get('capital', 0):,.0f}"])
        if data.get('reserves', 0) > 0:
            passif_data.append(["  • Réserves", f"{data.get('reserves', 0):,.0f}"])
        if data.get('report_nouveau', 0) != 0:
            passif_data.append(["  • Report à nouveau", f"{data.get('report_nouveau', 0):,.0f}"])
        
        passif_data.append(["  • Résultat net", f"{data.get('resultat_net', 0):,.0f}"])
        passif_data.append(["**TOTAL CAPITAUX PROPRES**", f"**{data.get('capitaux_propres', 0):,.0f}**"])
        passif_data.append(["", ""])  # Ligne vide
        
        # DETTES FINANCIÈRES
        passif_data.append(["**DETTES FINANCIÈRES**", ""])
        
        if data.get('emprunts_bancaires_long_terme', 0) > 0:
            passif_data.append(["  • Emprunts bancaires LT", f"{data.get('emprunts_bancaires_long_terme', 0):,.0f}"])
        if data.get('emprunts_obligataires', 0) > 0:
            passif_data.append(["  • Emprunts obligataires", f"{data.get('emprunts_obligataires', 0):,.0f}"])
        if data.get('autres_dettes_financieres', 0) > 0:
            passif_data.append(["  • Autres dettes financières", f"{data.get('autres_dettes_financieres', 0):,.0f}"])
        
        passif_data.append(["**TOTAL DETTES FINANCIÈRES**", f"**{data.get('dettes_financieres', 0):,.0f}**"])
        passif_data.append(["", ""])  # Ligne vide
        
        # DETTES COURT TERME
        passif_data.append(["**DETTES COURT TERME**", ""])
        
        if data.get('dettes_fournisseurs', 0) > 0:
            passif_data.append(["  • Dettes fournisseurs", f"{data.get('dettes_fournisseurs', 0):,.0f}"])
        if data.get('dettes_fiscales', 0) > 0:
            passif_data.append(["  • Dettes fiscales", f"{data.get('dettes_fiscales', 0):,.0f}"])
        if data.get('dettes_sociales', 0) > 0:
            passif_data.append(["  • Dettes sociales", f"{data.get('dettes_sociales', 0):,.0f}"])
        
        passif_data.append(["**TOTAL DETTES CT**", f"**{data.get('dettes_court_terme', 0):,.0f}**"])
        passif_data.append(["", ""])  # Ligne vide
        
        # TRÉSORERIE PASSIF
        if data.get('tresorerie_passif', 0) > 0:
            passif_data.append(["**TRÉSORERIE PASSIF**", ""])
            
            if data.get('banques_credits_tresorerie', 0) > 0:
                passif_data.append(["  • Banques - crédits trésorerie", f"{data.get('banques_credits_tresorerie', 0):,.0f}"])
            if data.get('banques_credits_escompte', 0) > 0:
                passif_data.append(["  • Banques - crédits escompte", f"{data.get('banques_credits_escompte', 0):,.0f}"])
            
            passif_data.append(["**TOTAL TRÉSORERIE PASSIF**", f"**{data.get('tresorerie_passif', 0):,.0f}**"])
            passif_data.append(["", ""])  # Ligne vide
        
        # TOTAL GÉNÉRAL PASSIF
        total_passif = (data.get('capitaux_propres', 0) + data.get('dettes_financieres', 0) + 
                       data.get('dettes_court_terme', 0) + data.get('tresorerie_passif', 0))
        passif_data.append(["**TOTAL GÉNÉRAL PASSIF**", f"**{total_passif:,.0f}**"])
        
        # Affichage du tableau passif avec grandes masses en gras
        display_formatted_balance_sheet(passif_data)
    
    # Vérification de l'équilibre du bilan
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("**Total Actif**", f"{data.get('total_actif', 0):,.0f} FCFA")
    
    with col2:
        total_passif = (data.get('capitaux_propres', 0) + data.get('dettes_financieres', 0) + 
                       data.get('dettes_court_terme', 0) + data.get('tresorerie_passif', 0))
        st.metric("**Total Passif**", f"{total_passif:,.0f} FCFA")
    
    with col3:
        equilibre = abs(data.get('total_actif', 0) - total_passif)
        color = "normal" if equilibre < 1000 else "inverse"
        st.metric("**Équilibre**", f"{equilibre:,.0f} FCFA", delta_color=color)
        
    if equilibre > 1000:
        st.warning(f"⚠️ Déséquilibre détecté dans le bilan : {equilibre:,.0f} FCFA")
    else:
        st.success("✅ Bilan équilibré")

def show_detailed_income_statement(data):
    """Affiche le compte de résultat détaillé avec formatage cohérent"""
    
    st.header("📈 Compte de Résultat Détaillé")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## **PRODUITS**")
        
        # Construire les données PRODUITS avec structure cohérente
        produits_data = []
        produits_data.append(["**PRODUITS**", "**Montant (FCFA)**"])
        
        # CHIFFRE D'AFFAIRES
        produits_data.append(["**CHIFFRE D'AFFAIRES**", ""])
        if data.get('ventes_marchandises', 0) > 0:
            produits_data.append(["  • Ventes de marchandises", f"{data.get('ventes_marchandises', 0):,.0f}"])
        if data.get('ventes_produits_fabriques', 0) > 0:
            produits_data.append(["  • Ventes de produits fabriqués", f"{data.get('ventes_produits_fabriques', 0):,.0f}"])
        if data.get('travaux_services_vendus', 0) > 0:
            produits_data.append(["  • Travaux et services vendus", f"{data.get('travaux_services_vendus', 0):,.0f}"])
        if data.get('produits_accessoires', 0) > 0:
            produits_data.append(["  • Produits accessoires", f"{data.get('produits_accessoires', 0):,.0f}"])
        if data.get('marge_commerciale', 0) > 0:
            produits_data.append(["  • Marge commerciale", f"{data.get('marge_commerciale', 0):,.0f}"])
        
        produits_data.append(["**TOTAL CHIFFRE D'AFFAIRES**", f"**{data.get('chiffre_affaires', 0):,.0f}**"])
        produits_data.append(["", ""])
        
        # AUTRES PRODUITS D'EXPLOITATION
        if (data.get('autres_produits', 0) > 0 or data.get('production_stockee', 0) > 0 or 
            data.get('production_immobilisee', 0) > 0 or data.get('subventions_exploitation', 0) > 0):
            
            produits_data.append(["**AUTRES PRODUITS D'EXPLOITATION**", ""])
            if data.get('production_stockee', 0) > 0:
                produits_data.append(["  • Production stockée", f"{data.get('production_stockee', 0):,.0f}"])
            if data.get('production_immobilisee', 0) > 0:
                produits_data.append(["  • Production immobilisée", f"{data.get('production_immobilisee', 0):,.0f}"])
            if data.get('subventions_exploitation', 0) > 0:
                produits_data.append(["  • Subventions d'exploitation", f"{data.get('subventions_exploitation', 0):,.0f}"])
            if data.get('autres_produits', 0) > 0:
                produits_data.append(["  • Autres produits", f"{data.get('autres_produits', 0):,.0f}"])
            produits_data.append(["", ""])
        
        # PRODUITS FINANCIERS
        if data.get('revenus_financiers', 0) > 0:
            produits_data.append(["**PRODUITS FINANCIERS**", ""])
            produits_data.append(["  • Revenus financiers", f"{data.get('revenus_financiers', 0):,.0f}"])
            produits_data.append(["", ""])
        
        # TOTAL GÉNÉRAL PRODUITS
        total_produits = (data.get('chiffre_affaires', 0) + data.get('autres_produits', 0) + 
                         data.get('production_stockee', 0) + data.get('production_immobilisee', 0) +
                         data.get('subventions_exploitation', 0) + data.get('revenus_financiers', 0))
        produits_data.append(["**TOTAL GÉNÉRAL PRODUITS**", f"**{total_produits:,.0f}**"])
        
        # Afficher le tableau PRODUITS
        display_formatted_balance_sheet(produits_data)
    
    with col2:
        st.markdown("## **CHARGES**")
        
        # Construire les données CHARGES avec structure cohérente
        charges_data = []
        charges_data.append(["**CHARGES**", "**Montant (FCFA)**"])
        
        # CHARGES D'EXPLOITATION
        charges_data.append(["**CHARGES D'EXPLOITATION**", ""])
        
        # Achats détaillés
        if (data.get('achats_marchandises', 0) > 0 or data.get('achats_matieres_premieres', 0) > 0 or 
            data.get('autres_achats', 0) > 0):
            if data.get('achats_marchandises', 0) > 0:
                charges_data.append(["  • Achats de marchandises", f"{data.get('achats_marchandises', 0):,.0f}"])
            if data.get('achats_matieres_premieres', 0) > 0:
                charges_data.append(["  • Achats matières premières", f"{data.get('achats_matieres_premieres', 0):,.0f}"])
            if data.get('autres_achats', 0) > 0:
                charges_data.append(["  • Autres achats", f"{data.get('autres_achats', 0):,.0f}"])
        
        # Charges externes détaillées
        if (data.get('transports', 0) > 0 or data.get('services_exterieurs', 0) > 0 or 
            data.get('impots_taxes', 0) > 0 or data.get('autres_charges', 0) > 0):
            if data.get('transports', 0) > 0:
                charges_data.append(["  • Transports", f"{data.get('transports', 0):,.0f}"])
            if data.get('services_exterieurs', 0) > 0:
                charges_data.append(["  • Services extérieurs", f"{data.get('services_exterieurs', 0):,.0f}"])
            if data.get('impots_taxes', 0) > 0:
                charges_data.append(["  • Impôts et taxes", f"{data.get('impots_taxes', 0):,.0f}"])
            if data.get('autres_charges', 0) > 0:
                charges_data.append(["  • Autres charges", f"{data.get('autres_charges', 0):,.0f}"])
        
        # Charges de personnel
        if data.get('charges_personnel', 0) > 0:
            charges_data.append(["  • Charges de personnel", f"{data.get('charges_personnel', 0):,.0f}"])
        
        # Amortissements
        if data.get('dotations_amortissements', 0) > 0:
            charges_data.append(["  • Dotations amortissements", f"{data.get('dotations_amortissements', 0):,.0f}"])
        
        charges_data.append(["**TOTAL CHARGES D'EXPLOITATION**", f"**{data.get('charges_exploitation', 0):,.0f}**"])
        charges_data.append(["", ""])
        
        # CHARGES FINANCIÈRES
        if data.get('frais_financiers', 0) > 0:
            charges_data.append(["**CHARGES FINANCIÈRES**", ""])
            charges_data.append(["  • Frais financiers", f"{data.get('frais_financiers', 0):,.0f}"])
            charges_data.append(["", ""])
        
        # IMPÔTS SUR LES BÉNÉFICES
        if data.get('impots_resultat', 0) > 0:
            charges_data.append(["**IMPÔTS SUR BÉNÉFICES**", ""])
            charges_data.append(["  • Impôts sur le résultat", f"{data.get('impots_resultat', 0):,.0f}"])
            charges_data.append(["", ""])
        
        # TOTAL GÉNÉRAL CHARGES
        total_charges = (data.get('charges_exploitation', 0) + data.get('frais_financiers', 0) + 
                        data.get('impots_resultat', 0))
        charges_data.append(["**TOTAL GÉNÉRAL CHARGES**", f"**{total_charges:,.0f}**"])
        
        # Afficher le tableau CHARGES
        display_formatted_balance_sheet(charges_data)
    
    # SOLDES INTERMÉDIAIRES DE GESTION
    st.markdown("---")
    st.markdown("## **SOLDES INTERMÉDIAIRES DE GESTION**")
    
    # Calculs des soldes avec détail complet
    valeur_ajoutee = data.get('valeur_ajoutee', 0)
    excedent_brut = data.get('excedent_brut', 0)
    resultat_exploitation = data.get('resultat_exploitation', 0)
    resultat_financier = data.get('resultat_financier', 0)
    resultat_net = data.get('resultat_net', 0)
    
    # Affichage des soldes avec calculs détaillés
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### **📊 FORMATION DE LA VALEUR AJOUTÉE**")
        st.write(f"Chiffre d'affaires : **{data.get('chiffre_affaires', 0):,.0f}** FCFA")
        
        # Détail des consommations
        consommations = (data.get('achats_marchandises', 0) + data.get('achats_matieres_premieres', 0) + 
                        data.get('autres_achats', 0) + data.get('transports', 0) + 
                        data.get('services_exterieurs', 0) + data.get('autres_charges', 0))
        
        if consommations > 0:
            st.write(f"- Consommations externes : **({consommations:,.0f})** FCFA")
        
        st.metric("**= VALEUR AJOUTÉE**", f"{valeur_ajoutee:,.0f} FCFA",
                 delta=f"{(valeur_ajoutee/data.get('chiffre_affaires', 1)*100):.1f}% du CA" if data.get('chiffre_affaires', 0) > 0 else None)
    
    with col2:
        st.markdown("#### **📊 FORMATION DE L'EBE**")
        st.write(f"Valeur ajoutée : **{valeur_ajoutee:,.0f}** FCFA")
        if data.get('charges_personnel', 0) > 0:
            st.write(f"- Charges de personnel : **({data.get('charges_personnel', 0):,.0f})** FCFA")
        
        st.metric("**= EXCÉDENT BRUT EXPLOITATION**", f"{excedent_brut:,.0f} FCFA",
                 delta=f"{(excedent_brut/data.get('chiffre_affaires', 1)*100):.1f}% du CA" if data.get('chiffre_affaires', 0) > 0 else None)
        
        st.markdown("#### **📊 RÉSULTAT D'EXPLOITATION**")
        if data.get('dotations_amortissements', 0) > 0:
            st.write(f"- Dotations amortissements : **({data.get('dotations_amortissements', 0):,.0f})** FCFA")
        
        st.metric("**= RÉSULTAT EXPLOITATION**", f"{resultat_exploitation:,.0f} FCFA",
                 delta=f"{(resultat_exploitation/data.get('chiffre_affaires', 1)*100):.1f}% du CA" if data.get('chiffre_affaires', 0) > 0 else None)
    
    with col3:
        st.markdown("#### **📊 RÉSULTAT FINAL**")
        
        if data.get('revenus_financiers', 0) > 0:
            st.write(f"+ Revenus financiers : **{data.get('revenus_financiers', 0):,.0f}** FCFA")
        if data.get('frais_financiers', 0) > 0:
            st.write(f"- Frais financiers : **({data.get('frais_financiers', 0):,.0f})** FCFA")
        
        st.metric("**= RÉSULTAT FINANCIER**", f"{resultat_financier:,.0f} FCFA")
        
        if data.get('impots_resultat', 0) > 0:
            st.write(f"- Impôts sur résultat : **({data.get('impots_resultat', 0):,.0f})** FCFA")
        
        # Résultat net final avec couleur selon signe
        if resultat_net >= 0:
            st.markdown(f"### 🟢 **RÉSULTAT NET : {resultat_net:,.0f} FCFA**")
            st.caption(f"Soit {(resultat_net/data.get('chiffre_affaires', 1)*100):.1f}% du CA" if data.get('chiffre_affaires', 0) > 0 else "")
        else:
            st.markdown(f"### 🔴 **RÉSULTAT NET : {resultat_net:,.0f} FCFA**")
            st.caption("⚠️ Perte de l'exercice")
    
    # Graphique waterfall des soldes
    create_waterfall_chart(data)

def show_detailed_cash_flow(data):
    """Affiche le tableau des flux de trésorerie détaillé"""
    
    st.header("💰 Tableau des Flux de Trésorerie Détaillé")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **Flux d'Exploitation**")
        
        # Flux opérationnels détaillés
        flux_exp_data = []
        flux_exp_data.append(["**CAPACITÉ D'AUTOFINANCEMENT**", "**Montant (FCFA)**"])
        flux_exp_data.append(["Résultat net", f"{data.get('resultat_net', 0):,.0f}"])
        flux_exp_data.append(["+ Dotations amortissements", f"{data.get('dotations_amortissements', 0):,.0f}"])
        flux_exp_data.append(["**= CAFG**", f"**{data.get('cafg', 0):,.0f}**"])
        flux_exp_data.append(["", ""])
        
        flux_exp_data.append(["**VARIATION DU BFR**", ""])
        flux_exp_data.append(["Variation du BFR", f"{data.get('variation_bfr', 0):,.0f}"])
        flux_exp_data.append(["", ""])
        
        flux_exp_data.append(["**FLUX OPÉRATIONNELS**", f"**{data.get('flux_activites_operationnelles', 0):,.0f}**"])
        
        # Afficher le tableau avec formatage cohérent
        display_formatted_balance_sheet(flux_exp_data)
        
        st.markdown("### **Flux d'Investissement**")
        
        flux_inv_data = []
        flux_inv_data.append(["**INVESTISSEMENTS**", "**Montant (FCFA)**"])
        if data.get('acquisitions_immobilisations', 0) != 0:
            flux_inv_data.append(["Acquisitions d'immobilisations", f"({abs(data.get('acquisitions_immobilisations', 0)):,.0f})"])
        if data.get('cessions_immobilisations', 0) > 0:
            flux_inv_data.append(["Cessions d'immobilisations", f"{data.get('cessions_immobilisations', 0):,.0f}"])
        
        flux_inv_data.append(["**FLUX INVESTISSEMENT**", f"**{data.get('flux_activites_investissement', 0):,.0f}**"])
        
        # Afficher le tableau avec formatage cohérent
        display_formatted_balance_sheet(flux_inv_data)
    
    with col2:
        st.markdown("### **Flux de Financement**")
        
        flux_fin_data = []
        flux_fin_data.append(["**CAPITAUX PROPRES**", "**Montant (FCFA)**"])
        if data.get('augmentation_capital', 0) > 0:
            flux_fin_data.append(["Augmentation de capital", f"{data.get('augmentation_capital', 0):,.0f}"])
        if data.get('dividendes_verses', 0) > 0:
            flux_fin_data.append(["Dividendes versés", f"({data.get('dividendes_verses', 0):,.0f})"])
        
        flux_fin_data.append(["", ""])
        
        flux_fin_data.append(["**CAPITAUX ÉTRANGERS**", ""])
        if data.get('nouveaux_emprunts', 0) > 0:
            flux_fin_data.append(["Nouveaux emprunts", f"{data.get('nouveaux_emprunts', 0):,.0f}"])
        if data.get('remboursements_emprunts', 0) > 0:
            flux_fin_data.append(["Remboursements d'emprunts", f"({data.get('remboursements_emprunts', 0):,.0f})"])
        
        flux_fin_data.append(["", ""])
        
        flux_fin_data.append(["**FLUX FINANCEMENT**", f"**{data.get('flux_activites_financement', 0):,.0f}**"])
        
        # Afficher le tableau avec formatage cohérent
        display_formatted_balance_sheet(flux_fin_data)
        
        st.markdown("### **Synthèse des Flux**")
        
        synthese_data = []
        synthese_data.append(["**ÉLÉMENTS**", "**Montant (FCFA)**"])
        synthese_data.append(["Trésorerie d'ouverture", f"{data.get('tresorerie_ouverture', 0):,.0f}"])
        synthese_data.append(["+ Flux opérationnels", f"{data.get('flux_activites_operationnelles', 0):,.0f}"])
        synthese_data.append(["+ Flux d'investissement", f"{data.get('flux_activites_investissement', 0):,.0f}"])
        synthese_data.append(["+ Flux de financement", f"{data.get('flux_activites_financement', 0):,.0f}"])
        synthese_data.append(["**= Variation trésorerie**", f"**{data.get('variation_tresorerie', 0):,.0f}**"])
        synthese_data.append(["**= Trésorerie clôture**", f"**{data.get('tresorerie_cloture', 0):,.0f}**"])
        
        # Afficher le tableau avec formatage cohérent
        display_formatted_balance_sheet(synthese_data)

def show_complete_ratios_analysis(ratios, scores):
    """Affiche l'analyse complète des ratios"""
    
    st.header("📉 Analyse Complète des Ratios")
    
    # Onglets pour organiser les ratios
    ratio_tabs = st.tabs([
        "💧 Liquidité", "🏛️ Solvabilité", "📈 Rentabilité", 
        "⚡ Activité", "🔧 Gestion"
    ])
    
    with ratio_tabs[0]:  # Liquidité
        show_liquidity_ratios(ratios, scores)
    
    with ratio_tabs[1]:  # Solvabilité
        show_solvency_ratios(ratios, scores)
    
    with ratio_tabs[2]:  # Rentabilité
        show_profitability_ratios(ratios, scores)
    
    with ratio_tabs[3]:  # Activité
        show_activity_ratios(ratios, scores)
    
    with ratio_tabs[4]:  # Gestion
        show_management_ratios(ratios, scores)

def show_liquidity_ratios(ratios, scores):
    """Affiche les ratios de liquidité détaillés avec formules et normes BCEAO"""
    
    st.subheader(f"💧 Ratios de Liquidité - Score: {scores.get('liquidite', 0)}/40")
    st.markdown("*Évaluation de la capacité à honorer les engagements court terme selon les normes BCEAO*")
    
    # Ratios de liquidité avec formules détaillées
    liquidity_ratios = [
        {
            "label": "Liquidité Générale",
            "key": "ratio_liquidite_generale",
            "formula": "Actif Circulant / Dettes Court Terme",
            "target_excellent": "> 2.0",
            "target_good": "1.5 - 2.0", 
            "target_acceptable": "1.2 - 1.5",
            "target_poor": "< 1.2",
            "bceao_min": "≥ 1.5 (Norme BCEAO)",
            "description": "Mesure la capacité à honorer les dettes court terme avec l'actif circulant"
        },
        {
            "label": "Liquidité Immédiate (Acid Test)",
            "key": "ratio_liquidite_immediate", 
            "formula": "(Créances + Trésorerie) / Dettes Court Terme",
            "target_excellent": "> 1.2",
            "target_good": "1.0 - 1.2",
            "target_acceptable": "0.8 - 1.0", 
            "target_poor": "< 0.8",
            "bceao_min": "≥ 1.0 (Norme BCEAO)",
            "description": "Liquidité immédiate sans dépendre de la vente des stocks"
        },
        {
            "label": "BFR en jours de CA",
            "key": "bfr_jours_ca",
            "formula": "(BFR × 360) / Chiffre d'Affaires",
            "target_excellent": "< 30 jours",
            "target_good": "30 - 60 jours",
            "target_acceptable": "60 - 90 jours",
            "target_poor": "> 90 jours", 
            "bceao_min": "≤ 90 jours (Norme BCEAO)",
            "description": "Nombre de jours de CA nécessaires pour financer l'exploitation"
        }
    ]
    
    for ratio_info in liquidity_ratios:
        if ratio_info["key"] in ratios:
            # En-tête du ratio avec expandeur pour détails
            # Format the display value properly
            current_val = ratios[ratio_info["key"]]
            if ratio_info["key"] == "bfr_jours_ca":
                display_val = f"{current_val:.0f} jours"
            else:
                display_val = f"{current_val:.2f}"
            
            with st.expander(f"📊 **{ratio_info['label']}** - Valeur: {display_val}", expanded=False):
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### 📐 Formule de Calcul")
                    st.code(ratio_info["formula"], language="text")
                    
                    st.markdown("### 🎯 Norme BCEAO")
                    st.info(ratio_info["bceao_min"])
                    
                    st.markdown("### 📝 Description")
                    st.write(ratio_info["description"])
                
                with col2:
                    st.markdown("### 📊 Barème d'Évaluation")
                    
                    current_value = ratios[ratio_info["key"]]
                    
                    # Déterminer le statut actuel
                    if ratio_info["key"] == "bfr_jours_ca":
                        if current_value < 30:
                            current_status = "🟢 Excellent"
                            status_color = "green"
                        elif current_value <= 60:
                            current_status = "🟡 Bon" 
                            status_color = "orange"
                        elif current_value <= 90:
                            current_status = "🟠 Acceptable"
                            status_color = "orange"
                        else:
                            current_status = "🔴 Faible"
                            status_color = "red"
                    else:
                        thresholds = {"ratio_liquidite_generale": [1.2, 1.5, 2.0], "ratio_liquidite_immediate": [0.8, 1.0, 1.2]}
                        thresh = thresholds[ratio_info["key"]]
                        if current_value >= thresh[2]:
                            current_status = "🟢 Excellent"
                            status_color = "green"
                        elif current_value >= thresh[1]:
                            current_status = "🟡 Bon"
                            status_color = "orange" 
                        elif current_value >= thresh[0]:
                            current_status = "🟠 Acceptable"
                            status_color = "orange"
                        else:
                            current_status = "🔴 Faible"
                            status_color = "red"
                    
                    # Afficher le barème avec mise en évidence
                    st.markdown(f"🟢 **Excellent:** {ratio_info['target_excellent']}")
                    st.markdown(f"🟡 **Bon:** {ratio_info['target_good']}")
                    st.markdown(f"🟠 **Acceptable:** {ratio_info['target_acceptable']}")
                    st.markdown(f"🔴 **Faible:** {ratio_info['target_poor']}")
                    
                    st.markdown("---")
                    st.markdown(f"### Votre Position: {current_status}")
                    
                    # Barre de progression visuelle
                    if ratio_info["key"] == "bfr_jours_ca":
                        # Inverser la logique pour BFR (plus bas = mieux)
                        progress_val = max(0, min(1, (120 - current_value) / 120))
                    else:
                        max_display = {"ratio_liquidite_generale": 3.0, "ratio_liquidite_immediate": 2.0}[ratio_info["key"]]
                        progress_val = min(1, current_value / max_display)
                    
                    st.progress(progress_val)
            
            st.markdown("---")

def show_solvency_ratios(ratios, scores):
    """Affiche les ratios de solvabilité détaillés avec formules et normes BCEAO"""
    
    st.subheader(f"🏛️ Ratios de Solvabilité - Score: {scores.get('solvabilite', 0)}/40")
    st.markdown("*Évaluation de la solidité de la structure financière selon les normes BCEAO*")
    
    # Ratios de solvabilité avec formules détaillées
    solvency_ratios = [
        {
            "label": "Autonomie Financière",
            "key": "ratio_autonomie_financiere",
            "formula": "(Capitaux Propres / Total Actif) × 100",
            "target_excellent": "> 50%",
            "target_good": "30% - 50%", 
            "target_acceptable": "20% - 30%",
            "target_poor": "< 20%",
            "bceao_min": "≥ 30% (Norme BCEAO)",
            "description": "Mesure l'indépendance financière. Plus élevé = moins de dépendance aux créanciers.",
            "unit": "%"
        },
        {
            "label": "Endettement Global",
            "key": "ratio_endettement", 
            "formula": "(Total Dettes / Total Actif) × 100",
            "target_excellent": "< 40%",
            "target_good": "40% - 50%",
            "target_acceptable": "50% - 65%", 
            "target_poor": "> 65%",
            "bceao_min": "≤ 65% (Norme BCEAO)",
            "description": "Part du patrimoine financée par endettement. Plus bas = meilleure solvabilité.",
            "unit": "%"
        },
        {
            "label": "Capacité de Remboursement",
            "key": "capacite_remboursement",
            "formula": "Dettes Financières / Capacité d'Autofinancement",
            "target_excellent": "< 3 ans",
            "target_good": "3 - 4 ans",
            "target_acceptable": "4 - 5 ans",
            "target_poor": "> 5 ans", 
            "bceao_min": "≤ 5 ans (Norme BCEAO)",
            "description": "Nombre d'années nécessaires pour rembourser les dettes avec la CAF actuelle.",
            "unit": " ans"
        },
        {
            "label": "Couverture des Immobilisations",
            "key": "ratio_couverture_immobilisations",
            "formula": "Capitaux Permanents / Immobilisations Nettes",
            "target_excellent": "> 1.3",
            "target_good": "1.1 - 1.3",
            "target_acceptable": "1.0 - 1.1",
            "target_poor": "< 1.0",
            "bceao_min": "≥ 1.0 (Norme BCEAO)", 
            "description": "Financement des immobilisations par des ressources stables.",
            "unit": ""
        }
    ]
    
    for ratio_info in solvency_ratios:
        if ratio_info["key"] in ratios:
            # En-tête du ratio avec expandeur pour détails
            current_val = ratios[ratio_info["key"]]
            display_val = f"{current_val:.1f}{ratio_info['unit']}" if ratio_info['unit'] else f"{current_val:.2f}"
            
            with st.expander(f"🏛️ **{ratio_info['label']}** - Valeur: {display_val}", expanded=False):
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### 📐 Formule de Calcul")
                    st.code(ratio_info["formula"], language="text")
                    
                    st.markdown("### 🎯 Norme BCEAO")
                    st.info(ratio_info["bceao_min"])
                    
                    st.markdown("### 📝 Description")
                    st.write(ratio_info["description"])
                
                with col2:
                    st.markdown("### 📊 Barème d'Évaluation")
                    
                    # Déterminer le statut actuel selon le type de ratio
                    if ratio_info["key"] == "ratio_autonomie_financiere":
                        if current_val >= 50:
                            current_status = "🟢 Excellent"
                        elif current_val >= 30:
                            current_status = "🟡 Bon"
                        elif current_val >= 20:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    elif ratio_info["key"] == "ratio_endettement":
                        if current_val < 40:
                            current_status = "🟢 Excellent"
                        elif current_val <= 50:
                            current_status = "🟡 Bon"
                        elif current_val <= 65:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    elif ratio_info["key"] == "capacite_remboursement":
                        if current_val < 3:
                            current_status = "🟢 Excellent"
                        elif current_val <= 4:
                            current_status = "🟡 Bon"
                        elif current_val <= 5:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    else:  # couverture_immobilisations
                        if current_val >= 1.3:
                            current_status = "🟢 Excellent"
                        elif current_val >= 1.1:
                            current_status = "🟡 Bon"
                        elif current_val >= 1.0:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    
                    # Afficher le barème
                    st.markdown(f"🟢 **Excellent:** {ratio_info['target_excellent']}")
                    st.markdown(f"🟡 **Bon:** {ratio_info['target_good']}")
                    st.markdown(f"🟠 **Acceptable:** {ratio_info['target_acceptable']}")
                    st.markdown(f"🔴 **Faible:** {ratio_info['target_poor']}")
                    
                    st.markdown("---")
                    st.markdown(f"### Votre Position: {current_status}")
                    
                    # Barre de progression visuelle
                    if ratio_info["key"] == "ratio_endettement" or ratio_info["key"] == "capacite_remboursement":
                        # Inverser pour les ratios où plus bas = mieux
                        if ratio_info["key"] == "ratio_endettement":
                            progress_val = max(0, min(1, (100 - current_val) / 100))
                        else:  # capacite_remboursement
                            progress_val = max(0, min(1, (8 - current_val) / 8))
                    else:
                        # Ratios où plus haut = mieux
                        if ratio_info["key"] == "ratio_autonomie_financiere":
                            progress_val = min(1, current_val / 60)
                        else:  # couverture_immobilisations
                            progress_val = min(1, current_val / 1.5)
                    
                    st.progress(progress_val)
            
            st.markdown("---")

def show_profitability_ratios(ratios, scores):
    """Affiche les ratios de rentabilité détaillés avec formules et normes BCEAO"""
    
    st.subheader(f"📈 Ratios de Rentabilité - Score: {scores.get('rentabilite', 0)}/30")
    st.markdown("*Évaluation de la performance économique et profitabilité selon les normes BCEAO*")
    
    # Ratios de rentabilité avec formules détaillées
    profitability_ratios = [
        {
            "label": "ROE (Return on Equity)",
            "key": "roe",
            "formula": "(Résultat Net / Capitaux Propres) × 100",
            "target_excellent": "> 15%",
            "target_good": "10% - 15%", 
            "target_acceptable": "5% - 10%",
            "target_poor": "< 5%",
            "bceao_min": "≥ 10% (Norme BCEAO)",
            "description": "Rentabilité des fonds propres. Mesure l'efficacité d'utilisation des capitaux propres."
        },
        {
            "label": "ROA (Return on Assets)",
            "key": "roa", 
            "formula": "(Résultat Net / Total Actif) × 100",
            "target_excellent": "> 5%",
            "target_good": "2% - 5%",
            "target_acceptable": "1% - 2%", 
            "target_poor": "< 1%",
            "bceao_min": "≥ 2% (Norme BCEAO)",
            "description": "Rentabilité de l'actif total. Indique l'efficacité globale de l'entreprise."
        },
        {
            "label": "Marge Nette",
            "key": "marge_nette",
            "formula": "(Résultat Net / Chiffre d'Affaires) × 100",
            "target_excellent": "> 8%",
            "target_good": "5% - 8%",
            "target_acceptable": "2% - 5%",
            "target_poor": "< 2%", 
            "bceao_min": "≥ 5% (Norme BCEAO)",
            "description": "Rentabilité des ventes. Part du CA qui se transforme en bénéfice net."
        },
        {
            "label": "Marge d'Exploitation (EBIT)",
            "key": "marge_exploitation",
            "formula": "(Résultat Exploitation / Chiffre d'Affaires) × 100",
            "target_excellent": "> 10%",
            "target_good": "5% - 10%",
            "target_acceptable": "2% - 5%",
            "target_poor": "< 2%",
            "bceao_min": "≥ 5% (Norme BCEAO)", 
            "description": "Rentabilité opérationnelle avant frais financiers et impôts."
        },
        {
            "label": "Marge Brute",
            "key": "marge_brute",
            "formula": "(Marge Commerciale / Chiffre d'Affaires) × 100",
            "target_excellent": "> 40%",
            "target_good": "25% - 40%",
            "target_acceptable": "15% - 25%",
            "target_poor": "< 15%",
            "bceao_min": "≥ 20% (Recommandation BCEAO)", 
            "description": "Marge commerciale sur les ventes. Indicateur de pricing power."
        }
    ]
    
    for ratio_info in profitability_ratios:
        if ratio_info["key"] in ratios:
            # En-tête du ratio avec expandeur pour détails
            current_val = ratios[ratio_info["key"]]
            
            with st.expander(f"📈 **{ratio_info['label']}** - Valeur: {current_val:.1f}%", expanded=False):
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### 📐 Formule de Calcul")
                    st.code(ratio_info["formula"], language="text")
                    
                    st.markdown("### 🎯 Norme BCEAO")
                    st.info(ratio_info["bceao_min"])
                    
                    st.markdown("### 📝 Description")
                    st.write(ratio_info["description"])
                
                with col2:
                    st.markdown("### 📊 Barème d'Évaluation")
                    
                    # Déterminer le statut actuel selon le type de ratio
                    if ratio_info["key"] == "roe":
                        if current_val >= 15:
                            current_status = "🟢 Excellent"
                        elif current_val >= 10:
                            current_status = "🟡 Bon"
                        elif current_val >= 5:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    elif ratio_info["key"] == "roa":
                        if current_val >= 5:
                            current_status = "🟢 Excellent"
                        elif current_val >= 2:
                            current_status = "🟡 Bon"
                        elif current_val >= 1:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    elif ratio_info["key"] == "marge_nette":
                        if current_val >= 8:
                            current_status = "🟢 Excellent"
                        elif current_val >= 5:
                            current_status = "🟡 Bon"
                        elif current_val >= 2:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    elif ratio_info["key"] == "marge_exploitation":
                        if current_val >= 10:
                            current_status = "🟢 Excellent"
                        elif current_val >= 5:
                            current_status = "🟡 Bon"
                        elif current_val >= 2:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    else:  # marge_brute
                        if current_val >= 40:
                            current_status = "🟢 Excellent"
                        elif current_val >= 25:
                            current_status = "🟡 Bon"
                        elif current_val >= 15:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    
                    # Afficher le barème
                    st.markdown(f"🟢 **Excellent:** {ratio_info['target_excellent']}")
                    st.markdown(f"🟡 **Bon:** {ratio_info['target_good']}")
                    st.markdown(f"🟠 **Acceptable:** {ratio_info['target_acceptable']}")
                    st.markdown(f"🔴 **Faible:** {ratio_info['target_poor']}")
                    
                    st.markdown("---")
                    st.markdown(f"### Votre Position: {current_status}")
                    
                    # Barre de progression visuelle
                    if ratio_info["key"] == "roe":
                        progress_val = min(1, current_val / 20)
                    elif ratio_info["key"] == "roa":
                        progress_val = min(1, current_val / 6)
                    elif ratio_info["key"] == "marge_nette":
                        progress_val = min(1, current_val / 10)
                    elif ratio_info["key"] == "marge_exploitation":
                        progress_val = min(1, current_val / 12)
                    else:  # marge_brute
                        progress_val = min(1, current_val / 50)
                    
                    st.progress(max(0, progress_val))
            
            st.markdown("---")

def show_activity_ratios(ratios, scores):
    """Affiche les ratios d'activité détaillés avec formules et normes BCEAO"""
    
    st.subheader(f"⚡ Ratios d'Activité - Score: {scores.get('activite', 0)}/15")
    st.markdown("*Évaluation de l'efficacité opérationnelle et rotation des actifs selon les normes BCEAO*")
    
    # Ratios d'activité avec formules détaillées
    activity_ratios = [
        {
            "label": "Rotation de l'Actif Total",
            "key": "rotation_actif",
            "formula": "Chiffre d'Affaires / Total Actif",
            "target_excellent": "> 2.0",
            "target_good": "1.5 - 2.0", 
            "target_acceptable": "1.0 - 1.5",
            "target_poor": "< 1.0",
            "bceao_min": "≥ 1.5 (Norme BCEAO)",
            "description": "Mesure l'efficacité d'utilisation des actifs pour générer du CA.",
            "unit": ""
        },
        {
            "label": "Rotation des Stocks",
            "key": "rotation_stocks", 
            "formula": "Coût des Ventes / Stock Moyen",
            "target_excellent": "> 8",
            "target_good": "6 - 8",
            "target_acceptable": "4 - 6", 
            "target_poor": "< 4",
            "bceao_min": "≥ 6 (Norme BCEAO)",
            "description": "Vitesse d'écoulement des stocks. Plus élevé = meilleure gestion.",
            "unit": ""
        },
        {
            "label": "Délai Recouvrement Clients",
            "key": "delai_recouvrement_clients",
            "formula": "(Créances Clients × 360) / Chiffre d'Affaires",
            "target_excellent": "< 30 jours",
            "target_good": "30 - 45 jours",
            "target_acceptable": "45 - 60 jours",
            "target_poor": "> 60 jours", 
            "bceao_min": "≤ 45 jours (Norme BCEAO)",
            "description": "Temps moyen de recouvrement des créances clients.",
            "unit": " jours"
        },
        {
            "label": "Délai Règlement Fournisseurs",
            "key": "delai_reglement_fournisseurs",
            "formula": "(Dettes Fournisseurs × 360) / Achats",
            "target_excellent": "> 60 jours",
            "target_good": "45 - 60 jours",
            "target_acceptable": "30 - 45 jours",
            "target_poor": "< 30 jours",
            "bceao_min": "≥ 30 jours (Recommandation BCEAO)", 
            "description": "Délai de paiement des fournisseurs. Plus élevé = meilleure trésorerie.",
            "unit": " jours"
        }
    ]
    
    for ratio_info in activity_ratios:
        if ratio_info["key"] in ratios:
            # En-tête du ratio avec expandeur pour détails
            current_val = ratios[ratio_info["key"]]
            display_val = f"{current_val:.1f}{ratio_info['unit']}" if ratio_info['unit'] else f"{current_val:.1f}"
            
            with st.expander(f"⚡ **{ratio_info['label']}** - Valeur: {display_val}", expanded=False):
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### 📐 Formule de Calcul")
                    st.code(ratio_info["formula"], language="text")
                    
                    st.markdown("### 🎯 Norme BCEAO")
                    st.info(ratio_info["bceao_min"])
                    
                    st.markdown("### 📝 Description")
                    st.write(ratio_info["description"])
                
                with col2:
                    st.markdown("### 📊 Barème d'Évaluation")
                    
                    # Déterminer le statut actuel selon le type de ratio
                    if ratio_info["key"] == "rotation_actif":
                        if current_val >= 2.0:
                            current_status = "🟢 Excellent"
                        elif current_val >= 1.5:
                            current_status = "🟡 Bon"
                        elif current_val >= 1.0:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    elif ratio_info["key"] == "rotation_stocks":
                        if current_val >= 8:
                            current_status = "🟢 Excellent"
                        elif current_val >= 6:
                            current_status = "🟡 Bon"
                        elif current_val >= 4:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    elif ratio_info["key"] == "delai_recouvrement_clients":
                        if current_val < 30:
                            current_status = "🟢 Excellent"
                        elif current_val <= 45:
                            current_status = "🟡 Bon"
                        elif current_val <= 60:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    else:  # delai_reglement_fournisseurs
                        if current_val > 60:
                            current_status = "🟢 Excellent"
                        elif current_val >= 45:
                            current_status = "🟡 Bon"
                        elif current_val >= 30:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    
                    # Afficher le barème
                    st.markdown(f"🟢 **Excellent:** {ratio_info['target_excellent']}")
                    st.markdown(f"🟡 **Bon:** {ratio_info['target_good']}")
                    st.markdown(f"🟠 **Acceptable:** {ratio_info['target_acceptable']}")
                    st.markdown(f"🔴 **Faible:** {ratio_info['target_poor']}")
                    
                    st.markdown("---")
                    st.markdown(f"### Votre Position: {current_status}")
                    
                    # Barre de progression visuelle
                    if ratio_info["key"] == "rotation_actif":
                        progress_val = min(1, current_val / 2.5)
                    elif ratio_info["key"] == "rotation_stocks":
                        progress_val = min(1, current_val / 10)
                    elif ratio_info["key"] == "delai_recouvrement_clients":
                        # Inverser pour les délais (plus bas = mieux)
                        progress_val = max(0, min(1, (90 - current_val) / 90))
                    else:  # delai_reglement_fournisseurs
                        # Pour ce ratio, plus haut = mieux
                        progress_val = min(1, current_val / 80)
                    
                    st.progress(max(0, progress_val))
            
            st.markdown("---")

def show_management_ratios(ratios, scores):
    """Affiche les ratios de gestion détaillés avec formules et normes BCEAO"""
    
    st.subheader(f"🔧 Ratios de Gestion - Score: {scores.get('gestion', 0)}/15")  
    st.markdown("*Évaluation de la qualité du management et productivité selon les normes BCEAO*")
    
    # Ratios de gestion avec formules détaillées
    management_ratios = [
        {
            "label": "Productivité du Personnel",
            "key": "productivite_personnel",
            "formula": "Valeur Ajoutée / Charges de Personnel",
            "target_excellent": "> 3.0",
            "target_good": "2.0 - 3.0", 
            "target_acceptable": "1.5 - 2.0",
            "target_poor": "< 1.5",
            "bceao_min": "≥ 2.0 (Norme BCEAO)",
            "description": "Valeur ajoutée générée par euro de charges de personnel. Indicateur de productivité.",
            "unit": ""
        },
        {
            "label": "Taux Charges Personnel",
            "key": "taux_charges_personnel", 
            "formula": "(Charges Personnel / Valeur Ajoutée) × 100",
            "target_excellent": "< 40%",
            "target_good": "40% - 50%",
            "target_acceptable": "50% - 60%", 
            "target_poor": "> 60%",
            "bceao_min": "≤ 50% (Norme BCEAO)",
            "description": "Part de la valeur ajoutée consacrée aux charges de personnel.",
            "unit": "%"
        },
        {
            "label": "CAFG / Chiffre d'Affaires",
            "key": "ratio_cafg_ca",
            "formula": "(Capacité Autofinancement / Chiffre d'Affaires) × 100",
            "target_excellent": "> 10%",
            "target_good": "7% - 10%",
            "target_acceptable": "5% - 7%",
            "target_poor": "< 5%", 
            "bceao_min": "≥ 7% (Norme BCEAO)",
            "description": "Capacité de génération de trésorerie par rapport au CA.",
            "unit": "%"
        },
        {
            "label": "Intensité Capitalistique",
            "key": "intensite_capitaliste",
            "formula": "Immobilisations Nettes / Valeur Ajoutée",
            "target_excellent": "< 2.0",
            "target_good": "2.0 - 3.0",
            "target_acceptable": "3.0 - 4.0",
            "target_poor": "> 4.0",
            "bceao_min": "≤ 3.0 (Recommandation BCEAO)", 
            "description": "Capital immobilisé nécessaire pour créer 1 FCFA de valeur ajoutée.",
            "unit": ""
        }
    ]
    
    for ratio_info in management_ratios:
        if ratio_info["key"] in ratios:
            # En-tête du ratio avec expandeur pour détails
            current_val = ratios[ratio_info["key"]]
            display_val = f"{current_val:.1f}{ratio_info['unit']}" if ratio_info['unit'] else f"{current_val:.2f}"
            
            with st.expander(f"🔧 **{ratio_info['label']}** - Valeur: {display_val}", expanded=False):
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### 📐 Formule de Calcul")
                    st.code(ratio_info["formula"], language="text")
                    
                    st.markdown("### 🎯 Norme BCEAO")
                    st.info(ratio_info["bceao_min"])
                    
                    st.markdown("### 📝 Description")
                    st.write(ratio_info["description"])
                
                with col2:
                    st.markdown("### 📊 Barème d'Évaluation")
                    
                    # Déterminer le statut actuel selon le type de ratio
                    if ratio_info["key"] == "productivite_personnel":
                        if current_val >= 3.0:
                            current_status = "🟢 Excellent"
                        elif current_val >= 2.0:
                            current_status = "🟡 Bon"
                        elif current_val >= 1.5:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    elif ratio_info["key"] == "taux_charges_personnel":
                        if current_val < 40:
                            current_status = "🟢 Excellent"
                        elif current_val <= 50:
                            current_status = "🟡 Bon"
                        elif current_val <= 60:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    elif ratio_info["key"] == "ratio_cafg_ca":
                        if current_val >= 10:
                            current_status = "🟢 Excellent"
                        elif current_val >= 7:
                            current_status = "🟡 Bon"
                        elif current_val >= 5:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    else:  # intensite_capitaliste
                        if current_val < 2.0:
                            current_status = "🟢 Excellent"
                        elif current_val <= 3.0:
                            current_status = "🟡 Bon"
                        elif current_val <= 4.0:
                            current_status = "🟠 Acceptable"
                        else:
                            current_status = "🔴 Faible"
                    
                    # Afficher le barème
                    st.markdown(f"🟢 **Excellent:** {ratio_info['target_excellent']}")
                    st.markdown(f"🟡 **Bon:** {ratio_info['target_good']}")
                    st.markdown(f"🟠 **Acceptable:** {ratio_info['target_acceptable']}")
                    st.markdown(f"🔴 **Faible:** {ratio_info['target_poor']}")
                    
                    st.markdown("---")
                    st.markdown(f"### Votre Position: {current_status}")
                    
                    # Barre de progression visuelle
                    if ratio_info["key"] == "productivite_personnel":
                        progress_val = min(1, current_val / 4.0)
                    elif ratio_info["key"] == "taux_charges_personnel":
                        # Inverser (plus bas = mieux)
                        progress_val = max(0, min(1, (80 - current_val) / 80))
                    elif ratio_info["key"] == "ratio_cafg_ca":
                        progress_val = min(1, current_val / 12)
                    else:  # intensite_capitaliste
                        # Inverser (plus bas = mieux)
                        progress_val = max(0, min(1, (5 - current_val) / 5))
                    
                    st.progress(max(0, progress_val))
            
            st.markdown("---")
    
    # Section récapitulative pour les ratios de gestion
    st.markdown("---")
    st.markdown("### 📋 Synthèse Ratios de Gestion")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Points Forts")
        strong_points = []
        for ratio_info in management_ratios:
            if ratio_info["key"] in ratios:
                current_val = ratios[ratio_info["key"]]
                if ratio_info["key"] == "productivite_personnel" and current_val >= 2.0:
                    strong_points.append("✅ Bonne productivité du personnel")
                elif ratio_info["key"] == "taux_charges_personnel" and current_val <= 50:
                    strong_points.append("✅ Charges personnel maîtrisées")
                elif ratio_info["key"] == "ratio_cafg_ca" and current_val >= 7:
                    strong_points.append("✅ Bonne capacité d'autofinancement")
                elif ratio_info["key"] == "intensite_capitaliste" and current_val <= 3.0:
                    strong_points.append("✅ Intensité capitalistique raisonnable")
        
        if strong_points:
            for point in strong_points:
                st.markdown(point)
        else:
            st.info("Aucun point fort identifié selon les normes BCEAO")
    
    with col2:
        st.markdown("#### ⚠️ Points d'Amélioration")
        weak_points = []
        for ratio_info in management_ratios:
            if ratio_info["key"] in ratios:
                current_val = ratios[ratio_info["key"]]
                if ratio_info["key"] == "productivite_personnel" and current_val < 2.0:
                    weak_points.append("🔍 Améliorer la productivité du personnel")
                elif ratio_info["key"] == "taux_charges_personnel" and current_val > 50:
                    weak_points.append("🔍 Réduire les charges de personnel")
                elif ratio_info["key"] == "ratio_cafg_ca" and current_val < 7:
                    weak_points.append("🔍 Améliorer la génération de cash")
                elif ratio_info["key"] == "intensite_capitaliste" and current_val > 3.0:
                    weak_points.append("🔍 Optimiser l'utilisation des immobilisations")
        
        if weak_points:
            for point in weak_points:
                st.markdown(point)
        else:
            st.success("Tous les ratios respectent les normes BCEAO")

def show_sectoral_comparison_detailed(ratios, secteur):
    """Affiche la comparaison sectorielle détaillée"""
    
    st.header("🔍 Comparaison Sectorielle Détaillée")
    
    if not secteur:
        st.warning("Secteur non spécifié pour la comparaison")
        return
    
    # Données sectorielles simplifiées (à remplacer par des données réelles)
    sectoral_data = {
        'industrie_manufacturiere': {
            'ratio_liquidite_generale': {'q1': 1.2, 'median': 1.8, 'q3': 2.5},
            'ratio_autonomie_financiere': {'q1': 25, 'median': 40, 'q3': 55},
            'roe': {'q1': 8, 'median': 15, 'q3': 22},
            'marge_nette': {'q1': 2, 'median': 4.5, 'q3': 8}
        },
        'commerce_detail': {
            'ratio_liquidite_generale': {'q1': 1.0, 'median': 1.5, 'q3': 2.2},
            'ratio_autonomie_financiere': {'q1': 20, 'median': 35, 'q3': 50},
            'roe': {'q1': 5, 'median': 12, 'q3': 20},
            'marge_nette': {'q1': 0.5, 'median': 2, 'q3': 4}
        },
        'services_professionnels': {
            'ratio_liquidite_generale': {'q1': 1.2, 'median': 1.7, 'q3': 2.5},
            'ratio_autonomie_financiere': {'q1': 30, 'median': 45, 'q3': 65},
            'roe': {'q1': 15, 'median': 25, 'q3': 40},
            'marge_nette': {'q1': 5, 'median': 10, 'q3': 18}
        },
        'construction_btp': {
            'ratio_liquidite_generale': {'q1': 1.2, 'median': 1.5, 'q3': 1.9},
            'ratio_autonomie_financiere': {'q1': 22, 'median': 35, 'q3': 48},
            'roe': {'q1': 8, 'median': 16, 'q3': 28},
            'marge_nette': {'q1': 1.5, 'median': 3.5, 'q3': 6}
        },
        'agriculture': {
            'ratio_liquidite_generale': {'q1': 1.1, 'median': 1.6, 'q3': 2.3},
            'ratio_autonomie_financiere': {'q1': 35, 'median': 50, 'q3': 70},
            'roe': {'q1': 2, 'median': 8, 'q3': 15},
            'marge_nette': {'q1': -5, 'median': 2, 'q3': 8}
        },
        'commerce_gros': {
            'ratio_liquidite_generale': {'q1': 1.1, 'median': 1.4, 'q3': 1.8},
            'ratio_autonomie_financiere': {'q1': 18, 'median': 30, 'q3': 45},
            'roe': {'q1': 6, 'median': 12, 'q3': 20},
            'marge_nette': {'q1': 0.5, 'median': 1.5, 'q3': 3}
        }
    }
    
    if secteur not in sectoral_data:
        st.info("Données sectorielles détaillées non disponibles pour ce secteur")
        return
    
    st.subheader(f"📊 Positionnement - {secteur.replace('_', ' ').title()}")
    
    sector_ratios = sectoral_data[secteur]
    comparison_data = []
    
    for ratio_key, benchmarks in sector_ratios.items():
        if ratio_key in ratios:
            entreprise_val = ratios[ratio_key]
            q1, median, q3 = benchmarks['q1'], benchmarks['median'], benchmarks['q3']
            
            # Déterminer le quartile
            if entreprise_val >= q3:
                quartile = "Q4 (Top 25%)"
                color = "🟢"
            elif entreprise_val >= median:
                quartile = "Q3 (50-75%)"
                color = "🟡"
            elif entreprise_val >= q1:
                quartile = "Q2 (25-50%)"
                color = "🟠"
            else:
                quartile = "Q1 (Bottom 25%)"
                color = "🔴"
            
            comparison_data.append({
                'Ratio': ratio_key.replace('_', ' ').title(),
                'Votre Valeur': f"{entreprise_val:.2f}",
                'Q1 Secteur': f"{q1:.2f}",
                'Médiane': f"{median:.2f}",
                'Q3 Secteur': f"{q3:.2f}",
                'Position': f"{color} {quartile}"
            })
    
    if comparison_data:
        # Afficher le tableau avec formatage simple (pas de grandes masses ici)
        df_comparison = pd.DataFrame(comparison_data)
        # Ensure all columns are strings to avoid Arrow conversion issues
        df_comparison = df_comparison.astype(str)
        st.dataframe(df_comparison, hide_index=True, use_container_width=True)

def create_performance_radar(scores):
    """Crée un graphique radar des performances"""
    
    categories = ['Liquidité', 'Solvabilité', 'Rentabilité', 'Activité', 'Gestion']
    values = [
        scores.get('liquidite', 0) / 40 * 100,
        scores.get('solvabilite', 0) / 40 * 100,
        scores.get('rentabilite', 0) / 30 * 100,
        scores.get('activite', 0) / 15 * 100,
        scores.get('gestion', 0) / 15 * 100
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Performance Actuelle',
        line_color='rgb(46, 125, 50)',
        fillcolor='rgba(76, 175, 80, 0.3)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[100, 100, 100, 100, 100, 100],
        theta=categories + [categories[0]],
        fill='tonext',
        name='Performance Maximale',
        line_color='rgb(211, 47, 47)',
        fillcolor='rgba(244, 67, 54, 0.1)',
        line_dash='dash'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticktext=['0%', '25%', '50%', '75%', '100%'],
                tickvals=[0, 25, 50, 75, 100]
            )),
        showlegend=True,
        title="Radar de Performance par Catégorie BCEAO",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_waterfall_chart(data):
    """Crée un graphique waterfall des soldes intermédiaires"""
    
    st.subheader("📊 Formation du Résultat Net")
    
    # Calculs des soldes
    ca = data.get('chiffre_affaires', 0)
    charges_variables = (data.get('achats_marchandises', 0) + 
                        data.get('achats_matieres_premieres', 0) + 
                        data.get('autres_achats', 0))
    va = data.get('valeur_ajoutee', 0)
    charges_fixes = data.get('charges_personnel', 0)
    ebe = data.get('excedent_brut', 0)
    amortissements = data.get('dotations_amortissements', 0)
    re = data.get('resultat_exploitation', 0)
    rf = data.get('resultat_financier', 0)
    rn = data.get('resultat_net', 0)
    
    fig = go.Figure(go.Waterfall(
        name="Formation du Résultat",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "relative", "relative", "total"],
        x=["CA", "- Charges Variables", "- Charges Personnel", "- Amortissements", "+ Résultat Financier", "- Impôts", "= Résultat Net"],
        y=[ca, -charges_variables, -charges_fixes, -amortissements, rf, -data.get('impots_resultat', 0), rn],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
        text=[f"{ca:,.0f}", f"-{charges_variables:,.0f}", f"-{charges_fixes:,.0f}", 
              f"-{amortissements:,.0f}", f"{rf:+,.0f}", f"-{data.get('impots_resultat', 0):,.0f}", f"{rn:,.0f}"],
        textposition="outside"
    ))
    
    fig.update_layout(
        title="Formation du Résultat Net - Waterfall",
        height=500,
        yaxis_title="Montant (FCFA)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def get_ratio_status(value, threshold, higher_is_better=True):
    """Retourne le statut d'un ratio avec icône"""
    
    if higher_is_better:
        if value >= threshold * 1.2:
            return "🟢 Excellent"
        elif value >= threshold:
            return "🟡 Bon"
        elif value >= threshold * 0.8:
            return "🟠 Acceptable"
        else:
            return "🔴 Faible"
    else:
        if value <= threshold * 0.8:
            return "🟢 Excellent"
        elif value <= threshold:
            return "🟡 Bon"
        elif value <= threshold * 1.2:
            return "🟠 Acceptable"
        else:
            return "🔴 Faible"

def display_formatted_balance_sheet(data_rows):
    """Affiche une section du bilan avec formatage Streamlit natif"""
    
    # Convertir en DataFrame avec formatage approprié
    formatted_data = []
    
    for row in data_rows:
        poste, montant = row
        
        if poste == "" and montant == "":
            # Ignorer les lignes vides
            continue
            
        # Nettoyer les markers ** pour l'affichage
        clean_poste = poste.replace("**", "") if isinstance(poste, str) else str(poste)
        clean_montant = montant.replace("**", "") if isinstance(montant, str) else str(montant)
        
        formatted_data.append([clean_poste, clean_montant])
    
    # Créer le DataFrame et l'afficher
    if formatted_data:
        df = pd.DataFrame(formatted_data, columns=["Poste", "Montant (FCFA)"])
        
        # Identifier les grandes masses pour le styling
        def highlight_major_categories(row):
            poste_original = None
            # Trouver le poste original correspondant
            for orig_row in data_rows:
                if orig_row[0].replace("**", "") == row["Poste"]:
                    poste_original = orig_row[0]
                    break
            
            if poste_original and poste_original.startswith("**") and poste_original.endswith("**"):
                if "TOTAL" in row["Poste"]:
                    return ['background-color: #e3f2fd; font-weight: bold; color: #1976d2'] * len(row)
                else:
                    return ['background-color: #f3e5f5; font-weight: bold; color: #7b1fa2'] * len(row)
            else:
                return [''] * len(row)
        
        # Ensure all columns are strings to avoid Arrow conversion issues
        df = df.astype(str)
        
        # Afficher avec style
        st.dataframe(
            df.style.apply(highlight_major_categories, axis=1),
            hide_index=True,
            use_container_width=True
        )
