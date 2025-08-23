#!/usr/bin/env python3
"""
Test d'Extraction Corrigé: Plex à Trois-Rivières
============================================================
Version corrigée qui force l'utilisation de la configuration Trois-Rivières
et évite les conflits avec la configuration par défaut.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extractors.centris_extractor import CentrisExtractor
from src.services.database_service import DatabaseService
from config.settings import load_config
from src.models.property import PropertyType, LocationConfig
from src.extractors.centris.data_validator import CentrisDataValidator
import structlog

# Configuration du logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


class TroisRivieresPlexExtractionTestFixed:
    """Test d'extraction de plex à Trois-Rivières (Version Corrigée)"""
    
    def __init__(self):
        self.config = None
        self.extractor = None
        self.db_service = None
        self.validator = None
        self.test_results = {}
        
    async def setup(self):
        """Configuration du test avec configuration forcée"""
        logger.info("🔧 Configuration du test d'extraction Trois-Rivières (Corrigé)")
        
        # Charger la configuration spécifique à Trois-Rivières
        config_path = "config/config.trois_rivieres_test.yml"
        try:
            self.config = load_config(config_path)
            logger.info(f"✅ Configuration chargée depuis {config_path}")
        except Exception as e:
            logger.error(f"❌ Impossible de charger {config_path}: {e}")
            raise
        
        # Vérifier que la configuration contient bien Trois-Rivières
        if not self.config.centris.locations_searched:
            raise ValueError("Configuration Centris vide")
        
        # Forcer la configuration Trois-Rivières
        self.config.centris.locations_searched = [
            {
                'type': 'CityDistrict',
                'value': 'Trois-Rivières',
                'type_id': 449
            }
        ]
        
        logger.info(f"🔒 Configuration forcée: {self.config.centris.locations_searched}")
        
        # Initialiser l'extracteur Centris avec la configuration forcée
        self.extractor = CentrisExtractor(
            config=self.config.centris
        )
        logger.debug("✅ CentrisExtractor initialisé avec configuration Trois-Rivières")
        
        # Initialiser le service de base de données
        self.db_service = DatabaseService(self.config.database)
        await self.db_service.connect()
        logger.debug("✅ DatabaseService initialisé et connecté")
        
        # Initialiser le validateur
        self.validator = CentrisDataValidator()
        
        logger.info("✅ Configuration terminée avec configuration Trois-Rivières forcée")
        
    async def create_search_query(self):
        """Créer la requête de recherche pour Trois-Rivières (forcée)"""
        logger.info("🔍 Création de la requête de recherche Trois-Rivières (forcée)")
        
        # Configuration Trois-Rivières FORCÉE
        location = LocationConfig(
            type="CityDistrict",
            value="Trois-Rivières", 
            type_id=449
        )
        
        # Types de propriétés à rechercher
        property_types = [PropertyType.PLEX]
        
        # Fourchette de prix
        min_price = 100000
        max_price = 1000000
        
        logger.info(f"📍 Recherche configurée: Trois-Rivières - Plex (FORCÉE)")
        logger.info(f"💰 Fourchette de prix: {min_price:,.0f}$ - {max_price:,.0f}$")
        logger.info(f"🔒 Localisation forcée: {location.value} (ID: {location.type_id})")
        
        return {
            'location': location,
            'property_types': property_types,
            'min_price': min_price,
            'max_price': max_price
        }
        
    async def extract_properties(self, search_query):
        """Extraire les résumés de propriétés selon les critères (forcés)"""
        logger.info("🏠 Début de l'extraction des propriétés Trois-Rivières (forcée)")
        
        try:
            # Créer l'objet SearchQuery
            from src.models.property import SearchQuery
            
            search_query_obj = SearchQuery(
                locations=[search_query['location']],
                property_types=search_query['property_types'],
                min_price=search_query['min_price'],
                max_price=search_query['max_price']
            )
            
            logger.info(f"🔒 SearchQuery créée avec localisation forcée: {search_query_obj.locations}")
            
            # Extraire les résumés
            summaries = await self.extractor.extract_summaries(search_query_obj)
            
            logger.info(f"📊 {len(summaries)} résumés de propriétés extraits")
            
            # Filtrer STRICTEMENT les propriétés à Trois-Rivières
            trois_rivieres_properties = []
            for summary in summaries:
                if self._is_trois_rivieres_property_strict(summary):
                    trois_rivieres_properties.append(summary)
                    logger.info(f"🏠 Propriété Trois-Rivières confirmée: {summary.address.street}, {summary.address.city}")
                else:
                    logger.warning(f"⚠️ Propriété rejetée (pas à Trois-Rivières): {summary.address.street}, {summary.address.city}")
            
            logger.info(f"🎯 {len(trois_rivieres_properties)} propriétés confirmées à Trois-Rivières")
            
            if len(trois_rivieres_properties) == 0:
                logger.error("❌ AUCUNE propriété Trois-Rivières trouvée - Vérifier la configuration")
            
            return trois_rivieres_properties
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction: {e}")
            return []
            
    def _is_trois_rivieres_property_strict(self, summary):
        """Vérification STRICTE que la propriété est à Trois-Rivières"""
        try:
            if not summary.address or not summary.address.city:
                return False
            
            city_lower = summary.address.city.lower()
            street_lower = summary.address.street.lower() if summary.address.street else ""
            
            # Vérification stricte avec gestion du formatage incorrect
            is_trois_rivieres = (
                "trois-rivières" in city_lower or 
                "trois-rivières" in street_lower or
                "trois-rivieres" in city_lower or
                "trois-rivieres" in street_lower or
                # Gestion du cas où la ville est collée à la rue (bug de formatage)
                "trois-rivières" in (street_lower + city_lower) or
                "trois-rivieres" in (street_lower + city_lower)
            )
            
            # Log de débogage
            if not is_trois_rivieres:
                logger.debug(f"🔍 Propriété rejetée - Ville: '{summary.address.city}', Rue: '{summary.address.street}'")
                logger.debug(f"🔍 Concaténation: '{street_lower + city_lower}'")
            
            return is_trois_rivieres
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation Trois-Rivières: {e}")
            return False
            
    async def extract_property_details(self, summaries):
        """Extraire les détails des propriétés à partir des résumés"""
        logger.info("🔍 Extraction des détails des propriétés Trois-Rivières")
        detailed_properties = []
        
        for i, summary in enumerate(summaries):
            logger.info(f"🔍 Extraction détaillée {i+1}/{len(summaries)}: {summary.id}")
            
            try:
                # Construire l'URL complète
                property_url = f"https://www.centris.ca/fr/propriete/{summary.id}"
                
                # Extraire les détails
                property_details = await self.extractor.extract_details(property_url)
                
                if property_details:
                    # Vérifier à nouveau que c'est bien Trois-Rivières
                    if self._is_trois_rivieres_property_strict(property_details):
                        detailed_properties.append(property_details)
                        logger.info(f"✅ Détails extraits pour {summary.address.street} (Trois-Rivières confirmé)")
                    else:
                        logger.warning(f"⚠️ Propriété rejetée après extraction détaillée: {summary.address.street}")
                else:
                    logger.warning(f"⚠️ Aucun détail extrait pour {summary.id}")
                    
            except Exception as e:
                logger.error(f"❌ Erreur lors de l'extraction des détails: {e}")
                continue
                
        logger.info(f"📋 {len(detailed_properties)} propriétés Trois-Rivières détaillées extraites")
        return detailed_properties
            
    async def save_to_database(self, properties):
        """Sauvegarder les propriétés en base (collections temporaires)"""
        if not properties:
            logger.warning("⚠️ Aucune propriété à sauvegarder")
            return None
            
        try:
            # Créer un nom de collection unique avec timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            collection_name = f"trois_rivieres_plex_test_fixed_{timestamp}"
            
            logger.info(f"💾 Sauvegarde de {len(properties)} propriétés dans {collection_name}")
            logger.info(f"🔒 Utilisation de collection temporaire (évite properties_2024)")
            
            # Forcer l'utilisation de la collection temporaire
            self.db_service.set_collection_names({
                'properties': collection_name,
                'summaries': f"trois_rivieres_summaries_fixed_{timestamp}",
                'logs': f"trois_rivieres_logs_fixed_{timestamp}"
            })
            
            # Créer la collection
            await self.db_service.create_collection(collection_name)
            logger.info(f"✅ Collection {collection_name} créée avec succès")
            
            # Sauvegarder chaque propriété
            saved_count = 0
            for prop in properties:
                try:
                    await self.db_service.save_property(prop)
                    saved_count += 1
                    logger.info(f"💾 Propriété Trois-Rivières sauvegardée: {prop.address.street}")
                except Exception as e:
                    logger.error(f"❌ Erreur lors de la sauvegarde de {prop.id}: {e}")
                    
            logger.info(f"✅ {saved_count}/{len(properties)} propriétés Trois-Rivières sauvegardées avec succès")
            return collection_name
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")
            return None
            
    async def validate_results(self, collection_name):
        """Valider les résultats extraits (Trois-Rivières uniquement)"""
        if not collection_name:
            logger.warning("⚠️ Aucune collection à valider")
            return {}
            
        logger.info(f"🔍 Validation des résultats Trois-Rivières dans {collection_name}")
        
        try:
            # Configurer la collection
            self.db_service.set_collection_names({
                'properties': collection_name
            })
            
            # Compter les propriétés
            total_properties = await self.db_service.count_properties()
            logger.info(f"📊 {total_properties} propriétés trouvées en base")
            
            # Récupérer quelques propriétés pour validation
            properties = await self.db_service.get_properties(limit=5)
            logger.info(f"📊 {len(properties)} propriétés récupérées depuis {collection_name}")
            
            # Afficher des exemples
            for i, prop in enumerate(properties, 1):
                logger.info(f"🏠 Exemple {i}:")
                logger.info(f"   📍 Adresse: {prop.address.street}, {prop.address.city}")
                logger.info(f"   💰 Prix: {prop.financial.price:,.0f}$")
                logger.info(f"   🏠 Type: {prop.type}")
                logger.info(f"   🆔 ID: {prop.id}")
                
            # Validation des données
            validation_results = await self._validate_data_quality(properties)
            
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation: {e}")
            return {}
            
    async def _validate_data_quality(self, properties):
        """Valider la qualité des données extraites (Trois-Rivières)"""
        if not properties:
            return {}
            
        results = {}
        
        try:
            # Validation des adresses
            addresses_complete = all(
                p.address and p.address.street and p.address.city 
                for p in properties
            )
            results['adresses_complètes'] = addresses_complete
            
            # Validation des prix
            prices_valid = all(
                p.financial and p.financial.price and p.financial.price > 0
                for p in properties
            )
            results['prix_valides'] = prices_valid
            
            # Validation des types
            types_correct = all(
                p.type and p.type.lower() in ['plex', 'duplex', 'triplex', 'quadruplex', 'quintuplex']
                for p in properties
            )
            results['types_corrects'] = types_correct
            
            # Validation des IDs
            ids_unique = len(set(p.id for p in properties)) == len(properties)
            results['ids_uniques'] = ids_unique
            
            # Validation STRICTE de la localisation Trois-Rivières
            location_trois_rivieres = all(
                p.address and p.address.city and 
                ("trois-rivières" in p.address.city.lower() or "trois-rivières" in p.address.street.lower())
                for p in properties
            )
            results['localisation_trois_rivieres'] = location_trois_rivieres
            
            logger.info("📋 Résultats de validation Trois-Rivières:")
            for key, value in results.items():
                status = "✅" if value else "❌"
                logger.info(f"   {status} {key}: {value}")
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation des données: {e}")
            
        return results
        
    async def cleanup(self):
        """Nettoyer les ressources"""
        logger.info("🧹 Nettoyage des ressources")
        
        try:
            # Fermer l'extracteur
            if hasattr(self, 'extractor') and self.extractor is not None:
                await self.extractor.close()
                logger.info("🔌 CentrisExtractor fermé proprement")
                
            # Fermer la connexion MongoDB
            if hasattr(self, 'db_service') and self.db_service is not None:
                await self.db_service.close()
                logger.info("🔌 Connexion MongoDB fermée")
                
            logger.info("✅ Nettoyage terminé")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage: {e}")
            
    async def run_test(self):
        """Exécute le test complet d'extraction (Version Corrigée)."""
        logger.info("🚀 Démarrage du test d'extraction Trois-Rivières Plex (Version Corrigée)")
        
        try:
            # Configuration
            await self.setup()
            
            # Création de la requête
            search_query = await self.create_search_query()
            
            # Extraction des propriétés
            summaries = await self.extract_properties(search_query)
            
            if not summaries:
                logger.error("❌ AUCUNE propriété Trois-Rivières trouvée - Test échoué")
                return {
                    "success": False,
                    "error": "Aucune propriété Trois-Rivières trouvée"
                }
            
            # Extraction des détails
            detailed_properties = await self.extract_property_details(summaries)
            
            if not detailed_properties:
                logger.error("❌ AUCUN détail extrait - Test échoué")
                return {
                    "success": False,
                    "error": "Aucun détail extrait"
                }
            
            # Sauvegarde en base
            collection_name = await self.save_to_database(detailed_properties)
            
            # Validation des résultats
            validation_results = await self.validate_results(collection_name)
            
            # Résumé du test
            logger.info("🎉 Test d'extraction Trois-Rivières (Corrigé) terminé avec succès!")
            logger.info(f"📊 Résumé:")
            logger.info(f"   🏠 Résumés extraits: {len(summaries)}")
            logger.info(f"   🔍 Détails extraits: {len(detailed_properties)}")
            logger.info(f"   💾 Collection créée: {collection_name}")
            logger.info(f"   ✅ Validation: {sum(validation_results.values())}/{len(validation_results)} critères")
            logger.info(f"   🔒 Configuration Trois-Rivières forcée: ✅")
            
            return {
                "success": True,
                "summaries_count": len(summaries),
                "details_count": len(detailed_properties),
                "collection_name": collection_name,
                "validation_results": validation_results
            }
            
        except Exception as e:
            logger.error(f"❌ Test échoué: {e}")
            return {
                "success": False,
                "error": str(e)
            }
        
        finally:
            await self.cleanup()


if __name__ == "__main__":
    # Test direct
    async def test():
        test_instance = TroisRivieresPlexExtractionTestFixed()
        result = await test_instance.run_test()
        print(f"Résultat: {result}")
    
    asyncio.run(test())
