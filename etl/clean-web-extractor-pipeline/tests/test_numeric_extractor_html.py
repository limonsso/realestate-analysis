#!/usr/bin/env python3
"""
Test de l'extracteur numérique avec le HTML fourni
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.extractors.centris.extractors.numeric_extractor import NumericExtractor
from bs4 import BeautifulSoup
import structlog

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

def test_numeric_extraction():
    """Test l'extraction des valeurs numériques avec le HTML fourni"""
    
    # HTML fourni par l'utilisateur
    html_content = """
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
            <div class="carac-value"><span>1976</span></div>
        </div>
        <div class="col-lg-3 col-sm-6 carac-container">
            <div class="carac-title">Superficie du terrain</div>
            <div class="carac-value"><span>5 654 pc</span></div>
        </div>
        
        <div class="col-lg-3 col-sm-6 carac-container">
            <div class="carac-title">Stationnement total</div>
            <div class="carac-value"><span>Garage (1)</span></div>
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
            <div class="carac-value"><span>43 320 $</span></div>
        </div>
        
        <div class="col-lg-3 col-sm-6 carac-container">
            <div class="carac-title">Date d'emménagement</div>
            <div class="carac-value"><span>Selon les baux</span></div>
        </div>
        
        <div class="col-lg-3 col-sm-6 carac-container">
            <div class="carac-title">walkscore</div>
            <div class="carac-value">
                <a onclick="OpenWalkScore(this);" title="La plupart des services à distance de marche" data-url="https://www.walkscore.com/score/608--612-boulevard-brassard-chambly/lat=45.44759306/lng=-73.30302874/?utm_source=centris.ca&amp;utm_medium=ws_api&amp;utm_campaign=ws_api" style="" target="_blank"><span>71</span></a>
            </div>
        </div>
    </div>
    """
    
    # Parsing du HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Test de l'extracteur
    extractor = NumericExtractor()
    
    print("🔍 Test de l'extraction des valeurs numériques")
    print("=" * 50)
    
    # Test 1: Extraction des valeurs numériques de base
    print("\n📊 1. Extraction des valeurs numériques de base:")
    numeric_values = extractor.extract_numeric_values(soup)
    
    expected_values = {
        'construction_year': 1976,
        'terrain_area': 5654,
        'parking_count': 1,
        'units_count': 3,
        'potential_revenue': 43320,
        'walk_score': 71
    }
    
    for key, expected in expected_values.items():
        actual = numeric_values.get(key)
        status = "✅" if actual == expected else "❌"
        print(f"   {status} {key}: attendu {expected}, obtenu {actual}")
    
    # Test 2: Extraction des caractéristiques détaillées
    print("\n🔍 2. Extraction des caractéristiques détaillées:")
    detailed_features = extractor.extract_detailed_features(soup)
    
    print(f"   📋 Unités résidentielles: {detailed_features.get('residential_units_detail', 'Non trouvé')}")
    print(f"   🏠 Unité principale: {detailed_features.get('main_unit_detail', 'Non trouvé')}")
    print(f"   🔢 Répartition unités: {detailed_features.get('units_breakdown', 'Non trouvé')}")
    print(f"   🔢 Nombres unité principale: {detailed_features.get('main_unit_numbers', 'Non trouvé')}")
    
    # Test 3: Validation des résultats
    print("\n📋 3. Résumé des extractions:")
    print(f"   🏗️ Année construction: {numeric_values.get('construction_year', 'Non trouvé')}")
    print(f"   📏 Superficie terrain: {numeric_values.get('terrain_area', 'Non trouvé')} pc")
    print(f"   🚗 Stationnements: {numeric_values.get('parking_count', 'Non trouvé')}")
    print(f"   🏘️ Nombre d'unités: {numeric_values.get('units_count', 'Non trouvé')}")
    print(f"   💰 Revenus potentiels: {numeric_values.get('potential_revenue', 'Non trouvé')}$")
    print(f"   🚶 Walk Score: {numeric_values.get('walk_score', 'Non trouvé')}")
    
    # Test 4: Vérification des patterns regex
    print("\n🔍 4. Test des patterns regex:")
    test_cases = [
        ("1976", "Année construction"),
        ("5 654 pc", "Superficie terrain"),
        ("Garage (1)", "Stationnements"),
        ("Résidentiel (3)", "Nombre d'unités"),
        ("43 320 $", "Revenus"),
        ("71", "Walk Score")
    ]
    
    for test_value, description in test_cases:
        if "1976" in test_value:
            result = extractor._extract_year(test_value)
        elif "pc" in test_value:
            result = extractor._extract_terrain_area(test_value)
        elif "(" in test_value and ")" in test_value:
            if "Résidentiel" in test_value:
                result = extractor._extract_units_count(test_value)
            else:
                result = extractor._extract_parking_count(test_value)
        elif "$" in test_value:
            result = extractor._extract_revenue(test_value)
        else:
            result = extractor._extract_walk_score(test_value)
        
        status = "✅" if result is not None else "❌"
        print(f"   {status} {description}: '{test_value}' -> {result}")
    
    print("\n🎯 Test terminé !")

if __name__ == "__main__":
    test_numeric_extraction()
