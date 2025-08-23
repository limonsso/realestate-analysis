#!/usr/bin/env python3
"""
Test des extracteurs spécialisés avec le HTML réel de Chambly
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

async def test_specialized_extractors():
    """Test des extracteurs spécialisés avec le HTML réel de Chambly"""
    try:
        logger.info("🧪 Début du test des extracteurs spécialisés")
        
        # Import des extracteurs spécialisés
        from src.extractors.centris.extractors import AddressExtractor, FinancialExtractor, NumericExtractor
        
        # Création des instances
        address_extractor = AddressExtractor()
        financial_extractor = FinancialExtractor()
        numeric_extractor = NumericExtractor()
        
        logger.info("✅ Extracteurs spécialisés créés avec succès")
        
        # HTML réel de Chambly (extrait du test précédent)
        real_html = """
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
        
        soup = BeautifulSoup(real_html, 'html.parser')
        
        logger.info("🧪 Test des extracteurs avec le HTML réel de Chambly...")
        
        # Test AddressExtractor
        logger.info("📍 Test AddressExtractor...")
        address_data = address_extractor.extract_address(soup)
        logger.info(f"📍 Adresse extraite: {address_data}")
        
        # Test FinancialExtractor
        logger.info("💰 Test FinancialExtractor...")
        financial_data = financial_extractor.extract_financial(soup)
        logger.info(f"💰 Données financières: {financial_data}")
        
        # Test NumericExtractor
        logger.info("🔢 Test NumericExtractor...")
        numeric_values = numeric_extractor.extract_numeric_values(soup)
        logger.info(f"🔢 Valeurs numériques: {numeric_values}")
        
        detailed_features = numeric_extractor.extract_detailed_features(soup)
        logger.info(f"🔍 Caractéristiques détaillées: {detailed_features}")
        
        # Validation des résultats
        logger.info("✅ Validation des résultats...")
        
        # Validation AddressExtractor
        assert address_data.get('city') == 'Chambly', f"Ville incorrecte: {address_data.get('city')}"
        assert address_data.get('latitude') == 45.441214, f"Latitude incorrecte: {address_data.get('latitude')}"
        assert address_data.get('longitude') == -73.296067, f"Longitude incorrecte: {address_data.get('longitude')}"
        logger.info("✅ AddressExtractor: Validation réussie")
        
        # Validation FinancialExtractor
        assert financial_data.get('potential_gross_revenue') == 36960, f"Revenus incorrects: {financial_data.get('potential_gross_revenue')}"
        logger.info("✅ FinancialExtractor: Validation réussie")
        
        # Validation NumericExtractor
        assert numeric_values.get('construction_year') == 1989, f"Année incorrecte: {numeric_values.get('construction_year')}"
        assert numeric_values.get('terrain_area') == 4755, f"Superficie incorrecte: {numeric_values.get('terrain_area')}"
        assert numeric_values.get('parking_count') == 4, f"Stationnements incorrects: {numeric_values.get('parking_count')}"
        assert numeric_values.get('units_count') == 3, f"Unités incorrectes: {numeric_values.get('units_count')}"
        assert numeric_values.get('potential_revenue') == 36960, f"Revenus incorrects: {numeric_values.get('potential_revenue')}"
        logger.info("✅ NumericExtractor: Validation réussie")
        
        # Validation des caractéristiques détaillées
        assert detailed_features.get('residential_units_detail') == '1 x 4 ½, 2 x 5 ½', f"Détail unités incorrect: {detailed_features.get('residential_units_detail')}"
        assert detailed_features.get('main_unit_detail') == '5 pièces, 3 chambres, 1 salle de bain', f"Unité principale incorrecte: {detailed_features.get('main_unit_detail')}"
        logger.info("✅ Caractéristiques détaillées: Validation réussie")
        
        logger.info("🎉 Tous les tests des extracteurs spécialisés ont réussi !")
        
        # Résumé des performances
        logger.info("📊 Résumé des performances:")
        logger.info(f"📍 AddressExtractor: {len(address_data)} champs extraits")
        logger.info(f"💰 FinancialExtractor: {len(financial_data)} champs extraits")
        logger.info(f"🔢 NumericExtractor: {len(numeric_values)} valeurs numériques extraites")
        logger.info(f"🔍 Caractéristiques: {len(detailed_features)} champs détaillés extraits")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_specialized_extractors())
