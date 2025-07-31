"""
Utilitaires pour gérer les boutons et éviter les IDs dupliqués
"""

import streamlit as st
import hashlib

def create_unique_button(label, page_context="", **kwargs):
    """
    Crée un bouton avec une clé unique basée sur le label et le contexte
    
    Args:
        label (str): Texte du bouton
        page_context (str): Contexte de la page pour différencier
        **kwargs: Autres paramètres pour st.button
    
    Returns:
        bool: Résultat du clic sur le bouton
    """
    # Générer une clé unique
    unique_string = f"{page_context}_{label}_{str(kwargs)}"
    unique_key = hashlib.md5(unique_string.encode()).hexdigest()[:8]
    
    # Ajouter la clé aux kwargs
    kwargs['key'] = f"btn_{unique_key}"
    
    return st.button(label, **kwargs)

def create_unique_selectbox(label, options, page_context="", **kwargs):
    """
    Crée une selectbox avec une clé unique
    
    Args:
        label (str): Label de la selectbox
        options (list): Options disponibles
        page_context (str): Contexte de la page
        **kwargs: Autres paramètres pour st.selectbox
    
    Returns:
        Valeur sélectionnée
    """
    unique_string = f"{page_context}_{label}_{str(options)}"
    unique_key = hashlib.md5(unique_string.encode()).hexdigest()[:8]
    
    kwargs['key'] = f"select_{unique_key}"
    
    return st.selectbox(label, options, **kwargs)

def create_unique_text_input(label, page_context="", **kwargs):
    """
    Crée un text_input avec une clé unique
    
    Args:
        label (str): Label du champ
        page_context (str): Contexte de la page
        **kwargs: Autres paramètres pour st.text_input
    
    Returns:
        Valeur saisie
    """
    unique_string = f"{page_context}_{label}"
    unique_key = hashlib.md5(unique_string.encode()).hexdigest()[:8]
    
    kwargs['key'] = f"input_{unique_key}"
    
    return st.text_input(label, **kwargs)

def create_unique_number_input(label, page_context="", **kwargs):
    """
    Crée un number_input avec une clé unique
    
    Args:
        label (str): Label du champ
        page_context (str): Contexte de la page
        **kwargs: Autres paramètres pour st.number_input
    
    Returns:
        Valeur numérique saisie
    """
    unique_string = f"{page_context}_{label}"
    unique_key = hashlib.md5(unique_string.encode()).hexdigest()[:8]
    
    kwargs['key'] = f"num_{unique_key}"
    
    return st.number_input(label, **kwargs)

# Constantes pour les contextes de pages
class PageContext:
    HOME = "home"
    EXCEL_IMPORT = "excel_import"
    MANUAL_INPUT = "manual_input"
    ANALYSIS = "analysis"
    REPORTS = "reports"