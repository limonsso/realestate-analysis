#!/usr/bin/env python3
"""
Test du modèle Property mis à jour avec les nouvelles informations numériques
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.models.property import Property, PropertyType, PropertyStatus, Address, Location, FinancialInfo, PropertyFeatures, PropertyDimensions, PropertyMedia, PropertyDescription, PropertyMetadata
from datetime import datetime

def test_property_model():
    """Test la création d'un objet Property avec toutes les nouvelles informations"""
    
    print("🔍 Test du modèle Property mis à jour")
    print("=" * 50)
    
    try:
        # Création d'un objet Property complet avec les nouvelles informations
        property_data = Property(
            id="12345678",
            type="Triplex",
            category=PropertyType.PLEX,
            status=PropertyStatus.FOR_SALE,
            
            # Adresse et localisation
            address=Address(
                street="608 - 612, boulevard Brassard",
                city="Chambly",
                region="Montérégie",
                country="Canada"
            ),
            location=Location(
                latitude=45.44759306,
                longitude=-73.30302874
            ),
            
            # Informations financières
            financial=FinancialInfo(
                price=699000.0,
                municipal_evaluation_total=701200.0,
                municipal_evaluation_year=2025,
                municipal_tax=362.0,
                school_tax=446.0,
                potential_gross_revenue=43000.0
            ),
            
            # Caractéristiques physiques
            features=PropertyFeatures(
                rooms=5,
                bedrooms=3,
                bedrooms_basement=4,
                bathrooms=1
            ),
            
            # Dimensions
            dimensions=PropertyDimensions(
                lot_size=5654.0,
                year_built=1976
            ),
            
            # Médias
            media=PropertyMedia(
                main_image="https://example.com/main.jpg",
                images=["https://example.com/img1.jpg", "https://example.com/img2.jpg"]
            ),
            
            # Descriptions
            description=PropertyDescription(
                short_description="Triplex bien entretenu avec revenus annuels de 43 000$",
                long_description="Description détaillée du triplex...",
                features=["Revenus garantis", "Bien entretenu"],
                amenities=["Stationnement", "Proche services"]
            ),
            
            # Nouvelles informations détaillées
            property_usage="Résidentielle",
            building_style="Jumelé",
            parking_info="Garage (1)",
            units_info="Résidentiel (3)",
            main_unit_info="5 pièces, 3 chambres, 1 salle de bain",
            move_in_date="Selon les baux",
            
            # Nouvelles informations numériques extraites
            construction_year=1976,
            terrain_area_sqft=5654,
            parking_count=1,
            units_count=3,
            walk_score=71,
            
            # Informations détaillées des unités
            residential_units_detail="1 x 4 ½, 2 x 5 ½",
            main_unit_detail="5 pièces, 3 chambres, 1 salle de bain",
            
            # Métadonnées
            metadata=PropertyMetadata(
                source="Centris_Test",
                source_id="12345678",
                url="https://www.centris.ca/fr/propriete/12345678"
            )
        )
        
        print("✅ Objet Property créé avec succès !")
        
        # Test des nouvelles propriétés
        print("\n📊 Validation des nouvelles informations numériques:")
        print(f"   🏗️ Année construction: {property_data.construction_year}")
        print(f"   📏 Superficie terrain: {property_data.terrain_area_sqft} pc")
        print(f"   🚗 Nombre stationnements: {property_data.parking_count}")
        print(f"   🏘️ Nombre d'unités: {property_data.units_count}")
        print(f"   🚶 Walk Score: {property_data.walk_score}")
        
        print("\n🔍 Validation des informations détaillées:")
        print(f"   📋 Détail unités résidentielles: {property_data.residential_units_detail}")
        print(f"   🏠 Détail unité principale: {property_data.main_unit_detail}")
        
        # Test des champs calculés
        print("\n🧮 Test des champs calculés:")
        print(f"   💰 Prix par pied carré: {property_data.price_per_sqft}")
        print(f"   🆕 Construction récente: {property_data.is_new_construction}")
        print(f"   💎 Propriété de luxe: {property_data.is_luxury}")
        print(f"   🚗 Total des taxes: {property_data.financial.total_taxes}")
        print(f"   🏠 Total des chambres: {property_data.features.total_bedrooms}")
        
        # Test de sérialisation JSON
        print("\n📝 Test de sérialisation JSON:")
        property_json = property_data.model_dump_json(indent=2)
        print("   ✅ Sérialisation JSON réussie")
        
        # Test de validation des données
        print("\n✅ Validation des données:")
        print(f"   🆔 ID: {property_data.id}")
        print(f"   🏷️ Type: {property_data.type}")
        print(f"   🏠 Catégorie: {property_data.category}")
        print(f"   📍 Adresse: {property_data.address.full_address}")
        print(f"   💰 Prix: {property_data.financial.price}$")
        print(f"   🖼️ Nombre d'images: {property_data.media.image_count}")
        
        print("\n🎯 Test du modèle Property réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_property_model()
    if success:
        print("\n🎉 Tous les tests sont passés !")
    else:
        print("\n💥 Certains tests ont échoué !")
