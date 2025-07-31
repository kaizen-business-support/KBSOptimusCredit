"""
Page d'analyse financière complète avec graphiques interactifs
Version corrigée sans bugs de réinitialisation
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# Import des modules internes
try:
    from session_manager import SessionManager
except ImportError as e:
    st.error(f"Erreur d'import: {e}")

def show_analysis_page():
    """Page d'analyse financière complète - Point d'entrée principal"""
    
    # Vérifier si des données d'analyse existent
    if not SessionManager.has_analysis_data():
        st.warning("⚠️ Aucune analyse disponible.")
        st.info("👈 Utilisez le menu de navigation pour analyser vos données financières.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Import Excel", type="primary", use_container_width=True):
                SessionManager.set_current_page('excel_import')
                st.rerun()
        with col2:
            if st.button("✏️ Saisie Manuelle", use_container_width=True):
                SessionManager.set_current_page('manual_input')
                st.rerun()
        return
    
    # Récupérer les données d'analyse
    analysis_data = SessionManager.get_analysis_data()
    data = analysis_data['data']
    ratios = analysis_data['ratios']
    scores = analysis_data['scores']
    metadata = analysis_data['metadata']
    
    # Afficher l'analyse complète
    display_complete_analysis(data, ratios, scores, metadata)

def display_complete_analysis(data: Dict[str, Any], ratios: Dict[str, Any], 
                            scores: Dict[str, Any], metadata: Dict[str, Any]):
    """Affiche l'analyse financière complète"""
    
    st.title("📊 Analyse Financière Complète - BCEAO")
    
    # En-tête avec informations principales
    display_analysis_header(data, scores, metadata)
    
    # Tabs pour organiser l'affichage
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Synthèse", "📊 États Financiers", "📈 Ratios", "📉 Graphiques", "🎯 Recommandations"
    ])
    
    with tab1:
        display_executive_summary(data, ratios, scores, metadata)
    
    with tab2:
        display_financial_statements(data)
    
    with tab3:
        display_ratios_analysis(ratios, metadata.get('secteur'))
    
    with tab4:
        display_interactive_charts(data, ratios, scores)
    
    with tab5:
        display_recommendations(data, ratios, scores)

def display_analysis_header(data: Dict[str, Any], scores: Dict[str, Any], metadata: Dict[str, Any]):
    """Affiche l'en-tête de l'analyse"""
    
    # Informations sur le fichier analysé
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        filename = metadata.get('fichier_nom', 'Fichier analysé')
        secteur = metadata.get('secteur', 'Non spécifié').replace('_', ' ').title()
        date_analyse = metadata.get('date_analyse', 'N/A')
        
        st.markdown(f"""
        **📄 Fichier:** {filename}  
        **🏭 Secteur:** {secteur}  
        **📅 Date d'analyse:** {date_analyse}
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
        
        st.metric("Chiffre d'Affaires", f"{ca:,.0f} FCFA")
        st.metric("Total Actif", f"{actif:,.0f} FCFA")

def display_executive_summary(data: Dict[str, Any], ratios: Dict[str, Any], 
                            scores: Dict[str, Any], metadata: Dict[str, Any]):
    """Affiche le résumé exécutif"""
    
    st.header("🎯 Résumé Exécutif")
    
    # Scores par catégorie
    st.subheader("📊 Performance par Catégorie")
    
    categories_scores = [
        ("💧 Liquidité", scores.get('liquidite', 0), 40),
        ("🏛️ Solvabilité", scores.get('solvabilite', 0), 40), 
        ("📈 Rentabilité", scores.get('rentabilite', 0), 30),
        ("⚡ Activité", scores.get('activite', 0), 15),
        ("🔧 Gestion", scores.get('gestion', 0), 15)
    ]
    
    # Affichage en colonnes
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for i, (label, score, max_score) in enumerate(categories_scores):
        with [col1, col2, col3, col4, col5][i]:
            percentage = (score / max_score) * 100
            color = get_performance_color(percentage)
            
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; border-radius: 8px; background-color: {color}20; border: 1px solid {color};">
                <h4 style="margin: 0; color: {color};">{label}</h4>
                <h2 style="margin: 5px 0; color: {color};">{score}/{max_score}</h2>
                <p style="margin: 0; color: {color}; font-weight: bold;">{percentage:.0f}%</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Ratios clés
    st.subheader("🔑 Ratios Clés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        liquidite = ratios.get('ratio_liquidite_generale', 0)
        status = get_ratio_status(liquidite, 1.5, True)
        st.metric("Liquidité Générale", f"{liquidite:.2f}", status)
    
    with col2:
        autonomie = ratios.get('ratio_autonomie_financiere', 0)
        status = get_ratio_status(autonomie, 30, True)
        st.metric("Autonomie Financière", f"{autonomie:.1f}%", status)
    
    with col3:
        roe = ratios.get('roe', 0)
        status = get_ratio_status(roe, 10, True)
        st.metric("ROE", f"{roe:.1f}%", status)
    
    with col4:
        marge = ratios.get('marge_nette', 0)
        status = get_ratio_status(marge, 5, True)
        st.metric("Marge Nette", f"{marge:.1f}%", status)
    
    # Points forts et faibles
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Points Forts")
        strengths = identify_strengths(scores, ratios)
        if strengths:
            for strength in strengths[:5]:
                st.success(f"• {strength}")
        else:
            st.info("Analyse en cours...")
    
    with col2:
        st.subheader("⚠️ Points d'Amélioration")
        weaknesses = identify_weaknesses(scores, ratios)
        if weaknesses:
            for weakness in weaknesses[:5]:
                st.warning(f"• {weakness}")
        else:
            st.info("Situation satisfaisante")

def display_financial_statements(data: Dict[str, Any]):
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

def display_balance_sheet(data: Dict[str, Any]):
    """Affiche le bilan détaillé"""
    
    st.subheader("📊 Bilan")
    
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

def display_income_statement(data: Dict[str, Any]):
    """Affiche le compte de résultat"""
    
    st.subheader("📈 Compte de Résultat")
    
    # Soldes intermédiaires de gestion
    sig_data = [
        ["Chiffre d'Affaires", data.get('chiffre_affaires', 0), "100.0%"],
        ["Valeur Ajoutée", data.get('valeur_ajoutee', 0), 
         f"{data.get('valeur_ajoutee', 0)/data.get('chiffre_affaires', 1)*100:.1f}%" if data.get('chiffre_affaires', 0) > 0 else ""],
        ["Excédent Brut d'Exploitation", data.get('excedent_brut', 0),
         f"{data.get('excedent_brut', 0)/data.get('chiffre_affaires', 1)*100:.1f}%" if data.get('chiffre_affaires', 0) > 0 else ""],
        ["Résultat d'Exploitation", data.get('resultat_exploitation', 0),
         f"{data.get('resultat_exploitation', 0)/data.get('chiffre_affaires', 1)*100:.1f}%" if data.get('chiffre_affaires', 0) > 0 else ""],
        ["Résultat Net", data.get('resultat_net', 0),
         f"{data.get('resultat_net', 0)/data.get('chiffre_affaires', 1)*100:.1f}%" if data.get('chiffre_affaires', 0) > 0 else ""]
    ]
    
    df_sig = pd.DataFrame(sig_data, columns=["Poste", "Montant (FCFA)", "% CA"])
    df_sig['Montant (FCFA)'] = df_sig['Montant (FCFA)'].apply(lambda x: f"{x:,.0f}".replace(',', ' '))
    st.dataframe(df_sig, hide_index=True, use_container_width=True)

def display_cash_flow(data: Dict[str, Any]):
    """Affiche les flux de trésorerie"""
    
    st.subheader("💰 Flux de Trésorerie")
    
    if data.get('cafg', 0) == 0:
        st.info("Données de flux de trésorerie non disponibles dans ce fichier")
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

def display_ratios_analysis(ratios: Dict[str, Any], secteur: Optional[str]):
    """Affiche l'analyse des ratios"""
    
    st.header("📈 Analyse des Ratios")
    
    # Catégories de ratios
    ratio_tabs = st.tabs(["💧 Liquidité", "🏛️ Solvabilité", "📈 Rentabilité", "⚡ Activité"])
    
    with ratio_tabs[0]:
        display_liquidity_ratios(ratios)
    
    with ratio_tabs[1]:
        display_solvency_ratios(ratios)
    
    with ratio_tabs[2]:
        display_profitability_ratios(ratios)
    
    with ratio_tabs[3]:
        display_activity_ratios(ratios)

def display_liquidity_ratios(ratios: Dict[str, Any]):
    """Affiche les ratios de liquidité"""
    
    st.subheader("💧 Ratios de Liquidité")
    
    liquidity_data = []
    
    if 'ratio_liquidite_generale' in ratios:
        liquidity_data.append([
            "Liquidité Générale", 
            f"{ratios['ratio_liquidite_generale']:.2f}",
            "> 1.5",
            get_ratio_interpretation(ratios['ratio_liquidite_generale'], 1.5, True)
        ])
    
    if 'ratio_liquidite_immediate' in ratios:
        liquidity_data.append([
            "Liquidité Immédiate",
            f"{ratios['ratio_liquidite_immediate']:.2f}",
            "> 1.0", 
            get_ratio_interpretation(ratios['ratio_liquidite_immediate'], 1.0, True)
        ])
    
    if 'bfr_jours_ca' in ratios:
        liquidity_data.append([
            "BFR en jours de CA",
            f"{ratios['bfr_jours_ca']:.0f} jours",
            "< 60 jours",
            get_ratio_interpretation(ratios['bfr_jours_ca'], 60, False)
        ])
    
    if liquidity_data:
        df = pd.DataFrame(liquidity_data, columns=["Ratio", "Valeur", "Norme", "Interprétation"])
        st.dataframe(df, hide_index=True, use_container_width=True)

def display_solvency_ratios(ratios: Dict[str, Any]):
    """Affiche les ratios de solvabilité"""
    
    st.subheader("🏛️ Ratios de Solvabilité")
    
    solvency_data = []
    
    if 'ratio_autonomie_financiere' in ratios:
        solvency_data.append([
            "Autonomie Financière",
            f"{ratios['ratio_autonomie_financiere']:.1f}%",
            "> 30%",
            get_ratio_interpretation(ratios['ratio_autonomie_financiere'], 30, True)
        ])
    
    if 'ratio_endettement' in ratios:
        solvency_data.append([
            "Endettement Global",
            f"{ratios['ratio_endettement']:.1f}%", 
            "< 65%",
            get_ratio_interpretation(ratios['ratio_endettement'], 65, False)
        ])
    
    if 'capacite_remboursement' in ratios:
        solvency_data.append([
            "Capacité de Remboursement",
            f"{ratios['capacite_remboursement']:.1f} années",
            "< 5 ans",
            get_ratio_interpretation(ratios['capacite_remboursement'], 5, False)
        ])
    
    if solvency_data:
        df = pd.DataFrame(solvency_data, columns=["Ratio", "Valeur", "Norme", "Interprétation"])
        st.dataframe(df, hide_index=True, use_container_width=True)

def display_profitability_ratios(ratios: Dict[str, Any]):
    """Affiche les ratios de rentabilité"""
    
    st.subheader("📈 Ratios de Rentabilité")
    
    profitability_data = []
    
    if 'roe' in ratios:
        profitability_data.append([
            "ROE (Return on Equity)",
            f"{ratios['roe']:.1f}%",
            "> 10%",
            get_ratio_interpretation(ratios['roe'], 10, True)
        ])
    
    if 'roa' in ratios:
        profitability_data.append([
            "ROA (Return on Assets)",
            f"{ratios['roa']:.1f}%",
            "> 2%",
            get_ratio_interpretation(ratios['roa'], 2, True)
        ])
    
    if 'marge_nette' in ratios:
        profitability_data.append([
            "Marge Nette",
            f"{ratios['marge_nette']:.1f}%",
            "> 5%",
            get_ratio_interpretation(ratios['marge_nette'], 5, True)
        ])
    
    if profitability_data:
        df = pd.DataFrame(profitability_data, columns=["Ratio", "Valeur", "Norme", "Interprétation"])
        st.dataframe(df, hide_index=True, use_container_width=True)

def display_activity_ratios(ratios: Dict[str, Any]):
    """Affiche les ratios d'activité"""
    
    st.subheader("⚡ Ratios d'Activité")
    
    activity_data = []
    
    if 'rotation_actif' in ratios:
        activity_data.append([
            "Rotation de l'Actif",
            f"{ratios['rotation_actif']:.2f}",
            "> 1.5",
            get_ratio_interpretation(ratios['rotation_actif'], 1.5, True)
        ])
    
    if 'rotation_stocks' in ratios:
        activity_data.append([
            "Rotation des Stocks",
            f"{ratios['rotation_stocks']:.1f}",
            "> 6",
            get_ratio_interpretation(ratios['rotation_stocks'], 6, True)
        ])
    
    if 'delai_recouvrement_clients' in ratios:
        activity_data.append([
            "Délai Recouvrement",
            f"{ratios['delai_recouvrement_clients']:.0f} jours",
            "< 45 jours",
            get_ratio_interpretation(ratios['delai_recouvrement_clients'], 45, False)
        ])
    
    if activity_data:
        df = pd.DataFrame(activity_data, columns=["Ratio", "Valeur", "Norme", "Interprétation"])
        st.dataframe(df, hide_index=True, use_container_width=True)

def display_interactive_charts(data: Dict[str, Any], ratios: Dict[str, Any], scores: Dict[str, Any]):
    """Affiche les graphiques interactifs"""
    
    st.header("📉 Graphiques Interactifs")
    
    # Graphiques en colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        # Radar des performances
        create_performance_radar(scores)
    
    with col2:
        # Graphique en barres des ratios clés
        create_key_ratios_chart(ratios)
    
    # Graphiques supplémentaires
    col1, col2 = st.columns(2)
    
    with col1:
        # Structure du bilan
        create_balance_structure_chart(data)
    
    with col2:
        # Évolution des soldes intermédiaires
        create_income_evolution_chart(data)

def create_performance_radar(scores: Dict[str, Any]):
    """Crée le radar de performance"""
    
    st.subheader("🎯 Radar de Performance")
    
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
        name='Performance actuelle',
        line_color='rgb(46, 125, 50)',
        fillcolor='rgba(76, 175, 80, 0.3)'
    ))
    
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
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_key_ratios_chart(ratios: Dict[str, Any]):
    """Crée le graphique des ratios clés"""
    
    st.subheader("📊 Ratios Clés vs Normes")
    
    # Sélectionner les ratios clés avec leurs normes
    key_ratios = [
        ('Liquidité Générale', ratios.get('ratio_liquidite_generale', 0), 1.5),
        ('Autonomie Financière (%)', ratios.get('ratio_autonomie_financiere', 0), 30),
        ('ROE (%)', ratios.get('roe', 0), 10),
        ('Marge Nette (%)', ratios.get('marge_nette', 0), 5)
    ]
    
    ratios_names = [r[0] for r in key_ratios]
    entreprise_values = [r[1] for r in key_ratios]
    norme_values = [r[2] for r in key_ratios]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Votre Entreprise',
        x=ratios_names,
        y=entreprise_values,
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name='Norme BCEAO',
        x=ratios_names,
        y=norme_values,
        marker_color='red',
        opacity=0.7
    ))
    
    fig.update_layout(
        barmode='group',
        title='Comparaison avec les Normes BCEAO',
        height=400,
        yaxis_title='Valeur'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_balance_structure_chart(data: Dict[str, Any]):
    """Crée le graphique de structure du bilan"""
    
    st.subheader("🏗️ Structure du Bilan")
    
    # Structure de l'actif
    actif_labels = ['Immobilisations', 'Actif Circulant', 'Trésorerie']
    actif_values = [
        data.get('immobilisations_nettes', 0),
        data.get('total_actif_circulant', 0),
        data.get('tresorerie', 0)
    ]
    
    # Enlever les valeurs nulles
    actif_data = [(label, value) for label, value in zip(actif_labels, actif_values) if value > 0]
    
    if actif_data:
        labels, values = zip(*actif_data)
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3,
            marker_colors=['#ff9999', '#66b3ff', '#99ff99']
        )])
        
        fig.update_layout(
            title="Répartition de l'Actif",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Données insuffisantes pour créer le graphique")

def create_income_evolution_chart(data: Dict[str, Any]):
    """Crée le graphique d'évolution des soldes intermédiaires"""
    
    st.subheader("📈 Soldes Intermédiaires de Gestion")
    
    if data.get('chiffre_affaires', 0) == 0:
        st.info("Données insuffisantes pour créer le graphique")
        return
    
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
        marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    ))
    
    fig.update_layout(
        title="Évolution des Soldes Intermédiaires de Gestion",
        xaxis_title="Indicateurs",
        yaxis_title="Montant (FCFA)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_recommendations(data: Dict[str, Any], ratios: Dict[str, Any], scores: Dict[str, Any]):
    """Affiche les recommandations"""
    
    st.header("🎯 Recommandations Stratégiques")
    
    recommendations = generate_recommendations(data, ratios, scores)
    
    if not recommendations:
        st.success("✅ Aucune recommandation urgente. Situation financière satisfaisante.")
        return
    
    # Organiser par priorité
    urgent = [r for r in recommendations if "🔴" in r.get('Priorité', '')]
    important = [r for r in recommendations if "🟠" in r.get('Priorité', '')]
    moyen_terme = [r for r in recommendations if "🟡" in r.get('Priorité', '')]
    
    if urgent:
        st.subheader("🔴 Actions Urgentes (0-1 mois)")
        for rec in urgent:
            display_recommendation_card(rec)
    
    if important:
        st.subheader("🟠 Actions Importantes (1-3 mois)")
        for rec in important:
            display_recommendation_card(rec)
    
    if moyen_terme:
        st.subheader("🟡 Actions Moyen Terme (3-6 mois)")
        for rec in moyen_terme:
            display_recommendation_card(rec)

def display_recommendation_card(rec: Dict[str, Any]):
    """Affiche une carte de recommandation"""
    
    with st.expander(f"{rec.get('Priorité', '')} {rec.get('Catégorie', '')} - {rec.get('Problème', '')}"):
        st.markdown(f"**Impact:** {rec.get('Impact', '')}")
        
        if 'Recommandations' in rec:
            st.markdown("**Recommandations:**")
            for recommandation in rec['Recommandations']:
                st.write(f"• {recommandation}")
        
        if 'Indicateurs de suivi' in rec:
            st.markdown("**Indicateurs de suivi:**")
            for indicateur in rec['Indicateurs de suivi']:
                st.write(f"📊 {indicateur}")

def generate_recommendations(data: Dict[str, Any], ratios: Dict[str, Any], scores: Dict[str, Any]) -> list:
    """Génère des recommandations basées sur l'analyse"""
    
    recommendations = []
    
    # Recommandations de liquidité
    if scores.get('liquidite', 0) < 25:
        if ratios.get('ratio_liquidite_generale', 0) < 1.2:
            recommendations.append({
                "Priorité": "🔴 URGENT",
                "Catégorie": "💧 Liquidité",
                "Problème": f"Ratio de liquidité critique ({ratios.get('ratio_liquidite_generale', 0):.2f})",
                "Impact": "Risque de défaillance à court terme",
                "Recommandations": [
                    "Négocier des délais de paiement avec les fournisseurs",
                    "Accélérer le recouvrement des créances clients",
                    "Réduire les stocks non essentiels",
                    "Négocier une ligne de crédit court terme"
                ],
                "Indicateurs de suivi": [
                    "Ratio de liquidité générale > 1.5",
                    "Délai de recouvrement < 45 jours",
                    "Rotation des stocks > 6"
                ]
            })
    
    # Recommandations de solvabilité
    if scores.get('solvabilite', 0) < 25:
        if ratios.get('ratio_autonomie_financiere', 0) < 25:
            recommendations.append({
                "Priorité": "🟠 IMPORTANT",
                "Catégorie": "🏛️ Solvabilité",
                "Problème": f"Autonomie financière insuffisante ({ratios.get('ratio_autonomie_financiere', 0):.1f}%)",
                "Impact": "Structure financière déséquilibrée",
                "Recommandations": [
                    "Préparer une augmentation de capital",
                    "Renégocier les dettes financières",
                    "Mettre en réserve tous les bénéfices",
                    "Rechercher des subventions"
                ],
                "Indicateurs de suivi": [
                    "Ratio d'autonomie financière > 30%",
                    "Ratio d'endettement < 65%",
                    "Capacité de remboursement < 5 ans"
                ]
            })
    
    # Recommandations de rentabilité
    if scores.get('rentabilite', 0) < 15:
        if ratios.get('marge_nette', 0) < 3:
            recommendations.append({
                "Priorité": "🟡 MOYEN TERME",
                "Catégorie": "📈 Rentabilité",
                "Problème": f"Marge nette insuffisante ({ratios.get('marge_nette', 0):.1f}%)",
                "Impact": "Capacité d'autofinancement limitée",
                "Recommandations": [
                    "Analyser la structure des coûts",
                    "Optimiser les marges commerciales",
                    "Réduire les charges fixes",
                    "Améliorer la productivité"
                ],
                "Indicateurs de suivi": [
                    "Marge nette > 5%",
                    "ROE > 10%",
                    "Coefficient d'exploitation < 65%"
                ]
            })
    
    return recommendations

# Fonctions utilitaires

def get_performance_color(percentage: float) -> str:
    """Retourne une couleur basée sur le pourcentage de performance"""
    if percentage >= 80:
        return "green"
    elif percentage >= 60:
        return "orange"
    elif percentage >= 40:
        return "yellow"
    else:
        return "red"

def get_ratio_status(value: float, threshold: float, higher_is_better: bool = True) -> str:
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

def get_ratio_interpretation(value: float, threshold: float, higher_is_better: bool = True) -> str:
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

def identify_strengths(scores: Dict[str, Any], ratios: Dict[str, Any]) -> list:
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
    
    return strengths

def identify_weaknesses(scores: Dict[str, Any], ratios: Dict[str, Any]) -> list:
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
    
    return weaknesses