# 📚 INDEX DE LA DOCUMENTATION - Pipeline Ultra-Intelligent

## 🎯 Vue d'ensemble

Ce pipeline ETL ultra-intelligent est conçu pour nettoyer, consolider et transformer des données immobilières avec une approche basée sur l'IA et la détection automatique de similarités.

## 📁 Structure de la Documentation

### 🔧 **Configuration et Utilisation**

- **[README.md](../README.md)** ← Documentation principale du projet
- **[README_FICHIER_JSON.md](README_FICHIER_JSON.md)** ← Guide des requêtes MongoDB via JSON
- **[GIT_IGNORE_GUIDE.md](GIT_IGNORE_GUIDE.md)** ← Guide du fichier .gitignore

### 🏗️ **Architecture et Design**

- **[INDEX.md](INDEX.md)** ← Vue d'ensemble de l'architecture
- **[STRUCTURE.md](STRUCTURE.md)** ← Structure détaillée du projet
- **[ARCHITECTURE.md](ARCHITECTURE.md)** ← Design patterns et composants

### 🔄 **Stratégies de Consolidation**

- **[CONSOLIDATION_STRATEGY_VALIDATION.md](CONSOLIDATION_STRATEGY_VALIDATION.md)** ← Validation des stratégies
- **[VARIABLE_CONSOLIDATION.md](VARIABLE_CONSOLIDATION.md)** ← Logique de consolidation
- **[CUSTOM_CONFIG_HARMONIZATION.md](CUSTOM_CONFIG_HARMONIZATION.md)** ← Harmonisation des configurations

### 📊 **Validation et Qualité**

- **[ALIGNMENT_ANALYSIS.md](ALIGNMENT_ANALYSIS.md)** ← Analyse d'alignement des données
- **[AUDIT_ALIGNMENT_COMPLETE.md](AUDIT_ALIGNMENT_COMPLETE.md)** ← Audit complet d'alignement
- **[CONFIGURATION.md](CONFIGURATION.md)** ← Guide de configuration

### 🚀 **Déploiement et Maintenance**

- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** ← Guide d'utilisation complet
- **[GIT_MANAGEMENT.md](GIT_MANAGEMENT.md)** ← Gestion Git et versions
- **[REORGANISATION_SUMMARY.md](REORGANISATION_SUMMARY.md)** ← Résumé des réorganisations

### 📋 **Spécifications Métier**

- **[real_estate_prompt.md](real_estate_prompt.md)** ← Spécifications immobilières
- **[CUSTOM_FIELDS_MAPPING.md](CUSTOM_FIELDS_MAPPING.md)** ← Mapping des champs personnalisés

## 🎯 **Nouvelles Fonctionnalités (v7.0.0)**

### 🗄️ **Requêtes MongoDB via Fichier JSON**

- **Argument** : `--mongodb-query-file`
- **Avantage** : Évite les problèmes d'échappement du shell
- **Support** : Requêtes complexes avec regex, opérateurs MongoDB
- **Exemples** : `examples/query_trois_rivieres_triplex.json`

### 🔧 **Parser JSON Robuste**

- **Méthodes multiples** : JSON standard, ast.literal_eval, parsing manuel
- **Gestion d'erreurs** : Fallback automatique en cas d'échec
- **Support MongoDB** : Opérateurs `$regex`, `$options`, objets imbriqués

## 🚀 **Démarrage Rapide**

### 1. **Installation**

```bash
pip install -r requirements.txt
```

### 2. **Test Simple**

```bash
python3 main_ultra_intelligent.py --source test --dry-run
```

### 3. **MongoDB avec Fichier JSON**

```bash
python3 main_ultra_intelligent.py \
  --source mongodb \
  --mongodb-query-file examples/query_trois_rivieres_triplex.json \
  --limit 100 \
  --output exports/ \
  --formats csv
```

## 📊 **Métriques de Performance**

- **Réduction colonnes** : 65%+ (objectif)
- **Temps d'exécution** : < 1 seconde pour 1000 lignes
- **Score qualité** : 90%+ (objectif)
- **Support formats** : CSV, Parquet, GeoJSON, HDF5

## 🔍 **Troubleshooting**

- **Logs détaillés** : `pipeline.log`
- **Mode verbose** : `--verbose`
- **Validation uniquement** : `--validate-only`
- **Mode test** : `--dry-run`

## 📞 **Support**

- **Documentation** : Ce répertoire `docs/`
- **Exemples** : Répertoire `examples/`
- **Tests** : Répertoire `tests/`
- **Configuration** : Répertoire `config/`
