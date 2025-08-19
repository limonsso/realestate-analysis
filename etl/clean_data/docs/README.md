# 🧹 NETTOYAGE EXPERT DU DATASET IMMOBILIER

## 🎯 Vue d'ensemble

Ce dossier contient un système complet de nettoyage de données immobilières selon les spécifications détaillées dans `real_estate_prompt.md`. Le système implémente un pipeline en 5 phases pour transformer des données brutes en un dataset premium prêt pour l'analyse d'investissement.

> 📚 **Documentation complète** : Consultez `REORGANISATION_SUMMARY.md` pour comprendre l'évolution de l'architecture du projet et sa structure modulaire actuelle.

## 🚀 Installation et Configuration

### 📦 Dépendances requises

```bash
# Installer les dépendances Python
pip install -r requirements.txt

# Ou installer manuellement les packages principaux
pip install pandas numpy geopandas pyarrow openpyxl plotly seaborn matplotlib scipy scikit-learn
```

### 🔧 Structure des fichiers

```
clean_data/
├── real_estate_prompt.md          # Spécifications détaillées
├── real_estate_data_cleaning.py   # Script principal de nettoyage
├── real_estate_cleaning_notebook.ipynb  # Notebook Jupyter interactif
├── test_cleaning.py               # Script de test avec données d'exemple
├── requirements.txt                # Dépendances Python
└── README.md                      # Ce fichier
```

## 🎯 Phases du Pipeline de Nettoyage

### 🔍 Phase 1: Audit & Diagnostic Complet

- **Analyse exploratoire** des dimensions et types de données
- **Détection des valeurs manquantes** avec visualisations
- **Identification des colonnes problématiques** (doublons, incohérences)
- **Statistiques descriptives** de base

### 🛠️ Phase 2: Nettoyage Intelligent

- **Standardisation des noms** de colonnes en snake_case
- **Consolidation des colonnes redondantes** (revenus, dates, surfaces)
- **Nettoyage des variables financières** (prix, taxes, évaluations)
- **Nettoyage des caractéristiques physiques** (surfaces, chambres, années)
- **Validation de la géolocalisation** (coordonnées Québec)
- **Élimination des doublons** intelligente

### ⚡ Phase 3: Enrichissement Intelligent

- **Métriques financières calculées** (ROI, prix/pi², plus-value potentielle)
- **Métriques physiques** (âge du bâtiment, ratios)
- **Catégorisation automatique** (segments de prix, classes ROI)
- **Score de complétude** des données par propriété

### 🚨 Phase 4: Validation & Contrôle Qualité

- **Tests de cohérence financière** (ROI réaliste, écarts prix/évaluation)
- **Validation des caractéristiques physiques** (surfaces positives, âges logiques)
- **Contrôle de la géolocalisation** (dans les limites du Québec)
- **Tests généraux** de cohérence

### 🎯 Phase 5: Préparation pour l'Analyse

- **Structure finale optimisée** par catégories
- **Export multi-format** (Parquet, CSV, JSON, GeoJSON)
- **Rapport de qualité** détaillé
- **Préparation pour cartes interactives**

## 🚀 Utilisation

### 📊 Utilisation via Script Python

```python
from real_estate_data_cleaning import RealEstateDataCleaner

# Créer le nettoyeur
cleaner = RealEstateDataCleaner(input_file="votre_dataset.csv")

# Exécuter le pipeline complet
success = cleaner.run_complete_cleaning_pipeline()

if success:
    # Récupérer les données nettoyées
    cleaned_data = cleaner.get_cleaned_data()

    # Récupérer le rapport de qualité
    quality_report = cleaner.get_quality_report()

    print(f"✅ Nettoyage terminé: {len(cleaned_data)} propriétés")
```

### 🎮 Utilisation via Ligne de Commande

```bash
# Nettoyage d'un fichier CSV
python real_estate_data_cleaning.py --input votre_dataset.csv

# Nettoyage avec MongoDB
python real_estate_data_cleaning.py --mongodb "mongodb://localhost:27017/"

# Spécifier le répertoire de sortie
python real_estate_data_cleaning.py --input votre_dataset.csv --output-dir ./resultats
```

### 📓 Utilisation via Notebook Jupyter

1. Ouvrir `real_estate_cleaning_notebook.ipynb`
2. Exécuter les cellules dans l'ordre
3. Suivre le pipeline étape par étape
4. Visualiser les résultats et la qualité des données

## 🧪 Tests et Validation

### 🔬 Test avec Données d'Exemple

```bash
# Exécuter les tests complets
python test_cleaning.py

# Ou tester individuellement
python -c "
from test_cleaning import test_individual_phases, test_cleaning_pipeline
test_individual_phases()
test_cleaning_pipeline()
"
```

### ✅ Validation des Résultats

Le système génère automatiquement :

- **Fichiers de données nettoyés** dans plusieurs formats
- **Rapport de qualité** détaillé
- **Logs de validation** pour chaque phase
- **Métriques de performance** (temps, mémoire, taux de succès)

## 📊 Formats de Sortie

### 💾 Fichiers Générés

1. **`real_estate_cleaned_YYYYMMDD_HHMMSS.parquet`**

   - Format optimisé pour Python (pandas, dask)
   - Performance maximale pour gros datasets

2. **`real_estate_cleaned_YYYYMMDD_HHMMSS.csv`**

   - Compatibilité universelle
   - Ouverture dans Excel, Google Sheets, etc.

3. **`real_estate_cleaned_YYYYMMDD_HHMMSS.json`**

   - Pour applications web
   - API et intégrations

4. **`real_estate_cleaned_YYYYMMDD_HHMMSS.geojson`**

   - Cartes interactives (Folium, Mapbox)
   - Analyses géospatiales

5. **`quality_report_YYYYMMDD_HHMMSS.json`**
   - Rapport détaillé de la qualité
   - Métriques et statistiques

## 🔧 Personnalisation

### ⚙️ Configuration des Seuils

```python
# Modifier les seuils de validation dans la classe
class RealEstateDataCleaner:
    def __init__(self):
        # Seuils personnalisables
        self.roi_min = 0      # ROI minimum acceptable
        self.roi_max = 50      # ROI maximum acceptable
        self.price_eval_tolerance = 50  # Tolérance écart prix/évaluation (%)
        self.geo_bounds = {    # Limites géographiques
            'longitude': (-80, -55),
            'latitude': (45, 63)
        }
```

### 🎨 Ajout de Nouvelles Métriques

```python
def _create_custom_metrics(self):
    """Ajouter vos propres métriques calculées"""

    # Exemple: Score d'investissement personnalisé
    if all(col in self.df_cleaned.columns for col in ['roi_brut', 'plus_value_potential']):
        self.df_cleaned['investment_score'] = (
            self.df_cleaned['roi_brut'] * 0.6 +
            self.df_cleaned['plus_value_potential'] * 0.4
        )
```

## 📈 Intégration avec le Dashboard

### 🔗 Connexion au Dashboard Existant

```python
# Après nettoyage, charger dans le dashboard
cleaned_data = cleaner.get_cleaned_data()

# Sauvegarder dans le format attendu par le dashboard
cleaned_data.to_csv('../dashboard/src/data/cleaned_properties.csv', index=False)

# Ou exporter en JSON pour l'API
cleaned_data.to_json('../dashboard/src/data/cleaned_properties.json', orient='records')
```

### 🗺️ Utilisation des Données Géospatiales

```python
# Créer une carte interactive avec Folium
import folium

# Filtrer les propriétés avec coordonnées valides
geo_data = cleaned_data.dropna(subset=['longitude', 'latitude'])

# Créer la carte
m = folium.Map(location=[46.8139, -71.2080], zoom_start=8)

# Ajouter les propriétés
for idx, row in geo_data.iterrows():
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=f"Prix: ${row['price']:,}<br>ROI: {row['roi_brut']:.1f}%"
    ).add_to(m)

m.save('carte_proprietes.html')
```

## 🚨 Dépannage

### ❌ Problèmes Courants

1. **Erreur d'import des modules**

   ```bash
   pip install -r requirements.txt
   ```

2. **Données manquantes ou corrompues**

   - Vérifier le format du fichier d'entrée
   - Utiliser le mode verbose pour plus de détails

3. **Erreurs de géolocalisation**

   - Vérifier que les coordonnées sont numériques
   - Ajuster les limites géographiques si nécessaire

4. **Problèmes de mémoire**
   - Utiliser le format Parquet pour de gros datasets
   - Traiter par chunks si nécessaire

### 📞 Support

Pour toute question ou problème :

1. Vérifier les logs d'erreur détaillés
2. Consulter le fichier de spécifications `real_estate_prompt.md`
3. Exécuter les tests avec `test_cleaning.py`
4. Vérifier la compatibilité des versions Python

## 🎯 Prochaines Étapes

### 🚀 Améliorations Futures

1. **Intégration MongoDB native** pour chargement direct
2. **Pipeline automatisé** avec DVC (Data Version Control)
3. **Interface web** pour configuration et monitoring
4. **Machine Learning** pour détection automatique d'anomalies
5. **API REST** pour intégration avec d'autres systèmes

### 📊 Analyses Avancées

1. **Modèles de prédiction** de prix et ROI
2. **Clustering géographique** des quartiers
3. **Analyse temporelle** des tendances du marché
4. **Optimisation de portefeuille** immobilier

---

**🎉 Votre dataset immobilier est maintenant prêt pour des analyses d'investissement de niveau professionnel !**

_Développé selon les spécifications du fichier `real_estate_prompt.md` avec les meilleures pratiques de data science._
