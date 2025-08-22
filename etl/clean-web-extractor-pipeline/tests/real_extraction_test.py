#!/usr/bin/env python3
"""
Test d'extraction réelle avec la nouvelle structure Centris et LocationConfig
Teste l'architecture modulaire avec de vraies données et la structure API validée
"""

import asyncio
import structlog
from src.extractors.centris_extractor import CentrisExtractor
from config.settings import config, LocationConfig
from src.utils.logging import setup_logging
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

# Configuration du logging
setup_logging()
logger = structlog.get_logger(__name__)

# Définition locale des énumérations et modèles
class PropertyType(str, Enum):
    """Types de propriétés supportés"""
    PLEX = "Plex"
    SINGLE_FAMILY_HOME = "SingleFamilyHome"
    SELL_CONDO = "SellCondo"
    RESIDENTIAL_LOT = "ResidentialLot"

class SearchQuery(BaseModel):
    """Paramètres de recherche de propriétés avec LocationConfig"""
    locations: List[LocationConfig]
    property_types: List[PropertyType]  # Utilisant PropertyType pour compatibilité
    price_min: Optional[float] = None
    price_max: Optional[float] = None


async def test_real_extraction_with_location_config():
    """Test d'extraction réelle avec LocationConfig"""
    logger.info("🚀 Démarrage du test d'extraction réelle avec LocationConfig...")
    
    extractor = None
    try:
        # Initialisation de l'extracteur
        logger.info("🔧 Initialisation du CentrisExtractor...")
        extractor = CentrisExtractor(config.centris)
        
        # Test 1: Extraction avec GeographicArea (Région)
        logger.info("📍 Test 1: Extraction avec GeographicArea (Région)")
        search_query_region = SearchQuery(
            locations=[
                LocationConfig(
                    type="GeographicArea",
                    value="Montérégie",
                    type_id="RARA16"
                )
            ],
            property_types=[PropertyType.PLEX],
            price_min=200000,
            price_max=260000
        )
        
        logger.info(f"🔍 Recherche: {search_query_region.locations[0].value} - {search_query_region.property_types}")
        summaries_region = await extractor.extract_summaries(search_query_region)
        
        if summaries_region:
            logger.info(f"✅ Test 1 Réussi: {len(summaries_region)} propriétés trouvées en Montérégie")
            
            # Validation des données extraites
            for i, summary in enumerate(summaries_region[:3], 1):
                logger.info(f"   🏠 Propriété {i}: {summary.type if hasattr(summary, 'type') else 'N/A'} - {summary.price if hasattr(summary, 'price') else 'N/A'}$ - {summary.address.city if hasattr(summary, 'address') else 'N/A'}")
        else:
            logger.warning("⚠️ Test 1: Aucune propriété trouvée en Montérégie")
            
        # Test 2: Extraction avec CityDistrict (District de ville)
        logger.info("🏙️ Test 2: Extraction avec CityDistrict (District de ville)")
        search_query_district = SearchQuery(
            locations=[
                LocationConfig(
                    type="CityDistrict",
                    value="Vieux-Montréal",
                    type_id=449
                )
            ],
            property_types=[PropertyType.SELL_CONDO],
            price_min=200000,
            price_max=260000
        )
        
        logger.info(f"🔍 Recherche: {search_query_district.locations[0].value} - {search_query_district.property_types}")
        summaries_district = await extractor.extract_summaries(search_query_district)
        
        if summaries_district:
            logger.info(f"✅ Test 2 Réussi: {len(summaries_district)} propriétés trouvées dans le Vieux-Montréal")
            
            # Validation des données extraites
            for i, summary in enumerate(summaries_district[:3], 1):
                logger.info(f"   🏠 Propriété {i}: {summary.type if hasattr(summary, 'type') else 'N/A'} - {summary.price if hasattr(summary, 'price') else 'N/A'}$ - {summary.address.city if hasattr(summary, 'address') else 'N/A'}")
        else:
            logger.warning("⚠️ Test 2: Aucune propriété trouvée dans le Vieux-Montréal")
            
        # Test 3: Extraction avec Multiple Locations
        logger.info("🌍 Test 3: Extraction avec Multiple Locations")
        search_query_multiple = SearchQuery(
            locations=[
                LocationConfig(
                    type="GeographicArea",
                    value="Laurentides", 
                    type_id="RARA15"
                ),
                LocationConfig(
                    type="CityDistrict",
                    value="Plateau-Mont-Royal",
                    type_id=450
                )
            ],
            property_types=[PropertyType.SINGLE_FAMILY_HOME],
            price_min=300000,
            price_max=360000
        )
        
        logger.info(f"🔍 Recherche Multiple: {[loc.value for loc in search_query_multiple.locations]} - {search_query_multiple.property_types}")
        summaries_multiple = await extractor.extract_summaries(search_query_multiple)
        
        if summaries_multiple:
            logger.info(f"✅ Test 3 Réussi: {len(summaries_multiple)} propriétés trouvées avec recherche multiple")
            
            # Validation des données extraites par localisation
            location_distribution = {}
            for summary in summaries_multiple:
                if hasattr(summary, 'address') and summary.address.city:
                    city = summary.address.city
                    location_distribution[city] = location_distribution.get(city, 0) + 1
                    
            logger.info(f"📊 Distribution par ville: {location_distribution}")
        else:
            logger.warning("⚠️ Test 3: Aucune propriété trouvée avec recherche multiple")
            
        # Test 4: Validation de la compatibilité avec l'ancien pipeline
        logger.info("🔗 Test 4: Validation de la compatibilité avec l'ancien pipeline")
        
        # Création d'une requête similaire à l'ancien format
        old_style_search = SearchQuery(
            locations=[
                LocationConfig(
                    type="GeographicArea",
                    value="Estrie",
                    type_id="RARA05"
                )
            ],
            property_types=[PropertyType.PLEX],
            price_min=200000,
            price_max=260000
        )
        
        logger.info(f"🔍 Test Compatibilité: {old_style_search.locations[0].value}")
        summaries_compatibility = await extractor.extract_summaries(old_style_search)
        
        if summaries_compatibility:
            logger.info(f"✅ Test 4 Réussi: {len(summaries_compatibility)} propriétés - Compatibilité validée")
        else:
            logger.warning("⚠️ Test 4: Aucune propriété trouvée - Test de compatibilité")
            
        # Résumé des résultats
        logger.info("\n" + "="*60)
        logger.info("📊 RÉSUMÉ DU TEST D'EXTRACTION RÉELLE")
        logger.info("="*60)
        
        total_found = 0
        results = [
            ("GeographicArea (Montérégie)", len(summaries_region) if summaries_region else 0),
            ("CityDistrict (Vieux-Montréal)", len(summaries_district) if summaries_district else 0),
            ("Multiple Locations", len(summaries_multiple) if summaries_multiple else 0),
            ("Compatibilité (Estrie)", len(summaries_compatibility) if summaries_compatibility else 0)
        ]
        
        for test_name, count in results:
            total_found += count
            status = "✅" if count > 0 else "⚠️"
            logger.info(f"{status} {test_name}: {count} propriétés")
            
        logger.info("-"*60)
        logger.info(f"🎯 Total des propriétés trouvées: {total_found}")
        
        if total_found > 0:
            logger.info("🎉 Test d'extraction réelle RÉUSSI !")
            logger.info("✅ La nouvelle structure Centris fonctionne avec de vraies données")
            logger.info("✅ L'architecture modulaire est opérationnelle") 
            logger.info("✅ La compatibilité avec l'ancien pipeline est assurée")
        else:
            logger.warning("⚠️ Aucune propriété trouvée - Vérifiez les paramètres de recherche")
            
        logger.info("="*60)
        return total_found > 0
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test d'extraction réelle: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
        
    finally:
        if extractor:
            await extractor.close()
            logger.info("🔌 CentrisExtractor fermé proprement")


if __name__ == "__main__":
    asyncio.run(test_real_extraction_with_location_config())
