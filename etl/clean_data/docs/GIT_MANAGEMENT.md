# 🔒 Gestion Git et Fichiers Ignorés

## 🎯 **Objectif**

Ce document explique comment gérer les fichiers dans Git pour éviter de committer des données sensibles, des fichiers temporaires ou des résultats de traitement.

## 📍 **Gestion Centralisée du .gitignore**

Le projet utilise un **`.gitignore` centralisé** à la racine du repository qui couvre tous les dossiers et sous-dossiers. Cette approche offre plusieurs avantages :

- **🔄 Cohérence** : Mêmes règles pour tout le projet
- **📁 Simplicité** : Un seul fichier à maintenir
- **🎯 Couverture complète** : Tous les dossiers sont protégés
- **🛠️ Maintenance** : Modifications centralisées

## 🚫 **Fichiers Ignorés par Git**

> 📍 **Note** : Le projet utilise un `.gitignore` centralisé à la racine qui couvre tous les dossiers du projet.

### 📤 **Dossiers de Sortie (Exclus)**

```
etl/clean_data/outputs/           # ❌ Tous les résultats
├── cleaned_data/                 # ❌ Données nettoyées
├── reports/                      # ❌ Rapports de qualité
└── logs/                         # ❌ Fichiers de logs
```

**Pourquoi les exclure ?**

- **Taille** : Fichiers potentiellement volumineux
- **Génération** : Créés automatiquement lors de l'exécution
- **Données sensibles** : Peuvent contenir des informations privées
- **Performance** : Ralentissent les opérations Git

### 🗂️ **Fichiers Temporaires (Exclus)**

```
*.tmp                      # ❌ Fichiers temporaires
*.temp                     # ❌ Fichiers temporaires
*.cache                    # ❌ Cache
*.log                      # ❌ Logs d'exécution
```

### 🐍 **Python (Exclus)**

```
__pycache__/              # ❌ Cache Python
*.pyc                     # ❌ Bytecode Python
*.pyo                     # ❌ Bytecode Python optimisé
*.egg-info/               # ❌ Métadonnées de packages
```

### 🔥 **Environnements Virtuels (Exclus)**

```
.env                      # ❌ Variables d'environnement
.venv/                    # ❌ Environnement virtuel
venv/                     # ❌ Environnement virtuel
```

### 📊 **Données et Fichiers Volumineux (Exclus)**

```
*.csv                     # ❌ Données CSV
*.xlsx                    # ❌ Données Excel
*.parquet                 # ❌ Données Parquet
*.json                    # ❌ Données JSON
*.geojson                 # ❌ Données géospatiales
```

## ✅ **Fichiers Inclus dans Git**

### 🏗️ **Code Source**

```
src/                      # ✅ Code source modulaire
├── core/                 # ✅ Composants principaux
├── exporters/            # ✅ Modules d'export
├── validators/           # ✅ Modules de validation
└── utils/                # ✅ Utilitaires
```

### 📚 **Documentation**

```
docs/                     # ✅ Documentation complète
├── README.md             # ✅ Guide principal
├── INDEX.md              # ✅ Index des documents
├── STRUCTURE.md          # ✅ Organisation des dossiers
└── ARCHITECTURE.md       # ✅ Architecture modulaire
```

### 🛠️ **Scripts et Configuration**

```
scripts/                  # ✅ Scripts utilitaires
├── run_scripts.py        # ✅ Script principal
├── validate_specifications.py # ✅ Validation
└── cleanup_structure.py  # ✅ Nettoyage
```

### 🧪 **Tests**

```
tests/                    # ✅ Tests unitaires
├── test_cleaning.py      # ✅ Tests de nettoyage
└── test_organized_structure.py # ✅ Tests de structure
```

### 📋 **Configuration et Métadonnées**

```
main.py                   # ✅ Point d'entrée principal
requirements.txt          # ✅ Dépendances Python
README.md                 # ✅ Documentation principale
.gitignore               # ✅ Règles d'exclusion Git
```

## 🔧 **Gestion des Fichiers d'Entrée**

### 📥 **Données d'Exemple**

```
inputs/
└── sample_real_estate_data.csv  # ⚠️ À évaluer
```

**Recommandations :**

- **Petits fichiers d'exemple** (< 1MB) : ✅ Peuvent être inclus
- **Fichiers volumineux** (> 1MB) : ❌ Exclure avec `.gitignore`
- **Données sensibles** : ❌ Toujours exclure
- **Données publiques** : ✅ Peuvent être incluses

### 🔄 **Workflow Recommandé**

1. **Développement** : Utiliser des données d'exemple petites
2. **Tests** : Créer des datasets de test synthétiques
3. **Production** : Données dans des dossiers exclus de Git
4. **Partage** : Utiliser des liens vers les données originales

## 📝 **Commandes Git Utiles**

### 🔍 **Vérifier les Fichiers Ignorés**

```bash
# Voir quels fichiers sont ignorés
git status --ignored

# Vérifier si un fichier est ignoré
git check-ignore -v nom_du_fichier
```

### 🧹 **Nettoyer les Fichiers Ignorés**

```bash
# Supprimer les fichiers ignorés du suivi Git
git clean -fd

# Voir ce qui serait supprimé (dry run)
git clean -fd --dry-run
```

### 📦 **Gérer les Fichiers Volumineux**

```bash
# Ajouter un fichier volumineux au .gitignore
echo "mon_fichier_volumineux.csv" >> .gitignore

# Supprimer un fichier déjà suivi par Git
git rm --cached mon_fichier_volumineux.csv
```

## 🚨 **Bonnes Pratiques**

### ✅ **À Faire**

- **Toujours** vérifier le `.gitignore` avant de committer
- **Utiliser** des données d'exemple petites et publiques
- **Documenter** la source des données d'exemple
- **Tester** le `.gitignore` avec `git status --ignored`

### ❌ **À Éviter**

- **Jamais** committer des données sensibles
- **Jamais** committer des fichiers volumineux
- **Jamais** committer des fichiers temporaires
- **Jamais** committer des environnements virtuels

### 🔄 **Maintenance**

- **Mettre à jour** le `.gitignore` quand de nouveaux types de fichiers sont ajoutés
- **Vérifier** régulièrement que les bonnes règles sont en place
- **Former** l'équipe sur les bonnes pratiques Git

## 📊 **Structure Recommandée pour Git**

```
etl/clean_data/           # ✅ Inclus dans Git
├── src/                  # ✅ Code source
├── docs/                 # ✅ Documentation
├── scripts/              # ✅ Scripts utilitaires
├── tests/                # ✅ Tests
├── inputs/               # ⚠️ Données d'exemple (petites)
├── main.py               # ✅ Point d'entrée
├── requirements.txt      # ✅ Dépendances
└── README.md             # ✅ Documentation

# ❌ Exclus de Git (via .gitignore centralisé)
etl/clean_data/outputs/   # ❌ Résultats et sorties
etl/clean_data/__pycache__/ # ❌ Cache Python
.env                      # ❌ Variables d'environnement
*.log                     # ❌ Fichiers de logs
```

## 📍 **Localisation du .gitignore**

```
realestate-analysis/      # 📁 Racine du projet
├── .gitignore           # 🎯 Fichier principal (ICI)
├── etl/
│   └── clean_data/      # 📁 Projet de nettoyage
│       ├── src/         # ✅ Inclus dans Git
│       ├── docs/        # ✅ Inclus dans Git
│       └── outputs/     # ❌ Exclu via .gitignore racine
└── dashboard/           # 📁 Dashboard React
    └── node_modules/    # ❌ Exclu via .gitignore racine
```

## 🎯 **Conclusion**

Une gestion Git appropriée garantit :

- **🔒 Sécurité** : Pas de données sensibles exposées
- **📦 Performance** : Repository léger et rapide
- **🔄 Collaboration** : Équipe peut cloner et travailler efficacement
- **📚 Clarté** : Distinction claire entre code et données

**Suivez ces règles pour maintenir un repository Git propre et professionnel !** ✨

---

_Guide de gestion Git créé le 19 août 2025 - Projet de nettoyage immobilier québécois_ 🏠✨
