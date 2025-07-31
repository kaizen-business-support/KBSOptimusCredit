# Guide Utilisateur - Outil d'Analyse Financière BCEAO v2.0

## 🎯 Présentation Générale

L'outil d'analyse financière BCEAO est une application web moderne conçue pour évaluer la santé financière des entreprises selon les normes prudentielles de la Banque Centrale des États de l'Afrique de l'Ouest. Il offre une analyse complète avec notation automatique et recommandations personnalisées.

### 🌟 Fonctionnalités Principales

- **Analyse complète** : Plus de 25 ratios financiers calculés automatiquement
- **Scoring BCEAO** : Notation sur 100 points selon 5 catégories (liquidité, solvabilité, rentabilité, activité, gestion)
- **Comparaisons sectorielles** : Benchmarks par quartiles pour 6 secteurs d'activité
- **Import Excel** : Compatible avec les modèles BCEAO standard
- **Rapports professionnels** : Export en PDF, Excel et JSON
- **Recommandations** : Plan d'action personnalisé sur 6 mois

## 🚀 Démarrage Rapide

### Accès à l'Application

1. **URL** : https://bceao-financial-analyzer.streamlit.app
2. **Navigateurs supportés** : Chrome, Firefox, Safari, Edge (version récente)
3. **Connexion** : Aucune inscription requise

### Première Utilisation

1. **Page d'accueil** : Découvrez les fonctionnalités
2. **Démonstration** : Cliquez sur "Lancer la Démonstration" pour tester avec des données d'exemple
3. **Navigation** : Utilisez le menu horizontal pour naviguer entre les sections

## 📊 Types d'Analyse Disponibles

### 1. Import Excel

**Format requis :**
- Extension : .xlsx ou .xls
- Feuilles obligatoires : "Bilan", "CR" (Compte de Résultat)
- Feuille optionnelle : "TFT" (Tableau de Flux de Trésorerie)

**Procédure :**
1. Téléchargez le modèle Excel BCEAO depuis l'application
2. Remplissez vos données financières dans le modèle
3. Uploadez le fichier via l'interface
4. Sélectionnez votre secteur d'activité
5. Vérifiez l'extraction des données
6. Lancez l'analyse

### 2. Saisie Manuelle

**Sections disponibles :**
- **Bilan** : Actif immobilisé, actif circulant, capitaux propres, dettes
- **Compte de résultat** : Chiffre d'affaires, charges, résultats
- **Flux de trésorerie** : Activités opérationnelles, d'investissement, de financement

**Conseils de saisie :**
- Montants en FCFA sans espaces ni virgules
- Vérifiez l'équilibre du bilan (Actif = Passif)
- Complétez tous les champs obligatoires
- Utilisez la validation automatique

## 📈 Comprendre les Résultats

### Score Global BCEAO (sur 100 points)

Le score est calculé selon 5 catégories :

1. **Liquidité (40 points max)**
   - Ratio de liquidité générale
   - Ratio de liquidité réduite
   - Ratio de liquidité immédiate

2. **Solvabilité (40 points max)**
   - Ratio d'autonomie financière
   - Ratio d'endettement
   - Couverture des frais financiers

3. **Rentabilité (30 points max)**
   - Rentabilité des capitaux propres (ROE)
   - Rentabilité des actifs (ROA)
   - Marge bénéficiaire nette

4. **Activité (15 points max)**
   - Rotation des actifs
   - Rotation des stocks
   - Délai de recouvrement clients

5. **Gestion (15 points max)**
   - Productivité du personnel
   - Charges de personnel/VA
   - Capacité d'autofinancement

### Interprétation des Scores

- **80-100** : Excellent - Situation financière très solide
- **65-79** : Bon - Situation satisfaisante avec quelques points d'amélioration
- **50-64** : Acceptable - Situation correcte nécessitant une surveillance
- **35-49** : Préoccupant - Difficultés financières nécessitant des actions correctives
- **0-34** : Critique - Situation alarmante nécessitant une restructuration

### Comparaisons Sectorielles

Les benchmarks sectoriels sont disponibles pour :
- Agriculture et agro-alimentaire
- Industries manufacturières
- BTP (Bâtiment et Travaux Publics)
- Commerce
- Services
- Transport et logistique

**Quartiles d'interprétation :**
- Q4 (75-100%) : Performance supérieure
- Q3 (50-75%) : Performance bonne
- Q2 (25-50%) : Performance moyenne
- Q1 (0-25%) : Performance faible

## 📋 Génération de Rapports

### Types de Rapports

1. **Synthèse Exécutive**
   - Vue d'ensemble en 1 page
   - Score global et principaux ratios
   - Recommandations prioritaires

2. **Rapport Détaillé**
   - Analyse complète sur 10-15 pages
   - Tous les ratios calculés
   - Comparaisons sectorielles
   - Plan d'action détaillé

3. **Dashboard Interactif**
   - Graphiques dynamiques
   - Radar des performances
   - Évolution temporelle

### Formats d'Export

- **PDF** : Rapports formatés pour impression
- **Excel** : Données et calculs réutilisables
- **JSON** : Données brutes pour intégrations
- **Email** : Envoi direct des rapports

## 🔧 Fonctionnalités Avancées

### Sidebar de Navigation

La barre latérale affiche en permanence :
- Score global BCEAO
- Normes prudentielles par ratio
- Alertes et recommandations urgentes
- Liens vers la documentation

### Validation Automatique

L'outil vérifie automatiquement :
- Équilibre du bilan
- Cohérence des montants
- Complétude des données
- Aberrations dans les ratios

### Recommandations Personnalisées

Basées sur l'analyse, des recommandations sont générées pour :
- Amélioration de la liquidité
- Optimisation de la structure financière
- Renforcement de la rentabilité
- Efficacité opérationnelle

## ❓ FAQ - Questions Fréquentes

### Données et Sécurité

**Q : Mes données sont-elles sauvegardées ?**
R : Non, toutes les données sont traitées en mémoire et supprimées à la fermeture de session pour garantir la confidentialité.

**Q : Puis-je analyser plusieurs entreprises ?**
R : Oui, chaque analyse est indépendante. Vous pouvez effectuer plusieurs analyses dans la même session.

**Q : Les normes sont-elles à jour ?**
R : Oui, les normes BCEAO et sectorielles sont mises à jour mensuellement.

### Problèmes Techniques

**Q : Mon fichier Excel n'est pas reconnu**
R : Vérifiez que le fichier respecte le modèle BCEAO avec les feuilles "Bilan" et "CR" correctement nommées.

**Q : Les calculs semblent incorrects**
R : Vérifiez l'équilibre de votre bilan et la cohérence des montants saisis.

**Q : L'application est lente**
R : L'analyse de gros volumes peut prendre quelques secondes. Patientez ou rafraîchissez la page.

### Utilisation

**Q : Puis-je modifier les données après import ?**
R : Oui, vous pouvez ajuster manuellement les données extraites avant de lancer l'analyse.

**Q : Comment interpréter un ratio négatif ?**
R : Les ratios négatifs indiquent généralement des pertes ou des situations financières dégradées.

**Q : Puis-je comparer avec l'année précédente ?**
R : Cette fonctionnalité sera disponible dans la version 2.1 (analyse temporelle).

## 📞 Support et Assistance

### Contacts

- **Email** : support@bceao.int
- **Téléphone** : +221 33 839 05 00
- **Documentation** : https://bceao.int/outils-analyse
- **Horaires** : Lundi-Vendredi 8h-17h (GMT)

### Ressources Utiles

- [Modèle Excel BCEAO](assets/template_excel.xlsx)
- [Normes prudentielles BCEAO](data/bceao_norms.json)
- [Guide des ratios financiers](docs/api_reference.md)
- [Procédures de déploiement](docs/deployment.md)

### Formation

Des sessions de formation sont organisées trimestriellement :
- Formation initiale (2h) : Prise en main de l'outil
- Formation avancée (4h) : Interprétation des analyses
- Ateliers sectoriels : Spécificités par secteur d'activité

**Inscription** : formation@bceao.int

## 📈 Évolutions Prévues

### Version 2.1 (Q2 2025)

- Support multi-devises (USD, EUR)
- Analyses comparatives temporelles
- API REST pour intégrations
- Module de prévisions financières
- Tableaux de bord personnalisables

### Version 3.0 (Q4 2025)

- Intelligence artificielle prédictive
- Détection automatique d'anomalies
- Benchmarking international
- Interface mobile optimisée
- Intégration comptabilité en temps réel

---

**© 2024 BCEAO - Tous droits réservés**

*Ce guide est mis à jour régulièrement. Consultez la version en ligne pour les dernières fonctionnalités.*