#!/usr/bin/env python3
"""
Test simplifié du nouveau DetailExtractor refactorisé
"""

import asyncio
import time
import structlog
from bs4 import BeautifulSoup

# Configuration du logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
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

async def test_new_extractor_only():
    """Test uniquement du nouveau DetailExtractor refactorisé"""
    try:
        logger.info("🧪 Test du nouveau DetailExtractor refactorisé")
        
        # HTML de test
        test_html = """
        <html>
            <head>
                <title>Triplex à vendre - Chambly</title>
                <link rel="canonical" href="https://www.centris.ca/fr/propriete/21002530" />
            </head>
            <body>
                <div class="row">
                    <div class="col-lg-3 col-sm-6 carac-container">
                        <div class="carac-title">Utilisation de la propriété</div>
                        <div class="carac-value"><span>Résidentielle</span></div>
                    </div>
                    <div class="col-lg-3 col-sm-6 carac-container">
                        <div class="carac-title">Style de bâtiment</div>
                        <div class="carac-value"><span>Jumelé</span></div>
                    </div>
                    <div class="col-lg-3 col-sm-6 carac-container">
                        <div class="carac-title">Année de construction</div>
                        <div class="carac-value"><span>1989</span></div>
                    </div>
                    <div class="col-lg-3 col-sm-6 carac-container">
                        <div class="carac-title">Superficie du terrain</div>
                        <div class="carac-value"><span>4 755 pc</span></div>
                    </div>
                    <div class="col-lg-3 col-sm-6 carac-container">
                        <div class="carac-title">Stationnement total</div>
                        <div class="carac-value"><span>Allée (3), Garage (1)</span></div>
                    </div>
                    <div class="col-lg-3 col-sm-6 carac-container">
                        <div class="carac-title">Nombre d'unités</div>
                        <div class="carac-value"><span data-id="NbUniteFormatted">Résidentiel (3)</span></div>
                    </div>
                    <div class="col-lg-3 col-sm-6 carac-container">
                        <div class="carac-title">Unités résidentielles</div>
                        <div class="carac-value"><span data-id="NbUniteFormatted">1 x 4 ½, 2 x 5 ½</span></div>
                    </div>
                    <div class="col-lg-3 col-sm-6 carac-container">
                        <div class="carac-title">Unité principale</div>
                        <div class="carac-value"><span data-id="NbUniteFormatted">5 pièces, 3 chambres, 1 salle de bain</span></div>
                    </div>
                    <div class="col-lg-3 col-sm-6 carac-container">
                        <div class="carac-title">Revenus bruts potentiels</div>
                        <div class="carac-value"><span>36&nbsp;960 $</span></div>
                    </div>
                    <div class="col-lg-3 col-sm-6 carac-container">
                        <div class="carac-title">Date d'emménagement</div>
                        <div class="carac-value"><span>Selon les baux</span></div>
                    </div>
                    <div class="col-lg-3 col-sm-6 carac-container">
                        <div class="walkscore">
                            <a onclick="OpenWalkScore(this);" title="La plupart des services à distance de marche">
                                <span>65</span>
                            </a>
                        </div>
                    </div>
                </div>
                <script>
                    var lat = 45.441214;
                    var lng = -73.296067;
                </script>
            </body>
        </html>
        """
        
        soup = BeautifulSoup(test_html, 'html.parser')
        test_url = "https://test.com"
        
        # Test du nouveau DetailExtractor refactorisé
        logger.info("🔄 Test du nouveau DetailExtractor refactorisé...")
        try:
            from src.extractors.centris.detail_extractor_refactored import CentrisDetailExtractor
            
            new_extractor = CentrisDetailExtractor()
            
            start_time = time.time()
            new_result = await new_extractor.extract_property_details(soup, test_url)
            new_execution_time = time.time() - start_time
            
            logger.info(f"⏱️ Nouveau DetailExtractor: {new_execution_time:.4f} secondes")
            
            if new_result:
                logger.info(f"✅ Propriété extraite avec succès: {new_result.id}")
                logger.info(f"🏷️ Type: {new_result.type}")
                logger.info(f"🏠 Catégorie: {new_result.category}")
                logger.info(f"📍 Adresse: {new_result.address.street if new_result.address else 'N/A'}")
                
                # Validation des champs extraits
                logger.info("🔍 Validation des champs extraits...")
                
                # Vérification des nouvelles informations détaillées
                if new_result.property_usage:
                    logger.info(f"🏠 Utilisation: {new_result.property_usage}")
                if new_result.building_style:
                    logger.info(f"🏗️ Style: {new_result.building_style}")
                if new_result.parking_info:
                    logger.info(f"🚗 Stationnement: {new_result.parking_info}")
                if new_result.units_info:
                    logger.info(f"🏘️ Unités: {new_result.units_info}")
                if new_result.main_unit_info:
                    logger.info(f"🏠 Unité principale: {new_result.main_unit_info}")
                if new_result.move_in_date:
                    logger.info(f"📅 Date d'emménagement: {new_result.move_in_date}")
                if new_result.walk_score:
                    logger.info(f"🚶 Walk Score: {new_result.walk_score}")
                
                logger.info("✅ Tous les champs ont été extraits avec succès !")
                
            else:
                logger.warning("⚠️ Aucune propriété extraite")
            
        except Exception as e:
            logger.error(f"❌ Erreur avec le nouveau DetailExtractor: {e}")
            import traceback
            traceback.print_exc()
        
        # Test des extracteurs spécialisés individuellement
        logger.info("🧪 Test des extracteurs spécialisés individuellement...")
        
        try:
            from src.extractors.centris.extractors import AddressExtractor, FinancialExtractor, NumericExtractor
            
            # Test AddressExtractor
            start_time = time.time()
            address_extractor = AddressExtractor()
            address_data = address_extractor.extract_address(soup)
            address_time = time.time() - start_time
            logger.info(f"📍 AddressExtractor: {address_time:.4f}s - {len(address_data)} champs")
            logger.info(f"📍 Données: {address_data}")
            
            # Test FinancialExtractor
            start_time = time.time()
            financial_extractor = FinancialExtractor()
            financial_data = financial_extractor.extract_financial(soup)
            financial_time = time.time() - start_time
            logger.info(f"💰 FinancialExtractor: {financial_time:.4f}s - {len(financial_data)} champs")
            logger.info(f"💰 Données: {financial_data}")
            
            # Test NumericExtractor
            start_time = time.time()
            numeric_extractor = NumericExtractor()
            numeric_values = numeric_extractor.extract_numeric_values(soup)
            detailed_features = numeric_extractor.extract_detailed_features(soup)
            numeric_time = time.time() - start_time
            logger.info(f"🔢 NumericExtractor: {numeric_time:.4f}s - {len(numeric_values)} valeurs + {len(detailed_features)} détails")
            logger.info(f"🔢 Valeurs numériques: {numeric_values}")
            logger.info(f"🔍 Caractéristiques détaillées: {detailed_features}")
            
            total_specialized_time = address_time + financial_time + numeric_time
            logger.info(f"⏱️ Temps total extracteurs spécialisés: {total_specialized_time:.4f}s")
            
        except Exception as e:
            logger.error(f"❌ Erreur avec les extracteurs spécialisés: {e}")
            import traceback
            traceback.print_exc()
        
        logger.info("🎉 Test terminé avec succès !")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_new_extractor_only())
