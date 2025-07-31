"""
Page de génération de rapports pour OptimusCredit
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json

try:
    from session_manager import SessionManager
except ImportError:
    st.error("❌ Impossible d'importer session_manager")
    st.stop()

def show_rapports_page():
    """Affiche la page de génération de rapports"""
    
    st.title("📋 Génération de Rapports")
    st.markdown("---")
    
    # Vérifier si des données d'analyse sont disponibles
    if not SessionManager.has_analysis_data():
        st.warning("⚠️ Aucune analyse disponible. Veuillez d'abord importer et analyser un fichier Excel.")
        
        if st.button("📤 Aller à l'Import Excel"):
            SessionManager.set_current_page("excel_import")
            st.rerun()
        
        return
    
    # Récupérer les données d'analyse
    analysis_data = SessionManager.get_analysis_data()
    data = analysis_data['data']
    ratios = analysis_data['ratios']
    scores = analysis_data['scores']
    metadata = analysis_data['metadata']
    
    st.success(f"✅ Analyse disponible - Score: {scores.get('global', 0)}/100")
    
    # Types de rapports disponibles
    st.header("📊 Types de Rapports Disponibles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📄 Synthèse Exécutive")
        st.write("Résumé en 1-2 pages avec les points clés")
        if st.button("📥 Télécharger Synthèse", use_container_width=True):
            generate_executive_summary(data, ratios, scores, metadata)
    
    with col2:
        st.subheader("📑 Rapport Détaillé")
        st.write("Analyse complète avec tous les ratios")
        if st.button("📥 Télécharger Rapport Complet", use_container_width=True):
            generate_detailed_report(data, ratios, scores, metadata)
    
    with col3:
        st.subheader("💾 Données Brutes")
        st.write("Export JSON avec toutes les données")
        if st.button("📥 Télécharger JSON", use_container_width=True):
            generate_json_export(data, ratios, scores, metadata)
    
    # Aperçu des données
    st.markdown("---")
    st.header("👁️ Aperçu des Données")
    
    tab1, tab2, tab3 = st.tabs(["📊 Scores", "📈 Ratios Clés", "💰 Données Financières"])
    
    with tab1:
        show_scores_preview(scores)
    
    with tab2:
        show_ratios_preview(ratios)
    
    with tab3:
        show_financial_preview(data)

def generate_executive_summary(data, ratios, scores, metadata):
    """Génère et télécharge la synthèse exécutive"""
    
    summary = f"""
SYNTHÈSE EXÉCUTIVE - ANALYSE FINANCIÈRE
======================================

Date d'analyse: {metadata.get('date_analyse', datetime.now().strftime('%d/%m/%Y'))}
Secteur: {metadata.get('secteur', 'N/A').replace('_', ' ').title()}
Fichier analysé: {metadata.get('fichier_nom', 'N/A')}

RÉSULTAT GLOBAL
===============
Score BCEAO: {scores.get('global', 0)}/100
Évaluation: {get_interpretation(scores.get('global', 0))}

INDICATEURS CLÉS
================
• Chiffre d'Affaires: {data.get('chiffre_affaires', 0):,.0f} FCFA
• Résultat Net: {data.get('resultat_net', 0):,.0f} FCFA
• Total Actif: {data.get('total_actif', 0):,.0f} FCFA
• Capitaux Propres: {data.get('capitaux_propres', 0):,.0f} FCFA

PERFORMANCE PAR CATÉGORIE
=========================
• Liquidité: {scores.get('liquidite', 0)}/40 ({scores.get('liquidite', 0)/40*100:.0f}%)
• Solvabilité: {scores.get('solvabilite', 0)}/40 ({scores.get('solvabilite', 0)/40*100:.0f}%)
• Rentabilité: {scores.get('rentabilite', 0)}/30 ({scores.get('rentabilite', 0)/30*100:.0f}%)
• Activité: {scores.get('activite', 0)}/15 ({scores.get('activite', 0)/15*100:.0f}%)
• Gestion: {scores.get('gestion', 0)}/15 ({scores.get('gestion', 0)/15*100:.0f}%)

RATIOS FINANCIERS CLÉS
======================
• Liquidité Générale: {ratios.get('ratio_liquidite_generale', 'N/A')}
• Autonomie Financière: {ratios.get('ratio_autonomie_financiere', 'N/A')}%
• ROE: {ratios.get('roe', 'N/A')}%
• Marge Nette: {ratios.get('marge_nette', 'N/A')}%

RECOMMANDATIONS PRIORITAIRES
============================
{get_priority_recommendations(scores, ratios)}

CONCLUSION
==========
{get_conclusion(scores)}

---
Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
OptimusCredit - Développé par Kaizen Corporation
"""
    
    st.download_button(
        label="📄 Télécharger Synthèse Exécutive",
        data=summary,
        file_name=f"synthese_executive_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )

def generate_detailed_report(data, ratios, scores, metadata):
    """Génère et télécharge le rapport détaillé"""
    
    # Version simplifiée pour éviter les erreurs
    report = f"""
RAPPORT D'ANALYSE FINANCIÈRE DÉTAILLÉ
=====================================

Date: {datetime.now().strftime('%d/%m/%Y à %H:%M')}
Secteur: {metadata.get('secteur', 'N/A').replace('_', ' ').title()}

SCORE GLOBAL: {scores.get('global', 0)}/100

DONNÉES FINANCIÈRES COMPLÈTES
=============================
{json.dumps(data, indent=2, ensure_ascii=False)}

RATIOS FINANCIERS COMPLETS
==========================
{json.dumps(ratios, indent=2, ensure_ascii=False)}

SCORES DÉTAILLÉS
================
{json.dumps(scores, indent=2, ensure_ascii=False)}

---
Généré par OptimusCredit - Kaizen Corporation
"""
    
    st.download_button(
        label="📑 Télécharger Rapport Détaillé",
        data=report,
        file_name=f"rapport_detaille_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )

def generate_json_export(data, ratios, scores, metadata):
    """Génère et télécharge l'export JSON"""
    
    export_data = {
        'metadata': metadata,
        'date_export': datetime.now().isoformat(),
        'data': data,
        'ratios': ratios,
        'scores': scores,
        'version': '2.1.0'
    }
    
    json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
    
    st.download_button(
        label="💾 Télécharger Données JSON",
        data=json_data,
        file_name=f"optimuscredit_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
        mime="application/json"
    )

def show_scores_preview(scores):
    """Affiche un aperçu des scores"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Score Global", f"{scores.get('global', 0)}/100")
        st.metric("Liquidité", f"{scores.get('liquidite', 0)}/40")
        st.metric("Solvabilité", f"{scores.get('solvabilite', 0)}/40")
    
    with col2:
        st.metric("Rentabilité", f"{scores.get('rentabilite', 0)}/30")
        st.metric("Activité", f"{scores.get('activite', 0)}/15")
        st.metric("Gestion", f"{scores.get('gestion', 0)}/15")

def show_ratios_preview(ratios):
    """Affiche un aperçu des ratios clés"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Liquidité Générale", f"{ratios.get('ratio_liquidite_generale', 0):.2f}")
        st.metric("Autonomie Financière", f"{ratios.get('ratio_autonomie_financiere', 0):.1f}%")
    
    with col2:
        st.metric("ROE", f"{ratios.get('roe', 0):.1f}%")
        st.metric("Marge Nette", f"{ratios.get('marge_nette', 0):.1f}%")

def show_financial_preview(data):
    """Affiche un aperçu des données financières"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Chiffre d'Affaires", f"{data.get('chiffre_affaires', 0):,.0f} FCFA")
        st.metric("Total Actif", f"{data.get('total_actif', 0):,.0f} FCFA")
    
    with col2:
        st.metric("Résultat Net", f"{data.get('resultat_net', 0):,.0f} FCFA")
        st.metric("Capitaux Propres", f"{data.get('capitaux_propres', 0):,.0f} FCFA")

def get_interpretation(score):
    """Retourne l'interprétation du score"""
    if score >= 85:
        return "Excellence financière"
    elif score >= 70:
        return "Très bonne situation"
    elif score >= 55:
        return "Bonne situation"
    elif score >= 40:
        return "Situation acceptable"
    elif score >= 25:
        return "Situation fragile"
    else:
        return "Situation critique"

def get_priority_recommendations(scores, ratios):
    """Retourne les recommandations prioritaires"""
    recommendations = []
    
    if scores.get('liquidite', 0) < 25:
        recommendations.append("- URGENT: Améliorer la liquidité")
    if scores.get('solvabilite', 0) < 25:
        recommendations.append("- IMPORTANT: Renforcer la solvabilité")
    if scores.get('rentabilite', 0) < 15:
        recommendations.append("- Optimiser la rentabilité")
    
    if not recommendations:
        recommendations.append("- Maintenir les bonnes performances actuelles")
    
    return "\n".join(recommendations)

def get_conclusion(scores):
    """Retourne la conclusion de l'analyse"""
    score_global = scores.get('global', 0)
    
    if score_global >= 70:
        return "L'entreprise présente une situation financière solide avec de bonnes perspectives."
    elif score_global >= 50:
        return "L'entreprise a une situation correcte mais des améliorations sont possibles."
    else:
        return "L'entreprise nécessite des actions correctives pour améliorer sa situation financière."