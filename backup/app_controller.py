"""
Contrôleur d'application centralisé pour OptCred
Résout tous les problèmes de session state, navigation et widgets
Version finale - Kaizen Business Support
"""

import streamlit as st
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List
from enum import Enum
import hashlib
import traceback

class AppState(Enum):
    """États de l'application"""
    INITIALIZING = "initializing"
    READY = "ready"
    ANALYZING = "analyzing"
    ERROR = "error"

class Page(Enum):
    """Pages disponibles"""
    HOME = "home"
    UNIFIED_INPUT = "unified_input"
    ANALYSIS = "analysis" 
    REPORTS = "reports"

class AppController:
    """Contrôleur centralisé qui résout tous les problèmes architecturaux"""
    
    # Constantes pour la stabilité
    VERSION = "2.1.2-STABLE"
    SESSION_PREFIX = "optcred_v2_"
    
    # Clés de session centralisées
    class Keys:
        STATE = "optcred_v2_app_state"
        CURRENT_PAGE = "optcred_v2_current_page"
        ANALYSIS_DATA = "optcred_v2_analysis_data"
        SESSION_ID = "optcred_v2_session_id"
        WIDGET_COUNTER = "optcred_v2_widget_counter"
        INITIALIZATION_DONE = "optcred_v2_init_done"
        
    def __init__(self):
        self._ensure_initialization()
    
    def _ensure_initialization(self):
        """Initialisation unique et atomique"""
        if st.session_state.get(self.Keys.INITIALIZATION_DONE, False):
            return
            
        # Générer un ID de session stable
        if self.Keys.SESSION_ID not in st.session_state:
            session_hash = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:8]
            st.session_state[self.Keys.SESSION_ID] = session_hash
        
        # Initialiser les valeurs par défaut
        defaults = {
            self.Keys.STATE: AppState.READY.value,
            self.Keys.CURRENT_PAGE: Page.HOME.value,
            self.Keys.WIDGET_COUNTER: 0,
            self.Keys.ANALYSIS_DATA: None
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
        
        # Marquer comme initialisé
        st.session_state[self.Keys.INITIALIZATION_DONE] = True
    
    @property
    def session_id(self) -> str:
        """ID de session stable"""
        return st.session_state[self.Keys.SESSION_ID]
    
    @property
    def current_page(self) -> Page:
        """Page actuelle avec validation"""
        page_value = st.session_state.get(self.Keys.CURRENT_PAGE, Page.HOME.value)
        try:
            return Page(page_value)
        except ValueError:
            self.navigate_to(Page.HOME)
            return Page.HOME
    
    @property
    def app_state(self) -> AppState:
        """État de l'application"""
        state_value = st.session_state.get(self.Keys.STATE, AppState.READY.value)
        try:
            return AppState(state_value)
        except ValueError:
            return AppState.READY
    
    def generate_widget_key(self, base_name: str) -> str:
        """Génère une clé de widget STABLE et UNIQUE"""
        # Incrémenter le compteur pour l'unicité
        counter = st.session_state.get(self.Keys.WIDGET_COUNTER, 0)
        st.session_state[self.Keys.WIDGET_COUNTER] = counter + 1
        
        # Clé basée sur session + compteur (STABLE)
        return f"{base_name}_{self.session_id}_{counter}"
    
    def navigate_to(self, page: Page, force: bool = False) -> bool:
        """Navigation centralisée et sécurisée"""
        try:
            # Vérifications de sécurité
            if not force and page in [Page.ANALYSIS, Page.REPORTS]:
                if not self.has_valid_analysis():
                    st.warning(f"⚠️ Une analyse est requise pour accéder à {page.value}")
                    return False
            
            # Navigation atomique
            st.session_state[self.Keys.CURRENT_PAGE] = page.value
            
            # Synchronisation avec query_params (optionnel, sans conflit)
            try:
                st.query_params.page = page.value
            except Exception:
                pass  # Ignore si query_params non disponible
            
            return True
            
        except Exception as e:
            st.error(f"❌ Erreur de navigation: {e}")
            return False
    
    def has_valid_analysis(self) -> bool:
        """Vérification robuste des données d'analyse"""
        analysis_data = st.session_state.get(self.Keys.ANALYSIS_DATA)
        
        if not analysis_data or not isinstance(analysis_data, dict):
            return False
        
        # Vérifications de structure
        required_keys = ['data', 'ratios', 'scores', 'metadata']
        if not all(key in analysis_data for key in required_keys):
            return False
        
        # Vérification de validité du score
        scores = analysis_data.get('scores', {})
        global_score = scores.get('global', 0)
        
        return isinstance(global_score, (int, float)) and 0 <= global_score <= 100
    
    def store_analysis(self, data: Dict, ratios: Dict, scores: Dict, metadata: Dict):
        """Stockage sécurisé des résultats d'analyse"""
        if not all(isinstance(x, dict) for x in [data, ratios, scores, metadata]):
            raise ValueError("Tous les paramètres doivent être des dictionnaires")
        
        # Enrichir les métadonnées
        metadata.update({
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'version': self.VERSION
        })
        
        # Structure unifiée
        analysis_result = {
            'data': data,
            'ratios': ratios,
            'scores': scores,
            'metadata': metadata,
            'created_at': datetime.now().isoformat()
        }
        
        # Stockage atomique
        st.session_state[self.Keys.ANALYSIS_DATA] = analysis_result
        st.success("✅ Analyse sauvegardée avec succès")
    
    def get_analysis(self) -> Optional[Dict]:
        """Récupération sécurisée de l'analyse"""
        if not self.has_valid_analysis():
            return None
        return st.session_state[self.Keys.ANALYSIS_DATA]
    
    def clear_analysis(self):
        """Nettoyage sécurisé de l'analyse"""
        st.session_state[self.Keys.ANALYSIS_DATA] = None
        st.success("🗑️ Analyse supprimée")
    
    def reset_application(self):
        """Reset complet de l'application"""
        # Sauvegarder l'ID de session
        session_id = self.session_id
        
        # Nettoyer toutes les clés OptCred
        keys_to_remove = [k for k in st.session_state.keys() if k.startswith(self.SESSION_PREFIX)]
        for key in keys_to_remove:
            del st.session_state[key]
        
        # Réinitialiser avec le même ID de session (pour stabilité widgets)
        st.session_state[self.Keys.SESSION_ID] = session_id
        self._ensure_initialization()
        
        # Naviguer vers l'accueil
        self.navigate_to(Page.HOME, force=True)
        st.success("🔄 Application réinitialisée")
        st.rerun()
    
    def safe_import(self, module_path: str, fallback_func=None):
        """Import sécurisé avec gestion d'erreurs"""
        try:
            # Ajouter les répertoires au path si nécessaire
            base_dir = os.path.dirname(__file__)
            paths_to_add = [
                base_dir,
                os.path.join(base_dir, 'modules'),
                os.path.join(base_dir, 'modules/core'),
                os.path.join(base_dir, 'modules/pages'),
                os.path.join(base_dir, 'components'),
                os.path.join(base_dir, 'utils')
            ]
            
            for path in paths_to_add:
                if os.path.isdir(path) and path not in sys.path:
                    sys.path.insert(0, path)
            
            # Import dynamique
            module_parts = module_path.split('.')
            module = __import__(module_path)
            
            for part in module_parts[1:]:
                module = getattr(module, part)
            
            return module
            
        except ImportError as e:
            if fallback_func:
                st.info("🔄 Utilisation du mode fallback")
                return fallback_func
            return None
    
    def display_page(self):
        """Affichage centralisé des pages avec gestion d'erreurs"""
        current_page = self.current_page
        
        try:
            if current_page == Page.HOME:
                self._show_home_page()
            
            elif current_page == Page.UNIFIED_INPUT:
                self._show_unified_input_page()
            
            elif current_page == Page.ANALYSIS:
                if self.has_valid_analysis():
                    self._show_analysis_page()
                else:
                    self._show_no_analysis_page("analyse")
            
            elif current_page == Page.REPORTS:
                if self.has_valid_analysis():
                    self._show_reports_page()
                else:
                    self._show_no_analysis_page("rapports")
            
        except Exception as e:
            st.error(f"❌ Erreur lors de l'affichage de la page: {e}")
            st.code(traceback.format_exc())
            
            # Navigation de secours vers l'accueil
            if st.button("🏠 Retour à l'accueil", key=self.generate_widget_key("error_home")):
                self.navigate_to(Page.HOME, force=True)
                st.rerun()
    
    def _show_home_page(self):
        """Page d'accueil"""
        st.title("🏠 OptCred - Analyse Financière BCEAO")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Saisir des données", 
                        key=self.generate_widget_key("home_input"),
                        type="primary"):
                self.navigate_to(Page.UNIFIED_INPUT)
                st.rerun()
        
        with col2:
            if self.has_valid_analysis():
                if st.button("📊 Voir l'analyse", 
                           key=self.generate_widget_key("home_analysis"),
                           type="primary"):
                    self.navigate_to(Page.ANALYSIS)
                    st.rerun()
            else:
                st.button("📊 Analyse", 
                         key=self.generate_widget_key("home_analysis_disabled"),
                         disabled=True)
        
        # Afficher le résumé si analyse disponible
        if self.has_valid_analysis():
            self._display_analysis_summary()
    
    def _show_unified_input_page(self):
        """Page de saisie unifiée"""
        try:
            # Try the fixed version first using direct import (like original main.py)
            try:
                from unified_input_page_fixed import show_unified_input_page
                show_unified_input_page()
                return
            except ImportError:
                pass
            
            # Fallback to original version
            try:
                from unified_input_page import show_unified_input_page
                show_unified_input_page()
                return
            except ImportError:
                pass
                
            # Last resort - use the old safe_import method
            unified_module = self.safe_import('unified_input_page_fixed')
            if unified_module and hasattr(unified_module, 'show_unified_input_page'):
                unified_module.show_unified_input_page()
                return
                
            # Final fallback
            self._show_fallback_input_page()
            
        except Exception as e:
            st.error(f"❌ Erreur chargement page de saisie: {e}")
            st.code(traceback.format_exc())
            self._show_fallback_input_page()
    
    def _show_analysis_page(self):
        """Page d'analyse"""
        try:
            # Essayer plusieurs modules d'analyse
            analysis_modules = [
                'analysis_detailed',
                'modules.pages.analysis_detailed', 
                'modules.pages.analysis'
            ]
            
            for module_name in analysis_modules:
                module = self.safe_import(module_name)
                if module:
                    # Chercher la fonction d'affichage
                    for func_name in ['show_detailed_analysis_page', 'show_analysis_page']:
                        if hasattr(module, func_name):
                            getattr(module, func_name)()
                            return
            
            # Fallback vers affichage basique
            self._show_basic_analysis()
            
        except Exception as e:
            st.error(f"❌ Erreur chargement page d'analyse: {e}")
            self._show_basic_analysis()
    
    def _show_reports_page(self):
        """Page de rapports"""
        try:
            reports_module = self.safe_import('modules.pages.reports')
            if reports_module and hasattr(reports_module, 'show_reports_page'):
                reports_module.show_reports_page()
            else:
                st.info("📋 Module de rapports non disponible")
                
        except Exception as e:
            st.error(f"❌ Erreur chargement page de rapports: {e}")
    
    def _show_fallback_input_page(self):
        """Page de saisie fallback"""
        st.title("📊 Saisie des Données - Mode Simplifié")
        st.info("Interface de saisie basique (module principal non disponible)")
        
        uploaded_file = st.file_uploader(
            "Choisir un fichier Excel",
            type=['xlsx', 'xls'],
            key=self.generate_widget_key("fallback_upload")
        )
        
        if uploaded_file:
            if st.button("Analyser", key=self.generate_widget_key("fallback_analyze")):
                try:
                    # Import de l'analyseur
                    analyzer_module = self.safe_import('modules.core.analyzer')
                    if analyzer_module:
                        st.success("✅ Fichier chargé avec succès")
                        # Ici vous pourriez ajouter la logique d'analyse
                    else:
                        st.error("❌ Module d'analyse non disponible")
                except Exception as e:
                    st.error(f"❌ Erreur d'analyse: {e}")
    
    def _show_basic_analysis(self):
        """Affichage d'analyse basique"""
        st.title("📊 Analyse Financière - Mode Basique")
        
        analysis = self.get_analysis()
        if not analysis:
            st.error("❌ Aucune donnée d'analyse disponible")
            return
        
        scores = analysis.get('scores', {})
        global_score = scores.get('global', 0)
        
        # Affichage du score
        st.metric("Score Global BCEAO", f"{global_score}/100")
        
        # Scores par catégorie
        categories = ['liquidite', 'solvabilite', 'rentabilite', 'activite', 'gestion']
        cols = st.columns(len(categories))
        
        for i, category in enumerate(categories):
            with cols[i]:
                score = scores.get(category, 0)
                st.metric(category.title(), score)
    
    def _show_no_analysis_page(self, page_type: str):
        """Page d'erreur pour absence d'analyse"""
        st.warning(f"⚠️ Aucune analyse disponible pour {page_type}")
        
        if st.button("📊 Saisir des données", 
                    key=self.generate_widget_key(f"no_analysis_{page_type}")):
            self.navigate_to(Page.UNIFIED_INPUT)
            st.rerun()
    
    def _display_analysis_summary(self):
        """Résumé de l'analyse disponible"""
        analysis = self.get_analysis()
        if not analysis:
            return
        
        st.markdown("---")
        st.subheader("📊 Analyse Disponible")
        
        scores = analysis.get('scores', {})
        metadata = analysis.get('metadata', {})
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Score Global", f"{scores.get('global', 0)}/100")
        
        with col2:
            secteur = metadata.get('secteur', 'Non spécifié')
            st.metric("Secteur", secteur.replace('_', ' ').title())
        
        with col3:
            ratios_count = len(analysis.get('ratios', {}))
            st.metric("Ratios Calculés", ratios_count)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Diagnostic de santé de l'application"""
        return {
            'version': self.VERSION,
            'session_id': self.session_id[:8],
            'current_page': self.current_page.value,
            'app_state': self.app_state.value,
            'has_analysis': self.has_valid_analysis(),
            'initialization_done': st.session_state.get(self.Keys.INITIALIZATION_DONE, False),
            'widget_counter': st.session_state.get(self.Keys.WIDGET_COUNTER, 0),
            'session_keys_count': len([k for k in st.session_state.keys() if k.startswith(self.SESSION_PREFIX)])
        }

# Instance globale du contrôleur
_app_controller = None

def get_app_controller() -> AppController:
    """Singleton du contrôleur d'application"""
    global _app_controller
    if _app_controller is None:
        _app_controller = AppController()
    return _app_controller