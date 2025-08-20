# 🎯 Guide de Mapping des Champs - Dataset Immobilier Personnalisé

## 📊 Vue d'ensemble

Ce guide détaille le mapping spécifique entre vos **67 champs** et les **20 groupes de consolidation** du pipeline ETL ultra-intelligent.

## 🔍 Analyse de vos champs

### **Total des champs** : 67

### **Champs consolidables** : 45+ (groupés en 20 catégories)

### **Champs uniques** : 22 (pas de consolidation possible)

## 🏠 **GROUPE 1: PRIX**

### Vos champs source

- `price` → **Colonne finale** : `price_final`
- `prix_evaluation` → **Priorité 2**
- `price_assessment` → **Priorité 3**

### Stratégie de consolidation

```python
# Priorité : price > prix_evaluation > price_assessment
price_final = coalesce(price, prix_evaluation, price_assessment)
```

---

## 📏 **GROUPE 2: SURFACE**

### Vos champs source

- `surface` → **Colonne finale** : `surface_final`
- `living_area` → **Priorité 2**
- `superficie` → **Priorité 3**
- `lot_size` → **Priorité 4** (terrain)

### Stratégie de consolidation

```python
# Priorité : surface > living_area > superficie > lot_size
surface_final = coalesce(surface, living_area, superficie, lot_size)
```

---

## 🛏️ **GROUPE 3: CHAMBRES**

### Vos champs source

- `bedrooms` → **Colonne finale** : `bedrooms_final`
- `nbr_chanbres` → **Priorité 2**
- `nb_bedroom` → **Priorité 3**
- `rooms` → **Priorité 4** (général)

### Stratégie de consolidation

```python
# Priorité : bedrooms > nbr_chanbres > nb_bedroom > rooms
bedrooms_final = coalesce(bedrooms, nbr_chanbres, nb_bedroom, rooms)
```

---

## 🚿 **GROUPE 4: SALLES DE BAIN**

### Vos champs source

- `bathrooms` → **Colonne finale** : `bathrooms_final`
- `nbr_sal_deau` → **Priorité 2**
- `nbr_sal_bain` → **Priorité 3**
- `nb_bathroom` → **Priorité 4**
- `water_rooms` → **Priorité 5**

### Stratégie de consolidation

```python
# Priorité : bathrooms > nbr_sal_deau > nbr_sal_bain > nb_bathroom > water_rooms
bathrooms_final = coalesce(bathrooms, nbr_sal_deau, nbr_sal_bain, nb_bathroom, water_rooms)
```

---

## 🌍 **GROUPE 5: COORDONNÉES GÉOGRAPHIQUES**

### Vos champs source

- `latitude` → **Colonne finale** : `latitude_final`
- `longitude` → **Colonne finale** : `longitude_final`
- `geolocation` → **Priorité 2** (objet géolocalisation)
- `geo` → **Priorité 3** (géolocalisation alternative)

### Stratégie de consolidation

```python
# Extraction des coordonnées depuis les objets géolocalisation
latitude_final = coalesce(latitude, extract_lat(geolocation), extract_lat(geo))
longitude_final = coalesce(longitude, extract_lng(geolocation), extract_lng(geo))
```

---

## 🏠 **GROUPE 6: ADRESSES**

### Vos champs source

- `address` → **Colonne finale** : `address_final`
- `full_address` → **Priorité 2**
- `location` → **Priorité 3**
- `city` → **Priorité 4**
- `postal_code` → **Priorité 5**

### Stratégie de consolidation

```python
# Construction d'adresse complète
address_final = coalesce(full_address, address, f"{location}, {city} {postal_code}")
```

---

## 🏗️ **GROUPE 7: TYPES DE PROPRIÉTÉ**

### Vos champs source

- `type` → **Colonne finale** : `property_type_final`
- `building_style` → **Priorité 2**
- `style` → **Priorité 3**

### Stratégie de consolidation

```python
# Priorité : type > building_style > style
property_type_final = coalesce(type, building_style, style)
```

---

## 📅 **GROUPE 8: ANNÉE DE CONSTRUCTION**

### Vos champs source

- `year_built` → **Colonne finale** : `year_built_final`
- `construction_year` → **Priorité 2**
- `annee` → **Priorité 3**

### Stratégie de consolidation

```python
# Priorité : year_built > construction_year > annee
year_built_final = coalesce(year_built, construction_year, annee)
```

---

## 💰 **GROUPE 9: TAXES MUNICIPALES**

### Vos champs source

- `municipal_taxes` → **Colonne finale** : `tax_municipal_final`
- `municipal_tax` → **Priorité 2**
- `taxes` → **Priorité 3**

### Stratégie de consolidation

```python
# Priorité : municipal_taxes > municipal_tax > taxes
tax_municipal_final = coalesce(municipal_taxes, municipal_tax, taxes)
```

---

## 🏆 **GROUPE 10: ÉVALUATION MUNICIPALE**

### Vos champs source

- `evaluation_total` → **Colonne finale** : `evaluation_final`
- `municipal_evaluation_total` → **Priorité 2**
- `evaluation_terrain` → **Priorité 3**
- `evaluation_batiment` → **Priorité 4**

### Stratégie de consolidation

```python
# Priorité : evaluation_total > municipal_evaluation_total > evaluation_terrain > evaluation_batiment
evaluation_final = coalesce(evaluation_total, municipal_evaluation_total, evaluation_terrain, evaluation_batiment)
```

---

## 💵 **GROUPE 11: REVENUS LOCATIFS**

### Vos champs source

- `revenu` → **Colonne finale** : `revenue_final`
- `revenus_annuels_bruts` → **Priorité 2**
- `plex-revenu` → **Priorité 3**
- `plex_revenu` → **Priorité 4**

### Stratégie de consolidation

```python
# Priorité : revenu > revenus_annuels_bruts > plex-revenu > plex_revenu
revenue_final = coalesce(revenu, revenus_annuels_bruts, plex-revenu, plex_revenu)
```

---

## 💸 **GROUPE 12: CHARGES ET DÉPENSES**

### Vos champs source

- `expense` → **Colonne finale** : `expenses_final`
- `depenses` → **Priorité 2**
- `expense_period` → **Priorité 3**

### Stratégie de consolidation

```python
# Priorité : expense > depenses > expense_period
expenses_final = coalesce(expense, depenses, expense_period)
```

---

## 🌳 **GROUPE 13: TAILLE DU TERRAIN**

### Vos champs source

- `lot_size` → **Colonne finale** : `lot_size_final`
- `evaluation_terrain` → **Priorité 2**

### Stratégie de consolidation

```python
# Priorité : lot_size > evaluation_terrain
lot_size_final = coalesce(lot_size, evaluation_terrain)
```

---

## 🚗 **GROUPE 14: PLACES DE STATIONNEMENT**

### Vos champs source

- `nb_parking` → **Colonne finale** : `nb_parking_final`
- `parking` → **Priorité 2**
- `nb_garage` → **Priorité 3**

### Stratégie de consolidation

```python
# Priorité : nb_parking > parking > nb_garage
nb_parking_final = coalesce(nb_parking, parking, nb_garage)
```

---

## 🏢 **GROUPE 15: NOMBRE D'UNITÉS**

### Vos champs source

- `unites` → **Colonne finale** : `nb_unit_final`
- `residential_units` → **Priorité 2**
- `commercial_units` → **Priorité 3**

### Stratégie de consolidation

```python
# Priorité : unites > residential_units > commercial_units
nb_unit_final = coalesce(unites, residential_units, commercial_units)
```

---

## 🔗 **GROUPE 16: LIENS ET URLS**

### Vos champs source

- `link` → **Colonne finale** : `link_final`
- `img_src` → **Priorité 2**

### Stratégie de consolidation

```python
# Priorité : link > img_src
link_final = coalesce(link, img_src)
```

---

## 🏢 **GROUPE 17: ENTREPRISES IMMOBILIÈRES**

### Vos champs source

- `company` → **Colonne finale** : `company_final`

### Stratégie de consolidation

```python
# Pas de consolidation nécessaire
company_final = company
```

---

## 📊 **GROUPE 18: VERSIONS DES DONNÉES**

### Vos champs source

- `version` → **Colonne finale** : `version_final`

### Stratégie de consolidation

```python
# Pas de consolidation nécessaire
version_final = version
```

---

## 📋 **CHAMPS NON CONSOLIDABLES**

### Champs uniques (22 champs)

- `basement` - Sous-sol
- `main_unit_details` - Détails de l'unité principale
- `vendue` - Statut de vente
- `description` - Description
- `image` - Image
- `images` - Images multiples
- `_id` - Identifiant MongoDB
- `updated_at` - Date de mise à jour
- `evaluation_year` - Année d'évaluation
- `add_date` - Date d'ajout
- `created_at` - Date de création
- `municipal_evaluation_year` - Année d'évaluation municipale
- `revenu_period` - Période de revenu
- `update_at` - Date de mise à jour alternative
- `extraction_metadata` - Métadonnées d'extraction

### Champs vides ou invalides

- `""` - Champ vide (à supprimer)

## 🔧 Configuration Personnalisée

### Créer un fichier de configuration spécifique

```python
# custom_fields_config.py
from config.consolidation_config import ConsolidationConfig

class CustomFieldsConfig(ConsolidationConfig):
    # Redéfinir les groupes avec vos champs spécifiques
    CONSOLIDATION_GROUPS = {
        "Prix": ["price", "prix_evaluation", "price_assessment"],
        "Surface": ["surface", "living_area", "superficie", "lot_size"],
        "Chambres": ["bedrooms", "nbr_chanbres", "nb_bedroom", "rooms"],
        "Salles_de_bain": ["bathrooms", "nbr_sal_deau", "nbr_sal_bain", "nb_bathroom", "water_rooms"],
        "Coordonnees": ["latitude", "longitude", "geolocation", "geo"],
        "Adresses": ["address", "full_address", "location", "city", "postal_code"],
        "Type_propriete": ["type", "building_style", "style"],
        "Annee_construction": ["year_built", "construction_year", "annee"],
        "Taxes_municipales": ["municipal_taxes", "municipal_tax", "taxes"],
        "Evaluation": ["evaluation_total", "municipal_evaluation_total", "evaluation_terrain", "evaluation_batiment"],
        "Revenus": ["revenu", "revenus_annuels_bruts", "plex-revenu", "plex_revenu"],
        "Depenses": ["expense", "depenses", "expense_period"],
        "Taille_terrain": ["lot_size", "evaluation_terrain"],
        "Stationnement": ["nb_parking", "parking", "nb_garage"],
        "Unites": ["unites", "residential_units", "commercial_units"],
        "Liens": ["link", "img_src"],
        "Entreprise": ["company"],
        "Version": ["version"]
    }
```

## 🚀 Utilisation avec vos données

### Pipeline avec configuration personnalisée

```bash
python main_ultra_intelligent.py \
  --source csv \
  --source-path your_data.csv \
  --config custom_fields_config.py \
  --output exports/ \
  --formats csv,parquet \
  --verbose
```

### Pipeline avec validation uniquement

```bash
python main_ultra_intelligent.py \
  --source csv \
  --source-path your_data.csv \
  --validate-only \
  --verbose
```

## 📊 Résultats attendus

### Avant consolidation

- **67 champs** avec redondances et variations
- **Données dispersées** sur plusieurs colonnes similaires
- **Qualité variable** selon la source

### Après consolidation

- **19 colonnes consolidées** + **22 champs uniques**
- **Données récupérées** depuis les colonnes redondantes
- **Qualité améliorée** par consolidation intelligente

---

**🚀 Pipeline ETL Ultra-Intelligent v7.0.0** - Mapping personnalisé pour votre dataset
