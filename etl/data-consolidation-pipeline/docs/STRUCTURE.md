# 🏗️ Structure Organisée du Projet de Nettoyage Immobilier

## 📁 Organisation des Dossiers

```
etl/clean_data/
├── 📥 inputs/                    # Données d'entrée
│   └── sample_real_estate_data.csv
├── 📤 outputs/                   # Tous les fichiers de sortie
│   ├── 🗂️ cleaned_data/         # Données nettoyées (CSV, Parquet, JSON, GeoJSON)
│   ├── 📊 reports/              # Rapports de qualité et analyses
│   └── 📝 logs/                 # Fichiers de logs
├── ⚙️ config.py                  # Configuration des chemins
├── 🧹 real_estate_data_cleaning.py      # Script principal de nettoyage
├── 🧹 real_estate_data_cleaning_simple.py # Version simplifiée
├── 🧪 test_cleaning.py          # Tests du système de nettoyage
├── 🧪 test_organized_structure.py # Tests de la structure
├── 📋 README.md                  # Documentation principale
├── 📋 STRUCTURE.md               # Ce fichier
└── 📋 real_estate_prompt.md     # Spécifications du projet
```

## 🎯 Avantages de cette Structure

### ✅ **Organisation Claire**
- **Inputs** : Tous les fichiers de données d'entrée
- **Outputs** : Tous les fichiers générés organisés par type
- **Scripts** : Code source et tests séparés des données

### ✅ **Facilité de Maintenance**
- Pas de mélange entre données et code
- Logs centralisés dans un dossier dédié
- Rapports organisés et facilement accessibles

### ✅ **Réutilisabilité**
- Structure standardisée pour d'autres projets
- Configuration centralisée dans `config.py`
- Chemins automatiquement créés

## 🚀 Utilisation

### 📥 **Ajouter des Données**
1. Placez vos fichiers CSV/Excel dans le dossier `inputs/`
2. Le script détectera automatiquement `sample_real_estate_data.csv`
3. Ou spécifiez un fichier personnalisé : `python real_estate_data_cleaning.py --input inputs/votre_fichier.csv`

### 📤 **Récupérer les Résultats**
- **Données nettoyées** : `outputs/cleaned_data/`
- **Rapports de qualité** : `outputs/reports/`
- **Logs d'exécution** : `outputs/logs/`

### ⚙️ **Configuration**
```python
from config import INPUT_DIR, OUTPUT_DIR, CLEANED_DATA_DIR

# Utiliser les chemins configurés
input_file = INPUT_DIR / "mon_fichier.csv"
output_file = CLEANED_DATA_DIR / "resultat.parquet"
```

## 🔧 Personnalisation

### 📂 **Ajouter de Nouveaux Dossiers**
Modifiez `config.py` :
```python
# Ajouter un nouveau dossier
NEW_DIR = OUTPUT_DIR / "nouveau_dossier"

# L'ajouter à la liste des dossiers à créer
directories = [INPUT_DIR, OUTPUT_DIR, CLEANED_DATA_DIR, REPORTS_DIR, LOGS_DIR, NEW_DIR]
```

### 🎨 **Modifier les Formats de Sortie**
Dans `config.py` :
```python
SUPPORTED_OUTPUT_FORMATS = {
    'csv': '.csv',
    'parquet': '.parquet',
    'json': '.json',
    'geojson': '.geojson',
    'excel': '.xlsx'  # Nouveau format
}
```

## 📊 Formats de Sortie Supportés

| Format | Extension | Usage | Taille |
|--------|-----------|-------|---------|
| **CSV** | `.csv` | Compatibilité universelle, Excel | ~5.7 MB |
| **Parquet** | `.parquet` | Performance Python, pandas | ~0.9 MB |
| **JSON** | `.json` | Applications web, API | ~8.8 MB |
| **GeoJSON** | `.geojson` | Cartes interactives, GIS | ~8.5 MB |

## 🧪 Tests

### ✅ **Tester la Structure**
```bash
python test_organized_structure.py
```

### ✅ **Tester le Nettoyage**
```bash
python test_cleaning.py
```

### ✅ **Exécuter le Pipeline Complet**
```bash
python real_estate_data_cleaning.py
```

## 🔍 Surveillance

### 📝 **Logs Automatiques**
- Tous les logs sont sauvegardés dans `outputs/logs/`
- Format : `cleaning_log_username.log`
- Niveau : INFO par défaut

### 📊 **Rapports de Qualité**
- Générés automatiquement après chaque nettoyage
- Sauvegardés dans `outputs/reports/`
- Format JSON avec métriques détaillées

## 🎉 Résultats

Cette structure organisée permet :
- **🎯 Clarté** : Chaque fichier a sa place logique
- **🔄 Maintenance** : Facile de nettoyer et organiser
- **📈 Évolutivité** : Simple d'ajouter de nouveaux formats
- **👥 Collaboration** : Structure claire pour l'équipe
- **🚀 Production** : Prêt pour la mise en production

---

*Structure créée le 19 août 2025 - Projet de nettoyage immobilier québécois* 🏠✨
