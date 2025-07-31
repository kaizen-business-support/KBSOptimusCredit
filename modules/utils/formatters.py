"""
Utilitaires de formatage pour l'application d'analyse financière
"""

def format_currency(value, currency="FCFA"):
    """Formate un montant en devise"""
    if value is None:
        return "0 " + currency
    try:
        return f"{float(value):,.0f} {currency}"
    except (ValueError, TypeError):
        return "0 " + currency

def format_percentage(value, decimals=1):
    """Formate un pourcentage"""
    if value is None:
        return "0.0%"
    try:
        return f"{float(value):.{decimals}f}%"
    except (ValueError, TypeError):
        return "0.0%"

def format_ratio(value, decimals=2):
    """Formate un ratio"""
    if value is None:
        return "0.00"
    try:
        return f"{float(value):.{decimals}f}"
    except (ValueError, TypeError):
        return "0.00"

def format_number(value, decimals=0):
    """Formate un nombre"""
    if value is None:
        return "0"
    try:
        if decimals == 0:
            return f"{float(value):,.0f}"
        else:
            return f"{float(value):,.{decimals}f}"
    except (ValueError, TypeError):
        return "0"

def get_status_indicator(value, threshold, higher_better=True):
    """Retourne un indicateur de statut (emoji)"""
    if value is None:
        return "⚪"
    
    try:
        val = float(value)
        thresh = float(threshold)
        
        if higher_better:
            if val >= thresh * 1.2:
                return "🟢"
            elif val >= thresh:
                return "🟡"
            else:
                return "🔴"
        else:
            if val <= thresh * 0.8:
                return "🟢"
            elif val <= thresh:
                return "🟡"
            else:
                return "🔴"
    except (ValueError, TypeError):
        return "⚪"

def get_performance_color(value, threshold, higher_better=True):
    """Retourne une couleur selon la performance"""
    if value is None:
        return "gray"
    
    try:
        val = float(value)
        thresh = float(threshold)
        
        if higher_better:
            if val >= thresh * 1.2:
                return "green"
            elif val >= thresh:
                return "orange"
            else:
                return "red"
        else:
            if val <= thresh * 0.8:
                return "green"
            elif val <= thresh:
                return "orange"
            else:
                return "red"
    except (ValueError, TypeError):
        return "gray"