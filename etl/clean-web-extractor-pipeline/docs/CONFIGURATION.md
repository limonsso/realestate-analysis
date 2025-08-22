# ⚙️ Guide de Configuration du Pipeline

## 📋 Vue d'Ensemble

Le pipeline utilise un système de configuration flexible combinant variables d'environnement, fichiers YAML et validation Pydantic. Cette approche permet une configuration adaptée à différents environnements (développement, test, production).

## 🎯 **Configuration Optimisée**

La configuration a été **nettoyée et optimisée** pour :

- ✅ Supprimer les fichiers redondants (`simple_chambly_config.yml`)
- ✅ Simplifier la gestion des environnements
- ✅ Centraliser les validations dans `TypeCategoryValidator`
- ✅ Améliorer la maintenabilité et la lisibilité

## 🏗️ Architecture de Configuration

### **Hiérarchie des Fichiers**

```
config/
├── 📄 config.yml              # Configuration principale
├── ⚙️ settings.py             # Modèles Pydantic et validation
├── 🆔 centris_ids.yml         # Identifiants Centris
└── 🔧 config.example.yml      # Exemple de configuration
```

### **Ordre de Priorité**

1. **Variables d'environnement** (priorité haute)
2. **Fichier YAML** (`config/config.yml`)
3. **Valeurs par défaut** (dans le code)

## 🔧 Configuration Principale

### **Fichier `config/config.yml`**

#### **Structure Complète**

```yaml
# Configuration de la base de données
database:
  uri: ${MONGODB_URI}
  database: ${MONGODB_DATABASE}
  collection: ${MONGODB_COLLECTION}
  max_pool_size: 100
  min_pool_size: 0
  server_selection_timeout_ms: 5000
  connect_timeout_ms: 5000
  socket_timeout_ms: 5000

# Configuration Centris
centris:
  base_url: ${CENTRIS_BASE_URL}
  user_agent: ${CENTRIS_USER_AGENT}
  request_timeout: ${REQUEST_TIMEOUT}
  max_retries: ${MAX_RETRIES}
  retry_delay: ${RETRY_DELAY}

  # Localisations de recherche
  locations_searched:
    - type: "GeographicArea"
      value: "Montérégie"
      type_id: "RARA16"
    - type: "CityDistrict"
      value: "Vieux-Montréal"
      type_id: 449

  # Types de propriétés
  property_types: ["Plex", "SingleFamilyHome", "SellCondo"]

  # Fourchettes de prix
  sale_price_min: ${SALE_PRICE_MIN}
  sale_price_max: ${SALE_PRICE_MAX}

# Configuration du pipeline
pipeline:
  max_workers: ${MAX_WORKERS}
  batch_size: ${BATCH_SIZE}
  request_timeout: ${REQUEST_TIMEOUT}
  max_retries: ${MAX_RETRIES}
  retry_delay: ${RETRY_DELAY}

  # Logging
  log_level: ${LOG_LEVEL}
  log_file: ${LOG_FILE}
  log_format: ${LOG_FORMAT}

  # Performance
  enable_cache: true
  cache_ttl: 3600
  rate_limit: 10 # requêtes par seconde
```

## 🔑 Variables d'Environnement

### **Fichier `.env`**

#### **Configuration MongoDB**

```bash
# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=real_estate
MONGODB_COLLECTION=properties
MONGODB_USERNAME=admin
MONGODB_PASSWORD=secret
MONGODB_AUTH_SOURCE=admin
```

#### **Configuration Centris**

```bash
# Centris
CENTRIS_BASE_URL=https://www.centris.ca
CENTRIS_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
```

#### **Configuration Pipeline**

```bash
# Pipeline
MAX_WORKERS=4
BATCH_SIZE=10
REQUEST_TIMEOUT=30
MAX_RETRIES=3
RETRY_DELAY=1
LOG_LEVEL=INFO
LOG_FILE=logs/pipeline.log
LOG_FORMAT=json
```

#### **Configuration des Prix**

```bash
# Fourchettes de prix
SALE_PRICE_MIN=200000
SALE_PRICE_MAX=260000
```

### **Variables d'Environnement Système**

```bash
# Linux/Mac
export MONGODB_URI="mongodb://localhost:27017"
export LOG_LEVEL="DEBUG"

# Windows PowerShell
$env:MONGODB_URI="mongodb://localhost:27017"
$env:LOG_LEVEL="DEBUG"
```

## 🆔 Configuration Centris

### **Fichier `config/centris_ids.yml`**

#### **Structure des Identifiants**

```yaml
# Types de localisations supportés
location_types:
  GeographicArea:
    description: "Régions administratives du Québec"
    examples:
      - type: "GeographicArea"
        value: "Montérégie"
        type_id: "RARA16"
      - type: "GeographicArea"
        value: "Laurentides"
        type_id: "RARA15"
      - type: "GeographicArea"
        value: "Lanaudière"
        type_id: "RARA14"
      - type: "GeographicArea"
        value: "Laval"
        type_id: "RARA13"
      - type: "GeographicArea"
        value: "Montréal (Île)"
        type_id: "RARA12"
      - type: "GeographicArea"
        value: "Mauricie"
        type_id: "RARA11"
      - type: "GeographicArea"
        value: "Estrie"
        type_id: "RARA10"

  CityDistrict:
    description: "Districts de ville spécifiques"
    examples:
      - type: "CityDistrict"
        value: "Vieux-Montréal"
        type_id: 449
      - type: "CityDistrict"
        value: "Plateau-Mont-Royal"
        type_id: 450
      - type: "CityDistrict"
        value: "Mile-End"
        type_id: 451
      - type: "CityDistrict"
        value: "Outremont"
        type_id: 452

# Structure des requêtes API
request_structure:
  description: "Format des requêtes pour l'API Centris"
  example:
    query:
      UseGeographyShapes: 0
      FieldsValues:
        - fieldId: "GeographicArea"
          value: "RARA16"
        - fieldId: "PropertyType"
          value: "Plex"
        - fieldId: "SalePrice"
          value: 200000.0
        - fieldId: "SalePrice"
          value: 260000.0

# Types de propriétés supportés
property_types:
  - "SingleFamilyHome" # Maison unifamiliale
  - "Plex" # Plex (duplex, triplex, etc.)
  - "SellCondo" # Condo à vendre
  - "RentalCondo" # Condo à louer
  - "ResidentialLot" # Terrain résidentiel
  - "Commercial" # Commercial
  - "Industrial" # Industriel
```

## ⚙️ Modèles de Configuration Pydantic

### **Fichier `config/settings.py`**

#### **Modèles de Configuration**

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from typing_extensions import Literal

class DatabaseConfig(BaseModel):
    uri: str = Field(..., description="URI de connexion MongoDB")
    database: str = Field(..., description="Nom de la base de données")
    collection: str = Field(..., description="Nom de la collection")
    max_pool_size: int = Field(default=100, description="Taille max du pool de connexions")
    min_pool_size: int = Field(default=0, description="Taille min du pool de connexions")
    server_selection_timeout_ms: int = Field(default=5000, description="Timeout de sélection du serveur")
    connect_timeout_ms: int = Field(default=5000, description="Timeout de connexion")
    socket_timeout_ms: int = Field(default=5000, description="Timeout des sockets")

class LocationConfig(BaseModel):
    type: str = Field(..., description="Type de localisation (GeographicArea, CityDistrict)")
    value: str = Field(..., description="Nom de la localisation")
    type_id: Union[str, int] = Field(..., description="ID Centris (string pour GeographicArea, int pour CityDistrict)")

    class Config:
        validate_by_name = True

class CentrisConfig(BaseModel):
    base_url: str = Field(default="https://www.centris.ca", description="URL de base Centris")
    user_agent: str = Field(..., description="User-Agent pour les requêtes HTTP")
    request_timeout: int = Field(default=30, description="Timeout des requêtes en secondes")
    max_retries: int = Field(default=3, description="Nombre maximum de tentatives")
    retry_delay: int = Field(default=1, description="Délai entre tentatives en secondes")
    locations_searched: List[LocationConfig] = Field(..., description="Localisations de recherche")
    property_types: List[str] = Field(..., description="Types de propriétés à rechercher")
    sale_price_min: Optional[float] = Field(None, description="Prix de vente minimum")
    sale_price_max: Optional[float] = Field(None, description="Prix de vente maximum")

class PipelineConfig(BaseModel):
    max_workers: int = Field(default=4, description="Nombre maximum de workers concurrents")
    batch_size: int = Field(default=10, description="Taille des lots de traitement")
    request_timeout: int = Field(default=30, description="Timeout des requêtes en secondes")
    max_retries: int = Field(default=3, description="Nombre maximum de tentatives")
    retry_delay: int = Field(default=1, description="Délai entre tentatives en secondes")
    log_level: str = Field(default="INFO", description="Niveau de log")
    log_file: Optional[str] = Field(None, description="Fichier de log")
    log_format: Literal["json", "text"] = Field(default="json", description="Format des logs")
    enable_cache: bool = Field(default=True, description="Activer le cache")
    cache_ttl: int = Field(default=3600, description="TTL du cache en secondes")
    rate_limit: int = Field(default=10, description="Limite de taux (requêtes/seconde)")

class Config(BaseModel):
    database: DatabaseConfig
    centris: CentrisConfig
    pipeline: PipelineConfig
```

## 🔄 Chargement de la Configuration

### **Fonction `load_config()`**

#### **Logique de Chargement**

```python
import os
from pathlib import Path
from typing import Optional
from .settings import Config

def load_config(config_path: Optional[str] = None) -> Config:
    """
    Charge la configuration depuis les variables d'environnement et le fichier YAML.

    Args:
        config_path: Chemin vers le fichier de configuration YAML

    Returns:
        Config: Configuration validée

    Raises:
        FileNotFoundError: Si le fichier de configuration n'existe pas
        ValidationError: Si la configuration est invalide
    """
    # Définir le chemin par défaut
    if config_path is None:
        config_path = "config/config.yml"

    # Vérifier l'existence du fichier
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Fichier de configuration non trouvé: {config_path}")

    # Charger depuis YAML
    config_data = load_yaml_config(config_path)

    # Fusionner avec les variables d'environnement
    config_data = merge_with_env_vars(config_data)

    # Valider et retourner
    return Config(**config_data)
```

#### **Fusion avec les Variables d'Environnement**

```python
def merge_with_env_vars(config_data: dict) -> dict:
    """
    Fusionne la configuration YAML avec les variables d'environnement.

    Args:
        config_data: Configuration chargée depuis YAML

    Returns:
        dict: Configuration fusionnée
    """
    # Variables MongoDB
    if os.getenv("MONGODB_URI"):
        config_data["database"]["uri"] = os.getenv("MONGODB_URI")
    if os.getenv("MONGODB_DATABASE"):
        config_data["database"]["database"] = os.getenv("MONGODB_DATABASE")
    if os.getenv("MONGODB_COLLECTION"):
        config_data["database"]["collection"] = os.getenv("MONGODB_COLLECTION")

    # Variables Centris
    if os.getenv("CENTRIS_BASE_URL"):
        config_data["centris"]["base_url"] = os.getenv("CENTRIS_BASE_URL")
    if os.getenv("CENTRIS_USER_AGENT"):
        config_data["centris"]["user_agent"] = os.getenv("CENTRIS_USER_AGENT")

    # Variables Pipeline
    if os.getenv("MAX_WORKERS"):
        config_data["pipeline"]["max_workers"] = int(os.getenv("MAX_WORKERS"))
    if os.getenv("BATCH_SIZE"):
        config_data["pipeline"]["batch_size"] = int(os.getenv("BATCH_SIZE"))
    if os.getenv("LOG_LEVEL"):
        config_data["pipeline"]["log_level"] = os.getenv("LOG_LEVEL")

    return config_data
```

## 🎯 Configurations par Environnement

### **Développement**

```yaml
# config/config.dev.yml
database:
  uri: mongodb://localhost:27017
  database: real_estate_dev
  collection: properties_dev

pipeline:
  log_level: DEBUG
  max_workers: 2
  batch_size: 5
  enable_cache: false
```

### **Test**

```yaml
# config/config.test.yml
database:
  uri: mongodb://localhost:27017
  database: real_estate_test
  collection: properties_test

pipeline:
  log_level: INFO
  max_workers: 1
  batch_size: 3
  enable_cache: false
```

### **Production**

```yaml
# config/config.prod.yml
database:
  uri: ${MONGODB_PROD_URI}
  database: ${MONGODB_PROD_DATABASE}
  collection: ${MONGODB_PROD_COLLECTION}
  max_pool_size: 200
  min_pool_size: 10

pipeline:
  log_level: WARNING
  max_workers: 8
  batch_size: 20
  enable_cache: true
  rate_limit: 5
```

## 🔧 Configuration Avancée

### **Gestion des Timeouts**

```yaml
centris:
  request_timeout: 60 # Timeout principal
  connect_timeout: 30 # Timeout de connexion
  read_timeout: 45 # Timeout de lecture
  write_timeout: 45 # Timeout d'écriture
```

### **Configuration des Retry**

```yaml
centris:
  max_retries: 5
  retry_delay: 2
  retry_backoff: 1.5 # Multiplicateur exponentiel
  retry_exceptions:
    - "ConnectionError"
    - "TimeoutError"
    - "HTTPError"
```

### **Configuration du Cache**

```yaml
pipeline:
  enable_cache: true
  cache_ttl: 7200 # 2 heures
  cache_max_size: 10000 # 10k entrées max
  cache_eviction_policy: "lru"
```

### **Configuration du Rate Limiting**

```yaml
pipeline:
  rate_limit: 10 # 10 requêtes/seconde
  rate_limit_burst: 20 # Burst de 20 requêtes
  rate_limit_window: 60 # Fenêtre de 60 secondes
```

## 🧪 Validation de Configuration

### **Tests de Configuration**

```python
# tests/test_config.py
def test_config_validation():
    """Test de validation de la configuration."""
    config = load_config("config/config.yml")

    # Validation de la base de données
    assert config.database.uri.startswith("mongodb://")
    assert config.database.database
    assert config.database.collection

    # Validation de Centris
    assert config.centris.base_url.startswith("https://")
    assert config.centris.user_agent
    assert len(config.centris.locations_searched) > 0

    # Validation du pipeline
    assert config.pipeline.max_workers > 0
    assert config.pipeline.batch_size > 0
    assert config.pipeline.log_level in ["DEBUG", "INFO", "WARNING", "ERROR"]

def test_environment_override():
    """Test de surcharge par variables d'environnement."""
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["MAX_WORKERS"] = "8"

    config = load_config("config/config.yml")

    assert config.pipeline.log_level == "DEBUG"
    assert config.pipeline.max_workers == 8
```

## 🚨 Dépannage de Configuration

### **Problèmes Courants**

#### **1. Fichier de Configuration Introuvable**

```bash
# Vérifier le chemin
ls -la config/
cat config/config.yml

# Vérifier les permissions
chmod 644 config/config.yml
```

#### **2. Erreurs de Validation**

```bash
# Activer les logs de validation
export PYDANTIC_VERBOSE=1
python -c "from config.settings import load_config; load_config()"
```

#### **3. Variables d'Environnement Manquantes**

```bash
# Vérifier les variables
env | grep -E "(MONGODB|CENTRIS|PIPELINE)"

# Charger depuis un fichier
source .env
```

### **Outils de Diagnostic**

```python
# diagnostic_config.py
from config.settings import load_config
import json

def diagnose_config():
    """Diagnostique de la configuration."""
    try:
        config = load_config()
        print("✅ Configuration valide")
        print(json.dumps(config.model_dump(), indent=2, default=str))
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        print(f"Type d'erreur: {type(e).__name__}")

if __name__ == "__main__":
    diagnose_config()
```

## 📈 Optimisation de Configuration

### **Performance**

```yaml
pipeline:
  max_workers: 4 # Optimisé pour 4 cœurs
  batch_size: 10 # Équilibre mémoire/performance
  enable_cache: true # Cache activé
  cache_ttl: 3600 # Cache 1 heure
```

### **Résilience**

```yaml
centris:
  max_retries: 5 # Plus de tentatives
  retry_delay: 2 # Délai plus long
  request_timeout: 60 # Timeout plus long
```

### **Monitoring**

```yaml
pipeline:
  log_level: INFO # Logs informatifs
  log_format: json # Format structuré
  log_file: logs/pipeline.log # Fichier de log
```

---

## 🎉 Conclusion

Le système de configuration flexible du pipeline permet une adaptation facile à différents environnements et besoins. La validation Pydantic garantit la cohérence des données, tandis que la fusion avec les variables d'environnement offre flexibilité et sécurité.

**⚙️ Configuration robuste et flexible - Pipeline adapté à tous les environnements !**
