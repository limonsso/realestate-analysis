#!/usr/bin/env python3
"""
Exemple de PropertyTypeNormalizer language-agnostic
Démontre la capacité de normaliser des types en différentes langues
"""

import pandas as pd
from lib.property_type_normalizer import PropertyTypeNormalizer

def test_multilingual_normalizer():
    """Teste le normalisateur avec des types en différentes langues"""
    
    # Données d'exemple avec types en plusieurs langues
    property_types_data = [
        {
            "_id": "house_detached",
            "display_names": {
                "fr": "Maison unifamiliale",
                "en": "Single-family house"
            },
            "category": "Résidentiel"
        },
        {
            "_id": "condo_apartment",
            "display_names": {
                "fr": "Condominium",
                "en": "Condominium"
            },
            "category": "Résidentiel"
        },
        {
            "_id": "commercial_office",
            "display_names": {
                "fr": "Bureau commercial",
                "en": "Commercial office"
            },
            "category": "Commercial"
        },
        {
            "_id": "land_vacant",
            "display_names": {
                "fr": "Terrain vacant",
                "en": "Vacant land"
            },
            "category": "Terrain"
        }
    ]
    
    # Créer le normalisateur
    print("🔧 Création du normalisateur language-agnostic...")
    normalizer = PropertyTypeNormalizer(property_types_data, default_language='fr')
    
    # Afficher les statistiques
    stats = normalizer.get_statistics()
    print(f"\n📊 Statistiques du normalisateur:")
    print(f"   • Types totaux: {stats['total_types']}")
    print(f"   • Variations totales: {stats['total_variations']}")
    print(f"   • Langues supportées: {stats['supported_languages']}")
    print(f"   • Langue par défaut: {stats['default_language']}")
    
    # Données de test avec types mixtes (français et anglais)
    test_data = {
        'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'type': [
            "Maison unifamiliale",      # Français exact
            "Single-family house",      # Anglais exact
            "maison",                   # Français partiel
            "house",                    # Anglais partiel
            "Condo",                    # Variation commune
            "Condominium",              # Exact
            "Bureau commercial",        # Français exact
            "Commercial office",        # Anglais exact  
            "Terrain vacant",           # Français exact
            "Type inconnu"              # Non reconnu
        ],
        'prix': [300000, 250000, 400000, 350000, 200000, 180000, 500000, 450000, 100000, 275000]
    }
    
    df = pd.DataFrame(test_data)
    
    print(f"\n🏠 Test avec types mixtes français/anglais:")
    print("Types d'entrée:")
    for i, prop_type in enumerate(df['type'], 1):
        print(f"   {i}. {prop_type}")
    
    # Normaliser
    df_normalized = normalizer.normalize_property_types(df)
    
    # Afficher les résultats
    print(f"\n✅ Résultats de la normalisation:")
    print(f"Nouvelles colonnes créées: {[col for col in df_normalized.columns if col not in df.columns]}")
    
    print(f"\n📋 Mapping des types:")
    for i, row in df_normalized.iterrows():
        original = row['type']
        type_id = row['type_id']
        display = row['type_display']
        category = row['type_category']
        print(f"   {i+1}. '{original}' → {type_id} → '{display}' ({category})")
    
    # Test avec DataFrame plus complexe
    print(f"\n🔄 Test avec plus de variations:")
    
    complex_data = {
        'property_id': range(1, 21),
        'type': [
            "Maison unifamiliale", "Single-family house", "maison", "house", "home",
            "Condo", "Condominium", "condo", "condominium", "Condo à vendre",
            "Bureau commercial", "Commercial office", "office", "bureau",
            "Terrain vacant", "Vacant land", "land", "terrain", "lot",
            "Duplex"  # Non défini dans notre exemple
        ]
    }
    
    df_complex = pd.DataFrame(complex_data)
    df_complex_normalized = normalizer.normalize_property_types(df_complex)
    
    # Analyse des catégories
    print(f"\n📊 Distribution par catégorie:")
    category_counts = df_complex_normalized['type_category'].value_counts()
    for category, count in category_counts.items():
        print(f"   • {category}: {count} propriétés")
    
    # Analyse des types normalisés
    print(f"\n🏷️ Distribution par type normalisé:")
    type_counts = df_complex_normalized['type_id'].value_counts()
    for type_id, count in type_counts.items():
        display_name = normalizer.display_names_map.get(type_id, type_id)
        print(f"   • {display_name} ({type_id}): {count} propriétés")
    
    return df_normalized, df_complex_normalized

def demonstrate_language_flexibility():
    """Démontre la flexibilité linguistique"""
    
    print(f"\n" + "="*60)
    print("🌐 DÉMONSTRATION DE LA FLEXIBILITÉ LINGUISTIQUE")
    print("="*60)
    
    # Test avec des types similaires mais en différentes langues
    mixed_types = [
        "Maison", "House", "Home", "maison", "house", "home",
        "Appartement", "Apartment", "appartement", "apartment", "apt",
        "Terrain", "Land", "terrain", "land", "lot"
    ]
    
    # Données d'exemple étendues
    extended_data = [
        {
            "_id": "house_single",
            "display_names": {
                "fr": "Maison",
                "en": "House"
            },
            "category": "Résidentiel"
        },
        {
            "_id": "apartment_unit",
            "display_names": {
                "fr": "Appartement", 
                "en": "Apartment"
            },
            "category": "Résidentiel"
        },
        {
            "_id": "land_plot",
            "display_names": {
                "fr": "Terrain",
                "en": "Land"
            },
            "category": "Terrain"
        }
    ]
    
    normalizer = PropertyTypeNormalizer(extended_data, default_language='fr')
    
    print(f"\n🧪 Test de normalisation avec types mixtes:")
    
    for prop_type in mixed_types:
        normalized = normalizer._normalize_single_type(prop_type)
        display_name = normalizer.display_names_map.get(normalized, normalized)
        print(f"   '{prop_type}' → {normalized} → '{display_name}'")
    
    # Montrer toutes les variations reconnues
    print(f"\n📝 Variations reconnues par le normalisateur:")
    for variation, type_id in sorted(normalizer.property_types_map.items()):
        display_name = normalizer.display_names_map.get(type_id, type_id)
        print(f"   '{variation}' → {type_id} → '{display_name}'")

if __name__ == "__main__":
    print("🚀 Test du PropertyTypeNormalizer language-agnostic")
    print("="*60)
    
    # Test principal
    df_normalized, df_complex = test_multilingual_normalizer()
    
    # Démonstration de flexibilité
    demonstrate_language_flexibility()
    
    print(f"\n✅ Tests terminés avec succès!")
    print(f"💡 Le normalisateur peut maintenant traiter des types en français, anglais ou mixte!") 