"""
Gestionnaire d'état centralisé pour l'application OptimusCredit - VERSION 1.0
Ce module garantit la cohérence des données entre toutes les pages
"""

import streamlit as st
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

class SessionManager:
    """Gestionnaire centralisé pour l'état de session de l'application"""
    
    # Clés standardisées pour l'état de session
    ANALYSIS_RESULTS = 'analysis_results'
    CURRENT_PAGE = 'current_page'
    RESET_COUNTER = 'reset_counter'
    
    @staticmethod
    def initialize():
        """Initialise l'état de session avec les valeurs par défaut"""
        if SessionManager.CURRENT_PAGE not in st.session_state:
            st.session_state[SessionManager.CURRENT_PAGE] = 'home'
        
        if SessionManager.RESET_COUNTER not in st.session_state:
            st.session_state[SessionManager.RESET_COUNTER] = 0
    
    @staticmethod
    def has_analysis_data() -> bool:
        """Vérifie si des données d'analyse valides existent"""
        if SessionManager.ANALYSIS_RESULTS not in st.session_state:
            return False
        
        analysis_results = st.session_state[SessionManager.ANALYSIS_RESULTS]
        
        # Vérifier la structure complète
        required_keys = ['data', 'ratios', 'scores', 'metadata']
        if not all(key in analysis_results for key in required_keys):
            return False
        
        # Vérifier que les scores sont valides
        scores = analysis_results.get('scores', {})
        if not isinstance(scores, dict) or 'global' not in scores:
            return False
        
        # Vérifier que les ratios existent
        ratios = analysis_results.get('ratios', {})
        if not isinstance(ratios, dict) or len(ratios) == 0:
            return False
        
        return True
    
    @staticmethod
    def get_analysis_info() -> Tuple[int, Dict[str, Any]]:
        """Récupère les informations d'analyse actuelles"""
        if not SessionManager.has_analysis_data():
            return 0, {}
        
        analysis_results = st.session_state[SessionManager.ANALYSIS_RESULTS]
        score = analysis_results['scores'].get('global', 0)
        metadata = analysis_results.get('metadata', {})
        
        return score, metadata
    
    @staticmethod
    def get_analysis_data() -> Optional[Dict[str, Any]]:
        """Récupère toutes les données d'analyse"""
        if not SessionManager.has_analysis_data():
            return None
        
        return st.session_state[SessionManager.ANALYSIS_RESULTS]
    
    @staticmethod
    def store_analysis_results(data: Dict[str, Any], ratios: Dict[str, Any], 
                             scores: Dict[str, Any], metadata: Dict[str, Any]):
        """Stocke les résultats d'analyse de manière unifiée"""
        
        # Ajouter timestamp si pas présent
        if 'date_analyse' not in metadata:
            metadata['date_analyse'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Ajouter compteur de ratios
        metadata['ratios_count'] = len(ratios)
        
        # Structure unifiée
        analysis_results = {
            'data': data,
            'ratios': ratios,
            'scores': scores,
            'metadata': metadata,
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        }
        
        # CORRECTION: Stocker directement sans nettoyer d'abord
        st.session_state[SessionManager.ANALYSIS_RESULTS] = analysis_results
        
        # Marquer l'analyse comme terminée
        st.session_state['analysis_completed'] = True
    
    @staticmethod
    def clear_analysis_data():
        """Nettoie toutes les données d'analyse"""
        
        # Liste des clés d'analyse à supprimer
        analysis_keys = [
            SessionManager.ANALYSIS_RESULTS,
            'analysis_completed',
            'uploaded_file_content',
            'uploaded_file_name',
            'uploaded_file_type',
            'analysis_in_progress',
            'show_sectoral',
            'show_charts'
        ]
        
        # Supprimer toutes les clés d'analyse
        for key in analysis_keys:
            if key in st.session_state:
                del st.session_state[key]
    
    @staticmethod
    def reset_application():
        """Réinitialise complètement l'application"""
        
        # Incrémenter le compteur de reset
        old_counter = st.session_state.get(SessionManager.RESET_COUNTER, 0)
        st.session_state[SessionManager.RESET_COUNTER] = old_counter + 1
        
        # Nettoyer toutes les données d'analyse
        SessionManager.clear_analysis_data()
        
        # Marquer qu'un reset complet a eu lieu
        st.session_state['complete_reset'] = True
        
        # Retourner à la page d'import
        st.session_state[SessionManager.CURRENT_PAGE] = 'excel_import'
    
    @staticmethod
    def get_current_page() -> str:
        """Récupère la page actuelle"""
        return st.session_state.get(SessionManager.CURRENT_PAGE, 'home')
    
    @staticmethod
    def set_current_page(page: str):
        """Définit la page actuelle"""
        st.session_state[SessionManager.CURRENT_PAGE] = page
    
    @staticmethod
    def get_reset_counter() -> int:
        """Récupère le compteur de reset pour les widgets"""
        return st.session_state.get(SessionManager.RESET_COUNTER, 0)
    
    @staticmethod
    def get_financial_class(score: int) -> str:
        """Retourne la classe financière selon le score BCEAO"""
        if score >= 85:
            return "A+"
        elif score >= 70:
            return "A"
        elif score >= 55:
            return "B"
        elif score >= 40:
            return "C"
        elif score >= 25:
            return "D"
        else:
            return "E"
    
    @staticmethod
    def get_interpretation(score: int) -> Tuple[str, str]:
        """Retourne l'interprétation du score avec couleur"""
        if score >= 85:
            return "Excellence financière", "green"
        elif score >= 70:
            return "Très bonne situation", "green"
        elif score >= 55:
            return "Bonne situation", "orange"
        elif score >= 40:
            return "Situation moyenne", "orange"
        elif score >= 25:
            return "Situation faible", "red"
        else:
            return "Situation très faible", "red"


# Fonctions utilitaires simplifiées
def init_session():
    """Fonction d'initialisation simple à appeler dans main.py"""
    SessionManager.initialize()

def has_analysis() -> bool:
    """Fonction simple pour vérifier la présence d'analyse"""
    return SessionManager.has_analysis_data()

def get_analysis():
    """Fonction simple pour récupérer l'analyse"""
    return SessionManager.get_analysis_data()

def clear_analysis():
    """Fonction simple pour nettoyer l'analyse"""
    SessionManager.clear_analysis_data()

def reset_app():
    """Fonction simple pour réinitialiser l'app"""
    SessionManager.reset_application()

def store_analysis(data, ratios, scores, metadata):
    """Fonction simple pour stocker l'analyse"""
    SessionManager.store_analysis_results(data, ratios, scores, metadata)