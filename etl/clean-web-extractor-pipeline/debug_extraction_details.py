#!/usr/bin/env python3
"""
Script de débogage détaillé pour SummaryExtractor
Analyse chaque étape de l'extraction des propriétés
"""

import asyncio
import structlog
from src.extractors.centris_extractor import CentrisExtractor
from config.settings import config, LocationConfig
from src.utils.logging import setup_logging
from pydantic import BaseModel
from typing import List
from enum import Enum
from bs4 import BeautifulSoup

# Configuration du logging
setup_logging()
logger = structlog.get_logger(__name__)

# Définition locale des modèles
class PropertyType(str, Enum):
    PLEX = "Plex"
    SINGLE_FAMILY_HOME = "SingleFamilyHome"
    SELL_CONDO = "SellCondo"

class SearchQuery(BaseModel):
    locations: List[LocationConfig]
    property_types: List[PropertyType]
    price_min: float = 200000
    price_max: float = 260000

async def debug_extraction_details():
    """Débogage détaillé de l'extraction"""
    logger.info("🔍 Démarrage du débogage détaillé de l'extraction...")
    
    extractor = None
    try:
        # Initialisation
        extractor = CentrisExtractor(config.centris)
        
        # Test avec une recherche simple
        search_query = SearchQuery(
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
        
        logger.info(f"🔍 Test de recherche: {search_query.locations[0].value}")
        
        # Récupération des pages HTML
        pages = await extractor.search_manager.search_with_pagination(search_query, max_pages=1)
        
        if not pages:
            logger.error("❌ Aucune page récupérée")
            return
            
        first_page = pages[0]
        logger.info(f"📄 Page analysée: {len(first_page)} caractères")
        
        # Test direct du parsing HTML
        logger.info(f"\n🧪 TEST DIRECT DU PARSING HTML")
        logger.info("="*60)
        
        soup = BeautifulSoup(first_page, 'html.parser')
        
        # Recherche des conteneurs de propriétés
        property_containers = soup.find_all('div', class_='property-thumbnail-item')
        logger.info(f"🔍 Conteneurs trouvés: {len(property_containers)}")
        
        if not property_containers:
            # Essayer d'autres sélecteurs
            property_containers = soup.find_all('div', class_='thumbnailItem')
            logger.info(f"🔍 Conteneurs thumbnailItem: {len(property_containers)}")
            
        if not property_containers:
            property_containers = soup.find_all('div', attrs={'itemscope': True, 'itemtype': 'http://schema.org/Product'})
            logger.info(f"🔍 Conteneurs schema.org: {len(property_containers)}")
        
        if not property_containers:
            logger.error("❌ Aucun conteneur de propriété trouvé")
            return
            
        # Analyser le premier conteneur en détail
        first_container = property_containers[0]
        logger.info(f"\n🔍 ANALYSE DU PREMIER CONTENEUR")
        logger.info("="*60)
        
        # Afficher la structure HTML du conteneur
        logger.info(f"📋 Structure HTML du conteneur:")
        logger.info("-" * 40)
        container_html = str(first_container)[:1000]  # Limiter à 1000 caractères
        logger.info(container_html)
        
        # Test des méthodes d'extraction une par une
        logger.info(f"\n🧪 TEST DES MÉTHODES D'EXTRACTION")
        logger.info("="*60)
        
        # 1. Test extraction ID
        logger.info("🔑 Test extraction ID...")
        try:
            id_element = first_container.find('a', href=True)
            if id_element:
                href = id_element.get('href', '')
                logger.info(f"✅ Lien trouvé: {href}")
                if '/property/' in href:
                    property_id = href.split('/property/')[-1].split('/')[0]
                    logger.info(f"✅ ID extrait: {property_id}")
                else:
                    logger.warning(f"⚠️ Format de lien non reconnu: {href}")
            else:
                logger.warning("⚠️ Aucun lien trouvé")
                
            # Test des attributs data
            data_id = first_container.get('data-property-id') or first_container.get('data-id')
            if data_id:
                logger.info(f"✅ ID dans data: {data_id}")
            else:
                logger.warning("⚠️ Aucun ID dans les attributs data")
                
        except Exception as e:
            logger.error(f"❌ Erreur extraction ID: {e}")
        
        # 2. Test extraction adresse
        logger.info("\n📍 Test extraction adresse...")
        try:
            address_element = (
                first_container.find('div', {'class': 'location-container'}) or
                first_container.find('div', {'class': 'address'}) or
                first_container.find('span', {'class': 'address'})
            )
            
            if address_element:
                logger.info(f"✅ Élément adresse trouvé: {address_element.name}.{address_element.get('class', [])}")
                
                # Chercher le texte d'adresse
                address_text_element = address_element.find('div', {'class': 'address'})
                if address_text_element:
                    address_text = address_text_element.get_text(strip=True)
                    logger.info(f"✅ Texte adresse: '{address_text}'")
                else:
                    address_text = address_element.get_text(strip=True)
                    logger.info(f"✅ Texte adresse (conteneur): '{address_text}'")
            else:
                logger.warning("⚠️ Aucun élément adresse trouvé")
                
        except Exception as e:
            logger.error(f"❌ Erreur extraction adresse: {e}")
        
        # 3. Test extraction prix
        logger.info("\n💰 Test extraction prix...")
        try:
            price_element = (
                first_container.find('div', {'class': 'plex-revenue'}) or
                first_container.find('div', {'class': 'price'}) or
                first_container.find('span', {'class': 'price'})
            )
            
            if price_element:
                logger.info(f"✅ Élément prix trouvé: {price_element.name}.{price_element.get('class', [])}")
                price_text = price_element.get_text(strip=True)
                logger.info(f"✅ Texte prix: '{price_text}'")
                
                # Test du nettoyage du prix
                price_clean = ''.join(filter(str.isdigit, price_text))
                if price_clean:
                    logger.info(f"✅ Prix numérique extrait: {price_clean}")
                else:
                    logger.warning(f"⚠️ Impossible d'extraire le prix numérique de: '{price_text}'")
            else:
                logger.warning("⚠️ Aucun élément prix trouvé")
                
        except Exception as e:
            logger.error(f"❌ Erreur extraction prix: {e}")
        
        # 4. Test extraction type
        logger.info("\n🏠 Test extraction type...")
        try:
            type_element = (
                first_container.find('div', {'class': 'category'}) or
                first_container.find('span', {'class': 'property-type'}) or
                first_container.find('div', {'class': 'property-type'})
            )
            
            if type_element:
                logger.info(f"✅ Élément type trouvé: {type_element.name}.{type_element.get('class', [])}")
                type_text = type_element.get_text(strip=True)
                logger.info(f"✅ Texte type: '{type_text}'")
            else:
                logger.warning("⚠️ Aucun élément type trouvé")
                
        except Exception as e:
            logger.error(f"❌ Erreur extraction type: {e}")
        
        # Test complet de l'extraction
        logger.info(f"\n🧪 TEST COMPLET DE L'EXTRACTION")
        logger.info("="*60)
        
        try:
            summaries = await extractor.extract_summaries(search_query)
            if summaries:
                logger.info(f"✅ Extraction réussie: {len(summaries)} propriétés")
                for i, summary in enumerate(summaries[:3]):
                    logger.info(f"   🏠 Propriété {i+1}: {summary.id} - {summary.price}$ - {summary.address.street}")
            else:
                logger.warning("⚠️ Aucune propriété extraite")
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        # Résumé du débogage
        logger.info(f"\n📊 RÉSUMÉ DU DÉBOGAGE DÉTAILLÉ")
        logger.info("="*60)
        logger.info(f"📄 Page analysée: {len(first_page)} caractères")
        logger.info(f"🔍 Conteneurs trouvés: {len(property_containers)}")
        logger.info(f"📏 Premier conteneur: {len(str(first_container))} caractères")
        
        if len(property_containers) > 0:
            logger.info("✅ Les conteneurs de propriétés sont trouvés")
            logger.info("🔧 Le problème est dans l'extraction des données individuelles")
        else:
            logger.warning("⚠️ Aucun conteneur de propriété trouvé")
            
    except Exception as e:
        logger.error(f"❌ Erreur lors du débogage détaillé: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
    finally:
        if extractor:
            await extractor.close()
            logger.info("🔌 CentrisExtractor fermé")

if __name__ == "__main__":
    asyncio.run(debug_extraction_details())
