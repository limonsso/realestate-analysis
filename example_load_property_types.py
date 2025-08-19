#!/usr/bin/env python3
"""
Exemple d'utilisation du chargeur MongoDB pour les types de propriétés
"""

import pandas as pd
from lib.mongodb_loader import MongoDBLoader
from lib.property_type_normalizer import PropertyTypeNormalizer
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_property_types_from_mongo():
    """
    Charge les types de propriétés depuis MongoDB
    
    Returns:
        List[Dict]: Liste des types de propriétés
    """
    print("🔗 Chargement des types de propriétés depuis MongoDB...")
    
    # Initialiser le chargeur MongoDB
    loader = MongoDBLoader()
    
    # Connexion à la base de données
    if not loader.connect("real_estate_db"):
        print("❌ Impossible de se connecter à MongoDB")
        return []
    
    try:
        # Charger les types de propriétés
        property_types = loader.load_property_types()
        
        # Afficher les types chargés
        print(f"\n✅ {len(property_types)} types de propriétés chargés:")
        for i, prop_type in enumerate(property_types[:5]):  # Afficher les 5 premiers
            print(f"   {i+1}. ID: {prop_type.get('_id', 'N/A')}")
            display_names = prop_type.get('display_names', {})
            print(f"      Nom FR: {display_names.get('fr', 'N/A')}")
            print(f"      Nom EN: {display_names.get('en', 'N/A')}")
            print(f"      Catégorie: {prop_type.get('category', 'N/A')}")
            print()
        
        if len(property_types) > 5:
            print(f"   ... et {len(property_types) - 5} autres types")
        
        return property_types
        
    finally:
        # Fermer la connexion
        loader.disconnect()


def example_normalize_with_mongo_types():
    """
    Exemple d'utilisation du PropertyTypeNormalizer avec les types MongoDB
    """
    print("\n" + "="*60)
    print("🏠 EXEMPLE DE NORMALISATION AVEC LES TYPES MONGODB")
    print("="*60)
    
    # 1. Charger les types depuis MongoDB
    property_types = load_property_types_from_mongo()
    
    if not property_types:
        print("❌ Aucun type de propriété chargé depuis MongoDB")
        return
    
    # 2. Initialiser le normalisateur avec les données MongoDB
    print("\n🔧 Initialisation du normalisateur...")
    normalizer = PropertyTypeNormalizer(property_types_data=property_types, language='fr')
    
    # 3. Créer un DataFrame d'exemple avec des types non normalisés
    print("\n📊 Création d'un DataFrame d'exemple...")
    sample_data = {
        'id': range(1, 11),
        'type': [
            'Maison',
            'Condo',
            'Duplex',
            'Maison à vendre',
            'Condominium',
            'Triplex',
            'House',
            'Maison unifamiliale',
            'Copropriété',
            'Type inconnu'
        ],
        'prix': [350000, 280000, 450000, 520000, 320000, 380000, 400000, 600000, 290000, 150000]
    }
    
    df = pd.DataFrame(sample_data)
    print(f"✅ DataFrame créé avec {len(df)} propriétés")
    
    # 4. Normaliser les types
    print("\n🔄 Normalisation des types...")
    df_normalized = normalizer.normalize_property_types(df, type_column='type')
    
    # 5. Afficher les résultats
    print("\n📋 Résultats de la normalisation:")
    print(df_normalized[['id', 'type', 'type_id', 'prix']].to_string(index=False))
    
    # 6. Statistiques du normalisateur
    print("\n📈 Statistiques du normalisateur:")
    stats = normalizer.get_statistics()
    print(f"   📊 Total des types: {stats['total_types']}")
    print(f"   📊 Total des variations: {stats['total_variations']}")
    print(f"   📊 Catégories disponibles: {', '.join(stats['categories'])}")
    
    # 7. Afficher les catégories
    print("\n🗂️ Types par catégorie:")
    categories = normalizer.get_property_categories()
    for category, type_ids in categories.items():
        print(f"   📂 {category}: {len(type_ids)} types")
        for type_id in type_ids[:3]:  # Afficher les 3 premiers
            display_name = normalizer.display_names_map.get(type_id, type_id)
            print(f"      • {display_name}")
        if len(type_ids) > 3:
            print(f"      ... et {len(type_ids) - 3} autres")


def main():
    """Fonction principale"""
    print("🚀 CHARGEMENT DES TYPES DE PROPRIÉTÉS DEPUIS MONGODB")
    print("="*60)
    
    try:
        # Exemple complet
        example_normalize_with_mongo_types()
        
        print("\n✅ Exemple terminé avec succès!")
        print("\n💡 Pour utiliser dans votre code:")
        print("   1. Importez MongoDBLoader et PropertyTypeNormalizer")
        print("   2. Chargez les types avec loader.load_property_types()")
        print("   3. Initialisez le normalisateur avec ces données")
        print("   4. Utilisez normalize_property_types() sur votre DataFrame")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        logger.error(f"Erreur dans l'exemple: {e}")


if __name__ == "__main__":
    main() 