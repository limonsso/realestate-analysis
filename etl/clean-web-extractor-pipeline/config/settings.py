"""
Configuration du pipeline d'extraction web immobilière
Utilise Pydantic pour la validation et la gestion des paramètres
"""

from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field, validator
from pathlib import Path
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()


class LocationConfig(BaseModel):
    """Configuration d'une localisation géographique"""
    type: str = Field(..., description="Type de localisation (GeographicArea, CityDistrict)")
    value: str = Field(..., description="Nom de la localisation")
    type_id: Union[str, int] = Field(..., description="ID unique de la localisation (string pour GeographicArea, int pour CityDistrict)")
    
    class Config:
        validate_by_name = True


class CentrisConfig(BaseModel):
    """Configuration spécifique à Centris"""
    base_url: str = Field("https://www.centris.ca", description="URL de base de Centris")
    locations_searched: List[LocationConfig] = Field(..., description="Localisations à rechercher")
    property_types: List[str] = Field(..., description="Types de propriétés à extraire")
    sale_price_max: int = Field(5000000, description="Prix de vente maximum")
    sale_price_min: int = Field(0, description="Prix de vente minimum")
    force_update: bool = Field(False, description="Forcer la mise à jour de toutes les propriétés")
    
    @validator('sale_price_max')
    def validate_price_max(cls, v):
        if v <= 0:
            raise ValueError("Le prix maximum doit être positif")
        return v


class DatabaseConfig(BaseModel):
    """Configuration de la base de données MongoDB"""
    server_url: str = Field(..., description="URL du serveur MongoDB")
    connection_string: str = Field(..., description="Chaîne de connexion MongoDB")
    database_name: str = Field(..., description="Nom de la base de données")
    username: Optional[str] = Field(None, description="Nom d'utilisateur MongoDB")
    password: Optional[str] = Field(None, description="Mot de passe MongoDB")
    auth_source: str = Field("admin", description="Source d'authentification")
    auth_mechanism: str = Field("SCRAM-SHA-256", description="Mécanisme d'authentification")
    
    # Noms des collections
    properties_collection: str = Field("properties", description="Nom de la collection des propriétés")
    summaries_collection: str = Field("property_summaries", description="Nom de la collection des résumés")
    logs_collection: str = Field("extraction_logs", description="Nom de la collection des logs")
    
    # Options de connexion
    max_pool_size: int = Field(100, description="Taille maximale du pool de connexions")
    min_pool_size: int = Field(0, description="Taille minimale du pool de connexions")
    max_idle_time_ms: int = Field(30000, description="Temps d'inactivité maximal en ms")
    server_selection_timeout_ms: int = Field(5000, description="Timeout de sélection du serveur en ms")
    connect_timeout_ms: int = Field(5000, description="Timeout de connexion en ms")
    socket_timeout_ms: int = Field(5000, description="Timeout de socket en ms")
    
    @validator('connection_string')
    def validate_connection_string(cls, v):
        if not v.startswith(('mongodb://', 'mongodb+srv://')):
            raise ValueError("La chaîne de connexion doit commencer par 'mongodb://' ou 'mongodb+srv://'")
        return v


class PipelineConfig(BaseModel):
    """Configuration globale du pipeline"""
    # Sources de données
    centris: CentrisConfig
    
    # Base de données
    database: DatabaseConfig
    
    # Performance et concurrence
    max_workers: int = Field(4, description="Nombre maximum de workers pour le traitement parallèle")
    batch_size: int = Field(50, description="Taille des lots de traitement")
    request_timeout: int = Field(30, description="Timeout des requêtes HTTP en secondes")
    
    # Logging et monitoring
    log_level: str = Field("INFO", description="Niveau de logging")
    log_file: Optional[str] = Field(None, description="Fichier de log (optionnel)")
    
    # Retry et résilience
    max_retries: int = Field(3, description="Nombre maximum de tentatives")
    retry_delay: int = Field(5, description="Délai entre les tentatives en secondes")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_config(config_path: Optional[str] = None) -> PipelineConfig:
    """
    Charge la configuration depuis un fichier YAML ou des variables d'environnement
    
    Args:
        config_path: Chemin vers le fichier de configuration YAML
        
    Returns:
        Configuration du pipeline
    """
    if config_path and Path(config_path).exists():
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        return PipelineConfig(**config_data)
    
    # Configuration par défaut depuis les variables d'environnement
    return PipelineConfig(
        centris=CentrisConfig(
            locations_searched=[
                LocationConfig(
                    type="GeographicArea",
                    value="Montérégie",
                    type_id="RARA16"
                ),
                LocationConfig(
                    type="GeographicArea", 
                    value="Laurentides",
                    type_id="RARA15"
                ),
                LocationConfig(
                    type="GeographicArea",
                    value="Lanaudière", 
                    type_id="RARA14"
                ),
                LocationConfig(
                    type="GeographicArea",
                    value="Estrie",
                    type_id="RARA05"
                ),
                LocationConfig(
                    type="GeographicArea",
                    value="Mauricie",
                    type_id="RARA04"
                ),
                LocationConfig(
                    type="GeographicArea",
                    value="Chaudière-Appalaches",
                    type_id="RARA12"
                ),
                LocationConfig(
                    type="GeographicArea",
                    value="Montréal (Île)",
                    type_id="GSGS4621"
                ),
                LocationConfig(
                    type="GeographicArea",
                    value="Laval",
                    type_id="GSGS4622"
                )
            ],
            property_types=["Plex", "SingleFamilyHome", "SellCondo", "ResidentialLot"],
            sale_price_max=int(os.getenv("SALE_PRICE_MAX", "5000000")),
            sale_price_min=int(os.getenv("SALE_PRICE_MIN", "0")),
            force_update=os.getenv("FORCE_UPDATE", "false").lower() == "true"
        ),
        database=DatabaseConfig(
            server_url=os.getenv("MONGODB_URL", "localhost:27017"),
            database_name=os.getenv("MONGODB_DB", "real_estate_db"),
            username=os.getenv("MONGODB_USERNAME"),
            password=os.getenv("MONGODB_PASSWORD")
        ),
        max_workers=int(os.getenv("MAX_WORKERS", "4")),
        batch_size=int(os.getenv("BATCH_SIZE", "50")),
        request_timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=os.getenv("LOG_FILE"),
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
        retry_delay=int(os.getenv("RETRY_DELAY", "5"))
    )


# Configuration globale
config = load_config("config/config.yml")
