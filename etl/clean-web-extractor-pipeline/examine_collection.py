#!/usr/bin/env python3
"""
Examen du contenu d'une collection MongoDB pour voir quels IDs sont présents
"""

import asyncio
import motor.motor_asyncio

async def examine_collection():
    """Examine le contenu d'une collection MongoDB"""
    
    print("🔍 Examen du contenu d'une collection MongoDB")
    print("=" * 50)
    
    try:
        # Connexion à MongoDB
        client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
        
        # Test de connexion
        await client.admin.command('ping')
        print("✅ Connexion MongoDB réussie")
        
        # Base de données
        db = client['real_estate_analytics']
        
        # Collection à examiner
        collection_name = "chambly_plex_test_20250822_155540"
        collection = db[collection_name]
        
        print(f"\n📊 Examen de la collection: {collection_name}")
        
        # Compter les documents
        count = await collection.count_documents({})
        print(f"📈 Nombre total de documents: {count}")
        
        if count > 0:
            # Lister tous les documents avec leurs IDs
            print(f"\n🔍 IDs des propriétés dans la collection:")
            cursor = collection.find({}, {"id": 1, "address.street": 1, "financial.price": 1})
            
            documents = await cursor.to_list(length=count)
            
            for i, doc in enumerate(documents, 1):
                doc_id = doc.get('id', 'N/A')
                street = doc.get('address', {}).get('street', 'N/A')
                price = doc.get('financial', {}).get('price', 'N/A')
                print(f"   {i}. ID: {doc_id}")
                print(f"      📍 Rue: {street}")
                print(f"      💰 Prix: {price}")
                print()
            
            # Chercher spécifiquement la propriété 21002530
            print(f"🔍 Recherche spécifique de la propriété 21002530...")
            property_doc = await collection.find_one({"id": "21002530"})
            
            if property_doc:
                print(f"✅ Propriété 21002530 trouvée!")
                print(f"   📍 Adresse: {property_doc.get('address', {}).get('street', 'N/A')}")
                print(f"   💰 Prix: {property_doc.get('financial', {}).get('price', 'N/A')}")
                print(f"   🏠 Type: {property_doc.get('type', 'N/A')}")
                print(f"   🏠 Catégorie: {property_doc.get('category', 'N/A')}")
                
                # Vérifier les informations détaillées
                print(f"\n🔍 Informations détaillées:")
                print(f"   🏘️ Unités résidentielles: {property_doc.get('residential_units_detail', '❌ NULL')}")
                print(f"   🏠 Unité principale: {property_doc.get('main_unit_detail', '❌ NULL')}")
                print(f"   🏗️ Année construction: {property_doc.get('construction_year', '❌ NULL')}")
                print(f"   📏 Superficie terrain: {property_doc.get('terrain_area_sqft', '❌ NULL')}")
                print(f"   🚗 Nombre stationnements: {property_doc.get('parking_count', '❌ NULL')}")
                print(f"   🏘️ Nombre d'unités: {property_doc.get('units_count', '❌ NULL')}")
                print(f"   🚶 Walk Score: {property_doc.get('walk_score', '❌ NULL')}")
                print(f"   🏠 Utilisation: {property_doc.get('property_usage', '❌ NULL')}")
                print(f"   🏗️ Style bâtiment: {property_doc.get('building_style', '❌ NULL')}")
                print(f"   📅 Date emménagement: {property_doc.get('move_in_date', '❌ NULL')}")
                
                # Vérifier les compteurs d'unités spécifiques
                print(f"\n🔢 Compteurs d'unités spécifiques:")
                unit_fields = [
                    'units_2_half_count', 'units_3_half_count', 'units_4_half_count',
                    'units_5_half_count', 'units_6_half_count', 'units_7_half_count',
                    'units_8_half_count', 'units_9_half_count'
                ]
                
                for field in unit_fields:
                    value = property_doc.get(field)
                    print(f"   {field}: {value or '❌ NULL'}")
                
                # Informations de l'unité principale
                print(f"\n🏠 Informations de l'unité principale:")
                main_unit_fields = [
                    'main_unit_rooms', 'main_unit_bedrooms', 'main_unit_bathrooms'
                ]
                
                for field in main_unit_fields:
                    value = property_doc.get(field)
                    print(f"   {field}: {value or '❌ NULL'}")
                
            else:
                print(f"❌ Propriété 21002530 non trouvée")
                
                # Vérifier s'il y a des propriétés avec des IDs similaires
                print(f"\n🔍 Recherche d'IDs similaires...")
                cursor = collection.find({"id": {"$regex": "2100"}})
                similar_docs = await cursor.to_list(length=10)
                
                if similar_docs:
                    print(f"📋 Propriétés avec des IDs commençant par '2100':")
                    for doc in similar_docs:
                        print(f"   ID: {doc.get('id')} - Rue: {doc.get('address', {}).get('street', 'N/A')}")
                else:
                    print(f"   Aucune propriété avec un ID commençant par '2100'")
        else:
            print(f"❌ Collection vide")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'examen: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if 'client' in locals():
            client.close()
            print("\n🔌 Connexion MongoDB fermée")

if __name__ == "__main__":
    asyncio.run(examine_collection())
