# 🏠 Pipeline d'Extraction Web Immobilier - Version Finale

> **Pipeline d'extraction de données immobilières depuis Centris.ca avec architecture modulaire et validation avancée**

## 🎯 **Statut du Projet : 100% Fonctionnel ✅**

- ✅ **Extraction complète** : Toutes les informations demandées sont extraites
- ✅ **Validation des données** : Règles de cohérence type/catégorie implémentées
- ✅ **Architecture modulaire** : Composants séparés et maintenables
- ✅ **Tests d'intégration** : Validation sur cas réel (Chambly)
- ✅ **Structure nettoyée** : Fichiers temporaires supprimés, code optimisé

## 🚀 **Fonctionnalités Principales**

### 🔍 **Extraction de Données Complète**

- **Informations de base** : Prix, adresse, type, statut
- **Détails techniques** : Dimensions, caractéristiques, médias
- **Informations détaillées** : Utilisation, style bâtiment, stationnement, unités, Walk Score
- **Validation intelligente** : Cohérence type/catégorie, règles métier

### 🏗️ **Architecture Modulaire**

- **SessionManager** : Gestion des sessions HTTP et cookies
- **SearchManager** : Recherche et pagination des résultats
- **SummaryExtractor** : Extraction des résumés de propriétés
- **DetailExtractor** : Extraction détaillée des pages individuelles
- **DataValidator** : Validation et nettoyage des données

### 🗄️ **Gestion des Données**

- **Modèles Pydantic** : Validation et sérialisation robustes
- **MongoDB** : Stockage flexible et scalable
- **Configuration** : Paramètres personnalisables par table/collection

## 📁 **Structure du Projet (Nettoyée)**

```
clean-web-extractor-pipeline/
├── 📁 src/                          # Code source principal
│   ├── 📁 core/                     # Pipeline principal
│   ├── 📁 extractors/               # Extracteurs spécialisés
│   │   └── 📁 centris/             # Extracteur Centris modulaire
│   ├── 📁 models/                   # Modèles de données
│   ├── 📁 services/                 # Services (base de données)
│   └── 📁 utils/                    # Utilitaires et validation
├── 📁 config/                       # Configuration
├── 📁 tests/                        # Tests d'intégration
├── 📁 examples/                     # Exemples d'utilisation
├── 📁 scripts/                      # Scripts d'exécution
├── 📁 docs/                         # Documentation complète
└── 📁 logs/                         # Logs d'exécution
```

## 🛠️ **Installation et Configuration**

### **Prérequis**

- Python 3.8+
- MongoDB 4.4+
- Dépendances listées dans `requirements.txt`

### **Installation**

```bash
# Cloner le projet
git clone <repository>
cd clean-web-extractor-pipeline

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp env.example env.local
# Éditer env.local avec vos paramètres
```

### **Configuration**

```yaml
# config/config.yml
database:
  host: localhost
  port: 27017
  name: realestate_analysis
  collection: votre_collection

extraction:
  max_properties: 100
  delay_between_requests: 2
  timeout: 30
```

## 🚀 **Utilisation**

### **Test Rapide (Chambly)**

```bash
# Test d'extraction réel avec stockage en base
python run_chambly_test.py
```

### **Pipeline Complet**

```bash
# Exécution du pipeline principal
python run.py

# Avec paramètres personnalisés
python scripts/run_pipeline.py --table votre_table --max 50
```

### **Exemples d'Utilisation**

```bash
# Validation des données
python examples/validation_example.py

# Exécution avec table personnalisée
python examples/run_with_custom_table.py
```

## 🧪 **Tests et Validation**

### **Tests d'Intégration**

- **Test Chambly** : Extraction réelle de plex à Chambly
- **Validation des données** : Vérification de la cohérence
- **Tests de robustesse** : Gestion des erreurs et timeouts

### **Validation des Données**

- **Cohérence type/catégorie** : Vérification des règles métier
- **Validation des adresses** : Format et géolocalisation
- **Validation des prix** : Plages et cohérence
- **Nettoyage des textes** : Suppression des caractères spéciaux

## 📊 **Données Extraites**

### **Informations de Base**

- ID, type, catégorie, statut
- Prix, évaluations municipales, taxes
- Adresse complète avec coordonnées GPS

### **Caractéristiques Techniques**

- Dimensions du terrain et de la construction
- Nombre de pièces, chambres, salles de bain
- Année de construction, état du bâtiment

### **Informations Détaillées (Nouvelles)**

- **Utilisation** : Résidentielle, commerciale, etc.
- **Style bâtiment** : Jumelé, détaché, etc.
- **Stationnement** : Garage, allée, nombre de places
- **Unités** : Nombre et détails des unités
- **Walk Score** : Score de marcheabilité
- **Date d'emménagement** : Selon les baux, etc.

## 🔧 **Maintenance et Développement**

### **Ajout de Nouveaux Champs**

1. Étendre le modèle `Property` dans `src/models/property.py`
2. Implémenter l'extraction dans `DetailExtractor`
3. Ajouter la validation dans `DataValidator`
4. Mettre à jour les tests

### **Support de Nouveaux Sites**

1. Créer un nouvel extracteur dans `src/extractors/`
2. Implémenter l'interface d'extraction
3. Adapter les modèles de données
4. Ajouter les tests correspondants

## 📚 **Documentation Complète**

- **📖 Architecture** : `docs/ARCHITECTURE.md`
- **⚙️ Configuration** : `docs/CONFIGURATION.md`
- **📊 Modèles de Données** : `docs/DATA_MODELS.md`
- **🧪 Tests** : `docs/TESTING.md`
- **🚀 Démarrage Rapide** : `docs/QUICKSTART.md`
- **🏠 Test Chambly** : `docs/CHAMBLY_TEST_GUIDE.md`

## 🤝 **Contribution**

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 **Licence**

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 **Support**

- **Issues** : Utiliser les GitHub Issues pour les bugs et demandes
- **Documentation** : Consulter le dossier `docs/`
- **Tests** : Exécuter `python run_chambly_test.py` pour validation

---

**🎉 Pipeline 100% Fonctionnel - Prêt pour la Production !**
