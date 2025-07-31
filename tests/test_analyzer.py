import unittest
import sys
import os

# Ajouter le dossier parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.core.analyzer import FinancialAnalyzer
from modules.core.excel_loader import ExcelDataLoader

class TestFinancialAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = FinancialAnalyzer()
        self.sample_data = {
            'total_actif': 1000000,
            'capitaux_propres': 400000,
            'dettes_financieres': 300000,
            'dettes_court_terme': 300000,
            'chiffre_affaires': 1500000,
            'resultat_net': 75000,
            'stocks': 150000,
            'creances_clients': 100000,
            'tresorerie': 50000
        }
    
    def test_analyze_manual_data(self):
        """Test de l'analyse avec données manuelles"""
        result = self.analyzer.analyze_manual_data(self.sample_data, 'industrie_manufacturiere')
        
        self.assertIn('ratios', result)
        self.assertIn('scores', result)
        self.assertIn('recommendations', result)
        self.assertIn('validation', result)
    
    def test_calculate_bceao_score(self):
        """Test du calcul de score BCEAO"""
        ratios = self.analyzer.ratios_calculator.calculate_all_ratios(self.sample_data)
        scores = self.analyzer.calculate_bceao_score(ratios)
        
        self.assertIn('global', scores)
        self.assertIn('liquidite', scores)
        self.assertIn('solvabilite', scores)
        self.assertTrue(0 <= scores['global'] <= 100)
    
    def test_validation(self):
        """Test de la validation des données"""
        validation = self.analyzer.validate_financial_data(self.sample_data)
        
        self.assertIn('is_valid', validation)
        self.assertIn('errors', validation)
        self.assertIn('warnings', validation)

if __name__ == '__main__':
    unittest.main()