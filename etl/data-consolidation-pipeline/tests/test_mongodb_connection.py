#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Test de connexion MongoDB
============================

Script simple pour tester la connectivité MongoDB
"""

import pymongo
import json
from pathlib import Path

def test_mongodb_connection():
    """Test de la connexion MongoDB"""
    print("🔍 Test de connexion MongoDB...")
    
    try:
        # Connexion par défaut (localhost:27017)
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        
        # Test de la connexion
        client.admin.command('ping')
        print("✅ Connexion MongoDB réussie")
        
        # Lister les bases de données
        databases = client.list_database_names()
        print(f"📊 Bases de données disponibles: {databases}")
        
        # Si real_estate_db existe, lister les collections
        if 'real_estate_db' in databases:
            db = client['real_estate_db']
            collections = db.list_collection_names()
            print(f"📁 Collections dans real_estate_db: {collections}")
            
            # Si properties existe, compter les documents
            if 'properties' in collections:
                count = db.properties.count_documents({})
                print(f"📊 Nombre total de propriétés: {count}")
                
                # Test de la requête Trois-Rivières triplex
                query = {
                    "city": {"$regex": "Trois-Rivières", "$options": "i"},
                    "type": {"$regex": "triplex", "$options": "i"}
                }
                
                triplex_count = db.properties.count_documents(query)
                print(f"🏠 Propriétés Trois-Rivières triplex: {triplex_count}")
                
                # Aperçu d'un document
                if triplex_count > 0:
                    sample = db.properties.find_one(query)
                    print(f"📋 Exemple de document:")
                    print(f"   Type: {sample.get('type', 'N/A')}")
                    print(f"   Ville: {sample.get('city', 'N/A')}")
                    print(f"   Prix: {sample.get('price', 'N/A')}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion MongoDB: {e}")
        return False

def test_query_file():
    """Test du fichier de requête JSON"""
    print("\n📄 Test du fichier de requête...")
    
    query_file = Path("examples/query_test_final.json")
    if query_file.exists():
        try:
            with open(query_file, 'r', encoding='utf-8') as f:
                query = json.load(f)
            print(f"✅ Fichier de requête chargé: {query}")
            return query
        except Exception as e:
            print(f"❌ Erreur lecture fichier: {e}")
            return None
    else:
        print(f"❌ Fichier non trouvé: {query_file}")
        return None

if __name__ == "__main__":
    print("🧪 === TEST CONNEXION MONGODB ===\n")
    
    # Test connexion
    connection_ok = test_mongodb_connection()
    
    # Test fichier de requête
    query = test_query_file()
    
    print(f"\n📊 Résumé:")
    print(f"   Connexion MongoDB: {'✅' if connection_ok else '❌'}")
    print(f"   Fichier requête: {'✅' if query else '❌'}")
    
    if connection_ok and query:
        print("\n🚀 Prêt pour le pipeline MongoDB !")
    else:
        print("\n⚠️ Vérifiez la configuration avant de lancer le pipeline")
