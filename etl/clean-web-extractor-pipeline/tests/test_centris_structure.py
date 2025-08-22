#!/usr/bin/env python3
"""
Test de validation de la structure Centris avec les vrais IDs
Valide que notre SearchManager génère la bonne structure d'API
"""

import asyncio
import structlog
from src.extractors.centris.search_manager import CentrisSearchManager
from src.extractors.centris.session_manager import CentrisSessionManager
from src.models.property import PropertyType
from config.settings import config, LocationConfig
from src.utils.logging import setup_logging
from pydantic import BaseModel
from typing import List, Optional

# Définition locale de SearchQuery pour éviter les imports circulaires
class SearchQuery(BaseModel):
    """Paramètres de recherche de propriétés"""
    locations: List[LocationConfig]
    property_types: List[PropertyType]
    price_min: Optional[float] = None
    price_max: Optional[float] = None

# Configuration du logging
setup_logging()
logger = structlog.get_logger(__name__)


async def test_centris_structure():
    """Test de la structure Centris avec les vrais IDs"""
    logger.info("🔍 Test de validation de la structure Centris...")
    
    try:
        # Initialisation des composants
        session_manager = CentrisSessionManager(config.centris)
        search_manager = CentrisSearchManager(session_manager)
        
        # Test 1: GeographicArea (région)
        logger.info("📍 Test 1: GeographicArea (région)")
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
        
        request_region = search_manager._build_search_request(search_query_region)
        logger.info(f"✅ Requête région: {request_region}")
        
        # Validation de la structure
        assert 'query' in request_region, "Clé 'query' manquante"
        assert 'FieldsValues' in request_region['query'], "Clé 'FieldsValues' manquante"
        assert 'Filters' not in request_region['query'], "Clé 'Filters' ne devrait pas être présente"
        
        # Vérification des champs de localisation
        location_fields = [f for f in request_region['query']['FieldsValues'] if f['fieldId'] == 'GeographicArea']
        assert len(location_fields) == 1, f"Nombre de champs GeographicArea incorrect: {len(location_fields)}"
        assert location_fields[0]['value'] == 'RARA16', f"Valeur GeographicArea incorrecte: {location_fields[0]['value']}"
        
        # Test 2: CityDistrict (district de ville)
        logger.info("🏙️ Test 2: CityDistrict (district de ville)")
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
        
        request_district = search_manager._build_search_request(search_query_district)
        logger.info(f"✅ Requête district: {request_district}")
        
        # Validation de la structure
        location_fields = [f for f in request_district['query']['FieldsValues'] if f['fieldId'] == 'CityDistrict']
        assert len(location_fields) == 1, f"Nombre de champs CityDistrict incorrect: {len(location_fields)}"
        assert location_fields[0]['value'] == 449, f"Valeur CityDistrict incorrecte: {location_fields[0]['value']}"
        
        # Test 3: Multiple locations
        logger.info("🌍 Test 3: Multiple locations")
        search_query_multiple = SearchQuery(
            locations=[
                LocationConfig(
                    type="GeographicArea",
                    value="Montérégie",
                    type_id="RARA16"
                ),
                LocationConfig(
                    type="CityDistrict",
                    value="Vieux-Montréal",
                    type_id=449
                )
            ],
            property_types=[PropertyType.SINGLE_FAMILY_HOME],
            price_min=300000,
            price_max=360000
        )
        
        request_multiple = search_manager._build_search_request(search_query_multiple)
        logger.info(f"✅ Requête multiple: {request_multiple}")
        
        # Validation des champs multiples
        geographic_fields = [f for f in request_multiple['query']['FieldsValues'] if f['fieldId'] == 'GeographicArea']
        city_district_fields = [f for f in request_multiple['query']['FieldsValues'] if f['fieldId'] == 'CityDistrict']
        
        assert len(geographic_fields) == 1, f"Nombre de champs GeographicArea incorrect: {len(geographic_fields)}"
        assert len(city_district_fields) == 1, f"Nombre de champs CityDistrict incorrect: {len(city_district_fields)}"
        
        # Test 4: Validation de la structure complète
        logger.info("🔍 Test 4: Validation de la structure complète")
        
        # Vérification que tous les champs sont dans FieldsValues
        all_field_ids = [f['fieldId'] for f in request_multiple['query']['FieldsValues']]
        expected_field_ids = ['GeographicArea', 'CityDistrict', 'PropertyType', 'SalePrice', 'SalePrice']
        
        for expected_id in expected_field_ids:
            assert expected_id in all_field_ids, f"Champ manquant: {expected_id}"
            
        # Vérification des types de propriété
        property_type_fields = [f for f in request_multiple['query']['FieldsValues'] if f['fieldId'] == 'PropertyType']
        assert len(property_type_fields) == 1, f"Nombre de champs PropertyType incorrect: {len(property_type_fields)}"
        assert property_type_fields[0]['value'] == 'SingleFamilyHome', f"Valeur PropertyType incorrecte: {property_type_fields[0]['value']}"
        
        # Vérification des prix
        price_fields = [f for f in request_multiple['query']['FieldsValues'] if f['fieldId'] == 'SalePrice']
        assert len(price_fields) == 2, f"Nombre de champs SalePrice incorrect: {len(price_fields)}"
        
        prices = [f['value'] for f in price_fields]
        assert 300000 in prices, "Prix minimum manquant"
        assert 360000 in prices, "Prix maximum manquant"
        
        logger.info("🎉 Tous les tests de structure Centris ont réussi !")
        
        # Affichage de la structure finale
        logger.info("📋 Structure finale de la requête:")
        import json
        logger.info(json.dumps(request_multiple, indent=2))
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test de structure Centris: {e}")
        return False
        
    finally:
        if 'session_manager' in locals():
            await session_manager.close()


if __name__ == "__main__":
    asyncio.run(test_centris_structure())
