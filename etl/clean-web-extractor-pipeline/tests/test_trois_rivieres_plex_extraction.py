#!/usr/bin/env python3
"""
Test d'Extraction Réelle: Plex à Trois-Rivières
============================================================
Ce test va:
1. 🔍 Rechercher des plex à Trois-Rivières sur Centris.ca
2. 📊 Extraire les résumés et détails des propriétés
3. 💾 Sauvegarder les données en base MongoDB
4. ✅ Valider la qualité des données extraites
============================================================
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


class TroisRivieresPlexExtractionTest:
    """Test d'extraction de plex à Trois-Rivières"""
    
    def __init__(self):
        self.config = None
        self.extractor = None
        self.db_service = None
        self.validator = None
        self.test_results = {}
        
    async def setup(self):
        """Configuration du test"""
        logger.info("🔧 Configuration du test d'extraction Trois-Rivières")
        
        # Charger la configuration spécifique à Trois-Rivières
        config_path = "config/config.trois_rivieres_test.yml"
        try:
            self.config = load_config(config_path)
            logger.info(f"✅ Configuration chargée depuis {config_path}")
        except Exception as e:
            logger.warning(f"⚠️ Impossible de charger {config_path}, utilisation de la config par défaut: {e}")
            self.config = load_config("config/config.yml")
        
        # Initialiser l'extracteur Centris
        self.extractor = CentrisExtractor(
            config=self.config.centris
        )
        logger.debug("✅ CentrisExtractor initialisé")
        
        # Initialiser le service de base de données
        self.db_service = DatabaseService(self.config.database)
        await self.db_service.connect()
        logger.debug("✅ DatabaseService initialisé et connecté")
        
        # Initialiser le validateur
        self.validator = CentrisDataValidator()
        
        logger.info("✅ Configuration terminée")
        
    async def create_search_query(self):
        """Créer la requête de recherche pour Trois-Rivières"""
        logger.info("🔍 Création de la requête de recherche Trois-Rivières")
        
        # Configuration Trois-Rivières
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
        
        logger.info(f"📍 Recherche configurée: Trois-Rivières - Plex")
        logger.info(f"💰 Fourchette de prix: {min_price:,.0f}$ - {max_price:,.0f}$")
        
        return {
            'location': location,
            'property_types': property_types,
            'min_price': min_price,
            'max_price': max_price
        }
        
    async def extract_properties(self, search_query):
        """Extraire les résumés de propriétés selon les critères"""
        logger.info("🏠 Début de l'extraction des propriétés")
        
        try:
            # Créer l'objet SearchQuery
            from src.models.property import SearchQuery
            
            search_query_obj = SearchQuery(
                locations=[search_query['location']],
                property_types=search_query['property_types'],
                min_price=search_query['min_price'],
                max_price=search_query['max_price']
            )
            
            # Extraire les résumés
            summaries = await self.extractor.extract_summaries(search_query_obj)
            
            logger.info(f"📊 {len(summaries)} résumés de propriétés extraits")
            
            # Filtrer les propriétés à Trois-Rivières
            trois_rivieres_properties = []
            for summary in summaries:
                if self._is_trois_rivieres_property(summary):
                    trois_rivieres_properties.append(summary)
                    logger.info(f"🏠 Propriété Trois-Rivières trouvée: {summary.address.street}{summary.address.city}, {summary.address.street}")
            
            logger.info(f"🎯 {len(trois_rivieres_properties)} propriétés confirmées à Trois-Rivières")
            
            return trois_rivieres_properties
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction: {e}")
            return []
            
    async def extract_property_details(self, summaries):
        """Extraire les détails des propriétés à partir des résumés"""
        logger.info("🔍 Extraction des détails des propriétés")
        detailed_properties = []
        
        for i, summary in enumerate(summaries):
            logger.info(f"🔍 Extraction détaillée {i+1}/{len(summaries)}: {summary.id}")
            
            try:
                # Construire l'URL complète
                property_url = f"https://www.centris.ca/fr/propriete/{summary.id}"
                
                # Extraire les détails
                property_details = await self.extractor.extract_details(property_url)
                
                if property_details:
                    detailed_properties.append(property_details)
                    logger.info(f"✅ Détails extraits pour {summary.address.street}")
                else:
                    logger.warning(f"⚠️ Aucun détail extrait pour {summary.id}")
                    
            except Exception as e:
                logger.error(f"❌ Erreur lors de l'extraction des détails: {e}")
                continue
                
        logger.info(f"📋 {len(detailed_properties)} propriétés détaillées extraites")
        return detailed_properties
            
    def _is_trois_rivieres_property(self, summary):
        """Vérifier si la propriété est à Trois-Rivières"""
        try:
            # Vérifier la ville dans l'adresse
            if summary.address and summary.address.city:
                return "trois-rivières" in summary.address.city.lower() or "trois-rivières" in summary.address.street.lower()
            return False
        except:
            return False
            
    async def save_to_database(self, properties):
        """Sauvegarder les propriétés en base"""
        if not properties:
            logger.warning("⚠️ Aucune propriété à sauvegarder")
            return None
            
        try:
            # Créer un nom de collection unique avec timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            collection_name = f"trois_rivieres_plex_test_{timestamp}"
            
            logger.info(f"💾 Sauvegarde de {len(properties)} propriétés dans {collection_name}")
            logger.info(f"🔒 Utilisation de collection temporaire (évite properties_2024)")
            
            # Forcer l'utilisation de la collection temporaire
            self.db_service.set_collection_names({
                'properties': collection_name,
                'summaries': f"trois_rivieres_summaries_{timestamp}",
                'logs': f"trois_rivieres_logs_{timestamp}"
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
                    logger.info(f"💾 Propriété sauvegardée: {prop.address.street}")
                except Exception as e:
                    logger.error(f"❌ Erreur lors de la sauvegarde de {prop.id}: {e}")
                    
            logger.info(f"✅ {saved_count}/{len(properties)} propriétés sauvegardées avec succès")
            return collection_name
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")
            return None
            
    async def validate_results(self, collection_name):
        """Valider les résultats extraits"""
        if not collection_name:
            logger.warning("⚠️ Aucune collection à valider")
            return {}
            
        logger.info(f"🔍 Validation des résultats dans {collection_name}")
        
        try:
            # Configurer la collection
            self.db_service.set_collection_names({
                'properties': collection_name
            })
            
            # Compter les propriétés
            total_properties = await self.db_service.count_properties()
            logger.info(f"📊 {total_properties} propriétés trouvées en base")
            
            # Récupérer quelques propriétés pour validation
            properties = await self.db_service.get_properties(limit=3)
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
        """Valider la qualité des données extraites"""
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
                p.type and "plex" in p.type.lower()
                for p in properties
            )
            results['types_corrects'] = types_correct
            
            # Validation des IDs
            ids_unique = len(set(p.id for p in properties)) == len(properties)
            results['ids_uniques'] = ids_unique
            
            # Validation de la localisation Trois-Rivières
            location_trois_rivieres = all(
                p.address and p.address.city and 
                ("trois-rivières" in p.address.city.lower() or "trois-rivières" in p.address.street.lower())
                for p in properties
            )
            results['localisation_trois_rivieres'] = location_trois_rivieres
            
            logger.info("📋 Résultats de validation:")
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
        """Exécute le test complet d'extraction."""
        logger.info("🚀 Démarrage du test d'extraction Trois-Rivières Plex")
        
        try:
            # Configuration
            await self.setup()
            
            # Création de la requête
            search_query = await self.create_search_query()
            
            # Extraction des propriétés
            summaries = await self.extract_properties(search_query)
            
            if not summaries:
                logger.warning("⚠️ Aucune propriété trouvée à Trois-Rivières")
                return
            
            # Extraction des détails
            detailed_properties = await self.extract_property_details(summaries)
            
            if not detailed_properties:
                logger.warning("⚠️ Aucun détail extrait")
                return
            
            # Sauvegarde en base
            collection_name = await self.save_to_database(detailed_properties)
            
            # Validation des résultats
            validation_results = await self.validate_results(collection_name)
            
            # Résumé du test
            logger.info("🎉 Test d'extraction Trois-Rivières terminé avec succès!")
            logger.info(f"📊 Résumé:")
            logger.info(f"   🏠 Résumés extraits: {len(summaries)}")
            logger.info(f"   🔍 Détails extraits: {len(detailed_properties)}")
            logger.info(f"   💾 Collection créée: {collection_name}")
            logger.info(f"   ✅ Validation: {sum(validation_results.values())}/{len(validation_results)} critères")
            
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


async def main():
    """Fonction principale du test."""
    logger.info("🧪 Test d'Extraction Réelle: Plex à Trois-Rivières")
    logger.info("=" * 60)
    
    # Créer et exécuter le test
    test = TroisRivieresPlexExtractionTest()
    results = await test.run_test()
    
    # Affichage des résultats
    if results["success"]:
        logger.info("🎉 Test réussi!")
        logger.info(f"📊 Résultats: {results}")
    else:
        logger.error("❌ Test échoué!")
        logger.error(f"🚨 Erreur: {results.get('error', 'Erreur inconnue')}")
    
    return results


if __name__ == "__main__":
    # Exécution du test
    results = asyncio.run(main())
    
    # Code de sortie approprié
    sys.exit(0 if results.get("success", False) else 1)
