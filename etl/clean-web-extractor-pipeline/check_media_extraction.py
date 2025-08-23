#!/usr/bin/env python3
"""
Script de vérification de l'extraction des médias
Vérifie que les images sont bien extraites et sauvegardées
"""

import pymongo
from datetime import datetime

def check_media_extraction():
    """Vérifie l'extraction des médias dans la dernière collection"""
    
    print("🔍 Vérification de l'extraction des médias")
    print("=" * 50)
    
    try:
        # Connexion directe à MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        
        # Lister toutes les bases de données
        print("📊 Bases de données disponibles:")
        for db_name in client.list_database_names():
            print(f"   - {db_name}")
        
        # Essayer de trouver la base de données avec les collections Chambly
        for db_name in client.list_database_names():
            if db_name not in ['admin', 'local', 'config']:  # Ignorer les bases système
                db = client[db_name]
                collections = db.list_collection_names()
                chambly_collections = [col for col in collections if "chambly_plex_test" in col]
                
                if chambly_collections:
                    print(f"\n🎯 Collection(s) Chambly trouvée(s) dans {db_name}:")
                    for col in chambly_collections:
                        print(f"   - {col}")
                    
                    # Analyser la dernière collection
                    latest_collection = sorted(chambly_collections, key=lambda x: x.split('_')[-2] + '_' + x.split('_')[-1] if len(x.split('_')) >= 4 else '00000000_000000', reverse=True)[0]
                    print(f"\n📊 Collection analysée: {latest_collection}")
                    
                    # Récupérer toutes les propriétés
                    collection = db[latest_collection]
                    properties = list(collection.find({}))
                    
                    if not properties:
                        print("❌ Aucune propriété trouvée")
                        return
                    
                    print(f"🏠 {len(properties)} propriétés trouvées")
                    print()
                    
                    # Analyser les médias de chaque propriété
                    for i, prop in enumerate(properties, 1):
                        print(f"🏠 Propriété {i}: {prop.get('address', {}).get('street', 'N/A')}")
                        
                        media = prop.get('media', {})
                        images = media.get('images', [])
                        image_count = media.get('image_count', 0)
                        main_image = media.get('main_image')
                        virtual_tour = media.get('virtual_tour_url')
                        
                        print(f"   🖼️ Nombre d'images: {image_count}")
                        print(f"   🖼️ Image principale: {main_image[:80] + '...' if main_image and len(main_image) > 80 else main_image}")
                        print(f"   🎥 Visite virtuelle: {virtual_tour or 'Non disponible'}")
                        
                        if images:
                            print(f"   📸 Premières images:")
                            for j, img in enumerate(images[:3], 1):  # Afficher les 3 premières
                                print(f"      {j}. {img[:80] + '...' if len(img) > 80 else img}")
                            if len(images) > 3:
                                print(f"      ... et {len(images) - 3} autres")
                        else:
                            print("   ❌ Aucune image trouvée")
                        
                        print()
                    
                    # Statistiques globales
                    total_images = sum(prop.get('media', {}).get('image_count', 0) for prop in properties)
                    properties_with_images = sum(1 for prop in properties if prop.get('media', {}).get('images'))
                    
                    print("📊 STATISTIQUES DES MÉDIAS")
                    print("=" * 30)
                    print(f"🏠 Propriétés avec images: {properties_with_images}/{len(properties)}")
                    print(f"🖼️ Total d'images: {total_images}")
                    print(f"📸 Moyenne par propriété: {total_images/len(properties):.1f}")
                    
                    if properties_with_images == len(properties):
                        print("✅ SUCCÈS: Toutes les propriétés ont des images !")
                    else:
                        print(f"⚠️ ATTENTION: {len(properties) - properties_with_images} propriétés sans images")
                    
                    break
        else:
            print("\n❌ Aucune collection de test Chambly trouvée dans aucune base de données")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    check_media_extraction()
