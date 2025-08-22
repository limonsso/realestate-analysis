#!/usr/bin/env python3
"""
🧪 Test Réel : Extraction Plex à Chambly

Ce test effectue une extraction réelle de données de plex à Chambly depuis Centris.ca
et stocke les résultats dans MongoDB pour validation.
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Ajouter le répertoire racine au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.extractors.centris_extractor import CentrisExtractor
from src.models.property import SearchQuery, PropertyType
from src.utils.validators import TypeCategoryValidator
from config.settings import LocationConfig
from config.settings import load_config
from src.services.database_service import DatabaseService
import structlog

# Configuration du logging
logger = structlog.get_logger()

class ChamblyPlexExtractionTest:
    """Test d'extraction réelle de plex à Chambly."""
    
    def __init__(self):
        """Initialise le test avec la configuration."""
        self.config = load_config("config/config.yml")
        self.extractor = None
        self.db_service = None
        
    async def setup(self):
        """Configure l'extracteur et la base de données."""
        logger.info("🔧 Configuration du test d'extraction Chambly")
        
        # Initialiser l'extracteur Centris
        self.extractor = CentrisExtractor(self.config.centris)
        
        # Initialiser le service de base de données
        self.db_service = DatabaseService(self.config.database)
        await self.db_service.connect()
        
        logger.info("✅ Configuration terminée")
    
    async def create_search_query(self) -> SearchQuery:
        """Crée une requête de recherche pour Chambly."""
        logger.info("🔍 Création de la requête de recherche Chambly")
        
        # Configuration spécifique pour Chambly
        # Utilisation du CityDistrict spécifique à Chambly pour une recherche précise
        chambly_location = LocationConfig(
            type="CityDistrict",
            value="Chambly",  # Chambly spécifiquement avec son ID exact
            type_id=730
        )
        
        search_query = SearchQuery(
            locations=[chambly_location],
            property_types=[PropertyType.PLEX],
            price_min=100000,    # Prix minimum plus bas pour capturer plus de propriétés
            price_max=1000000    # Prix maximum plus haut pour capturer plus de propriétés
        )
        
        logger.info(f"📍 Recherche configurée: {chambly_location.value} - Plex")
        logger.info(f"💰 Fourchette de prix: {search_query.price_min:,}$ - {search_query.price_max:,}$")
        
        return search_query
    
    async def extract_properties(self, search_query: SearchQuery) -> List:
        """Extrait les propriétés selon la requête de recherche."""
        logger.info("🏠 Début de l'extraction des propriétés")
        
        try:
            # Extraction des résumés
            summaries = await self.extractor.extract_summaries(search_query)
            logger.info(f"📊 {len(summaries)} résumés de propriétés extraits")
            
            # Filtrer pour Chambly spécifiquement
            chambly_properties = []
            for summary in summaries:
                if self._is_chambly_property(summary):
                    chambly_properties.append(summary)
                    logger.info(f"🏠 Propriété Chambly trouvée: {summary.address.street}, {summary.address.city}")
            
            logger.info(f"🎯 {len(chambly_properties)} propriétés confirmées à Chambly")
            
            return chambly_properties
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction: {e}")
            raise
    
    def _is_chambly_property(self, summary) -> bool:
        """Vérifie si une propriété est à Chambly."""
        if not summary.address:
            return False
        
        # Vérifier la ville
        city = summary.address.city.lower()
        return "chambly" in city or "chambly" in summary.address.street.lower()
    
    async def extract_property_details(self, summaries: List) -> List:
        """Extrait les détails complets des propriétés."""
        logger.info("🔍 Extraction des détails des propriétés")
        
        detailed_properties = []
        
        for i, summary in enumerate(summaries[:5]):  # Limiter à 5 pour le test
            try:
                logger.info(f"🔍 Extraction détaillée {i+1}/{min(len(summaries), 5)}: {summary.id}")
                
                # Construction de l'URL complète pour l'extraction des détails
                property_url = f"https://www.centris.ca/fr/propriete/{summary.id}"
                logger.debug(f"🔗 URL construite: {property_url}")
                
                # Extraction des détails
                details = await self.extractor.extract_details(property_url)
                
                if details:
                    detailed_properties.append(details)
                    logger.info(f"✅ Détails extraits pour {details.address.street}")
                else:
                    logger.warning(f"⚠️ Aucun détail trouvé pour {summary.id}")
                    
            except Exception as e:
                logger.error(f"❌ Erreur extraction détails {summary.id}: {e}")
                continue
        
        logger.info(f"📋 {len(detailed_properties)} propriétés détaillées extraites")
        return detailed_properties
    
    async def save_to_database(self, properties: List, collection_name: str = None):
        """Sauvegarde les propriétés en base de données."""
        if not properties:
            logger.warning("⚠️ Aucune propriété à sauvegarder")
            return
        
        # Utiliser une collection dédiée pour le test
        if collection_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            collection_name = f"chambly_plex_test_{timestamp}"
        
        logger.info(f"💾 Sauvegarde de {len(properties)} propriétés dans {collection_name}")
        
        try:
            # Créer la collection de test
            await self.db_service.create_collection(collection_name)
            
            # Sauvegarder les propriétés
            saved_count = 0
            for property_data in properties:
                try:
                    # Mettre à jour les métadonnées de test
                    property_data.metadata.source = "Centris_Chambly_Test"
                    property_data.metadata.last_updated = datetime.now()
                    
                    # Sauvegarder en base
                    await self.db_service.save_property(property_data, collection_name)
                    saved_count += 1
                    
                    logger.info(f"💾 Propriété sauvegardée: {property_data.address.street}")
                    
                except Exception as e:
                    logger.error(f"❌ Erreur sauvegarde propriété: {e}")
                    continue
            
            logger.info(f"✅ {saved_count}/{len(properties)} propriétés sauvegardées avec succès")
            
            # Retourner le nom de la collection pour référence
            return collection_name
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde: {e}")
            raise
    
    async def validate_results(self, collection_name: str):
        """Valide les résultats sauvegardés en base."""
        logger.info(f"🔍 Validation des résultats dans {collection_name}")
        
        try:
            # Compter les propriétés sauvegardées
            count = await self.db_service.count_properties(collection_name)
            logger.info(f"📊 {count} propriétés trouvées en base")
            
            # Récupérer quelques exemples pour validation
            sample_properties = await self.db_service.get_properties(collection_name, limit=3)
            
            for i, prop in enumerate(sample_properties):
                logger.info(f"🏠 Exemple {i+1}:")
                logger.info(f"   📍 Adresse: {prop.address.street}, {prop.address.city}")
                logger.info(f"   💰 Prix: {prop.financial.price:,}$" if prop.financial else "   💰 Prix: Non spécifié")
                logger.info(f"   🏠 Type: {prop.type}")
                logger.info(f"   🆔 ID: {prop.id}")
            
            # Validation des données
            validation_results = await self._validate_data_quality(sample_properties)
            
            logger.info("📋 Résultats de validation:")
            for field, result in validation_results.items():
                status = "✅" if result else "❌"
                logger.info(f"   {status} {field}: {result}")
            
            return validation_results
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la validation: {e}")
            return {}
    
    async def _validate_data_quality(self, properties: List) -> dict:
        """Valide la qualité des données extraites."""
        if not properties:
            return {"données": False}
        
        validation = {
            "adresses_complètes": all(p.address and p.address.street and p.address.city for p in properties),
            "prix_valides": all(p.financial and p.financial.price > 0 for p in properties if p.financial),
            "types_corrects": all(TypeCategoryValidator.validate_type_category_consistency(p) for p in properties),
            "ids_uniques": len(set(p.id for p in properties)) == len(properties),
            "localisation_chambly": all("chambly" in p.address.city.lower() for p in properties if p.address and p.address.city)
        }
        
        return validation
    

    async def cleanup(self):
        """Nettoie les ressources."""
        logger.info("🧹 Nettoyage des ressources")
        
        try:
            if hasattr(self, 'extractor') and self.extractor:
                await self.extractor.close()
                logger.debug("✅ CentrisExtractor fermé")
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de la fermeture de l'extracteur: {e}")
        
        try:
            if hasattr(self, 'db_service') and self.db_service:
                await self.db_service.close()
                logger.debug("✅ DatabaseService fermé")
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de la fermeture de la base de données: {e}")
        
        logger.info("✅ Nettoyage terminé")
    
    async def run_test(self):
        """Exécute le test complet d'extraction."""
        logger.info("🚀 Démarrage du test d'extraction Chambly Plex")
        
        try:
            # Configuration
            await self.setup()
            
            # Création de la requête
            search_query = await self.create_search_query()
            
            # Extraction des propriétés
            summaries = await self.extract_properties(search_query)
            
            if not summaries:
                logger.warning("⚠️ Aucune propriété trouvée à Chambly")
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
            logger.info("🎉 Test d'extraction Chambly terminé avec succès!")
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
    logger.info("🧪 Test d'Extraction Réelle: Plex à Chambly")
    logger.info("=" * 60)
    
    # Créer et exécuter le test
    test = ChamblyPlexExtractionTest()
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
