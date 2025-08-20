# 🚫 Guide du fichier .gitignore

Ce document explique la configuration du fichier `.gitignore` pour le pipeline ultra-intelligent.

## 🎯 **Objectif**

Le fichier `.gitignore` est configuré pour :

- **Exclure** les fichiers temporaires et de données volumineux
- **Protéger** les secrets et configurations locales
- **Garder** les fichiers de configuration et d'exemples importants
- **Optimiser** la taille du repository Git

## 📁 **Structure des exclusions**

### **📤 Sorties et résultats**

```
etl/clean_data/exports/          ← Dossiers d'export
etl/clean_data/logs/             ← Fichiers de log
etl/clean_data/backup/           ← Sauvegardes
etl/clean_data/data/             ← Données brutes
```

### **🗂️ Fichiers temporaires**

```
*.tmp                            ← Fichiers temporaires
*.temp                           ← Fichiers temporaires
*.cache                          ← Cache
*.log                            ← Logs
pipeline.log                     ← Log principal du pipeline
```

### **🐍 Python**

```
__pycache__/                     ← Cache Python
*.pyc                            ← Bytecode Python
*.pyo                            ← Bytecode Python optimisé
*.so                             ← Extensions C
```

### **🔥 Environnements virtuels**

```
.env                             ← Variables d'environnement
.venv/                           ← Environnement virtuel
venv/                            ← Environnement virtuel
env/                             ← Environnement virtuel
```

### **📊 Données volumineuses**

```
*.csv                            ← Fichiers CSV
*.xlsx                           ← Fichiers Excel
*.parquet                        ← Fichiers Parquet
*.h5                             ← Fichiers HDF5
*.json                           ← Fichiers JSON (avec exceptions)
*.geojson                        ← Fichiers GeoJSON
```

## ✅ **Exceptions importantes**

### **Fichiers JSON conservés**

```
!etl/clean_data/examples/*.json  ← Exemples de requêtes MongoDB
!etl/clean_data/config/*.json    ← Configuration du pipeline
!etl/clean_data/config/*.yaml    ← Configuration YAML
!etl/clean_data/config/*.yml     ← Configuration YAML
```

### **Fichiers de configuration conservés**

```
etl/clean_data/examples/         ← Exemples de requêtes
etl/clean_data/config/           ← Configuration du pipeline
etl/clean_data/docs/             ← Documentation
etl/clean_data/README.md         ← Documentation principale
```

## 🚫 **Fichiers exclus par sécurité**

### **Secrets et configuration locale**

```
etl/clean_data/config/local_*.py ← Configuration locale
etl/clean_data/config/secrets.py ← Fichiers de secrets
etl/clean_data/.env              ← Variables d'environnement
etl/clean_data/.env.*            ← Variables d'environnement
```

### **Tests et fichiers temporaires**

```
etl/clean_data/test_*.py         ← Fichiers de test
etl/clean_data/debug_*.py        ← Fichiers de debug
etl/clean_data/temp_*.py         ← Fichiers temporaires
etl/clean_data/*_test.py         ← Fichiers de test
```

### **Cache et builds**

```
etl/clean_data/__pycache__/      ← Cache Python
etl/clean_data/*/__pycache__/    ← Cache Python des sous-modules
etl/clean_data/*.log             ← Logs
etl/clean_data/*.tmp             ← Fichiers temporaires
```

## 🔍 **Vérification du .gitignore**

### **Tester l'exclusion d'un fichier**

```bash
# Créer un fichier temporaire
echo "test" > etl/clean_data/test_temp.py

# Vérifier le statut Git
git status etl/clean_data/test_temp.py

# Le fichier devrait être ignoré (non affiché)
```

### **Tester l'inclusion d'un fichier d'exemple**

```bash
# Créer un fichier d'exemple
echo '{"test": "value"}' > etl/clean_data/examples/test.json

# Vérifier le statut Git
git status etl/clean_data/examples/test.json

# Le fichier devrait être visible (non ignoré)
```

## 📋 **Bonnes pratiques**

### **✅ À faire**

- **Committer** les fichiers de configuration
- **Committer** les exemples et la documentation
- **Committer** le code source principal
- **Committer** les tests unitaires

### **❌ À éviter**

- **Committer** les fichiers de données volumineux
- **Committer** les logs et fichiers temporaires
- **Committer** les secrets et configurations locales
- **Committer** les fichiers de cache Python

### **🔄 Maintenance**

- **Mettre à jour** le `.gitignore` lors de l'ajout de nouveaux types de fichiers
- **Tester** les exclusions avec `git status --ignored`
- **Documenter** les nouvelles règles d'exclusion
- **Vérifier** que les fichiers importants ne sont pas ignorés

## 🚨 **Dépannage**

### **Fichier ignoré par erreur**

Si un fichier important est ignoré :

1. **Vérifier** la règle dans `.gitignore`
2. **Ajouter** une exception avec `!`
3. **Tester** avec `git status`
4. **Committer** le changement

### **Fichier non ignoré**

Si un fichier temporaire n'est pas ignoré :

1. **Vérifier** la règle dans `.gitignore`
2. **Ajouter** la règle appropriée
3. **Tester** avec `git status`
4. **Committer** le changement

### **Règles en conflit**

Si des règles se contredisent :

1. **L'ordre** dans `.gitignore` est important
2. **Les exceptions** (`!`) ont la priorité
3. **Tester** avec `git status --ignored`
4. **Ajuster** l'ordre des règles si nécessaire

## 📚 **Ressources**

- **Documentation Git** : [git-scm.com/docs/gitignore](https://git-scm.com/docs/gitignore)
- **Patterns glob** : [git-scm.com/docs/gitignore#\_pattern_format](https://git-scm.com/docs/gitignore#_pattern_format)
- **Exemples** : [github.com/github/gitignore](https://github.com/github/gitignore)
