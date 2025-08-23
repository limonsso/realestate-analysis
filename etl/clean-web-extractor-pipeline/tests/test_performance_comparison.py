#!/usr/bin/env python3
"""
Test de comparaison des performances entre l'ancien et le nouveau DetailExtractor
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

async def test_performance_comparison():
    """Compare les performances entre l'ancien et le nouveau DetailExtractor"""
    try:
        logger.info("🧪 Début du test de comparaison des performances")
        
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
        
        # Test de l'ancien DetailExtractor
        logger.info("🔄 Test de l'ancien DetailExtractor...")
        try:
            from src.extractors.centris.detail_extractor import CentrisDetailExtractor as OldDetailExtractor
            
            old_extractor = OldDetailExtractor()
            
            start_time = time.time()
            old_result = await old_extractor.extract_property_details(soup, test_url)
            old_execution_time = time.time() - start_time
            
            logger.info(f"⏱️ Ancien DetailExtractor: {old_execution_time:.4f} secondes")
            logger.info(f"✅ Ancien: Propriété extraite: {old_result.id if old_result else 'None'}")
            
        except Exception as e:
            logger.error(f"❌ Erreur avec l'ancien DetailExtractor: {e}")
            old_execution_time = None
            old_result = None
        
        # Test du nouveau DetailExtractor refactorisé
        logger.info("🔄 Test du nouveau DetailExtractor refactorisé...")
        try:
            from src.extractors.centris.detail_extractor_refactored import CentrisDetailExtractor as NewDetailExtractor
            
            new_extractor = NewDetailExtractor()
            
            start_time = time.time()
            new_result = await new_extractor.extract_property_details(soup, test_url)
            new_execution_time = time.time() - start_time
            
            logger.info(f"⏱️ Nouveau DetailExtractor: {new_execution_time:.4f} secondes")
            logger.info(f"✅ Nouveau: Propriété extraite: {new_result.id if new_result else 'None'}")
            
        except Exception as e:
            logger.error(f"❌ Erreur avec le nouveau DetailExtractor: {e}")
            new_execution_time = None
            new_result = None
        
        # Comparaison des performances
        logger.info("📊 Comparaison des performances...")
        
        if old_execution_time and new_execution_time:
            if new_execution_time < old_execution_time:
                improvement = ((old_execution_time - new_execution_time) / old_execution_time) * 100
                logger.info(f"🚀 Amélioration: {improvement:.2f}% plus rapide")
            else:
                degradation = ((new_execution_time - old_execution_time) / old_execution_time) * 100
                logger.info(f"⚠️ Dégradation: {degradation:.2f}% plus lent")
        
        # Comparaison des résultats
        logger.info("🔍 Comparaison des résultats...")
        
        if old_result and new_result:
            logger.info("✅ Les deux extracteurs ont produit des résultats")
            
            # Comparaison des champs clés
            key_fields = ['id', 'type', 'category', 'status']
            for field in key_fields:
                old_value = getattr(old_result, field, None)
                new_value = getattr(new_result, field, None)
                
                if old_value == new_value:
                    logger.info(f"✅ {field}: Identique ({old_value})")
                else:
                    logger.warning(f"⚠️ {field}: Différent (Ancien: {old_value}, Nouveau: {new_value})")
        
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
            
            # Test FinancialExtractor
            start_time = time.time()
            financial_extractor = FinancialExtractor()
            financial_data = financial_extractor.extract_financial(soup)
            financial_time = time.time() - start_time
            logger.info(f"💰 FinancialExtractor: {financial_time:.4f}s - {len(financial_data)} champs")
            
            # Test NumericExtractor
            start_time = time.time()
            numeric_extractor = NumericExtractor()
            numeric_values = numeric_extractor.extract_numeric_values(soup)
            detailed_features = numeric_extractor.extract_detailed_features(soup)
            numeric_time = time.time() - start_time
            logger.info(f"🔢 NumericExtractor: {numeric_time:.4f}s - {len(numeric_values)} valeurs + {len(detailed_features)} détails")
            
            total_specialized_time = address_time + financial_time + numeric_time
            logger.info(f"⏱️ Temps total extracteurs spécialisés: {total_specialized_time:.4f}s")
            
        except Exception as e:
            logger.error(f"❌ Erreur avec les extracteurs spécialisés: {e}")
        
        logger.info("🎉 Test de comparaison terminé !")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test de comparaison: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_performance_comparison())
