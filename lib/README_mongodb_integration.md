# 🏠 Intégration MongoDB - Système d'Analyse Immobilière

## 📋 Vue d'ensemble

Ce guide explique comment utiliser le système d'analyse immobilière modulaire avec des données MongoDB provenant de Centris.ca. Le système a été optimisé pour traiter la structure spécifique des données immobilières québécoises.

## 🗄️ Structure des Données MongoDB

### Variables Numériques Principales

- **`price`** : Prix de vente (en dollars canadiens)
- **`living_area`** : Surface habitable (en pieds carrés)
- **`lot_size`** : Taille du terrain (en pieds carrés)
- **`municipal_evaluation_total`** : Évaluation municipale totale
- **`bedrooms`** : Nombre de chambres
- **`bathrooms`** : Nombre de salles de bain
- **`year_built`** : Année de construction

### Variables Catégorielles

- **`type`** : Type de propriété (Maison, Condo, Duplex, etc.)
- **`city`** : Ville
- **`region`** : Région administrative
- **`building_style`** : Style de construction

### Variables de Taxes

- **`municipal_tax`** : Taxes municipales
- **`school_tax`** : Taxes scolaires

## 🔧 Optimisations MongoDB

### Nettoyage Automatique

Le système supprime automatiquement les colonnes MongoDB non pertinentes :

- Métadonnées d'extraction (`extraction_metadata`)
- Identifiants et liens (`_id`, `link`, `images`)
- Données temporelles (`add_date`, `update_at`)
- Informations de courtier et agence

### Normalisation des Colonnes

Le système normalise automatiquement les colonnes dupliquées :

- `nb_bathroom` → `bathrooms`
- `nb_bedroom` → `bedrooms`
- `construction_year` → `year_built`
- `municipal_taxes` → `municipal_tax`
- `school_taxes` → `school_tax`

## 🚀 Utilisation avec MongoDB

### 1. Import des Données

```python
import pandas as pd
from pymongo import MongoClient
from lib import PropertyAnalyzer

# Connexion MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['realestate']
collection = db['properties']

# Charger les données
cursor = collection.find({})
df = pd.DataFrame(list(cursor))

print(f"Données chargées: {df.shape}")
```

### 2. Analyse Complète

```python
# Créer l'analyseur
analyzer = PropertyAnalyzer()

# Exécuter l'analyse
results = analyzer.analyze_properties(df, target_column='price')

# Accéder aux résultats
print(f"Variables sélectionnées: {results['selected_features']}")
print(f"Classification: {results['classification_stats']}")
```

### 3. Utilisation Modulaire

```python
from lib.data_processors import PropertyDataProcessor
from lib.classifiers import PropertyClassifier
from lib.feature_selectors import FeatureSelector

# Traitement des données
processor = PropertyDataProcessor()
df_clean = processor.clean_data(df)
df_encoded = processor.encode_features(df_clean)
df_imputed = processor.impute_missing_values(df_encoded)

# Classification
classifier = PropertyClassifier()
df_classified = classifier.classify_properties(df_imputed)

# Sélection de variables
selector = FeatureSelector()
X = df_classified.drop(columns=['price'])
y = df_classified['price']
selected_features = selector.select_features(X, y)
```

## 🏠 Classification des Propriétés

### Seuils Adaptés au Marché Québécois

| Catégorie      | Prix    | Surface Habitable | Salles de Bain | Évaluation Municipale |
| -------------- | ------- | ----------------- | -------------- | --------------------- |
| **Luxe**       | ≥ 1.5M$ | ≥ 3000 pi²        | ≥ 3            | ≥ 1M$                 |
| **Moyen-Haut** | ≥ 800k$ | ≥ 2000 pi²        | ≥ 2            | ≥ 600k$               |
| **Moyen**      | ≥ 500k$ | ≥ 1500 pi²        | ≥ 1            | ≥ 400k$               |
| **Économique** | < 500k$ | < 1500 pi²        | < 1            | < 400k$               |

### Méthodes de Classification

1. **Multi-critères** : Prix + Surface + Salles de bain + Évaluation
2. **Prix + Surface** : Si données limitées
3. **Prix uniquement** : En dernier recours

## 🎯 Sélection de Variables

### Algorithmes Utilisés

1. **Lasso (L1)** : Régularisation avec validation croisée
2. **Random Forest** : Importance des variables
3. **Combinaison** : Union des variables sélectionnées

### Variables Typiquement Sélectionnées

- `living_area` : Surface habitable
- `municipal_evaluation_total` : Évaluation municipale
- `bathrooms` : Nombre de salles de bain
- `bedrooms` : Nombre de chambres
- `year_built` : Année de construction
- `lot_size` : Taille du terrain
- `municipal_tax` : Taxes municipales

## 📊 Exemple d'Analyse Complète

```python
import pandas as pd
from lib import PropertyAnalyzer

# Charger les données MongoDB
df = pd.read_json('mongodb_export.json')  # ou depuis MongoDB

# Analyse complète
analyzer = PropertyAnalyzer()
results = analyzer.analyze_properties(df, target_column='price')

# Résultats détaillés
print("=== RÉSULTATS DE L'ANALYSE ===")
print(f"Propriétés analysées: {results['shape_original'][0]:,}")
print(f"Variables initiales: {results['shape_original'][1]}")
print(f"Variables finales: {results['shape_processed'][1]}")
print(f"Variables sélectionnées: {len(results['selected_features'])}")

# Classification
stats = results['classification_stats']
print("\n=== CLASSIFICATION ===")
for category, count in stats['counts'].items():
    pct = stats['percentages'][category]
    print(f"{category}: {count:,} propriétés ({pct:.1f}%)")

# Variables importantes
print("\n=== VARIABLES IMPORTANTES ===")
importance = results['feature_importance']
for feature, imp in sorted(importance.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{feature}: {imp:.4f}")
```

## 🧪 Tests et Validation

### Script de Test Intégré

```bash
# Test avec données factices
python test_mongodb_data.py

# Test du module principal
python -m lib.property_analysis
```

### Validation des Données

```python
from lib.validators import DataValidator

# Valider les données
if DataValidator.validate_target_column(df, 'price'):
    print("✅ Données valides")
else:
    print("❌ Problème avec les données")
```

## 🔍 Logs et Monitoring

Le système génère des logs détaillés pour chaque étape :

```
🧹 Nettoyage des données MongoDB...
🗑️ === ÉTAPE 2: SUPPRESSION DES COLONNES MONGODB ===
🔄 === ÉTAPE 5: NORMALISATION DES COLONNES ===
🏠 === CLASSIFICATION DES PROPRIÉTÉS MONGODB ===
🎯 === SÉLECTION DE VARIABLES ===
```

## 📈 Métriques de Performance

### Réduction Typique des Variables

- **Avant nettoyage** : 40-50 variables
- **Après nettoyage** : 15-25 variables
- **Après sélection** : 8-15 variables
- **Réduction totale** : 60-80%

### Temps d'Exécution

- **1000 propriétés** : ~30 secondes
- **10000 propriétés** : ~3 minutes
- **100000 propriétés** : ~30 minutes

## 🚨 Problèmes Courants

### Erreurs Fréquentes

1. **Colonne 'price' manquante**

   ```python
   # Vérifier la structure
   print(df.columns.tolist())
   ```

2. **Données non numériques**

   ```python
   # Convertir en numérique
   df['price'] = pd.to_numeric(df['price'], errors='coerce')
   ```

3. **Valeurs manquantes excessives**
   ```python
   # Ajuster le seuil
   processor = PropertyDataProcessor(missing_threshold=0.1)
   ```

## 🔧 Configuration Avancée

### Paramètres Personnalisés

```python
# Processeur avec seuil personnalisé
processor = PropertyDataProcessor(missing_threshold=0.1)

# Classificateur avec seuils personnalisés
classifier = PropertyClassifier()
classifier.classification_rules['luxe']['price_threshold'] = 2000000

# Sélecteur avec paramètres personnalisés
selector = FeatureSelector(
    cv_folds=10,
    rf_n_estimators=200,
    rf_threshold=0.005
)
```

---

**Version** : 2.0.0  
**Optimisé pour** : Données MongoDB Centris  
**Compatibilité** : Python 3.7+, MongoDB 4.0+  
**Dépendances** : pandas, numpy, scikit-learn, pymongo
