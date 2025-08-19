# 🏗️ Architecture Modulaire d'Analyse des Propriétés

## 📋 Vue d'ensemble

Cette architecture modulaire respecte les **principes SOLID** pour une analyse des propriétés immobilières maintenable, extensible et testable.

## 🏛️ Architecture des Classes

### Interfaces (Abstractions)

#### `IDataProcessor`

Interface pour le traitement des données

- `clean_data()`: Nettoyage des données
- `encode_features()`: Encodage des variables catégorielles
- `impute_missing_values()`: Imputation des valeurs manquantes

#### `IPropertyClassifier`

Interface pour la classification des propriétés

- `classify_properties()`: Classification en types (Résidentiel/Revenu/Autre)
- `get_classification_stats()`: Statistiques de classification

#### `IFeatureSelector`

Interface pour la sélection de variables

- `select_features()`: Sélection des variables importantes
- `get_feature_importance()`: Importance des variables

### Implémentations Concrètes

#### `PropertyDataProcessor`

```python
processor = PropertyDataProcessor(missing_threshold=0.05)
df_clean = processor.clean_data(df)
df_encoded = processor.encode_features(df_clean)
df_final = processor.impute_missing_values(df_encoded)
```

**Paramètres:**

- `missing_threshold`: Seuil pour supprimer les colonnes (défaut: 0.05 = 5%)

#### `PropertyClassifier`

```python
classifier = PropertyClassifier()
df_classified = classifier.classify_properties(df)
stats = classifier.get_classification_stats(df_classified)
```

**Classifications:**

- **Revenu**: Duplex, Triplex, Quadruplex, etc.
- **Résidentiel**: Maison, Condo, Chalet, etc.
- **Autre**: Terrain, Ferme, etc.

#### `FeatureSelector`

```python
selector = FeatureSelector(
    cv_folds=5,
    random_state=42,
    max_iter=10000,
    rf_threshold=0.01
)
features = selector.select_features(X, y)
```

**Paramètres:**

- `cv_folds`: Nombre de plis pour la validation croisée
- `max_iter`: Itérations maximum pour Lasso
- `rf_threshold`: Seuil d'importance pour Random Forest

### Classe Orchestratrice

#### `PropertyAnalyzer`

```python
analyzer = PropertyAnalyzer(
    data_processor=processor,
    property_classifier=classifier,
    feature_selector=selector
)
results = analyzer.analyze_properties(df, target_column='price')
```

## 🎯 Utilisation Basique

```python
from lib.property_analysis import PropertyAnalyzer

# Configuration par défaut
analyzer = PropertyAnalyzer()

# Analyse complète
results = analyzer.analyze_properties(properties_db)

# Variables importantes
important_features = results['selected_features']
X = analyzer.processed_data['X']
y = analyzer.processed_data['y']
```

## 🔧 Configurations Avancées

### Configuration Stricte

```python
from lib.property_analysis import (
    PropertyAnalyzer, PropertyDataProcessor,
    PropertyClassifier, FeatureSelector
)

strict_processor = PropertyDataProcessor(missing_threshold=0.02)
strict_selector = FeatureSelector(rf_threshold=0.05)

strict_analyzer = PropertyAnalyzer(
    data_processor=strict_processor,
    property_classifier=PropertyClassifier(),
    feature_selector=strict_selector
)
```

### Extension Personnalisée

```python
class CustomClassifier(PropertyClassifier):
    def classify_properties(self, df):
        df_classified = super().classify_properties(df)

        # Logique personnalisée
        large_properties = df['surface'] > df['surface'].quantile(0.9)
        df_classified.loc[large_properties, 'classification_immobiliere'] = 'Luxe'

        return df_classified

custom_analyzer = PropertyAnalyzer(
    property_classifier=CustomClassifier()
)
```

## 📊 Résultats

### Structure des Résultats

```python
results = {
    'shape_original': (lignes, colonnes),
    'shape_processed': (lignes, colonnes),
    'classification_stats': {
        'counts': {'Résidentiel': count, 'Revenu': count},
        'percentages': {'Résidentiel': %, 'Revenu': %},
        'price_analysis': {
            'Résidentiel': {'mean': prix, 'median': prix, 'count': nb},
            'Revenu': {'mean': prix, 'median': prix, 'count': nb}
        }
    },
    'selected_features': ['feature1', 'feature2', ...],
    'classification_features': {
        'Résidentiel': ['feature1', ...],
        'Revenu': ['feature2', ...]
    },
    'feature_importance': {'feature1': 0.15, 'feature2': 0.12, ...}
}
```

### Résumé

```python
summary = analyzer.get_summary()
# {
#     'total_properties': 1000,
#     'total_features': 50,
#     'selected_features_count': 15,
#     'reduction_percentage': 70.0,
#     'price_stats': {'mean': 350000, 'median': 320000},
#     'classification_distribution': {'Résidentiel': 600, 'Revenu': 400}
# }
```

## 🧪 Tests et Validation

### Validation des Données

```python
from lib.property_analysis import DataValidator

# Validation des colonnes requises
is_valid = DataValidator.validate_dataframe(df, ['price', 'surface'])

# Validation de la colonne cible
is_target_valid = DataValidator.validate_target_column(df, 'price')
```

### Accès aux Modèles

```python
# Modèles entraînés
lasso_model = analyzer.feature_selector.lasso_model
rf_model = analyzer.feature_selector.rf_model

# Scores
lasso_score = lasso_model.score(X, y)
rf_score = rf_model.score(X, y)
```

## 🎯 Principes SOLID Appliqués

### **S - Single Responsibility Principle**

- `PropertyDataProcessor`: Se contente du preprocessing
- `PropertyClassifier`: Se contente de la classification
- `FeatureSelector`: Se contente de la sélection de variables

### **O - Open-Closed Principle**

- Extension via héritage (ex: `CustomClassifier`)
- Ajout de nouvelles implémentations sans modifier l'existant

### **L - Liskov Substitution Principle**

- Toute implémentation d'une interface peut être substituée
- `PropertyAnalyzer` fonctionne avec n'importe quelle implémentation

### **I - Interface Segregation Principle**

- Interfaces spécialisées (`IDataProcessor`, `IPropertyClassifier`, etc.)
- Pas de méthodes inutiles dans les interfaces

### **D - Dependency Inversion Principle**

- `PropertyAnalyzer` dépend des abstractions, pas des implémentations
- Injection de dépendances dans le constructeur

## 📈 Avantages

### Maintenabilité

- Code organisé en responsabilités claires
- Modifications localisées
- Tests unitaires simplifiés

### Extensibilité

- Ajout de nouvelles classifications
- Nouveaux algorithmes de sélection
- Personnalisation sans casser l'existant

### Réutilisabilité

- Classes utilisables dans d'autres projets
- Configuration flexible
- Composants indépendants

### Testabilité

- Mocking des dépendances
- Tests isolés par composant
- Validation par couche

## 🚀 Migration depuis l'Ancien Code

### Avant (Monolithique)

```python
# Code directement dans le notebook
df = properties_db.copy()
df = df.loc[:, df.notnull().mean() > 0.05]
# ... 200 lignes de code ...
lasso = LassoCV().fit(X, y)
important_features = ...
```

### Après (Modulaire)

```python
# Code organisé et réutilisable
analyzer = PropertyAnalyzer()
results = analyzer.analyze_properties(properties_db)
important_features = results['selected_features']
```

## 💡 Bonnes Pratiques

### Configuration

- Utilisez l'injection de dépendances
- Configurez les paramètres selon vos besoins
- Testez différentes configurations

### Extension

- Héritez des classes existantes
- Implémentez les interfaces pour de nouveaux comportements
- Conservez la compatibilité avec `PropertyAnalyzer`

### Performance

- Réutilisez les instances d'`PropertyAnalyzer`
- Stockez les modèles entraînés
- Profilez vos extensions personnalisées

### Debugging

- Activez les logs (`logging.INFO`)
- Utilisez `get_summary()` pour les métriques
- Accédez aux modèles pour l'analyse détaillée
