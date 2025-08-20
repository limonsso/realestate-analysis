# 🏗️ Architecture Modulaire du Projet de Nettoyage Immobilier

## 📁 Structure Réorganisée

```
etl/clean_data/
├── 📥 inputs/                    # Données d'entrée
├── 📤 outputs/                   # Résultats organisés
│   ├── 🗂️ cleaned_data/         # Données nettoyées
│   ├── 📊 reports/              # Rapports de qualité
│   └── 📝 logs/                 # Fichiers de logs
├── 🧩 src/                       # Code source modulaire
│   ├── __init__.py              # Package principal
│   ├── core/                    # Composants principaux
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration centralisée
│   │   ├── cleaner.py           # Nettoyeur principal
│   │   └── simple_cleaner.py    # Nettoyeur simplifié
│   ├── exporters/               # Gestion de l'export
│   │   ├── __init__.py
│   │   ├── data_exporter.py     # Export des données
│   │   └── report_exporter.py   # Export des rapports
│   ├── validators/              # Validation des données
│   │   ├── __init__.py
│   │   └── data_validator.py    # Validateur principal
│   └── utils/                   # Utilitaires
│       ├── __init__.py
│       └── data_utils.py        # Utilitaires de données
├── 🧪 tests/                    # Tests unitaires
├── 📋 docs/                     # Documentation
├── 📁 examples/                 # Exemples d'utilisation
├── 🚀 main.py                   # Point d'entrée principal
└── 📋 requirements.txt           # Dépendances
```

## 🎯 Principes de l'Architecture

### ✅ **Séparation des Responsabilités**

- **Core** : Logique métier principale
- **Exporters** : Gestion de l'export des données
- **Validators** : Validation et contrôle qualité
- **Utils** : Fonctions utilitaires réutilisables

### ✅ **Modularité**

- Chaque composant a une responsabilité unique
- Interfaces claires entre les modules
- Facile d'ajouter de nouvelles fonctionnalités

### ✅ **Réutilisabilité**

- Composants indépendants
- Utilitaires génériques
- Configuration centralisée

## 🔧 Composants Principaux

### 🧩 **Module Core**

```python
from src.core import RealEstateDataCleaner, SimpleRealEstateCleaner

# Nettoyeur principal avec toutes les phases
cleaner = RealEstateDataCleaner(input_file="data.csv")
success = cleaner.run_complete_cleaning_pipeline()

# Nettoyeur simplifié pour cas basiques
simple_cleaner = SimpleRealEstateCleaner("data.csv")
simple_cleaner.clean_data()
```

### 📤 **Module Exporters**

```python
from src.exporters import DataExporter, ReportExporter

# Export des données dans différents formats
data_exporter = DataExporter(output_dir="outputs/cleaned_data")
exported_files = data_exporter.export_data(df, "mon_dataset")

# Export des rapports
report_exporter = ReportExporter(reports_dir="outputs/reports")
quality_report = report_exporter.export_quality_report(df, validation_results)
```

### ✅ **Module Validators**

```python
from src.validators import DataValidator

# Validation complète du dataset
validator = DataValidator()
validation_results = validator.validate_dataset(df)

print(f"Taux de succès: {validation_results['summary']['success_rate']:.1f}%")
```

### 🛠️ **Module Utils**

```python
from src.utils import DataUtils

# Standardisation des noms de colonnes
df = DataUtils.standardize_column_names(df)

# Consolidation des colonnes de revenus
df = DataUtils.consolidate_revenue_columns(df)

# Création de métriques financières
df = DataUtils.create_financial_metrics(df)
```

## 🚀 Utilisation

### 📋 **Script Principal**

```bash
# Mode complet (par défaut)
python main.py

# Mode simple
python main.py --mode simple

# Fichier personnalisé
python main.py --input inputs/mon_fichier.csv

# Mode complet avec MongoDB
python main.py --mongodb "mongodb://localhost:27017/"
```

### 🔧 **Utilisation Programmée**

```python
import sys
from pathlib import Path

# Ajouter le dossier src au path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from core.cleaner import RealEstateDataCleaner
from exporters.data_exporter import DataExporter
from validators.data_validator import DataValidator

# Créer le nettoyeur
cleaner = RealEstateDataCleaner("inputs/data.csv")

# Exécuter le pipeline
if cleaner.run_complete_cleaning_pipeline():
    # Récupérer les données nettoyées
    df_cleaned = cleaner.get_cleaned_data()

    # Valider les données
    validator = DataValidator()
    validation_results = validator.validate_dataset(df_cleaned)

    # Exporter les données
    exporter = DataExporter("outputs/cleaned_data")
    exported_files = exporter.export_data(df_cleaned)

    print("✅ Pipeline terminé avec succès!")
```

## 🔄 Flux de Données

```
📥 Input CSV → 🔍 Audit → 🧹 Nettoyage → ⚡ Enrichissement → ✅ Validation → 📤 Export
     ↓              ↓          ↓              ↓              ↓          ↓
  [DataLoader] → [Auditor] → [Cleaner] → [Enricher] → [Validator] → [Exporter]
```

## 🧪 Tests

### ✅ **Tests de Structure**

```bash
python tests/test_organized_structure.py
```

### ✅ **Tests de Nettoyage**

```bash
python tests/test_cleaning.py
```

### ✅ **Tests de Validation**

```bash
python tests/test_validators.py
```

## 🔧 Configuration

### ⚙️ **Fichier de Configuration**

```python
# src/core/config.py
INPUT_DIR = Path("inputs")
OUTPUT_DIR = Path("outputs")
CLEANED_DATA_DIR = OUTPUT_DIR / "cleaned_data"
REPORTS_DIR = OUTPUT_DIR / "reports"
LOGS_DIR = OUTPUT_DIR / "logs"
```

### 🎨 **Personnalisation**

```python
# Ajouter un nouveau format d'export
SUPPORTED_OUTPUT_FORMATS = {
    'csv': '.csv',
    'parquet': '.parquet',
    'json': '.json',
    'geojson': '.geojson',
    'excel': '.xlsx'  # Nouveau format
}

# Ajouter un nouveau dossier
NEW_DIR = OUTPUT_DIR / "nouveau_dossier"
```

## 📊 Avantages de cette Architecture

### 🎯 **Maintenabilité**

- Code organisé et lisible
- Responsabilités clairement séparées
- Facile de déboguer et modifier

### 📈 **Évolutivité**

- Ajout simple de nouveaux composants
- Extension facile des fonctionnalités
- Architecture extensible

### 👥 **Collaboration**

- Structure claire pour l'équipe
- Modules indépendants
- Tests séparés par composant

### 🚀 **Production**

- Code prêt pour la production
- Gestion d'erreurs robuste
- Logging et monitoring

## 🔮 Extensions Futures

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

---

_Architecture créée le 19 août 2025 - Projet de nettoyage immobilier québécois_ 🏠✨
