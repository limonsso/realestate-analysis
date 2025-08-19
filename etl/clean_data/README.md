# 🧹 Projet de Nettoyage Immobilier Québécois

## 🎯 **Mission**

Transformer des données immobilières brutes en une base de données premium prête pour l'analyse d'investissement, en appliquant les meilleures pratiques de data cleaning avec une approche méthodique et intelligente.

## 🏗️ **Architecture Modulaire**

Ce projet utilise une architecture modulaire professionnelle organisée en composants spécialisés :

```
etl/clean_data/
├── 🧩 src/                          # Code source modulaire
│   ├── core/                        # Composants principaux
│   ├── exporters/                   # Gestion de l'export
│   ├── validators/                  # Validation des données
│   └── utils/                       # Utilitaires réutilisables
├── 📥 inputs/                       # Données d'entrée
├── 📤 outputs/                      # Résultats organisés
├── 🧪 tests/                        # Tests unitaires
├── 📋 docs/                         # Documentation complète
└── 🚀 main.py                       # Point d'entrée unique
```

## 🛠️ **Stack Technologique**

### 📊 **Python - Écosystème Data Science**

- **Pandas** : DataFrames et manipulation des données
- **NumPy** : Calculs numériques et arrays
- **GeoPandas** : Manipulation de données géographiques
- **Folium** : Cartes interactives
- **Geopy** : Géocodage et calculs géographiques

### 📈 **Analyse & Visualisation**

- **Matplotlib** : Graphiques de base
- **Seaborn** : Visualisations statistiques avancées
- **Plotly** : Graphiques interactifs premium

### 🔍 **Détection Outliers & Anomalies**

- **SciPy Stats** : Tests statistiques et détection anomalies
- **Scikit-learn** : Algorithmes de détection d'outliers
- **StandardScaler/RobustScaler** : Normalisation des données

## 🔄 **Pipeline de Nettoyage (5 Phases)**

### 🔍 **Phase 1: Audit & Diagnostic Complet**

- Analyse exploratoire avec Pandas/Seaborn
- Matrice des valeurs manquantes
- Détection d'outliers avec IsolationForest
- Analyse des corrélations

### 🛠️ **Phase 2: Nettoyage Intelligent**

- Standardisation des noms de colonnes
- Consolidation des colonnes redondantes
- Nettoyage des variables financières
- Nettoyage des caractéristiques physiques
- Filtrage géographique

### ⚡ **Phase 3: Enrichissement Intelligent**

- Création de métriques financières (ROI, prix/pi²)
- Création de métriques physiques (âge bâtiment)
- Catégorisation et segmentation
- Score de complétude des données

### 🚨 **Phase 4: Validation & Contrôle Qualité**

- Tests automatiques de cohérence
- Validation des métriques financières
- Contrôle de la géolocalisation
- Rapport de qualité détaillé

### 🎯 **Phase 5: Préparation pour l'Analyse**

- Optimisation de la structure finale
- Export multi-format (CSV, Parquet, JSON, GeoJSON)
- Documentation des métadonnées

## 🚀 **Utilisation Rapide**

### 📋 **Installation**

```bash
# Cloner le projet
git clone <repository-url>
cd etl/clean_data

# Installer les dépendances
pip install -r requirements.txt
```

### 🔧 **Exécution**

```bash
# Mode complet (par défaut)
python main.py

# Mode simple
python main.py --mode simple

# Fichier personnalisé
python main.py --input inputs/mon_fichier.csv
```

### 🔧 **Utilisation Programmée**

```python
from src.core import RealEstateDataCleaner
from src.exporters import DataExporter
from src.validators import DataValidator

# Créer le nettoyeur
cleaner = RealEstateDataCleaner("inputs/data.csv")

# Exécuter le pipeline complet
if cleaner.run_complete_cleaning_pipeline():
    print("✅ Pipeline terminé avec succès!")
```

## 📊 **Formats de Sortie Supportés**

| Format      | Extension  | Usage                            | Avantages             |
| ----------- | ---------- | -------------------------------- | --------------------- |
| **CSV**     | `.csv`     | Compatibilité universelle, Excel | Standard, lisible     |
| **Parquet** | `.parquet` | Performance Python, pandas       | Compression, rapidité |
| **JSON**    | `.json`    | Applications web, API            | Structuré, flexible   |
| **GeoJSON** | `.geojson` | Cartes interactives, GIS         | Géospatial, cartes    |

## 🧪 **Tests et Validation**

### ✅ **Tests de Structure**

```bash
python tests/test_organized_structure.py
```

### ✅ **Tests de Nettoyage**

```bash
python tests/test_cleaning.py
```

### ✅ **Validation des Spécifications**

```bash
python validate_specifications.py
```

## 📁 **Organisation des Dossiers**

### 📥 **Inputs**

- Placez vos fichiers CSV/Excel dans le dossier `inputs/`
- Le script détecte automatiquement `sample_real_estate_data.csv`

### 📤 **Outputs**

- **Données nettoyées** : `outputs/cleaned_data/`
- **Rapports de qualité** : `outputs/reports/`
- **Logs d'exécution** : `outputs/logs/`

## 🔧 **Configuration**

### ⚙️ **Chemins Automatiques**

```python
from src.core.config import ensure_directories

# Création automatique des dossiers
ensure_directories()

# Chemins configurés
INPUT_DIR = Path("inputs")
OUTPUT_DIR = Path("outputs")
CLEANED_DATA_DIR = OUTPUT_DIR / "cleaned_data"
REPORTS_DIR = OUTPUT_DIR / "reports"
LOGS_DIR = OUTPUT_DIR / "logs"
```

## 📋 **Colonnes Supportées**

### 🏷️ **Identifiants**

- `_id`, `link`, `company`, `version`, `created_at`, `updated_at`

### 📍 **Localisation**

- `address`, `full_address`, `city`, `region`, `longitude`, `latitude`

### 💰 **Prix & Évaluations**

- `price`, `price_assessment`, `municipal_evaluation_total`

### 💵 **Revenus**

- `revenu`, `plex_revenue`, `potential_gross_revenue`

### 🏠 **Caractéristiques**

- `surface`, `bedrooms`, `bathrooms`, `construction_year`

## 🎯 **Fonctionnalités Avancées**

### 🔍 **Détection d'Opportunités**

- **Sous-évaluations** : Prix < évaluation municipale
- **Anomalies suspectes** : Données nécessitant validation
- **Patterns géographiques** : Zones à forte performance

### 📊 **Métriques Calculées**

- **ROI brut/net** : Retour sur investissement
- **Prix/pi²** : Ratio prix sur surface
- **Potentiel plus-value** : Écart évaluation/prix
- **Âge bâtiment** : Différence avec année actuelle

## 🔮 **Extensions Futures**

### 📊 **Nouveaux Exporteurs**

- Export vers bases de données
- Intégration avec APIs
- Formats spécialisés

### 🔍 **Nouveaux Validateurs**

- Validation métier spécifique
- Règles personnalisées
- Intégration avec systèmes externes

### 🛠️ **Nouveaux Utilitaires**

- Traitement de texte avancé
- Analyse géospatiale
- Machine Learning

## 📚 **Documentation**

- **📋 ARCHITECTURE.md** : Documentation de l'architecture modulaire
- **📋 STRUCTURE.md** : Guide de la structure organisée
- **📋 REORGANISATION_SUMMARY.md** : Résumé de la réorganisation

## 👥 **Contribution**

Ce projet suit les meilleures pratiques de développement :

- **Architecture modulaire** et extensible
- **Tests unitaires** pour chaque composant
- **Documentation complète** et maintenue
- **Code réutilisable** et maintenable

## 🏆 **Objectif Final**

Un dataset premium, traité avec les meilleures technologies Python, **fiable à 99%**, prêt pour des analyses d'investissement de niveau professionnel !

---

_Projet créé le 19 août 2025 - Équipe de nettoyage immobilier québécois_ 🏠✨
