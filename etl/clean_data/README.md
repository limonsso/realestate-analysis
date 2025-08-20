# 🚀 PIPELINE ULTRA-INTELLIGENT - Nettoyage et Consolidation de Données Immobilières

## 📁 Structure du Projet

```
etl/clean_data/
├── README.md                        ← Documentation principale
├── requirements.txt                 ← Dépendances Python
├── main_ultra_intelligent.py       ← Point d'entrée principal
├── config/                          ← Configuration du pipeline
│   ├── __init__.py
│   ├── consolidation_config.py      ← Configuration de base (30 groupes)
│   └── custom_fields_config.py     ← Configuration personnalisée (67 champs)
├── core/                            ← Logique métier principale
│   ├── __init__.py
│   └── ultra_intelligent_cleaner.py
├── tests/                           ← Tests de validation
│   ├── __init__.py
│   ├── test_consolidation_strategy.py
│   ├── test_custom_config_integration.py
│   └── test_new_features.py
├── logs/                            ← Fichiers de log
│   └── pipeline.log
├── docs/                            ← Documentation détaillée
│   ├── INDEX.md
│   ├── real_estate_prompt.md
│   ├── CONSOLIDATION_STRATEGY_VALIDATION.md
│   ├── CUSTOM_CONFIG_HARMONIZATION.md
│   └── README_FICHIER_JSON.md      ← Guide requêtes MongoDB via JSON
├── examples/                        ← Exemples de requêtes MongoDB
│   ├── query_trois_rivieres_triplex.json
│   └── query_montreal_triplex.json
├── dashboard/                       ← Dashboard de validation
├── export/                          ← Export des données
├── intelligence/                    ← Détection de similarités
├── performance/                     ← Optimisations de performance
├── validation/                      ← Validation des données
└── utils/                           ← Utilitaires
```

## 🎯 Utilisation Recommandée

### **Requêtes MongoDB via Fichier JSON**

```bash
# Utiliser un fichier JSON pour des requêtes complexes
python3 main_ultra_intelligent.py \
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

### **Configuration Personnalisée (67 champs)**

```python
from config.custom_fields_config import custom_config
from core.ultra_intelligent_cleaner import UltraIntelligentCleaner

# Utilisez votre configuration personnalisée
cleaner = UltraIntelligentCleaner(custom_config)
```

### **Configuration Standard (78 colonnes)**

```python
from config.consolidation_config import ConsolidationConfig
from core.ultra_intelligent_cleaner import UltraIntelligentCleaner

# Utilisez la configuration standard
config = ConsolidationConfig()
cleaner = UltraIntelligentCleaner(config)
```

## 🧪 Tests de Validation

### **Exécution des Tests**

```bash
# Test de la stratégie de consolidation
python tests/test_consolidation_strategy.py

# Test d'intégration de la config personnalisée
python tests/test_custom_config_integration.py

# Test des nouvelles fonctionnalités
python tests/test_new_features.py
```

## 📊 Fonctionnalités Principales

- **🔗 Consolidation Avancée** : 30+ groupes de consolidation
- **⚡ Performance Optimisée** : Dask, Modin, Numba, PyArrow
- **🌍 Clustering Spatial** : DBSCAN pour zones géographiques
- **🏷️ Catégorisation Automatique** : ROI, prix, opportunités
- **📊 Dashboard Interactif** : Validation visuelle avec Plotly
- **🔧 Configuration Flexible** : Standard + Personnalisée
- **🗄️ Requêtes MongoDB Avancées** : Support des fichiers JSON pour requêtes complexes
