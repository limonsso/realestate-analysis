# 🐍 GUIDE D'UTILISATION DE L'ENVIRONNEMENT VIRTUEL

## 🚀 CRÉATION ET ACTIVATION

### **1. Création de l'environnement :**

```bash
python3 -m venv venv_pipeline
```

### **2. Activation de l'environnement :**

#### **Sur macOS/Linux :**

```bash
source venv_pipeline/bin/activate
```

#### **Sur Windows :**

```bash
venv_pipeline\Scripts\activate
```

### **3. Vérification de l'activation :**

```bash
which python
pip --version
```

## 📦 INSTALLATION DES DÉPENDANCES

### **Installation complète :**

```bash
pip install -r requirements.txt
```

### **Installation par étapes :**

```bash
# Core data science
pip install pandas numpy scipy

# Machine learning
pip install scikit-learn great-expectations ydata-profiling

# MongoDB
pip install pymongo dnspython

# Visualisation
pip install plotly matplotlib seaborn

# Utilitaires
pip install fuzzywuzzy python-Levenshtein
```

## 🔧 UTILISATION DU PIPELINE

### **1. Activation de l'environnement :**

```bash
source venv_pipeline/bin/activate
```

### **2. Test du pipeline :**

```bash
cd etl/data-consolidation-pipeline
python3 main_modular_pipeline.py --help
```

### **3. Exécution d'un test :**

```bash
python3 main_modular_pipeline.py --source test --limit 10 --output exports/test_venv
```

## 🧹 MAINTENANCE

### **Désactivation :**

```bash
deactivate
```

### **Mise à jour des dépendances :**

```bash
pip install --upgrade -r requirements.txt
```

### **Suppression de l'environnement :**

```bash
rm -rf venv_pipeline
```

## ⚠️ NOTES IMPORTANTES

- **Toujours activer l'environnement** avant d'utiliser le pipeline
- **Utiliser `pip`** au lieu de `pip3` dans l'environnement activé
- **Vérifier les versions** avec `pip list` après installation
- **Conserver `requirements.txt`** à jour avec `pip freeze > requirements.txt`

## 🎯 AVANTAGES DE CET ENVIRONNEMENT

✅ **Pas de conflits** avec l'environnement système  
✅ **Dépendances isolées** et contrôlées  
✅ **Reproductibilité** garantie  
✅ **Facilité de déploiement**  
✅ **Gestion des versions** simplifiée
