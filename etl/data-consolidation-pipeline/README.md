# 🚀 PIPELINE DE CONSOLIDATION DE DONNÉES - Architecture Modulaire Unifiée

## 📋 Description

Pipeline ETL modulaire et unifié pour la consolidation de données immobilières. Utilise une architecture modulaire moderne avec des composants spécialisés pour une maintenance et une extensibilité optimales.

## 🏗️ Architecture Modulaire

### **Composants Principaux**

- **🎼 PipelineManager** : Orchestrateur principal intégré
- **📊 DataProcessor** : Traitement et validation des données
- **💾 ExportManager** : Export multi-formats avancé
- **📋 ReportGenerator** : Génération automatique des rapports
- **⚙️ ConfigManager** : Gestion de la configuration

### **Composants Spécialisés**

- **🔍 DataExtractor** : Extraction depuis MongoDB, CSV, JSON
- **🧠 DataConsolidator** : Consolidation intelligente des colonnes
- **🧹 DataCleaner** : Nettoyage et normalisation
- **🚀 DataEnricher** : Enrichissement des données
- **✅ DataValidator** : Validation complète des données

### **Modules Externes (Optionnels)**

- **🧠 SimilarityDetector** : Détection de similarités avancée
- **📊 QualityValidator** : Validation de qualité avec Great Expectations
- **💾 AdvancedExporter** : Export vers formats spécialisés
- **⚡ PerformanceOptimizer** : Optimisations de performance
- **🎨 ValidationDashboard** : Dashboard interactif avec Plotly

## 📁 Structure du Projet

```
etl/data-consolidation-pipeline/
├── README.md                        ← Documentation principale
├── requirements.txt                 ← Dépendances Python
├── main_modular_pipeline.py        ← Point d'entrée principal
├── config/                          ← Configuration du pipeline
│   ├── __init__.py
│   ├── consolidation_config.py      ← Configuration de base (30 groupes)
│   ├── custom_fields_config.py     ← Configuration personnalisée (67 champs)
│   └── final_columns_config.py     ← Configuration finale des colonnes
├── core/                            ← Architecture modulaire principale
│   ├── __init__.py
│   ├── pipeline_manager.py          ← Orchestrateur principal intégré
│   ├── data_processor.py            ← Traitement des données
│   ├── export_manager.py            ← Gestion des exports
│   ├── report_generator.py          ← Génération des rapports
│   ├── config_manager.py            ← Gestion de la configuration
│   └── components/                  ← Composants spécialisés
│       ├── data_extractor.py        ← Extraction des données
│       ├── data_consolidator.py     ← Consolidation intelligente
│       ├── data_cleaner.py          ← Nettoyage des données
│       ├── data_enricher.py         ← Enrichissement des données
│       ├── data_validator.py        ← Validation des données
│       └── pipeline_orchestrator.py ← Orchestration modulaire
├── tests/                           ← Tests de validation
│   ├── __init__.py
│   ├── test_mongodb_connection.py   ← Test connexion MongoDB
│   ├── test_complete_pipeline.py    ← Test pipeline complet
│   ├── test_consolidation_strategy.py ← Test stratégie
│   ├── test_custom_config_integration.py ← Test intégration
│   ├── test_new_features.py         ← Test nouvelles fonctionnalités
│   ├── test_pipeline_complet.py     ← Test pipeline complet
│   └── test_pipeline_simplifie.py   ← Test pipeline simplifié
├── logs/                            ← Fichiers de log
├── docs/                            ← Documentation détaillée
├── examples/                        ← Exemples de requêtes MongoDB
├── dashboard/                       ← Dashboard de validation
├── export/                          ← Export des données
├── intelligence/                    ← Détection de similarités
├── performance/                     ← Optimisations de performance
├── validation/                      ← Validation des données
└── utils/                           ← Utilitaires
```

## 🎯 Utilisation Recommandée

### **Pipeline Modulaire Unifié (RECOMMANDÉ)**

```bash
# Utiliser le pipeline modulaire unifié
python3 main_modular_pipeline.py \
  --source mongodb \
  --mongodb-db real_estate_db \
  --mongodb-collection properties \
  --mongodb-query-file examples/query_trois_rivieres_triplex.json \
  --limit 100 \
  --output exports/ \
  --formats csv \
  --optimization medium
```

**Avantages :**

- ✅ Architecture modulaire et maintenable
- ✅ Composants spécialisés et réutilisables
- ✅ Performance optimisée avec modules externes
- ✅ Validation et rapports automatiques
- ✅ Export multi-formats avancé

### **Requêtes MongoDB via Fichier JSON**

```bash
# Utiliser un fichier JSON pour des requêtes complexes
python3 main_modular_pipeline.py \
  --source mongodb \
  --mongodb-db real_estate_db \
  --mongodb-collection properties \
  --mongodb-query-file examples/query_trois_rivieres_triplex.json \
  --limit 100 \
  --output exports/ \
  --formats csv \
  --optimization medium
```

**Avantages :**

- ✅ Pas de problèmes d'échappement du shell
- ✅ Requêtes MongoDB complexes supportées
- ✅ Lisibilité et réutilisabilité
- ✅ Versioning Git des requêtes

### **Architecture Modulaire (Programmatique)**

```python
from core import PipelineManager, DataProcessor, ExportManager

# Utilisez l'architecture modulaire
pipeline = PipelineManager(config)
processor = DataProcessor(pipeline)
exporter = ExportManager(pipeline)

# Traitement personnalisé
results = processor.process_data(df, config)
```

## ⚡ Options d'Optimisation

### **Niveaux d'optimisation disponibles :**

```bash
--optimization {light, medium, aggressive}
```

#### **🟢 LIGHT (léger)**

- **Mémoire** : Optimisations de base uniquement
- **Performance** : Traitement standard
- **Ressources** : Utilisation minimale
- **Idéal pour** : Tests, petits datasets, développement

#### **🟡 MEDIUM (moyen) - DÉFAUT**

- **Mémoire** : Optimisations avancées
- **Performance** : Traitement optimisé
- **Ressources** : Équilibre performance/ressources
- **Idéal pour** : Production, datasets moyens

#### **🔴 AGGRESSIVE (agressif)**

- **Mémoire** : Optimisations maximales
- **Performance** : Traitement ultra-optimisé
- **Ressources** : Utilisation intensive
- **Idéal pour** : Gros datasets, performance critique

### **Exemples d'utilisation :**

#### **Test rapide avec optimisation légère :**

```bash
python3 main_modular_pipeline.py \
  --source test \
  --output exports/test_light \
  --formats csv \
  --optimization light
```

#### **Production avec optimisation moyenne :**

```bash
python3 main_modular_pipeline.py \
  --source mongodb \
  --mongodb-db real_estate_db \
  --mongodb-collection properties \
  --mongodb-query-file examples/query_test_final.json \
  --limit 1000 \
  --output exports/production_medium \
  --formats csv json \
  --optimization medium
```

#### **Traitement intensif avec optimisation agressive :**

```bash
python3 main_modular_pipeline.py \
  --source mongodb \
  --mongodb-db real_estate_db \
  --mongodb-collection properties \
  --limit 10000 \
  --output exports/aggressive_processing \
  --formats csv parquet \
  --optimization aggressive \
  --parallel
```

## 🧪 Tests de Validation

### **Test du Pipeline Complet**

```bash
# Test avec données de test
python3 main_modular_pipeline.py --source test --output exports/test --formats csv

# Test avec MongoDB (si disponible)
python3 main_modular_pipeline.py --source mongodb --mongodb-db test_db --limit 10
```

### **Tests des Composants Individuels**

```bash
# Test de la connexion MongoDB
python3 tests/test_mongodb_connection.py

# Test du pipeline complet
python3 tests/test_complete_pipeline.py

# Test de la stratégie de consolidation
python3 tests/test_consolidation_strategy.py

# Test d'intégration de la config personnalisée
python3 tests/test_custom_config_integration.py
```

## 🔧 Configuration

### **Variables d'environnement**

```bash
# MongoDB
export MONGODB_URI="mongodb://localhost:27017/"
export MONGODB_DB="real_estate_db"

# Performance
export OPTIMIZATION_LEVEL="medium"
export PARALLEL_PROCESSING="true"
```

### **Fichier de configuration JSON**

```json
{
  "source": "mongodb",
  "mongodb_db": "real_estate_db",
  "mongodb_collection": "properties",
  "limit": 1000,
  "output": "exports/",
  "formats": ["csv", "json"],
  "optimization": "medium",
  "parallel": true
}
```

## 📊 Fonctionnalités

### **Sources de données supportées**

- **🗄️ MongoDB** : Extraction avec requêtes JSON complexes
- **📄 CSV** : Import de fichiers CSV
- **📋 JSON** : Import de fichiers JSON
- **🧪 Test** : Génération de données de test

### **Formats d'export supportés**

- **📊 CSV** : Export standard
- **📋 JSON** : Export structuré
- **🏗️ Parquet** : Export optimisé pour Big Data
- **🌍 GeoJSON** : Export géospatial (si GeoPandas disponible)
- **💾 HDF5** : Export haute performance (si H5Py disponible)

### **Validation des données**

- **📋 Validation de base** : Complétude, unicité, cohérence
- **🔧 Validation des types** : Types de données
- **✅ Validation des valeurs** : Plages, formats
- **🌍 Validation géographique** : Coordonnées, adresses
- **💼 Validation métier** : Règles spécifiques au domaine
- **🚨 Détection d'anomalies** : Valeurs aberrantes

## 🚀 Installation

### **Prérequis**

- Python 3.8+
- MongoDB (optionnel)
- pip

### **Installation des dépendances**

```bash
# Installation de base
pip install -r requirements.txt

# Installation avec optimisations
pip install -r requirements.txt
pip install dask modin numba pyarrow

# Installation pour le dashboard
pip install plotly seaborn
```

## 📈 Performance

### **Métriques typiques**

- **Extraction** : 1000 documents MongoDB en ~2s
- **Validation** : 1000 lignes en ~0.1s
- **Transformation** : Réduction de 30-40% des colonnes
- **Export** : CSV 1MB en ~0.01s

### **Optimisations disponibles**

- **Mémoire** : Gestion intelligente des types de données
- **Parallélisme** : Traitement multi-cœurs
- **Chunking** : Traitement par blocs
- **Compression** : Export compressé

## 🐛 Dépannage

### **Problèmes courants**

#### **Erreur de connexion MongoDB**

```bash
# Vérifier la connexion
python3 tests/test_mongodb_connection.py

# Vérifier les paramètres
echo $MONGODB_URI
echo $MONGODB_DB
```

#### **Erreur de mémoire**

```bash
# Utiliser l'optimisation light
--optimization light

# Réduire la limite
--limit 100
```

#### **Erreur de validation**

```bash
# Mode validation uniquement
--validate-only

# Mode dry run
--dry-run
```

## 📚 Documentation Complémentaire

- **📋 docs/INDEX.md** : Index de la documentation
- **🏗️ docs/ARCHITECTURE.md** : Architecture détaillée
- **⚙️ docs/CONFIGURATION.md** : Guide de configuration
- **🧪 docs/TESTS.md** : Guide des tests
- **🚀 docs/DEPLOYMENT.md** : Guide de déploiement

## 🤝 Contribution

### **Structure des tests**

```bash
# Exécuter tous les tests
python -m pytest tests/

# Test spécifique
python -m pytest tests/test_mongodb_connection.py

# Test avec couverture
python -m pytest --cov=core tests/
```

### **Standards de code**

- **PEP 8** : Style de code Python
- **Type hints** : Annotations de types
- **Docstrings** : Documentation des fonctions
- **Logging** : Logs structurés

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 👥 Auteurs

- **Pipeline ETL Modulaire Team**
- **Version** : 7.0.0
- **Dernière mise à jour** : Août 2025

---

## 🎯 Résumé des Changements

### **🔄 Migration depuis l'ancienne architecture :**

- ❌ `main_ultra_intelligent.py` → ✅ `main_modular_pipeline.py`
- ❌ `UltraIntelligentCleaner` → ✅ Architecture modulaire
- ❌ Classes monolithiques → ✅ Composants spécialisés
- ❌ Tests dispersés → ✅ Tests organisés dans `tests/`

### **🚀 Nouveautés :**

- **Architecture modulaire** : Composants interchangeables
- **Orchestrateur intégré** : Gestion unifiée des dépendances
- **Validation avancée** : Multi-niveaux de validation
- **Export multi-formats** : Support de formats spécialisés
- **Optimisations intelligentes** : Gestion automatique des ressources

### **📊 Avantages :**

- **Maintenabilité** : Code modulaire et testable
- **Performance** : Optimisations automatiques
- **Extensibilité** : Ajout facile de nouveaux composants
- **Robustesse** : Validation et gestion d'erreurs avancées
