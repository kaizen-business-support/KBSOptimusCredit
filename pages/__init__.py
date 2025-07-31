"""
Package des pages de l'application OptimusCredit
Dossier pages à la racine du projet
"""

# Import conditionnel des pages pour éviter les erreurs
try:
    from .excel_import import show_excel_import_page
except ImportError:
    show_excel_import_page = None

try:
    from .analysis import show_analysis_page
except ImportError:
    show_analysis_page = None

try:
    from .manual_input import show_manual_input_page
except ImportError:
    show_manual_input_page = None

try:
    from .reports import show_reports_page
except ImportError:
    show_reports_page = None

# Liste des fonctions exportées
__all__ = [
    'show_excel_import_page',
    'show_analysis_page',
    'show_manual_input_page', 
    'show_reports_page'
]

# Fonction utilitaire pour vérifier les pages disponibles
def get_available_pages():
    """Retourne la liste des pages disponibles"""
    available = {}
    
    if show_excel_import_page is not None:
        available['excel_import'] = show_excel_import_page
    
    if show_analysis_page is not None:
        available['analysis'] = show_analysis_page
    
    if show_manual_input_page is not None:
        available['manual_input'] = show_manual_input_page
    
    if show_reports_page is not None:
        available['reports'] = show_reports_page
    
    return available

# Information sur le package
__version__ = "2.1.0"
__author__ = "OptimusCredit Team"
__description__ = "Pages de l'application OptimusCredit - Analyse Financière BCEAO"