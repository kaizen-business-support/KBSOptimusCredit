"""
Page d'import unifiée - Section unique avec 3 options
Import Excel, Saisie Manuelle, Import OCR (non actif)
CORRECTION: Navigation vers l'analyse après succès
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

def show_unified_input_page():
    """Page d'import unifiée avec 3 options : Excel, Manuel, OCR"""
    
    st.title("📊 Analyse des États Financiers - BCEAO")
    st.markdown("*Choisissez votre méthode de saisie des données financières*")
    st.markdown("---")
    
    # CORRECTION: Vérifier si une analyse vient d'être terminée et rediriger automatiquement
    if st.session_state.get('analysis_just_completed', False):
        st.session_state['analysis_just_completed'] = False  # Reset du flag
        SessionManager.set_current_page('analysis')
        st.rerun()
    
    # SECTION UNIQUE - Choix de la méthode
    st.header("🔧 Méthode de Saisie des Données")
    
    # Radio buttons horizontaux pour les 3 options
    reset_counter = SessionManager.get_reset_counter()
    method_key = f"input_method_{reset_counter}"
    
    input_method = st.radio(
        "**Sélectionnez votre méthode de saisie :**",
        options=["📤 Import Excel", "✏️ Saisie Manuelle", "🤖 Import OCR"],
        horizontal=True,
        help="Choisissez la méthode qui convient le mieux à vos données",
        key=method_key
    )
    
    st.markdown("---")
    
    # SECTION CONDITIONNELLE SELON LA MÉTHODE CHOISIE
    if input_method == "📤 Import Excel":
        show_excel_import_section()
    
    elif input_method == "✏️ Saisie Manuelle":
        show_manual_input_section()
    
    elif input_method == "🤖 Import OCR":
        show_ocr_import_section()

def show_excel_import_section():
    """Section d'import Excel"""
    
    st.subheader("📤 Import de Fichier Excel")
    
    # Vérifier s'il y a déjà une analyse
    if SessionManager.has_analysis_data():
        show_existing_analysis_warning("excel")
        return
    
    # Initialiser les variables de session
    if 'file_uploaded' not in st.session_state:
        st.session_state['file_uploaded'] = False
    if 'file_content' not in st.session_state:
        st.session_state['file_content'] = None
    if 'file_name' not in st.session_state:
        st.session_state['file_name'] = None
    if 'analysis_running' not in st.session_state:
        st.session_state['analysis_running'] = False
    
    # Gérer le reset si nécessaire
    if st.session_state.get('complete_reset', False):
        st.success("🔄 Application réinitialisée! Vous pouvez importer un nouveau fichier.")
        st.session_state['file_uploaded'] = False
        st.session_state['file_content'] = None
        st.session_state['file_name'] = None
        st.session_state['analysis_running'] = False
        del st.session_state['complete_reset']
        st.rerun()
    
    if not st.session_state['file_uploaded']:
        # Zone d'upload de fichier
        with st.container():
            st.markdown("#### 📁 Sélection du Fichier")
            st.info("💡 **Format requis :** Fichier Excel (.xlsx, .xls) avec les feuilles 'Bilan' et 'CR' (Compte de Résultat)")
            
            reset_counter = SessionManager.get_reset_counter()
            uploader_key = f"file_uploader_unified_{reset_counter}"
            
            uploaded_file = st.file_uploader(
                "Glissez-déposez votre fichier ou cliquez pour sélectionner",
                type=['xlsx', 'xls'],
                help="Le fichier doit contenir les feuilles : Bilan, CR (Compte de Résultat)",
                key=uploader_key
            )
            
            if uploaded_file is not None:
                st.session_state['file_content'] = uploaded_file.getbuffer()
                st.session_state['file_name'] = uploaded_file.name
                st.session_state['file_uploaded'] = True
                st.success(f"✅ Fichier '{uploaded_file.name}' chargé avec succès!")
                st.rerun()
    
    else:
        # Fichier uploadé - Configuration et analyse
        with st.expander("📋 Fichier Sélectionné", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("**Nom du fichier**", st.session_state['file_name'])
            with col2:
                st.metric("**Taille**", f"{len(st.session_state['file_content']) / 1024:.1f} KB")
            with col3:
                st.success("✅ **Statut :** Prêt pour analyse")
        
        # Sélection du secteur
        st.markdown("#### 🏭 Configuration de l'Analyse")
        
        reset_counter = SessionManager.get_reset_counter()
        secteur_key = f"secteur_excel_{reset_counter}"
        
        secteur = st.selectbox(
            "**Secteur d'activité pour comparaison :**",
            options=[
                "industrie_manufacturiere",
                "commerce_detail", 
                "services_professionnels",
                "construction_btp",
                "agriculture",
                "commerce_gros"
            ],
            format_func=lambda x: {
                "industrie_manufacturiere": "🏭 Industrie Manufacturière",
                "commerce_detail": "🛒 Commerce de Détail",
                "services_professionnels": "💼 Services Professionnels", 
                "construction_btp": "🏗️ Construction / BTP",
                "agriculture": "🌾 Agriculture",
                "commerce_gros": "📦 Commerce de Gros"
            }.get(x, x),
            key=secteur_key,
            help="Sélectionnez le secteur le plus proche de votre activité pour une comparaison pertinente"
        )
        
        # Boutons d'action
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if not st.session_state['analysis_running']:
                analyze_key = f"analyze_excel_btn_{reset_counter}"
                if st.button("🚀 Analyser", type="primary", use_container_width=True, key=analyze_key):
                    st.session_state['analysis_running'] = True
                    analyze_excel_file(st.session_state['file_content'], st.session_state['file_name'], secteur)
            else:
                st.info("🔄 Analyse en cours...")
        
        with col2:
            new_file_key = f"new_excel_file_{reset_counter}"
            if st.button("📄 Nouveau Fichier", use_container_width=True, key=new_file_key):
                st.session_state['file_uploaded'] = False
                st.session_state['file_content'] = None
                st.session_state['file_name'] = None
                st.session_state['analysis_running'] = False
                st.rerun()
        
        with col3:
            home_key = f"excel_home_{reset_counter}"
            if st.button("🏠 Accueil", use_container_width=True, key=home_key):
                SessionManager.set_current_page('home')
                st.rerun()

def show_manual_input_section():
    """Section de saisie manuelle"""
    
    st.subheader("✏️ Saisie Manuelle des Données")
    
    # Vérifier s'il y a déjà une analyse
    if SessionManager.has_analysis_data():
        show_existing_analysis_warning("manuel")
        return
    
    st.info("💡 Saisissez vos données financières pour obtenir une analyse complète selon les normes BCEAO")
    
    # Sélection du secteur
    st.markdown("#### 🏭 Secteur d'Activité")
    
    reset_counter = SessionManager.get_reset_counter()
    secteur_key = f"secteur_manual_{reset_counter}"
    
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
            "industrie_manufacturiere": "🏭 Industrie Manufacturière",
            "commerce_detail": "🛒 Commerce de Détail",
            "services_professionnels": "💼 Services Professionnels", 
            "construction_btp": "🏗️ Construction / BTP",
            "agriculture": "🌾 Agriculture",
            "commerce_gros": "📦 Commerce de Gros"
        }.get(x, x),
        key=secteur_key
    )
    
    # Onglets pour organiser la saisie
    tab_bilan, tab_cr, tab_flux = st.tabs([
        "📊 Bilan", "📈 Compte de Résultat", "💰 Flux de Trésorerie"
    ])
    
    # Initialiser les données
    data = {}
    
    with tab_bilan:
        data = create_bilan_input_section(data, reset_counter)
    
    with tab_cr:
        data = create_cr_input_section(data, reset_counter)
    
    with tab_flux:
        data = create_flux_input_section(data, reset_counter)
    
    # Validation et analyse
    st.markdown("---")
    st.header("🔍 Validation et Analyse")
    
    errors, warnings = validate_financial_data(data)
    
    # Affichage des erreurs et avertissements
    if errors:
        st.error("❌ **Erreurs à corriger :**")
        for error in errors:
            st.error(f"• {error}")
    
    if warnings:
        st.warning("⚠️ **Avertissements :**")
        for warning in warnings:
            st.warning(f"• {warning}")
    
    # Boutons d'action
    col1, col2 = st.columns(2)
    
    with col1:
        if not errors:
            analyze_key = f"analyze_manual_{reset_counter}"
            if st.button("🔍 Lancer l'Analyse", type="primary", use_container_width=True, key=analyze_key):
                analyze_manual_data(data, secteur)
        else:
            st.button("🔍 Analyse (Corrigez les erreurs)", disabled=True, use_container_width=True)
    
    with col2:
        home_manual_key = f"manual_home_{reset_counter}"
        if st.button("🏠 Accueil", use_container_width=True, key=home_manual_key):
            SessionManager.set_current_page('home')
            st.rerun()

def show_ocr_import_section():
    """Section d'import OCR (en développement)"""
    
    st.subheader("🤖 Import OCR - Reconnaissance Optique")
    
    # Message de développement
    st.info("🚧 **Fonctionnalité en développement**")
    
    st.markdown("""
    ### 🔮 Prochainement Disponible
    
    Cette fonctionnalité permettra d'extraire automatiquement les données financières 
    à partir de documents scannés ou photographiés.
    
    **Fonctionnalités prévues :**
    - 📸 Import de photos de documents
    - 📄 Traitement de PDF scannés
    - 🤖 Reconnaissance automatique des montants
    - ✅ Validation intelligente des données extraites
    - 📊 Analyse immédiate après extraction
    
    **Formats supportés :**
    - Images : JPG, PNG, TIFF
    - Documents : PDF scannés
    - Qualité : Haute résolution recommandée
    
    ### 📅 Disponibilité Prévue
    
    **Version 2.2** - Q3 2025
    """)
    
    # Interface factice pour donner un aperçu
    st.markdown("---")
    st.markdown("#### 📸 Interface de Démonstration")
    
    # Upload factice (désactivé)
    uploaded_image = st.file_uploader(
        "Sélectionnez une image ou un PDF (Non fonctionnel)",
        type=['jpg', 'jpeg', 'png', 'pdf'],
        disabled=True,
        help="Cette fonctionnalité sera disponible dans la version 2.2"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.button("🤖 Analyser avec OCR", disabled=True, use_container_width=True)
        st.caption("En développement")
    
    with col2:
        home_ocr_key = f"ocr_home_{SessionManager.get_reset_counter()}"
        if st.button("🏠 Retour Accueil", use_container_width=True, key=home_ocr_key):
            SessionManager.set_current_page('home')
            st.rerun()
    
    # Section d'aide
    with st.expander("💡 En attendant cette fonctionnalité", expanded=False):
        st.markdown("""
        ### 🔄 Solutions Actuelles
        
        En attendant l'OCR, vous pouvez utiliser :
        
        **📤 Import Excel :**
        - Tapez vos données dans le modèle Excel BCEAO
        - Import instantané et analyse automatique
        
        **✏️ Saisie Manuelle :**
        - Interface guidée étape par étape
        - Validation en temps réel
        - Calculs automatiques
        
        ### 📧 Être Notifié
        
        Pour être informé de la disponibilité de l'OCR :
        - Email : contact@kaizen-corporation.com
        - Objet : "Notification OCR - OptimusCredit"
        """)

def create_bilan_input_section(data, reset_counter):
    """Crée la section de saisie du bilan avec données détaillées"""
    
    st.header("📊 Bilan Détaillé")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## **ACTIF**")
        
        # Immobilisations
        st.markdown("### **Immobilisations**")
        data['terrains'] = st.number_input(
            "Terrains", min_value=0.0, value=0.0, format="%.0f",
            key=f"terrains_{reset_counter}")
        data['batiments'] = st.number_input(
            "Bâtiments", min_value=0.0, value=0.0, format="%.0f",
            key=f"batiments_{reset_counter}")
        data['materiel_mobilier'] = st.number_input(
            "Matériel et mobilier", min_value=0.0, value=0.0, format="%.0f",
            key=f"materiel_{reset_counter}")
        data['materiel_transport'] = st.number_input(
            "Matériel de transport", min_value=0.0, value=0.0, format="%.0f",
            key=f"transport_{reset_counter}")
        
        data['immobilisations_nettes'] = (data['terrains'] + data['batiments'] + 
                                        data['materiel_mobilier'] + data['materiel_transport'])
        st.markdown(f"**Total Immobilisations : {data['immobilisations_nettes']:,.0f} FCFA**")
        
        # Actif Circulant
        st.markdown("### **Actif Circulant**")
        data['stocks'] = st.number_input(
            "Stocks", min_value=0.0, value=0.0, format="%.0f",
            key=f"stocks_{reset_counter}")
        data['creances_clients'] = st.number_input(
            "Créances clients", min_value=0.0, value=0.0, format="%.0f",
            key=f"creances_clients_{reset_counter}")
        data['autres_creances'] = st.number_input(
            "Autres créances", min_value=0.0, value=0.0, format="%.0f",
            key=f"autres_creances_{reset_counter}")
        
        data['total_actif_circulant'] = (data['stocks'] + data['creances_clients'] + data['autres_creances'])
        st.markdown(f"**Total Actif Circulant : {data['total_actif_circulant']:,.0f} FCFA**")
        
        # Trésorerie Actif
        st.markdown("### **Trésorerie Actif**")
        data['banques_caisses'] = st.number_input(
            "Banques et caisses", min_value=0.0, value=0.0, format="%.0f",
            key=f"banques_{reset_counter}")
        data['titres_placement'] = st.number_input(
            "Titres de placement", min_value=0.0, value=0.0, format="%.0f",
            key=f"titres_placement_{reset_counter}")
        
        data['tresorerie'] = data['banques_caisses'] + data['titres_placement']
        st.markdown(f"**Total Trésorerie Actif : {data['tresorerie']:,.0f} FCFA**")
        
        # Total Actif
        data['total_actif'] = data['immobilisations_nettes'] + data['total_actif_circulant'] + data['tresorerie']
        st.markdown(f"# **TOTAL ACTIF : {data['total_actif']:,.0f} FCFA**")
    
    with col2:
        st.markdown("## **PASSIF**")
        
        # Capitaux Propres
        st.markdown("### **Capitaux Propres**")
        data['capital'] = st.number_input(
            "Capital social", min_value=0.0, value=0.0, format="%.0f",
            key=f"capital_{reset_counter}")
        data['reserves'] = st.number_input(
            "Réserves", min_value=0.0, value=0.0, format="%.0f",
            key=f"reserves_{reset_counter}")
        data['report_nouveau'] = st.number_input(
            "Report à nouveau", value=0.0, format="%.0f",
            key=f"report_{reset_counter}")
        data['resultat_net'] = st.number_input(
            "Résultat net de l'exercice", value=0.0, format="%.0f",
            key=f"resultat_{reset_counter}")
        
        data['capitaux_propres'] = (data['capital'] + data['reserves'] + 
                                   data['report_nouveau'] + data['resultat_net'])
        st.markdown(f"**Total Capitaux Propres : {data['capitaux_propres']:,.0f} FCFA**")
        
        # Dettes Financières
        st.markdown("### **Dettes Financières**")
        data['emprunts_bancaires'] = st.number_input(
            "Emprunts bancaires", min_value=0.0, value=0.0, format="%.0f",
            key=f"emprunts_{reset_counter}")
        data['autres_dettes_financieres'] = st.number_input(
            "Autres dettes financières", min_value=0.0, value=0.0, format="%.0f",
            key=f"autres_dettes_fin_{reset_counter}")
        
        data['dettes_financieres'] = data['emprunts_bancaires'] + data['autres_dettes_financieres']
        st.markdown(f"**Total Dettes Financières : {data['dettes_financieres']:,.0f} FCFA**")
        
        # Dettes Court Terme
        st.markdown("### **Dettes Court Terme**")
        data['fournisseurs'] = st.number_input(
            "Dettes fournisseurs", min_value=0.0, value=0.0, format="%.0f",
            key=f"fournisseurs_{reset_counter}")
        data['dettes_sociales_fiscales'] = st.number_input(
            "Dettes sociales et fiscales", min_value=0.0, value=0.0, format="%.0f",
            key=f"dettes_soc_fisc_{reset_counter}")
        data['autres_dettes'] = st.number_input(
            "Autres dettes", min_value=0.0, value=0.0, format="%.0f",
            key=f"autres_dettes_{reset_counter}")
        
        data['dettes_court_terme'] = (data['fournisseurs'] + data['dettes_sociales_fiscales'] + 
                                     data['autres_dettes'])
        st.markdown(f"**Total Dettes Court Terme : {data['dettes_court_terme']:,.0f} FCFA**")
        
        # Trésorerie Passif
        st.markdown("### **Trésorerie Passif**")
        data['tresorerie_passif'] = st.number_input(
            "Crédits de trésorerie", min_value=0.0, value=0.0, format="%.0f",
            key=f"credits_treso_{reset_counter}")
        
        # Total Passif
        total_passif = (data['capitaux_propres'] + data['dettes_financieres'] + 
                       data['dettes_court_terme'] + data['tresorerie_passif'])
        st.markdown(f"# **TOTAL PASSIF : {total_passif:,.0f} FCFA**")
        
        # Vérification équilibre
        equilibre = abs(data['total_actif'] - total_passif)
        if equilibre < 1000:
            st.success(f"✅ **Bilan équilibré** (écart: {equilibre:,.0f})")
        else:
            st.error(f"❌ **Bilan déséquilibré** (écart: {equilibre:,.0f})")
    
    return data

def create_cr_input_section(data, reset_counter):
    """Crée la section de saisie du compte de résultat"""
    
    st.header("📈 Compte de Résultat")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **Produits**")
        
        data['ventes_marchandises'] = st.number_input(
            "Ventes de marchandises", min_value=0.0, value=0.0, format="%.0f",
            key=f"ventes_march_{reset_counter}")
        data['ventes_produits_fabriques'] = st.number_input(
            "Ventes de produits fabriqués", min_value=0.0, value=0.0, format="%.0f",
            key=f"ventes_prod_{reset_counter}")
        data['travaux_services_vendus'] = st.number_input(
            "Travaux et services vendus", min_value=0.0, value=0.0, format="%.0f",
            key=f"services_{reset_counter}")
        
        data['chiffre_affaires'] = (data['ventes_marchandises'] + data['ventes_produits_fabriques'] + 
                                   data['travaux_services_vendus'])
        st.markdown(f"**Chiffre d'Affaires : {data['chiffre_affaires']:,.0f} FCFA**")
        
        data['autres_produits'] = st.number_input(
            "Autres produits", min_value=0.0, value=0.0, format="%.0f",
            key=f"autres_prod_{reset_counter}")
        data['revenus_financiers'] = st.number_input(
            "Revenus financiers", min_value=0.0, value=0.0, format="%.0f",
            key=f"rev_fin_{reset_counter}")
        
        total_produits = data['chiffre_affaires'] + data['autres_produits'] + data['revenus_financiers']
        st.markdown(f"**Total Produits : {total_produits:,.0f} FCFA**")
    
    with col2:
        st.markdown("### **Charges**")
        
        data['achats_marchandises'] = st.number_input(
            "Achats de marchandises", min_value=0.0, value=0.0, format="%.0f",
            key=f"achats_march_{reset_counter}")
        data['achats_matieres_premieres'] = st.number_input(
            "Achats matières premières", min_value=0.0, value=0.0, format="%.0f",
            key=f"achats_mp_{reset_counter}")
        data['autres_achats'] = st.number_input(
            "Autres achats", min_value=0.0, value=0.0, format="%.0f",
            key=f"autres_achats_{reset_counter}")
        data['charges_externes'] = st.number_input(
            "Charges externes", min_value=0.0, value=0.0, format="%.0f",
            key=f"charges_ext_{reset_counter}")
        data['charges_personnel'] = st.number_input(
            "Charges de personnel", min_value=0.0, value=0.0, format="%.0f",
            key=f"charges_pers_{reset_counter}")
        data['dotations_amortissements'] = st.number_input(
            "Dotations amortissements", min_value=0.0, value=0.0, format="%.0f",
            key=f"amort_{reset_counter}")
        data['frais_financiers'] = st.number_input(
            "Frais financiers", min_value=0.0, value=0.0, format="%.0f",
            key=f"frais_fin_{reset_counter}")
        data['impots_resultat'] = st.number_input(
            "Impôts sur le résultat", min_value=0.0, value=0.0, format="%.0f",
            key=f"impots_{reset_counter}")
        
        data['charges_exploitation'] = (data['achats_marchandises'] + data['achats_matieres_premieres'] + 
                                       data['autres_achats'] + data['charges_externes'] + 
                                       data['charges_personnel'] + data['dotations_amortissements'])
        
        total_charges = (data['charges_exploitation'] + data['frais_financiers'] + data['impots_resultat'])
        st.markdown(f"**Total Charges : {total_charges:,.0f} FCFA**")
    
    # Calculs des soldes
    data['valeur_ajoutee'] = data['chiffre_affaires'] - (data['achats_marchandises'] + 
                                                        data['achats_matieres_premieres'] + 
                                                        data['autres_achats'] + data['charges_externes'])
    data['excedent_brut'] = data['valeur_ajoutee'] - data['charges_personnel']
    data['resultat_exploitation'] = data['excedent_brut'] - data['dotations_amortissements']
    data['resultat_financier'] = data['revenus_financiers'] - data['frais_financiers']
    
    # Vérification cohérence
    resultat_calcule = data['resultat_exploitation'] + data['resultat_financier'] - data['impots_resultat']
    
    st.markdown("---")
    st.markdown("### **Soldes Intermédiaires**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Valeur Ajoutée", f"{data['valeur_ajoutee']:,.0f}")
        st.metric("Excédent Brut", f"{data['excedent_brut']:,.0f}")
    
    with col2:
        st.metric("Résultat Exploitation", f"{data['resultat_exploitation']:,.0f}")
        st.metric("Résultat Financier", f"{data['resultat_financier']:,.0f}")
    
    with col3:
        st.metric("Résultat Calculé", f"{resultat_calcule:,.0f}")
        if abs(resultat_calcule - data['resultat_net']) > 1000:
            st.warning(f"⚠️ Écart: {abs(resultat_calcule - data['resultat_net']):,.0f}")
        else:
            st.success("✅ Cohérent")
    
    return data

def create_flux_input_section(data, reset_counter):
    """Crée la section de saisie des flux de trésorerie"""
    
    st.header("💰 Flux de Trésorerie")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **Flux d'Exploitation**")
        
        data['cafg'] = st.number_input(
            "CAFG (Capacité d'autofinancement)", 
            value=data.get('resultat_net', 0) + data.get('dotations_amortissements', 0),
            format="%.0f",
            key=f"cafg_{reset_counter}")
        
        data['variation_bfr'] = st.number_input(
            "Variation du BFR", value=0.0, format="%.0f",
            key=f"var_bfr_{reset_counter}")
        
        data['flux_activites_operationnelles'] = data['cafg'] - data['variation_bfr']
        st.metric("Flux Opérationnels", f"{data['flux_activites_operationnelles']:,.0f} FCFA")
        
        st.markdown("### **Flux d'Investissement**")
        
        data['acquisitions_immobilisations'] = st.number_input(
            "Acquisitions d'immobilisations", value=0.0, format="%.0f",
            key=f"acq_immob_{reset_counter}")
        data['cessions_immobilisations'] = st.number_input(
            "Cessions d'immobilisations", min_value=0.0, value=0.0, format="%.0f",
            key=f"cess_immob_{reset_counter}")
        
        data['flux_activites_investissement'] = (data['cessions_immobilisations'] - 
                                                data['acquisitions_immobilisations'])
        st.metric("Flux Investissement", f"{data['flux_activites_investissement']:,.0f} FCFA")
    
    with col2:
        st.markdown("### **Flux de Financement**")
        
        data['augmentation_capital'] = st.number_input(
            "Augmentation de capital", min_value=0.0, value=0.0, format="%.0f",
            key=f"aug_capital_{reset_counter}")
        data['nouveaux_emprunts'] = st.number_input(
            "Nouveaux emprunts", min_value=0.0, value=0.0, format="%.0f",
            key=f"nouveaux_emprunts_{reset_counter}")
        data['remboursements_emprunts'] = st.number_input(
            "Remboursements d'emprunts", min_value=0.0, value=0.0, format="%.0f",
            key=f"rembours_emprunts_{reset_counter}")
        data['dividendes_verses'] = st.number_input(
            "Dividendes versés", min_value=0.0, value=0.0, format="%.0f",
            key=f"dividendes_{reset_counter}")
        
        data['flux_activites_financement'] = (data['augmentation_capital'] + data['nouveaux_emprunts'] - 
                                             data['remboursements_emprunts'] - data['dividendes_verses'])
        st.metric("Flux Financement", f"{data['flux_activites_financement']:,.0f} FCFA")
        
        st.markdown("### **Synthèse**")
        
        data['variation_tresorerie'] = (data['flux_activites_operationnelles'] + 
                                       data['flux_activites_investissement'] + 
                                       data['flux_activites_financement'])
        
        data['tresorerie_ouverture'] = st.number_input(
            "Trésorerie d'ouverture", value=0.0, format="%.0f",
            key=f"treso_ouverture_{reset_counter}")
        
        data['tresorerie_cloture'] = data['tresorerie_ouverture'] + data['variation_tresorerie']
        
        st.metric("Variation Trésorerie", f"{data['variation_tresorerie']:,.0f} FCFA")
        st.metric("Trésorerie Clôture", f"{data['tresorerie_cloture']:,.0f} FCFA")
    
    return data

def show_existing_analysis_warning(source_type):
    """Affiche un avertissement si une analyse existe déjà"""
    
    score, metadata = SessionManager.get_analysis_info()
    source = metadata.get('source', 'inconnue')
    
    st.warning(f"⚠️ **Analyse existante détectée** (Source: {source}, Score: {score}/100)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        view_key = f"view_existing_{source_type}_{SessionManager.get_reset_counter()}"
        if st.button("📊 Voir l'Analyse", key=view_key, type="primary"):
            SessionManager.set_current_page('analysis')
            st.rerun()
    
    with col2:
        reset_key = f"reset_for_new_{source_type}_{SessionManager.get_reset_counter()}"
        if st.button("🔄 Nouvelle Analyse", key=reset_key, type="secondary"):
            reset_app()
            st.rerun()
    
    with col3:
        home_key = f"home_from_{source_type}_{SessionManager.get_reset_counter()}"
        if st.button("🏠 Accueil", key=home_key):
            SessionManager.set_current_page('home')
            st.rerun()
    
    st.markdown("---")

def validate_financial_data(data):
    """Valide la cohérence des données financières"""
    
    errors = []
    warnings = []
    
    # Vérifications obligatoires
    if data.get('total_actif', 0) <= 0:
        errors.append("Total actif invalide ou nul")
    
    if data.get('chiffre_affaires', 0) <= 0:
        errors.append("Chiffre d'affaires invalide ou nul")
    
    # Vérifications de cohérence du bilan
    total_passif = (
        data.get('capitaux_propres', 0) + 
        data.get('dettes_financieres', 0) + 
        data.get('dettes_court_terme', 0) + 
        data.get('tresorerie_passif', 0)
    )
    
    if abs(data.get('total_actif', 0) - total_passif) > 1000:
        errors.append(f"Bilan non équilibré (écart: {abs(data.get('total_actif', 0) - total_passif):,.0f} FCFA)")
    
    # Vérifications de vraisemblance
    if data.get('capitaux_propres', 0) <= 0:
        warnings.append("Capitaux propres négatifs ou nuls - Situation critique")
    
    if data.get('resultat_net', 0) < 0:
        warnings.append("Résultat net négatif - Perte de l'exercice")
    
    # Vérifications sectorielles
    if data.get('chiffre_affaires', 0) > 0:
        if data.get('charges_personnel', 0) > data.get('chiffre_affaires', 0):
            warnings.append("Charges de personnel supérieures au chiffre d'affaires")
        
        if data.get('charges_exploitation', 0) > data.get('chiffre_affaires', 0) * 1.2:
            warnings.append("Charges d'exploitation très élevées (>120% du CA)")
    
    return errors, warnings

def analyze_excel_file(file_content, filename, secteur):
    """CORRECTION: Analyse le fichier Excel avec redirection automatique"""
    
    try:
        with st.spinner("📊 Analyse du fichier Excel en cours..."):
            # Créer un fichier temporaire
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(file_content)
                temp_path = tmp_file.name
            
            try:
                # Importer l'analyseur
                from modules.core.analyzer import FinancialAnalyzer
                
                # Analyser le fichier
                analyzer = FinancialAnalyzer()
                data = analyzer.load_excel_template(temp_path)
                
                if data is None:
                    st.error("❌ Erreur lors du chargement du fichier Excel")
                    st.error("Vérifiez que le fichier contient les feuilles 'Bilan' et 'CR' avec les données aux bonnes positions")
                    st.session_state['analysis_running'] = False
                    return
                
                # Calculer les ratios et scores
                ratios = analyzer.calculate_ratios(data)
                scores = analyzer.calculate_score(ratios, secteur)
                
                # Métadonnées
                metadata = {
                    'secteur': secteur,
                    'fichier_nom': filename,
                    'source': 'excel_import_unified'
                }
                
                # Stocker l'analyse
                store_analysis(data, ratios, scores, metadata)
                
                st.success("✅ Analyse terminée avec succès!")
                
                # Afficher un résumé rapide
                score_global = scores.get('global', 0)
                interpretation, color = SessionManager.get_interpretation(score_global)
                
                st.markdown(f"""
                ### 📊 Résultat de l'Analyse
                **Score Global BCEAO :** {score_global}/100  
                **Évaluation :** {interpretation}  
                **Classe :** {SessionManager.get_financial_class(score_global)}
                """)
                
                # Réinitialiser le flag
                st.session_state['analysis_running'] = False
                
                # CORRECTION: Proposer la navigation avec redirection automatique
                col1, col2 = st.columns(2)
                
                reset_counter = SessionManager.get_reset_counter()
                
                with col1:
                    goto_analysis_key = f"goto_analysis_excel_{reset_counter}"
                    if st.button("📊 Voir l'Analyse Complète", key=goto_analysis_key, type="primary"):
                        # CORRECTION: Redirection immédiate vers l'analyse
                        SessionManager.set_current_page('analysis')
                        st.rerun()
                
                with col2:
                    goto_reports_key = f"goto_reports_excel_{reset_counter}"
                    if st.button("📋 Générer un Rapport", key=goto_reports_key, type="secondary"):
                        SessionManager.set_current_page('reports')
                        st.rerun()
                
                # CORRECTION: Auto-redirection après 3 secondes (optionnel)
                st.info("💡 **Cliquez sur 'Voir l'Analyse Complète' pour accéder aux détails ou attendez la redirection automatique...**")
                
                # IMPORTANT: Marquer que l'analyse vient d'être complétée
                st.session_state['analysis_just_completed'] = True
                
                # Auto-redirection après un délai
                import time
                time.sleep(1)  # Délai pour que l'utilisateur voie le message
                SessionManager.set_current_page('analysis')
                st.rerun()
                
            finally:
                # Nettoyer le fichier temporaire
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
    
    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse : {str(e)}")
        st.session_state['analysis_running'] = False

def analyze_manual_data(data, secteur):
    """CORRECTION: Analyse les données saisies avec redirection automatique"""
    
    try:
        with st.spinner("📊 Analyse des données saisies..."):
            # Importer l'analyseur
            from modules.core.analyzer import FinancialAnalyzer
            
            # Créer l'analyseur
            analyzer = FinancialAnalyzer()
            
            # Calculer les ratios
            ratios = analyzer.calculate_ratios(data)
            
            # Calculer les scores
            scores = analyzer.calculate_score(ratios, secteur)
            
            # Métadonnées
            metadata = {
                'secteur': secteur,
                'source': 'manual_input_unified',
                'mode_saisie': 'manuelle_unifiee',
                'fichier_nom': 'Saisie Manuelle Unifiée'
            }
            
            # Stocker via le gestionnaire centralisé
            store_analysis(data, ratios, scores, metadata)
            
            st.success("✅ Analyse financière réalisée avec succès!")
            
            # Afficher un résumé rapide
            score_global = scores.get('global', 0)
            interpretation, color = SessionManager.get_interpretation(score_global)
            
            st.markdown(f"""
            ### 📊 Résultat de l'Analyse
            **Score Global BCEAO :** {score_global}/100  
            **Évaluation :** {interpretation}  
            **Classe :** {SessionManager.get_financial_class(score_global)}
            """)
            
            # Proposition de navigation avec redirection automatique
            col1, col2 = st.columns(2)
            
            reset_counter = SessionManager.get_reset_counter()
            
            with col1:
                goto_analysis_key = f"goto_analysis_manual_{reset_counter}"
                if st.button("📊 Voir l'Analyse Complète", key=goto_analysis_key, type="primary"):
                    # CORRECTION: Redirection immédiate vers l'analyse
                    SessionManager.set_current_page('analysis')
                    st.rerun()
            
            with col2:
                goto_reports_key = f"goto_reports_manual_{reset_counter}"
                if st.button("📋 Générer un Rapport", key=goto_reports_key, type="secondary"):
                    SessionManager.set_current_page('reports')
                    st.rerun()
            
            # CORRECTION: Auto-redirection après message
            st.info("💡 **Redirection automatique vers l'analyse complète...**")
            
            # IMPORTANT: Marquer que l'analyse vient d'être complétée
            st.session_state['analysis_just_completed'] = True
            
            # Auto-redirection immédiate
            import time
            time.sleep(1)
            SessionManager.set_current_page('analysis')
            st.rerun()
    
    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse: {str(e)}")
        st.error("Vérifiez vos données et réessayez.")

def show_analysis_summary_unified():
    """Affiche un résumé de l'analyse dans la page unifiée"""
    
    if not SessionManager.has_analysis_data():
        return
    
    analysis_data = SessionManager.get_analysis_data()
    scores = analysis_data['scores']
    metadata = analysis_data['metadata']
    
    st.markdown("---")
    st.header("📊 Analyse Disponible")
    
    score_global = scores.get('global', 0)
    interpretation, color = SessionManager.get_interpretation(score_global)
    
    # Affichage du score
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: {color}20; border: 2px solid {color};">
            <h2 style="color: {color}; margin: 0;">Score Global BCEAO</h2>
            <h1 style="color: {color}; margin: 10px 0;">{score_global}/100</h1>
            <p style="color: {color}; margin: 0; font-weight: bold;">{interpretation}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Informations sur l'analyse
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        source = metadata.get('source', 'inconnue').replace('_', ' ').title()
        st.metric("Source", source)
    
    with col2:
        secteur = metadata.get('secteur', '').replace('_', ' ').title()
        st.metric("Secteur", secteur)
    
    with col3:
        classe = SessionManager.get_financial_class(score_global)
        st.metric("Classe BCEAO", classe)
    
    with col4:
        ratios_count = metadata.get('ratios_count', 0)
        st.metric("Ratios Calculés", ratios_count)
    
    # Actions disponibles
    st.markdown("#### 🎯 Actions Disponibles")
    
    col1, col2, col3, col4 = st.columns(4)
    
    reset_counter = SessionManager.get_reset_counter()
    
    with col1:
        view_analysis_key = f"view_analysis_unified_{reset_counter}"
        if st.button("📊 Analyse Complète", key=view_analysis_key, type="primary", use_container_width=True):
            SessionManager.set_current_page('analysis')
            st.rerun()
    
    with col2:
        generate_report_key = f"generate_report_unified_{reset_counter}"
        if st.button("📋 Générer Rapport", key=generate_report_key, use_container_width=True):
            SessionManager.set_current_page('reports')
            st.rerun()
    
    with col3:
        new_analysis_key = f"new_analysis_unified_{reset_counter}"
        if st.button("🔄 Nouvelle Analyse", key=new_analysis_key, use_container_width=True):
            if st.session_state.get('confirm_reset', False):
                reset_app()
                st.rerun()
            else:
                st.session_state['confirm_reset'] = True
                st.warning("⚠️ Cliquez à nouveau pour confirmer")
    
    with col4:
        home_unified_key = f"home_unified_{reset_counter}"
        if st.button("🏠 Accueil", key=home_unified_key, use_container_width=True):
            SessionManager.set_current_page('home')
            st.rerun()

# Instructions d'utilisation de la page unifiée
def show_unified_instructions():
    """Affiche les instructions pour la page unifiée"""
    
    with st.expander("💡 Guide d'Utilisation de la Page Unifiée", expanded=False):
        st.markdown("""
        ### 🎯 Méthodes de Saisie Disponibles
        
        **📤 Import Excel :**
        - Format BCEAO standard avec feuilles Bilan et CR
        - Extraction automatique des données
        - Analyse instantanée après import
        - Idéal pour : Données déjà informatisées
        
        **✏️ Saisie Manuelle :**
        - Interface simplifiée avec les postes essentiels
        - Validation en temps réel et calculs automatiques
        - Grandes masses mises en évidence (en gras)
        - Idéal pour : Données papier ou saisie directe
        
        **🤖 Import OCR :**
        - Reconnaissance automatique de documents scannés
        - Extraction intelligente des montants
        - ⚠️ En développement - Disponible Q3 2025
        - Idéal pour : Documents papier numérisés
        
        ### 📊 Avantages de la Version Unifiée
        
        - **Interface unique** : Plus de navigation entre pages
        - **Choix adapté** : Méthode selon vos besoins
        - **Validation renforcée** : Contrôles de cohérence
        - **Navigation fluide** : Passage direct à l'analyse
        - **Anti-réinitialisation** : Vos données persistent
        """)
    
    with st.expander("🎯 Recommandations par Type d'Entreprise", expanded=False):
        st.markdown("""
        ### 🏭 Industrie Manufacturière
        **Méthode recommandée :** Import Excel
        **Points d'attention :** Stocks de matières premières, immobilisations
        
        ### 🛒 Commerce de Détail
        **Méthode recommandée :** Import Excel
        **Points d'attention :** Rotation des stocks, trésorerie
        
        ### 💼 Services Professionnels
        **Méthode recommandée :** Saisie Manuelle
        **Points d'attention :** Charges de personnel, créances clients
        
        ### 🏗️ Construction / BTP
        **Méthode recommandée :** Saisie Manuelle
        **Points d'attention :** Avances clients, immobilisations
        
        ### 🌾 Agriculture
        **Méthode recommandée :** Import Excel
        **Points d'attention :** Stocks biologiques, saisonnalité
        
        ### 📦 Commerce de Gros
        **Méthode recommandée :** Import Excel
        **Points d'attention :** Rotation des stocks, délais de paiement
        """)

# Si l'analyse est disponible, l'afficher à la fin
if __name__ == "__main__":
    # Cette section ne sera exécutée que si le fichier est lancé directement
    # (pour des tests par exemple)
    pass
