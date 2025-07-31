"""
Page d'analyse financière complète pour OptimusCredit
Version finale avec toutes les fonctionnalités
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Import du gestionnaire de session
try:
    from session_manager import SessionManager
except ImportError:
    st.error("❌ Impossible d'importer session_manager.py")
    st.stop()

def show_analysis_page():
    """Page d'analyse financière complète - Point d'entrée principal"""
    
    # Vérifier si des données d'analyse existent
    if not SessionManager.has_analysis_data():
        st.warning("⚠️ Aucune analyse disponible. Veuillez d'abord importer et analyser un fichier.")
        st.info("👈 Utilisez le menu de navigation pour accéder à la page d'import Excel.")
        
        # Boutons de redirection
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Import Excel", key="analysis_goto_import", type="primary"):
                SessionManager.set_current_page('excel_import')
                st.rerun()
        with col2:
            if st.button("✏️ Saisie Manuelle", key="analysis_goto_manual", type="secondary"):
                SessionManager.set_current_page('manual_input')
                st.rerun()
        return
    
    # Récupérer les données d'analyse
    analysis_data = SessionManager.get_analysis_data()
    if not analysis_data:
        st.error("❌ Erreur lors de la récupération des données d'analyse")
        return
    
    data = analysis_data['data']
    ratios = analysis_data['ratios']
    scores = analysis_data['scores']
    metadata = analysis_data['metadata']
    
    # Afficher l'analyse complète
    st.title("📊 Analyse Financière Complète - BCEAO")
    
    # En-tête avec informations principales
    display_analysis_header(data, scores, metadata)
    
    # Tabs pour organiser l'affichage
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Synthèse Executive", "📊 États Financiers", "📈 Ratios Détaillés", 
        "📉 Graphiques Interactifs", "🎯 Recommandations"
    ])
    
    with tab1:
        display_executive_summary(data, ratios, scores, metadata)
    
    with tab2:
        display_financial_statements(data)
    
    with tab3:
        display_detailed_ratios(ratios, metadata.get('secteur'))
    
    with tab4:
        display_interactive_charts(data, ratios, scores)
    
    with tab5:
        display_detailed_recommendations(data, ratios, scores)

def display_analysis_header(data, scores, metadata):
    """Affiche l'en-tête de l'analyse"""
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        filename = metadata.get('fichier_nom', 'Analyse financière')
        secteur = metadata.get('secteur', 'Non spécifié').replace('_', ' ').title()
        date_analyse = metadata.get('date_analyse', datetime.now().strftime('%Y-%m-%d %H:%M'))
        source = metadata.get('source', 'Import')
        
        st.markdown(f"""
        **📄 Source:** {filename}  
        **🏭 Secteur:** {secteur}  
        **📅 Date d'analyse:** {date_analyse}  
        **📋 Type:** {source.replace('_', ' ').title()}
        """)
    
    with col2:
        score_global = scores.get('global', 0)
        classe_financiere = SessionManager.get_financial_class(score_global)
        interpretation, color = SessionManager.get_interpretation(score_global)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; border-radius: 10px; background-color: {color}20; border: 2px solid {color};">
            <h3 style="color: {color}; margin: 0;">Score BCEAO</h3>
            <h1 style="color: {color}; margin: 10px 0;">{score_global}/100</h1>
            <p style="color: {color}; margin: 0; font-weight: bold;">Classe {classe_financiere}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        ca = data.get('chiffre_affaires', 0)
        actif = data.get('total_actif', 0)
        
        st.metric("Chiffre d'Affaires", f"{ca:,.0f}".replace(',', ' ') + " FCFA")
        st.metric("Total Actif", f"{actif:,.0f}".replace(',', ' ') + " FCFA")

def display_executive_summary(data, ratios, scores, metadata):
    """Affiche le résumé exécutif"""
    
    st.header("🎯 Synthèse Executive")
    
    # Évaluation globale
    score_global = scores.get('global', 0)
    interpretation, color = SessionManager.get_interpretation(score_global)
    
    if score_global >= 70:
        st.success(f"✅ {interpretation} - L'entreprise présente une situation financière solide.")
    elif score_global >= 40:
        st.warning(f"⚠️ {interpretation} - Des améliorations sont possibles dans certains domaines.")
    else:
        st.error(f"❌ {interpretation} - Des actions correctives sont nécessaires.")
    
    # Scores par catégorie
    st.subheader("📊 Performance par Catégorie")
    
    categories_data = [
        ("💧 Liquidité", scores.get('liquidite', 0), 40),
        ("🏛️ Solvabilité", scores.get('solvabilite', 0), 40), 
        ("📈 Rentabilité", scores.get('rentabilite', 0), 30),
        ("⚡ Activité", scores.get('activite', 0), 15),
        ("🔧 Gestion", scores.get('gestion', 0), 15)
    ]
    
    # Affichage en tableau avec statuts
    perf_data = []
    for label, score, max_score in categories_data:
        percentage = (score / max_score) * 100
        status = get_performance_status(percentage)
        perf_data.append([label, f"{score}/{max_score}", f"{percentage:.0f}%", status])
    
    df_perf = pd.DataFrame(perf_data, columns=["Catégorie", "Score", "Performance", "Statut"])
    st.dataframe(df_perf, hide_index=True, use_container_width=True)
    
    # Ratios clés avec comparaison aux normes
    st.subheader("🔑 Ratios Clés vs Normes BCEAO")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        liquidite = ratios.get('ratio_liquidite_generale', 0)
        delta = get_ratio_delta_text(liquidite, 1.5, True)
        st.metric("Liquidité Générale", f"{liquidite:.2f}", delta)
        st.caption("Norme: > 1.5")
    
    with col2:
        autonomie = ratios.get('ratio_autonomie_financiere', 0)
        delta = get_ratio_delta_text(autonomie, 30, True)
        st.metric("Autonomie Financière", f"{autonomie:.1f}%", delta)
        st.caption("Norme: > 30%")
    
    with col3:
        roe = ratios.get('roe', 0)
        delta = get_ratio_delta_text(roe, 10, True)
        st.metric("ROE", f"{roe:.1f}%", delta)
        st.caption("Norme: > 10%")
    
    with col4:
        marge = ratios.get('marge_nette', 0)
        delta = get_ratio_delta_text(marge, 5, True)
        st.metric("Marge Nette", f"{marge:.1f}%", delta)
        st.caption("Norme: > 5%")
    
    # Points forts et points faibles
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Points Forts")
        strengths = identify_strengths(scores, ratios)
        if strengths:
            for strength in strengths[:5]:
                st.success(f"• {strength}")
        else:
            st.info("• Analyse en cours...")
    
    with col2:
        st.subheader("⚠️ Axes d'Amélioration")
        weaknesses = identify_weaknesses(scores, ratios)
        if weaknesses:
            for weakness in weaknesses[:5]:
                st.warning(f"• {weakness}")
        else:
            st.success("• Situation globalement satisfaisante")

def display_financial_statements(data):
    """Affiche les états financiers détaillés"""
    
    st.header("📊 États Financiers Détaillés")
    
    # Sous-tabs pour les états
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["Bilan", "Compte de Résultat", "Flux de Trésorerie"])
    
    with sub_tab1:
        display_balance_sheet(data)
    
    with sub_tab2:
        display_income_statement(data)
    
    with sub_tab3:
        display_cash_flow(data)

def display_balance_sheet(data):
    """Affiche le bilan détaillé"""
    
    st.subheader("📊 Bilan Synthétique")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ACTIF")
        
        # Regrouper les données d'actif
        actif_data = [
            ["Immobilisations nettes", data.get('immobilisations_nettes', 0)],
            ["Stocks", data.get('stocks', 0)],
            ["Créances clients", data.get('creances_clients', 0)],
            ["Autres créances", data.get('autres_creances', 0)],
            ["Trésorerie", data.get('tresorerie', 0)],
            ["**TOTAL ACTIF**", data.get('total_actif', 0)]
        ]
        
        df_actif = pd.DataFrame(actif_data, columns=["Poste", "Montant (FCFA)"])
        df_actif['Montant (FCFA)'] = df_actif['Montant (FCFA)'].apply(lambda x: f"{x:,.0f}".replace(',', ' '))
        st.dataframe(df_actif, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("#### PASSIF")
        
        # Regrouper les données de passif
        passif_data = [
            ["Capitaux propres", data.get('capitaux_propres', 0)],
            ["Dettes financières", data.get('dettes_financieres', 0)],
            ["Dettes court terme", data.get('dettes_court_terme', 0)],
            ["Trésorerie passif", data.get('tresorerie_passif', 0)],
            ["**TOTAL PASSIF**", 
             data.get('capitaux_propres', 0) + data.get('dettes_financieres', 0) + 
             data.get('dettes_court_terme', 0) + data.get('tresorerie_passif', 0)]
        ]
        
        df_passif = pd.DataFrame(passif_data, columns=["Poste", "Montant (FCFA)"])
        df_passif['Montant (FCFA)'] = df_passif['Montant (FCFA)'].apply(lambda x: f"{x:,.0f}".replace(',', ' '))
        st.dataframe(df_passif, hide_index=True, use_container_width=True)
    
    # Structure du bilan
    st.markdown("#### Structure du Bilan")
    
    total_actif = data.get('total_actif', 1)
    structure_data = [
        ["Immobilisations", data.get('immobilisations_nettes', 0), f"{data.get('immobilisations_nettes', 0)/total_actif*100:.1f}%"],
        ["Actif circulant", data.get('stocks', 0) + data.get('creances_clients', 0) + data.get('autres_creances', 0), f"{(data.get('stocks', 0) + data.get('creances_clients', 0) + data.get('autres_creances', 0))/total_actif*100:.1f}%"],
        ["Trésorerie", data.get('tresorerie', 0), f"{data.get('tresorerie', 0)/total_actif*100:.1f}%"]
    ]
    
    df_structure = pd.DataFrame(structure_data, columns=["Composante", "Montant (FCFA)", "% Total"])
    df_structure['Montant (FCFA)'] = df_structure['Montant (FCFA)'].apply(lambda x: f"{x:,.0f}".replace(',', ' '))
    st.dataframe(df_structure, hide_index=True, use_container_width=True)

def display_income_statement(data):
    """Affiche le compte de résultat"""
    
    st.subheader("📈 Compte de Résultat - Soldes Intermédiaires")
    
    # Soldes intermédiaires de gestion
    ca = data.get('chiffre_affaires', 0)
    sig_data = [
        ["Chiffre d'Affaires", ca, "100.0%"],
        ["Valeur Ajoutée", data.get('valeur_ajoutee', 0), 
         f"{data.get('valeur_ajoutee', 0)/ca*100:.1f}%" if ca > 0 else ""],
        ["Excédent Brut d'Exploitation", data.get('excedent_brut', 0),
         f"{data.get('excedent_brut', 0)/ca*100:.1f}%" if ca > 0 else ""],
        ["Résultat d'Exploitation", data.get('resultat_exploitation', 0),
         f"{data.get('resultat_exploitation', 0)/ca*100:.1f}%" if ca > 0 else ""],
        ["Résultat Net", data.get('resultat_net', 0),
         f"{data.get('resultat_net', 0)/ca*100:.1f}%" if ca > 0 else ""]
    ]
    
    df_sig = pd.DataFrame(sig_data, columns=["Solde Intermédiaire", "Montant (FCFA)", "% CA"])
    df_sig['Montant (FCFA)'] = df_sig['Montant (FCFA)'].apply(lambda x: f"{x:,.0f}".replace(',', ' '))
    st.dataframe(df_sig, hide_index=True, use_container_width=True)

def display_cash_flow(data):
    """Affiche les flux de trésorerie"""
    
    st.subheader("💰 Flux de Trésorerie")
    
    if data.get('cafg', 0) == 0:
        st.info("📋 Données de flux de trésorerie non disponibles ou incomplètes")
        
        # Calculer une CAFG approximative
        cafg_approx = data.get('resultat_net', 0) + data.get('dotations_amortissements', 0)
        if cafg_approx > 0:
            st.markdown("#### Estimation de la Capacité d'Autofinancement")
            st.metric("CAFG Estimée", f"{cafg_approx:,.0f}".replace(',', ' ') + " FCFA")
            st.caption("Calcul: Résultat Net + Dotations aux Amortissements")
        return
    
    flux_data = [
        ["CAFG", data.get('cafg', 0)],
        ["Flux activités opérationnelles", data.get('flux_activites_operationnelles', 0)],
        ["Flux activités d'investissement", data.get('flux_activites_investissement', 0)],
        ["Flux activités de financement", data.get('flux_activites_financement', 0)],
        ["Variation de trésorerie", data.get('variation_tresorerie', 0)]
    ]
    
    df_flux = pd.DataFrame(flux_data, columns=["Poste", "Montant (FCFA)"])
    df_flux['Montant (FCFA)'] = df_flux['Montant (FCFA)'].apply(lambda x: f"{x:,.0f}".replace(',', ' '))
    st.dataframe(df_flux, hide_index=True, use_container_width=True)

def display_detailed_ratios(ratios, secteur):
    """Affiche l'analyse détaillée des ratios"""
    
    st.header("📈 Analyse Détaillée des Ratios")
    
    # Catégories de ratios avec onglets
    ratio_tabs = st.tabs(["💧 Liquidité", "🏛️ Solvabilité", "📈 Rentabilité", "⚡ Activité", "🔧 Gestion"])
    
    with ratio_tabs[0]:
        display_liquidity_ratios(ratios)
    
    with ratio_tabs[1]:
        display_solvency_ratios(ratios)
    
    with ratio_tabs[2]:
        display_profitability_ratios(ratios)
    
    with ratio_tabs[3]:
        display_activity_ratios(ratios)
    
    with ratio_tabs[4]:
        display_management_ratios(ratios)

def display_liquidity_ratios(ratios):
    """Affiche les ratios de liquidité"""
    
    st.subheader("💧 Ratios de Liquidité")
    
    liquidity_data = []
    
    if 'ratio_liquidite_generale' in ratios:
        liquidity_data.append([
            "Liquidité Générale", 
            f"{ratios['ratio_liquidite_generale']:.2f}",
            "> 1.5",
            get_ratio_interpretation(ratios['ratio_liquidite_generale'], 1.5, True),
            "Capacité à honorer les dettes à court terme"
        ])
    
    if 'ratio_liquidite_immediate' in ratios:
        liquidity_data.append([
            "Liquidité Immédiate",
            f"{ratios['ratio_liquidite_immediate']:.2f}",
            "> 1.0", 
            get_ratio_interpretation(ratios['ratio_liquidite_immediate'], 1.0, True),
            "Liquidité sans compter les stocks"
        ])
    
    if 'bfr_jours_ca' in ratios:
        liquidity_data.append([
            "BFR en jours de CA",
            f"{ratios['bfr_jours_ca']:.0f} jours",
            "< 60 jours",
            get_ratio_interpretation(ratios['bfr_jours_ca'], 60, False),
            "Besoin de financement du cycle d'exploitation"
        ])
    
    if 'tresorerie_nette' in ratios:
        liquidity_data.append([
            "Trésorerie Nette",
            f"{ratios['tresorerie_nette']:,.0f} FCFA".replace(',', ' '),
            "> 0",
            "Positive" if ratios['tresorerie_nette'] > 0 else "Négative",
            "Situation de trésorerie nette"
        ])
    
    if liquidity_data:
        df = pd.DataFrame(liquidity_data, columns=["Ratio", "Valeur", "Norme BCEAO", "Évaluation", "Signification"])
        st.dataframe(df, hide_index=True, use_container_width=True)

def display_solvency_ratios(ratios):
    """Affiche les ratios de solvabilité"""
    
    st.subheader("🏛️ Ratios de Solvabilité")
    
    solvency_data = []
    
    if 'ratio_autonomie_financiere' in ratios:
        solvency_data.append([
            "Autonomie Financière",
            f"{ratios['ratio_autonomie_financiere']:.1f}%",
            "> 30%",
            get_ratio_interpretation(ratios['ratio_autonomie_financiere'], 30, True),
            "Indépendance vis-à-vis des créanciers"
        ])
    
    if 'ratio_endettement' in ratios:
        solvency_data.append([
            "Endettement Global",
            f"{ratios['ratio_endettement']:.1f}%", 
            "< 65%",
            get_ratio_interpretation(ratios['ratio_endettement'], 65, False),
            "Niveau global d'endettement"
        ])
    
    if 'capacite_remboursement' in ratios:
        solvency_data.append([
            "Capacité de Remboursement",
            f"{ratios['capacite_remboursement']:.1f} années",
            "< 5 ans",
            get_ratio_interpretation(ratios['capacite_remboursement'], 5, False),
            "Temps nécessaire pour rembourser les dettes"
        ])
    
    if solvency_data:
        df = pd.DataFrame(solvency_data, columns=["Ratio", "Valeur", "Norme BCEAO", "Évaluation", "Signification"])
        st.dataframe(df, hide_index=True, use_container_width=True)

def display_profitability_ratios(ratios):
    """Affiche les ratios de rentabilité"""
    
    st.subheader("📈 Ratios de Rentabilité")
    
    profitability_data = []
    
    if 'roe' in ratios:
        profitability_data.append([
            "ROE (Return on Equity)",
            f"{ratios['roe']:.1f}%",
            "> 10%",
            get_ratio_interpretation(ratios['roe'], 10, True),
            "Rentabilité des capitaux propres"
        ])
    
    if 'roa' in ratios:
        profitability_data.append([
            "ROA (Return on Assets)",
            f"{ratios['roa']:.1f}%",
            "> 2%",
            get_ratio_interpretation(ratios['roa'], 2, True),
            "Rentabilité de l'ensemble des actifs"
        ])
    
    if 'marge_nette' in ratios:
        profitability_data.append([
            "Marge Nette",
            f"{ratios['marge_nette']:.1f}%",
            "> 5%",
            get_ratio_interpretation(ratios['marge_nette'], 5, True),
            "Rentabilité après toutes charges"
        ])
    
    if 'marge_exploitation' in ratios:
        profitability_data.append([
            "Marge d'Exploitation",
            f"{ratios['marge_exploitation']:.1f}%",
            "> 5%",
            get_ratio_interpretation(ratios['marge_exploitation'], 5, True),
            "Rentabilité de l'activité principale"
        ])
    
    if profitability_data:
        df = pd.DataFrame(profitability_data, columns=["Ratio", "Valeur", "Norme BCEAO", "Évaluation", "Signification"])
        st.dataframe(df, hide_index=True, use_container_width=True)

def display_activity_ratios(ratios):
    """Affiche les ratios d'activité"""
    
    st.subheader("⚡ Ratios d'Activité")
    
    activity_data = []
    
    if 'rotation_actif' in ratios:
        activity_data.append([
            "Rotation de l'Actif",
            f"{ratios['rotation_actif']:.2f}",
            "> 1.5",
            get_ratio_interpretation(ratios['rotation_actif'], 1.5, True),
            "Efficacité d'utilisation des actifs"
        ])
    
    if 'rotation_stocks' in ratios:
        activity_data.append([
            "Rotation des Stocks",
            f"{ratios['rotation_stocks']:.1f}",
            "> 6",
            get_ratio_interpretation(ratios['rotation_stocks'], 6, True),
            "Vitesse d'écoulement des stocks"
        ])
    
    if 'delai_recouvrement_clients' in ratios:
        activity_data.append([
            "Délai Recouvrement",
            f"{ratios['delai_recouvrement_clients']:.0f} jours",
            "< 45 jours",
            get_ratio_interpretation(ratios['delai_recouvrement_clients'], 45, False),
            "Temps de recouvrement des créances"
        ])
    
    if activity_data:
        df = pd.DataFrame(activity_data, columns=["Ratio", "Valeur", "Norme BCEAO", "Évaluation", "Signification"])
        st.dataframe(df, hide_index=True, use_container_width=True)

def display_management_ratios(ratios):
    """Affiche les ratios de gestion"""
    
    st.subheader("🔧 Ratios de Gestion")
    
    management_data = []
    
    if 'productivite_personnel' in ratios:
        management_data.append([
            "Productivité du Personnel",
            f"{ratios['productivite_personnel']:.2f}",
            "> 2.0",
            get_ratio_interpretation(ratios['productivite_personnel'], 2.0, True),
            "Efficacité de la main d'œuvre"
        ])
    
    if 'taux_charges_personnel' in ratios:
        management_data.append([
            "Charges Personnel / VA",
            f"{ratios['taux_charges_personnel']:.1f}%",
            "< 50%",
            get_ratio_interpretation(ratios['taux_charges_personnel'], 50, False),
            "Poids du personnel dans la valeur ajoutée"
        ])
    
    if 'ratio_cafg_ca' in ratios:
        management_data.append([
            "CAFG / CA",
            f"{ratios['ratio_cafg_ca']:.1f}%",
            "> 7%",
            get_ratio_interpretation(ratios['ratio_cafg_ca'], 7, True),
            "Capacité d'autofinancement relative"
        ])
    
    if management_data:
        df = pd.DataFrame(management_data, columns=["Ratio", "Valeur", "Norme BCEAO", "Évaluation", "Signification"])
        st.dataframe(df, hide_index=True, use_container_width=True)

def display_interactive_charts(data, ratios, scores):
    """Affiche les graphiques interactifs"""
    
    st.header("📉 Visualisations Interactives")
    
    # 1. Radar des performances
    create_performance_radar(scores)
    
    # 2. Graphique des soldes intermédiaires
    create_sig_waterfall(data)
    
    # 3. Comparaison avec les normes
    create_ratios_comparison_chart(ratios)

def create_performance_radar(scores):
    """Crée le radar de performance"""
    
    st.subheader("🎯 Radar de Performance BCEAO")
    
    categories = ['Liquidité', 'Solvabilité', 'Rentabilité', 'Activité', 'Gestion']
    values = [
        scores.get('liquidite', 0) / 40 * 100,
        scores.get('solvabilite', 0) / 40 * 100,
        scores.get('rentabilite', 0) / 30 * 100,
        scores.get('activite', 0) / 15 * 100,
        scores.get('gestion', 0) / 15 * 100
    ]
    
    fig = go.Figure()
    
    # Performance actuelle
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Performance actuelle',
        line_color='rgb(46, 125, 50)',
        fillcolor='rgba(76, 175, 80, 0.3)'
    ))
    
    # Objectif 100%
    fig.add_trace(go.Scatterpolar(
        r=[100, 100, 100, 100, 100, 100],
        theta=categories + [categories[0]],
        fill='tonext',
        name='Objectif (100%)',
        line_color='rgb(211, 47, 47)',
        fillcolor='rgba(244, 67, 54, 0.1)',
        line_dash='dash'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticktext=['0%', '20%', '40%', '60%', '80%', '100%'],
                tickvals=[0, 20, 40, 60, 80, 100]
            )),
        showlegend=True,
        title="Performance par Catégorie (%)",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_sig_waterfall(data):
    """Crée le graphique waterfall des soldes intermédiaires"""
    
    st.subheader("📊 Formation du Résultat (Waterfall)")
    
    if data.get('chiffre_affaires', 0) == 0:
        st.info("Données insuffisantes pour créer le graphique waterfall")
        return
    
    # Graphique en barres simple si waterfall complexe
    categories = ['CA', 'Valeur Ajoutée', 'EBE', 'Résultat Exploitation', 'Résultat Net']
    values = [
        data.get('chiffre_affaires', 0),
        data.get('valeur_ajoutee', 0),
        data.get('excedent_brut', 0),
        data.get('resultat_exploitation', 0),
        data.get('resultat_net', 0)
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        name='Soldes Intermédiaires',
        marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
        text=[f"{v:,.0f}".replace(',', ' ') for v in values],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Évolution des Soldes Intermédiaires de Gestion",
        xaxis_title="Indicateurs",
        yaxis_title="Montant (FCFA)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_ratios_comparison_chart(ratios):
    """Crée le graphique de comparaison avec les normes"""
    
    st.subheader("📈 Vos Ratios vs Normes BCEAO")
    
    # Ratios clés avec leurs normes
    ratios_comparison = [
        ('Liquidité Générale', ratios.get('ratio_liquidite_generale', 0), 1.5),
        ('Autonomie Financière (%)', ratios.get('ratio_autonomie_financiere', 0), 30),
        ('ROE (%)', ratios.get('roe', 0), 10),
        ('Marge Nette (%)', ratios.get('marge_nette', 0), 5)
    ]
    
    ratios_names = [r[0] for r in ratios_comparison]
    entreprise_values = [r[1] for r in ratios_comparison]
    norme_values = [r[2] for r in ratios_comparison]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Votre Entreprise',
        x=ratios_names,
        y=entreprise_values,
        marker_color='lightblue',
        text=[f"{v:.1f}" for v in entreprise_values],
        textposition='auto'
    ))
    
    fig.add_trace(go.Bar(
        name='Norme BCEAO',
        x=ratios_names,
        y=norme_values,
        marker_color='red',
        opacity=0.7,
        text=[f"{v:.1f}" for v in norme_values],
        textposition='auto'
    ))
    
    fig.update_layout(
        barmode='group',
        title='Comparaison de vos ratios avec les normes BCEAO',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_detailed_recommendations(data, ratios, scores):
    """Affiche les recommandations détaillées"""
    
    st.header("🎯 Recommandations Stratégiques Détaillées")
    
    recommendations = generate_detailed_recommendations(data, ratios, scores)
    
    if not recommendations:
        st.success("✅ Félicitations ! Votre situation financière ne nécessite pas de recommandations urgentes.")
        st.info("💡 Continuez à surveiller vos ratios clés et maintenez les bonnes pratiques de gestion.")
        return
    
    # Organiser par priorité
    urgent = [r for r in recommendations if r.get('priority') == 'urgent']
    important = [r for r in recommendations if r.get('priority') == 'important']
    improvement = [r for r in recommendations if r.get('priority') == 'improvement']
    
    if urgent:
        st.subheader("🔴 Actions Urgentes (0-1 mois)")
        for rec in urgent:
            display_recommendation_card(rec)
    
    if important:
        st.subheader("🟠 Actions Importantes (1-3 mois)")
        for rec in important:
            display_recommendation_card(rec)
    
    if improvement:
        st.subheader("🟡 Améliorations (3-6 mois)")
        for rec in improvement:
            display_recommendation_card(rec)

def display_recommendation_card(rec):
    """Affiche une carte de recommandation"""
    
    with st.expander(f"{rec.get('title', 'Recommandation')}"):
        st.markdown(f"**Problème identifié:** {rec.get('problem', '')}")
        st.markdown(f"**Impact:** {rec.get('impact', '')}")
        
        if 'actions' in rec:
            st.markdown("**Actions recommandées:**")
            for action in rec['actions']:
                st.write(f"• {action}")
        
        if 'kpi' in rec:
            st.markdown("**Indicateurs de suivi:**")
            for kpi in rec['kpi']:
                st.write(f"📊 {kpi}")

def generate_detailed_recommendations(data, ratios, scores):
    """Génère des recommandations détaillées basées sur l'analyse"""
    
    recommendations = []
    
    # Recommandations de liquidité
    if scores.get('liquidite', 0) < 25:
        if ratios.get('ratio_liquidite_generale', 0) < 1.2:
            recommendations.append({
                'priority': 'urgent',
                'title': '💧 Améliorer la Liquidité Immédiatement',
                'problem': f"Ratio de liquidité critique ({ratios.get('ratio_liquidite_generale', 0):.2f})",
                'impact': 'Risque de défaillance à court terme et difficultés de paiement',
                'actions': [
                    'Négocier des délais de paiement avec les fournisseurs (30-60 jours)',
                    'Accélérer le recouvrement des créances clients (relances, escompte)',
                    'Réduire les stocks non essentiels et obsolètes',
                    'Négocier une ligne de crédit court terme d\'urgence',
                    'Reporter tous les investissements non critiques'
                ],
                'kpi': [
                    'Ratio de liquidité générale > 1.5',
                    'Délai de recouvrement < 45 jours',
                    'Rotation des stocks > 6',
                    'Trésorerie nette positive'
                ]
            })
    
    # Recommandations de solvabilité
    if scores.get('solvabilite', 0) < 25:
        if ratios.get('ratio_autonomie_financiere', 0) < 25:
            recommendations.append({
                'priority': 'important',
                'title': '🏛️ Renforcer la Structure Financière',
                'problem': f"Autonomie financière insuffisante ({ratios.get('ratio_autonomie_financiere', 0):.1f}%)",
                'impact': 'Structure financière déséquilibrée, dépendance excessive aux dettes',
                'actions': [
                    'Préparer une augmentation de capital avec les associés',
                    'Renégocier les conditions des dettes financières (taux, échéances)',
                    'Mettre en réserve tous les bénéfices futurs',
                    'Rechercher des subventions ou aides publiques',
                    'Envisager l\'entrée d\'un investisseur stratégique',
                    'Convertir une partie des dettes en capital si possible'
                ],
                'kpi': [
                    'Ratio d\'autonomie financière > 30%',
                    'Ratio d\'endettement < 65%',
                    'Capacité de remboursement < 5 ans',
                    'Couverture des charges financières > 3'
                ]
            })
    
    # Recommandations de rentabilité
    if scores.get('rentabilite', 0) < 15:
        if ratios.get('marge_nette', 0) < 3:
            recommendations.append({
                'priority': 'improvement',
                'title': '📈 Optimiser la Rentabilité',
                'problem': f"Marge nette insuffisante ({ratios.get('marge_nette', 0):.1f}%)",
                'impact': 'Capacité d\'autofinancement limitée, développement compromis',
                'actions': [
                    'Analyser la structure des coûts par produit/service',
                    'Revoir la politique de prix (étude de marché)',
                    'Optimiser les coûts opérationnels (négociation fournisseurs)',
                    'Améliorer la productivité (formation, outils)',
                    'Développer les produits/services à forte marge',
                    'Externaliser les activités non rentables'
                ],
                'kpi': [
                    'Marge nette > 5%',
                    'ROE > 10%',
                    'Marge d\'exploitation > 5%',
                    'Coefficient d\'exploitation < 65%'
                ]
            })
    
    # Recommandations d'activité
    if scores.get('activite', 0) < 8:
        if ratios.get('rotation_stocks', 0) < 4:
            recommendations.append({
                'priority': 'improvement',
                'title': '⚡ Améliorer l\'Efficacité Opérationnelle',
                'problem': f"Rotation des stocks lente ({ratios.get('rotation_stocks', 0):.1f})",
                'impact': 'Immobilisation excessive de fonds de roulement',
                'actions': [
                    'Analyser les stocks dormants et obsolètes',
                    'Améliorer la prévision de la demande',
                    'Négocier des approvisionnements en flux tendu',
                    'Diversifier les fournisseurs pour réduire les stocks de sécurité',
                    'Mettre en place un système de gestion des stocks (FIFO, ABC)'
                ],
                'kpi': [
                    'Rotation des stocks > 6',
                    'Durée d\'écoulement < 60 jours',
                    'Taux de rupture < 5%',
                    'BFR en jours de CA < 60'
                ]
            })
    
    # Recommandations de gestion
    if scores.get('gestion', 0) < 8:
        if ratios.get('taux_charges_personnel', 0) > 60:
            recommendations.append({
                'priority': 'improvement',
                'title': '🔧 Optimiser la Gestion',
                'problem': f"Charges de personnel élevées ({ratios.get('taux_charges_personnel', 0):.1f}% de la VA)",
                'impact': 'Productivité insuffisante, rigidité de la structure',
                'actions': [
                    'Analyser la productivité par service/collaborateur',
                    'Former le personnel aux nouvelles technologies',
                    'Optimiser l\'organisation du travail',
                    'Développer la polyvalence des équipes',
                    'Automatiser les tâches répétitives'
                ],
                'kpi': [
                    'Charges personnel / VA < 50%',
                    'Productivité personnel > 2.0',
                    'CA par employé en progression',
                    'CAFG / CA > 7%'
                ]
            })
    
    return recommendations

# Fonctions utilitaires

def get_performance_status(percentage):
    """Retourne le statut de performance"""
    if percentage >= 80:
        return "🟢 Excellent"
    elif percentage >= 60:
        return "🟡 Bon"
    elif percentage >= 40:
        return "🟠 Moyen"
    else:
        return "🔴 Faible"

def get_ratio_delta_text(value, threshold, higher_is_better=True):
    """Retourne le texte delta pour un ratio"""
    if higher_is_better:
        if value >= threshold:
            return f"✅ +{((value/threshold-1)*100):.0f}%"
        else:
            return f"❌ -{((1-value/threshold)*100):.0f}%"
    else:
        if value <= threshold:
            return f"✅ -{((1-value/threshold)*100):.0f}%"
        else:
            return f"❌ +{((value/threshold-1)*100):.0f}%"

def get_ratio_interpretation(value, threshold, higher_is_better=True):
    """Retourne l'interprétation d'un ratio"""
    if higher_is_better:
        if value >= threshold * 1.2:
            return "Excellent"
        elif value >= threshold:
            return "Bon"
        elif value >= threshold * 0.8:
            return "Acceptable"
        else:
            return "Faible"
    else:
        if value <= threshold * 0.8:
            return "Excellent"
        elif value <= threshold:
            return "Bon"
        elif value <= threshold * 1.2:
            return "Acceptable"
        else:
            return "Faible"

def identify_strengths(scores, ratios):
    """Identifie les points forts de l'entreprise"""
    strengths = []
    
    if scores.get('liquidite', 0) >= 30:
        strengths.append("Excellente liquidité")
    
    if scores.get('solvabilite', 0) >= 30:
        strengths.append("Structure financière solide")
    
    if scores.get('rentabilite', 0) >= 20:
        strengths.append("Rentabilité satisfaisante")
    
    if ratios.get('tresorerie_nette', 0) > 0:
        strengths.append("Trésorerie nette positive")
    
    if ratios.get('roe', 0) >= 15:
        strengths.append("Excellente rentabilité des capitaux propres")
    
    if ratios.get('ratio_autonomie_financiere', 0) >= 40:
        strengths.append("Forte autonomie financière")
    
    if ratios.get('rotation_stocks', 0) >= 8:
        strengths.append("Bonne rotation des stocks")
    
    if ratios.get('marge_nette', 0) >= 8:
        strengths.append("Marges bénéficiaires élevées")
    
    return strengths

def identify_weaknesses(scores, ratios):
    """Identifie les points faibles de l'entreprise"""
    weaknesses = []
    
    if scores.get('liquidite', 0) < 20:
        weaknesses.append("Liquidité insuffisante")
    
    if scores.get('solvabilite', 0) < 20:
        weaknesses.append("Structure financière fragile")
    
    if scores.get('rentabilite', 0) < 15:
        weaknesses.append("Rentabilité faible")
    
    if ratios.get('ratio_liquidite_generale', 0) < 1.2:
        weaknesses.append("Ratio de liquidité critique")
    
    if ratios.get('ratio_autonomie_financiere', 0) < 25:
        weaknesses.append("Dépendance excessive aux dettes")
    
    if ratios.get('marge_nette', 0) < 3:
        weaknesses.append("Marge nette insuffisante")
    
    if ratios.get('delai_recouvrement_clients', 0) > 60:
        weaknesses.append("Délai de recouvrement trop long")
    
    if ratios.get('rotation_stocks', 0) < 4:
        weaknesses.append("Rotation des stocks lente")
    
    return weaknesses