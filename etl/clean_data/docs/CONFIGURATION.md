# ⚙️ Guide de Configuration - Pipeline ETL Ultra-Intelligent

## 🎯 Vue d'ensemble

Ce guide détaille la configuration complète du pipeline ETL ultra-intelligent, incluant les paramètres, les variables d'environnement, et la personnalisation avancée.

## 🔧 Configuration de Base

### Fichiers de configuration

#### 1. `requirements.txt`
Dépendances Python principales :
```txt
pandas>=1.5.0
numpy>=1.21.0
fuzzywuzzy>=0.18.0
python-Levenshtein>=0.12.0
scikit-learn>=1.1.0
pymongo>=4.0.0
```

#### 2. `requirements_advanced.txt`
Dépendances avancées pour optimisations :
```txt
dask>=2022.0.0
modin>=0.20.0
numba>=0.56.0
pyarrow>=8.0.0
geopandas>=0.12.0
h5py>=3.7.0
openpyxl>=3.0.0
```

#### 3. `config/consolidation_config.py`
Configuration centralisée de la consolidation :
```python
# Seuils de similarité
SIMILARITY_THRESHOLD = 80.0
REGEX_SIMILARITY_THRESHOLD = 85.0

# Groupes de consolidation prédéfinis
CONSOLIDATION_GROUPS = {
    "Prix": ["price", "prix", "asking_price"],
    "Surface": ["surface", "superficie", "sqft"],
    # ... autres groupes
}
```

## 🚀 Paramètres de Ligne de Commande

### Arguments principaux

#### Source de données
```bash
# MongoDB
--source mongodb
--mongodb-db real_estate_db
--mongodb-collection properties
--mongodb-query '{"type": "triplex"}'
--limit 1000

# CSV
--source csv
--source-path data/properties.csv

# JSON
--source json
--source-path data/properties.json

# Test (données synthétiques)
--source test
```

#### Sortie et formats
```bash
--output exports/
--formats parquet,csv,json
```

#### Optimisation
```bash
--optimization light      # Optimisations de base
--optimization medium     # Optimisations avancées
--optimization aggressive # Toutes optimisations
```

### Options avancées

#### Performance
```bash
--parallel              # Traitement parallèle
--chunked               # Export par chunks
--memory-limit 4GB      # Limite mémoire
```

#### Validation
```bash
--validate-only         # Validation uniquement
--dry-run              # Mode simulation
--verbose               # Logs détaillés
```

#### Configuration personnalisée
```bash
--config custom_config.json
--similarity-threshold 85.0
--quality-threshold 90.0
```

## 🔧 Configuration Avancée

### 1. Personnalisation des Groupes de Consolidation

#### Créer un fichier de configuration personnalisé
```python
# custom_config.py
from config.consolidation_config import ConsolidationConfig

class CustomConsolidationConfig(ConsolidationConfig):
    # Redéfinir les groupes de consolidation
    CONSOLIDATION_GROUPS = {
        "Prix_Custom": ["price", "prix", "asking_price", "list_price"],
        "Surface_Custom": ["surface", "superficie", "sqft", "area"],
        "Chambres_Custom": ["bedrooms", "chambres", "nb_bedrooms", "chambre_count"]
    }
    
    # Ajuster les seuils
    SIMILARITY_THRESHOLD = 85.0
    REGEX_SIMILARITY_THRESHOLD = 90.0
    
    # Priorités personnalisées
    COLUMN_PRIORITIES = {
        "Prix_Custom": ["prix", "price", "asking_price"],  # 'prix' en premier
        "Surface_Custom": ["superficie", "surface", "sqft"]  # 'superficie' en premier
    }
```

#### Utiliser la configuration personnalisée
```bash
python main_ultra_intelligent.py \
  --source test \
  --config custom_config.py \
  --output exports/
```

### 2. Configuration des Optimisations

#### Niveau Light (rapide)
```python
# Optimisations de base
OPTIMIZATIONS = {
    "memory_optimization": True,
    "type_optimization": True,
    "parallel_processing": False,
    "jit_compilation": False,
    "chunked_processing": False
}
```

#### Niveau Medium (équilibré)
```python
# Optimisations avancées
OPTIMIZATIONS = {
    "memory_optimization": True,
    "type_optimization": True,
    "parallel_processing": True,
    "jit_compilation": False,
    "chunked_processing": True,
    "categorization": True
}
```

#### Niveau Aggressive (maximal)
```python
# Toutes optimisations
OPTIMIZATIONS = {
    "memory_optimization": True,
    "type_optimization": True,
    "parallel_processing": True,
    "jit_compilation": True,
    "chunked_processing": True,
    "categorization": True,
    "advanced_algorithms": True
}
```

### 3. Configuration de la Validation

#### Seuils de qualité
```python
# Seuils configurables
QUALITY_THRESHOLDS = {
    "global_score": 80.0,        # Score global minimum
    "type_consistency": 85.0,    # Cohérence des types
    "value_validity": 90.0,      # Validité des valeurs
    "geographic_validation": 95.0, # Validation géographique
    "business_rules": 88.0       # Règles métier
}
```

#### Règles de validation métier
```python
# Règles spécifiques immobilier
BUSINESS_RULES = {
    "price_range": (10000, 10000000),      # Prix en dollars
    "surface_range": (20, 10000),          # Surface en m²
    "bedrooms_range": (0, 20),             # Nombre de chambres
    "bathrooms_range": (0, 20),            # Nombre de salles de bain
    "year_range": (1900, 2025),            # Année de construction
    "quebec_coordinates": {                 # Limites Québec
        "lat_min": 45.0, "lat_max": 63.0,
        "lng_min": -80.0, "lng_max": -57.0
    }
}
```

## 🌍 Variables d'Environnement

### Configuration MongoDB
```bash
# Variables d'environnement MongoDB
export MONGODB_URI="mongodb://user:pass@host:port"
export MONGODB_DB="real_estate_db"
export MONGODB_COLLECTION="properties"
export MONGODB_TIMEOUT=30000
export MONGODB_MAX_POOL_SIZE=100
```

### Configuration des performances
```bash
# Limites de performance
export PIPELINE_MEMORY_LIMIT="4GB"
export PIPELINE_CHUNK_SIZE=10000
export PIPELINE_MAX_WORKERS=4
export PIPELINE_TIMEOUT=3600
```

### Configuration des logs
```bash
# Niveaux de logging
export LOG_LEVEL="INFO"
export LOG_FILE="pipeline.log"
export LOG_FORMAT="%(asctime)s - %(levelname)s - %(message)s"
```

## 📊 Configuration des Rapports

### Personnalisation des rapports
```python
# Configuration des rapports
REPORT_CONFIG = {
    "include_metadata": True,
    "include_performance": True,
    "include_quality_metrics": True,
    "include_similarity_matrix": True,
    "report_format": "markdown",
    "include_charts": True,
    "custom_templates": "templates/"
}
```

### Templates personnalisés
```python
# Créer des templates de rapport personnalisés
CUSTOM_TEMPLATES = {
    "executive_summary": "templates/executive_summary.md",
    "technical_details": "templates/technical_details.md",
    "quality_metrics": "templates/quality_metrics.md"
}
```

## 🔄 Configuration Dynamique

### 1. Configuration par fichier JSON
```json
{
  "source": "mongodb",
  "mongodb": {
    "db": "real_estate_db",
    "collection": "properties",
    "query": {"type": "triplex"},
    "limit": 1000
  },
  "optimization": "medium",
  "output": "exports/",
  "formats": ["csv", "parquet"],
  "validation": {
    "quality_threshold": 85.0,
    "similarity_threshold": 80.0
  }
}
```

#### Utilisation
```bash
python main_ultra_intelligent.py --config config.json
```

### 2. Configuration par variables d'environnement
```bash
# Configuration complète par variables d'environnement
export PIPELINE_SOURCE="mongodb"
export PIPELINE_MONGODB_DB="real_estate_db"
export PIPELINE_MONGODB_COLLECTION="properties"
export PIPELINE_OPTIMIZATION="medium"
export PIPELINE_OUTPUT="exports/"
export PIPELINE_FORMATS="csv,parquet"
```

### 3. Configuration par API
```python
# Configuration programmatique
from core.ultra_intelligent_cleaner import UltraIntelligentCleaner

config = {
    "source": "mongodb",
    "mongodb_db": "real_estate_db",
    "mongodb_collection": "properties",
    "optimization": "medium",
    "output": "exports/",
    "formats": ["csv", "parquet"]
}

cleaner = UltraIntelligentCleaner(config)
cleaner.run_complete_pipeline()
```

## 🎯 Configuration des Cas d'Usage

### 1. Pipeline de Production
```bash
# Configuration production
python main_ultra_intelligent.py \
  --source mongodb \
  --mongodb-db real_estate_prod \
  --mongodb-collection properties \
  --limit 10000 \
  --optimization aggressive \
  --parallel \
  --chunked \
  --output production_exports/ \
  --formats parquet,csv \
  --verbose
```

### 2. Pipeline de Test
```bash
# Configuration test
python main_ultra_intelligent.py \
  --source test \
  --limit 100 \
  --optimization light \
  --output test_exports/ \
  --formats csv \
  --dry-run
```

### 3. Pipeline de Validation
```bash
# Configuration validation
python main_ultra_intelligent.py \
  --source csv \
  --source-path data/sample.csv \
  --validate-only \
  --verbose \
  --output validation_reports/
```

## 🔍 Validation de la Configuration

### Vérifier la configuration
```bash
# Validation de la configuration
python main_ultra_intelligent.py --config config.json --dry-run --verbose

# Test de la configuration
python -c "
from config.consolidation_config import ConsolidationConfig
config = ConsolidationConfig()
print('✅ Configuration valide')
print(f'Seuil de similarité: {config.SIMILARITY_THRESHOLD}%')
print(f'Groupes de consolidation: {len(config.CONSOLIDATION_GROUPS)}')
"
```

### Test de connectivité
```bash
# Test MongoDB
python -c "
from utils.db import test_mongodb_connection
result = test_mongodb_connection('mongodb://localhost:27017')
print(f'Connexion MongoDB: {"✅ OK" if result else "❌ Échec"}')
"
```

## 📝 Exemples de Configuration Complète

### Configuration MongoDB avec authentification
```json
{
  "source": "mongodb",
  "source_path": "mongodb://user:password@host:port",
  "mongodb_db": "real_estate_db",
  "mongodb_collection": "properties",
  "mongodb_query": "{\"status\": \"active\"}",
  "limit": 5000,
  "optimization": "medium",
  "parallel": true,
  "chunked": true,
  "output": "exports/",
  "formats": ["parquet", "csv", "json"],
  "verbose": true,
  "quality_threshold": 85.0,
  "similarity_threshold": 80.0
}
```

### Configuration CSV avec validation stricte
```json
{
  "source": "csv",
  "source_path": "data/properties.csv",
  "optimization": "light",
  "output": "exports/",
  "formats": ["csv"],
  "validate_only": false,
  "quality_threshold": 95.0,
  "similarity_threshold": 90.0,
  "business_rules": {
    "strict_validation": true,
    "auto_correction": false
  }
}
```

---

**🚀 Pipeline ETL Ultra-Intelligent v7.0.0** - Guide de configuration complet
