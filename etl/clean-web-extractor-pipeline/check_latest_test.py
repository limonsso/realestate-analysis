#!/usr/bin/env python3
"""
Script pour vérifier les données de la dernière collection de test Chambly
"""

import pymongo
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


async def check_latest_test():
    """Vérifie les données de la dernière collection de test"""
    try:
        # Connexion directe à MongoDB
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client["real_estate_analytics"]
        
        # Liste des collections
        collection_names = await db.list_collection_names()
        
        # Filtrer les collections Chambly test
        chambly_collections = [name for name in collection_names if "chambly" in name and "test" in name]
        
        if not chambly_collections:
            print("❌ Aucune collection de test Chambly trouvée")
            return
        
        # Trier par timestamp pour obtenir la plus récente
        def extract_timestamp(collection_name):
            parts = collection_name.split('_')
            for i, part in enumerate(parts):
                if part.isdigit() and len(part) == 8:  # Format YYYYMMDD
                    try:
                        timestamp_parts = parts[i:i+2]  # Date et heure
                        return ''.join(timestamp_parts)
                    except:
                        pass
            return collection_name
        
        latest_collection = sorted(chambly_collections, key=extract_timestamp, reverse=True)[0]
        print(f"📊 Collection la plus récente: {latest_collection}")
        
        # Récupérer une propriété exemple
        collection = db[latest_collection]
        property_doc = await collection.find_one({})
        
        if not property_doc:
            print("❌ Aucune propriété trouvée dans la collection")
            return
        
        print(f"🏠 Propriété exemple: {property_doc.get('id', 'Unknown')}")
        print(f"📍 Adresse: {property_doc.get('address', {}).get('street', 'N/A')}")
        print(f"🏷️ Type: {property_doc.get('type', 'N/A')}")
        print(f"🏠 Catégorie: {property_doc.get('category', 'N/A')}")
        
        # Vérifier les champs numériques spécifiques
        print("\n🔢 Champs numériques:")
        numeric_fields = [
            'construction_year', 'terrain_area_sqft', 'parking_count', 
            'units_count', 'walk_score', 'main_unit_rooms', 
            'main_unit_bedrooms', 'main_unit_bathrooms', 'total_units'
        ]
        
        for field in numeric_fields:
            value = property_doc.get(field)
            status = "✅" if value is not None else "❌"
            print(f"   {status} {field}: {value}")
        
        # Vérifier les features
        print("\n🏠 Features:")
        features = property_doc.get('features', {})
        if features:
            for key, value in features.items():
                status = "✅" if value is not None else "❌"
                print(f"   {status} {key}: {value}")
        else:
            print("   ❌ Aucune feature trouvée")
        
        # Vérifier les infos textuelles
        print("\n📝 Informations textuelles:")
        text_fields = ['units_info', 'parking_info', 'residential_units_detail', 'main_unit_detail']
        for field in text_fields:
            value = property_doc.get(field)
            status = "✅" if value is not None else "❌"
            print(f"   {status} {field}: {value}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(check_latest_test())
