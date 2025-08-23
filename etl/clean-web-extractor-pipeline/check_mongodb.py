#!/usr/bin/env python3
"""
Vérification simple de la connexion MongoDB
"""

import asyncio
import motor.motor_asyncio

async def check_mongodb():
    """Vérifie la connexion MongoDB et liste les bases de données"""
    
    print("🔍 Vérification de la connexion MongoDB")
    print("=" * 40)
    
    try:
        # Connexion à MongoDB
        client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
        
        # Test de connexion
        await client.admin.command('ping')
        print("✅ Connexion MongoDB réussie")
        
        # Lister toutes les bases de données
        print("\n📚 Bases de données disponibles:")
        databases = await client.list_database_names()
        
        if databases:
            for i, db_name in enumerate(databases, 1):
                print(f"   {i}. {db_name}")
                
                # Lister les collections de chaque base de données
                db = client[db_name]
                collections = await db.list_collection_names()
                
                if collections:
                    for j, collection in enumerate(collections, 1):
                        print(f"      {j}. {collection}")
                        
                        # Compter les documents dans la collection
                        count = await db[collection].count_documents({})
                        print(f"         📊 {count} document(s)")
                else:
                    print("      (aucune collection)")
        else:
            print("   (aucune base de données)")
        
        # Vérifier spécifiquement la base 'realestate'
        if 'realestate' in databases:
            print(f"\n🏠 Base de données 'realestate' trouvée")
            db = client['realestate']
            collections = await db.list_collection_names()
            
            if collections:
                print(f"📋 Collections dans 'realestate':")
                for i, collection in enumerate(collections, 1):
                    count = await db[collection].count_documents({})
                    print(f"   {i}. {collection} ({count} document(s))")
                    
                    # Chercher la propriété 21002530 dans cette collection
                    if "chambly" in collection.lower() or "test" in collection.lower():
                        print(f"      🔍 Recherche de la propriété 21002530...")
                        property_doc = await db[collection].find_one({"id": "21002530"})
                        if property_doc:
                            print(f"      ✅ Propriété 21002530 trouvée!")
                            print(f"         📍 Adresse: {property_doc.get('address', {}).get('street', 'N/A')}")
                            print(f"         💰 Prix: {property_doc.get('financial', {}).get('price', 'N/A')}")
                        else:
                            print(f"      ❌ Propriété 21002530 non trouvée")
            else:
                print("   (aucune collection)")
        else:
            print(f"\n❌ Base de données 'realestate' non trouvée")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification MongoDB: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if 'client' in locals():
            client.close()
            print("\n🔌 Connexion MongoDB fermée")

if __name__ == "__main__":
    asyncio.run(check_mongodb())
