# 🧪 Tests d'Intégration - Architecture Modulaire

## 📋 Vue d'Ensemble

Cette suite de tests d'intégration valide que l'architecture modulaire du `CentrisExtractor` fonctionne correctement ensemble. Les tests couvrent l'intégration, la performance et la robustesse.

## 🏗️ Structure des Tests

```
tests/
├── integration_test.py      # Tests d'intégration de base
├── performance_test.py      # Tests de performance et scalabilité
├── robustness_test.py       # Tests de robustesse et gestion d'erreurs
└── run_integration_tests.py # Script principal d'exécution
```

## 🚀 Exécution des Tests

### **Exécution Complète**

```bash
python run_integration_tests.py
```

### **Exécution Individuelle**

```bash
# Tests d'intégration de base
python tests/integration_test.py

# Tests de performance
python tests/performance_test.py

# Tests de robustesse
python tests/robustness_test.py
```

## 🔗 Phase 1: Tests d'Intégration de Base

### **Objectifs**

- Vérifier que tous les composants s'intègrent correctement
- Valider les interactions entre composants
- Tester le workflow complet d'extraction

### **Tests Inclus**

#### **1. Workflow Complet d'Extraction**

- ✅ Création de l'extracteur avec tous les composants
- ✅ Exécution du workflow d'extraction end-to-end
- ✅ Validation des résultats et des appels aux composants

#### **2. Interactions Entre Composants**

- ✅ Vérification des références entre composants
- ✅ Validation de la configuration partagée
- ✅ Test des dépendances circulaires

#### **3. Gestion d'Erreurs en Intégration**

- ✅ Gestion des échecs de recherche
- ✅ Gestion des échecs de validation
- ✅ Récupération gracieuse des erreurs

#### **4. Intégration du Seuil de Validation**

- ✅ Configuration et récupération du seuil
- ✅ Propagation des changements aux composants internes
- ✅ Validation de la cohérence des paramètres

#### **5. Gestion des Sessions**

- ✅ Initialisation et fermeture des sessions
- ✅ Partage des sessions entre composants
- ✅ Nettoyage propre des ressources

## ⚡ Phase 2: Tests de Performance

### **Objectifs**

- Mesurer les performances de l'architecture modulaire
- Valider la scalabilité avec la charge
- Vérifier la gestion mémoire

### **Tests Inclus**

#### **1. Performance d'Extraction Concurrente**

- ✅ Traitement de multiples requêtes simultanées
- ✅ Mesure des temps d'exécution
- ✅ Validation de la concurrence

#### **2. Utilisation Mémoire Sous Charge**

- ✅ Simulation de charges importantes
- ✅ Vérification de la gestion mémoire
- ✅ Test avec de grandes quantités de données

#### **3. Cohérence des Temps de Réponse**

- ✅ Mesure de la variance des temps de réponse
- ✅ Validation de la stabilité des performances
- ✅ Test de la reproductibilité

#### **4. Scalabilité avec le Nombre de Composants**

- ✅ Test avec différents nombres de composants
- ✅ Analyse de la courbe de scalabilité
- ✅ Validation de la croissance linéaire

## 🛡️ Phase 3: Tests de Robustesse

### **Objectifs**

- Valider la gestion des erreurs et exceptions
- Tester l'isolation des échecs
- Vérifier la dégradation gracieuse

### **Tests Inclus**

#### **1. Gestion des Échecs Réseau**

- ✅ Simulation d'erreurs de connexion
- ✅ Gestion des timeouts
- ✅ Récupération après échec

#### **2. Gestion des Données Invalides**

- ✅ Traitement de HTML malformé
- ✅ Gestion des données corrompues
- ✅ Validation des entrées

#### **3. Isolation des Échecs de Composants**

- ✅ Test de l'isolation des erreurs
- ✅ Validation de la non-propagation
- ✅ Gestion des composants défaillants

#### **4. Prévention des Fuites Mémoire**

- ✅ Exécution multiple pour détecter les fuites
- ✅ Validation de la gestion des ressources
- ✅ Test de la stabilité à long terme

#### **5. Dégradation Gracieuse**

- ✅ Test avec composants partiellement défaillants
- ✅ Validation de la continuité de service
- ✅ Gestion des dégradations progressives

## 📊 Métriques et Seuils

### **Seuils de Performance**

- **Temps de réponse** : < 100ms par requête
- **Utilisation mémoire** : < 100MB sous charge normale
- **Scalabilité** : Croissance linéaire (facteur < 3x)

### **Seuils de Robustesse**

- **Taux de réussite** : > 95% en conditions normales
- **Récupération d'erreur** : < 1s après échec
- **Isolation des erreurs** : 100% des erreurs isolées

### **Seuils d'Intégration**

- **Tests réussis** : 100% des tests d'intégration
- **Couverture des composants** : 100% des composants testés
- **Interactions validées** : 100% des interactions testées

## 🔧 Configuration des Tests

### **Variables d'Environnement**

```bash
# Configuration des tests
export TEST_TIMEOUT=30          # Timeout des tests en secondes
export TEST_MAX_RETRIES=3       # Nombre maximum de tentatives
export TEST_LOG_LEVEL=INFO      # Niveau de log des tests
```

### **Configuration des Mocks**

Les tests utilisent des mocks pour simuler :

- Les réponses HTTP
- Les données HTML
- Les composants externes
- Les erreurs réseau

## 📈 Interprétation des Résultats

### **Succès (100%)**

- ✅ Architecture modulaire entièrement validée
- ✅ Prêt pour la production
- ✅ Tous les composants fonctionnent ensemble

### **Succès Partiel (80-99%)**

- ⚠️ Architecture globalement fonctionnelle
- 🔧 Quelques composants nécessitent des ajustements
- 📋 Vérifier les composants défaillants

### **Échec (< 80%)**

- ❌ Problèmes majeurs dans l'architecture
- 🔧 Refactorisation nécessaire
- 📋 Analyse approfondie requise

## 🚨 Dépannage

### **Problèmes Courants**

#### **1. Erreurs d'Import**

```bash
# Vérifier la structure des dossiers
ls -la src/extractors/centris/
ls -la tests/
```

#### **2. Erreurs de Mock**

```bash
# Vérifier les dépendances
pip install unittest-mock
```

#### **3. Erreurs de Configuration**

```bash
# Vérifier la configuration
python -c "from config.settings import config; print(config)"
```

### **Logs de Débogage**

```bash
# Activer les logs détaillés
export TEST_LOG_LEVEL=DEBUG
python run_integration_tests.py
```

## 📚 Ressources Additionnelles

- [Architecture Modulaire](README.md#architecture-modulaire-du-centrisextractor)
- [Composants Spécialisés](src/extractors/centris/)
- [Tests Unitaires](test_pipeline.py)
- [Documentation API](docs/)

## 🤝 Contribution

Pour ajouter de nouveaux tests d'intégration :

1. **Créer le test** dans le dossier `tests/`
2. **Ajouter le test** à la suite appropriée
3. **Documenter le test** dans ce fichier
4. **Valider** que tous les tests passent

---

**🎯 Objectif** : Garantir que l'architecture modulaire est robuste, performante et prête pour la production.

