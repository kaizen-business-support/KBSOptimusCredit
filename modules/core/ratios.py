"""
Calculateur de ratios financiers conforme aux normes BCEAO
"""

import numpy as np
from typing import Dict, Any, Optional

class RatiosCalculator:
    """Calculateur de tous les ratios financiers"""
    
    def __init__(self):
        self.epsilon = 1e-6  # Pour éviter les divisions par zéro
    
    def calculate_all_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
        """Calcule tous les ratios financiers"""
        ratios = {}
        
        # Ratios de liquidité
        ratios.update(self.calculate_liquidite_ratios(data))
        
        # Ratios de solvabilité
        ratios.update(self.calculate_solvabilite_ratios(data))
        
        # Ratios de rentabilité
        ratios.update(self.calculate_rentabilite_ratios(data))
        
        # Ratios d'activité
        ratios.update(self.calculate_activite_ratios(data))
        
        # Ratios de gestion
        ratios.update(self.calculate_gestion_ratios(data))
        
        # Ratios de structure
        ratios.update(self.calculate_structure_ratios(data))
        
        # Ratios BCEAO spécifiques
        ratios.update(self.calculate_bceao_ratios(data))
        
        return ratios
    
    def safe_divide(self, numerator: float, denominator: float, default: float = 0) -> float:
        """Division sécurisée pour éviter les erreurs"""
        if abs(denominator) < self.epsilon:
            return default
        return numerator / denominator
    
    def calculate_liquidite_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
        """Calcule les ratios de liquidité"""
        ratios = {}
        
        # Actif circulant total
        actif_circulant = (
            data.get('stocks', 0) + 
            data.get('creances_clients', 0) + 
            data.get('autres_creances', 0) + 
            data.get('tresorerie', 0)
        )
        
        # Actif liquide (sans stocks)
        actif_liquide = (
            data.get('creances_clients', 0) + 
            data.get('autres_creances', 0) + 
            data.get('tresorerie', 0)
        )
        
        dettes_ct = data.get('dettes_court_terme', 0)
        
        # Ratio de liquidité générale
        ratios['ratio_liquidite_generale'] = self.safe_divide(actif_circulant, dettes_ct, 0)
        
        # Ratio de liquidité immédiate (quick ratio)
        ratios['ratio_liquidite_immediate'] = self.safe_divide(actif_liquide, dettes_ct, 0)
        
        # Ratio de liquidité absolue
        ratios['ratio_liquidite_absolue'] = self.safe_divide(data.get('tresorerie', 0), dettes_ct, 0)
        
        # BFR et ratios associés
        bfr = self.calculate_bfr(data)
        ratios['bfr'] = bfr
        
        if data.get('chiffre_affaires', 0) > 0:
            ratios['bfr_jours_ca'] = (bfr / data['chiffre_affaires']) * 365
            ratios['bfr_pourcentage_ca'] = (bfr / data['chiffre_affaires']) * 100
        
        # Trésorerie nette
        tresorerie_nette = data.get('tresorerie', 0) - data.get('tresorerie_passif', 0)
        ratios['tresorerie_nette'] = tresorerie_nette
        
        return ratios
    
    def calculate_solvabilite_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
        """Calcule les ratios de solvabilité"""
        ratios = {}
        
        total_actif = data.get('total_actif', 0)
        capitaux_propres = data.get('capitaux_propres', 0)
        dettes_financieres = data.get('dettes_financieres', 0)
        dettes_ct = data.get('dettes_court_terme', 0)
        
        # Dettes totales
        dettes_totales = dettes_financieres + dettes_ct
        
        # Ratio d'autonomie financière
        ratios['ratio_autonomie_financiere'] = self.safe_divide(capitaux_propres, total_actif, 0) * 100
        
        # Ratio d'endettement global
        ratios['ratio_endettement'] = self.safe_divide(dettes_totales, total_actif, 0) * 100
        
        # Ratio d'endettement financier
        ratios['ratio_endettement_financier'] = self.safe_divide(dettes_financieres, capitaux_propres, 0)
        
        # Ratio de structure financière
        ratios['ratio_structure_financiere'] = self.safe_divide(dettes_financieres, dettes_totales, 0) * 100
        
        # Financement des immobilisations
        ressources_stables = data.get('ressources_stables', capitaux_propres + dettes_financieres)
        immobilisations = data.get('immobilisations_nettes', 0)
        ratios['financement_immobilisations'] = self.safe_divide(ressources_stables, immobilisations, 0) * 100
        
        # Capacité de remboursement
        cafg = data.get('cafg', 0)
        if cafg > 0:
            ratios['capacite_remboursement'] = self.safe_divide(dettes_financieres, cafg, 999)
        else:
            ratios['capacite_remboursement'] = 999
        
        # Couverture des charges financières
        ebe = data.get('excedent_brut', 0)
        frais_financiers = abs(data.get('frais_financiers', 0))
        ratios['couverture_charges_financieres'] = self.safe_divide(ebe, frais_financiers, 0)
        
        return ratios
    
    def calculate_rentabilite_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
        """Calcule les ratios de rentabilité"""
        ratios = {}
        
        total_actif = data.get('total_actif', 0)
        capitaux_propres = data.get('capitaux_propres', 0)
        chiffre_affaires = data.get('chiffre_affaires', 0)
        resultat_net = data.get('resultat_net', 0)
        resultat_exploitation = data.get('resultat_exploitation', 0)
        
        # ROA (Return on Assets)
        ratios['roa'] = self.safe_divide(resultat_net, total_actif, 0) * 100
        ratios['roa_exploitation'] = self.safe_divide(resultat_exploitation, total_actif, 0) * 100
        
        # ROE (Return on Equity)
        ratios['roe'] = self.safe_divide(resultat_net, capitaux_propres, 0) * 100
        ratios['roe_exploitation'] = self.safe_divide(resultat_exploitation, capitaux_propres, 0) * 100
        
        # Marges
        if chiffre_affaires > 0:
            ratios['marge_commerciale_pct'] = self.safe_divide(data.get('marge_commerciale', 0), chiffre_affaires, 0) * 100
            ratios['marge_valeur_ajoutee'] = self.safe_divide(data.get('valeur_ajoutee', 0), chiffre_affaires, 0) * 100
            ratios['marge_excedent_brut'] = self.safe_divide(data.get('excedent_brut', 0), chiffre_affaires, 0) * 100
            ratios['marge_exploitation'] = self.safe_divide(resultat_exploitation, chiffre_affaires, 0) * 100
            ratios['marge_nette'] = self.safe_divide(resultat_net, chiffre_affaires, 0) * 100
            
            # Marge brute (approximation)
            couts_directs = data.get('achats_matieres_premieres', 0) + data.get('autres_achats', 0)
            marge_brute_montant = chiffre_affaires - couts_directs
            ratios['marge_brute'] = self.safe_divide(marge_brute_montant, chiffre_affaires, 0) * 100
        
        # Coefficient d'exploitation
        charges_exploitation = data.get('charges_exploitation', 0)
        if chiffre_affaires > 0:
            ratios['coefficient_exploitation'] = self.safe_divide(charges_exploitation, chiffre_affaires, 0) * 100
        
        # Rentabilité économique
        resultat_economique = resultat_exploitation + abs(data.get('frais_financiers', 0))
        actif_economique = total_actif - data.get('tresorerie', 0)
        ratios['rentabilite_economique'] = self.safe_divide(resultat_economique, actif_economique, 0) * 100
        
        return ratios
    
    def calculate_activite_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
        """Calcule les ratios d'activité"""
        ratios = {}
        
        chiffre_affaires = data.get('chiffre_affaires', 0)
        total_actif = data.get('total_actif', 0)
        
        # Rotation de l'actif total
        ratios['rotation_actif'] = self.safe_divide(chiffre_affaires, total_actif, 0)
        
        # Rotation des immobilisations
        immobilisations = data.get('immobilisations_nettes', 0)
        ratios['rotation_immobilisations'] = self.safe_divide(chiffre_affaires, immobilisations, 0)
        
        # Rotation des stocks
        stocks = data.get('stocks', 0)
        if stocks > 0:
            ratios['rotation_stocks'] = self.safe_divide(chiffre_affaires, stocks, 0)
            ratios['duree_ecoulement_stocks'] = self.safe_divide(365, ratios['rotation_stocks'], 0)
        
        # Rotation des créances clients
        creances_clients = data.get('creances_clients', 0)
        if creances_clients > 0:
            ratios['rotation_creances'] = self.safe_divide(chiffre_affaires, creances_clients, 0)
            ratios['delai_recouvrement_clients'] = self.safe_divide(365, ratios['rotation_creances'], 0)
        
        # Rotation des fournisseurs
        fournisseurs = data.get('fournisseurs_exploitation', 0)
        achats_totaux = data.get('achats_matieres_premieres', 0) + data.get('autres_achats', 0)
        if fournisseurs > 0 and achats_totaux > 0:
            ratios['rotation_fournisseurs'] = self.safe_divide(achats_totaux, fournisseurs, 0)
            ratios['delai_paiement_fournisseurs'] = self.safe_divide(365, ratios['rotation_fournisseurs'], 0)
        
        # Vitesse de rotation du BFR
        bfr = self.calculate_bfr(data)
        if bfr > 0:
            ratios['rotation_bfr'] = self.safe_divide(chiffre_affaires, bfr, 0)
        
        return ratios
    
    def calculate_gestion_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
        """Calcule les ratios de gestion"""
        ratios = {}
        
        valeur_ajoutee = data.get('valeur_ajoutee', 0)
        charges_personnel = data.get('charges_personnel', 0)
        chiffre_affaires = data.get('chiffre_affaires', 0)
        
        # Productivité du personnel
        if charges_personnel > 0:
            ratios['productivite_personnel'] = self.safe_divide(valeur_ajoutee, charges_personnel, 0)
            
        if chiffre_affaires > 0:
            ratios['ca_par_employe'] = self.safe_divide(chiffre_affaires, charges_personnel, 0) * 50000  # Approximation
        
        # Taux de charges de personnel
        if valeur_ajoutee > 0:
            ratios['taux_charges_personnel'] = self.safe_divide(charges_personnel, valeur_ajoutee, 0) * 100
        
        # Intensité capitalistique
        immobilisations = data.get('immobilisations_nettes', 0)
        if charges_personnel > 0:
            ratios['intensite_capitalistique'] = self.safe_divide(immobilisations, charges_personnel, 0)
        
        # Ratios de flux de trésorerie
        cafg = data.get('cafg', 0)
        if chiffre_affaires > 0:
            ratios['ratio_cafg_ca'] = self.safe_divide(cafg, chiffre_affaires, 0) * 100
        
        if data.get('total_actif', 0) > 0:
            ratios['ratio_cafg_actif'] = self.safe_divide(cafg, data['total_actif'], 0) * 100
        
        # Efficacité opérationnelle
        ebe = data.get('excedent_brut', 0)
        if valeur_ajoutee > 0:
            ratios['taux_ebe_va'] = self.safe_divide(ebe, valeur_ajoutee, 0) * 100
        
        return ratios
    
    def calculate_structure_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
        """Calcule les ratios de structure"""
        ratios = {}
        
        # Fonds de roulement
        ressources_stables = data.get('ressources_stables', 
                                    data.get('capitaux_propres', 0) + data.get('dettes_financieres', 0))
        immobilisations = data.get('immobilisations_nettes', 0)
        fonds_roulement = ressources_stables - immobilisations
        ratios['fonds_roulement'] = fonds_roulement
        
        # Ratio de fonds de roulement
        if data.get('chiffre_affaires', 0) > 0:
            ratios['fonds_roulement_jours_ca'] = self.safe_divide(fonds_roulement, data['chiffre_affaires'], 0) * 365
        
        # Structure de l'actif
        total_actif = data.get('total_actif', 0)
        if total_actif > 0:
            ratios['pct_immobilisations'] = self.safe_divide(immobilisations, total_actif, 0) * 100
            ratios['pct_actif_circulant'] = self.safe_divide(data.get('total_actif_circulant', 0), total_actif, 0) * 100
            ratios['pct_tresorerie'] = self.safe_divide(data.get('tresorerie', 0), total_actif, 0) * 100
        
        # Structure du passif
        if total_actif > 0:
            ratios['pct_capitaux_propres'] = self.safe_divide(data.get('capitaux_propres', 0), total_actif, 0) * 100
            ratios['pct_dettes_financieres'] = self.safe_divide(data.get('dettes_financieres', 0), total_actif, 0) * 100
            ratios['pct_dettes_court_terme'] = self.safe_divide(data.get('dettes_court_terme', 0), total_actif, 0) * 100
        
        return ratios
    
    def calculate_bceao_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
        """Calcule les ratios spécifiques BCEAO (adaptation banques/entreprises)"""
        ratios = {}
        
        # Adaptation des ratios BCEAO pour les entreprises
        total_actif = data.get('total_actif', 0)
        capitaux_propres = data.get('capitaux_propres', 0)
        
        # Ratio de fonds propres de base (adapté)
        if total_actif > 0:
            ratios['ratio_fonds_propres_base'] = self.safe_divide(capitaux_propres, total_actif, 0) * 100
        
        # Ratio de couverture des emplois MLT
        ressources_stables = data.get('ressources_stables', capitaux_propres + data.get('dettes_financieres', 0))
        emplois_mlt = data.get('immobilisations_nettes', 0)
        ratios['coeff_couverture_emplois_mlt'] = self.safe_divide(ressources_stables, emplois_mlt, 0) * 100
        
        # Ratio de transformation (adapté)
        emplois_long_terme = emplois_mlt
        ressources_long_terme = ressources_stables
        ratios['ratio_transformation'] = self.safe_divide(emplois_long_terme, ressources_long_terme, 0) * 100
        
        # Indicateurs de qualité (adapté)
        creances_totales = data.get('creances_clients', 0) + data.get('autres_creances', 0)
        if creances_totales > 0:
            # Approximation des créances douteuses (si données disponibles)
            creances_douteuses = data.get('provisions_clients', 0)  # Si disponible
            ratios['taux_creances_douteuses'] = self.safe_divide(creances_douteuses, creances_totales, 0) * 100
        
        return ratios
    
    def calculate_bfr(self, data: Dict[str, float]) -> float:
        """Calcule le Besoin en Fonds de Roulement"""
        bfr_exploitation = (
            data.get('stocks', 0) + 
            data.get('creances_clients', 0) + 
            data.get('autres_creances', 0) + 
            data.get('fournisseurs_avances_versees', 0) -
            data.get('fournisseurs_exploitation', 0) - 
            data.get('dettes_sociales_fiscales', 0) - 
            data.get('autres_dettes', 0) -
            data.get('clients_avances_recues', 0)
        )
        return bfr_exploitation
    
    def get_ratio_interpretation(self, ratio_name: str, value: float, sector: str = None) -> Dict[str, str]:
        """Retourne l'interprétation d'un ratio"""
        interpretations = {
            'ratio_liquidite_generale': {
                'excellent': (2.0, float('inf')),
                'bon': (1.5, 2.0),
                'acceptable': (1.0, 1.5),
                'faible': (0, 1.0)
            },
            'ratio_autonomie_financiere': {
                'excellent': (50, 100),
                'bon': (30, 50),
                'acceptable': (20, 30),
                'faible': (0, 20)
            },
            'roe': {
                'excellent': (15, float('inf')),
                'bon': (10, 15),
                'acceptable': (5, 10),
                'faible': (-float('inf'), 5)
            },
            'marge_nette': {
                'excellent': (10, float('inf')),
                'bon': (5, 10),
                'acceptable': (2, 5),
                'faible': (-float('inf'), 2)
            }
        }
        
        if ratio_name not in interpretations:
            return {'level': 'unknown', 'description': 'Ratio non référencé'}
        
        ranges = interpretations[ratio_name]
        
        for level, (min_val, max_val) in ranges.items():
            if min_val <= value < max_val:
                return {
                    'level': level,
                    'description': f'{level.title()} ({value:.2f})',
                    'color': self._get_color_for_level(level)
                }
        
        return {'level': 'unknown', 'description': 'Valeur hors norme'}
    
    def _get_color_for_level(self, level: str) -> str:
        """Retourne la couleur associée au niveau de performance"""
        colors = {
            'excellent': '#22c55e',  # Vert
            'bon': '#3b82f6',        # Bleu
            'acceptable': '#f59e0b', # Orange
            'faible': '#ef4444',     # Rouge
            'unknown': '#6b7280'     # Gris
        }
        return colors.get(level, '#6b7280')
        