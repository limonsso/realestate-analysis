# 🚀 PIPELINE DE CONSOLIDATION DE DONNÉES - Architecture Modulaire Unifiée

## 📁 Structure du Projet

```
etl/data-consolidation-pipeline/
├── README.md                        ← Documentation principale
├── requirements.txt                 ← Dépendances Python
├── main_modular_pipeline.py        ← Point d'entrée principal (NOUVEAU)
├── config/                          ← Configuration du pipeline
│   ├── __init__.py
│   ├── consolidation_config.py      ← Configuration de base (30 groupes)
│   └── custom_fields_config.py     ← Configuration personnalisée (67 champs)
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

## 📊 Fonctionnalités Principales

- **🔗 Consolidation Avancée** : 30+ groupes de consolidation
- **⚡ Performance Optimisée** : Dask, Modin, Numba, PyArrow
- **🌍 Clustering Spatial** : DBSCAN pour zones géographiques
- **🏷️ Catégorisation Automatique** : ROI, prix, opportunités
- **📊 Dashboard Interactif** : Validation visuelle avec Plotly
- **🔧 Configuration Flexible** : Standard + Personnalisée
- **🗄️ Requêtes MongoDB Avancées** : Support des fichiers JSON pour requêtes complexes
