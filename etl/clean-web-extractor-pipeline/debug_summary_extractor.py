#!/usr/bin/env python3
"""
Script de débogage pour SummaryExtractor
Analyse le HTML récupéré et identifie pourquoi aucune propriété n'est trouvée
"""

import asyncio
import structlog
from src.extractors.centris_extractor import CentrisExtractor
from config.settings import config, LocationConfig
from src.utils.logging import setup_logging
from pydantic import BaseModel
from typing import List
from enum import Enum

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

async def debug_summary_extractor():
    """Débogage du SummaryExtractor"""
    logger.info("🔍 Démarrage du débogage du SummaryExtractor...")
    
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
        pages = await extractor.search_manager.search_with_pagination(search_query, max_pages=2)
        logger.info(f"📄 Pages récupérées: {len(pages)}")
        
        for i, page_data in enumerate(pages):
            logger.info(f"📄 Page {i+1}: {len(page_data)} caractères")
        
        if not pages:
            logger.error("❌ Aucune page récupérée")
            return
            
        # Analyse de la première page
        first_page = pages[0]
        logger.info(f"\n🔍 ANALYSE DE LA PREMIÈRE PAGE ({len(first_page)} caractères)")
        logger.info("="*60)
        
        # Recherche d'indicateurs de propriétés
        property_indicators = [
            "property-card",
            "property-item", 
            "listing-item",
            "search-result",
            "property-result",
            "centris-property",
            "property-listing"
        ]
        
        found_indicators = []
        for indicator in property_indicators:
            if indicator in first_page.lower():
                found_indicators.append(indicator)
                count = first_page.lower().count(indicator)
                logger.info(f"✅ Trouvé '{indicator}': {count} occurrences")
        
        if not found_indicators:
            logger.warning("⚠️ Aucun indicateur de propriété trouvé")
            
            # Recherche d'autres patterns
            other_patterns = [
                "price",
                "address", 
                "bedroom",
                "bathroom",
                "sqft",
                "m²",
                "pi²"
            ]
            
            for pattern in other_patterns:
                if pattern in first_page.lower():
                    count = first_page.lower().count(pattern)
                    logger.info(f"🔍 Pattern '{pattern}': {count} occurrences")
        
        # Extraire un extrait du HTML pour analyse
        logger.info(f"\n📋 EXTRACTS DU HTML")
        logger.info("="*60)
        
        # Chercher des sections qui pourraient contenir des propriétés
        html_sections = [
            first_page[:1000],  # Début
            first_page[len(first_page)//2-500:len(first_page)//2+500],  # Milieu
            first_page[-1000:]  # Fin
        ]
        
        for i, section in enumerate(html_sections):
            logger.info(f"\n📍 Section {i+1} ({len(section)} caractères):")
            logger.info("-" * 40)
            
            # Nettoyer et afficher le HTML
            clean_html = section.replace('\n', ' ').replace('\r', ' ').strip()
            if len(clean_html) > 200:
                logger.info(f"HTML: {clean_html[:200]}...")
            else:
                logger.info(f"HTML: {clean_html}")
        
        # Test direct du SummaryExtractor
        logger.info(f"\n🧪 TEST DIRECT DU SUMMARYEXTRACTOR")
        logger.info("="*60)
        
        try:
            summaries = await extractor.extract_summaries(search_query)
            if summaries:
                logger.info(f"✅ SummaryExtractor a trouvé {len(summaries)} propriétés")
                for i, summary in enumerate(summaries[:3]):
                    logger.info(f"   🏠 Propriété {i+1}: {summary.id} - {summary.price}$")
            else:
                logger.warning("⚠️ SummaryExtractor n'a trouvé aucune propriété")
                
                # Vérifier les logs du SummaryExtractor
                logger.info("🔍 Vérification des logs du SummaryExtractor...")
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        # Résumé du débogage
        logger.info(f"\n📊 RÉSUMÉ DU DÉBOGAGE")
        logger.info("="*60)
        logger.info(f"📄 Pages récupérées: {len(pages)}")
        logger.info(f"🔍 Indicateurs trouvés: {found_indicators}")
        logger.info(f"📏 Taille totale HTML: {sum(len(p) for p in pages)} caractères")
        
        if found_indicators:
            logger.info("✅ Le HTML contient des indicateurs de propriétés")
            logger.info("🔧 Le problème est probablement dans le parsing")
        else:
            logger.warning("⚠️ Le HTML ne semble pas contenir de propriétés")
            logger.info("🔧 Vérifiez la structure de l'API Centris")
            
    except Exception as e:
        logger.error(f"❌ Erreur lors du débogage: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
    finally:
        if extractor:
            await extractor.close()
            logger.info("🔌 CentrisExtractor fermé")

if __name__ == "__main__":
    asyncio.run(debug_summary_extractor())
