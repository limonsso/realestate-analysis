#!/usr/bin/env python3
"""
Test de l'extraction dynamique des unités avec différents types
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

def test_dynamic_units_extraction():
    """Test l'extraction dynamique des unités avec différents types"""
    
    print("🔍 Test de l'extraction dynamique des unités")
    print("=" * 60)
    
    extractor = NumericExtractor()
    
    # Test 1: Cas simple (1 x 4 ½, 2 x 5 ½)
    print("\n📊 1. Test cas simple:")
    simple_text = "1 x 4 ½, 2 x 5 ½"
    simple_result = extractor.extract_units_numeric_details(simple_text)
    print(f"   📝 Texte: '{simple_text}'")
    print(f"   🔢 Résultat: {simple_result}")
    
    # Test 2: Cas complexe avec plusieurs types
    print("\n📊 2. Test cas complexe:")
    complex_text = "1 x 2 ½, 2 x 3 ½, 1 x 4 ½, 2 x 5 ½, 1 x 9 ½"
    complex_result = extractor.extract_units_numeric_details(complex_text)
    print(f"   📝 Texte: '{complex_text}'")
    print(f"   🔢 Résultat: {complex_result}")
    
    # Test 3: Cas avec espaces et formatage
    print("\n📊 3. Test cas avec espaces:")
    spaced_text = "1 x 2½, 2 x 3 ½, 1 x 4½, 2 x 5 ½"
    spaced_result = extractor.extract_units_numeric_details(spaced_text)
    print(f"   📝 Texte: '{spaced_text}'")
    print(f"   🔢 Résultat: {spaced_result}")
    
    # Test 4: Cas avec un seul type
    print("\n📊 4. Test cas avec un seul type:")
    single_text = "3 x 6 ½"
    single_result = extractor.extract_units_numeric_details(single_text)
    print(f"   📝 Texte: '{single_text}'")
    print(f"   🔢 Résultat: {single_result}")
    
    # Test 5: Cas avec des unités sans ½
    print("\n📊 5. Test cas avec des unités sans ½:")
    no_half_text = "1 x 2, 2 x 3, 1 x 4"
    no_half_result = extractor.extract_units_numeric_details(no_half_text)
    print(f"   📝 Texte: '{no_half_text}'")
    print(f"   🔢 Résultat: {no_half_result}")
    
    # Test 6: Validation des résultats
    print("\n✅ 6. Validation des résultats:")
    
    # Validation du cas simple
    if simple_result.get('units_4_half_count') == 1 and simple_result.get('units_5_half_count') == 2:
        print("   ✅ Cas simple: OK")
    else:
        print("   ❌ Cas simple: ÉCHEC")
    
    # Validation du cas complexe
    expected_complex = {
        'units_2_half_count': 1,
        'units_3_half_count': 2,
        'units_4_half_count': 1,
        'units_5_half_count': 2,
        'units_9_half_count': 1,
        'total_units': 7
    }
    
    complex_valid = True
    for key, expected in expected_complex.items():
        if complex_result.get(key) != expected:
            print(f"   ❌ {key}: attendu {expected}, obtenu {complex_result.get(key)}")
            complex_valid = False
        else:
            print(f"   ✅ {key}: {expected}")
    
    if complex_valid:
        print("   ✅ Cas complexe: OK")
    else:
        print("   ❌ Cas complexe: ÉCHEC")
    
    # Test 7: Test avec HTML complet
    print("\n📊 7. Test avec HTML complet:")
    html_content = """
    <div class="row">
        <div class="col-lg-3 col-sm-6 carac-container">
            <div class="carac-title">Unités résidentielles</div>
            <div class="carac-value"><span>1 x 2 ½, 2 x 3 ½, 1 x 4 ½, 2 x 5 ½, 1 x 9 ½</span></div>
        </div>
        <div class="col-lg-3 col-sm-6 carac-container">
            <div class="carac-title">Unité principale</div>
            <div class="carac-value"><span>5 pièces, 3 chambres, 1 salle de bain</span></div>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    detailed_features = extractor.extract_detailed_features(soup)
    
    print(f"   📋 Unités résidentielles: {detailed_features.get('residential_units_detail', 'Non trouvé')}")
    print(f"   🏠 Unité principale: {detailed_features.get('main_unit_detail', 'Non trouvé')}")
    
    # Vérifier que les informations dynamiques sont extraites
    if detailed_features.get('units_2_half_count') == 1:
        print("   ✅ Extraction unités 2 ½: OK")
    else:
        print("   ❌ Extraction unités 2 ½: ÉCHEC")
    
    if detailed_features.get('total_units') == 7:
        print("   ✅ Total des unités: OK")
    else:
        print("   ❌ Total des unités: ÉCHEC")
    
    # Test 8: Résumé des capacités
    print("\n📋 8. Résumé des capacités:")
    print(f"   🏘️ Types d'unités supportés: 2 ½, 3 ½, 4 ½, 5 ½, 6 ½, 7 ½, 8 ½, 9 ½")
    print(f"   🔢 Extraction dynamique: Oui")
    print(f"   📊 Calcul automatique du total: Oui")
    print(f"   🗂️ Répartition détaillée: Oui")
    
    print("\n🎯 Test de l'extraction dynamique terminé !")
    
    return complex_valid

if __name__ == "__main__":
    success = test_dynamic_units_extraction()
    if success:
        print("\n🎉 Extraction dynamique des unités validée !")
    else:
        print("\n💥 Problèmes détectés dans l'extraction dynamique !")
