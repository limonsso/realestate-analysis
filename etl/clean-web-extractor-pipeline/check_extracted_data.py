#!/usr/bin/env python3
"""
Vérification des données extraites pour voir si les informations détaillées sont maintenant correctement extraites
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.database_service import DatabaseService
from config.settings import DatabaseConfig
import asyncio

async def check_extracted_data():
    """Vérifie les données extraites pour voir si les informations détaillées sont correctement extraites"""
    
    print("🔍 Vérification des données extraites")
    print("=" * 50)
    
    # Configuration de base de données
    db_config = DatabaseConfig(
        server_url="mongodb://localhost:27017",
        connection_string="mongodb://localhost:27017",
        database_name="real_estate_analytics",
        username=None,
        password=None
    )
    
    # Connexion à MongoDB
    db_service = DatabaseService(db_config)
    await db_service.connect()
    
    try:
        # Lister toutes les collections disponibles
        print("📚 Collections disponibles dans la base de données:")
        
        # Utiliser la base de données directement pour lister les collections
        collections = await db_service.db.list_collection_names()
        for i, collection in enumerate(collections, 1):
            print(f"   {i}. {collection}")
        
        # Utiliser directement la nouvelle collection
        collection_name = "chambly_plex_test_20250822_163349"
        print(f"\n🔍 Vérification de la collection: {collection_name}")
        
        # Configurer la collection à utiliser
        db_service.set_collection_names(properties_collection=collection_name)
        
        # Compter les documents
        count = await db_service.db[collection_name].count_documents({})
        print(f"📊 Nombre de documents: {count}")
        
        if count == 0:
            print(f"❌ Aucun document trouvé dans {collection_name}")
            return
        
        # Récupérer et analyser directement les données MongoDB
        print(f"\n🔍 Analyse des données dans {collection_name}:")
        print("-" * 60)
        
        # Récupérer toutes les propriétés
        all_properties = await db_service.db[collection_name].find({}).to_list(length=None)
        
        for i, prop in enumerate(all_properties, 1):
            print(f"\n🏠 PROPRIÉTÉ {i}: {prop.get('id', 'N/A')}")
            print(f"   📍 Adresse: {prop.get('address', {}).get('street', 'N/A')}, {prop.get('address', {}).get('city', 'N/A')}")
            print(f"   💰 Prix: {prop.get('financial', {}).get('price', 'N/A'):,}$" if prop.get('financial', {}).get('price') else "   💰 Prix: N/A")
            print(f"   🏠 Type: {prop.get('type', 'N/A')}")
            print(f"   🏷️ Catégorie: {prop.get('category', 'N/A')}")
            
            # Vérifier les champs détaillés
            print("\n   📋 CHAMPS DÉTAILLÉS:")
            
            # Champs généraux
            print(f"      • property_usage: {prop.get('property_usage', 'NULL')}")
            print(f"      • building_style: {prop.get('building_style', 'NULL')}")
            print(f"      • construction_year: {prop.get('construction_year', 'NULL')}")
            print(f"      • terrain_area_sqft: {prop.get('terrain_area_sqft', 'NULL')}")
            print(f"      • move_in_date: {prop.get('move_in_date', 'NULL')}")
            print(f"      • walk_score: {prop.get('walk_score', 'NULL')}")
            
            # Stationnement et unités
            print(f"      • parking_info: {prop.get('parking_info', 'NULL')}")
            print(f"      • parking_count: {prop.get('parking_count', 'NULL')}")
            print(f"      • units_info: {prop.get('units_info', 'NULL')}")
            print(f"      • units_count: {prop.get('units_count', 'NULL')}")
            
            # Unités résidentielles
            print(f"      • residential_units_detail: {prop.get('residential_units_detail', 'NULL')}")
            print(f"      • main_unit_detail: {prop.get('main_unit_detail', 'NULL')}")
            
            # Compteurs d'unités
            print(f"      • units_4_half_count: {prop.get('units_4_half_count', 'NULL')}")
            print(f"      • units_5_half_count: {prop.get('units_5_half_count', 'NULL')}")
            
            # Revenus potentiels
            potential_revenue = prop.get('financial', {}).get('potential_gross_revenue')
            print(f"      • potential_gross_revenue: {potential_revenue or 'NULL'}$")
            
            if i >= 2:  # Limiter à 2 propriétés pour la lisibilité
                print("   ... (autres propriétés omises pour la lisibilité)")
                break
        
        # Résumé des champs NULL
        print("\n📊 ANALYSE DES CHAMPS NULL:")
        print("=" * 60)
        
        null_fields = {}
        total_properties = len(all_properties)
        
        for prop in all_properties:
            # Vérifier chaque champ détaillé
            fields_to_check = [
                'property_usage', 'building_style', 'construction_year', 
                'terrain_area_sqft', 'move_in_date', 'walk_score',
                'parking_info', 'parking_count', 'units_info', 'units_count',
                'residential_units_detail', 'main_unit_detail'
            ]
            
            # Ajouter les compteurs d'unités
            for j in range(2, 10):
                fields_to_check.append(f'units_{j}_half_count')
            
            for field in fields_to_check:
                value = prop.get(field, None)
                if value is None:
                    if field not in null_fields:
                        null_fields[field] = 0
                    null_fields[field] += 1
        
        # Afficher le résumé
        if null_fields:
            print("❌ Champs avec des valeurs NULL:")
            for field, count in sorted(null_fields.items()):
                percentage = (count / total_properties) * 100
                print(f"   • {field}: {count}/{total_properties} ({percentage:.1f}%)")
        else:
            print("✅ Tous les champs détaillés ont des valeurs!")
        
        print()
        print(f"📊 Total: {len(null_fields)} champs avec des valeurs NULL sur {total_properties} propriétés")
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await db_service.close()

if __name__ == "__main__":
    asyncio.run(check_extracted_data())
