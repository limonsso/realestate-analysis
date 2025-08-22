# 📚 Documentation du Pipeline d'Extraction Immobilière

## 🎯 Vue d'Ensemble

Bienvenue dans la documentation complète du pipeline d'extraction immobilière ! Cette documentation vous guidera à travers tous les aspects du système, de l'installation à l'utilisation avancée.

## 📖 Table des Matières

### **🚀 Démarrage Rapide**

- **[Guide de Démarrage Rapide](QUICKSTART.md)** - Installation et première utilisation
- **[README Principal](../README.md)** - Vue d'ensemble complète du projet

### **🏗️ Architecture et Conception**

- **[Architecture Modulaire](ARCHITECTURE.md)** - Structure et composants du pipeline
- **[Modèles de Données](DATA_MODELS.md)** - Schémas et validation des données

### **⚙️ Configuration et Déploiement**

- **[Guide de Configuration](CONFIGURATION.md)** - Configuration complète du système
- **[Variables d'Environnement](../env.example)** - Exemple de configuration

### **🧪 Tests et Qualité**

- **[Guide des Tests](TESTING.md)** - Suite de tests et validation
- **[Tests d'Intégration](../tests/)** - Tests complets du système

### **🔧 Utilisation et API**

- **[Exemples d'Utilisation](../examples/)** - Cas d'usage et exemples
- **[Scripts d'Exécution](../scripts/)** - Scripts d'automatisation

## 🎯 Par Où Commencer ?

### **👶 Nouveau Utilisateur**

1. **Lire le [README Principal](../README.md)** pour comprendre le projet
2. **Suivre le [Guide de Démarrage Rapide](QUICKSTART.md)** pour l'installation
3. **Consulter l'[Architecture](ARCHITECTURE.md)** pour comprendre la structure

### **🔧 Développeur**

1. **Étudier l'[Architecture Modulaire](ARCHITECTURE.md)** en détail
2. **Comprendre les [Modèles de Données](DATA_MODELS.md)**
3. **Configurer avec le [Guide de Configuration](CONFIGURATION.md)**

### **🧪 Testeur**

1. **Exécuter les [Tests d'Intégration](../tests/)**
2. **Consulter le [Guide des Tests](TESTING.md)**
3. **Valider la configuration avec les exemples**

### **🚀 Production**

1. **Configurer l'environnement de production**
2. **Optimiser les paramètres de performance**
3. **Mettre en place le monitoring et les logs**

## 🏗️ Architecture du Système

### **Composants Principaux**

```
📦 Pipeline Principal
├── 🔌 SessionManager      # Gestion des sessions HTTP
├── 🔍 SearchManager       # Recherche et pagination
├── 📋 SummaryExtractor    # Extraction des résumés
├── 🔎 DetailExtractor     # Extraction des détails
├── ✅ DataValidator       # Validation des données
└── 🚀 Orchestrateur       # Coordination globale
```

### **Flux de Données**

```
1. 🔧 Configuration → Chargement des paramètres
2. 🔍 Recherche → Construction des requêtes API
3. 📊 Extraction → Parsing HTML et extraction
4. ✅ Validation → Vérification de la qualité
5. 💾 Sauvegarde → Stockage en base MongoDB
```

## 🎯 Fonctionnalités Clés

### **✅ Extraction Robuste**

- **Gestion des erreurs** : Retry automatique et fallback
- **Validation des données** : Pydantic pour la cohérence
- **Parsing HTML** : BeautifulSoup pour l'extraction
- **Gestion des sessions** : Sessions HTTP persistantes

### **🚀 Performance Optimisée**

- **Architecture asynchrone** : asyncio pour la concurrence
- **Pool de workers** : Traitement parallèle configurable
- **Cache intelligent** : Mise en cache des résultats
- **Rate limiting** : Contrôle du débit des requêtes

### **🔧 Configuration Flexible**

- **Variables d'environnement** : Surcharge des paramètres
- **Fichiers YAML** : Configuration structurée
- **Validation Pydantic** : Vérification automatique
- **Environnements multiples** : Dev, test, production

### **🧪 Tests Complets**

- **Tests unitaires** : Validation des composants
- **Tests d'intégration** : Validation des interactions
- **Tests de performance** : Mesure des métriques
- **Tests de robustesse** : Gestion des erreurs

## 📊 Modèles de Données

### **Entités Principales**

- **Property** : Propriété immobilière complète
- **PropertySummary** : Résumé pour les listes
- **SearchQuery** : Critères de recherche
- **LocationConfig** : Configuration des localisations

### **Types Supportés**

- **GeographicArea** : Régions administratives (Montérégie, Laurentides, etc.)
- **CityDistrict** : Districts de ville (Vieux-Montréal, Plateau-Mont-Royal, etc.)
- **PropertyType** : Types de propriétés (Plex, Condo, Maison, etc.)

## 🔧 Configuration

### **Fichiers de Configuration**

- **`config/config.yml`** : Configuration principale
- **`config/centris_ids.yml`** : Identifiants Centris
- **`.env`** : Variables d'environnement
- **`config/settings.py`** : Modèles Pydantic

### **Paramètres Clés**

- **MongoDB** : Connexion et collections
- **Centris** : URLs, User-Agents, localisations
- **Pipeline** : Workers, batch size, timeouts
- **Logging** : Niveaux, formats, fichiers

## 🧪 Tests et Validation

### **Suite de Tests**

- **Tests de structure** : Validation des requêtes API
- **Tests d'extraction** : Extraction réelle de données
- **Tests d'intégration** : Validation des composants
- **Tests de performance** : Métriques et benchmarks

### **Exécution des Tests**

```bash
# Tests individuels
python tests/test_centris_structure.py
python tests/real_extraction_test.py
python tests/updated_integration_test.py

# Suite complète
python tests/run_integration_tests.py
```

## 🚀 Utilisation

### **Exécution Simple**

```python
from src.extractors.centris_extractor import CentrisExtractor
from config.settings import config

# Initialisation
extractor = CentrisExtractor(config.centris)

# Recherche et extraction
summaries = await extractor.extract_summaries(search_query)
print(f"✅ {len(summaries)} propriétés trouvées")
```

### **Configuration Personnalisée**

```yaml
# config/config.yml
centris:
  locations_searched:
    - type: "GeographicArea"
      value: "Montérégie"
      type_id: "RARA16"
  property_types: ["Plex"]
  sale_price_min: 200000
  sale_price_max: 260000
```

## 📈 Performance et Métriques

### **Métriques Typiques**

- **Extraction** : 8-20 propriétés par page
- **Pagination** : Jusqu'à 7+ pages par recherche
- **Débit** : 138+ propriétés en recherche multiple
- **Temps de réponse** : 1-2 secondes par page

### **Optimisations**

- **Workers concurrents** : Configurable selon les ressources
- **Taille des lots** : Équilibre mémoire/performance
- **Cache** : Réduction des requêtes répétées
- **Rate limiting** : Respect des limites de l'API

## 🚨 Dépannage

### **Problèmes Courants**

1. **Erreurs de module** : Vérifier PYTHONPATH
2. **Erreurs de configuration** : Valider les fichiers YAML
3. **Timeouts** : Ajuster les paramètres de timeout
4. **Erreurs de validation** : Vérifier les modèles Pydantic

### **Outils de Diagnostic**

- **Logs structurés** : Niveaux DEBUG, INFO, WARNING, ERROR
- **Tests de validation** : Scripts de diagnostic
- **Monitoring** : Métriques de performance et d'erreurs

## 🔮 Évolutions Futures

### **Fonctionnalités Planifiées**

- **Support multi-sources** : Autres sites immobiliers
- **Interface web** : Dashboard de monitoring
- **Pipeline distribué** : Traitement à grande échelle
- **Analytics avancés** : Analyse des tendances

### **Extensibilité**

- **Nouveaux extracteurs** : Architecture modulaire
- **Nouvelles validations** : Règles métier extensibles
- **Nouveaux formats** : Support de nouvelles sources

## 🤝 Contribution

### **Standards de Code**

- **PEP 8** : Style de code Python
- **Type hints** : Annotations de types complètes
- **Docstrings** : Documentation des fonctions
- **Tests** : Couverture de code élevée

### **Processus de Développement**

1. **Fork du repository**
2. **Création d'une branche feature**
3. **Développement avec tests**
4. **Pull request avec documentation**

## 📞 Support

### **Ressources**

- **Documentation** : Ce guide et les fichiers associés
- **Tests** : Exemples d'utilisation et validation
- **Configuration** : Exemples et templates
- **Logs** : Traçabilité complète des opérations

### **Débogage**

- **Niveau DEBUG** : Détails techniques complets
- **Tests d'intégration** : Validation des composants
- **Scripts de diagnostic** : Outils de dépannage

---

## 🎉 Conclusion

Cette documentation vous fournit tous les outils nécessaires pour comprendre, configurer et utiliser le pipeline d'extraction immobilière. Que vous soyez un utilisateur débutant ou un développeur expérimenté, vous trouverez ici les informations nécessaires pour réussir.

**🚀 Prêt à extraire des données immobilières à grande échelle !**

---

## 📚 Références Rapides

- **[Installation Express](QUICKSTART.md#⚡-installation-express)**
- **[Configuration Minimale](CONFIGURATION.md#configuration-essentielle)**
- **[Tests Essentiels](TESTING.md#tests-essentiels)**
- **[Architecture Modulaire](ARCHITECTURE.md#structure-modulaire)**
- **[Modèles de Données](DATA_MODELS.md#structure-des-modèles)**
