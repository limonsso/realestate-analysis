# 🏷️ Normalisation des Types de Propriétés

## 📋 Vue d'ensemble

Le système d'analyse immobilière inclut maintenant une fonctionnalité de normalisation des types de propriétés qui utilise la collection `property_types` de MongoDB pour standardiser et classifier les types de propriétés de manière cohérente.

## 🗄️ Structure de la Collection `property_types`

### Format des Données

```json
{
  "_id": "quadruplex",
  "category": "Résidentiel",
  "description": {
    "fr": "Immeuble à revenus composé de 4 unités d'habitation",
    "en": "Building with four residential units"
  },
  "features": {
    "fr": ["4 unités", "Revenus locatifs", "Investissement"],
    "en": ["4 units", "Rental income", "Investment"]
  },
  "common_uses": {
    "fr": ["Investissement locatif", "Résidence principale + revenus"],
    "en": ["Rental investment", "Owner-occupied + rental"]
  },
  "typical_characteristics": {
    "units": 4,
    "min_bedrooms_per_unit": 1,
    "min_bathrooms_per_unit": 1
  },
  "display_names": {
    "fr": "Quadruplex à vendre",
    "en": "Quadruplex for sale"
  }
}
```

### Champs Clés

- **`_id`** : Identifiant unique du type (ex: "quadruplex", "maison", "condo")
- **`category`** : Catégorie principale (ex: "Résidentiel", "Commercial")
- **`display_names`** : Noms d'affichage en français et anglais
- **`typical_characteristics`** : Caractéristiques typiques du type

## 🔧 Utilisation du Normalisateur

### 1. Chargement depuis MongoDB

```python
from lib import MongoDBLoader, PropertyTypeNormalizer

# Connexion MongoDB
loader = MongoDBLoader("mongodb://localhost:27017/")
loader.connect("realestate")

# Charger les types de propriétés
property_types = loader.load_property_types()

# Créer le normalisateur
normalizer = PropertyTypeNormalizer(property_types, language='fr')
```

### 2. Normalisation des Données

```python
import pandas as pd
from lib import PropertyDataProcessor

# Créer le processeur avec normalisation
processor = PropertyDataProcessor(property_types_data=property_types)

# Charger les propriétés
df = loader.load_properties(collection_name="properties")

# Le nettoyage inclura automatiquement la normalisation des types
df_clean = processor.clean_data(df)
```

### 3. Utilisation avec l'Analyseur Principal

```python
from lib import PropertyAnalyzer

# Créer l'analyseur avec normalisation intégrée
analyzer = PropertyAnalyzer()
analyzer.data_processor = PropertyDataProcessor(property_types_data=property_types)

# L'analyse inclura automatiquement la normalisation
results = analyzer.analyze_properties(df, target_column='price')
```

## 🎯 Fonctionnalités de Normalisation

### Reconnaissance Intelligente

Le normalisateur reconnaît automatiquement les variations courantes :

| Type Original         | Type Normalisé | ID         |
| --------------------- | -------------- | ---------- |
| "Maison à vendre"     | "maison"       | maison     |
| "House for sale"      | "maison"       | maison     |
| "Condo à vendre"      | "condo"        | condo      |
| "Duplex à vendre"     | "duplex"       | duplex     |
| "Triplex à vendre"    | "triplex"      | triplex    |
| "Quadruplex à vendre" | "quadruplex"   | quadruplex |

### Correspondance Approximative

- **Sans accents** : "Maison" → "maison"
- **Variations de casse** : "MAISON" → "maison"
- **Correspondance partielle** : "Maison moderne" → "maison"

### Gestion des Types Inconnus

- Les types non reconnus sont marqués comme "unknown"
- Statistiques détaillées des types non reconnus
- Possibilité d'ajouter manuellement des types

## 📊 Avantages de la Normalisation

### ✅ **Cohérence des Données**

- Standardisation des noms de types
- Élimination des doublons et variations
- Classification uniforme

### ✅ **Amélioration de l'Analyse**

- Meilleure classification des propriétés
- Variables plus pertinentes
- Résultats plus fiables

### ✅ **Flexibilité**

- Support multilingue (FR/EN)
- Ajout facile de nouveaux types
- Configuration personnalisable

## 🔍 Logs et Monitoring

### Exemple de Sortie

```
🏷️ === ÉTAPE 6: NORMALISATION DES TYPES DE PROPRIÉTÉS ===
📊 Types avant normalisation:
   📝 Maison à vendre: 1,234 propriétés
   📝 Condo à vendre: 567 propriétés
   📝 Duplex à vendre: 89 propriétés

✅ Types après normalisation:
   🏷️ maison: 1,234 propriétés
   🏷️ condo: 567 propriétés
   🏷️ duplex: 89 propriétés

⚠️ Types non reconnus (3):
   ❓ Propriété commerciale
   ❓ Terrain à vendre
   ❓ Autre
```

## 🧪 Tests et Validation

### Test de Normalisation

```python
# Test avec des types factices
test_types = [
    {"_id": "maison", "display_names": {"fr": "Maison à vendre"}},
    {"_id": "condo", "display_names": {"fr": "Condo à vendre"}}
]

normalizer = PropertyTypeNormalizer(test_types)

# Tester la normalisation
test_data = pd.DataFrame({
    'type': ['Maison à vendre', 'Condo à vendre', 'Type inconnu']
})

normalized = normalizer.normalize_property_types(test_data)
print(normalized['type'].tolist())  # ['maison', 'condo', 'unknown']
```

### Validation des Mappings

```python
# Obtenir les statistiques
stats = normalizer.get_statistics()
print(f"Types total: {stats['total_types']}")
print(f"Variations: {stats['total_variations']}")
print(f"Catégories: {stats['categories']}")
```

## 🔧 Configuration Avancée

### Ajout Manuel de Types

```python
# Ajouter un type manuellement
normalizer.add_property_type(
    type_id="maison_prestige",
    display_name="Maison de prestige à vendre",
    category="Résidentiel"
)
```

### Personnalisation des Correspondances

```python
# Créer un normalisateur personnalisé
custom_types = [
    {
        "_id": "maison_prestige",
        "display_names": {"fr": "Maison de prestige à vendre"},
        "category": "Résidentiel"
    }
]

normalizer = PropertyTypeNormalizer(custom_types, language='fr')
```

## 🚨 Problèmes Courants

### Types Non Reconnus

1. **Vérifier la collection `property_types`**
2. **Ajouter les types manquants**
3. **Vérifier les variations de noms**

### Erreurs de Normalisation

1. **Vérifier la langue configurée**
2. **Contrôler les caractères spéciaux**
3. **Valider la structure des données**

## 📈 Impact sur l'Analyse

### Avant Normalisation

- Types incohérents : "Maison", "maison", "MAISON"
- Classification imprécise
- Variables moins pertinentes

### Après Normalisation

- Types standardisés : "maison", "condo", "duplex"
- Classification précise
- Variables optimisées
- Résultats plus fiables

---

**Version** : 2.0.0  
**Dépendances** : pymongo, pandas  
**Compatibilité** : MongoDB 4.0+, Python 3.7+
