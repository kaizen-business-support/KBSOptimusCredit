"""
Composant Sidebar avec normes BCEAO et informations de référence
"""

import streamlit as st
import json
from pathlib import Path

def show_bceao_sidebar():
    """Affiche la sidebar avec les normes BCEAO"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Normes BCEAO")
    
    # Informations générales
    with st.sidebar.expander("ℹ️ Informations Générales", expanded=False):
        st.markdown("""
        **Banque Centrale des États de l'Afrique de l'Ouest**
        
        - **8 pays membres** : Bénin, Burkina Faso, Côte d'Ivoire, Guinée-Bissau, Mali, Niger, Sénégal, Togo
        - **Monnaie** : Franc CFA (XOF)
        - **Siège** : Dakar, Sénégal
        - **Supervision** : Prudentielle et financière
        """)
    
    # Ratios de solvabilité
    with st.sidebar.expander("🏛️ Ratios de Solvabilité"):
        st.markdown("""
        **Fonds propres de base (CET1)**
        - Minimum : 5,0%
        - Objectif : 7,0%
        
        **Fonds propres Tier 1**
        - Minimum : 6,625%
        - Objectif : 8,5%
        
        **Solvabilité globale**
        - Minimum : 8,625%
        - Objectif : 11,5%
        
        **Coussin de conservation**
        - Obligatoire : 2,5%
        """)
    
    # Ratios de liquidité
    with st.sidebar.expander("💧 Ratios de Liquidité"):
        st.markdown("""
        **Liquidité court terme**
        - Minimum : 75%
        
        **Couverture emplois MLT**
        - Minimum : 100%
        
        **Ratio de transformation**
        - Maximum : 100%
        
        *Contrôles mensuels via FODEP*
        """)
    
    # Division des risques
    with st.sidebar.expander("⚖️ Division des Risques"):
        st.markdown("""
        **Division des risques**
        - Maximum : 65% des FP
        
        **Grands risques**
        - Maximum : 8 fois les FP
        
        **Engagements apparentés**
        - Maximum : 20%
        
        *Limitation concentration débiteurs*
        """)
    
    # Qualité du portefeuille
    with st.sidebar.expander("📈 Qualité Portefeuille"):
        st.markdown("""
        **Créances douteuses**
        - Surveillance continue
        
        **Taux de provisionnement**
        - Variable selon garanties
        
        **Créances > 5 ans**
        - Passage en perte obligatoire
        
        *Classification des risques*
        """)
    
    # Capital minimum
    with st.sidebar.expander("💰 Capital Minimum"):
        st.markdown("""
        **Capital social minimum**
        - 20 milliards FCFA (2023)
        - Mise en conformité progressive
        
        **Refinancement BCEAO**
        - ≥ 60% crédits éligibles
        
        **Pondération des risques**
        - États UEMOA : 0%
        - Banques UEMOA : 20%
        - Entreprises : 20-150%
        """)
    
    # Méthode de scoring
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎯 Méthode de Scoring")
    
    with st.sidebar.expander("📊 Barème de Notation"):
        st.markdown("""
        **Score Global sur 100 points**
        
        - **Liquidité** : 40 points
        - **Solvabilité** : 40 points  
        - **Rentabilité** : 30 points
        - **Activité** : 15 points
        - **Gestion** : 15 points
        
        **Interprétation**
        - 85-100 : Excellente
        - 70-84 : Très bonne
        - 55-69 : Bonne
        - 40-54 : Acceptable
        - 25-39 : Faible
        - 0-24 : Critique
        """)
    
    # Secteurs de référence
    st.sidebar.markdown("---")
    st.sidebar.subheader("🏭 Secteurs Référence")
    
    with st.sidebar.expander("📋 Secteurs Disponibles"):
        secteurs = [
            ("🏭", "Industrie Manufacturière"),
            ("🛒", "Commerce de Détail"),
            ("💼", "Services Professionnels"),
            ("🏗️", "Construction BTP"),
            ("🌾", "Agriculture"),
            ("📦", "Commerce de Gros")
        ]
        
        for icon, nom in secteurs:
            st.markdown(f"{icon} {nom}")
    
    # Contact et support
    st.sidebar.markdown("---")
    st.sidebar.subheader("📞 Support")
    
    with st.sidebar.expander("💬 Aide et Contact"):
        st.markdown("""
        **Support Technique**
        - 📧 contact@kaizen-corporation.com
        - ☎️ +221 75 645 45 00
        
        **Documentation**
        - Guide utilisateur
        - Modèles Excel
        - Exemples d'analyse
        
        **Formation**
        - Sessions en ligne
        - Webinaires mensuels
        - Support personnalisé
        """)

def show_ratios_reference():
    """Affiche la référence des ratios dans la sidebar"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📐 Référence Ratios")
    
    ratios_reference = {
        "Liquidité": {
            "Liquidité générale": "> 1,5",
            "Liquidité immédiate": "> 1,0", 
            "BFR en jours": "< 60 jours",
            "Trésorerie nette": "> 0"
        },
        "Solvabilité": {
            "Autonomie financière": "> 30%",
            "Endettement global": "< 65%",
            "Capacité remboursement": "< 5 ans",
            "Financement immob.": "> 100%"
        },
        "Rentabilité": {
            "ROE": "> 10%",
            "ROA": "> 2%",
            "Marge nette": "> 5%",
            "Marge exploitation": "> 5%"
        },
        "Activité": {
            "Rotation actif": "> 1,5",
            "Rotation stocks": "> 6",
            "Délai recouvrement": "< 45 jours",
            "Rotation créances": "> 8"
        },
        "Gestion": {
            "Productivité personnel": "> 2,0",
            "Charges personnel/VA": "< 50%",
            "CAFG/CA": "> 7%",
            "Coefficient exploit.": "< 65%"
        }
    }
    
    for categorie, ratios in ratios_reference.items():
        with st.sidebar.expander(f"📊 {categorie}"):
            for ratio, norme in ratios.items():
                st.markdown(f"**{ratio}** : {norme}")

def show_sectoral_benchmarks(secteur: str = None):
    """Affiche les benchmarks sectoriels"""
    
    if not secteur:
        return
    
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"🎯 Benchmarks {secteur.title()}")
    
    # Charger les données sectorielles
    sectoral_data = load_sectoral_data()
    
    if secteur in sectoral_data:
        data = sectoral_data[secteur]
        
        with st.sidebar.expander("📈 Ratios Sectoriels"):
            for ratio_name, values in data.items():
                if isinstance(values, dict) and 'median' in values:
                    st.markdown(f"""
                    **{ratio_name.replace('_', ' ').title()}**
                    - Q1: {values['q1']:.2f}
                    - Médiane: {values['median']:.2f}
                    - Q3: {values['q3']:.2f}
                    """)

def load_sectoral_data():
    """Charge les données sectorielles"""
    try:
        data_path = Path(__file__).parent.parent.parent / "data" / "sectoral_norms.json"
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def show_calculation_methods():
    """Affiche les méthodes de calcul"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧮 Méthodes de Calcul")
    
    with st.sidebar.expander("📐 Formules Principales"):
        st.markdown("""
        **Liquidité Générale**
        ```
        (Actif Circulant + Trésorerie) / 
        Dettes Court Terme
        ```
        
        **Autonomie Financière** 
        ```
        Capitaux Propres / Total Actif × 100
        ```
        
        **ROE**
        ```
        Résultat Net / Capitaux Propres × 100
        ```
        
        **BFR**
        ```
        (Stocks + Créances) - 
        (Fournisseurs + Dettes Sociales)
        ```
        
        **Rotation Stocks**
        ```
        Chiffre d'Affaires / Stocks Moyens
        ```
        """)
    
    with st.sidebar.expander("⚡ Calculs Automatiques"):
        st.markdown("""
        L'outil calcule automatiquement :
        
        ✅ **25+ ratios financiers**
        ✅ **Score pondéré sur 100**
        ✅ **Comparaisons sectorielles**
        ✅ **Tendances et évolutions**
        ✅ **Recommandations ciblées**
        ✅ **Plan d'action prioritaire**
        
        *Tous les calculs respectent les normes comptables OHADA et BCEAO*
        """)

def show_interpretation_guide():
    """Guide d'interprétation des résultats"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📖 Guide Interprétation")
    
    with st.sidebar.expander("🎨 Code Couleurs"):
        st.markdown("""
        **Niveaux de Performance**
        
        🟢 **Vert** : Excellent (≥ 85%)
        🔵 **Bleu** : Très bon (70-84%)
        🟡 **Jaune** : Bon (55-69%)
        🟠 **Orange** : Acceptable (40-54%)
        🔴 **Rouge** : Faible (25-39%)
        ⚫ **Noir** : Critique (< 25%)
        """)
    
    with st.sidebar.expander("🚨 Signaux d'Alerte"):
        st.markdown("""
        **Attention Immédiate**
        - Liquidité < 1,2
        - Autonomie < 20%
        - Marge nette < 2%
        - BFR > 90 jours CA
        
        **Surveillance Renforcée**
        - ROE < 5%
        - Endettement > 80%
        - Rotation stocks < 4
        - Charges personnel > 60% VA
        """)

def show_export_options():
    """Options d'export et sauvegarde"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("💾 Export & Sauvegarde")
    
    with st.sidebar.expander("📄 Formats Disponibles"):
        st.markdown("""
        **Rapports Complets**
        - 📊 PDF exécutif (2 pages)
        - 📋 Excel détaillé (5 feuilles)
        - 🗂️ JSON données brutes
        - 📝 TXT synthèse
        
        **Graphiques**
        - 📈 PNG haute résolution
        - 🎯 SVG vectoriels
        - 📊 Graphiques interactifs
        
        **Données**
        - 💽 CSV ratios complets
        - 📊 Excel template vierge
        """)
    
    with st.sidebar.expander("🔄 Historique & Suivi"):
        st.markdown("""
        **Fonctionnalités Avancées**
        
        ⏱️ **Analyses Périodiques**
        - Mensuelle, trimestrielle
        - Comparaisons temporelles
        - Tendances automatiques
        
        📊 **Tableaux de Bord**
        - KPI personnalisés
        - Alertes automatiques
        - Reporting automatisé
        """)

def show_version_info():
    """Informations de version et changelog"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Version Info")
    
    with st.sidebar.expander("🔖 Version Actuelle"):
        st.markdown("""
        **Version 1.0.0** - Juillet 2025
        
        🆕 **Nouveautés**
        - Modularité complète
        - 25+ ratios calculés
        - Comparaisons sectorielles
        - Recommandations IA
        - Export multi-formats
        
        🔧 **Améliorations**
        - Performance optimisée
        - Interface modernisée
        - Validation renforcée
        - Support multi-devises
        """)
    
    with st.sidebar.expander("📅 Changelog"):
        st.markdown("""
        **v2.0.0** (Déc 2024)
        - Architecture modulaire
        - Ratios BCEAO complets
        - Scoring avancé
        
        **v1.5.0** (Nov 2024)
        - Comparaisons sectorielles
        - Export automatisé
        
        **v1.0.0** (Oct 2024)
        - Version initiale
        - Ratios de base
        """)

def show_help_section():
    """Section d'aide et tutoriels"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("❓ Aide & Tutoriels")
    
    with st.sidebar.expander("🎓 Guide Rapide"):
        st.markdown("""
        **1. Import des Données**
        - Excel BCEAO recommandé
        - Saisie manuelle possible
        - Validation automatique
        
        **2. Analyse Financière**
        - 5 catégories de ratios
        - Score global sur 100
        - Comparaisons sectorielles
        
        **3. Recommandations**
        - Actions prioritaires
        - Plan à 6 mois
        - Indicateurs de suivi
        
        **4. Export Résultats**
        - Rapports exécutifs
        - Données détaillées
        - Graphiques interactifs
        """)
    
    with st.sidebar.expander("🎥 Vidéos Tutoriels"):
        st.markdown("""
        
        👨‍🏫 **Sessions Formation**
        - Webinaires
        - Support personnalisé
        - Q&A
        """)
    
    with st.sidebar.expander("🚫 Problèmes Fréquents"):
        st.markdown("""
        **Excel non reconnu**
        ➡️ Vérifier format .xlsx
        ➡️ Contrôler noms feuilles
        
        **Bilan déséquilibré**
        ➡️ Vérifier totaux
        ➡️ Corriger les erreurs
        
        **Ratios aberrants**
        ➡️ Contrôler données source
        ➡️ Valider cohérence
        
        **Export impossible**
        ➡️ Autoriser téléchargements
        ➡️ Vérifier espace disque
        """)

def show_footer_info():
    """Informations de pied de page"""
    
    st.sidebar.markdown("---")
    
    # Informations légales
    st.sidebar.markdown("""
    <div style='text-align: center; font-size: 0.8em; color: #666;'>
        <p><b>OptimusCredit - Outil d'Analyse Financière</b></p>
        <p>Version 1.0.0 | Juillet 2025</p>
        <p>© 2025 OptimusCredit</p>
        <p>Tous droits réservés</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Liens utiles
    st.sidebar.markdown("""
    **Liens Utiles**
    - 🌐 [Site Kaizen Business Support](https://kaizen-corporation.com)
    - 📚 [Documentation](https://www.kaizen-corporation.com)
    - 📧 [Support](mailto:support@kaizen-corporation.com)
    """)

def show_advanced_settings():
    """Paramètres avancés pour les utilisateurs expérimentés"""
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Paramètres Avancés")
    
    with st.sidebar.expander("🎛️ Configuration"):
        
        # Seuils personnalisés
        st.markdown("**Seuils Personnalisés**")
        
        liquidite_seuil = st.slider(
            "Seuil liquidité générale",
            min_value=1.0, max_value=3.0, value=1.5, step=0.1,
            help="Ajuster selon le secteur d'activité"
        )
        
        autonomie_seuil = st.slider(
            "Seuil autonomie financière (%)",
            min_value=20, max_value=60, value=30, step=5,
            help="Pourcentage minimum recommandé"
        )
        
        # Devise de référence
        devise = st.selectbox(
            "Devise de référence",
            ["FCFA", "EUR", "USD"],
            index=0,
            help="Pour l'affichage des montants"
        )
        
        # Precision des calculs
        precision = st.selectbox(
            "Précision des ratios",
            [1, 2, 3],
            index=1,
            help="Nombre de décimales"
        )
        
        # Mode debug
        debug_mode = st.checkbox(
            "Mode debug",
            help="Afficher les détails de calcul"
        )
        
        # Sauvegarde en session
        if st.button("💾 Sauvegarder Config"):
            st.session_state.custom_config = {
                'liquidite_seuil': liquidite_seuil,
                'autonomie_seuil': autonomie_seuil,
                'devise': devise,
                'precision': precision,
                'debug_mode': debug_mode
            }
            st.success("Configuration sauvegardée!")

def get_user_config():
    """Récupère la configuration utilisateur"""
    default_config = {
        'liquidite_seuil': 1.5,
        'autonomie_seuil': 30,
        'devise': 'FCFA',
        'precision': 2,
        'debug_mode': False
    }
    
    return st.session_state.get('custom_config', default_config)