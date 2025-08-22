#!/usr/bin/env python3
"""
Exemple d'utilisation de la validation des résultats de recherche
"""

import sys
import asyncio
from pathlib import Path

# Ajout des chemins au PYTHONPATH
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir / "src"))
sys.path.insert(0, str(current_dir / "config"))

from src.extractors.centris_extractor import CentrisExtractor
from src.models.property import PropertySummary, Address, PropertyType, SearchQuery
from config.settings import config

async def demonstrate_validation():
    """Démontre la validation des résultats de recherche"""
    
    print("🔍 Démonstration de la Validation des Résultats")
    print("=" * 60)
    
    # Création de l'extracteur
    extractor = CentrisExtractor(config.centris)
    
    # Scénario 1: Résultats valides (Montréal + Condos)
    print("\n📋 Scénario 1: Résultats Valides")
    print("-" * 40)
    
    valid_properties = [
        PropertySummary(
            id="prop1",
            address=Address(city="Montréal", region="Québec"),
            type=PropertyType.CONDO,
            price=250000
        ),
        PropertySummary(
            id="prop2",
            address=Address(city="Montréal", region="Québec"),
            type=PropertyType.CONDO,
            price=300000
        ),
        PropertySummary(
            id="prop3",
            address=Address(city="Montréal", region="Québec"),
            type=PropertyType.CONDO,
            price=275000
        )
    ]
    
    search_query = SearchQuery(
        locations=["Montréal"],
        property_types=[PropertyType.CONDO]
    )
    
    print("🔍 Test de validation des localisations...")
    location_valid = extractor._validate_locations_searched(valid_properties, ["Montréal"])
    print(f"   Localisations: {location_valid}")
    
    print("🔍 Test de validation des types...")
    type_valid = extractor._validate_property_types(valid_properties, [PropertyType.CONDO])
    print(f"   Types: {type_valid}")
    
    print("🔍 Test de validation globale...")
    is_valid = extractor._validate_search_results(valid_properties, search_query)
    print(f"   Global: {is_valid}")
    
    # Scénario 2: Résultats partiellement valides
    print("\n📋 Scénario 2: Résultats Partiellement Valides")
    print("-" * 40)
    
    mixed_properties = [
        PropertySummary(
            id="prop4",
            address=Address(city="Montréal", region="Québec"),
            type=PropertyType.CONDO,
            price=250000
        ),
        PropertySummary(
            id="prop5",
            address=Address(city="Laval", region="Québec"),  # Mauvais ville
            type=PropertyType.CONDO,
            price=300000
        ),
        PropertySummary(
            id="prop6",
            address=Address(city="Montréal", region="Québec"),
            type=PropertyType.SINGLE_FAMILY_HOME,  # Mauvais type
            price=275000
        )
    ]
    
    print("🔍 Test de validation des localisations...")
    location_valid_mixed = extractor._validate_locations_searched(mixed_properties, ["Montréal"])
    print(f"   Localisations: {location_valid_mixed}")
    
    print("🔍 Test de validation des types...")
    type_valid_mixed = extractor._validate_property_types(mixed_properties, [PropertyType.CONDO])
    print(f"   Types: {type_valid_mixed}")
    
    print("🔍 Test de validation globale...")
    is_valid_mixed = extractor._validate_search_results(mixed_properties, search_query)
    print(f"   Global: {is_valid_mixed}")
    
    # Scénario 3: Résultats invalides
    print("\n📋 Scénario 3: Résultats Invalides")
    print("-" * 40)
    
    invalid_properties = [
        PropertySummary(
            id="prop7",
            address=Address(city="Laval", region="Québec"),
            type=PropertyType.SINGLE_FAMILY_HOME,
            price=250000
        ),
        PropertySummary(
            id="prop8",
            address=Address(city="Brossard", region="Québec"),
            type=PropertyType.PLEX,
            price=300000
        ),
        PropertySummary(
            id="prop9",
            address=Address(city="Longueuil", region="Québec"),
            type=PropertyType.RESIDENTIAL_LOT,
            price=275000
        )
    ]
    
    print("🔍 Test de validation des localisations...")
    location_valid_invalid = extractor._validate_locations_searched(invalid_properties, ["Montréal"])
    print(f"   Localisations: {location_valid_invalid}")
    
    print("🔍 Test de validation des types...")
    type_valid_invalid = extractor._validate_property_types(invalid_properties, [PropertyType.CONDO])
    print(f"   Types: {type_valid_invalid}")
    
    print("🔍 Test de validation globale...")
    is_valid_invalid = extractor._validate_search_results(invalid_properties, search_query)
    print(f"   Global: {is_valid_invalid}")
    
    print("\n🎯 Résumé de la Validation")
    print("-" * 40)
    print("✅ Scénario 1: 100% correspondance → Validation réussie")
    print("⚠️ Scénario 2: 33% correspondance → Validation échoue")
    print("❌ Scénario 3: 0% correspondance → Validation échoue")
    print("\n💡 La validation s'arrête si moins de 70% des résultats correspondent")
    print("💡 Les deux validations (localisation + type) doivent réussir")

if __name__ == "__main__":
    try:
        asyncio.run(demonstrate_validation())
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
