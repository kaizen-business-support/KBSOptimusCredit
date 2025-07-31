"""
Page de génération de rapports pour OptimusCredit
Version complète avec exports multiples
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Import du gestionnaire de session
try:
    from session_manager import SessionManager
except ImportError:
    st.error("❌ Impossible d'importer session_manager.py")
    st.stop()

def show_reports_page():
    """Affiche la page de génération de rapports"""
    
    # Vérifier si des données d'analyse existent
    if not SessionManager.has_analysis_data():
        st.warning("⚠️ Aucune analyse disponible pour générer des rapports.")
        st.info("👈 Utilisez le menu de navigation pour accéder à la page d'import Excel.")
        
        # Boutons de redirection
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Import Excel", key="reports_goto_import", type="primary"):
                SessionManager.set_current_page('excel_import')
                st.rerun()
        with col2:
            if st.button("✏️ Saisie Manuelle", key="reports_goto_manual", type="secondary"):
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
    
    st.title("📋 Génération de Rapports")
    st.markdown("---")
    
    # Informations sur l'analyse
    display_analysis_overview(data, scores, metadata)
    
    # Types de rapports disponibles
    st.header("📄 Types de Rapports Disponibles")
    
    # Tabs pour organiser les rapports
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Synthèse Exécutive", "📋 Rapport Détaillé", "💾 Export Données", "🔧 Rapports Personnalisés"
    ])
    
    with tab1:
        generate_executive_summary_tab(data, ratios, scores, metadata)
    
    with tab2:
        generate_detailed_report_tab(data, ratios, scores, metadata)
    
    with tab3:
        export_data_tab(analysis_data)
    
    with tab4:
        custom_reports_tab(data, ratios, scores, metadata)

def display_analysis_overview(data, scores, metadata):
    """Affiche un aperçu de l'analyse"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score_global = scores.get('global', 0)
        st.metric("Score Global", f"{score_global}/100")
    
    with col2:
        classe = SessionManager.get_financial_class(score_global)
        st.metric("Classe BCEAO", classe)
    
    with col3:
        secteur = metadata.get('secteur', 'Non spécifié').replace('_', ' ').title()
        st.metric("Secteur", secteur)
    
    with col4:
        date_analyse = metadata.get('date_analyse', 'N/A')
        if date_analyse != 'N/A':
            date_obj = datetime.fromisoformat(date_analyse.replace('Z', '+00:00')) if 'T' in date_analyse else datetime.strptime(date_analyse, '%Y-%m-%d %H:%M:%S')
            st.metric("Date Analyse", date_obj.strftime('%d/%m/%Y'))
        else:
            st.metric("Date Analyse", "N/A")

def generate_executive_summary_tab(data, ratios, scores, metadata):
    """Onglet de génération de la synthèse exécutive"""
    
    st.subheader("📊 Synthèse Exécutive")
    
    st.markdown("""
    **Contenu de la synthèse exécutive :**
    - Résumé sur 1-2 pages
    - Score global et interprétation
    - Ratios clés vs normes BCEAO
    - Points forts et axes d'amélioration
    - Recommandations prioritaires
    """)
    
    if st.button("📄 Générer la Synthèse Exécutive", key="generate_summary", type="primary", use_container_width=True):
        generate_executive_summary(data, ratios, scores, metadata)

def generate_executive_summary(data, ratios, scores, metadata):
    """Génère et affiche la synthèse exécutive"""
    
    st.markdown("---")
    st.subheader("📊 SYNTHÈSE EXÉCUTIVE")
    
    # En-tête
    score_global = scores.get('global', 0)
    interpretation, color = SessionManager.get_interpretation(score_global)
    classe = SessionManager.get_financial_class(score_global)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        ### Analyse Financière - {metadata.get('secteur', 'Entreprise').replace('_', ' ').title()}
        
        **Date d'analyse :** {metadata.get('date_analyse', datetime.now().strftime('%d/%m/%Y'))}  
        **Source des données :** {metadata.get('source', 'Import').replace('_', ' ').title()}  
        **Secteur d'activité :** {metadata.get('secteur', 'Non spécifié').replace('_', ' ').title()}  
        """)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: {color}20; border: 2px solid {color};">
            <h3 style="color: {color}; margin: 0;">Score BCEAO</h3>
            <h1 style="color: {color}; margin: 10px 0;">{score_global}/100</h1>
            <p style="color: {color}; margin: 0; font-weight: bold;">Classe {classe}</p>
            <p style="color: {color}; margin: 5px 0; font-size: 14px;">{interpretation}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Indicateurs financiers clés
    st.markdown("### 💰 Indicateurs Financiers Clés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ca = data.get('chiffre_affaires', 0)
        st.metric("Chiffre d'Affaires", f"{ca:,.0f}".replace(',', ' ') + " FCFA")
    
    with col2:
        rn = data.get('resultat_net', 0)
        st.metric("Résultat Net", f"{rn:,.0f}".replace(',', ' ') + " FCFA")
    
    with col3:
        ta = data.get('total_actif', 0)
        st.metric("Total Actif", f"{ta:,.0f}".replace(',', ' ') + " FCFA")
    
    with col4:
        cp = data.get('capitaux_propres', 0)
        st.metric("Capitaux Propres", f"{cp:,.0f}".replace(',', ' ') + " FCFA")
    
    # Performance par catégorie
    st.markdown("### 📊 Performance par Catégorie")
    
    categories_data = [
        ("💧 Liquidité", scores.get('liquidite', 0), 40),
        ("🏛️ Solvabilité", scores.get('solvabilite', 0), 40),
        ("📈 Rentabilité", scores.get('rentabilite', 0), 30),
        ("⚡ Activité", scores.get('activite', 0), 15),
        ("🔧 Gestion", scores.get('gestion', 0), 15)
    ]
    
    summary_data = []
    for label, score, max_score in categories_data:
        percentage = (score / max_score) * 100
        status = "✅ Bon" if percentage >= 70 else "⚠️ À améliorer" if percentage >= 40 else "❌ Critique"
        summary_data.append([label, f"{score}/{max_score}", f"{percentage:.0f}%", status])
    
    df_summary = pd.DataFrame(summary_data, columns=["Catégorie", "Score", "Performance", "Évaluation"])
    st.dataframe(df_summary, hide_index=True, use_container_width=True)
    
    # Ratios clés vs normes
    st.markdown("### 🔑 Ratios Clés vs Normes BCEAO")
    
    key_ratios_data = []
    key_ratios = [
        ("Liquidité Générale", "ratio_liquidite_generale", "> 1.5"),
        ("Autonomie Financière", "ratio_autonomie_financiere", "> 30%"),
        ("ROE", "roe", "> 10%"),
        ("Marge Nette", "marge_nette", "> 5%")
    ]
    
    for label, key, norm in key_ratios:
        if key in ratios:
            value = ratios[key]
            if '%' in norm:
                formatted_value = f"{value:.1f}%"
                threshold = float(norm.replace('>', '').replace('%', '').strip())
                status = "✅" if value >= threshold else "❌"
                ecart = f"{value - threshold:+.1f}%"
            else:
                formatted_value = f"{value:.2f}"
                threshold = float(norm.replace('>', '').strip())
                status = "✅" if value >= threshold else "❌"
                ecart = f"{value - threshold:+.2f}"
            
            key_ratios_data.append([label, formatted_value, norm, status, ecart])
    
    if key_ratios_data:
        df_ratios = pd.DataFrame(key_ratios_data, columns=["Ratio", "Valeur", "Norme", "Statut", "Écart"])
        st.dataframe(df_ratios, hide_index=True, use_container_width=True)
    
    # Points forts et faibles
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Points Forts")
        strengths = identify_strengths(scores, ratios)
        if strengths:
            for strength in strengths[:5]:
                st.success(f"• {strength}")
        else:
            st.info("• Analyse en cours...")
    
    with col2:
        st.markdown("### ⚠️ Axes d'Amélioration")
        weaknesses = identify_weaknesses(scores, ratios)
        if weaknesses:
            for weakness in weaknesses[:5]:
                st.warning(f"• {weakness}")
        else:
            st.success("• Situation globalement satisfaisante")
    
    # Recommandations prioritaires
    st.markdown("### 🎯 Recommandations Prioritaires")
    
    if score_global >= 70:
        st.success("✅ Situation financière satisfaisante. Maintenir les bonnes pratiques et surveiller l'évolution des ratios clés.")
    elif score_global >= 40:
        st.warning("⚠️ Quelques améliorations sont recommandées. Focus sur les catégories avec les scores les plus faibles.")
    else:
        st.error("❌ Des actions correctives urgentes sont nécessaires. Prioriser la liquidité et la solvabilité.")
    
    # Générer des recommandations spécifiques
    recommendations = []
    if scores.get('liquidite', 0) < 25:
        recommendations.append("• **URGENT** : Améliorer la liquidité (négocier délais fournisseurs, accélérer recouvrement)")
    if scores.get('solvabilite', 0) < 25:
        recommendations.append("• **IMPORTANT** : Renforcer les capitaux propres (augmentation capital, mise en réserves)")
    if scores.get('rentabilite', 0) < 15:
        recommendations.append("• **MOYEN TERME** : Optimiser la rentabilité (revoir prix, réduire coûts)")
    
    if recommendations:
        for rec in recommendations:
            st.write(rec)
    else:
        st.info("• Continuer à surveiller les ratios clés et maintenir les bonnes pratiques")
    
    # Footer de la synthèse
    st.markdown("---")
    st.caption(f"Synthèse générée le {datetime.now().strftime('%d/%m/%Y à %H:%M')} par OptimusCredit • Conforme aux normes BCEAO 2024")

def generate_detailed_report_tab(data, ratios, scores, metadata):
    """Onglet de génération du rapport détaillé"""
    
    st.subheader("📋 Rapport Détaillé")
    
    st.markdown("""
    **Contenu du rapport détaillé :**
    - Analyse complète sur 10-15 pages
    - États financiers détaillés
    - Tous les ratios calculés (25+)
    - Graphiques et tableaux
    - Comparaison sectorielle
    - Plan d'action détaillé sur 6 mois
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Générer Rapport Complet", key="generate_detailed", type="primary", use_container_width=True):
            generate_detailed_report(data, ratios, scores, metadata)
    
    with col2:
        if st.button("📋 Aperçu du Rapport", key="preview_detailed", use_container_width=True):
            show_detailed_report_preview()

def generate_detailed_report(data, ratios, scores, metadata):
    """Génère le rapport détaillé"""
    
    st.markdown("---")
    st.subheader("📋 RAPPORT D'ANALYSE FINANCIÈRE DÉTAILLÉ")
    
    # En-tête du rapport
    score_global = scores.get('global', 0)
    interpretation, color = SessionManager.get_interpretation(score_global)
    
    st.markdown(f"""
    ### OptimusCredit - Analyse Financière BCEAO
    
    **Entreprise analysée :** {metadata.get('fichier_nom', 'Entreprise')}  
    **Secteur d'activité :** {metadata.get('secteur', 'Non spécifié').replace('_', ' ').title()}  
    **Date d'analyse :** {metadata.get('date_analyse', datetime.now().strftime('%d/%m/%Y'))}  
    **Score global :** {score_global}/100 - {interpretation}  
    **Classe BCEAO :** {SessionManager.get_financial_class(score_global)}
    
    ---
    """)
    
    # Table des matières
    st.markdown("""
    ### 📋 Table des Matières
    
    1. **Résumé Exécutif**
    2. **Analyse du Bilan**
    3. **Analyse du Compte de Résultat**  
    4. **Analyse des Ratios par Catégorie**
    5. **Comparaison avec les Normes BCEAO**
    6. **Recommandations et Plan d'Action**
    7. **Annexes**
    
    ---
    """)
    
    # 1. Résumé Exécutif
    st.markdown("### 1. 📊 Résumé Exécutif")
    
    if score_global >= 70:
        st.success(f"L'entreprise présente une situation financière {interpretation.lower()} avec un score BCEAO de {score_global}/100.")
    elif score_global >= 40:
        st.warning(f"L'entreprise affiche une situation financière {interpretation.lower()} nécessitant une attention particulière sur certains aspects.")
    else:
        st.error(f"L'entreprise se trouve dans une situation financière {interpretation.lower()} nécessitant des actions correctives urgentes.")
    
    # 2. Analyse du Bilan
    st.markdown("### 2. 📊 Analyse du Bilan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Structure de l'Actif")
        total_actif = data.get('total_actif', 1)
        actif_structure = [
            ["Immobilisations", data.get('immobilisations_nettes', 0), f"{data.get('immobilisations_nettes', 0)/total_actif*100:.1f}%"],
            ["Actif circulant", data.get('stocks', 0) + data.get('creances_clients', 0) + data.get('autres_creances', 0), f"{(data.get('stocks', 0) + data.get('creances_clients', 0) + data.get('autres_creances', 0))/total_actif*100:.1f}%"],
            ["Trésorerie", data.get('tresorerie', 0), f"{data.get('tresorerie', 0)/total_actif*100:.1f}%"]
        ]
        df_actif = pd.DataFrame(actif_structure, columns=["Composante", "Montant (FCFA)", "% Total"])
        df_actif['Montant (FCFA)'] = df_actif['Montant (FCFA)'].apply(lambda x: f"{x:,.0f}".replace(',', ' '))
        st.dataframe(df_actif, hide_index=True, use_container_width=True)
    
    with col2:
        st.markdown("#### Structure du Passif")
        passif_structure = [
            ["Capitaux propres", data.get('capitaux_propres', 0), f"{data.get('capitaux_propres', 0)/total_actif*100:.1f}%"],
            ["Dettes financières", data.get('dettes_financieres', 0), f"{data.get('dettes_financieres', 0)/total_actif*100:.1f}%"],
            ["Dettes court terme", data.get('dettes_court_terme', 0), f"{data.get('dettes_court_terme', 0)/total_actif*100:.1f}%"],
            ["Trésorerie passif", data.get('tresorerie_passif', 0), f"{data.get('tresorerie_passif', 0)/total_actif*100:.1f}%"]
        ]
        df_passif = pd.DataFrame(passif_structure, columns=["Composante", "Montant (FCFA)", "% Total"])
        df_passif['Montant (FCFA)'] = df_passif['Montant (FCFA)'].apply(lambda x: f"{x:,.0f}".replace(',', ' '))
        st.dataframe(df_passif, hide_index=True, use_container_width=True)
    
    # 3. Analyse du Compte de Résultat
    st.markdown("### 3. 📈 Analyse du Compte de Résultat")
    
    ca = data.get('chiffre_affaires', 1)
    sig_data = [
        ["Chiffre d'Affaires", ca, "100.0%"],
        ["Valeur Ajoutée", data.get('valeur_ajoutee', 0), f"{data.get('valeur_ajoutee', 0)/ca*100:.1f}%"],
        ["Excédent Brut d'Exploitation", data.get('excedent_brut', 0), f"{data.get('excedent_brut', 0)/ca*100:.1f}%"],
        ["Résultat d'Exploitation", data.get('resultat_exploitation', 0), f"{data.get('resultat_exploitation', 0)/ca*100:.1f}%"],
        ["Résultat Net", data.get('resultat_net', 0), f"{data.get('resultat_net', 0)/ca*100:.1f}%"]
    ]
    
    df_sig = pd.DataFrame(sig_data, columns=["Solde Intermédiaire", "Montant (FCFA)", "% CA"])
    df_sig['Montant (FCFA)'] = df_sig['Montant (FCFA)'].apply(lambda x: f"{x:,.0f}".replace(',', ' '))
    st.dataframe(df_sig, hide_index=True, use_container_width=True)
    
    # 4. Scores détaillés
    st.markdown("### 4. 🎯 Scores Détaillés par Catégorie")
    
    detailed_scores = [
        ["💧 Liquidité", scores.get('liquidite', 0), 40, f"{scores.get('liquidite', 0)/40*100:.0f}%"],
        ["🏛️ Solvabilité", scores.get('solvabilite', 0), 40, f"{scores.get('solvabilite', 0)/40*100:.0f}%"],
        ["📈 Rentabilité", scores.get('rentabilite', 0), 30, f"{scores.get('rentabilite', 0)/30*100:.0f}%"],
        ["⚡ Activité", scores.get('activite', 0), 15, f"{scores.get('activite', 0)/15*100:.0f}%"],
        ["🔧 Gestion", scores.get('gestion', 0), 15, f"{scores.get('gestion', 0)/15*100:.0f}%"]
    ]
    
    df_scores = pd.DataFrame(detailed_scores, columns=["Catégorie", "Score Obtenu", "Score Maximum", "Performance"])
    st.dataframe(df_scores, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    st.caption(f"Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} par OptimusCredit • Version 2.1 • Conforme BCEAO 2024")

def show_detailed_report_preview():
    """Affiche un aperçu du rapport détaillé"""
    
    with st.expander("👁️ Aperçu du Rapport Détaillé", expanded=True):
        st.markdown("""
        ### 📋 Structure du Rapport Détaillé
        
        **Section 1 : Résumé Exécutif (2 pages)**
        - Score global et interprétation
        - Indicateurs financiers clés
        - Points forts et axes d'amélioration
        - Recommandations prioritaires
        
        **Section 2 : Analyse Bilancielle (3 pages)**
        - Structure détaillée de l'actif
        - Structure détaillée du passif
        - Équilibre financier et fonds de roulement
        - Évolution des masses biliancielles
        
        **Section 3 : Analyse de la Performance (3 pages)**
        - Formation du résultat (SIG)
        - Analyse des marges
        - Rentabilité et profitabilité
        - Capacité d'autofinancement
        
        **Section 4 : Analyse par Ratios (4 pages)**
        - Ratios de liquidité (7 ratios)
        - Ratios de solvabilité (6 ratios)
        - Ratios de rentabilité (5 ratios)
        - Ratios d'activité (4 ratios)
        - Ratios de gestion (3 ratios)
        
        **Section 5 : Comparaison Sectorielle (2 pages)**
        - Positionnement vs médiane sectorielle
        - Analyse par quartiles
        - Benchmarking des ratios clés
        
        **Section 6 : Recommandations et Plan d'Action (3 pages)**
        - Actions urgentes (0-1 mois)
        - Actions importantes (1-3 mois)
        - Actions moyen terme (3-6 mois)
        - Indicateurs de suivi
        - Calendrier de mise en œuvre
        
        **Annexes (2 pages)**
        - Méthodologie de calcul
        - Définitions des ratios
        - Normes BCEAO de référence
        """)

def export_data_tab(analysis_data):
    """Onglet d'export des données"""
    
    st.subheader("💾 Export des Données")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 Données JSON")
        st.markdown("Export complet de toutes les données d'analyse")
        
        if st.button("📥 Télécharger JSON", key="download_json", use_container_width=True):
            download_json_data(analysis_data)
    
    with col2:
        st.markdown("#### 📈 Ratios Excel")
        st.markdown("Tableau Excel avec tous les ratios calculés")
        
        if st.button("📥 Télécharger Excel", key="download_excel", use_container_width=True):
            download_excel_data(analysis_data)
    
    with col3:
        st.markdown("#### 📋 Ratios CSV")
        st.markdown("Fichier CSV simple avec les ratios")
        
        if st.button("📥 Télécharger CSV", key="download_csv", use_container_width=True):
            download_csv_data(analysis_data)

def download_json_data(analysis_data):
    """Permet le téléchargement des données en format JSON"""
    
    # Préparer les données pour l'export
    export_data = {
        **analysis_data,
        'export_info': {
            'date_export': datetime.now().isoformat(),
            'version': '2.1.0',
            'format': 'json',
            'source': 'OptimusCredit'
        }
    }
    
    json_string = json.dumps(export_data, indent=2, ensure_ascii=False, default=str)
    
    st.download_button(
        label="📥 Télécharger les données JSON",
        data=json_string,
        file_name=f"analyse_financiere_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        help="Télécharge toutes les données d'analyse au format JSON"
    )

def download_excel_data(analysis_data):
    """Permet le téléchargement des données en format Excel"""
    
    # Créer un DataFrame avec les ratios et scores
    data = analysis_data['data']
    ratios = analysis_data['ratios']
    scores = analysis_data['scores']
    metadata = analysis_data['metadata']
    
    # Préparer les données pour Excel
    excel_data = []
    
    # Section données financières
    excel_data.append(["=== DONNÉES FINANCIÈRES ===", "", "", ""])
    excel_data.append(["Chiffre d'Affaires", data.get('chiffre_affaires', 0), "FCFA", ""])
    excel_data.append(["Total Actif", data.get('total_actif', 0), "FCFA", ""])
    excel_data.append(["Capitaux Propres", data.get('capitaux_propres', 0), "FCFA", ""])
    excel_data.append(["Résultat Net", data.get('resultat_net', 0), "FCFA", ""])
    excel_data.append(["", "", "", ""])
    
    # Section ratios
    excel_data.append(["=== RATIOS FINANCIERS ===", "", "", ""])
    for ratio_name, ratio_value in ratios.items():
        ratio_label = ratio_name.replace('_', ' ').title()
        if isinstance(ratio_value, (int, float)):
            excel_data.append([ratio_label, f"{ratio_value:.4f}", "", ""])
        else:
            excel_data.append([ratio_label, str(ratio_value), "", ""])
    
    excel_data.append(["", "", "", ""])
    
    # Section scores
    excel_data.append(["=== SCORES BCEAO ===", "", "", ""])
    for score_name, score_value in scores.items():
        score_label = f"Score {score_name.replace('_', ' ').title()}"
        excel_data.append([score_label, score_value, "points", ""])
    
    # Créer le DataFrame
    df_excel = pd.DataFrame(excel_data, columns=["Indicateur", "Valeur", "Unité", "Commentaire"])
    
    # Conversion en CSV (Excel sera supporté dans une version future)
    csv_string = df_excel.to_csv(index=False, encoding='utf-8', sep=';')
    
    st.download_button(
        label="📥 Télécharger les données Excel (CSV)",
        data=csv_string,
        file_name=f"analyse_excel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        help="Télécharge les données formatées pour Excel (format CSV)"
    )

def download_csv_data(analysis_data):
    """Permet le téléchargement des ratios en format CSV"""
    
    ratios = analysis_data['ratios']
    scores = analysis_data['scores']
    
    # Créer un DataFrame avec les ratios
    ratios_data = []
    
    for key, value in ratios.items():
        ratio_name = key.replace('_', ' ').title()
        if isinstance(value, (int, float)):
            ratios_data.append([ratio_name, f"{value:.4f}", "ratio"])
        else:
            ratios_data.append([ratio_name, str(value), "ratio"])
    
    # Ajouter les scores
    for key, value in scores.items():
        score_name = f"Score {key.replace('_', ' ').title()}"
        ratios_data.append([score_name, f"{value}", "score"])
    
    df_ratios = pd.DataFrame(ratios_data, columns=["Indicateur", "Valeur", "Type"])
    
    csv_string = df_ratios.to_csv(index=False, encoding='utf-8')
    
    st.download_button(
        label="📥 Télécharger les ratios CSV",
        data=csv_string,
        file_name=f"ratios_financiers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        help="Télécharge tous les ratios calculés au format CSV"
    )

def custom_reports_tab(data, ratios, scores, metadata):
    """Onglet pour les rapports personnalisés"""
    
    st.subheader("🔧 Rapports Personnalisés")
    
    st.markdown("""
    Créez des rapports adaptés à vos besoins spécifiques :
    """)
    
    # Options de personnalisation
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📋 Contenu du Rapport")
        
        include_summary = st.checkbox("Synthèse exécutive", value=True)
        include_balance = st.checkbox("Analyse du bilan", value=True)
        include_income = st.checkbox("Compte de résultat", value=True)
        include_ratios = st.checkbox("Ratios détaillés", value=True)
        include_charts = st.checkbox("Graphiques", value=False)
        include_recommendations = st.checkbox("Recommandations", value=True)
    
    with col2:
        st.markdown("#### 🎯 Public Cible")
        
        target_audience = st.selectbox(
            "Rapport destiné à :",
            [
                "Direction générale",
                "Conseil d'administration", 
                "Banque/Investisseurs",
                "Comptable/Expert-comptable",
                "Usage interne"
            ]
        )
        
        report_length = st.selectbox(
            "Longueur souhaitée :",
            ["Synthèse (2-3 pages)", "Standard (5-8 pages)", "Détaillé (10-15 pages)"]
        )
    
    # Génération du rapport personnalisé
    if st.button("🔧 Générer Rapport Personnalisé", key="generate_custom", type="primary", use_container_width=True):
        generate_custom_report(
            data, ratios, scores, metadata,
            include_summary, include_balance, include_income, 
            include_ratios, include_charts, include_recommendations,
            target_audience, report_length
        )

def generate_custom_report(data, ratios, scores, metadata, 
                         include_summary, include_balance, include_income, 
                         include_ratios, include_charts, include_recommendations,
                         target_audience, report_length):
    """Génère un rapport personnalisé"""
    
    st.markdown("---")
    st.subheader(f"🔧 RAPPORT PERSONNALISÉ - {target_audience.upper()}")
    
    score_global = scores.get('global', 0)
    interpretation, color = SessionManager.get_interpretation(score_global)
    
    # En-tête adapté au public
    if target_audience == "Direction générale":
        st.markdown(f"""
        ### Tableau de Bord Financier - Direction Générale
        
        **Score de Performance :** {score_global}/100 ({interpretation})  
        **Situation :** {"🟢 Favorable" if score_global >= 70 else "🟡 Vigilance" if score_global >= 40 else "🔴 Critique"}  
        **Date :** {datetime.now().strftime('%d/%m/%Y')}
        """)
    
    elif target_audience == "Banque/Investisseurs":
        st.markdown(f"""
        ### Dossier Financier - Établissement de Crédit
        
        **Notation BCEAO :** {score_global}/100 - Classe {SessionManager.get_financial_class(score_global)}  
        **Secteur :** {metadata.get('secteur', 'Non spécifié').replace('_', ' ').title()}  
        **Conformité :** Normes prudentielles BCEAO 2024
        """)
    
    else:
        st.markdown(f"""
        ### Rapport d'Analyse Financière
        
        **Score Global :** {score_global}/100  
        **Public :** {target_audience}  
        **Type :** {report_length}
        """)
    
    # Contenu selon les options sélectionnées
    if include_summary:
        st.markdown("### 📊 Synthèse")
        if score_global >= 70:
            st.success(f"Situation financière {interpretation.lower()}. Indicateurs dans les normes.")
        elif score_global >= 40:
            st.warning(f"Situation {interpretation.lower()}. Surveillance recommandée.")
        else:
            st.error(f"Situation {interpretation.lower()}. Actions correctives nécessaires.")
    
    if include_balance:
        st.markdown("### 📊 Structure Bilancielle")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Actif", f"{data.get('total_actif', 0):,.0f}".replace(',', ' ') + " FCFA")
            st.metric("Immobilisations", f"{data.get('immobilisations_nettes', 0):,.0f}".replace(',', ' ') + " FCFA")
        
        with col2:
            st.metric("Capitaux Propres", f"{data.get('capitaux_propres', 0):,.0f}".replace(',', ' ') + " FCFA")
            autonomie = ratios.get('ratio_autonomie_financiere', 0)
            st.metric("Autonomie Financière", f"{autonomie:.1f}%")
    
    if include_income:
        st.markdown("### 📈 Résultats")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Chiffre d'Affaires", f"{data.get('chiffre_affaires', 0):,.0f}".replace(',', ' ') + " FCFA")
        with col2:
            st.metric("Résultat Net", f"{data.get('resultat_net', 0):,.0f}".replace(',', ' ') + " FCFA")
        with col3:
            marge = ratios.get('marge_nette', 0)
            st.metric("Marge Nette", f"{marge:.1f}%")
    
    if include_ratios:
        st.markdown("### 📈 Ratios Clés")
        
        key_ratios_custom = [
            ("Liquidité Générale", ratios.get('ratio_liquidite_generale', 0), "> 1.5"),
            ("ROE", ratios.get('roe', 0), "> 10%"),
            ("Autonomie Financière", ratios.get('ratio_autonomie_financiere', 0), "> 30%")
        ]
        
        for label, value, norm in key_ratios_custom:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{label}**")
            with col2:
                if '%' in norm:
                    st.write(f"{value:.1f}%")
                else:
                    st.write(f"{value:.2f}")
            with col3:
                st.write(norm)
    
    if include_recommendations and target_audience != "Banque/Investisseurs":
        st.markdown("### 🎯 Recommandations")
        
        if score_global < 40:
            st.error("**Actions urgentes requises :**")
            st.write("• Améliorer la liquidité immédiatement")
            st.write("• Renforcer la structure financière")
        elif score_global < 70:
            st.warning("**Points d'attention :**")
            st.write("• Surveiller l'évolution des ratios clés")
            st.write("• Optimiser la rentabilité")
        else:
            st.success("**Maintenir les bonnes pratiques :**")
            st.write("• Continuer le suivi des indicateurs")
            st.write("• Préserver l'équilibre financier")
    
    st.markdown("---")
    st.caption(f"Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} • OptimusCredit v2.1 • {target_audience}")

# Fonctions utilitaires (réutilisées depuis analysis.py)

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
    
    return weaknesses