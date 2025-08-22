# 🏠 Pipeline d'Extraction Web Immobilière

Un pipeline **autonome et maintenable** pour extraire, traiter et analyser les données immobilières depuis le web. **Aucune dépendance externe** comme Airflow ou Prefect - exécution directe avec paramètres en ligne de commande.

## ✨ Caractéristiques

- **🚀 Autonome** : Aucune dépendance externe, exécution directe
- **⚙️ Paramétrable** : Arguments en ligne de commande pour personnaliser l'exécution
- **🏗️ Architecture moderne** : Pydantic pour la validation, asyncio pour la performance
- **🔍 Extraction robuste** : Gestion des erreurs, retry automatique, rotation des User-Agents
- **🗄️ Base de données optimisée** : MongoDB avec index et agrégations
- **📝 Logging structuré** : Structlog avec métriques et observabilité
- **⚙️ Configuration flexible** : Variables d'environnement et fichiers YAML
- **🧪 Tests complets** : Suite de tests avec pytest
- **📚 Documentation détaillée** : API docs et guides d'utilisation

## 🏗️ Architecture

### **Architecture Générale**

```
clean-web-extractor-pipeline/
├── run.py                   # 🚀 Script de démarrage simple
├── src/                     # Code source principal
│   ├── core/               # Pipeline principal autonome
│   ├── extractors/         # Extracteurs web (Centris, DuProprio, etc.)
│   │   └── centris/        # Package Centris modulaire
│   ├── models/             # Modèles de données Pydantic
│   ├── services/           # Services métier
│   └── utils/              # Utilitaires et helpers
├── config/                  # Configuration et paramètres
├── scripts/                 # Scripts d'exécution avancés
├── tests/                   # Tests unitaires et d'intégration
├── data/                    # Données extraites et cache
├── logs/                    # Fichiers de logs
└── docs/                    # Documentation
```

### **Architecture Modulaire du CentrisExtractor** 🏗️

Le `CentrisExtractor` a été refactorisé en composants spécialisés pour une meilleure maintenabilité :

```
📦 CentrisExtractor (Orchestrateur principal)
├── 🔌 CentrisSessionManager     # Gestion des sessions HTTP
├── 🔍 CentrisSearchManager      # Recherche et pagination
├── 📋 CentrisSummaryExtractor   # Extraction des résumés
├── 🔎 CentrisDetailExtractor    # Extraction des détails
└── ✅ CentrisDataValidator      # Validation des données
```

#### **Responsabilités des Composants :**

- **`CentrisSessionManager`** : Configuration des sessions HTTP, headers, timeouts
- **`CentrisSearchManager`** : Initialisation des recherches, pagination, construction des requêtes API
- **`CentrisSummaryExtractor`** : Parsing HTML des pages de résultats, extraction des résumés
- **`CentrisDetailExtractor`** : Extraction des détails complets depuis les pages de propriétés
- **`CentrisDataValidator`** : Validation des résultats de recherche et des données extraites

#### **Avantages de l'Architecture Modulaire :**

✅ **Maintenabilité** : Chaque composant a une responsabilité unique  
✅ **Testabilité** : Tests unitaires indépendants pour chaque composant  
✅ **Extensibilité** : Ajout facile de nouveaux extracteurs ou validateurs  
✅ **Réutilisabilité** : Composants réutilisables dans d'autres contextes  
✅ **Débogage** : Isolation des problèmes et diagnostics plus précis  
✅ **Équipe** : Développement parallèle sur différents composants

## 🚀 Installation

### Prérequis

- Python 3.9+
- MongoDB 4.4+
- Git

### Installation

```bash
# Cloner le repository
git clone <repository-url>
cd clean-web-extractor-pipeline

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configuration des variables d'environnement
cp env.example .env
# Éditer .env avec vos paramètres

# Configuration optionnelle
cp config/config.example.yml config/config.yml
# Éditer config.yml selon vos besoins
```

## 🎯 Utilisation

### 🚀 Exécution Simple

```bash
# Exécution complète avec configuration par défaut
python run.py

# Exécution avec script avancé
python scripts/run_pipeline.py
```

### ⚙️ Paramètres en Ligne de Commande

```bash
# Extraction pour une localisation spécifique
python run.py --location "Montréal"

# Extraction pour un type de propriété spécifique
python run.py --property-type "Condo"

# Extraction pour une région spécifique
python run.py --region "Québec"

# Spécification du nom de la table/collection MongoDB
python run.py --table-name "properties_2024"

# Spécification du nom de la base de données
python run.py --database-name "real_estate_2024"

# Mode debug avec plus de logs
python run.py --debug

# Limitation du nombre de propriétés
python run.py --max-properties 100

# Personnalisation de la taille des lots
python run.py --batch-size 25

# Sortie en format JSON
python run.py --output-format json --output-file results.json

# Sortie en format CSV
python run.py --output-format csv --output-file results.csv

# Mode simulation (dry-run)
python run.py --dry-run
```

### 📋 Tous les Paramètres Disponibles

```bash
python run.py --help
```

**Filtres de localisation :**

- `--location, -l` : Localisation spécifique (ex: "Montréal", "Laval")
- `--region, -r` : Région spécifique (ex: "Québec", "Ontario")

**Filtres de propriété :**

- `--property-type, -t` : Type de propriété (ex: "Condo", "House")

**Options de base de données :**

- `--table-name, -n` : Nom de la collection MongoDB (ex: "properties_2024", "real_estate_data")
- `--database-name` : Nom de la base de données MongoDB (ex: "real_estate_db", "property_data")

**Options de performance :**

- `--max-properties` : Nombre maximum de propriétés à traiter
- `--batch-size` : Taille des lots de traitement

**Options de debug :**

- `--debug, -d` : Mode debug avec logs détaillés
- `--dry-run` : Simulation sans sauvegarde en base

**Options de sortie :**

- `--output-format` : Format de sortie (json, csv, console)
- `--output-file` : Fichier de sortie pour les résultats

### 🔧 Exemples d'Utilisation Avancés

#### **Organisation par Année/Mois**

```bash
# Extraction pour 2024
python run.py --table-name "properties_2024" --database-name "real_estate_2024"

# Extraction pour janvier 2024
python run.py --table-name "properties_2024_01" --database-name "real_estate_2024"

# Extraction pour une région spécifique en 2024
python run.py --location "Montréal" --table-name "montreal_2024"
```

#### **Organisation par Type de Propriété**

```bash
# Extraction des condos dans une collection dédiée
python run.py --property-type "Condo" --table-name "condos_2024"

# Extraction des maisons unifamiliales
python run.py --property-type "SingleFamilyHome" --table-name "houses_2024"

# Extraction des plex
python run.py --property-type "Plex" --table-name "plex_2024"
```

#### **Organisation par Localisation**

```bash
# Extraction pour Montréal
python run.py --location "Montréal" --table-name "montreal_properties"

# Extraction pour Laval
python run.py --location "Laval" --table-name "laval_properties"

# Extraction pour la Montérégie
python run.py --location "Montérégie" --table-name "monteregie_properties"
```

#### **Combinaisons de Paramètres**

```bash
# Extraction des condos à Montréal en 2024
python run.py --location "Montréal" --property-type "Condo" --table-name "montreal_condos_2024"

# Extraction des maisons en Montérégie avec sortie JSON
python run.py --location "Montérégie" --property-type "SingleFamilyHome" --table-name "monteregie_houses" --output-format json --output-file "monteregie_houses.json"

# Mode debug pour les plex à Laval
python run.py --location "Laval" --property-type "Plex" --table-name "laval_plex" --debug
```

## 🎯 Configuration

### 📁 Fichier de Configuration

Le pipeline utilise un fichier de configuration YAML (`config/config.yml`) pour définir tous les paramètres :

```yaml
# Configuration de la base de données MongoDB
database:
  server_url: "localhost:27017"
  connection_string: "mongodb://localhost:27017"
  database_name: "real_estate_analytics"

  # Noms des collections MongoDB
  properties_collection: "properties_2024" # Collection des propriétés
  summaries_collection: "summaries_2024" # Collection des résumés
  logs_collection: "extraction_logs_2024" # Collection des logs

  # Options de connexion avancées
  max_pool_size: 100
  min_pool_size: 0
  server_selection_timeout_ms: 5000
  connect_timeout_ms: 5000
  socket_timeout_ms: 5000

# Configuration Centris
centris:
  locations:
    - "Montréal"
    - "Laval"
    - "Montérégie"

  property_types:
    - "SingleFamilyHome"
    - "Condo"
    - "Plex"

  price_range:
    min: 100000
    max: 5000000

# Configuration des performances
performance:
  batch_size: 25
  max_concurrent_requests: 5
  max_retries: 3
  retry_delay: 5

# Configuration du logging
logging:
  level: "INFO"
  file: "logs/pipeline.log"
  format: "json"
```

### 🔑 Variables d'Environnement

Vous pouvez aussi utiliser des variables d'environnement (`.env`) :

```bash
# Noms des collections MongoDB
MONGODB_PROPERTIES_COLLECTION=properties_2024
MONGODB_SUMMARIES_COLLECTION=summaries_2024
MONGODB_LOGS_COLLECTION=extraction_logs_2024

# Base de données
MONGODB_DATABASE_NAME=real_estate_analytics
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
```

### 📊 Organisation des Collections

Le pipeline crée automatiquement plusieurs collections dans MongoDB :

- **`properties_collection`** : Propriétés complètes avec tous les détails
- **`summaries_collection`** : Résumés des propriétés (pour la recherche rapide)
- **`logs_collection`** : Logs d'extraction et de traitement

**Exemples d'organisation :**

```yaml
# Par année
database:
  database_name: "real_estate_analytics"
  properties_collection: "properties_2024"
  summaries_collection: "summaries_2024"
  logs_collection: "logs_2024"

# Par région
database:
  database_name: "real_estate_analytics"
  properties_collection: "montreal_properties"
  summaries_collection: "montreal_summaries"
  logs_collection: "montreal_logs"

# Par type de propriété
database:
  database_name: "real_estate_analytics"
  properties_collection: "condos_2024"
  summaries_collection: "condos_summaries_2024"
  logs_collection: "condos_logs_2024"
```

## 📊 Modèles de Données

### Property (Propriété complète)

```python
from src.models.property import Property, PropertyType, PropertyStatus

property_data = Property(
    id="MLS123456",
    type=PropertyType.SINGLE_FAMILY_HOME,
    status=PropertyStatus.FOR_SALE,
    address=Address(
        street="123 Main St",
        city="Montréal",
        region="Québec"
    ),
    financial=FinancialInfo(
        price=450000,
        municipal_tax=2500
    ),
    features=PropertyFeatures(
        bedrooms=3,
        bathrooms=2
    )
)
```

## 🔍 Extraction des Données

### Processus d'Extraction

1. **🚀 Initialisation** : Configuration de la session et authentification
2. **🔍 Recherche** : Construction des requêtes et pagination
3. **📋 Extraction des résumés** : Parsing des pages de résultats
4. **🔎 Extraction des détails** : Récupération des informations complètes
5. **✅ Validation** : Vérification de la qualité des données
6. **💾 Sauvegarde** : Stockage en base MongoDB

### Gestion des Erreurs

```python
from src.extractors.centris_extractor import CentrisExtractionError

try:
    summaries = await extractor.extract_summaries(search_query)
except CentrisExtractionError as e:
    logger.error(f"Erreur d'extraction: {e}")
    # Gestion de l'erreur et retry automatique
```

## 🗄️ Base de Données

### Collections MongoDB

- **properties** : Propriétés complètes avec tous les détails
- **property_summaries** : Résumés pour la recherche rapide
- **extraction_logs** : Logs d'extraction et métriques

### Requêtes d'Exemple

```python
from src.services.database_service import DatabaseService

db = DatabaseService(config.database)

# Propriétés par localisation
properties = db.get_properties_by_location("Montréal", "Québec")

# Propriétés par type
condos = db.get_properties_by_type("SellCondo")

# Propriétés récentes
recent = db.get_recent_properties(hours=24)

# Statistiques d'extraction
stats = db.get_extraction_stats(source="Centris", days=7)
```

## 📈 Monitoring et Observabilité

### Logs Structurés

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "info",
  "event": "Extraction des résumés",
  "location": "Montérégie",
  "property_type": "SingleFamilyHome",
  "count": 45,
  "duration_ms": 1250
}
```

### Métriques de Performance

- Temps d'exécution par étape
- Nombre de propriétés traitées
- Taux de succès/échec
- Utilisation des ressources

## 🧪 Tests

### Exécution des Tests

```bash
# Tests unitaires
pytest tests/unit/

# Tests d'intégration
pytest tests/integration/

# Tests complets avec couverture
pytest --cov=src --cov-report=html

# Tests de performance
pytest tests/performance/ -m "slow"
```

## 🚀 Déploiement

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "run.py"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: real-estate-pipeline
spec:
  replicas: 1
  selector:
    matchLabels:
      app: real-estate-pipeline
  template:
    metadata:
      labels:
        app: real-estate-pipeline
    spec:
      containers:
        - name: pipeline
          image: real-estate-pipeline:latest
          env:
            - name: MONGODB_URL
              value: "mongodb://mongodb:27017"
          args:
            - "--location"
            - "Montréal"
            - "--property-type"
            - "Condo"
```

### Cron Job

```bash
# Ajouter à crontab pour exécution quotidienne
0 2 * * * cd /path/to/pipeline && python run.py --location "Montréal" >> logs/cron.log 2>&1
```

## 🔒 Sécurité

### Bonnes Pratiques

- Rotation des User-Agents
- Gestion des sessions avec timeouts
- Validation des données d'entrée
- Logs sans informations sensibles
- Authentification MongoDB sécurisée

## 📚 API Reference

### Classes Principales

- `PipelineExecutor` : Exécuteur principal du pipeline
- `Property` : Modèle de propriété immobilière
- `CentrisExtractor` : Extracteur pour Centris.ca
- `DatabaseService` : Service de gestion de la base de données

### Méthodes Clés

```python
# Pipeline
executor = PipelineExecutor(args)
result = await executor.run_pipeline()

# Extraction
await extractor.extract_summaries(search_query)
await extractor.extract_details(property_url)

# Base de données
db_service.save_property(property_data)
db_service.get_properties_by_location(city, region)
```

## 🤝 Contribution

### Guide de Contribution

1. Fork le repository
2. Créer une branche feature (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

### Standards de Code

- **Formatage** : Black pour le formatage automatique
- **Linting** : Flake8 pour la qualité du code
- **Types** : MyPy pour le typage statique
- **Tests** : Pytest avec couverture de code

```bash
# Formatage automatique
black src/ tests/

# Vérification du code
flake8 src/ tests/
mypy src/

# Tests
pytest --cov=src --cov-report=html
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

### Documentation

- [Guide d'installation](docs/INSTALLATION.md)
- [Guide d'utilisation](docs/USAGE.md)
- [API Reference](docs/API.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

### Communauté

- [Issues GitHub](https://github.com/username/repo/issues)
- [Discussions](https://github.com/username/repo/discussions)
- [Wiki](https://github.com/username/repo/wiki)

---

**🚀 Pipeline autonome développé avec ❤️ par l'équipe Real Estate Analysis**

### **Validation des Résultats de Recherche**

Le pipeline inclut une **validation intelligente** des résultats de la première page pour s'assurer que les données extraites correspondent bien aux critères de recherche :

#### **Processus de Validation**

1. **Extraction de la première page** → Récupération des résultats initiaux
2. **Validation des localisations** → Vérification ville/région
3. **Validation des types** → Vérification type de propriété
4. **Calcul du score** → Pourcentage de correspondance pour chaque critère
5. **Décision finale** → Continuation ou arrêt selon les seuils

#### **Types de Validation**

##### **1. Validation des Localisations** 🌍

- **Objectif** : Vérifier que les propriétés sont dans les bonnes villes/régions
- **Seuil** : 70% des propriétés doivent correspondre
- **Critères** : Correspondance partielle des noms de localisation

##### **2. Validation des Types de Propriétés** 🏠

- **Objectif** : Vérifier que les propriétés sont du bon type
- **Seuil** : 70% des propriétés doivent correspondre
- **Critères** : Correspondance des types (Condo, House, Plex, etc.)
- **Bonus** : Distribution des types trouvés

#### **Seuils de Validation**

- **Seuil minimum** : 70% des propriétés doivent correspondre pour chaque critère
- **Validation globale** : Les deux validations doivent réussir
- **En dessous du seuil** : Pipeline s'arrête avec avertissement détaillé
- **Au-dessus du seuil** : Pipeline continue normalement

#### **Critères Validés**

##### **Validation des Résultats de Recherche**

- ✅ **Localisation** : Ville/région correspond aux paramètres
- ✅ **Type de propriété** : Type correspond aux critères
- ✅ **Distribution des types** : Statistiques des types trouvés

##### **Validation des Données de Propriétés**

- ✅ **Régions québécoises** : Validation contre la liste des régions connues
- ✅ **Codes postaux** : Format canadien valide (A1A 1A1)
- ✅ **Prix immobiliers** : Fourchette raisonnable (10k$ - 50M$)
- ✅ **Coordonnées GPS** : Limites géographiques du Québec
- ✅ **ID de propriété** : Format et unicité
- ✅ **Nettoyage des textes** : Suppression caractères de contrôle

#### **Exemple de Validation Complète**

```bash
🔍 Validation des localisations pour 20 propriétés...
📊 Validation localisations: 18/20 propriétés correspondent (90.0%)

🔍 Validation des types de propriétés pour 20 propriétés...
📊 Validation types: 19/20 propriétés correspondent (95.0%)
📊 Distribution des types: Condo: 15, House: 4, Plex: 1

✅ Validation des résultats réussie
```

#### **Gestion des Erreurs Détaillée**

```bash
🔍 Validation des localisations pour 20 propriétés...
📊 Validation localisations: 8/20 propriétés correspondent (40.0%)
⚠️ Faible taux de correspondance des localisations (40.0%)

🔍 Validation des types de propriétés pour 20 propriétés...
📊 Validation types: 12/20 propriétés correspondent (60.0%)
⚠️ Faible taux de correspondance des types (60.0%)

⚠️ Validation des localisations échouée
⚠️ Validation des types de propriétés échouée
⚠️ Vérifiez les paramètres de recherche
```

### **Configuration de la Validation**

```yaml
# Dans config.yml
validation:
  threshold: 0.7 # Seuil de validation (70%)
  strict_mode: false # Mode strict (arrêt immédiat si échec)
  log_details: true # Logs détaillés de validation
```

### **Avantages de la Validation**

🎯 **Qualité des données** : S'assure que les résultats sont pertinents  
🛡️ **Prévention des erreurs** : Évite l'extraction de données incorrectes  
📊 **Transparence** : Logs détaillés du processus de validation  
⚡ **Performance** : Arrêt rapide si les résultats sont incohérents  
🔧 **Maintenance** : Facilite le débogage des problèmes d'extraction
