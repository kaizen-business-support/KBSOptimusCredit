"""
Page d'analyse de fallback - Version simple et robuste
Compatible avec le SessionManager et sans dépendances externes
"""

import streamlit as st
from datetime import datetime

def show_fallback_analysis_page():
    """Affiche une page d'analyse simple et fonctionnelle"""
    
    # Import du gestionnaire de session
    try:
        from session_manager import SessionManager
    except ImportError:
        st.error("❌ SessionManager non disponible")
        return
    
    # Vérifier qu'une analyse existe
    if not SessionManager.has_analysis_data():
        st.error("❌ Aucune analyse disponible")
        st.info("💡 Veuillez d'abord importer des données via la page de saisie.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Saisir des Données", type="primary", use_container_width=True):
                SessionManager.set_current_page('unified_input')
                st.rerun()
        with col2:
            if st.button("🏠 Retour Accueil", type="secondary", use_container_width=True):
                SessionManager.set_current_page('home')
                st.rerun()
        return
    
    # Récupérer les données d'analyse
    analysis_data = SessionManager.get_analysis_data()
    if not analysis_data:
        st.error("❌ Erreur lors de la récupération des données d'analyse")
        return
    
    data = analysis_data.get('data', {})
    ratios = analysis_data.get('ratios', {})
    scores = analysis_data.get('scores', {})
    metadata = analysis_data.get('metadata', {})
    
    # Titre et informations générales
    st.title("📊 Analyse Financière Complète")
    
    # Informations sur l'analyse
    col1, col2, col3 = st.columns(3)
    
    with col1:
        secteur = metadata.get('secteur', 'Non spécifié')
        st.info(f"**🏭 Secteur:** {secteur.replace('_', ' ').title()}")
    
    with col2:
        source = metadata.get('source', 'Non spécifié')
        st.info(f"**📁 Source:** {source}")
    
    with col3:
        date_analyse = metadata.get('date_analyse', 'Non spécifiée')
        st.info(f"**📅 Date:** {date_analyse}")
    
    st.markdown("---")
    
    # Score global avec interprétation
    display_global_score(scores)
    
    st.markdown("---")
    
    # Scores détaillés par catégorie
    display_detailed_scores(scores)
    
    st.markdown("---")
    
    # Données financières principales
    display_financial_data(data)
    
    st.markdown("---")
    
    # Ratios financiers principaux
    display_main_ratios(ratios)
    
    st.markdown("---")
    
    # Interprétation et recommandations
    display_interpretation_and_recommendations(scores, ratios, data)
    
    st.markdown("---")
    
    # Actions disponibles
    display_analysis_actions()

def display_global_score(scores):
    """Affiche le score global avec interprétation"""
    
    st.subheader("🎯 Score Global BCEAO")
    
    score_global = scores.get('global', 0)
    
    # Déterminer la couleur et l'interprétation
    if score_global >= 85:
        color = "green"
        interpretation = "Excellence financière"
        recommendation = "Situation exceptionnelle à maintenir"
    elif score_global >= 70:
        color = "lightgreen"
        interpretation = "Très bonne situation"
        recommendation = "Performance solide avec quelques optimisations possibles"
    elif score_global >= 55:
        color = "orange"
        interpretation = "Bonne situation"
        recommendation = "Situation satisfaisante nécessitant une surveillance"
    elif score_global >= 40:
        color = "orange"
        interpretation = "Situation moyenne"
        recommendation = "Actions correctives recommandées"
    elif score_global >= 25:
        color = "red"
        interpretation = "Situation faible"
        recommendation = "Mesures d'amélioration urgentes requises"
    else:
        color = "darkred"
        interpretation = "Situation critique"
        recommendation = "Restructuration financière nécessaire"
    
    # Affichage du score
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 30px; border-radius: 15px; background-color: {color}20; border: 3px solid {color};">
            <h1 style="color: {color}; margin: 0; font-size: 4em;">{score_global}/100</h1>
            <h3 style="color: {color}; margin: 10px 0;">{interpretation}</h3>
            <p style="color: {color}; margin: 0; font-weight: bold;">{recommendation}</p>
        </div>
        """, unsafe_allow_html=True)

def display_detailed_scores(scores):
    """Affiche les scores détaillés par catégorie"""
    
    st.subheader("📈 Scores Détaillés par Catégorie")
    
    # Définition des catégories avec leurs poids maximum
    categories = [
        ("💧 Liquidité", scores.get('liquidite', 0), 40, "Capacité à honorer les engagements à court terme"),
        ("🏛️ Solvabilité", scores.get('solvabilite', 0), 40, "Solidité de la structure financière"),
        ("📈 Rentabilité", scores.get('rentabilite', 0), 30, "Performance économique et profitabilité"),
        ("⚡ Activité", scores.get('activite', 0), 15, "Efficacité dans l'utilisation des actifs"),
        ("🔧 Gestion", scores.get('gestion', 0), 15, "Qualité de la gestion opérationnelle")
    ]
    
    for emoji_label, score, max_score, description in categories:
        col1, col2, col3 = st.columns([2, 1, 3])
        
        with col1:
            st.markdown(f"**{emoji_label}**")
            st.caption(description)
        
        with col2:
            percentage = (score / max_score) * 100
            st.metric("Score", f"{score}/{max_score}", f"{percentage:.0f}%")
        
        with col3:
            # Barre de progression visuelle
            progress_html = f"""
            <div style="background-color: #f0f0f0; border-radius: 10px; padding: 5px;">
                <div style="background-color: {'green' if percentage >= 75 else 'orange' if percentage >= 50 else 'red'}; 
                            width: {percentage}%; height: 20px; border-radius: 5px; transition: width 0.3s;">
                </div>
            </div>
            <p style="text-align: center; margin: 5px 0; font-size: 12px;">{percentage:.0f}% de performance</p>
            """
            st.markdown(progress_html, unsafe_allow_html=True)

def display_financial_data(data):
    """Affiche les principales données financières"""
    
    st.subheader("💰 Données Financières Principales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Bilan")
        
        # Principales masses du bilan
        bilan_data = [
            ("Total Actif", data.get('total_actif', 0)),
            ("Immobilisations", data.get('immobilisations_nettes', 0)),
            ("Actif Circulant", data.get('total_actif_circulant', 0)),
            ("Trésorerie", data.get('tresorerie', 0)),
            ("Capitaux Propres", data.get('capitaux_propres', 0)),
            ("Dettes Financières", data.get('dettes_financieres', 0)),
            ("Dettes Court Terme", data.get('dettes_court_terme', 0))
        ]
        
        for label, value in bilan_data:
            st.metric(label, f"{value:,.0f} FCFA".replace(',', ' '))
    
    with col2:
        st.markdown("#### 📈 Compte de Résultat")
        
        # Principales données du CR
        cr_data = [
            ("Chiffre d'Affaires", data.get('chiffre_affaires', 0)),
            ("Valeur Ajoutée", data.get('valeur_ajoutee', 0)),
            ("Excédent Brut d'Exploitation", data.get('excedent_brut', 0)),
            ("Résultat d'Exploitation", data.get('resultat_exploitation', 0)),
            ("Résultat Financier", data.get('resultat_financier', 0)),
            ("Résultat Net", data.get('resultat_net', 0))
        ]
        
        for label, value in cr_data:
            # Coloration selon positif/négatif
            if value >= 0:
                st.metric(label, f"{value:,.0f} FCFA".replace(',', ' '))
            else:
                st.metric(label, f"{value:,.0f} FCFA".replace(',', ' '), delta=f"Négatif")

def display_main_ratios(ratios):
    """Affiche les principaux ratios financiers"""
    
    st.subheader("📊 Ratios Financiers Principaux")
    
    # Organisation en tabs pour une meilleure lisibilité
    tab1, tab2, tab3, tab4 = st.tabs(["💧 Liquidité", "🏛️ Solvabilité", "📈 Rentabilité", "⚡ Activité"])
    
    with tab1:
        st.markdown("#### Ratios de Liquidité")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            liquidite_generale = ratios.get('ratio_liquidite_generale', 0)
            interpretation = get_ratio_interpretation(liquidite_generale, 1.5, True)
            st.metric("Liquidité Générale", f"{liquidite_generale:.2f}", interpretation)
            st.caption("Norme : > 1.5")
        
        with col2:
            liquidite_immediate = ratios.get('ratio_liquidite_immediate', 0)
            interpretation = get_ratio_interpretation(liquidite_immediate, 1.0, True)
            st.metric("Liquidité Immédiate", f"{liquidite_immediate:.2f}", interpretation)
            st.caption("Norme : > 1.0")
        
        with col3:
            bfr_jours = ratios.get('bfr_jours_ca', 0)
            interpretation = get_ratio_interpretation(bfr_jours, 60, False)
            st.metric("BFR en jours", f"{bfr_jours:.0f} jours", interpretation)
            st.caption("Norme : < 60 jours")
    
    with tab2:
        st.markdown("#### Ratios de Solvabilité")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            autonomie = ratios.get('ratio_autonomie_financiere', 0)
            interpretation = get_ratio_interpretation(autonomie, 30, True)
            st.metric("Autonomie Financière", f"{autonomie:.1f}%", interpretation)
            st.caption("Norme : > 30%")
        
        with col2:
            endettement = ratios.get('ratio_endettement', 0)
            interpretation = get_ratio_interpretation(endettement, 65, False)
            st.metric("Endettement Global", f"{endettement:.1f}%", interpretation)
            st.caption("Norme : < 65%")
        
        with col3:
            capacite_remb = ratios.get('capacite_remboursement', 0)
            interpretation = get_ratio_interpretation(capacite_remb, 5, False)
            st.metric("Capacité Remboursement", f"{capacite_remb:.1f} ans", interpretation)
            st.caption("Norme : < 5 ans")
    
    with tab3:
        st.markdown("#### Ratios de Rentabilité")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            roe = ratios.get('roe', 0)
            interpretation = get_ratio_interpretation(roe, 10, True)
            st.metric("ROE", f"{roe:.1f}%", interpretation)
            st.caption("Norme : > 10%")
        
        with col2:
            roa = ratios.get('roa', 0)
            interpretation = get_ratio_interpretation(roa, 2, True)
            st.metric("ROA", f"{roa:.1f}%", interpretation)
            st.caption("Norme : > 2%")
        
        with col3:
            marge_nette = ratios.get('marge_nette', 0)
            interpretation = get_ratio_interpretation(marge_nette, 5, True)
            st.metric("Marge Nette", f"{marge_nette:.1f}%", interpretation)
            st.caption("Norme : > 5%")
    
    with tab4:
        st.markdown("#### Ratios d'Activité")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rotation_actif = ratios.get('rotation_actif', 0)
            interpretation = get_ratio_interpretation(rotation_actif, 1.5, True)
            st.metric("Rotation Actif", f"{rotation_actif:.2f}", interpretation)
            st.caption("Norme : > 1.5")
        
        with col2:
            rotation_stocks = ratios.get('rotation_stocks', 0)
            interpretation = get_ratio_interpretation(rotation_stocks, 6, True)
            st.metric("Rotation Stocks", f"{rotation_stocks:.1f}", interpretation)
            st.caption("Norme : > 6")
        
        with col3:
            delai_recouvrement = ratios.get('delai_recouvrement_clients', 0)
            interpretation = get_ratio_interpretation(delai_recouvrement, 45, False)
            st.metric("Délai Recouvrement", f"{delai_recouvrement:.0f} jours", interpretation)
            st.caption("Norme : < 45 jours")

def get_ratio_interpretation(value, norme, higher_is_better):
    """Retourne l'interprétation d'un ratio"""
    
    if higher_is_better:
        if value >= norme * 1.2:
            return "Excellent"
        elif value >= norme:
            return "Bon"
        elif value >= norme * 0.8:
            return "Acceptable"
        else:
            return "Faible"
    else:
        if value <= norme * 0.8:
            return "Excellent"
        elif value <= norme:
            return "Bon"
        elif value <= norme * 1.2:
            return "Acceptable"
        else:
            return "Faible"

def display_interpretation_and_recommendations(scores, ratios, data):
    """Affiche l'interprétation et les recommandations"""
    
    st.subheader("🎯 Interprétation et Recommandations")
    
    score_global = scores.get('global', 0)
    
    # Points forts
    points_forts = []
    if scores.get('liquidite', 0) >= 30:
        points_forts.append("✅ Excellente liquidité")
    if scores.get('solvabilite', 0) >= 30:
        points_forts.append("✅ Structure financière solide")
    if scores.get('rentabilite', 0) >= 20:
        points_forts.append("✅ Rentabilité satisfaisante")
    if ratios.get('tresorerie_nette', 0) > 0:
        points_forts.append("✅ Trésorerie nette positive")
    
    # Points faibles
    points_faibles = []
    if scores.get('liquidite', 0) < 20:
        points_faibles.append("❌ Liquidité insuffisante")
    if scores.get('solvabilite', 0) < 20:
        points_faibles.append("❌ Structure financière fragile")
    if scores.get('rentabilite', 0) < 15:
        points_faibles.append("❌ Rentabilité faible")
    if ratios.get('ratio_endettement', 0) > 80:
        points_faibles.append("❌ Endettement excessif")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💪 Points Forts")
        if points_forts:
            for point in points_forts:
                st.markdown(f"• {point}")
        else:
            st.info("Aucun point fort majeur identifié")
    
    with col2:
        st.markdown("#### ⚠️ Points à Améliorer")
        if points_faibles:
            for point in points_faibles:
                st.markdown(f"• {point}")
        else:
            st.success("Aucun point faible majeur identifié")
    
    # Recommandations générales
    st.markdown("#### 💡 Recommandations Prioritaires")
    
    if score_global >= 70:
        st.success("""
        **Maintenir la performance actuelle :**
        • Continuer les bonnes pratiques de gestion
        • Surveiller l'évolution des ratios clés
        • Prévoir les investissements futurs
        """)
    elif score_global >= 40:
        st.warning("""
        **Améliorer les points faibles identifiés :**
        • Renforcer la liquidité si nécessaire
        • Optimiser la structure financière
        • Améliorer l'efficacité opérationnelle
        """)
    else:
        st.error("""
        **Actions correctives urgentes :**
        • Revoir la stratégie financière
        • Négocier avec les créanciers
        • Améliorer la trésorerie rapidement
        • Considérer un apport en capital
        """)

def display_analysis_actions():
    """Affiche les actions disponibles"""
    
    st.subheader("🚀 Actions Disponibles")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 Retour Accueil", type="secondary", use_container_width=True):
            SessionManager.set_current_page('home')
            st.rerun()
    
    with col2:
        if st.button("📋 Générer Rapport", type="primary", use_container_width=True):
            SessionManager.set_current_page('reports')
            st.rerun()
    
    with col3:
        if st.button("📊 Nouvelle Saisie", type="secondary", use_container_width=True):
            SessionManager.set_current_page('unified_input')
            st.rerun()
    
    with col4:
        if st.button("🔄 Nouvelle Analyse", type="secondary", use_container_width=True):
            # Confirmation de reset
            if st.session_state.get('confirm_analysis_reset', False):
                try:
                    from session_manager import reset_app
                    reset_app()
                    st.success("🔄 Application réinitialisée!")
                    st.rerun()
                except:
                    st.error("Erreur lors de la réinitialisation")
            else:
                st.session_state['confirm_analysis_reset'] = True
                st.warning("⚠️ Cliquez à nouveau pour confirmer le reset")

# Point d'entrée si le fichier est exécuté directement
if __name__ == "__main__":
    show_fallback_analysis_page()
