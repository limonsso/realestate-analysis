#!/usr/bin/env python3
"""
Exemple simple pour charger les types de propriétés depuis MongoDB
"""

import pandas as pd
from lib.property_type_normalizer import PropertyTypeNormalizer

def example_simple_loading():
    """Exemple simple de chargement des types MongoDB"""
    print("🚀 EXEMPLE SIMPLE - CHARGEMENT DES TYPES MONGODB")
    print("="*50)
    
    # Méthode 1: Créer directement depuis MongoDB
    print("\n📍 Méthode 1: Création directe depuis MongoDB")
    try:
        normalizer = PropertyTypeNormalizer.create_from_mongodb(
            database_name="real_estate_db",
            language='fr'
        )
        
        # Afficher les statistiques
        stats = normalizer.get_statistics()
        print(f"✅ Normalisateur créé avec {stats['total_types']} types")
        
        # Exemple de normalisation rapide
        sample_types = ['Maison', 'Condo', 'Duplex', 'House', 'Condominium']
        print(f"\n🔄 Test de normalisation:")
        for original_type in sample_types:
            normalized = normalizer._normalize_single_type(original_type)
            display_name = normalizer.display_names_map.get(normalized, normalized)
            print(f"   '{original_type}' → '{display_name}'")
            
    except Exception as e:
        print(f"❌ Erreur méthode 1: {e}")
    
    # Méthode 2: Charger dans un normalisateur existant
    print("\n📍 Méthode 2: Chargement dans un normalisateur existant")
    try:
        normalizer2 = PropertyTypeNormalizer(language='fr')
        normalizer2.load_from_mongodb(database_name="real_estate_db")
        
        stats2 = normalizer2.get_statistics()
        print(f"✅ Types chargés: {stats2['total_types']}")
        
        # Afficher les catégories
        print(f"\n🗂️ Catégories disponibles:")
        for category, type_ids in normalizer2.get_property_categories().items():
            print(f"   📂 {category}: {len(type_ids)} types")
            
    except Exception as e:
        print(f"❌ Erreur méthode 2: {e}")


def example_with_dataframe():
    """Exemple avec un DataFrame réel"""
    print("\n" + "="*50)
    print("📊 EXEMPLE AVEC DATAFRAME")
    print("="*50)
    
    try:
        # Créer le normalisateur
        normalizer = PropertyTypeNormalizer.create_from_mongodb()
        
        # Créer un DataFrame d'exemple
        data = {
            'id': [1, 2, 3, 4, 5],
            'type': ['Maison unifamiliale', 'Condo', 'Duplex', 'House', 'Appartement'],
            'prix': [450000, 320000, 380000, 520000, 280000],
            'ville': ['Montréal', 'Québec', 'Laval', 'Gatineau', 'Sherbrooke']
        }
        
        df = pd.DataFrame(data)
        print(f"📄 DataFrame original:")
        print(df.to_string(index=False))
        
        # Normaliser
        df_normalized = normalizer.normalize_property_types(df, type_column='type')
        
        print(f"\n✅ DataFrame normalisé:")
        print(df_normalized[['id', 'type', 'type_id', 'prix', 'ville']].to_string(index=False))
        
    except Exception as e:
        print(f"❌ Erreur: {e}")


def main():
    """Fonction principale"""
    print("🏠 CHARGEMENT DES TYPES DE PROPRIÉTÉS - EXEMPLES SIMPLES")
    print("="*60)
    
    # Exemple simple
    example_simple_loading()
    
    # Exemple avec DataFrame
    example_with_dataframe()
    
    print("\n" + "="*60)
    print("✅ EXEMPLES TERMINÉS")
    print("\n💡 Utilisation recommandée:")
    print("   # Création directe depuis MongoDB")
    print("   normalizer = PropertyTypeNormalizer.create_from_mongodb()")
    print("   ")
    print("   # Normalisation d'un DataFrame")
    print("   df_normalized = normalizer.normalize_property_types(df)")
    print("   ")
    print("   # Ou chargement dans un normalisateur existant")
    print("   normalizer = PropertyTypeNormalizer()")
    print("   normalizer.load_from_mongodb()")


if __name__ == "__main__":
    main() 