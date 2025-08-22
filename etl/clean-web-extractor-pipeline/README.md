# 🏠 Pipeline d'Extraction Immobilière - Centris.ca

## 📋 Vue d'Ensemble

Pipeline modulaire et maintenable pour l'extraction de données immobilières depuis Centris.ca. Conçu avec une architecture moderne utilisant `asyncio`, Pydantic pour la validation des données, et une approche modulaire pour une maintenance facile.

## 🚀 Fonctionnalités Principales

- ✅ **Extraction complète** : Résumés + détails des propriétés
- ✅ **Architecture modulaire** : Composants spécialisés et réutilisables
- ✅ **Validation robuste** : Cohérence type/catégorie automatique
- ✅ **Structure propre** : Code organisé et maintenable
- ✅ **Test intégré** : Validation Chambly Plex fonctionnelle
- ✅ **Gestion des erreurs** : Retry automatique et gestion des timeouts
- ✅ **Logging structuré** : Traçabilité complète avec structlog
- ✅ **Configuration flexible** : YAML + variables d'environnement

## 🏗️ Architecture

### **Structure Modulaire**

```
src/extractors/centris/
├── 🎭 session_manager.py      # Gestion des sessions HTTP
├── 🔍 search_manager.py       # Recherche et pagination
├── 📊 summary_extractor.py    # Extraction des résumés
├── 🏠 detail_extractor.py     # Extraction des détails
├── ✅ data_validator.py       # Validation des données
└── 🚀 centris_extractor.py   # Orchestrateur principal
```

### **Composants Clés**

1. **CentrisSessionManager** : Gestion des sessions HTTP avec retry et timeout
2. **CentrisSearchManager** : Construction des requêtes et pagination
3. **CentrisSummaryExtractor** : Extraction des résumés de propriétés
4. **CentrisDetailExtractor** : Extraction des détails complets
5. **CentrisDataValidator** : Validation et nettoyage des données
6. **CentrisExtractor** : Orchestrateur principal coordonnant tous les composants

## 🛠️ Installation et Configuration

### **Prérequis**

```bash
Python 3.8+
pip install -r requirements.txt
```

### **Configuration**

1. **Copier le fichier d'environnement** :

```bash
cp env.example .env
```

2. **Configurer les variables** :

```bash
# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=real_estate
MONGODB_COLLECTION=properties

# Centris
CENTRIS_BASE_URL=https://www.centris.ca
CENTRIS_USER_AGENT=Mozilla/5.0...

# Pipeline
MAX_WORKERS=4
BATCH_SIZE=10
REQUEST_TIMEOUT=30
MAX_RETRIES=3
RETRY_DELAY=1
```

3. **Configuration YAML** (`config/config.yml`) :

```yaml
database:
  uri: ${MONGODB_URI}
  database: ${MONGODB_DATABASE}
  collection: ${MONGODB_COLLECTION}

centris:
  base_url: ${CENTRIS_BASE_URL}
  user_agent: ${CENTRIS_USER_AGENT}
  locations_searched:
    - type: "GeographicArea"
      value: "Montérégie"
      type_id: "RARA16"
    - type: "CityDistrict"
      value: "Vieux-Montréal"
      type_id: 449
  property_types: ["Plex", "SingleFamilyHome", "SellCondo"]
  sale_price_min: 200000
  sale_price_max: 260000

pipeline:
  max_workers: ${MAX_WORKERS}
  batch_size: ${BATCH_SIZE}
  request_timeout: ${REQUEST_TIMEOUT}
  max_retries: ${MAX_RETRIES}
  retry_delay: ${RETRY_DELAY}
  log_level: "INFO"
```

## 🎯 Utilisation

### **Test Principal : Chambly Plex**

```bash
# Test complet d'extraction de plex à Chambly
python run_chambly_test.py
```

### **Exécution Simple**

```bash
python run.py
```

### **Exécution avec Paramètres Personnalisés**

```python
from src.extractors.centris_extractor import CentrisExtractor
from config.settings import config
from src.models.property import SearchQuery, LocationConfig

# Initialisation
extractor = CentrisExtractor(config.centris)

# Création d'une requête de recherche
search_query = SearchQuery(
    locations=[
        LocationConfig(
            type="GeographicArea",
            value="Montérégie",
            type_id="RARA16"
        )
    ],
    property_types=["Plex"],
    price_min=200000,
    price_max=260000
)

# Extraction des résumés
summaries = await extractor.extract_summaries(search_query)
print(f"✅ {len(summaries)} propriétés trouvées")

# Extraction des détails (optionnel)
for summary in summaries[:3]:
    details = await extractor.extract_details(summary.id)
    print(f"🏠 {details.address.street} - {details.price}$")

# Fermeture propre
await extractor.close()
```

### **Types de Recherche Supportés**

#### **GeographicArea (Régions)**

```python
LocationConfig(
    type="GeographicArea",
    value="Montérégie",
    type_id="RARA16"
)
```

#### **CityDistrict (Districts de ville)**

```python
LocationConfig(
    type="CityDistrict",
    value="Vieux-Montréal",
    type_id: 449
)
```

#### **Recherche Multiple**

```python
locations=[
    LocationConfig(type="GeographicArea", value="Laurentides", type_id="RARA15"),
    LocationConfig(type="CityDistrict", value="Plateau-Mont-Royal", type_id=450)
]
```

## 🧪 Tests

### **Exécution des Tests**

```bash
# Tests de structure Centris
python tests/test_centris_structure.py

# Tests d'extraction réelle
python tests/real_extraction_test.py

# Tests d'intégration
python tests/updated_integration_test.py

# Tests de performance
python tests/performance_test.py

# Tests de robustesse
python tests/robustness_test.py

# Tous les tests d'intégration
python tests/run_integration_tests.py
```

### **Test Principal : Chambly Plex**

```bash
# Test d'extraction réelle de plex à Chambly
python run_chambly_test.py
```

Ce test valide l'extraction complète avec :

- ✅ Recherche de propriétés à Chambly
- ✅ Extraction des résumés et détails
- ✅ Sauvegarde en base MongoDB
- ✅ Validation de la cohérence type/catégorie
- ✅ Vérification de la qualité des données

### **Tests de Validation**

```bash
# Tests de performance
python tests/performance_test.py

# Tests de robustesse
python tests/robustness_test.py

# Tests d'intégration
python tests/run_integration_tests.py
```

## 📊 Modèles de Données

### **SearchQuery**

```python
class SearchQuery(BaseModel):
    locations: List[LocationConfig]
    property_types: List[PropertyType]
    price_min: Optional[float] = None
    price_max: Optional[float] = None
```

### **LocationConfig**

```python
class LocationConfig(BaseModel):
    type: str  # "GeographicArea" ou "CityDistrict"
    value: str  # Nom de la localisation
    type_id: Union[str, int]  # ID Centris (string pour GeographicArea, int pour CityDistrict)
```

### **PropertySummary**

```python
class PropertySummary(BaseModel):
    id: str
    address: Address
    price: Optional[float]
    type: PropertyType
    image_url: Optional[str]
    url: Optional[str]
    source: str = "Centris"
```

## 🔧 Configuration Avancée

### **Gestion des Timeouts**

```yaml
centris:
  request_timeout: 30 # secondes
  max_retries: 3
  retry_delay: 1
```

### **Limitation des Ressources**

```yaml
pipeline:
  max_workers: 4 # Nombre de workers concurrents
  batch_size: 10 # Taille des lots de traitement
```

### **Logging**

```yaml
pipeline:
  log_level: "INFO" # DEBUG, INFO, WARNING, ERROR
  log_file: "logs/pipeline.log"
  log_format: "json" # json ou text
```

## 📈 Performance

### **Métriques Typiques**

- **Extraction de résumés** : 8-20 propriétés par page
- **Pagination** : Jusqu'à 7+ pages par recherche
- **Débit** : 138+ propriétés en recherche multiple
- **Temps de réponse** : 1-2 secondes par page

### **Optimisations**

- Gestion asynchrone des requêtes
- Pool de workers configurable
- Retry automatique avec backoff
- Validation des données en streaming

## 🚨 Gestion des Erreurs

### **Types d'Erreurs Gérées**

- ✅ Timeouts de requêtes
- ✅ Erreurs réseau temporaires
- ✅ Données HTML malformées
- ✅ Limites de rate limiting
- ✅ Erreurs de validation des données

### **Stratégies de Récupération**

- Retry automatique avec délai progressif
- Fallback sur des sélecteurs alternatifs
- Logging détaillé pour le débogage
- Graceful degradation des fonctionnalités

## 🔄 Workflow d'Extraction

```
1. 🔧 Initialisation
   ├── Chargement de la configuration
   ├── Création des composants
   └── Validation des paramètres

2. 🔍 Recherche
   ├── Construction de la requête
   ├── Appel à l'API Centris
   └── Gestion de la pagination

3. 📊 Extraction
   ├── Parsing du HTML
   ├── Extraction des résumés
   └── Validation des données

4. 💾 Sauvegarde
   ├── Validation finale
   ├── Sauvegarde MongoDB
   └── Logging des résultats
```

## 📝 Logs et Monitoring

### **Format des Logs**

```json
{
  "timestamp": "2025-08-22T04:40:41.517661Z",
  "level": "info",
  "event": "🏠 Extraction réussie: 8 propriétés",
  "search_query": "Montérégie - Plex",
  "pages_processed": 1,
  "properties_found": 8
}
```

### **Niveaux de Log**

- **DEBUG** : Détails techniques et débogage
- **INFO** : Informations générales et métriques
- **WARNING** : Avertissements non critiques
- **ERROR** : Erreurs nécessitant une attention

## 🤝 Contribution

### **Structure du Code**

- **Type hints** : Utilisation complète des annotations Python
- **Docstrings** : Documentation claire de chaque fonction
- **Tests** : Couverture complète des fonctionnalités
- **Logging** : Traçabilité de toutes les opérations

### **Standards de Code**

- **PEP 8** : Style de code Python
- **Black** : Formatage automatique
- **isort** : Organisation des imports
- **mypy** : Vérification des types

## 📚 Ressources

### **Documentation Centris**

- [API Centris](https://www.centris.ca)
- [Structure des données](docs/centris_structure.md)

### **Technologies Utilisées**

- **asyncio** : Programmation asynchrone
- **Pydantic** : Validation des données
- **BeautifulSoup** : Parsing HTML
- **structlog** : Logging structuré
- **pymongo** : Interface MongoDB

## 🆘 Support

### **Problèmes Courants**

1. **Timeout des requêtes** : Augmenter `request_timeout`
2. **Erreurs de validation** : Vérifier la configuration YAML
3. **Problèmes de réseau** : Vérifier la connectivité et les proxies

### **Débogage**

- Activer le niveau de log `DEBUG`
- Vérifier les logs dans `logs/`
- Utiliser les scripts de test pour isoler les problèmes

---

## 🎉 Résumé

Ce pipeline offre une solution robuste et maintenable pour l'extraction de données immobilières depuis Centris.ca. Avec son architecture modulaire, ses tests complets et sa documentation détaillée, il est prêt pour la production et l'évolution future.

**🚀 Prêt à extraire des données immobilières à grande échelle !**
