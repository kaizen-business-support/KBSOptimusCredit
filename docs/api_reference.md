# Référence API - Outil d'Analyse Financière BCEAO v2.0

## 📚 Vue d'Ensemble de l'Architecture

L'outil d'analyse financière BCEAO est structuré en modules Python interconnectés offrant une API complète pour l'analyse des états financiers.

### Structure des Modules

```
modules/
├── core/              # Moteur d'analyse principal
│   ├── analyzer.py    # Classe principale FinancialAnalyzer
│   ├── ratios.py      # Calculateur de ratios RatiosCalculator
│   └── excel_loader.py # Chargeur Excel ExcelDataLoader
├── components/        # Composants interface utilisateur
│   ├── sidebar.py     # Barre latérale avec normes
│   ├── navigation.py  # Menu de navigation
│   ├── charts.py      # Graphiques Plotly
│   └── forms.py       # Formulaires de saisie
├── pages/             # Pages de l'application
│   ├── home.py        # Page d'accueil
│   ├── excel_import.py # Import Excel
│   ├── manual_input.py # Saisie manuelle
│   ├── analysis.py    # Résultats d'analyse
│   └── reports.py     # Génération de rapports
└── utils/             # Utilitaires
    ├── formatters.py  # Formatage des données
    └── validators.py  # Validation des données
```

## 🔧 Module Core - Moteur d'Analyse

### Classe FinancialAnalyzer

**Localisation** : `modules/core/analyzer.py`

#### Constructeur

```python
class FinancialAnalyzer:
    def __init__(self):
        """
        Initialise l'analyseur financier avec les calculateurs et données de référence
        """
```

**Attributs :**
- `ratios_calculator` : Instance de RatiosCalculator
- `excel_loader` : Instance de ExcelDataLoader  
- `bceao_norms` : Normes prudentielles BCEAO
- `sectoral_norms` : Normes sectorielles par industrie

#### Méthodes Principales

##### analyze_excel_file()

```python
def analyze_excel_file(self, file_path: str, secteur: str = None) -> Dict[str, Any]:
    """
    Analyse complète à partir d'un fichier Excel
    
    Args:
        file_path (str): Chemin vers le fichier Excel
        secteur (str, optional): Secteur d'activité de l'entreprise
    
    Returns:
        Dict[str, Any]: Résultats complets de l'analyse
        {
            'financial_data': dict,      # Données financières extraites
            'ratios': dict,              # Ratios calculés
            'scores': dict,              # Scores BCEAO par catégorie
            'sectoral_analysis': dict,   # Analyse sectorielle (si secteur)
            'recommendations': list,     # Recommandations d'amélioration
            'validation': dict,          # Résultats de validation
            'metadata': dict             # Métadonnées (date, secteur, etc.)
        }
    
    Raises:
        ValueError: Si l'extraction des données échoue
        FileNotFoundError: Si le fichier n'existe pas
    """
```

##### analyze_manual_data()

```python
def analyze_manual_data(self, financial_data: Dict[str, float], secteur: str = None) -> Dict[str, Any]:
    """
    Analyse complète à partir de données saisies manuellement
    
    Args:
        financial_data (Dict[str, float]): Données financières sous forme de dictionnaire
        secteur (str, optional): Secteur d'activité de l'entreprise
    
    Returns:
        Dict[str, Any]: Même structure que analyze_excel_file()
    """
```

##### calculate_bceao_score()

```python
def calculate_bceao_score(self, ratios: Dict[str, float], secteur: str = None) -> Dict[str, int]:
    """
    Calcule le score BCEAO selon les 5 catégories réglementaires
    
    Args:
        ratios (Dict[str, float]): Ratios financiers calculés
        secteur (str, optional): Secteur pour ajustements spécifiques
    
    Returns:
        Dict[str, int]: Scores par catégorie
        {
            'liquidite': int,      # Score liquidité (0-40)
            'solvabilite': int,    # Score solvabilité (0-40)
            'rentabilite': int,    # Score rentabilité (0-30)
            'activite': int,       # Score activité (0-15)
            'gestion': int,        # Score gestion (0-15)
            'global': int          # Score global (0-100)
        }
    """
```

##### validate_financial_data()

```python
def validate_financial_data(self, data: Dict[str, float]) -> Dict[str, Any]:
    """
    Valide la cohérence et complétude des données financières
    
    Args:
        data (Dict[str, float]): Données financières à valider
    
    Returns:
        Dict[str, Any]: Résultats de validation
        {
            'is_valid': bool,        # Validation globale
            'errors': List[str],     # Erreurs critiques
            'warnings': List[str],   # Avertissements
            'completeness': float    # Taux de complétude (0-100%)
        }
    """
```

### Classe RatiosCalculator

**Localisation** : `modules/core/ratios.py`

#### Méthodes de Calcul

##### calculate_all_ratios()

```python
def calculate_all_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
    """
    Calcule tous les ratios financiers (25+ ratios)
    
    Args:
        data (Dict[str, float]): Données financières de base
    
    Returns:
        Dict[str, float]: Tous les ratios calculés
        {
            # Ratios de liquidité
            'ratio_liquidite_generale': float,
            'ratio_liquidite_reduite': float,
            'ratio_liquidite_immediate': float,
            
            # Ratios de solvabilité  
            'ratio_autonomie_financiere': float,
            'ratio_endettement': float,
            'couverture_frais_financiers': float,
            
            # Ratios de rentabilité
            'roe': float,              # Return on Equity
            'roa': float,              # Return on Assets  
            'marge_nette': float,
            'marge_exploitation': float,
            
            # Ratios d'activité
            'rotation_actifs': float,
            'rotation_stocks': float,
            'delai_recouvrement_clients': float,
            'delai_paiement_fournisseurs': float,
            
            # Ratios de gestion
            'productivite_personnel': float,
            'taux_charges_personnel': float,
            'ratio_cafg_ca': float,
            
            # Ratios de structure
            'fonds_roulement': float,
            'besoin_fonds_roulement': float,
            'tresorerie_nette': float,
            
            # Et plus de 10 autres ratios spécialisés...
        }
    """
```

##### Ratios Spécialisés

```python
def calculate_liquidity_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
    """Calcule les ratios de liquidité"""

def calculate_solvency_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
    """Calcule les ratios de solvabilité"""

def calculate_profitability_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
    """Calcule les ratios de rentabilité"""

def calculate_activity_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
    """Calcule les ratios d'activité"""

def calculate_management_ratios(self, data: Dict[str, float]) -> Dict[str, float]:
    """Calcule les ratios de gestion"""
```

### Classe ExcelDataLoader

**Localisation** : `modules/core/excel_loader.py`

#### Méthodes d'Import

##### load_excel_template()

```python
def load_excel_template(self, file_path: str) -> Dict[str, float]:
    """
    Charge les données depuis un fichier Excel au format BCEAO
    
    Args:
        file_path (str): Chemin vers le fichier Excel
    
    Returns:
        Dict[str, float]: Données financières extraites
        {
            # Bilan - Actif
            'immobilisations_incorporelles': float,
            'immobilisations_corporelles': float,
            'immobilisations_financieres': float,
            'total_actif_immobilise': float,
            
            'stocks_marchandises': float,
            'creances_clients': float,
            'autres_creances': float,
            'tresorerie_actif': float,
            'total_actif_circulant': float,
            
            'total_actif': float,
            
            # Bilan - Passif
            'capital_social': float,
            'reserves': float,
            'resultat_net': float,
            'total_capitaux_propres': float,
            
            'dettes_financieres_long_terme': float,
            'dettes_financieres_court_terme': float,
            'dettes_fournisseurs': float,
            'autres_dettes': float,
            'total_dettes': float,
            
            'total_passif': float,
            
            # Compte de Résultat
            'chiffre_affaires': float,
            'production_vendue': float,
            'marge_commerciale': float,
            'production_stockee': float,
            'production_immobilisee': float,
            'valeur_ajoutee': float,
            
            'charges_personnel': float,
            'impots_taxes': float,
            'dotations_amortissements': float,
            'autres_charges_exploitation': float,
            'total_charges_exploitation': float,
            
            'resultat_exploitation': float,
            'charges_financieres': float,
            'produits_financiers': float,
            'resultat_financier': float,
            'resultat_courant': float,
            'resultat_exceptionnel': float,
            'impot_benefices': float,
            'resultat_net': float,
            
            # Flux de Trésorerie (si disponible)
            'flux_activites_operationnelles': float,
            'flux_activites_investissement': float,
            'flux_activites_financement': float,
            'variation_tresorerie': float
        }
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        ValueError: Si le format n'est pas conforme
        KeyError: Si les feuilles requises sont manquantes
    """
```

##### validate_excel_structure()

```python
def validate_excel_structure(self, file_path: str) -> Dict[str, Any]:
    """
    Valide la structure du fichier Excel avant extraction
    
    Args:
        file_path (str): Chemin vers le fichier Excel
    
    Returns:
        Dict[str, Any]: Résultats de validation
        {
            'is_valid': bool,
            'missing_sheets': List[str],
            'sheet_details': Dict[str, Dict],
            'errors': List[str]
        }
    """
```

## 🎨 Module Components - Interface Utilisateur

### Fonction show_financial_sidebar()

**Localisation** : `modules/components/sidebar.py`

```python
def show_financial_sidebar(analysis_results: Dict[str, Any] = None):
    """
    Affiche la barre latérale avec les normes BCEAO et résultats d'analyse
    
    Args:
        analysis_results (Dict[str, Any], optional): Résultats d'analyse à afficher
    
    Displays:
        - Score global BCEAO si disponible
        - Normes prudentielles par ratio
        - Alertes et recommandations urgentes
        - Liens utiles et documentation
    """
```

### Fonctions de Graphiques

**Localisation** : `modules/components/charts.py`

```python
def create_radar_chart(scores: Dict[str, int], categories: List[str]) -> go.Figure:
    """
    Crée un graphique radar des scores BCEAO
    
    Args:
        scores (Dict[str, int]): Scores par catégorie
        categories (List[str]): Liste des catégories
    
    Returns:
        go.Figure: Graphique Plotly
    """

def create_waterfall_chart(flux_data: Dict[str, float]) -> go.Figure:
    """
    Crée un graphique waterfall des flux de trésorerie
    
    Args:
        flux_data (Dict[str, float]): Données de flux
    
    Returns:
        go.Figure: Graphique Plotly
    """

def create_ratios_comparison_chart(ratios: Dict[str, float], sectoral_norms: Dict[str, Dict]) -> go.Figure:
    """
    Crée un graphique de comparaison avec les normes sectorielles
    
    Args:
        ratios (Dict[str, float]): Ratios calculés
        sectoral_norms (Dict[str, Dict]): Normes sectorielles
    
    Returns:
        go.Figure: Graphique Plotly
    """
```

## 🛠️ Module Utils - Utilitaires

### Fonctions de Formatage

**Localisation** : `modules/utils/formatters.py`

```python
def format_currency(amount: float, currency: str = "FCFA") -> str:
    """
    Formate un montant en devise avec séparateurs de milliers
    
    Args:
        amount (float): Montant à formater
        currency (str): Devise (défaut: "FCFA")
    
    Returns:
        str: Montant formaté (ex: "1 234 567 FCFA")
    """

def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Formate un pourcentage avec nombre de décimales spécifié
    
    Args:
        value (float): Valeur à formater
        decimals (int): Nombre de décimales
    
    Returns:
        str: Pourcentage formaté (ex: "15.3%")
    """

def format_ratio(value: float, decimals: int = 2) -> str:
    """
    Formate un ratio avec gestion des valeurs spéciales
    
    Args:
        value (float): Ratio à formater  
        decimals (int): Nombre de décimales
    
    Returns:
        str: Ratio formaté ou "N/A" si invalide
    """
```

### Fonctions de Validation

**Localisation** : `modules/utils/validators.py`

```python
def validate_balance_sheet(data: Dict[str, float]) -> Dict[str, Any]:
    """
    Valide l'équilibre et cohérence du bilan
    
    Args:
        data (Dict[str, float]): Données de bilan
    
    Returns:
        Dict[str, Any]: Résultats de validation
        {
            'is_balanced': bool,
            'balance_difference': float,
            'errors': List[str],
            'warnings': List[str]
        }
    """

def validate_income_statement(data: Dict[str, float]) -> Dict[str, Any]:
    """
    Valide la cohérence du compte de résultat
    
    Args:
        data (Dict[str, float]): Données de compte de résultat
    
    Returns:
        Dict[str, Any]: Résultats de validation
    """

def validate_data_completeness(data: Dict[str, float]) -> float:
    """
    Calcule le taux de complétude des données
    
    Args:
        data (Dict[str, float]): Données financières
    
    Returns:
        float: Taux de complétude (0-100%)
    """
```

## 📊 Normes et Références

### Structure des Normes BCEAO

**Fichier** : `data/bceao_norms.json`

```json
{
    "ratios_prudentiels": {
        "liquidite_generale": {
            "minimum": 1.0,
            "optimal": 1.5,
            "description": "Actif circulant / Dettes court terme"
        },
        "autonomie_financiere": {
            "minimum": 0.2,
            "optimal": 0.4,
            "description": "Capitaux propres / Total bilan"
        }
    },
    "scoring": {
        "liquidite": {
            "max_points": 40,
            "criteres": {...}
        },
        "solvabilite": {
            "max_points": 40,
            "criteres": {...}
        }
    }
}
```

### Structure des Normes Sectorielles

**Fichier** : `data/sectoral_norms.json`

```json
{
    "agriculture_agro_alimentaire": {
        "ratios": {
            "rotation_stocks": {
                "q1": 2.1,
                "median": 4.3,
                "q3": 7.2
            }
        }
    },
    "industrie_manufacturiere": {...},
    "btp": {...},
    "commerce": {...},
    "services": {...},
    "transport_logistique": {...}
}
```

## 🔗 Intégration et Extensions

### Utilisation Programmatique

```python
# Exemple d'utilisation complète
from modules.core.analyzer import FinancialAnalyzer

# Initialisation
analyzer = FinancialAnalyzer()

# Analyse depuis Excel
results = analyzer.analyze_excel_file("data/entreprise.xlsx", "industrie_manufacturiere")

# Analyse depuis données manuelles
financial_data = {
    'total_actif': 1000000,
    'capitaux_propres': 400000,
    'chiffre_affaires': 1500000,
    'resultat_net': 75000
    # ... autres données
}
results = analyzer.analyze_manual_data(financial_data, "commerce")

# Extraction des résultats
score_global = results['scores']['global']
ratios = results['ratios']
recommendations = results['recommendations']
```

### API REST Future (v2.1)

Endpoints prévus pour l'intégration :

```
POST /api/v1/analyze/excel
POST /api/v1/analyze/manual
GET  /api/v1/norms/bceao
GET  /api/v1/norms/sectoral/{sector}
GET  /api/v1/report/{analysis_id}/pdf
```

## 🧪 Tests et Qualité

### Tests Unitaires

**Localisation** : `tests/`

```python
# Exemple de tests pour FinancialAnalyzer
import unittest
from modules.core.analyzer import FinancialAnalyzer

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
```

### Couverture de Tests

- **Modules core** : 95%+ de couverture
- **Calculs de ratios** : 100% de couverture
- **Validation données** : 90%+ de couverture
- **Import Excel** : 85%+ de couverture

## 📋 Dictionnaire des Données

### Champs Obligatoires

#### Bilan - Actif
- `immobilisations_incorporelles` : Brevets, licences, fonds commercial
- `immobilisations_corporelles` : Terrains, bâtiments, matériel
- `immobilisations_financieres` : Participations, prêts long terme
- `stocks_marchandises` : Valeur des stocks de marchandises
- `creances_clients` : Créances clients et comptes rattachés
- `autres_creances` : Autres créances d'exploitation
- `tresorerie_actif` : Disponibilités et valeurs mobilières

#### Bilan - Passif
- `capital_social` : Capital social nominal
- `reserves` : Réserves légales et statutaires
- `resultat_net` : Résultat net de l'exercice
- `dettes_financieres_long_terme` : Emprunts > 1 an
- `dettes_financieres_court_terme` : Emprunts < 1 an
- `dettes_fournisseurs` : Dettes fournisseurs et comptes rattachés
- `autres_dettes` : Autres dettes d'exploitation

#### Compte de Résultat
- `chiffre_affaires` : Ventes de marchandises et productions vendues
- `marge_commerciale` : CA - Coût d'achat des marchandises vendues
- `valeur_ajoutee` : Production - Consommations externes
- `excedent_brut` : VA - Charges de personnel - Impôts et taxes
- `resultat_exploitation` : Excédent brut - Dotations + Reprises
- `charges_financieres` : Intérêts et charges assimilées
- `produits_financiers` : Revenus de participations et placements

### Champs Calculés Automatiquement

- `total_actif_immobilise` : Somme des immobilisations
- `total_actif_circulant` : Somme de l'actif circulant
- `total_capitaux_propres` : Capital + Réserves + Résultat
- `total_dettes` : Somme de toutes les dettes
- `fonds_roulement` : Ressources stables - Actif immobilisé
- `besoin_fonds_roulement` : Actif circulant (hors tréso) - Dettes CT (hors financières)
- `tresorerie_nette` : Fonds de roulement - BFR

## 🎯 Exemples d'Utilisation Avancée

### Analyse Batch de Plusieurs Entreprises

```python
import pandas as pd
from modules.core.analyzer import FinancialAnalyzer

def analyze_portfolio(excel_files: List[str], secteur: str) -> pd.DataFrame:
    """
    Analyse un portefeuille d'entreprises
    
    Args:
        excel_files: Liste des fichiers Excel
        secteur: Secteur d'activité commun
    
    Returns:
        DataFrame avec résultats comparatifs
    """
    analyzer = FinancialAnalyzer()
    results = []
    
    for file_path in excel_files:
        try:
            result = analyzer.analyze_excel_file(file_path, secteur)
            company_data = {
                'file': file_path,
                'score_global': result['scores']['global'],
                'roe': result['ratios']['roe'],
                'ratio_liquidite': result['ratios']['ratio_liquidite_generale'],
                'ratio_endettement': result['ratios']['ratio_endettement']
            }
            results.append(company_data)
        except Exception as e:
            print(f"Erreur analyse {file_path}: {e}")
    
    return pd.DataFrame(results)
```

### Génération de Rapports Personnalisés

```python
def generate_custom_report(analysis_results: Dict, template: str = "executive") -> str:
    """
    Génère un rapport personnalisé
    
    Args:
        analysis_results: Résultats d'analyse complète
        template: Type de rapport ("executive", "detailed", "regulatory")
    
    Returns:
        Rapport formaté en HTML/markdown
    """
    scores = analysis_results['scores']
    ratios = analysis_results['ratios']
    recommendations = analysis_results['recommendations']
    
    if template == "executive":
        report = f"""
        # Synthèse Exécutive
        
        ## Score Global : {scores['global']}/100
        
        ### Performance par Catégorie
        - Liquidité : {scores['liquidite']}/40
        - Solvabilité : {scores['solvabilite']}/40
        - Rentabilité : {scores['rentabilite']}/30
        
        ### Recommandations Prioritaires
        {chr(10).join(f"- {rec}" for rec in recommendations[:3])}
        """
    
    return report
```

### Intégration avec Bases de Données

```python
import sqlite3
import json
from datetime import datetime

def save_analysis_to_db(analysis_results: Dict, company_id: str, db_path: str):
    """
    Sauvegarde les résultats d'analyse en base
    
    Args:
        analysis_results: Résultats complets
        company_id: Identifiant entreprise
        db_path: Chemin vers la base SQLite
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Création table si nécessaire
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id TEXT,
            date_analyse DATE,
            score_global INTEGER,
            ratios TEXT,
            scores TEXT,
            recommendations TEXT
        )
    """)
    
    # Insertion données
    cursor.execute("""
        INSERT INTO analyses 
        (company_id, date_analyse, score_global, ratios, scores, recommendations)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        company_id,
        datetime.now().isoformat(),
        analysis_results['scores']['global'],
        json.dumps(analysis_results['ratios']),
        json.dumps(analysis_results['scores']),
        json.dumps(analysis_results['recommendations'])
    ))
    
    conn.commit()
    conn.close()
```

## 🔧 Configuration et Personnalisation

### Configuration des Seuils BCEAO

```python
# Modification des seuils dans bceao_norms.json
{
    "ratios_prudentiels": {
        "liquidite_generale": {
            "critique": 0.8,      # Seuil critique
            "minimum": 1.0,       # Seuil minimum
            "satisfaisant": 1.2,  # Seuil satisfaisant  
            "optimal": 1.5        # Seuil optimal
        }
    }
}
```

### Ajout de Nouveaux Ratios

```python
# Dans modules/core/ratios.py
def calculate_custom_ratio(self, data: Dict[str, float]) -> float:
    """
    Calcule un ratio personnalisé
    
    Args:
        data: Données financières
        
    Returns:
        Valeur du ratio personnalisé
    """
    if data.get('denominateur', 0) != 0:
        return data.get('numerateur', 0) / data['denominateur']
    return 0.0

# Ajout dans calculate_all_ratios()
ratios['mon_ratio_custom'] = self.calculate_custom_ratio(data)
```

### Personnalisation des Recommandations

```python
def generate_custom_recommendations(ratios: Dict, scores: Dict, secteur: str) -> List[str]:
    """
    Génère des recommandations personnalisées par secteur
    
    Args:
        ratios: Ratios calculés
        scores: Scores par catégorie
        secteur: Secteur d'activité
        
    Returns:
        Liste de recommandations spécifiques
    """
    recommendations = []
    
    # Recommandations spécifiques par secteur
    secteur_mapping = {
        'industrie_manufacturiere': {
            'stock_turnover_min': 4.0,
            'receivables_days_max': 45
        },
        'commerce': {
            'stock_turnover_min': 8.0,
            'receivables_days_max': 30
        }
    }
    
    if secteur in secteur_mapping:
        norms = secteur_mapping[secteur]
        
        if ratios.get('rotation_stocks', 0) < norms['stock_turnover_min']:
            recommendations.append(
                f"Améliorer la rotation des stocks (actuel: {ratios['rotation_stocks']:.1f}, "
                f"recommandé: {norms['stock_turnover_min']})"
            )
    
    return recommendations
```

## 📖 Glossaire des Termes Financiers

### Ratios de Liquidité
- **Liquidité générale** : Capacité à honorer les dettes court terme avec l'actif circulant
- **Liquidité réduite** : Liquidité sans les stocks (actif disponible/dettes CT)
- **Liquidité immédiate** : Liquidité avec seulement la trésorerie

### Ratios de Solvabilité
- **Autonomie financière** : Part des capitaux propres dans le financement
- **Endettement** : Niveau d'endettement par rapport aux capitaux propres
- **Couverture charges financières** : Capacité à couvrir les intérêts

### Ratios de Rentabilité
- **ROE** (Return on Equity) : Rentabilité des capitaux propres
- **ROA** (Return on Assets) : Rentabilité des actifs
- **Marge nette** : Pourcentage de bénéfice sur le chiffre d'affaires

### Ratios d'Activité
- **Rotation des actifs** : Efficacité d'utilisation des actifs
- **Rotation des stocks** : Vitesse d'écoulement des stocks
- **Délai de recouvrement** : Temps moyen de paiement des clients

### Ratios de Gestion
- **Productivité du personnel** : VA générée par employé
- **Taux de charges de personnel** : Part des charges RH dans la VA
- **Ratio CAFG/CA** : Capacité d'autofinancement sur CA

## 🔄 Historique des Versions

### v2.0 (Actuelle)
- Architecture modulaire complète
- 25+ ratios financiers
- Scoring BCEAO sur 100 points
- Comparaisons sectorielles
- Interface Streamlit moderne
- Export multi-formats

### v2.1 (Prévue Q2 2025)
- API REST
- Support multi-devises
- Analyses temporelles
- Module de prévisions
- Tableaux de bord personnalisables

### v3.0 (Prévue Q4 2025)
- Intelligence artificielle
- Détection d'anomalies
- Benchmarking international
- Interface mobile
- Intégration temps réel

---

**© 2024 BCEAO - Référence API v2.0**

*Cette documentation est mise à jour avec chaque version. Consultez le repository Git pour les dernières modifications.*