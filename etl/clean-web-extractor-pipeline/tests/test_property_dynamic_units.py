#!/usr/bin/env python3
"""
Test complet du modèle Property avec les nouvelles informations dynamiques des unités
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.models.property import Property, PropertyType, PropertyStatus, Address, Location, FinancialInfo, PropertyFeatures, PropertyDimensions, PropertyMedia, PropertyDescription, PropertyMetadata
from datetime import datetime

def test_property_dynamic_units():
    """Test la création d'un objet Property avec les nouvelles informations dynamiques des unités"""
    
    print("🔍 Test du modèle Property avec informations dynamiques des unités")
    print("=" * 70)
    
    try:
        # Création d'un objet Property avec des informations dynamiques complexes
        property_data = Property(
            id="12345678",
            type="Complexe Multi-Unités",
            category=PropertyType.PLEX,
            status=PropertyStatus.FOR_SALE,
            
            # Adresse et localisation
            address=Address(
                street="1234 - 1250, Avenue des Multi-Unités",
                city="Montréal",
                region="Québec",
                country="Canada"
            ),
            location=Location(
                latitude=45.5017,
                longitude=-73.5673
            ),
            
            # Informations financières
            financial=FinancialInfo(
                price=2500000.0,
                municipal_evaluation_total=2400000.0,
                municipal_evaluation_year=2025,
                municipal_tax=15000.0,
                school_tax=2000.0,
                potential_gross_revenue=180000.0
            ),
            
            # Caractéristiques physiques
            features=PropertyFeatures(
                rooms=25,
                bedrooms=15,
                bedrooms_basement=8,
                bathrooms=7
            ),
            
            # Dimensions
            dimensions=PropertyDimensions(
                lot_size=15000.0,
                year_built=1990
            ),
            
            # Médias
            media=PropertyMedia(
                main_image="https://example.com/main.jpg",
                images=["https://example.com/img1.jpg", "https://example.com/img2.jpg"]
            ),
            
            # Descriptions
            description=PropertyDescription(
                short_description="Complexe multi-unités avec répartition variée",
                long_description="Description détaillée du complexe...",
                features=["Revenus garantis", "Bien entretenu"],
                amenities=["Stationnement", "Proche services"]
            ),
            
            # Nouvelles informations détaillées
            property_usage="Résidentielle",
            building_style="Complexe",
            parking_info="Garage (5), Allée (10)",
            units_info="Multi-unités (15)",
            main_unit_info="8 pièces, 4 chambres, 2 salles de bain",
            move_in_date="Selon les baux",
            
            # Nouvelles informations numériques extraites
            construction_year=1990,
            terrain_area_sqft=15000,
            parking_count=15,
            units_count=15,
            walk_score=85,
            
            # Informations détaillées des unités
            residential_units_detail="1 x 2 ½, 2 x 3 ½, 1 x 4 ½, 2 x 5 ½, 1 x 9 ½, 3 x 6 ½, 2 x 7 ½, 1 x 8 ½",
            main_unit_detail="8 pièces, 4 chambres, 2 salles de bain",
            
            # Nouvelles informations numériques détaillées des unités (approche dynamique)
            units_2_half_count=1,
            units_3_half_count=2,
            units_4_half_count=1,
            units_5_half_count=2,
            units_6_half_count=3,
            units_7_half_count=2,
            units_8_half_count=1,
            units_9_half_count=1,
            
            # Informations de l'unité principale
            main_unit_rooms=8,
            main_unit_bedrooms=4,
            main_unit_bathrooms=2,
            
            # Champs dynamiques supplémentaires
            total_units=13,
            units_breakdown={
                "2_half": 1,
                "3_half": 2,
                "4_half": 1,
                "5_half": 2,
                "6_half": 3,
                "7_half": 2,
                "8_half": 1,
                "9_half": 1
            },
            
            # Métadonnées
            metadata=PropertyMetadata(
                source="Centris_Test_Dynamic",
                source_id="12345678",
                url="https://www.centris.ca/fr/propriete/12345678"
            )
        )
        
        print("✅ Objet Property créé avec succès !")
        
        # Test des nouvelles propriétés dynamiques
        print("\n📊 Validation des informations dynamiques des unités:")
        print(f"   🏘️ Unités 2 ½: {property_data.units_2_half_count}")
        print(f"   🏘️ Unités 3 ½: {property_data.units_3_half_count}")
        print(f"   🏘️ Unités 4 ½: {property_data.units_4_half_count}")
        print(f"   🏘️ Unités 5 ½: {property_data.units_5_half_count}")
        print(f"   🏘️ Unités 6 ½: {property_data.units_6_half_count}")
        print(f"   🏘️ Unités 7 ½: {property_data.units_7_half_count}")
        print(f"   🏘️ Unités 8 ½: {property_data.units_8_half_count}")
        print(f"   🏘️ Unités 9 ½: {property_data.units_9_half_count}")
        
        print("\n🔍 Validation des informations de l'unité principale:")
        print(f"   🏠 Pièces unité principale: {property_data.main_unit_rooms}")
        print(f"   🛏️ Chambres unité principale: {property_data.main_unit_bedrooms}")
        print(f"   🚿 Salles de bain unité principale: {property_data.main_unit_bathrooms}")
        
        print("\n📋 Validation des champs dynamiques:")
        print(f"   🔢 Total des unités: {property_data.total_units}")
        print(f"   🗂️ Répartition détaillée: {property_data.units_breakdown}")
        
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
        
        # Test de la flexibilité dynamique
        print("\n🔧 Test de la flexibilité dynamique:")
        
        # Vérifier que tous les types d'unités sont supportés
        unit_types = [2, 3, 4, 5, 6, 7, 8, 9]
        all_supported = True
        
        for unit_type in unit_types:
            field_name = f"units_{unit_type}_half_count"
            if hasattr(property_data, field_name):
                value = getattr(property_data, field_name)
                print(f"   ✅ {field_name}: {value}")
            else:
                print(f"   ❌ {field_name}: Non supporté")
                all_supported = False
        
        if all_supported:
            print("   🎯 Tous les types d'unités sont supportés !")
        else:
            print("   ⚠️ Certains types d'unités ne sont pas supportés")
        
        # Test de la cohérence des données
        print("\n🔍 Test de la cohérence des données:")
        
        # Vérifier que le total correspond à la somme des unités
        calculated_total = sum([
            property_data.units_2_half_count or 0,
            property_data.units_3_half_count or 0,
            property_data.units_4_half_count or 0,
            property_data.units_5_half_count or 0,
            property_data.units_6_half_count or 0,
            property_data.units_7_half_count or 0,
            property_data.units_8_half_count or 0,
            property_data.units_9_half_count or 0
        ])
        
        if calculated_total == property_data.total_units:
            print(f"   ✅ Cohérence du total: {calculated_total} = {property_data.total_units}")
        else:
            print(f"   ❌ Incohérence du total: {calculated_total} ≠ {property_data.total_units}")
        
        print("\n🎯 Test du modèle Property avec informations dynamiques réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_property_dynamic_units()
    if success:
        print("\n🎉 Modèle Property avec informations dynamiques validé !")
    else:
        print("\n💥 Problèmes détectés dans le modèle Property !")
