#!/usr/bin/env python3
"""
Test de l'extracteur d'adresse amélioré avec l'HTML réel de Centris
"""

from bs4 import BeautifulSoup
from src.extractors.centris.extractors.address_extractor import AddressExtractor

def test_address_extractor():
    """Test de l'extracteur d'adresse avec l'HTML réel de Centris"""
    
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
                    </div>
                </div>
            </div>
        </article>
    </div>
    """
    
    soup = BeautifulSoup(test_html, 'html.parser')
    extractor = AddressExtractor()
    
    print("🧪 Test de l'extracteur d'adresse avec HTML réel de Centris")
    print("=" * 60)
    
    # Test d'extraction de la rue
    street = extractor._extract_street(soup)
    print(f"🏠 Rue extraite: {street}")
    
    # Test d'extraction de la ville
    city = extractor._extract_city(soup)
    print(f"🏙️ Ville extraite: {city}")
    
    # Test d'extraction de la région
    region = extractor._extract_region(soup)
    print(f"🏛️ Région extraite: {region}")
    
    # Test d'extraction complète de l'adresse
    address = extractor.extract_address(soup)
    print(f"📍 Adresse complète: {address}")
    
    print("\n✅ Test terminé !")

if __name__ == "__main__":
    test_address_extractor()
