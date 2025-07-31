"""
Gestionnaire d'imports robuste pour l'application OptCred
Résout définitivement les problèmes d'import entre modules
Version STABLE - Kaizen Business Support
"""

import sys
import os
import importlib
import importlib.util
from typing import Any, Optional, List, Dict, Callable
import streamlit as st
from pathlib import Path

class ImportManager:
    """Gestionnaire centralisé des imports avec fallbacks"""
    
    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.path.dirname(os.path.dirname(__file__))
        self.module_cache = {}
        self.failed_imports = set()
        self._setup_paths()
    
    def _setup_paths(self):
        """Configure les chemins d'import"""
        paths_to_add = [
            self.base_dir,
            os.path.join(self.base_dir, 'modules'),
            os.path.join(self.base_dir, 'modules', 'core'),
            os.path.join(self.base_dir, 'modules', 'pages'),
            os.path.join(self.base_dir, 'modules', 'components'),
            os.path.join(self.base_dir, 'modules', 'utils'),
            os.path.join(self.base_dir, 'components'),
            os.path.join(self.base_dir, 'utils')
        ]
        
        for path in paths_to_add:
            if os.path.isdir(path) and path not in sys.path:
                sys.path.insert(0, path)
    
    def safe_import(self, 
                   module_name: str, 
                   fallback_paths: List[str] = None,
                   required_attributes: List[str] = None) -> Optional[Any]:
        """
        Import sécurisé avec gestion d'erreurs et fallbacks
        
        Args:
            module_name: Nom du module à importer
            fallback_paths: Chemins alternatifs à essayer
            required_attributes: Attributs requis dans le module
        
        Returns:
            Module importé ou None si échec
        """
        
        # Vérifier le cache
        cache_key = f"{module_name}_{hash(str(fallback_paths))}"
        if cache_key in self.module_cache:
            return self.module_cache[cache_key]
        
        # Si déjà échoué, ne pas réessayer
        if module_name in self.failed_imports:
            return None
        
        # Liste des tentatives d'import
        import_attempts = [module_name]
        if fallback_paths:
            import_attempts.extend(fallback_paths)
        
        for attempt in import_attempts:
            try:
                module = self._attempt_import(attempt)
                if module:
                    # Vérifier les attributs requis
                    if required_attributes:
                        if not all(hasattr(module, attr) for attr in required_attributes):
                            continue
                    
                    # Mise en cache et retour
                    self.module_cache[cache_key] = module
                    return module
                    
            except Exception as e:
                st.warning(f"⚠️ Échec import {attempt}: {e}")
                continue
        
        # Échec complet
        self.failed_imports.add(module_name)
        st.error(f"❌ Impossible d'importer {module_name}")
        return None
    
    def _attempt_import(self, module_path: str) -> Optional[Any]:
        """Tentative d'import d'un module"""
        
        try:
            # Import direct
            if '.' in module_path:
                module = importlib.import_module(module_path)
            else:
                # Import simple
                module = __import__(module_path)
            
            return module
            
        except ImportError:
            # Essayer import par fichier
            return self._import_by_file(module_path)
    
    def _import_by_file(self, module_name: str) -> Optional[Any]:
        """Import par fichier direct"""
        
        # Chercher le fichier dans les répertoires connus
        search_dirs = [
            self.base_dir,
            os.path.join(self.base_dir, 'modules'),
            os.path.join(self.base_dir, 'modules', 'pages'),
            os.path.join(self.base_dir, 'modules', 'core'),
            os.path.join(self.base_dir, 'components')
        ]
        
        for search_dir in search_dirs:
            file_path = os.path.join(search_dir, f"{module_name}.py")
            if os.path.isfile(file_path):
                return self._load_module_from_file(file_path, module_name)
        
        return None
    
    def _load_module_from_file(self, file_path: str, module_name: str) -> Optional[Any]:
        """Charge un module depuis un fichier"""
        
        try:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module
        except Exception as e:
            st.error(f"❌ Erreur chargement {file_path}: {e}")
        
        return None
    
    def get_available_modules(self) -> Dict[str, List[str]]:
        """Retourne la liste des modules disponibles par répertoire"""
        
        available = {}
        
        search_dirs = {
            'root': self.base_dir,
            'modules': os.path.join(self.base_dir, 'modules'),
            'pages': os.path.join(self.base_dir, 'modules', 'pages'),
            'core': os.path.join(self.base_dir, 'modules', 'core'),
            'components': os.path.join(self.base_dir, 'components')
        }
        
        for dir_name, dir_path in search_dirs.items():
            if os.path.isdir(dir_path):
                py_files = [f[:-3] for f in os.listdir(dir_path) 
                           if f.endswith('.py') and f != '__init__.py']
                available[dir_name] = py_files
        
        return available
    
    def import_with_fallback(self, 
                           primary_module: str,
                           fallback_function: Callable = None) -> Any:
        """
        Import avec fonction de fallback
        
        Args:
            primary_module: Module principal à importer
            fallback_function: Fonction à exécuter si import échoue
        
        Returns:
            Module importé ou résultat de la fonction fallback
        """
        
        module = self.safe_import(primary_module)
        
        if module:
            return module
        elif fallback_function:
            st.info(f"🔄 Utilisation du fallback pour {primary_module}")
            return fallback_function
        else:
            return None
    
    def validate_module_dependencies(self, module_name: str) -> Dict[str, bool]:
        """Valide les dépendances d'un module"""
        
        dependencies = {
            'streamlit': True,  # Toujours présent
            'pandas': self._check_import('pandas'),
            'numpy': self._check_import('numpy'),
            'openpyxl': self._check_import('openpyxl'),
            'plotly': self._check_import('plotly')
        }
        
        return dependencies
    
    def _check_import(self, module_name: str) -> bool:
        """Vérifie si un module peut être importé"""
        try:
            importlib.import_module(module_name)
            return True
        except ImportError:
            return False
    
    def clear_cache(self):
        """Vide le cache des modules"""
        self.module_cache.clear()
        self.failed_imports.clear()
        st.success("🗑️ Cache des imports vidé")
    
    def get_import_diagnostics(self) -> Dict[str, Any]:
        """Diagnostic des imports"""
        
        return {
            'cached_modules': len(self.module_cache),
            'failed_imports': len(self.failed_imports),
            'failed_modules': list(self.failed_imports),
            'available_modules': self.get_available_modules(),
            'dependencies': self.validate_module_dependencies('main'),
            'sys_path_count': len(sys.path)
        }

# Instance globale
_import_manager = None

def get_import_manager() -> ImportManager:
    """Singleton du gestionnaire d'imports"""
    global _import_manager
    if _import_manager is None:
        _import_manager = ImportManager()
    return _import_manager

# API simplifiée
def safe_import(module_name: str, fallback_paths: List[str] = None) -> Optional[Any]:
    """Import sécurisé simplifié"""
    return get_import_manager().safe_import(module_name, fallback_paths)

def import_with_fallback(primary: str, fallback_func: Callable = None) -> Any:
    """Import avec fallback simplifié"""
    return get_import_manager().import_with_fallback(primary, fallback_func)