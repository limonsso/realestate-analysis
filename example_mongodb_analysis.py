#!/usr/bin/env python3
"""
Exemple d'utilisation du système d'analyse immobilière avec MongoDB
Inclut la normalisation des types de propriétés
"""

import pandas as pd
import numpy as np
from lib import PropertyAnalyzer
from lib.mongodb_loader import MongoDBLoader
from lib.data_processors import PropertyDataProcessor
from lib.property_type_normalizer import PropertyTypeNormalizer

def example_with_mongodb():
    """Exemple complet avec données MongoDB réelles"""
    print("🚀 === EXEMPLE D'ANALYSE AVEC MONGODB ===")
    
    # 1. Connexion MongoDB
    loader = MongoDBLoader("mongodb://localhost:27017/")
    if not loader.connect("realestate"):
        print("❌ Impossible de se connecter à MongoDB")
        return
    
    try:
        # 2. Charger les types de propriétés
        print("\n📚 Chargement des types de propriétés...")
        property_types = loader.load_property_types()
        
        if not property_types:
            print("⚠️ Aucun type de propriété trouvé, utilisation sans normalisation")
            property_types = None
        
        # 3. Charger un échantillon de propriétés
        print("\n📊 Chargement des propriétés...")
        df = loader.load_sample_data(
            collection_name="properties",
            sample_size=2000,
            filters={"vendue": False}  # Seulement les propriétés non vendues
        )
        
        if df.empty:
            print("❌ Aucune propriété trouvée")
            return
        
        # 4. Afficher un résumé des données
        loader.print_data_summary(df)
        
        # 5. Valider la qualité des données
        validation = loader.validate_data_quality(df)
        print(f"\n🔍 Validation de la qualité:")
        print(f"   📊 Lignes: {validation['total_rows']:,}")
        print(f"   📈 Colonnes: {validation['total_columns']}")
        print(f"   💰 Prix manquants: {validation['missing_price']:,}")
        print(f"   📐 Surface manquante: {validation['missing_living_area']:,}")
        
        if validation['missing_required_columns']:
            print(f"   ⚠️ Colonnes requises manquantes: {validation['missing_required_columns']}")
        
        # 6. Créer l'analyseur avec normalisation des types
        print(f"\n🔧 Création de l'analyseur...")
        analyzer = PropertyAnalyzer()
        
        # Personnaliser le processeur avec les types de propriétés
        if property_types:
            processor = PropertyDataProcessor(property_types_data=property_types)
            analyzer.data_processor = processor
            print(f"✅ Normalisateur de types intégré ({len(property_types)} types)")
        
        # 7. Exécuter l'analyse complète
        print(f"\n🎯 Lancement de l'analyse...")
        results = analyzer.analyze_properties(df, target_column='price')
        
        # 8. Afficher les résultats
        print(f"\n🏆 === RÉSULTATS DE L'ANALYSE ===")
        print(f"📊 Propriétés analysées: {results['shape_original'][0]:,}")
        print(f"📈 Variables initiales: {results['shape_original'][1]}")
        print(f"📉 Variables finales: {results['shape_processed'][1]}")
        print(f"✅ Variables sélectionnées: {len(results['selected_features'])}")
        
        # Classification
        if 'classification_stats' in results:
            stats = results['classification_stats']
            print(f"\n🏠 === CLASSIFICATION ===")
            for category, count in stats.get('counts', {}).items():
                pct = stats.get('percentages', {}).get(category, 0)
                print(f"🏷️ {category}: {count:,} propriétés ({pct:.1f}%)")
        
        # Variables importantes
        if 'feature_importance' in results:
            print(f"\n🎯 === TOP 10 VARIABLES IMPORTANTES ===")
            importance = results['feature_importance']
            for i, (feature, imp) in enumerate(
                sorted(importance.items(), key=lambda x: x[1], reverse=True)[:10], 1
            ):
                print(f"{i:2d}. {feature}: {imp:.4f}")
        
        # 9. Résumé final
        summary = analyzer.get_summary()
        print(f"\n📋 === RÉSUMÉ FINAL ===")
        print(f"📊 Total propriétés: {summary['total_properties']:,}")
        print(f"📈 Variables totales: {summary['total_features']}")
        print(f"✅ Variables sélectionnées: {summary['selected_features_count']}")
        print(f"📉 Réduction: {summary['reduction_percentage']:.1f}%")
        
        if 'price_stats' in summary:
            price_stats = summary['price_stats']
            print(f"💰 Prix - Moy: ${price_stats['mean']:,.0f}, Méd: ${price_stats['median']:,.0f}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur pendant l'analyse: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Fermer la connexion
        loader.disconnect()

def example_without_mongodb():
    """Exemple avec données factices (sans MongoDB)"""
    print("🚀 === EXEMPLE AVEC DONNÉES FACTICES ===")
    
    # Créer des données factices avec types de propriétés
    np.random.seed(42)
    n_samples = 500
    
    # Types de propriétés factices basés sur la structure MongoDB
    property_types_data = [
        {
            "_id": "maison",
            "category": "Résidentiel",
            "display_names": {
                "fr": "Maison à vendre",
                "en": "House for sale"
            }
        },
        {
            "_id": "condo",
            "category": "Résidentiel", 
            "display_names": {
                "fr": "Condo à vendre",
                "en": "Condo for sale"
            }
        },
        {
            "_id": "duplex",
            "category": "Résidentiel",
            "display_names": {
                "fr": "Duplex à vendre", 
                "en": "Duplex for sale"
            }
        },
        {
            "_id": "triplex",
            "category": "Résidentiel",
            "display_names": {
                "fr": "Triplex à vendre",
                "en": "Triplex for sale"
            }
        }
    ]
    
    # Générer des données factices
    test_data = []
    for i in range(n_samples):
        # Prix aléatoire
        price = np.random.lognormal(13.5, 0.4)
        
        # Type de propriété
        prop_types = ["Maison à vendre", "Condo à vendre", "Duplex à vendre", "Triplex à vendre"]
        prop_type = np.random.choice(prop_types)
        
        # Autres variables
        living_area = np.random.normal(2000, 800)
        living_area = max(800, min(5000, living_area))
        
        bedrooms = np.random.randint(1, 6)
        bathrooms = np.random.randint(1, 5)
        
        municipal_evaluation = price * np.random.uniform(0.6, 0.9)
        
        property_data = {
            "price": int(price),
            "type": prop_type,
            "living_area": int(living_area),
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "municipal_evaluation_total": int(municipal_evaluation),
            "year_built": np.random.randint(1950, 2025),
            "city": np.random.choice(['Montréal', 'Laval', 'Longueuil']),
            "region": np.random.choice(['Montérégie', 'Laval', 'Montréal'])
        }
        
        test_data.append(property_data)
    
    df = pd.DataFrame(test_data)
    print(f"✅ Données factices créées: {df.shape}")
    
    # Créer l'analyseur avec normalisation des types
    processor = PropertyDataProcessor(property_types_data=property_types_data)
    analyzer = PropertyAnalyzer(data_processor=processor)
    
    # Exécuter l'analyse
    print(f"\n🎯 Lancement de l'analyse...")
    results = analyzer.analyze_properties(df, target_column='price')
    
    print(f"\n🏆 === RÉSULTATS ===")
    print(f"Variables sélectionnées: {results['selected_features']}")
    
    return True

def main():
    """Fonction principale"""
    print("🏠 === SYSTÈME D'ANALYSE IMMOBILIÈRE AVEC NORMALISATION DES TYPES ===")
    
    # Essayer d'abord avec MongoDB
    print("\n1️⃣ Tentative d'analyse avec MongoDB...")
    success = example_with_mongodb()
    
    if not success:
        print("\n2️⃣ Fallback vers données factices...")
        example_without_mongodb()
    
    print(f"\n🎉 === ANALYSE TERMINÉE ===")

if __name__ == "__main__":
    main() 