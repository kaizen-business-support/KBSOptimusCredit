"""
Tests unitaires pour le module ratios.py
"""

import unittest
import sys
import os

# Ajouter le dossier parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.core.ratios import RatiosCalculator


class TestRatiosCalculator(unittest.TestCase):
    """Tests pour la classe RatiosCalculator"""
    
    def setUp(self):
        """Configuration initiale des tests"""
        self.calculator = RatiosCalculator()
        
        # Données de test standardisées
        self.sample_data = {
            # Bilan - Actif
            'total_actif': 1000000,
            'immobilisations_nettes': 600000,
            'stocks': 150000,
            'creances_clients': 100000,
            'autres_creances': 50000,
            'tresorerie': 100000,
            'total_actif_circulant': 300000,
            
            # Bilan - Passif
            'capitaux_propres': 400000,
            'capital': 200000,
            'reserves': 100000,
            'resultat_net': 100000,
            'dettes_financieres': 300000,
            'dettes_court_terme': 200000,
            'tresorerie_passif': 100000,
            'ressources_stables': 700000,
            'fournisseurs_exploitation': 80000,
            'dettes_sociales_fiscales': 50000,
            'autres_dettes': 30000,
            'fournisseurs_avances_versees': 20000,
            'clients_avances_recues': 10000,
            
            # Compte de résultat
            'chiffre_affaires': 1500000,
            'valeur_ajoutee': 600000,
            'charges_personnel': 300000,
            'excedent_brut': 300000,
            'resultat_exploitation': 200000,
            'frais_financiers': 20000,
            'resultat_financier': -20000,
            'resultat_net': 100000,
            'achats_matieres_premieres': 500000,
            'autres_achats': 200000,
            'dotations_amortissements': 100000,
            'marge_commerciale': 300000,
            'charges_exploitation': 1300000,
            
            # Flux de trésorerie
            'cafg': 200000,
            'flux_activites_operationnelles': 150000,
            'flux_activites_investissement': -100000,
            'flux_activites_financement': -50000
        }
        
        # Données pour tests d'erreur
        self.invalid_data = {
            'total_actif': 0,
            'capitaux_propres': 0,
            'chiffre_affaires': 0,
            'dettes_court_terme': 0
        }
    
    def test_calculate_all_ratios(self):
        """Test du calcul de tous les ratios"""
        ratios = self.calculator.calculate_all_ratios(self.sample_data)
        
        # Vérifier que le dictionnaire n'est pas vide
        self.assertGreater(len(ratios), 0)
        
        # Vérifier la présence des catégories principales
        expected_categories = [
            'ratio_liquidite_generale', 'ratio_autonomie_financiere',
            'roe', 'roa', 'rotation_actif', 'productivite_personnel'
        ]
        
        for category in expected_categories:
            self.assertIn(category, ratios)
    
    def test_liquidite_ratios(self):
        """Test des ratios de liquidité"""
        ratios = self.calculator.calculate_liquidite_ratios(self.sample_data)
        
        # Test ratio de liquidité générale
        expected_liquidite_generale = (300000 + 100000) / 200000  # (AC + Tréso) / DCT
        self.assertAlmostEqual(
            ratios['ratio_liquidite_generale'], 
            expected_liquidite_generale, 
            places=2,
            msg="Ratio de liquidité générale incorrect"
        )
        
        # Test ratio de liquidité immédiate
        expected_liquidite_immediate = (100000 + 50000 + 100000) / 200000  # Sans stocks
        self.assertAlmostEqual(
            ratios['ratio_liquidite_immediate'],
            expected_liquidite_immediate,
            places=2,
            msg="Ratio de liquidité immédiate incorrect"
        )
        
        # Test BFR en jours de CA
        expected_bfr = 150000 + 100000 + 50000 + 20000 - 80000 - 50000 - 30000 - 10000
        expected_bfr_jours = (expected_bfr / 1500000) * 365
        self.assertAlmostEqual(
            ratios['bfr_jours_ca'],
            expected_bfr_jours,
            places=1,
            msg="BFR en jours de CA incorrect"
        )
    
    def test_solvabilite_ratios(self):
        """Test des ratios de solvabilité"""
        ratios = self.calculator.calculate_solvabilite_ratios(self.sample_data)
        
        # Test autonomie financière
        expected_autonomie = (400000 / 1000000) * 100
        self.assertAlmostEqual(
            ratios['ratio_autonomie_financiere'],
            expected_autonomie,
            places=1,
            msg="Ratio d'autonomie financière incorrect"
        )
        
        # Test endettement global
        expected_endettement = ((300000 + 200000) / 1000000) * 100
        self.assertAlmostEqual(
            ratios['ratio_endettement'],
            expected_endettement,
            places=1,
            msg="Ratio d'endettement global incorrect"
        )
        
        # Test capacité de remboursement
        expected_capacite = 300000 / 200000  # Dettes financières / CAFG
        self.assertAlmostEqual(
            ratios['capacite_remboursement'],
            expected_capacite,
            places=2,
            msg="Capacité de remboursement incorrecte"
        )
    
    def test_rentabilite_ratios(self):
        """Test des ratios de rentabilité"""
        ratios = self.calculator.calculate_rentabilite_ratios(self.sample_data)
        
        # Test ROA
        expected_roa = (100000 / 1000000) * 100
        self.assertAlmostEqual(
            ratios['roa'],
            expected_roa,
            places=1,
            msg="ROA incorrect"
        )
        
        # Test ROE
        expected_roe = (100000 / 400000) * 100
        self.assertAlmostEqual(
            ratios['roe'],
            expected_roe,
            places=1,
            msg="ROE incorrect"
        )
        
        # Test marge nette
        expected_marge_nette = (100000 / 1500000) * 100
        self.assertAlmostEqual(
            ratios['marge_nette'],
            expected_marge_nette,
            places=2,
            msg="Marge nette incorrecte"
        )
        
        # Test marge d'exploitation
        expected_marge_exploitation = (200000 / 1500000) * 100
        self.assertAlmostEqual(
            ratios['marge_exploitation'],
            expected_marge_exploitation,
            places=2,
            msg="Marge d'exploitation incorrecte"
        )
    
    def test_activite_ratios(self):
        """Test des ratios d'activité"""
        ratios = self.calculator.calculate_activite_ratios(self.sample_data)
        
        # Test rotation de l'actif
        expected_rotation_actif = 1500000 / 1000000
        self.assertAlmostEqual(
            ratios['rotation_actif'],
            expected_rotation_actif,
            places=2,
            msg="Rotation de l'actif incorrecte"
        )
        
        # Test rotation des stocks
        expected_rotation_stocks = 1500000 / 150000
        self.assertAlmostEqual(
            ratios['rotation_stocks'],
            expected_rotation_stocks,
            places=1,
            msg="Rotation des stocks incorrecte"
        )
        
        # Test délai de recouvrement clients
        expected_rotation_creances = 1500000 / 100000
        expected_delai_recouvrement = 365 / expected_rotation_creances
        self.assertAlmostEqual(
            ratios['delai_recouvrement_clients'],
            expected_delai_recouvrement,
            places=1,
            msg="Délai de recouvrement clients incorrect"
        )
    
    def test_gestion_ratios(self):
        """Test des ratios de gestion"""
        ratios = self.calculator.calculate_gestion_ratios(self.sample_data)
        
        # Test productivité du personnel
        expected_productivite = 600000 / 300000
        self.assertAlmostEqual(
            ratios['productivite_personnel'],
            expected_productivite,
            places=2,
            msg="Productivité du personnel incorrecte"
        )
        
        # Test taux de charges personnel
        expected_taux_charges = (300000 / 600000) * 100
        self.assertAlmostEqual(
            ratios['taux_charges_personnel'],
            expected_taux_charges,
            places=1,
            msg="Taux de charges personnel incorrect"
        )
        
        # Test ratio CAFG/CA
        expected_cafg_ca = (200000 / 1500000) * 100
        self.assertAlmostEqual(
            ratios['ratio_cafg_ca'],
            expected_cafg_ca,
            places=2,
            msg="Ratio CAFG/CA incorrect"
        )
    
    def test_structure_ratios(self):
        """Test des ratios de structure"""
        ratios = self.calculator.calculate_structure_ratios(self.sample_data)
        
        # Test fonds de roulement
        expected_fr = 700000 - 600000  # Ressources stables - Immobilisations
        self.assertEqual(
            ratios['fonds_roulement'],
            expected_fr,
            msg="Fonds de roulement incorrect"
        )
        
        # Test pourcentage des immobilisations
        expected_pct_immob = (600000 / 1000000) * 100
        self.assertAlmostEqual(
            ratios['pct_immobilisations'],
            expected_pct_immob,
            places=1,
            msg="Pourcentage des immobilisations incorrect"
        )
    
    def test_bceao_ratios(self):
        """Test des ratios spécifiques BCEAO adaptés"""
        ratios = self.calculator.calculate_bceao_ratios(self.sample_data)
        
        # Test ratio de fonds propres de base adapté
        expected_fp_base = (400000 / 1000000) * 100
        self.assertAlmostEqual(
            ratios['ratio_fonds_propres_base'],
            expected_fp_base,
            places=1,
            msg="Ratio de fonds propres de base incorrect"
        )
        
        # Test coefficient de couverture des emplois MLT
        expected_couverture = (700000 / 600000) * 100
        self.assertAlmostEqual(
            ratios['coeff_couverture_emplois_mlt'],
            expected_couverture,
            places=1,
            msg="Coefficient de couverture des emplois MLT incorrect"
        )
    
    def test_calculate_bfr(self):
        """Test du calcul du BFR"""
        bfr = self.calculator.calculate_bfr(self.sample_data)
        
        # BFR = Stocks + Créances + Avances versées - Fournisseurs - Dettes sociales - Autres dettes - Avances reçues
        expected_bfr = (150000 + 100000 + 50000 + 20000 - 
                       80000 - 50000 - 30000 - 10000)
        
        self.assertEqual(
            bfr,
            expected_bfr,
            msg="Calcul du BFR incorrect"
        )
    
    def test_safe_divide(self):
        """Test de la division sécurisée"""
        # Test division normale
        result = self.calculator.safe_divide(10, 2)
        self.assertEqual(result, 5.0)
        
        # Test division par zéro
        result = self.calculator.safe_divide(10, 0)
        self.assertEqual(result, 0)
        
        # Test division par zéro avec valeur par défaut
        result = self.calculator.safe_divide(10, 0, 999)
        self.assertEqual(result, 999)
        
        # Test avec epsilon
        result = self.calculator.safe_divide(10, 1e-7)  # Très proche de zéro
        self.assertEqual(result, 0)
    
    def test_division_by_zero_handling(self):
        """Test de la gestion des divisions par zéro"""
        ratios = self.calculator.calculate_all_ratios(self.invalid_data)
        
        # Vérifier que les ratios sont calculés sans erreur
        self.assertIsInstance(ratios, dict)
        
        # Vérifier que les ratios avec division par zéro retournent 0 ou valeur par défaut
        self.assertEqual(ratios.get('ratio_liquidite_generale', 0), 0)
        self.assertEqual(ratios.get('ratio_autonomie_financiere', 0), 0)
        
    def test_negative_values_handling(self):
        """Test de la gestion des valeurs négatives"""
        negative_data = self.sample_data.copy()
        negative_data['resultat_net'] = -50000
        negative_data['tresorerie'] = -10000
        
        ratios = self.calculator.calculate_all_ratios(negative_data)
        
        # Vérifier que les calculs se font sans erreur
        self.assertIsInstance(ratios, dict)
        
        # Vérifier que les valeurs négatives sont gérées
        self.assertLess(ratios['roe'], 0, "ROE négatif non géré")
        self.assertLess(ratios['tresorerie_nette'], 0, "Trésorerie nette négative non gérée")
    
    def test_ratio_interpretation(self):
        """Test de l'interprétation des ratios"""
        # Test d'interprétation pour un ratio connu
        interpretation = self.calculator.get_ratio_interpretation(
            'ratio_liquidite_generale', 1.8
        )
        
        self.assertIn('level', interpretation)
        self.assertIn('description', interpretation)
        
        # Test avec un ratio excellent
        interpretation_excellent = self.calculator.get_ratio_interpretation(
            'ratio_liquidite_generale', 2.5
        )
        self.assertEqual(interpretation_excellent['level'], 'excellent')
        
        # Test avec un ratio faible
        interpretation_faible = self.calculator.get_ratio_interpretation(
            'ratio_liquidite_generale', 0.8
        )
        self.assertEqual(interpretation_faible['level'], 'faible')
    
    def test_extreme_values(self):
        """Test avec des valeurs extrêmes"""
        extreme_data = {
            'total_actif': 1e12,  # Très grand
            'capitaux_propres': 1e12,
            'chiffre_affaires': 1e12,
            'dettes_court_terme': 1,  # Très petit
            'stocks': 1e-6,  # Très petit
            'creances_clients': 0,
            'autres_creances': 0,
            'tresorerie': 0,
            'total_actif_circulant': 1e-6,
            'valeur_ajoutee': 1e11,
            'charges_personnel': 1e10,
            'cafg': 1e11,
            'resultat_net': 1e11
        }
        
        ratios = self.calculator.calculate_all_ratios(extreme_data)
        
        # Vérifier que le calcul ne produit pas d'erreur
        self.assertIsInstance(ratios, dict)
        
        # Vérifier que certains ratios sont cohérents avec les valeurs extrêmes
        self.assertGreater(ratios['ratio_liquidite_generale'], 1000, "Ratio de liquidité générale avec valeurs extrêmes")
        self.assertGreater(ratios['productivite_personnel'], 10, "Productivité du personnel avec valeurs extrêmes")
    
    def test_consistency_across_methods(self):
        """Test de cohérence entre les différentes méthodes de calcul"""
        # Calculer tous les ratios
        all_ratios = self.calculator.calculate_all_ratios(self.sample_data)
        
        # Calculer les ratios par catégorie séparément
        liquidite_ratios = self.calculator.calculate_liquidite_ratios(self.sample_data)
        solvabilite_ratios = self.calculator.calculate_solvabilite_ratios(self.sample_data)
        rentabilite_ratios = self.calculator.calculate_rentabilite_ratios(self.sample_data)
        activite_ratios = self.calculator.calculate_activite_ratios(self.sample_data)
        gestion_ratios = self.calculator.calculate_gestion_ratios(self.sample_data)
        
        # Vérifier la cohérence pour quelques ratios clés
        self.assertAlmostEqual(
            all_ratios['ratio_liquidite_generale'],
            liquidite_ratios['ratio_liquidite_generale'],
            places=6,
            msg="Incohérence dans le calcul de la liquidité générale"
        )
        
        self.assertAlmostEqual(
            all_ratios['ratio_autonomie_financiere'],
            solvabilite_ratios['ratio_autonomie_financiere'],
            places=6,
            msg="Incohérence dans le calcul de l'autonomie financière"
        )
        
        self.assertAlmostEqual(
            all_ratios['roe'],
            rentabilite_ratios['roe'],
            places=6,
            msg="Incohérence dans le calcul du ROE"
        )
    
    def test_missing_data_handling(self):
        """Test de la gestion des données manquantes"""
        incomplete_data = {
            'total_actif': 1000000,
            'chiffre_affaires': 1500000,
            # Données manquantes volontairement
        }
        
        ratios = self.calculator.calculate_all_ratios(incomplete_data)
        
        # Vérifier que le calcul ne lève pas d'exception
        self.assertIsInstance(ratios, dict)
        
        # Vérifier que les ratios calculables le sont quand même
        self.assertGreater(ratios['rotation_actif'], 0)


class TestRatiosEdgeCases(unittest.TestCase):
    """Tests pour les cas limites et situations particulières"""
    
    def setUp(self):
        self.calculator = RatiosCalculator()
    
    def test_startup_company_profile(self):
        """Test avec le profil d'une startup (peu d'actifs, pas de revenus)"""
        startup_data = {
            'total_actif': 50000,
            'immobilisations_nettes': 10000,
            'tresorerie': 40000,
            'capitaux_propres': 50000,
            'capital': 50000,
            'chiffre_affaires': 0,  # Pas encore de revenus
            'resultat_net': -20000,  # Pertes initiales
            'charges_personnel': 30000,
            'total_actif_circulant': 0,
            'dettes_court_terme': 0,
            'dettes_financieres': 0
        }
        
        ratios = self.calculator.calculate_all_ratios(startup_data)
        
        # Vérifications spécifiques aux startups
        self.assertEqual(ratios['ratio_autonomie_financiere'], 100.0, "Startup devrait avoir 100% d'autonomie")
        self.assertLess(ratios['roe'], 0, "ROE négatif pour startup en perte")
        self.assertEqual(ratios['ratio_endettement'], 0.0, "Pas d'endettement pour cette startup")
    
    def test_mature_company_profile(self):
        """Test avec le profil d'une entreprise mature"""
        mature_data = {
            'total_actif': 10000000,
            'immobilisations_nettes': 6000000,
            'stocks': 1500000,
            'creances_clients': 1000000,
            'tresorerie': 500000,
            'total_actif_circulant': 3000000,
            'capitaux_propres': 4000000,
            'dettes_financieres': 3000000,
            'dettes_court_terme': 2000000,
            'chiffre_affaires': 15000000,
            'resultat_net': 1200000,
            'valeur_ajoutee': 6000000,
            'charges_personnel': 3000000,
            'cafg': 2000000
        }
        
        ratios = self.calculator.calculate_all_ratios(mature_data)
        
        # Vérifications pour entreprise mature
        self.assertGreater(ratios['ratio_liquidite_generale'], 1.0, "Liquidité suffisante")
        self.assertEqual(ratios['ratio_autonomie_financiere'], 40.0, "Autonomie financière équilibrée")
        self.assertGreater(ratios['roe'], 20.0, "ROE élevé pour entreprise performante")
        self.assertLess(ratios['capacite_remboursement'], 2.0, "Capacité de remboursement excellente")


if __name__ == '__main__':
    # Configuration des tests
    unittest.main(verbosity=2, buffer=True)
