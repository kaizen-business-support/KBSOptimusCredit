"""
Composant de téléchargement de fichier STABLE
Résout définitivement les problèmes de reset des widgets d'upload
Version STABLE - Kaizen Business Support
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any, Callable
from datetime import datetime
import hashlib
import io

class StableFileUpload:
    """Composant d'upload de fichier avec persistance de session"""
    
    def __init__(self, session_key_prefix: str = "stable_upload"):
        self.prefix = session_key_prefix
        self._init_session_keys()
    
    def _init_session_keys(self):
        """Initialise les clés de session pour la persistance"""
        self.keys = {
            'file_content': f'{self.prefix}_file_content',
            'file_name': f'{self.prefix}_file_name',
            'file_type': f'{self.prefix}_file_type',
            'file_size': f'{self.prefix}_file_size',
            'upload_timestamp': f'{self.prefix}_upload_timestamp',
            'file_hash': f'{self.prefix}_file_hash',
            'processing_complete': f'{self.prefix}_processing_complete'
        }
    
    def render(self, 
               label: str = "Choisir un fichier",
               accepted_types: list = None,
               max_size_mb: int = 200,
               widget_key: str = None) -> Optional[Dict[str, Any]]:
        """
        Affiche le composant d'upload avec persistance
        
        Returns:
            Dict avec les informations du fichier ou None
        """
        
        if accepted_types is None:
            accepted_types = ['xlsx', 'xls', 'csv']
        
        # Vérifier si un fichier est déjà en session
        has_persisted_file = self._has_persisted_file()
        
        if has_persisted_file:
            return self._display_persisted_file()
        
        # Widget d'upload avec clé stable
        upload_key = widget_key or f"{self.prefix}_uploader"
        
        uploaded_file = st.file_uploader(
            label,
            type=accepted_types,
            key=upload_key,
            help=f"Formats acceptés: {', '.join(accepted_types)}. Taille max: {max_size_mb}MB"
        )
        
        if uploaded_file is not None:
            return self._process_uploaded_file(uploaded_file, max_size_mb)
        
        return None
    
    def _has_persisted_file(self) -> bool:
        """Vérifie si un fichier est déjà persisté en session"""
        return (
            self.keys['file_content'] in st.session_state and
            self.keys['file_name'] in st.session_state and
            st.session_state[self.keys['file_content']] is not None
        )
    
    def _display_persisted_file(self) -> Dict[str, Any]:
        """Affiche les informations du fichier persisté"""
        
        file_name = st.session_state[self.keys['file_name']]
        file_size = st.session_state.get(self.keys['file_size'], 0)
        upload_time = st.session_state.get(self.keys['upload_timestamp'], 'Inconnu')
        
        # Interface utilisateur pour le fichier persisté
        st.success(f"✅ Fichier chargé: **{file_name}**")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.info(f"📁 Taille: {file_size:,} octets | ⏰ Chargé: {upload_time}")
        
        with col2:
            if st.button("🔄 Remplacer", key=f"{self.prefix}_replace"):
                self.clear_persisted_file()
                st.rerun()
        
        with col3:
            if st.button("🗑️ Supprimer", key=f"{self.prefix}_delete"):
                self.clear_persisted_file()
                st.rerun()
        
        # Retourner les informations du fichier
        return {
            'content': st.session_state[self.keys['file_content']],
            'name': file_name,
            'type': st.session_state.get(self.keys['file_type'], ''),
            'size': file_size,
            'timestamp': upload_time,
            'hash': st.session_state.get(self.keys['file_hash'], '')
        }
    
    def _process_uploaded_file(self, uploaded_file, max_size_mb: int) -> Optional[Dict[str, Any]]:
        """Traite et persiste le fichier uploadé"""
        
        try:
            # Vérifications de sécurité
            file_size = len(uploaded_file.getvalue())
            max_size_bytes = max_size_mb * 1024 * 1024
            
            if file_size > max_size_bytes:
                st.error(f"❌ Fichier trop volumineux ({file_size:,} octets). Maximum: {max_size_mb}MB")
                return None
            
            # Lecture du contenu
            file_content = uploaded_file.getvalue()
            file_hash = hashlib.md5(file_content).hexdigest()
            
            # Vérifier si c'est le même fichier que précédemment
            if (self.keys['file_hash'] in st.session_state and 
                st.session_state[self.keys['file_hash']] == file_hash):
                st.info("ℹ️ Ce fichier est déjà chargé")
                return self._get_persisted_file_info()
            
            # Validation du format
            if not self._validate_file_format(uploaded_file, file_content):
                return None
            
            # Persistance en session
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            st.session_state[self.keys['file_content']] = file_content
            st.session_state[self.keys['file_name']] = uploaded_file.name
            st.session_state[self.keys['file_type']] = uploaded_file.type
            st.session_state[self.keys['file_size']] = file_size
            st.session_state[self.keys['upload_timestamp']] = timestamp
            st.session_state[self.keys['file_hash']] = file_hash
            st.session_state[self.keys['processing_complete']] = False
            
            st.success(f"✅ Fichier **{uploaded_file.name}** chargé avec succès!")
            
            return {
                'content': file_content,
                'name': uploaded_file.name,
                'type': uploaded_file.type,
                'size': file_size,
                'timestamp': timestamp,
                'hash': file_hash
            }
            
        except Exception as e:
            st.error(f"❌ Erreur lors du traitement du fichier: {e}")
            return None
    
    def _validate_file_format(self, uploaded_file, file_content: bytes) -> bool:
        """Valide le format du fichier"""
        
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        try:
            if file_extension in ['xlsx', 'xls']:
                # Tenter de lire le fichier Excel
                pd.read_excel(io.BytesIO(file_content), nrows=1)
                return True
                
            elif file_extension == 'csv':
                # Tenter de lire le fichier CSV
                pd.read_csv(io.BytesIO(file_content), nrows=1)
                return True
                
            else:
                st.error(f"❌ Format de fichier non supporté: {file_extension}")
                return False
                
        except Exception as e:
            st.error(f"❌ Fichier corrompu ou format invalide: {e}")
            return False
    
    def _get_persisted_file_info(self) -> Dict[str, Any]:
        """Récupère les informations du fichier persisté"""
        return {
            'content': st.session_state[self.keys['file_content']],
            'name': st.session_state[self.keys['file_name']],
            'type': st.session_state.get(self.keys['file_type'], ''),
            'size': st.session_state.get(self.keys['file_size'], 0),
            'timestamp': st.session_state.get(self.keys['upload_timestamp'], ''),
            'hash': st.session_state.get(self.keys['file_hash'], '')
        }
    
    def clear_persisted_file(self):
        """Nettoie le fichier persisté de la session"""
        for key in self.keys.values():
            if key in st.session_state:
                del st.session_state[key]
        
        st.success("🗑️ Fichier supprimé de la session")
    
    def is_processing_complete(self) -> bool:
        """Vérifie si le traitement du fichier est terminé"""
        return st.session_state.get(self.keys['processing_complete'], False)
    
    def mark_processing_complete(self):
        """Marque le traitement comme terminé"""
        st.session_state[self.keys['processing_complete']] = True
    
    def get_file_preview(self, max_rows: int = 5) -> Optional[pd.DataFrame]:
        """Génère un aperçu du fichier"""
        
        if not self._has_persisted_file():
            return None
        
        try:
            file_content = st.session_state[self.keys['file_content']]
            file_name = st.session_state[self.keys['file_name']]
            
            file_extension = file_name.lower().split('.')[-1]
            
            if file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(io.BytesIO(file_content), nrows=max_rows)
            elif file_extension == 'csv':
                df = pd.read_csv(io.BytesIO(file_content), nrows=max_rows)
            else:
                return None
            
            return df
            
        except Exception as e:
            st.error(f"❌ Erreur génération aperçu: {e}")
            return None
    
    def display_file_preview(self, max_rows: int = 5):
        """Affiche un aperçu du fichier"""
        
        preview_df = self.get_file_preview(max_rows)
        
        if preview_df is not None:
            st.subheader("👁️ Aperçu du fichier")
            st.dataframe(preview_df, use_container_width=True)
            
            if len(preview_df) == max_rows:
                st.caption(f"Affichage des {max_rows} premières lignes seulement")
        else:
            st.info("📄 Aperçu non disponible pour ce type de fichier")

# Fonction utilitaire pour usage simple
def create_stable_upload(session_prefix: str = "main_upload") -> StableFileUpload:
    """Crée une instance de StableFileUpload"""
    return StableFileUpload(session_prefix)