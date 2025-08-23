"""
Service de base de données MongoDB
Gestion moderne des connexions et des opérations
"""

from typing import Optional, List, Dict, Any
import asyncio
from datetime import datetime, timedelta

import motor.motor_asyncio
from pymongo import ASCENDING, DESCENDING, IndexModel
from pymongo.errors import DuplicateKeyError, ConnectionFailure
import structlog

from config.settings import DatabaseConfig
from src.models.property import Property, PropertySummary


logger = structlog.get_logger()


class DatabaseService:
    """Service de gestion de la base de données MongoDB"""
    
    def __init__(self, db_config: DatabaseConfig):
        self.config = db_config
        self.client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
        self.db = None
        self.properties_collection = None
        self.summaries_collection = None
        self.extraction_logs_collection = None
        self.logger = logger  # Ajouter le logger comme attribut
        
        # Noms des collections depuis la configuration
        self.collection_names = {
            'properties': db_config.properties_collection,
            'summaries': db_config.summaries_collection,
            'logs': db_config.logs_collection
        }
    
    def set_collection_names(self, properties_collection: str = None, 
                           summaries_collection: str = None, 
                           logs_collection: str = None):
        """Configure les noms des collections MongoDB (remplace la configuration)"""
        if properties_collection:
            self.collection_names['properties'] = properties_collection
        if summaries_collection:
            self.collection_names['summaries'] = summaries_collection
        if logs_collection:
            self.collection_names['logs'] = logs_collection
        
        self.logger.info(f"📋 Noms des collections configurés:")
        self.logger.info(f"   - Propriétés: {self.collection_names['properties']}")
        self.logger.info(f"   - Résumés: {self.collection_names['summaries']}")
        self.logger.info(f"   - Logs: {self.collection_names['logs']}")
    
    async def connect(self):
        """Établit la connexion à la base de données"""
        try:
            self.logger.info(f"🔌 Connexion à MongoDB: {self.config.server_url}")
            
            # Connexion synchrone pour la compatibilité
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                self.config.connection_string,
                serverSelectionTimeoutMS=self.config.server_selection_timeout_ms,
                connectTimeoutMS=self.config.connect_timeout_ms,
                socketTimeoutMS=self.config.socket_timeout_ms,
                maxPoolSize=self.config.max_pool_size,
                minPoolSize=self.config.min_pool_size,
                maxIdleTimeMS=self.config.max_idle_time_ms
            )
            
            # Test de connexion
            self.client.admin.command('ping')
            
            # Sélection de la base de données
            self.db = self.client[self.config.database_name]
            
            # Initialisation des collections avec les noms configurés
            self.properties_collection = self.db[self.collection_names['properties']]
            self.summaries_collection = self.db[self.collection_names['summaries']]
            self.extraction_logs_collection = self.db[self.collection_names['logs']]
            
            self.logger.info("✅ Connexion MongoDB établie avec succès")
            
        except ConnectionFailure as e:
            self.logger.error(f"❌ Impossible de se connecter à MongoDB: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la connexion MongoDB: {str(e)}")
            raise
    
    async def close(self):
        """Ferme la connexion à la base de données"""
        if self.client:
            self.client.close()
            logger.info("🔌 Connexion MongoDB fermée")
    
    async def create_collection(self, collection_name: str):
        """Crée une nouvelle collection MongoDB"""
        try:
            # Vérifier si la collection existe déjà
            if collection_name in await self.db.list_collection_names():
                self.logger.info(f"📋 Collection {collection_name} existe déjà")
                return
            
            # Créer la collection
            await self.db.create_collection(collection_name)
            self.logger.info(f"✅ Collection {collection_name} créée avec succès")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la création de la collection {collection_name}: {str(e)}")
            raise
    
    async def count_properties(self, collection_name: str = None) -> int:
        """Compte le nombre de propriétés dans une collection"""
        try:
            collection = self.db[collection_name] if collection_name else self.properties_collection
            count = await collection.count_documents({})
            self.logger.debug(f"📊 {count} propriétés trouvées dans {collection_name or 'collection par défaut'}")
            return count
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du comptage des propriétés: {str(e)}")
            return 0
    
    async def get_properties(self, collection_name: str = None, limit: int = 10) -> List[Property]:
        """Récupère des propriétés depuis une collection"""
        try:
            collection = self.db[collection_name] if collection_name else self.properties_collection
            cursor = collection.find({}).limit(limit)
            properties = []
            async for doc in cursor:
                try:
                    # Convertir le document MongoDB en objet Property
                    property_data = Property(**doc)
                    properties.append(property_data)
                except Exception as e:
                    self.logger.warning(f"⚠️ Erreur lors de la conversion d'une propriété: {e}")
                    continue
            
            self.logger.debug(f"📊 {len(properties)} propriétés récupérées depuis {collection_name or 'collection par défaut'}")
            return properties
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la récupération des propriétés: {str(e)}")
            return []
    
    def ensure_indexes(self):
        """Crée les index nécessaires pour optimiser les performances"""
        try:
            logger.info("🔧 Création des index de la base de données...")
            
            # Index pour la collection des propriétés
            property_indexes = [
                IndexModel([("id", ASCENDING)], unique=True),
                IndexModel([("metadata.source", ASCENDING)]),
                IndexModel([("metadata.source_id", ASCENDING)]),
                IndexModel([("address.city", ASCENDING)]),
                IndexModel([("address.region", ASCENDING)]),
                IndexModel([("type", ASCENDING)]),
                IndexModel([("financial.price", ASCENDING)]),
                IndexModel([("metadata.last_updated", DESCENDING)]),
                IndexModel([("metadata.extraction_date", DESCENDING)])
            ]
            
            # Index pour la collection des résumés
            summary_indexes = [
                IndexModel([("id", ASCENDING)], unique=True),
                IndexModel([("source", ASCENDING)]),
                IndexModel([("address.city", ASCENDING)]),
                IndexModel([("address.region", ASCENDING)]),
                IndexModel([("type", ASCENDING)]),
                IndexModel([("price", ASCENDING)]),
                IndexModel([("last_updated", DESCENDING)])
            ]
            
            # Index pour les logs d'extraction
            log_indexes = [
                IndexModel([("timestamp", DESCENDING)]),
                IndexModel([("source", ASCENDING)]),
                IndexModel([("status", ASCENDING)]),
                IndexModel([("location", ASCENDING)]),
                IndexModel([("property_type", ASCENDING)])
            ]
            
            # Création des index
            self.properties_collection.create_indexes(property_indexes)
            self.summaries_collection.create_indexes(summary_indexes)
            self.extraction_logs_collection.create_indexes(log_indexes)
            
            logger.info("✅ Index de la base de données créés avec succès")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la création des index: {str(e)}")
            raise
    
    async def save_property(self, property_data: Property, collection_name: str = None) -> bool:
        """Sauvegarde une propriété dans la base de données"""
        try:
            if not property_data.id:
                logger.warning("⚠️ Tentative de sauvegarde d'une propriété sans ID")
                return False
            
            # Utiliser la collection spécifiée ou la collection par défaut
            collection = self.db[collection_name] if collection_name else self.properties_collection
            
            # Conversion en dictionnaire
            property_dict = property_data.dict()
            
            # Mise à jour de la date de dernière modification
            property_dict['metadata']['last_updated'] = datetime.now()
            
            # Upsert (insert ou update)
            result = await collection.update_one(
                {"id": property_data.id},
                {"$set": property_dict},
                upsert=True
            )
            
            if result.upserted_id or result.modified_count > 0:
                logger.debug(f"💾 Propriété {property_data.id} sauvegardée avec succès dans {collection_name or 'collection par défaut'}")
                return True
            else:
                logger.warning(f"⚠️ Aucune modification pour la propriété {property_data.id}")
                return False
                
        except DuplicateKeyError:
            logger.warning(f"⚠️ Propriété {property_data.id} déjà existante")
            return False
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde de {property_data.id}: {str(e)}")
            return False
    
    async def save_property_summary(self, summary: PropertySummary) -> bool:
        """Sauvegarde un résumé de propriété"""
        try:
            if not summary.id:
                logger.warning("⚠️ Tentative de sauvegarde d'un résumé sans ID")
                return False
            
            summary_dict = summary.dict()
            summary_dict['last_updated'] = datetime.now()
            
            result = await self.summaries_collection.update_one(
                {"id": summary.id},
                {"$set": summary_dict},
                upsert=True
            )
            
            if result.upserted_id or result.modified_count > 0:
                logger.debug(f"💾 Résumé {summary.id} sauvegardé avec succès")
                return True
            else:
                logger.warning(f"⚠️ Aucune modification pour le résumé {summary.id}")
                return False
                
        except DuplicateKeyError:
            logger.warning(f"⚠️ Résumé {summary.id} déjà existant")
            return False
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde du résumé {summary.id}: {str(e)}")
            return False
    
    async def get_property_by_id(self, property_id: str) -> Optional[Property]:
        """Récupère une propriété par son ID"""
        try:
            property_dict = await self.properties_collection.find_one({"id": property_id})
            if property_dict:
                return Property(**property_dict)
            return None
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération de {property_id}: {str(e)}")
            return None
    
    def get_properties_by_location(self, city: str, region: str = None) -> List[Property]:
        """Récupère les propriétés par localisation"""
        try:
            query = {"address.city": city}
            if region:
                query["address.region"] = region
            
            cursor = self.properties_collection.find(query)
            properties = []
            
            for property_dict in cursor:
                try:
                    properties.append(Property(**property_dict))
                except Exception as e:
                    logger.warning(f"⚠️ Erreur lors de la désérialisation d'une propriété: {str(e)}")
                    continue
            
            return properties
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération par localisation: {str(e)}")
            return []
    
    def get_properties_by_type(self, property_type: str) -> List[Property]:
        """Récupère les propriétés par type"""
        try:
            cursor = self.properties_collection.find({"type": property_type})
            properties = []
            
            for property_dict in cursor:
                try:
                    properties.append(Property(**property_dict))
                except Exception as e:
                    logger.warning(f"⚠️ Erreur lors de la désérialisation d'une propriété: {str(e)}")
                    continue
            
            return properties
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération par type: {str(e)}")
            return []
    
    def get_properties_by_price_range(self, min_price: float, max_price: float) -> List[Property]:
        """Récupère les propriétés dans une fourchette de prix"""
        try:
            query = {
                "financial.price": {
                    "$gte": min_price,
                    "$lte": max_price
                }
            }
            
            cursor = self.properties_collection.find(query).sort("financial.price", ASCENDING)
            properties = []
            
            for property_dict in cursor:
                try:
                    properties.append(Property(**property_dict))
                except Exception as e:
                    logger.warning(f"⚠️ Erreur lors de la désérialisation d'une propriété: {str(e)}")
                    continue
            
            return properties
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération par prix: {str(e)}")
            return []
    
    def get_recent_properties(self, hours: int = 24) -> List[Property]:
        """Récupère les propriétés ajoutées/modifiées récemment"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            cursor = self.properties_collection.find({
                "metadata.last_updated": {"$gte": cutoff_time}
            }).sort("metadata.last_updated", DESCENDING)
            
            properties = []
            for property_dict in cursor:
                try:
                    properties.append(Property(**property_dict))
                except Exception as e:
                    logger.warning(f"⚠️ Erreur lors de la désérialisation d'une propriété: {str(e)}")
                    continue
            
            return properties
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération des propriétés récentes: {str(e)}")
            return []
    
    def log_extraction(self, source: str, location: str, property_type: str, 
                       status: str, message: str, details: Dict[str, Any] = None):
        """Enregistre un log d'extraction"""
        try:
            log_entry = {
                "timestamp": datetime.now(),
                "source": source,
                "location": location,
                "property_type": property_type,
                "status": status,
                "message": message,
                "details": details or {}
            }
            
            self.extraction_logs_collection.insert_one(log_entry)
            logger.debug(f"📝 Log d'extraction enregistré: {source} - {location} - {property_type}")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'enregistrement du log: {str(e)}")
    
    def get_extraction_stats(self, source: str = None, days: int = 7) -> Dict[str, Any]:
        """Récupère les statistiques d'extraction"""
        try:
            cutoff_time = datetime.now() - timedelta(days=days)
            
            # Pipeline d'agrégation pour les statistiques
            pipeline = [
                {"$match": {"timestamp": {"$gte": cutoff_time}}},
                {"$group": {
                    "_id": {
                        "source": "$source",
                        "location": "$location",
                        "property_type": "$property_type",
                        "status": "$status"
                    },
                    "count": {"$sum": 1}
                }},
                {"$group": {
                    "_id": {
                        "source": "$_id.source",
                        "location": "$_id.location",
                        "property_type": "$_id.property_type"
                    },
                    "statuses": {
                        "$push": {
                            "status": "$_id.status",
                            "count": "$count"
                        }
                    },
                    "total": {"$sum": "$count"}
                }}
            ]
            
            if source:
                pipeline[0]["$match"]["source"] = source
            
            cursor = self.extraction_logs_collection.aggregate(pipeline)
            stats = list(cursor)
            
            return {
                "period_days": days,
                "source": source,
                "statistics": stats
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération des statistiques: {str(e)}")
            return {}
    
    def cleanup_old_logs(self, days: int = 30):
        """Nettoie les anciens logs d'extraction"""
        try:
            cutoff_time = datetime.now() - timedelta(days=days)
            
            result = self.extraction_logs_collection.delete_many({
                "timestamp": {"$lt": cutoff_time}
            })
            
            logger.info(f"🧹 {result.deleted_count} anciens logs supprimés (plus de {days} jours)")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage des logs: {str(e)}")
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques de la base de données"""
        try:
            stats = {
                "properties_count": self.properties_collection.count_documents({}),
                "summaries_count": self.summaries_collection.count_documents({}),
                "logs_count": self.extraction_logs_collection.count_documents({}),
                "database_size": self.db.command("dbStats")["dataSize"],
                "collections": self.db.list_collection_names()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération des stats DB: {str(e)}")
            return {}
