#!/usr/bin/env python3
"""
Test de l'extraction des informations numériques détaillées des unités
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

def test_units_numeric_extraction():
    """Test l'extraction des informations numériques des unités"""
    
    # HTML avec les informations des unités
    html_content = """
    <div class="row">
        <div class="col-lg-3 col-sm-6 carac-container">
            <div class="carac-title">Unités résidentielles</div>
            <div class="carac-value"><span>1 x 4 ½, 2 x 5 ½</span></div>
        </div>
        <div class="col-lg-3 col-sm-6 carac-container">
            <div class="carac-title">Unité principale</div>
            <div class="carac-value"><span>5 pièces, 3 chambres, 1 salle de bain</span></div>
        </div>
        <div class="col-lg-3 col-sm-6 carac-container">
            <div class="carac-title">Nombre d'unités</div>
            <div class="carac-value"><span>Résidentiel (3)</span></div>
        </div>
    </div>
    """
    
    # Parsing du HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Test de l'extracteur
    extractor = NumericExtractor()
    
    print("🔍 Test de l'extraction des informations numériques des unités")
    print("=" * 60)
    
    # Test 1: Extraction des caractéristiques détaillées
    print("\n📊 1. Extraction des caractéristiques détaillées:")
    detailed_features = extractor.extract_detailed_features(soup)
    
    print(f"   📋 Unités résidentielles: {detailed_features.get('residential_units_detail', 'Non trouvé')}")
    print(f"   🏠 Unité principale: {detailed_features.get('main_unit_detail', 'Non trouvé')}")
    
    # Test 2: Validation des nouvelles informations numériques des unités
    print("\n🔢 2. Validation des informations numériques des unités:")
    
    expected_units = {
        'units_4_half_count': 1,
        'units_5_half_count': 2,
        'units_6_half_count': None
    }
    
    for key, expected in expected_units.items():
        actual = detailed_features.get(key)
        status = "✅" if actual == expected else "❌"
        print(f"   {status} {key}: attendu {expected}, obtenu {actual}")
    
    # Test 3: Validation des informations numériques de l'unité principale
    print("\n🏠 3. Validation des informations numériques de l'unité principale:")
    
    expected_main_unit = {
        'main_unit_rooms': 5,
        'main_unit_bedrooms': 3,
        'main_unit_bathrooms': 1
    }
    
    for key, expected in expected_main_unit.items():
        actual = detailed_features.get(key)
        status = "✅" if actual == expected else "❌"
        print(f"   {status} {key}: attendu {expected}, obtenu {actual}")
    
    # Test 4: Test direct des méthodes d'extraction
    print("\n🔍 4. Test direct des méthodes d'extraction:")
    
    # Test extraction des unités
    units_text = "1 x 4 ½, 2 x 5 ½"
    units_details = extractor.extract_units_numeric_details(units_text)
    print(f"   🏘️ Détails des unités depuis '{units_text}': {units_details}")
    
    # Test extraction de l'unité principale
    main_unit_text = "5 pièces, 3 chambres, 1 salle de bain"
    main_unit_details = extractor.extract_main_unit_numeric_details(main_unit_text)
    print(f"   🏠 Détails de l'unité principale depuis '{main_unit_text}': {main_unit_details}")
    
    # Test 5: Résumé des extractions
    print("\n📋 5. Résumé des extractions:")
    print(f"   🏘️ Unités 4 ½: {detailed_features.get('units_4_half_count', 'Non trouvé')}")
    print(f"   🏘️ Unités 5 ½: {detailed_features.get('units_5_half_count', 'Non trouvé')}")
    print(f"   🏘️ Unités 6 ½: {detailed_features.get('units_6_half_count', 'Non trouvé')}")
    print(f"   🏠 Pièces unité principale: {detailed_features.get('main_unit_rooms', 'Non trouvé')}")
    print(f"   🛏️ Chambres unité principale: {detailed_features.get('main_unit_bedrooms', 'Non trouvé')}")
    print(f"   🚿 Salles de bain unité principale: {detailed_features.get('main_unit_bathrooms', 'Non trouvé')}")
    
    # Test 6: Validation des résultats
    print("\n✅ 6. Validation des résultats:")
    
    all_tests_passed = True
    
    # Vérification des unités
    if detailed_features.get('units_4_half_count') == 1:
        print("   ✅ Extraction unités 4 ½: OK")
    else:
        print("   ❌ Extraction unités 4 ½: ÉCHEC")
        all_tests_passed = False
    
    if detailed_features.get('units_5_half_count') == 2:
        print("   ✅ Extraction unités 5 ½: OK")
    else:
        print("   ❌ Extraction unités 5 ½: ÉCHEC")
        all_tests_passed = False
    
    # Vérification de l'unité principale
    if detailed_features.get('main_unit_rooms') == 5:
        print("   ✅ Extraction pièces unité principale: OK")
    else:
        print("   ❌ Extraction pièces unité principale: ÉCHEC")
        all_tests_passed = False
    
    if detailed_features.get('main_unit_bedrooms') == 3:
        print("   ✅ Extraction chambres unité principale: OK")
    else:
        print("   ❌ Extraction chambres unité principale: ÉCHEC")
        all_tests_passed = False
    
    if detailed_features.get('main_unit_bathrooms') == 1:
        print("   ✅ Extraction salles de bain unité principale: OK")
    else:
        print("   ❌ Extraction salles de bain unité principale: ÉCHEC")
        all_tests_passed = False
    
    print(f"\n🎯 Résultat final: {'✅ TOUS LES TESTS PASSÉS' if all_tests_passed else '❌ CERTAINS TESTS ONT ÉCHOUÉ'}")
    
    return all_tests_passed

if __name__ == "__main__":
    success = test_units_numeric_extraction()
    if success:
        print("\n🎉 Extraction des informations numériques des unités validée !")
    else:
        print("\n💥 Problèmes détectés dans l'extraction !")
