"""
Analyseur financier complet conforme aux normes BCEAO
"""

import pandas as pd
import numpy as np
import openpyxl
from datetime import datetime
import json

class FinancialAnalyzer:
    def __init__(self):
        self.ratios_bceao = {
            'solvabilite': {
                'ratio_fonds_propres_base': {'min': 5.0, 'objectif': 7.0, 'poids': 0.25},
                'ratio_fonds_propres_tier1': {'min': 6.625, 'objectif': 8.5, 'poids': 0.20},
                'ratio_solvabilite_global': {'min': 8.625, 'objectif': 11.5, 'poids': 0.30},
                'coussin_conservation': {'min': 2.5, 'objectif': 2.5, 'poids': 0.15},
                'coussin_contracyclique': {'min': 0.0, 'objectif': 2.5, 'poids': 0.10}
            },
            'liquidite': {
                'ratio_liquidite_court_terme': {'min': 75.0, 'objectif': 100.0, 'poids': 0.40},
                'coeff_couverture_emplois_mlt': {'min': 100.0, 'objectif': 120.0, 'poids': 0.35},
                'ratio_transformation': {'max': 100.0, 'objectif': 80.0, 'poids': 0.25}
            },
            'division_risques': {
                'ratio_division_risques': {'max': 65.0, 'objectif': 50.0, 'poids': 0.40},
                'limite_grands_risques': {'max': 8.0, 'objectif': 6.0, 'poids': 0.35},
                'engagements_apparentes': {'max': 20.0, 'objectif': 15.0, 'poids': 0.25}
            },
            'qualite_portefeuille': {
                'taux_creances_douteuses': {'max': 5.0, 'objectif': 3.0, 'poids': 0.40},
                'taux_provisionnement': {'min': 80.0, 'objectif': 100.0, 'poids': 0.35},
                'taux_creances_irrecouvrables': {'max': 2.0, 'objectif': 1.0, 'poids': 0.25}
            },
            'rentabilite': {
                'roa': {'min': 1.0, 'objectif': 2.0, 'poids': 0.25},
                'roe': {'min': 10.0, 'objectif': 15.0, 'poids': 0.25},
                'coefficient_exploitation': {'max': 65.0, 'objectif': 55.0, 'poids': 0.30},
                'marge_nette': {'min': 10.0, 'objectif': 15.0, 'poids': 0.20}
            }
        }
        
        # Ratios sectoriels basés sur les documents
        self.ratios_sectoriels = {
            'industrie_manufacturiere': {
                'ratio_liquidite_generale': {'q1': 1.2, 'median': 1.8, 'q3': 2.5},
                'ratio_liquidite_immediate': {'q1': 0.6, 'median': 0.9, 'q3': 1.3},
                'rotation_stocks': {'q1': 4.5, 'median': 6.8, 'q3': 10.2},
                'marge_brute': {'q1': 18, 'median': 25, 'q3': 35},
                'marge_nette': {'q1': 2, 'median': 4.5, 'q3': 8},
                'roe': {'q1': 8, 'median': 15, 'q3': 22}
            },
            'commerce_detail': {
                'ratio_liquidite_generale': {'q1': 1.0, 'median': 1.5, 'q3': 2.2},
                'rotation_stocks': {'q1': 4.0, 'median': 6.5, 'q3': 12.0},
                'marge_brute': {'q1': 20, 'median': 28, 'q3': 38},
                'marge_nette': {'q1': 0.5, 'median': 2, 'q3': 4},
                'roe': {'q1': 5, 'median': 12, 'q3': 20}
            },
            'services_professionnels': {
                'ratio_liquidite_generale': {'q1': 1.2, 'median': 1.7, 'q3': 2.5},
                'marge_brute': {'q1': 40, 'median': 55, 'q3': 70},
                'marge_nette': {'q1': 5, 'median': 10, 'q3': 18},
                'roe': {'q1': 15, 'median': 25, 'q3': 40}
            },
            'construction_btp': {
                'ratio_liquidite_generale': {'q1': 1.2, 'median': 1.5, 'q3': 1.9},
                'rotation_stocks': {'q1': 8, 'median': 15, 'q3': 25},
                'marge_brute': {'q1': 15, 'median': 22, 'q3': 30},
                'marge_nette': {'q1': 1.5, 'median': 3.5, 'q3': 6},
                'roe': {'q1': 8, 'median': 16, 'q3': 28}
            },
            'agriculture': {
                'ratio_liquidite_generale': {'q1': 1.1, 'median': 1.6, 'q3': 2.3},
                'rotation_stocks': {'q1': 1.5, 'median': 2.5, 'q3': 4.0},
                'marge_brute': {'q1': 10, 'median': 20, 'q3': 35},
                'marge_nette': {'q1': -5, 'median': 2, 'q3': 8},
                'roe': {'q1': 2, 'median': 8, 'q3': 15}
            },
            'commerce_gros': {
                'ratio_liquidite_generale': {'q1': 1.1, 'median': 1.4, 'q3': 1.8},
                'rotation_stocks': {'q1': 6, 'median': 10, 'q3': 18},
                'marge_brute': {'q1': 8, 'median': 15, 'q3': 25},
                'marge_nette': {'q1': 0.5, 'median': 1.5, 'q3': 3}
            }
        }

    def load_excel_template(self, file_path):
        """Charge le modèle Excel avec tous les détails des états financiers"""
        try:
            workbook = openpyxl.load_workbook(file_path, data_only=True)
            
            # Extraction détaillée du bilan
            bilan_sheet = workbook['Bilan']
            
            # ACTIFS DÉTAILLÉS
            # Immobilisations incorporelles
            frais_dev_prospection = self.get_cell_value(bilan_sheet, 'E6')
            brevets_licences = self.get_cell_value(bilan_sheet, 'E7')
            fond_commercial = self.get_cell_value(bilan_sheet, 'E8')
            autres_immob_incorp = self.get_cell_value(bilan_sheet, 'E9')
            
            # Immobilisations corporelles
            terrains = self.get_cell_value(bilan_sheet, 'E11')
            batiments = self.get_cell_value(bilan_sheet, 'E12')
            agencements = self.get_cell_value(bilan_sheet, 'E13')
            materiel_mobilier = self.get_cell_value(bilan_sheet, 'E14')
            materiel_transport = self.get_cell_value(bilan_sheet, 'E15')
            avances_immobilisations = self.get_cell_value(bilan_sheet, 'E16')
            
            # Immobilisations financières
            titres_participation = self.get_cell_value(bilan_sheet, 'E19')
            autres_immob_financieres = self.get_cell_value(bilan_sheet, 'E20')
            
            # Totaux immobilisations
            total_actif_immobilise = self.get_cell_value(bilan_sheet, 'E21')
            
            # Actif circulant
            actif_circulant_hao = self.get_cell_value(bilan_sheet, 'E22')
            stocks_et_encours = self.get_cell_value(bilan_sheet, 'E23')
            fournisseurs_avances = self.get_cell_value(bilan_sheet, 'E25')
            clients = self.get_cell_value(bilan_sheet, 'E26')
            autres_creances = self.get_cell_value(bilan_sheet, 'E27')
            total_actif_circulant = self.get_cell_value(bilan_sheet, 'E28')
            
            # Trésorerie actif
            titres_placement = self.get_cell_value(bilan_sheet, 'E30')
            valeurs_encaisser = self.get_cell_value(bilan_sheet, 'E31')
            banques_caisses = self.get_cell_value(bilan_sheet, 'E32')
            total_tresorerie_actif = self.get_cell_value(bilan_sheet, 'E33')
            
            # Ecart de conversion
            ecart_conversion_actif = self.get_cell_value(bilan_sheet, 'E34')
            
            # Total général actif
            total_general_actif = self.get_cell_value(bilan_sheet, 'E35')
            
            # PASSIFS DÉTAILLÉS
            # Capitaux propres
            capital = self.get_cell_value(bilan_sheet, 'I5')
            actionnaires_capital_non_appele = self.get_cell_value(bilan_sheet, 'I6')
            primes_capital = self.get_cell_value(bilan_sheet, 'I7')
            ecarts_reevaluation = self.get_cell_value(bilan_sheet, 'I8')
            reserves_indisponibles = self.get_cell_value(bilan_sheet, 'I9')
            reserves_libres = self.get_cell_value(bilan_sheet, 'I10')
            report_nouveau = self.get_cell_value(bilan_sheet, 'I11')
            resultat_net_bilan = self.get_cell_value(bilan_sheet, 'I12')
            subventions_investissement = self.get_cell_value(bilan_sheet, 'I13')
            provisions_reglementees = self.get_cell_value(bilan_sheet, 'I14')
            total_capitaux_propres = self.get_cell_value(bilan_sheet, 'I15')
            
            # Dettes financières
            emprunts_dettes_financieres = self.get_cell_value(bilan_sheet, 'I17')
            dettes_location_acquisition = self.get_cell_value(bilan_sheet, 'I18')
            provisions_financieres = self.get_cell_value(bilan_sheet, 'I19')
            total_dettes_financieres = self.get_cell_value(bilan_sheet, 'I20')
            
            # Ressources stables
            total_ressources_stables = self.get_cell_value(bilan_sheet, 'I21')
            
            # Passif circulant
            dettes_circulantes_hao = self.get_cell_value(bilan_sheet, 'I22')
            clients_avances_recues = self.get_cell_value(bilan_sheet, 'I23')
            fournisseurs_exploitation = self.get_cell_value(bilan_sheet, 'I24')
            dettes_sociales_fiscales = self.get_cell_value(bilan_sheet, 'I25')
            autres_dettes = self.get_cell_value(bilan_sheet, 'I26')
            provisions_risques_ct = self.get_cell_value(bilan_sheet, 'I27')
            total_passif_circulant = self.get_cell_value(bilan_sheet, 'I28')
            
            # Trésorerie passif
            banques_credits_escompte = self.get_cell_value(bilan_sheet, 'I30')
            banques_credits_tresorerie = self.get_cell_value(bilan_sheet, 'I31')
            total_tresorerie_passif = self.get_cell_value(bilan_sheet, 'I33')
            
            # Ecart de conversion passif
            ecart_conversion_passif = self.get_cell_value(bilan_sheet, 'I34')
            
            # Total général passif
            total_general_passif = self.get_cell_value(bilan_sheet, 'I35')
            
            # Extraction détaillée du compte de résultat
            cr_sheet = workbook['CR']
            
            # CHIFFRE D'AFFAIRES DÉTAILLÉ
            ventes_marchandises = self.get_cell_value(cr_sheet, 'E5')
            achats_marchandises = self.get_cell_value(cr_sheet, 'E6')
            variation_stocks_marchandises = self.get_cell_value(cr_sheet, 'E7')
            marge_commerciale = self.get_cell_value(cr_sheet, 'E8')
            
            ventes_produits_fabriques = self.get_cell_value(cr_sheet, 'E9')
            travaux_services_vendus = self.get_cell_value(cr_sheet, 'E10')
            produits_accessoires = self.get_cell_value(cr_sheet, 'E11')
            chiffre_affaires = self.get_cell_value(cr_sheet, 'E12')
            
            # PRODUCTION ET CHARGES
            production_stockee = self.get_cell_value(cr_sheet, 'E13')
            production_immobilisee = self.get_cell_value(cr_sheet, 'E14')
            subventions_exploitation = self.get_cell_value(cr_sheet, 'E15')
            autres_produits = self.get_cell_value(cr_sheet, 'E16')
            transferts_charges_exploitation = self.get_cell_value(cr_sheet, 'E17')
            
            achats_matieres_premieres = self.get_cell_value(cr_sheet, 'E18')
            variation_stocks_mp = self.get_cell_value(cr_sheet, 'E19')
            autres_achats = self.get_cell_value(cr_sheet, 'E20')
            variation_stocks_autres = self.get_cell_value(cr_sheet, 'E21')
            transports = self.get_cell_value(cr_sheet, 'E22')
            services_exterieurs = self.get_cell_value(cr_sheet, 'E23')
            impots_taxes = self.get_cell_value(cr_sheet, 'E24')
            autres_charges = self.get_cell_value(cr_sheet, 'E25')
            
            # SOLDES INTERMÉDIAIRES DE GESTION
            valeur_ajoutee = self.get_cell_value(cr_sheet, 'E26')
            charges_personnel = self.get_cell_value(cr_sheet, 'E27')
            excedent_brut = self.get_cell_value(cr_sheet, 'E28')
            
            reprises_amortissements = self.get_cell_value(cr_sheet, 'E29')
            dotations_amortissements = self.get_cell_value(cr_sheet, 'E30')
            resultat_exploitation = self.get_cell_value(cr_sheet, 'E31')
            
            # RÉSULTAT FINANCIER
            revenus_financiers = self.get_cell_value(cr_sheet, 'E32')
            reprises_provisions_financieres = self.get_cell_value(cr_sheet, 'E33')
            transferts_charges_financieres = self.get_cell_value(cr_sheet, 'E34')
            frais_financiers = self.get_cell_value(cr_sheet, 'E35')
            dotations_provisions_financieres = self.get_cell_value(cr_sheet, 'E36')
            resultat_financier = self.get_cell_value(cr_sheet, 'E37')
            
            # RÉSULTATS FINAUX
            resultat_activites_ordinaires = self.get_cell_value(cr_sheet, 'E38')
            
            produits_cessions_immob = self.get_cell_value(cr_sheet, 'E39')
            autres_produits_hao = self.get_cell_value(cr_sheet, 'E40')
            valeurs_comptables_cessions = self.get_cell_value(cr_sheet, 'E41')
            autres_charges_hao = self.get_cell_value(cr_sheet, 'E42')
            resultat_hao = self.get_cell_value(cr_sheet, 'E43')
            
            participation_travailleurs = self.get_cell_value(cr_sheet, 'E44')
            impots_resultat = self.get_cell_value(cr_sheet, 'E45')
            resultat_net_cr = self.get_cell_value(cr_sheet, 'E46')
            
            # Extraction du tableau de flux de trésorerie (TFT)
            try:
                tft_sheet = workbook['TFT']
                
                # FLUX DE TRÉSORERIE
                tresorerie_ouverture = self.get_cell_value(tft_sheet, 'E3')
                cafg = self.get_cell_value(tft_sheet, 'E5')
                flux_activites_operationnelles = self.get_cell_value(tft_sheet, 'E11')
                flux_activites_investissement = self.get_cell_value(tft_sheet, 'E18')
                flux_capitaux_propres = self.get_cell_value(tft_sheet, 'E24')
                flux_capitaux_etrangers = self.get_cell_value(tft_sheet, 'E29')
                flux_activites_financement = self.get_cell_value(tft_sheet, 'E30')
                variation_tresorerie = self.get_cell_value(tft_sheet, 'E31')
                tresorerie_cloture = self.get_cell_value(tft_sheet, 'E32')
            except:
                # Valeurs par défaut si TFT n'existe pas
                tresorerie_ouverture = 0
                cafg = excedent_brut + dotations_amortissements
                flux_activites_operationnelles = cafg
                flux_activites_investissement = 0
                flux_capitaux_propres = 0
                flux_capitaux_etrangers = 0
                flux_activites_financement = 0
                variation_tresorerie = 0
                tresorerie_cloture = total_tresorerie_actif - total_tresorerie_passif
            
            # Calculs dérivés et contrôles
            charges_exploitation_totales = (
                abs(achats_marchandises or 0) + 
                abs(achats_matieres_premieres or 0) + 
                abs(autres_achats or 0) + 
                abs(transports or 0) + 
                abs(services_exterieurs or 0) + 
                abs(impots_taxes or 0) + 
                abs(autres_charges or 0) + 
                abs(charges_personnel or 0) + 
                abs(dotations_amortissements or 0)
            )
            
            # Construction du dictionnaire de données complet
            data = {
                # ACTIFS DÉTAILLÉS
                'total_actif': total_general_actif,
                
                # Immobilisations incorporelles
                'frais_dev_prospection': frais_dev_prospection,
                'brevets_licences': brevets_licences,
                'fond_commercial': fond_commercial,
                'autres_immob_incorp': autres_immob_incorp,
                
                # Immobilisations corporelles
                'terrains': terrains,
                'batiments': batiments,
                'agencements': agencements,
                'materiel_mobilier': materiel_mobilier,
                'materiel_transport': materiel_transport,
                'avances_immobilisations': avances_immobilisations,
                
                # Immobilisations financières
                'titres_participation': titres_participation,
                'autres_immob_financieres': autres_immob_financieres,
                'immobilisations_nettes': total_actif_immobilise,
                
                # Actif circulant
                'actif_circulant_hao': actif_circulant_hao,
                'stocks': stocks_et_encours,
                'fournisseurs_avances_versees': fournisseurs_avances,
                'creances_clients': clients,
                'autres_creances': autres_creances,
                'total_actif_circulant': total_actif_circulant,
                
                # Trésorerie actif
                'titres_placement': titres_placement,
                'valeurs_encaisser': valeurs_encaisser,
                'banques_caisses': banques_caisses,
                'tresorerie': total_tresorerie_actif,
                
                # Ecarts
                'ecart_conversion_actif': ecart_conversion_actif,
                
                # PASSIFS DÉTAILLÉS
                # Capitaux propres
                'capital': capital,
                'actionnaires_capital_non_appele': actionnaires_capital_non_appele,
                'primes_capital': primes_capital,
                'ecarts_reevaluation': ecarts_reevaluation,
                'reserves_indisponibles': reserves_indisponibles,
                'reserves_libres': reserves_libres,
                'reserves': (reserves_indisponibles or 0) + (reserves_libres or 0),
                'report_nouveau': report_nouveau,
                'resultat_net_bilan': resultat_net_bilan,
                'subventions_investissement': subventions_investissement,
                'provisions_reglementees': provisions_reglementees,
                'capitaux_propres': total_capitaux_propres,
                
                # Dettes financières
                'emprunts_dettes_financieres': emprunts_dettes_financieres,
                'dettes_location_acquisition': dettes_location_acquisition,
                'provisions_financieres': provisions_financieres,
                'dettes_financieres': total_dettes_financieres,
                'ressources_stables': total_ressources_stables,
                
                # Passif circulant
                'dettes_circulantes_hao': dettes_circulantes_hao,
                'clients_avances_recues': clients_avances_recues,
                'fournisseurs_exploitation': fournisseurs_exploitation,
                'dettes_sociales_fiscales': dettes_sociales_fiscales,
                'autres_dettes': autres_dettes,
                'provisions_risques_ct': provisions_risques_ct,
                'dettes_court_terme': total_passif_circulant,
                
                # Trésorerie passif
                'banques_credits_escompte': banques_credits_escompte,
                'banques_credits_tresorerie': banques_credits_tresorerie,
                'tresorerie_passif': total_tresorerie_passif,
                
                # Ecarts
                'ecart_conversion_passif': ecart_conversion_passif,
                
                # COMPTE DE RÉSULTAT DÉTAILLÉ
                # Chiffre d'affaires
                'ventes_marchandises': ventes_marchandises,
                'achats_marchandises': achats_marchandises,
                'variation_stocks_marchandises': variation_stocks_marchandises,
                'marge_commerciale': marge_commerciale,
                'ventes_produits_fabriques': ventes_produits_fabriques,
                'travaux_services_vendus': travaux_services_vendus,
                'produits_accessoires': produits_accessoires,
                'chiffre_affaires': chiffre_affaires,
                
                # Production et autres produits
                'production_stockee': production_stockee,
                'production_immobilisee': production_immobilisee,
                'subventions_exploitation': subventions_exploitation,
                'autres_produits': autres_produits,
                'transferts_charges_exploitation': transferts_charges_exploitation,
                
                # Achats et charges externes
                'achats_matieres_premieres': achats_matieres_premieres,
                'variation_stocks_mp': variation_stocks_mp,
                'autres_achats': autres_achats,
                'variation_stocks_autres': variation_stocks_autres,
                'transports': transports,
                'services_exterieurs': services_exterieurs,
                'impots_taxes': impots_taxes,
                'autres_charges': autres_charges,
                
                # Soldes intermédiaires
                'valeur_ajoutee': valeur_ajoutee,
                'charges_personnel': charges_personnel,
                'excedent_brut': excedent_brut,
                'reprises_amortissements': reprises_amortissements,
                'dotations_amortissements': dotations_amortissements,
                'resultat_exploitation': resultat_exploitation,
                
                # Résultat financier
                'revenus_financiers': revenus_financiers,
                'reprises_provisions_financieres': reprises_provisions_financieres,
                'transferts_charges_financieres': transferts_charges_financieres,
                'frais_financiers': frais_financiers,
                'dotations_provisions_financieres': dotations_provisions_financieres,
                'resultat_financier': resultat_financier,
                
                # Résultats finaux
                'resultat_activites_ordinaires': resultat_activites_ordinaires,
                'produits_cessions_immob': produits_cessions_immob,
                'autres_produits_hao': autres_produits_hao,
                'valeurs_comptables_cessions': valeurs_comptables_cessions,
                'autres_charges_hao': autres_charges_hao,
                'resultat_hao': resultat_hao,
                'participation_travailleurs': participation_travailleurs,
                'impots_resultat': impots_resultat,
                'resultat_net': resultat_net_cr or resultat_net_bilan,
                
                # Charges d'exploitation totales (calculé)
                'charges_exploitation': charges_exploitation_totales,
                
                # FLUX DE TRÉSORERIE
                'tresorerie_ouverture': tresorerie_ouverture,
                'cafg': cafg,
                'flux_activites_operationnelles': flux_activites_operationnelles,
                'flux_activites_investissement': flux_activites_investissement,
                'flux_capitaux_propres': flux_capitaux_propres,
                'flux_capitaux_etrangers': flux_capitaux_etrangers,
                'flux_activites_financement': flux_activites_financement,
                'variation_tresorerie': variation_tresorerie,
                'tresorerie_cloture': tresorerie_cloture
            }
            
            workbook.close()
            return data
            
        except Exception as e:
            print(f"Erreur lors du chargement du fichier Excel: {e}")
            return None

    def get_cell_value(self, sheet, cell_ref):
        """Extrait la valeur d'une cellule Excel"""
        try:
            cell_value = sheet[cell_ref].value
            if cell_value is None:
                return 0
            if isinstance(cell_value, (int, float)):
                return float(cell_value)
            if isinstance(cell_value, str):
                cleaned_value = cell_value.replace(' ', '').replace(',', '.')
                try:
                    return float(cleaned_value)
                except ValueError:
                    return 0
            return 0
        except Exception:
            return 0

    def calculate_ratios(self, data):
        """Calcule les ratios financiers détaillés"""
        ratios = {}
        
        # Ratios de liquidité
        if data.get('dettes_court_terme', 0) > 0:
            actif_circulant_total = (data.get('stocks', 0) + data.get('creances_clients', 0) + 
                                   data.get('autres_creances', 0) + data.get('tresorerie', 0))
            ratios['ratio_liquidite_generale'] = actif_circulant_total / data['dettes_court_terme']
            
            actif_liquide_immediat = (data.get('creances_clients', 0) + data.get('autres_creances', 0) + data.get('tresorerie', 0))
            ratios['ratio_liquidite_immediate'] = actif_liquide_immediat / data['dettes_court_terme']
            
            ratios['ratio_liquidite_absolue'] = data.get('tresorerie', 0) / data['dettes_court_terme']
        
        # Ratios de solvabilité
        if data.get('total_actif', 0) > 0:
            dettes_totales = data.get('dettes_financieres', 0) + data.get('dettes_court_terme', 0)
            ratios['ratio_endettement'] = dettes_totales / data['total_actif'] * 100
            ratios['ratio_autonomie_financiere'] = data.get('capitaux_propres', 0) / data['total_actif'] * 100
            
            if data.get('dettes_financieres', 0) > 0 and data.get('frais_financiers', 0) != 0:
                ratios['ratio_couverture_charges_financieres'] = data.get('excedent_brut', 0) / abs(data.get('frais_financiers', 1))
        
        # Ratios d'activité et de rotation
        if data.get('chiffre_affaires', 0) > 0:
            ratios['rotation_actif'] = data['chiffre_affaires'] / data.get('total_actif', 1)
            
            if data.get('stocks', 0) > 0:
                ratios['rotation_stocks'] = data['chiffre_affaires'] / data['stocks']
                ratios['duree_ecoulement_stocks'] = 365 / ratios['rotation_stocks']
            
            if data.get('creances_clients', 0) > 0:
                ratios['rotation_creances'] = data['chiffre_affaires'] / data['creances_clients']
                ratios['delai_recouvrement_clients'] = 365 / ratios['rotation_creances']
            
            if data.get('fournisseurs_exploitation', 0) > 0:
                achats_totaux = (data.get('achats_matieres_premieres', 0) + data.get('autres_achats', 0))
                if achats_totaux > 0:
                    ratios['rotation_fournisseurs'] = achats_totaux / data['fournisseurs_exploitation']
                    ratios['delai_paiement_fournisseurs'] = 365 / ratios['rotation_fournisseurs']
        
        # Ratios de structure financière
        if data.get('immobilisations_nettes', 0) > 0:
            ratios['financement_immobilisations'] = data.get('ressources_stables', 0) / data['immobilisations_nettes'] * 100
        
        if data.get('capitaux_propres', 0) > 0:
            ratios['ratio_endettement_financier'] = data.get('dettes_financieres', 0) / data['capitaux_propres']
        
        # Ratios de rentabilité
        if data.get('total_actif', 0) > 0:
            ratios['roa'] = data.get('resultat_net', 0) / data['total_actif'] * 100
            ratios['roa_exploitation'] = data.get('resultat_exploitation', 0) / data['total_actif'] * 100
        
        if data.get('capitaux_propres', 0) > 0:
            ratios['roe'] = data.get('resultat_net', 0) / data['capitaux_propres'] * 100
            ratios['roe_exploitation'] = data.get('resultat_exploitation', 0) / data['capitaux_propres'] * 100
        
        if data.get('chiffre_affaires', 0) > 0:
            ratios['marge_commerciale_pct'] = data.get('marge_commerciale', 0) / data['chiffre_affaires'] * 100
            
            cout_marchandises = data.get('achats_matieres_premieres', 0) + data.get('autres_achats', 0)
            ratios['marge_brute'] = (data['chiffre_affaires'] - cout_marchandises) / data['chiffre_affaires'] * 100
            
            ratios['marge_valeur_ajoutee'] = data.get('valeur_ajoutee', 0) / data['chiffre_affaires'] * 100
            ratios['marge_excedent_brut'] = data.get('excedent_brut', 0) / data['chiffre_affaires'] * 100
            ratios['marge_exploitation'] = data.get('resultat_exploitation', 0) / data['chiffre_affaires'] * 100
            ratios['marge_nette'] = data.get('resultat_net', 0) / data['chiffre_affaires'] * 100
            
            if data.get('charges_exploitation', 0) > 0:
                ratios['coefficient_exploitation'] = data['charges_exploitation'] / data['chiffre_affaires'] * 100
        
        # Ratios de productivité
        if data.get('valeur_ajoutee', 0) > 0:
            ratios['taux_charges_personnel'] = data.get('charges_personnel', 0) / data['valeur_ajoutee'] * 100
            
            if data.get('charges_personnel', 0) > 0:
                ratios['productivite_personnel'] = data['valeur_ajoutee'] / data['charges_personnel']
        
        # Ratios de flux de trésorerie
        if data.get('chiffre_affaires', 0) > 0:
            ratios['ratio_cafg_ca'] = data.get('cafg', 0) / data['chiffre_affaires'] * 100
        
        if data.get('dettes_financieres', 0) > 0 and data.get('cafg', 0) > 0:
            ratios['capacite_remboursement'] = data['dettes_financieres'] / data['cafg']
        
        # Besoin en fonds de roulement
        bfr_exploitation = (data.get('stocks', 0) + data.get('creances_clients', 0) + data.get('autres_creances', 0) + 
                           data.get('fournisseurs_avances_versees', 0) - data.get('fournisseurs_exploitation', 0) - 
                           data.get('dettes_sociales_fiscales', 0) - data.get('autres_dettes', 0))
        ratios['bfr'] = bfr_exploitation
        
        if data.get('chiffre_affaires', 0) > 0:
            ratios['bfr_jours_ca'] = (bfr_exploitation / data['chiffre_affaires']) * 365
        
        # Fonds de roulement
        fonds_roulement = data.get('ressources_stables', 0) - data.get('immobilisations_nettes', 0)
        ratios['fonds_roulement'] = fonds_roulement
        
        # Trésorerie nette
        tresorerie_nette = data.get('tresorerie', 0) - data.get('tresorerie_passif', 0)
        ratios['tresorerie_nette'] = tresorerie_nette
        
        return ratios

    def calculate_score(self, ratios, secteur=None):
        """Calcule le score global basé sur les ratios détaillés"""
        scores = {}
        
        # Score de liquidité (40 points)
        liquidite_score = 0
        
        # Liquidité générale (15 points)
        if 'ratio_liquidite_generale' in ratios:
            if ratios['ratio_liquidite_generale'] >= 2.0:
                liquidite_score += 15
            elif ratios['ratio_liquidite_generale'] >= 1.5:
                liquidite_score += 12
            elif ratios['ratio_liquidite_generale'] >= 1.0:
                liquidite_score += 8
            else:
                liquidite_score += 3
        
        # Liquidité immédiate (10 points)
        if 'ratio_liquidite_immediate' in ratios:
            if ratios['ratio_liquidite_immediate'] >= 1.0:
                liquidite_score += 10
            elif ratios['ratio_liquidite_immediate'] >= 0.8:
                liquidite_score += 8
            elif ratios['ratio_liquidite_immediate'] >= 0.6:
                liquidite_score += 5
            else:
                liquidite_score += 2
        
        # BFR en jours de CA (10 points)
        if 'bfr_jours_ca' in ratios:
            if ratios['bfr_jours_ca'] <= 30:
                liquidite_score += 10
            elif ratios['bfr_jours_ca'] <= 60:
                liquidite_score += 7
            elif ratios['bfr_jours_ca'] <= 90:
                liquidite_score += 4
            else:
                liquidite_score += 1
        
        # Trésorerie nette (5 points)
        if 'tresorerie_nette' in ratios:
            if ratios['tresorerie_nette'] > 0:
                liquidite_score += 5
            else:
                liquidite_score += 1
        
        scores['liquidite'] = liquidite_score
        
        # Score de solvabilité (40 points)
        solvabilite_score = 0
        
        # Autonomie financière (20 points)
        if 'ratio_autonomie_financiere' in ratios:
            if ratios['ratio_autonomie_financiere'] >= 50:
                solvabilite_score += 20
            elif ratios['ratio_autonomie_financiere'] >= 40:
                solvabilite_score += 16
            elif ratios['ratio_autonomie_financiere'] >= 30:
                solvabilite_score += 12
            elif ratios['ratio_autonomie_financiere'] >= 20:
                solvabilite_score += 8
            else:
                solvabilite_score += 3
        
        # Endettement global (15 points)
        if 'ratio_endettement' in ratios:
            if ratios['ratio_endettement'] <= 50:
                solvabilite_score += 15
            elif ratios['ratio_endettement'] <= 65:
                solvabilite_score += 12
            elif ratios['ratio_endettement'] <= 80:
                solvabilite_score += 8
            else:
                solvabilite_score += 3
        
        # Capacité de remboursement (5 points)
        if 'capacite_remboursement' in ratios:
            if ratios['capacite_remboursement'] <= 3:
                solvabilite_score += 5
            elif ratios['capacite_remboursement'] <= 5:
                solvabilite_score += 3
            else:
                solvabilite_score += 1
        
        scores['solvabilite'] = solvabilite_score
        
        # Score de rentabilité (30 points)
        rentabilite_score = 0
        
        # ROE (10 points)
        if 'roe' in ratios:
            if ratios['roe'] >= 15:
                rentabilite_score += 10
            elif ratios['roe'] >= 10:
                rentabilite_score += 8
            elif ratios['roe'] >= 5:
                rentabilite_score += 5
            else:
                rentabilite_score += 2
        
        # ROA (8 points)
        if 'roa' in ratios:
            if ratios['roa'] >= 5:
                rentabilite_score += 8
            elif ratios['roa'] >= 3:
                rentabilite_score += 6
            elif ratios['roa'] >= 1:
                rentabilite_score += 4
            else:
                rentabilite_score += 1
        
        # Marge nette (7 points)
        if 'marge_nette' in ratios:
            if ratios['marge_nette'] >= 10:
                rentabilite_score += 7
            elif ratios['marge_nette'] >= 5:
                rentabilite_score += 5
            elif ratios['marge_nette'] >= 2:
                rentabilite_score += 3
            else:
                rentabilite_score += 1
        
        # Marge d'exploitation (5 points)
        if 'marge_exploitation' in ratios:
            if ratios['marge_exploitation'] >= 10:
                rentabilite_score += 5
            elif ratios['marge_exploitation'] >= 5:
                rentabilite_score += 4
            elif ratios['marge_exploitation'] >= 2:
                rentabilite_score += 2
            else:
                rentabilite_score += 1
        
        scores['rentabilite'] = rentabilite_score
        
        # Score d'activité (15 points)
        activite_score = 0
        
        # Rotation de l'actif (5 points)
        if 'rotation_actif' in ratios:
            if ratios['rotation_actif'] >= 2.0:
                activite_score += 5
            elif ratios['rotation_actif'] >= 1.5:
                activite_score += 4
            elif ratios['rotation_actif'] >= 1.0:
                activite_score += 3
            else:
                activite_score += 1
        
        # Rotation des stocks (5 points)
        if 'rotation_stocks' in ratios:
            if ratios['rotation_stocks'] >= 8:
                activite_score += 5
            elif ratios['rotation_stocks'] >= 6:
                activite_score += 4
            elif ratios['rotation_stocks'] >= 4:
                activite_score += 3
            else:
                activite_score += 1
        
        # Délai de recouvrement (5 points)
        if 'delai_recouvrement_clients' in ratios:
            if ratios['delai_recouvrement_clients'] <= 30:
                activite_score += 5
            elif ratios['delai_recouvrement_clients'] <= 45:
                activite_score += 4
            elif ratios['delai_recouvrement_clients'] <= 60:
                activite_score += 3
            else:
                activite_score += 1
        
        scores['activite'] = activite_score
        
        # Score de gestion (15 points)
        gestion_score = 0
        
        # Productivité du personnel (5 points)
        if 'productivite_personnel' in ratios:
            if ratios['productivite_personnel'] >= 3:
                gestion_score += 5
            elif ratios['productivite_personnel'] >= 2:
                gestion_score += 4
            elif ratios['productivite_personnel'] >= 1.5:
                gestion_score += 3
            else:
                gestion_score += 1
        
        # Taux de charges personnel / VA (5 points)
        if 'taux_charges_personnel' in ratios:
            if ratios['taux_charges_personnel'] <= 40:
                gestion_score += 5
            elif ratios['taux_charges_personnel'] <= 50:
                gestion_score += 4
            elif ratios['taux_charges_personnel'] <= 60:
                gestion_score += 3
            else:
                gestion_score += 1
        
        # CAFG / CA (5 points)
        if 'ratio_cafg_ca' in ratios:
            if ratios['ratio_cafg_ca'] >= 10:
                gestion_score += 5
            elif ratios['ratio_cafg_ca'] >= 7:
                gestion_score += 4
            elif ratios['ratio_cafg_ca'] >= 5:
                gestion_score += 3
            else:
                gestion_score += 1
        
        scores['gestion'] = gestion_score
        
        # Score global sur 140 points, ramené à 100
        score_brut = sum(scores.values())
        scores['global'] = min(100, int(score_brut * 100 / 140))
        
        return scores

    def get_interpretation(self, score):
        """Interprétation du score"""
        if score >= 85:
            return "Excellente", "green"
        elif score >= 70:
            return "Très bonne", "lightgreen"
        elif score >= 55:
            return "Bonne", "yellow"
        elif score >= 40:
            return "Acceptable", "orange"
        elif score >= 25:
            return "Faible", "red"
        else:
            return "Très faible", "darkred"

    def analyze_excel_file(self, file_path, secteur=None):
        """
        Analyse complète d'un fichier Excel
        
        Args:
            file_path (str): Chemin vers le fichier Excel
            secteur (str): Secteur d'activité pour comparaison
            
        Returns:
            dict: Dictionnaire contenant data, ratios, scores et recommandations
        """
        try:
            # Charger les données du fichier Excel
            data = self.load_excel_template(file_path)
            
            if data is None:
                return {
                    'success': False,
                    'error': 'Erreur lors du chargement du fichier Excel',
                    'data': None,
                    'ratios': None,
                    'scores': None,
                    'recommendations': None
                }
            
            # Calculer les ratios
            ratios = self.calculate_ratios(data)
            
            # Calculer les scores
            scores = self.calculate_score(ratios, secteur)
            
            # Générer les recommandations
            recommendations = self.generate_recommendations(data, ratios, scores)
            
            return {
                'success': True,
                'error': None,
                'data': data,
                'ratios': ratios,
                'scores': scores,
                'recommendations': recommendations,
                'secteur': secteur
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Erreur lors de l\'analyse: {str(e)}',
                'data': None,
                'ratios': None,
                'scores': None,
                'recommendations': None
            }

    def generate_recommendations(self, data, ratios, scores):
        """
        Génère des recommandations basées sur l'analyse
        
        Args:
            data (dict): Données financières
            ratios (dict): Ratios calculés
            scores (dict): Scores obtenus
            
        Returns:
            list: Liste des recommandations
        """
        recommendations = []
        
        # Recommandations de liquidité
        if scores.get('liquidite', 0) < 25:
            if ratios.get('ratio_liquidite_generale', 0) < 1.2:
                recommendations.append({
                    "priorite": "URGENT",
                    "categorie": "Liquidité",
                    "probleme": f"Ratio de liquidité générale critique ({ratios.get('ratio_liquidite_generale', 0):.2f})",
                    "impact": "Risque de défaillance à court terme",
                    "actions": [
                        "Négocier immédiatement des délais de paiement avec les fournisseurs",
                        "Accélérer le recouvrement des créances clients",
                        "Réduire les stocks non essentiels",
                        "Négocier une ligne de crédit court terme"
                    ]
                })
        
        # Recommandations de solvabilité
        if scores.get('solvabilite', 0) < 25:
            if ratios.get('ratio_autonomie_financiere', 0) < 25:
                recommendations.append({
                    "priorite": "IMPORTANT",
                    "categorie": "Solvabilité",
                    "probleme": f"Autonomie financière insuffisante ({ratios.get('ratio_autonomie_financiere', 0):.1f}%)",
                    "impact": "Structure financière déséquilibrée",
                    "actions": [
                        "Préparer une augmentation de capital",
                        "Renégocier les dettes financières",
                        "Mettre en réserve tous les bénéfices",
                        "Rechercher des subventions ou aides publiques"
                    ]
                })
        
        # Recommandations de rentabilité
        if scores.get('rentabilite', 0) < 15:
            if ratios.get('marge_nette', 0) < 3:
                recommendations.append({
                    "priorite": "MOYEN TERME",
                    "categorie": "Rentabilité",
                    "probleme": f"Marge nette insuffisante ({ratios.get('marge_nette', 0):.1f}%)",
                    "impact": "Capacité d'autofinancement limitée",
                    "actions": [
                        "Analyser la structure des coûts par activité",
                        "Optimiser les marges commerciales",
                        "Réduire les charges fixes",
                        "Améliorer la productivité"
                    ]
                })
        
        # Recommandations d'activité
        if scores.get('activite', 0) < 8:
            if ratios.get('rotation_stocks', 0) < 4:
                recommendations.append({
                    "priorite": "MOYEN TERME",
                    "categorie": "Activité",
                    "probleme": f"Rotation des stocks lente ({ratios.get('rotation_stocks', 0):.1f})",
                    "impact": "Immobilisation excessive de fonds de roulement",
                    "actions": [
                        "Analyser les stocks dormants et obsolètes",
                        "Améliorer la prévision de la demande",
                        "Négocier des approvisionnements en flux tendu",
                        "Mettre en place un système de gestion des stocks"
                    ]
                })
        
        # Recommandations de gestion
        if scores.get('gestion', 0) < 8:
            if ratios.get('taux_charges_personnel', 0) > 60:
                recommendations.append({
                    "priorite": "MOYEN TERME",
                    "categorie": "Gestion",
                    "probleme": f"Charges de personnel élevées ({ratios.get('taux_charges_personnel', 0):.1f}% de la VA)",
                    "impact": "Productivité insuffisante",
                    "actions": [
                        "Analyser la productivité par service",
                        "Former le personnel aux nouvelles technologies",
                        "Optimiser l'organisation du travail",
                        "Automatiser les tâches répétitives"
                    ]
                })
        
        # Si aucune recommandation critique, ajouter des suggestions d'amélioration
        if not recommendations:
            recommendations.append({
                "priorite": "OPTIMISATION",
                "categorie": "Performance",
                "probleme": "Situation financière globalement satisfaisante",
                "impact": "Opportunités d'optimisation",
                "actions": [
                    "Maintenir la surveillance des ratios clés",
                    "Rechercher des opportunités de croissance",
                    "Optimiser la structure du bilan",
                    "Développer de nouveaux indicateurs de performance"
                ]
            })
        
        return recommendations

    def get_sectoral_comparison(self, ratios, secteur):
        """
        Compare les ratios de l'entreprise avec ceux du secteur
        
        Args:
            ratios (dict): Ratios de l'entreprise
            secteur (str): Secteur d'activité
            
        Returns:
            dict: Comparaison sectorielle
        """
        if secteur not in self.ratios_sectoriels:
            return None
        
        secteur_data = self.ratios_sectoriels[secteur]
        comparison = {}
        
        for ratio_name, secteur_values in secteur_data.items():
            if ratio_name in ratios:
                entreprise_value = ratios[ratio_name]
                q1 = secteur_values['q1']
                median = secteur_values['median']
                q3 = secteur_values['q3']
                
                # Déterminer le quartile
                if entreprise_value >= q3:
                    quartile = 4
                    performance = "Excellente (Top 25%)"
                elif entreprise_value >= median:
                    quartile = 3
                    performance = "Au-dessus de la médiane"
                elif entreprise_value >= q1:
                    quartile = 2
                    performance = "Sous la médiane"
                else:
                    quartile = 1
                    performance = "Quartile inférieur"
                
                comparison[ratio_name] = {
                    'valeur_entreprise': entreprise_value,
                    'q1_secteur': q1,
                    'median_secteur': median,
                    'q3_secteur': q3,
                    'quartile': quartile,
                    'performance': performance
                }
        
        return comparison

    def export_analysis_json(self, analysis_result):
        """
        Exporte les résultats d'analyse en format JSON
        
        Args:
            analysis_result (dict): Résultats de l'analyse
            
        Returns:
            str: JSON formaté
        """
        export_data = {
            'date_analyse': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'donnees_financieres': analysis_result.get('data', {}),
            'ratios_calcules': analysis_result.get('ratios', {}),
            'scores_detailles': analysis_result.get('scores', {}),
            'recommandations': analysis_result.get('recommendations', []),
            'secteur': analysis_result.get('secteur', ''),
            'score_global': analysis_result.get('scores', {}).get('global', 0),
            'interpretation': self.get_interpretation(analysis_result.get('scores', {}).get('global', 0))[0]
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)

    def validate_data(self, data):
        """
        Valide la cohérence des données financières
        
        Args:
            data (dict): Données financières
            
        Returns:
            dict: Résultat de validation avec erreurs/avertissements
        """
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Vérification de l'équilibre du bilan
        total_actif = data.get('total_actif', 0)
        total_passif = (data.get('capitaux_propres', 0) + 
                       data.get('dettes_financieres', 0) + 
                       data.get('dettes_court_terme', 0) + 
                       data.get('tresorerie_passif', 0))
        
        ecart_bilan = abs(total_actif - total_passif)
        if ecart_bilan > total_actif * 0.01:  # Plus de 1% d'écart
            validation_result['errors'].append(
                f"Bilan déséquilibré: écart de {ecart_bilan:,.0f} FCFA entre actif et passif"
            )
            validation_result['is_valid'] = False
        
        # Vérification des valeurs négatives anormales
        critical_positive_fields = [
            'total_actif', 'capitaux_propres', 'chiffre_affaires'
        ]
        
        for field in critical_positive_fields:
            if data.get(field, 0) < 0:
                validation_result['errors'].append(
                    f"Valeur négative anormale pour {field}: {data.get(field, 0):,.0f}"
                )
                validation_result['is_valid'] = False
        
        # Avertissements pour des ratios suspects
        if data.get('chiffre_affaires', 0) > 0:
            if data.get('resultat_net', 0) / data['chiffre_affaires'] > 0.5:
                validation_result['warnings'].append(
                    "Marge nette très élevée (>50%), vérifier la cohérence"
                )
            
            if data.get('resultat_net', 0) / data['chiffre_affaires'] < -0.2:
                validation_result['warnings'].append(
                    "Perte importante (>20% du CA), situation critique"
                )
        
        return validation_result