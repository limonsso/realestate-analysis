# 📖 Guide d'Utilisation - Pipeline ETL Ultra-Intelligent

## 🎯 Vue d'ensemble

Ce guide détaille l'utilisation complète du pipeline ETL ultra-intelligent pour la consolidation des variables immobilières. Le pipeline transforme automatiquement 50+ colonnes en 20-25 colonnes consolidées avec une récupération massive des données manquantes.

## 🚀 Démarrage Rapide

### Installation et test

```bash
# 1. Vérifier l'installation
python main_ultra_intelligent.py --help

# 2. Test rapide avec données synthétiques
python main_ultra_intelligent.py --source test --output exports/ --formats csv

# 3. Vérifier les résultats
ls exports/
```

### Premier pipeline MongoDB

```bash
# Pipeline MongoDB basique
python main_ultra_intelligent.py \
  --source mongodb \
  --mongodb-db real_estate_db \
  --mongodb-collection properties \
  --limit 100 \
  --output exports/ \
  --formats csv \
  --verbose
```

## 📊 Sources de Données Supportées

### 1. MongoDB 🗄️

#### Connexion basique
```bash
python main_ultra_intelligent.py \
  --source mongodb \
  --output exports/
```

#### Connexion avec paramètres spécifiques
```bash
python main_ultra_intelligent.py \
  --source mongodb \
  --source-path "mongodb://user:pass@host:port" \
  --mongodb-db real_estate_db \
  --mongodb-collection properties \
  --mongodb-query '{"type": "triplex"}' \
  --limit 1000 \
  --output exports/
```

#### Paramètres MongoDB
- `--source-path` : Chaîne de connexion MongoDB
- `--mongodb-db` : Nom de la base de données
- `--mongodb-collection` : Nom de la collection
- `--mongodb-query` : Requête JSON de filtrage
- `--limit` : Nombre maximum de documents à traiter

### 2. Fichiers CSV 📄

```bash
python main_ultra_intelligent.py \
  --source csv \
  --source-path data/properties.csv \
  --output exports/ \
  --formats parquet,csv
```

### 3. Fichiers JSON 🔧

```bash
python main_ultra_intelligent.py \
  --source json \
  --source-path data/properties.json \
  --output exports/ \
  --formats csv,json
```

### 4. Données de Test 🧪

```bash
python main_ultra_intelligent.py \
  --source test \
  --output exports/ \
  --formats csv,parquet
```

## ⚙️ Configuration des Optimisations

### Niveaux d'optimisation

#### Light (rapide)
```bash
python main_ultra_intelligent.py \
  --source test \
  --optimization light \
  --output exports/
```

#### Medium (équilibré) - **Recommandé**
```bash
python main_ultra_intelligent.py \
  --source test \
  --optimization medium \
  --output exports/
```

#### Aggressive (maximal)
```bash
python main_ultra_intelligent.py \
  --source test \
  --optimization aggressive \
  --parallel \
  --output exports/
```

### Options de performance

```bash
# Traitement parallèle
python main_ultra_intelligent.py --source test --parallel

# Export par chunks (gros datasets)
python main_ultra_intelligent.py --source test --chunked

# Combinaison des optimisations
python main_ultra_intelligent.py \
  --source test \
  --optimization aggressive \
  --parallel \
  --chunked \
  --output exports/
```

## 🔍 Modes d'Exécution

### Pipeline complet (par défaut)
```bash
python main_ultra_intelligent.py --source test --output exports/
```

### Validation uniquement
```bash
python main_ultra_intelligent.py \
  --source test \
  --validate-only \
  --verbose
```

### Mode simulation (dry-run)
```bash
python main_ultra_intelligent.py \
  --source test \
  --dry-run \
  --verbose
```

### Mode verbeux
```bash
python main_ultra_intelligent.py \
  --source test \
  --verbose \
  --output exports/
```

## 📤 Formats d'Export

### Formats disponibles

```bash
# Export CSV uniquement
python main_ultra_intelligent.py --source test --formats csv

# Export multiple
python main_ultra_intelligent.py \
  --source test \
  --formats parquet,csv,json

# Tous les formats
python main_ultra_intelligent.py \
  --source test \
  --formats parquet,csv,geojson,hdf5,excel,json,pickle
```

### Formats par dépendance

| Format | Dépendance | Installation |
|--------|------------|--------------|
| CSV | pandas | ✅ Inclus |
| Parquet | pyarrow | `pip install pyarrow` |
| GeoJSON | geopandas | `pip install geopandas` |
| HDF5 | h5py | `pip install h5py` |
| Excel | openpyxl | `pip install openpyxl` |
| JSON | json | ✅ Inclus |
| Pickle | pickle | ✅ Inclus |

## 📊 Exemples d'Utilisation Avancés

### Pipeline de production MongoDB
```bash
python main_ultra_intelligent.py \
  --source mongodb \
  --source-path "mongodb://prod-server:27017" \
  --mongodb-db real_estate_prod \
  --mongodb-collection properties \
  --mongodb-query '{"status": "active", "price": {"$gt": 100000}}' \
  --limit 5000 \
  --optimization aggressive \
  --parallel \
  --output production_exports/ \
  --formats parquet,csv \
  --verbose
```

### Pipeline de validation rapide
```bash
python main_ultra_intelligent.py \
  --source csv \
  --source-path data/sample_100.csv \
  --validate-only \
  --verbose \
  --output validation_reports/
```

### Pipeline de test avec limitation
```bash
python main_ultra_intelligent.py \
  --source test \
  --limit 100 \
  --optimization light \
  --output test_exports/ \
  --formats csv \
  --dry-run
```

## 🔧 Gestion des Erreurs

### Erreurs MongoDB courantes

#### Connexion échouée
```bash
# Le pipeline bascule automatiquement vers les données de test
python main_ultra_intelligent.py \
  --source mongodb \
  --source-path "mongodb://invalid-host:27017" \
  --verbose
```

#### Requête invalide
```bash
# Erreur JSON - utilisation de la requête par défaut
python main_ultra_intelligent.py \
  --source mongodb \
  --mongodb-query '{"invalid": json}' \
  --verbose
```

### Erreurs de dépendances

#### PyArrow manquant
```bash
# Installation de PyArrow pour l'export Parquet
pip install pyarrow

# Ou utiliser uniquement CSV
python main_ultra_intelligent.py --source test --formats csv
```

#### GeoPandas manquant
```bash
# Installation de GeoPandas pour l'export GeoJSON
pip install geopandas

# Ou exclure GeoJSON
python main_ultra_intelligent.py --source test --formats parquet,csv
```

## 📈 Monitoring et Logs

### Niveaux de logging

#### Mode normal
```bash
python main_ultra_intelligent.py --source test --output exports/
```

#### Mode verbeux
```bash
python main_ultra_intelligent.py --source test --verbose --output exports/
```

#### Mode debug
```bash
# Configuration manuelle du logging
import logging
logging.getLogger().setLevel(logging.DEBUG)

python main_ultra_intelligent.py --source test --verbose --output exports/
```

### Fichiers de logs

- **Console** : Sortie en temps réel
- **Fichiers d'export** : Rapports détaillés
- **Logs système** : Traçabilité complète

## 🎯 Bonnes Pratiques

### 1. Commencer petit
```bash
# Test avec 100 documents
python main_ultra_intelligent.py --source test --limit 100 --output test/

# Puis augmenter progressivement
python main_ultra_intelligent.py --source test --limit 1000 --output test/
```

### 2. Utiliser le mode dry-run
```bash
# Simulation avant exécution
python main_ultra_intelligent.py --source test --dry-run --verbose
```

### 3. Valider d'abord
```bash
# Validation sans transformation
python main_ultra_intelligent.py --source test --validate-only --verbose
```

### 4. Optimiser progressivement
```bash
# Commencer light
python main_ultra_intelligent.py --source test --optimization light

# Puis medium
python main_ultra_intelligent.py --source test --optimization medium

# Enfin aggressive si nécessaire
python main_ultra_intelligent.py --source test --optimization aggressive
```

## 🔍 Dépannage

### Problèmes courants

#### Pipeline lent
```bash
# Vérifier l'optimisation
python main_ultra_intelligent.py --source test --optimization aggressive --parallel

# Réduire la taille des données
python main_ultra_intelligent.py --source test --limit 500
```

#### Erreurs de mémoire
```bash
# Utiliser le mode chunked
python main_ultra_intelligent.py --source test --chunked

# Réduire la taille des données
python main_ultra_intelligent.py --source test --limit 1000
```

#### Export échoué
```bash
# Vérifier les formats supportés
python main_ultra_intelligent.py --source test --formats csv

# Installer les dépendances manquantes
pip install pyarrow geopandas h5py openpyxl
```

## 📚 Ressources Additionnelles

### Documentation technique
- [Architecture du Pipeline](ARCHITECTURE.md)
- [Structure du Projet](STRUCTURE.md)
- [Configuration](CONFIGURATION.md)
- [API Reference](API_REFERENCE.md)

### Exemples et tutoriels
- [Exemples MongoDB](EXAMPLES_MONGODB.md)
- [Exemples CSV](EXAMPLES_CSV.md)
- [Cas d'usage](USE_CASES.md)

### Support et communauté
- [FAQ](FAQ.md)
- [Dépannage](TROUBLESHOOTING.md)
- [Contributions](CONTRIBUTING.md)

---

**🚀 Pipeline ETL Ultra-Intelligent v7.0.0** - Guide d'utilisation complet
