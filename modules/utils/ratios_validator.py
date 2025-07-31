"""
Module de validation des ratios financiers selon les normes BCEAO
"""

def validate_ratio_status(ratio_key: str, value: float) -> str:
    """
    Détermine le statut d'un ratio selon les normes BCEAO
    
    Args:
        ratio_key (str): Nom du ratio
        value (float): Valeur du ratio
    
    Returns:
        str: Statut du ratio ("✅ Conforme", "❌ Non conforme", "⚠️ Limite", "ℹ️ À analyser")
    """
    
    # Normes BCEAO par ratio
    ratio_norms = {
        # === LIQUIDITÉ ===
        'ratio_liquidite_generale': {
            'operator': '>=',
            'target': 1.5,
            'warning': 1.2,  # Seuil d'alerte
            'description': 'Liquidité Générale ≥ 1,5'
        },
        'ratio_liquidite_reduite': {
            'operator': '>=',
            'target': 1.0,
            'warning': 0.8,
            'description': 'Liquidité Réduite ≥ 1,0'
        },
        'ratio_liquidite_immediate': {
            'operator': '>=',
            'target': 0.3,
            'warning': 0.2,
            'description': 'Liquidité Immédiate ≥ 0,3'
        },
        
        # === STRUCTURE FINANCIÈRE ===
        'ratio_autonomie_financiere': {
            'operator': '>=',
            'target': 30.0,
            'warning': 25.0,
            'description': 'Autonomie Financière ≥ 30%'
        },
        'ratio_endettement': {
            'operator': '<=',
            'target': 70.0,
            'warning': 75.0,
            'description': 'Taux d\'Endettement ≤ 70%'
        },
        'ratio_couverture_charges': {
            'operator': '>=',
            'target': 3.0,
            'warning': 2.5,
            'description': 'Couverture Charges Financières ≥ 3,0'
        },
        
        # === RENTABILITÉ ===
        'roe': {
            'operator': '>=',
            'target': 10.0,
            'warning': 5.0,
            'description': 'ROE ≥ 10%'
        },
        'roa': {
            'operator': '>=',
            'target': 5.0,
            'warning': 2.0,
            'description': 'ROA ≥ 5%'
        },
        'marge_nette': {
            'operator': '>',
            'target': 5.0,
            'warning': 3.0,
            'description': 'Marge Nette > 5%'
        },
        'marge_brute': {
            'operator': '>=',
            'target': 20.0,
            'warning': 15.0,
            'description': 'Marge Brute ≥ 20%'
        },
        'marge_exploitation': {
            'operator': '>=',
            'target': 5.0,
            'warning': 3.0,
            'description': 'Marge d\'Exploitation ≥ 5%'
        },
        
        # === ACTIVITÉ ===
        'rotation_actif': {
            'operator': '>=',
            'target': 1.5,
            'warning': 1.0,
            'description': 'Rotation de l\'Actif ≥ 1,5'
        },
        'rotation_stocks': {
            'operator': '>=',
            'target': 6.0,
            'warning': 4.0,
            'description': 'Rotation des Stocks ≥ 6'
        },
        'delai_recouvrement': {
            'operator': '<=',
            'target': 45.0,
            'warning': 60.0,
            'description': 'Délai Recouvrement ≤ 45 jours'
        },
        
        # === GESTION ===
        'productivite_personnel': {
            'operator': '>=',
            'target': 2.0,
            'warning': 1.5,
            'description': 'Productivité Personnel ≥ 2,0'
        },
        'charges_personnel_va': {
            'operator': '<=',
            'target': 50.0,
            'warning': 60.0,
            'description': 'Charges Personnel/VA ≤ 50%'
        },
        'cafg_ca': {
            'operator': '>=',
            'target': 7.0,
            'warning': 5.0,
            'description': 'CAFG/CA ≥ 7%'
        }
    }
    
    # Vérifier si le ratio est connu
    if ratio_key not in ratio_norms:
        return "ℹ️ À analyser"
    
    norm = ratio_norms[ratio_key]
    operator = norm['operator']
    target = norm['target']
    warning = norm.get('warning')
    
    try:
        # Évaluer selon l'opérateur
        if operator == '>=':
            if value >= target:
                return "✅ Conforme"
            elif warning and value >= warning:
                return "⚠️ Limite"
            else:
                return "❌ Non conforme"
        
        elif operator == '>':
            if value > target:
                return "✅ Conforme"
            elif warning and value > warning:
                return "⚠️ Limite"
            else:
                return "❌ Non conforme"
        
        elif operator == '<=':
            if value <= target:
                return "✅ Conforme"
            elif warning and value <= warning:
                return "⚠️ Limite"
            else:
                return "❌ Non conforme"
        
        elif operator == '<':
            if value < target:
                return "✅ Conforme"
            elif warning and value < warning:
                return "⚠️ Limite"
            else:
                return "❌ Non conforme"
        
        else:
            return "ℹ️ À analyser"
    
    except (ValueError, TypeError):
        return "ℹ️ À analyser"

def get_ratio_norm_description(ratio_key: str) -> str:
    """Retourne la description de la norme pour un ratio"""
    
    ratio_norms = {
        'ratio_liquidite_generale': '> 1,5',
        'ratio_liquidite_reduite': '> 1,0',
        'ratio_liquidite_immediate': '> 0,3',
        'ratio_autonomie_financiere': '> 30%',
        'ratio_endettement': '< 70%',
        'ratio_couverture_charges': '> 3,0',
        'roe': '> 10%',
        'roa': '> 5%',
        'marge_nette': '> 5%',
        'marge_brute': '> 20%',
        'marge_exploitation': '> 5%',
        'rotation_actif': '> 1,5',
        'rotation_stocks': '> 6',
        'delai_recouvrement': '< 45 jours',
        'productivite_personnel': '> 2,0',
        'charges_personnel_va': '< 50%',
        'cafg_ca': '> 7%'
    }
    
    return ratio_norms.get(ratio_key, 'Non définie')

def get_ratio_category(ratio_key: str) -> str:
    """Retourne la catégorie d'un ratio"""
    
    categories = {
        'liquidite': ['ratio_liquidite_generale', 'ratio_liquidite_reduite', 'ratio_liquidite_immediate'],
        'structure_financiere': ['ratio_autonomie_financiere', 'ratio_endettement', 'ratio_couverture_charges'],
        'rentabilite': ['roe', 'roa', 'marge_nette', 'marge_brute', 'marge_exploitation'],
        'activite': ['rotation_actif', 'rotation_stocks', 'delai_recouvrement'],
        'gestion': ['productivite_personnel', 'charges_personnel_va', 'cafg_ca']
    }
    
    for category, ratios in categories.items():
        if ratio_key in ratios:
            return category
    
    return 'autre'

def validate_all_ratios(ratios: dict) -> dict:
    """Valide tous les ratios et retourne un rapport complet"""
    
    validation_report = {
        'conformes': [],
        'non_conformes': [],
        'limites': [],
        'a_analyser': [],
        'total': len(ratios),
        'taux_conformite': 0.0
    }
    
    for ratio_key, value in ratios.items():
        status = validate_ratio_status(ratio_key, value)
        
        ratio_info = {
            'ratio': ratio_key,
            'value': value,
            'status': status,
            'norm': get_ratio_norm_description(ratio_key),
            'category': get_ratio_category(ratio_key)
        }
        
        if status == "✅ Conforme":
            validation_report['conformes'].append(ratio_info)
        elif status == "❌ Non conforme":
            validation_report['non_conformes'].append(ratio_info)
        elif status == "⚠️ Limite":
            validation_report['limites'].append(ratio_info)
        else:
            validation_report['a_analyser'].append(ratio_info)
    
    # Calculer le taux de conformité
    nb_conformes = len(validation_report['conformes'])
    if validation_report['total'] > 0:
        validation_report['taux_conformite'] = (nb_conformes / validation_report['total']) * 100
    
    return validation_report