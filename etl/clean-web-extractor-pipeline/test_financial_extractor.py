#!/usr/bin/env python3
"""
Test de l'extracteur financier amélioré avec l'HTML réel de Centris
"""

from bs4 import BeautifulSoup
from src.extractors.centris.extractors.financial_extractor import FinancialExtractor

def test_financial_extractor():
    """Test de l'extracteur financier avec l'HTML réel de Centris"""
    
    # HTML réel de Centris (extrait)
    test_html = """
    <div class="region-content">
        <article id="overview" class="content-views" itemscope="" itemtype="http://schema.org/Product">
            <meta content="Triplex à vendre à Chambly, Montérégie, 608 - 612, boulevard Brassard, 10001989 - Centris.ca" itemprop="name">
            <div class="row property-tagline">
                <div class="d-none d-sm-block house-info">
                    <div class="row" itemscope="" itemtype="https://schema.org/Place">
                        <div class="col text-left pl-0" itemscope="" itemtype="https://schema.org/Place">
                            <h1 itemprop="category">
                                <span data-id="PageTitle">Triplex à vendre</span>
                            </h1>
                            <div class="d-flex mt-1">
                                <button class="btn-open-map" onclick="window.open('https://maps.google.ca/maps?z=15&amp;hl=fr&amp;q=45.44759306,-73.30302874');">
                                    <i class="fas fa-map-marker-alt"></i>
                                </button>
                                <h2 itemprop="address" class="pt-1">
                                    608 - 612, boulevard Brassard, Chambly
                                </h2>
                            </div>
                            <div itemprop="geo" itemscope="" itemtype="http://schema.org/GeoCoordinates">
                                <meta itemprop="latitude" content="45.4475930600">
                                <meta itemprop="longitude" content="-73.3030287400">
                            </div>
                        </div>
                        <div class="price-container">
                            <div class="price text-right" itemprop="offers" itemtype="http://schema.org/Offer" itemscope="">
                                <meta itemprop="priceCurrency" content="CAD">
                                <meta itemprop="price" content="699000">
                                <span id="BuyPrice" class="text-nowrap">699&nbsp;000 $</span>
                                <span class="desc"></span>
                                <span style="display:none;">ou</span>
                                <span class="text-nowrap"> <span class="desc"></span></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-3 col-sm-6 carac-container">
                    <div class="carac-title">Revenus bruts potentiels</div>
                    <div class="carac-value"><span>43&nbsp;320 $</span></div>
                </div>
            </div>
            <div class="financial-details-container container-fluid mb-5">
                <div class="financial-details-table">
                    <table class="table">
                        <thead>
                            <tr>
                                <th colspan="2" class="col pl-0 financial-details-table-title">Évaluation municipale (2025)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Terrain</td>
                                <td class="text-right">182&nbsp;100 $</td>
                            </tr>
                            <tr>
                                <td>Bâtiment</td>
                                <td class="text-right">393&nbsp;000 $</td>
                            </tr>
                        </tbody>
                        <tfoot>
                            <tr class="col pl-0 financial-details-table-total">
                                <td class="font-weight-bold">Total</td>
                                <td class="font-weight-bold text-right">575&nbsp;100 $</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
                <div class="financial-details-table">
                    <table class="table">
                        <thead>
                            <tr>
                                <th colspan="2" class="col pl-0 financial-details-table-title">Taxes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>Municipales (2025)</td>
                                <td class="text-right">4&nbsp;339 $</td>
                            </tr>
                            <tr>
                                <td>Scolaires (2024)</td>
                                <td class="text-right">446 $</td>
                            </tr>
                        </tbody>
                        <tfoot>
                            <tr class="col pl-0 financial-details-table-total">
                                <td class="font-weight-bold">Total</td>
                                <td class="font-weight-bold text-right">4&nbsp;785 $</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div>
        </article>
    </div>
    """
    
    soup = BeautifulSoup(test_html, 'html.parser')
    extractor = FinancialExtractor()
    
    print("🧪 Test de l'extracteur financier avec HTML réel de Centris")
    print("=" * 60)
    
    # Test d'extraction du prix
    price = extractor._extract_price(soup)
    print(f"💰 Prix extrait: {price}")
    
    # Test d'extraction complète des informations financières
    financial = extractor.extract_financial(soup)
    print(f"💳 Informations financières: {financial}")
    
    print("\n✅ Test terminé !")

if __name__ == "__main__":
    test_financial_extractor()
