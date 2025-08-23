# 🏗️ Structure du Projet - Version Nettoyée

## 📁 **Structure des Fichiers**

### **🚀 Lanceurs de Tests (Racine)**

- **`run_chambly_test.py`** - Test d'extraction Chambly Plex
- **`run_trois_rivieres_test.py`** - Test d'extraction Trois-Rivières Plex
- **`run_saint_hyacinthe_test.py`** - Test d'extraction Saint-Hyacinthe Plex

### **🧪 Tests (dossier `tests/`)**

- **`test_chambly_plex_extraction.py`** - Test Chambly avec extracteur unifié
- **`test_trois_rivieres_plex_extraction.py`** - Test Trois-Rivières avec extracteur unifié
- **`test_saint_hyacinthe_plex_extraction.py`** - Test Saint-Hyacinthe
- **`test_property_model.py`** - Tests des modèles de propriétés
- **`test_address_extractor.py`** - Tests de l'extracteur d'adresses
- **`test_financial_extractor.py`** - Tests de l'extracteur financier
- **`test_numeric_extractor_html.py`** - Tests de l'extracteur numérique
- **`test_units_numeric_extraction.py`** - Tests d'extraction des unités
- **`test_property_dynamic_units.py`** - Tests des unités dynamiques
- **`test_specialized_extractors.py`** - Tests des extracteurs spécialisés
- **`test_refactored_extractor.py`** - Tests de l'extracteur refactorisé
- **`test_new_extractor_only.py`** - Tests du nouvel extracteur
- **`test_performance_comparison.py`** - Tests de performance

### **⚙️ Configuration (dossier `config/`)**

- **`config.yml`** - Configuration principale (Chambly)
- **`config.trois_rivieres_test.yml`** - Configuration Trois-Rivières
- **`config.saint_hyacinthe_test.yml`** - Configuration Saint-Hyacinthe

### **🔧 Code Source (dossier `src/`)**

- **`extractors/`** - Extracteurs de données
  - **`centris_extractor.py`** - Extracteur Centris unifié (fusionné)
  - **`centris/`** - Composants spécialisés
    - **`session_manager.py`** - Gestionnaire de sessions
    - **`search_manager.py`** - Gestionnaire de recherche
    - **`detail_extractor_refactored.py`** - Extracteur de détails
    - **`extractors/`** - Extracteurs spécialisés
      - **`address_extractor.py`** - Extracteur d'adresses (config-driven)
      - **`financial_extractor.py`** - Extracteur financier
      - **`numeric_extractor.py`** - Extracteur numérique
- **`models/`** - Modèles de données
- **`services/`** - Services (base de données, etc.)
- **`utils/`** - Utilitaires

## 🎯 **Extracteur Unifié**

### **✅ Avantages de la Fusion :**

- **Un seul extracteur** : `CentrisExtractor` (plus de duplication)
- **Configuration respectée** : La config passée est VRAIMENT utilisée
- **Pas de hardcoding** : Villes et régions extraites dynamiquement
- **Logs détaillés** : Même niveau de détail pour tous les tests
- **Maintenance simplifiée** : Un seul fichier à maintenir

### **🔧 Fonctionnalités Clés :**

- **Extraction config-driven** : Utilise `config.locations_searched`
- **Logs détaillés** : Niveau debug pour tous les composants
- **Validation robuste** : Vérification des données extraites
- **Collections directes** : Création de collections timestampées

## 🚀 **Utilisation**

### **Test Chambly :**

```bash
python3 run_chambly_test.py
```

### **Test Trois-Rivières :**

```bash
python3 run_trois_rivieres_test.py
```

### **Test Saint-Hyacinthe :**

```bash
python3 run_saint_hyacinthe_test.py
```

## 📊 **Résultats Attendus**

### **✅ Chambly :**

- Collection : `chambly_plex_test_YYYYMMDD_HHMMSS`
- Logs détaillés avec niveau debug
- Validation complète des données

### **✅ Trois-Rivières :**

- Collection : `trois_rivieres_plex_test_YYYYMMDD_HHMMSS`
- **Même niveau de logs détaillés que Chambly**
- Validation complète des données
- **Aucune donnée Chambly** (configuration respectée)

## 🧹 **Nettoyage Effectué**

### **🗑️ Fichiers Supprimés :**

- ❌ `run_trois_rivieres_test_simple.py`
- ❌ `run_trois_rivieres_test_fixed.py`
- ❌ `run_trois_rivieres_test_safe.py`
- ❌ `run_trois_rivieres_test.py` (ancien)
- ❌ `test_trois_rivieres_plex_extraction_fixed.py`
- ❌ `test_trois_rivieres_plex_extraction.py` (ancien)
- ❌ `test_trois_rivieres_with_fixed_extractor.py`
- ❌ `README_TROIS_RIVIERES_SECURE.md`
- ❌ `check_trois_rivieres_collection.py`
- ❌ `env.trois_rivieres_test`
- ❌ `src/extractors/centris_extractor_fixed.py`

### **🔄 Fichiers Renommés :**

- **`run_trois_rivieres_fixed_extractor.py`** → **`run_trois_rivieres_test.py`**
- **`test_trois_rivieres_with_fixed_extractor.py`** → **`test_trois_rivieres_plex_extraction.py`**

### **📝 Classes Renommées :**

- **`TroisRivieresWithUnifiedExtractorTest`** → **`TroisRivieresPlexExtractionTest`**

## 🎉 **Bénéfices du Nettoyage**

1. **Structure cohérente** : Noms de fichiers uniformes
2. **Pas de duplication** : Un seul extracteur à maintenir
3. **Logs uniformes** : Même niveau de détail pour tous les tests
4. **Configuration respectée** : Plus de problèmes de hardcoding
5. **Maintenance simplifiée** : Moins de fichiers à gérer
6. **Tests fiables** : Extraction Trois-Rivières sans contamination Chambly

## 🔮 **Prochaines Étapes**

1. **Tester Saint-Hyacinthe** avec l'extracteur unifié
2. **Valider la cohérence** des logs pour tous les tests
3. **Documenter les configurations** pour chaque ville
4. **Optimiser les performances** si nécessaire
5. **Ajouter de nouveaux tests** si besoin

---

**🎯 Objectif atteint : Structure propre, cohérente et maintenable !**
