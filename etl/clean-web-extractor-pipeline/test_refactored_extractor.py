#!/usr/bin/env python3
"""
Test simple du DetailExtractor refactorisé
"""

import asyncio
import structlog
from bs4 import BeautifulSoup

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

async def test_refactored_extractor():
    """Test du DetailExtractor refactorisé"""
    try:
        logger.info("🧪 Début du test du DetailExtractor refactorisé")
        
        # Import du DetailExtractor refactorisé
        from src.extractors.centris.detail_extractor_refactored import CentrisDetailExtractor
        
        # Création d'une instance
        extractor = CentrisDetailExtractor()
        logger.info("✅ DetailExtractor refactorisé créé avec succès")
        
        # Vérification des extracteurs spécialisés
        logger.info(f"📍 AddressExtractor: {type(extractor.address_extractor)}")
        logger.info(f"💰 FinancialExtractor: {type(extractor.financial_extractor)}")
        logger.info(f"🔢 NumericExtractor: {type(extractor.numeric_extractor)}")
        
        # Test avec un HTML simple
        test_html = """
        <html>
            <head>
                <title>Triplex à vendre - Chambly</title>
                <link rel="canonical" href="https://www.centris.ca/fr/propriete/12345678" />
            </head>
            <body>
                <div class="carac-container">
                    <div class="carac-title">Utilisation de la propriété</div>
                    <div class="carac-value"><span>Résidentielle</span></div>
                </div>
                <div class="carac-container">
                    <div class="carac-title">Style de bâtiment</div>
                    <div class="carac-value"><span>Jumelé</span></div>
                </div>
                <div class="carac-container">
                    <div class="carac-title">Année de construction</div>
                    <div class="carac-value"><span>1976</span></div>
                </div>
                <div class="carac-container">
                    <div class="carac-title">Superficie du terrain</div>
                    <div class="carac-value"><span>5 654 pc</span></div>
                </div>
                <div class="walkscore">
                    <a onclick="OpenWalkScore(this);" title="La plupart des services à distance de marche">
                        <span>71</span>
                    </a>
                </div>
            </body>
        </html>
        """
        
        soup = BeautifulSoup(test_html, 'html.parser')
        
        # Test des extracteurs spécialisés
        logger.info("🧪 Test des extracteurs spécialisés...")
        
        # Test AddressExtractor
        address_data = extractor.address_extractor.extract_address(soup)
        logger.info(f"📍 Adresse extraite: {address_data}")
        
        # Test FinancialExtractor
        financial_data = extractor.financial_extractor.extract_financial(soup)
        logger.info(f"💰 Données financières: {financial_data}")
        
        # Test NumericExtractor
        numeric_values = extractor.numeric_extractor.extract_numeric_values(soup)
        logger.info(f"🔢 Valeurs numériques: {numeric_values}")
        
        detailed_features = extractor.numeric_extractor.extract_detailed_features(soup)
        logger.info(f"🔍 Caractéristiques détaillées: {detailed_features}")
        
        # Test de l'extraction complète
        logger.info("🧪 Test de l'extraction complète...")
        property_data = await extractor.extract_property_details(soup, "https://test.com")
        
        if property_data:
            logger.info(f"✅ Propriété extraite avec succès: {property_data.id}")
            logger.info(f"🏷️ Type: {property_data.type}")
            logger.info(f"🏠 Catégorie: {property_data.category}")
            logger.info(f"📍 Adresse: {property_data.address.street if property_data.address else 'N/A'}")
        else:
            logger.warning("⚠️ Aucune propriété extraite")
        
        logger.info("🎉 Test terminé avec succès !")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_refactored_extractor())
