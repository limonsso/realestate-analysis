# 🧹 PROMPT : Nettoyage Expert du Dataset Immobilier

## 🎯 MISSION : Transformer des Données Brutes en Or Analytique

Analysez et nettoyez le dataset immobilier suivant pour créer une base de données premium prête pour l'analyse d'investissement. Appliquez les meilleures pratiques de data cleaning avec une approche méthodique et intelligente.

## 🛠️ STACK TECHNOLOGIQUE REQUIS

### 📊 **PYTHON - Écosystème Data Science**
**Manipulation & Nettoyage :**
- **Pandas** : DataFrames et manipulation des données
- **NumPy** : Calculs numériques et arrays
- **Dask** : Pour traitement de gros datasets (>1GB)

**Analyse & Visualisation :**
- **Matplotlib** : Graphiques de base
- **Seaborn** : Visualisations statistiques avancées
- **Plotly Express/Graph Objects** : Graphiques interactifs premium

**Détection Outliers & Anomalies :**
- **SciPy Stats** : Tests statistiques et détection anomalies
- **Scikit-learn (IsolationForest)** : Algorithmes de détection d'outliers
- **StandardScaler/RobustScaler** : Normalisation des données

**Géolocalisation :**
- **GeoPandas** : Manipulation de données géographiques
- **Folium** : Cartes interactives
- **Geopy** : Géocodage et calculs géographiques

### 🚀 **ENVIRONNEMENT DE DÉVELOPPEMENT**
- **Jupyter Lab** ou **Google Colab** pour développement interactif
- **Python 3.9+** (compatibilité optimale)
- **Git** pour versioning du code de nettoyage
- **DVC (Data Version Control)** pour versioning des datasets

### 💾 **FORMATS & STOCKAGE**
**Formats par étape :**
- **Input** : CSV, Excel (.xlsx), JSON
- **Travail** : Parquet (performance optimale)
- **Output** : Parquet + CSV (compatibilité)
- **Backup** : HDF5 pour datasets complexes

---

## 📋 COLONNES DISPONIBLES
```
Identifiants: _id, link, company, version, created_at, updated_at, update_at, add_date
Localisation: address, full_address, city, region, longitude, latitude, location
Prix & Évaluations: price, price_assessment, municipal_evaluation_building, 
                    municipal_evaluation_land, municipal_evaluation_total
Revenus: revenu, plex-revenue, plex-revenu, potential_gross_revenue
Taxes: municipal_taxes, school_taxes, municipal_tax, school_tax
Caractéristiques: surface, living_area, construction_year, year_built, lot_size
Propriété: type, bedrooms, nb_bedroom, bathrooms, nb_bathroom, unites, 
           residential_units, commercial_units, parking, basement, building_style
Gestion: depenses, vendue, description, img_src, image, images, main_unit_details
Métadonnées: extraction_metadata, municipal_evaluation_year
```

---

## 🔍 PHASE 1 : AUDIT & DIAGNOSTIC COMPLET

### 📊 Analyse Exploratoire avec Pandas/Seaborn
- **Dimensions dataset** : Shape, memory usage, types de données
- **Matrice des valeurs manquantes** : Heatmap avec Seaborn
- **Distributions** : Histogrammes interactifs avec Plotly
- **Détection outliers** : IsolationForest de Scikit-learn
- **Corrélations** : Matrice avec Seaborn pour identifier redondances

### 🚨 Points de Vigilance Spécifiques
- **Doublons de colonnes** : `revenu` vs `plex-revenue` vs `plex-revenu`
- **Colonnes temporelles** : `created_at`, `updated_at`, `update_at`, `add_date`
- **Surfaces** : `surface` vs `living_area` (cohérence)
- **Années** : `construction_year` vs `year_built`
- **Taxes** : `municipal_taxes` vs `municipal_tax`
- **Chambres/SDB** : `bedrooms` vs `nb_bedroom`

---

## 🛠️ PHASE 2 : NETTOYAGE INTELLIGENT

### 🔧 Déduplication & Consolidation avec Pandas
- **Fusionner colonnes redondantes** : Utiliser fillna() pour consolider
- **Standardiser noms** : Regex pour snake_case cohérent
- **Éliminer doublons** : drop_duplicates() sur address + price
- **Date consolidée** : Max() sur colonnes temporelles

### 💰 Nettoyage Variables Financières
**Prix & Revenus avec Pandas/NumPy :**
- Convertir en numérique : Regex pour supprimer $, espaces, virgules
- Détecter outliers : Z-score avec SciPy, seuils métier
- Ratios de cohérence : revenu/price avec alertes
- Imputation groupée : Médiane par quartier/type

**Taxes & Dépenses :**
- Vérifier cohérence totaux calculés vs colonnes existantes
- Détection anomalies : Pourcentages aberrants
- Estimations basées sur évaluations municipales

### 🏠 Caractéristiques Physiques
**Surfaces avec Pandas :**
- Harmonisation unités : Détection automatique pi² vs m²
- Outliers contextuels : Surface par type de propriété
- Validation cohérence : lot_size >= surface_habitable
- Prix/pi² aberrants avec percentiles

**Dates & Âges :**
- Validation années : Between() pour plages réalistes
- Calculs d'âge : 2024 - construction_year
- Détection incohérences temporelles

### 📍 Géolocalisation avec GeoPandas
- **Validation coordonnées** : Between() pour longitude/latitude
- **Filtrage géographique** : Bounds pour Québec/région
- **Standardisation adresses** : String methods de Pandas
- **Clustering quartiers** : DBSCAN de Scikit-learn sur coordonnées
- **GeoDataFrame** : Points_from_xy pour analyses spatiales

---

## ⚡ PHASE 3 : ENRICHISSEMENT INTELLIGENT

### 🧮 Variables Calculées avec Pandas
- **ROI brut/net** : Calculs avec revenus, taxes, dépenses
- **Cash-flow mensuel** : Division par 12 des revenus nets
- **Prix/pi²** : Ratio prix sur surface
- **Potentiel plus-value** : Écart évaluation/prix
- **Âge bâtiment** : Différence avec année actuelle
- **Score complétude** : Pourcentage données non-manquantes

### 🏷️ Catégorisation avec Pandas Cut
- **Classe ROI** : Cut() avec bins personnalisés
- **Segments prix** : Quantiles ou seuils métier
- **Types d'opportunité** : Logic combinée sur plusieurs métriques
- **Zones performance** : GroupBy sur quartiers

---

## 🚨 PHASE 4 : VALIDATION & CONTRÔLE QUALITÉ

### ✅ Tests Automatiques avec Pandas Assert
- **ROI réaliste** : Between 0% et 50%
- **Cohérence financière** : Charges < revenus
- **Prix vs évaluation** : Écart acceptable (±50%)
- **Caractéristiques logiques** : Chambres/SDB pour surface donnée
- **Géolocalisation** : Dans zone d'étude
- **Pas de négatifs** : Assert >= 0 pour variables physiques

### 📊 Rapport Qualité avec Pandas Profiling
- **Avant/après** : Comparaison métriques qualité
- **Visualisations** : Graphiques des améliorations
- **Alertes** : Properties nécessitant vérification manuelle

---

## 🎯 PHASE 5 : PRÉPARATION POUR L'ANALYSE

### 🗂️ Structure Finale Optimisée
**Colonnes finales consolidées :**
- Identifiants unifiés et géolocalisation propre
- Métriques financières calculées et validées
- Caractéristiques standardisées
- Métadonnées de qualité et classification

### 💾 Export Multi-Format
- **Parquet** : Pour analyses Python (pandas, dask)
- **CSV** : Compatibilité universelle
- **JSON** : Pour applications web
- **GeoJSON** : Pour cartes interactives avec Folium

### 🏆 LIVRABLES FINAUX
1. **Dataset nettoyé** : Parquet optimisé + CSV backup
2. **Notebook documentation** : Jupyter avec toutes étapes
3. **Scripts réutilisables** : Fonctions de nettoyage modulaires
4. **Rapport qualité** : HTML avec pandas-profiling
5. **Carte validation** : Folium avec propriétés géolocalisées

---

## 🔥 BONUS : DÉTECTION D'OPPORTUNITÉS

**Pendant le nettoyage, identifier automatiquement :**
- 💎 **Sous-évaluations** : Prix significativement < évaluation municipale
- 🚨 **Anomalies suspectes** : Données nécessitant validation manuelle
- 📈 **Patterns géographiques** : Zones à forte performance
- ⚡ **Erreurs systématiques** : Patterns révélateurs dans les données

**Technologies pour analyses avancées :**
- **Scikit-learn** : Machine learning pour patterns
- **Plotly Dash** : Dashboard interactif pour exploration
- **Streamlit** : Interface utilisateur pour validation

**Objectif Final :** Un dataset premium, traité avec les meilleures technologies Python, fiable à 99%, prêt pour des analyses d'investissement de niveau professionnel !