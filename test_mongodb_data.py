#!/usr/bin/env python3
"""
Script de test pour le système d'analyse immobilière modulaire
Test avec des données MongoDB factices
"""

import pandas as pd
import numpy as np
import json
from lib import PropertyAnalyzer

def create_mongodb_test_data(n_samples=100):
    """Crée des données de test basées sur la structure MongoDB fournie"""
    print("🔧 Création de données MongoDB de test...")
    
    np.random.seed(42)
    
    # Générer des données factices basées sur la structure MongoDB
    test_data = []
    
    for i in range(n_samples):
        # Prix aléatoire avec distribution réaliste
        price = np.random.lognormal(13.5, 0.4)  # Distribution log-normale pour les prix
        
        # Surface habitable (pi²)
        living_area = np.random.normal(2000, 800)
        living_area = max(800, min(5000, living_area))  # Limiter entre 800 et 5000 pi²
        
        # Taille du terrain (pi²)
        lot_size = np.random.lognormal(9.5, 0.5)
        
        # Année de construction
        year_built = np.random.randint(1950, 2025)
        
        # Nombre de chambres et salles de bain
        bedrooms = np.random.randint(1, 6)
        bathrooms = np.random.randint(1, 5)
        
        # Évaluation municipale (corrélée avec le prix)
        municipal_evaluation = price * np.random.uniform(0.6, 0.9)
        
        # Taxes
        municipal_tax = municipal_evaluation * 0.006  # ~0.6% de l'évaluation
        school_tax = municipal_evaluation * 0.001     # ~0.1% de l'évaluation
        
        # Coordonnées géographiques (Montréal et environs)
        latitude = np.random.normal(45.5, 0.2)
        longitude = np.random.normal(-73.6, 0.3)
        
        # Type de propriété
        property_types = ['Maison à vendre', 'Condo à vendre', 'Duplex à vendre', 'Triplex à vendre']
        property_type = np.random.choice(property_types, p=[0.6, 0.3, 0.08, 0.02])
        
        # Ville
        cities = ['Montréal', 'Laval', 'Longueuil', 'Brossard', 'Saint-Laurent', 'Dorval']
        city = np.random.choice(cities)
        
        # Région
        regions = ['Montérégie', 'Laval', 'Montréal', 'Laurentides']
        region = np.random.choice(regions)
        
        # Style de construction
        building_styles = ['À étages, Détaché', 'Bungalow, Détaché', 'Cottage, Détaché', 'Moderne, Détaché']
        building_style = np.random.choice(building_styles)
        
        # Créer l'objet de données
        property_data = {
            "_id": 20000000 + i,
            "price": int(price),
            "living_area": int(living_area),
            "lot_size": int(lot_size),
            "year_built": year_built,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "municipal_evaluation_total": int(municipal_evaluation),
            "municipal_tax": int(municipal_tax),
            "school_tax": int(school_tax),
            "latitude": latitude,
            "longitude": longitude,
            "type": property_type,
            "city": city,
            "region": region,
            "building_style": building_style,
            "surface": np.random.uniform(0.1, 2.0),  # Surface en acres/hectares
            "municipal_evaluation_building": int(municipal_evaluation * 0.7),
            "municipal_evaluation_land": int(municipal_evaluation * 0.3),
            "municipal_evaluation_year": 2024,
            "basement": "Sous-sol 6 pieds +",
            "vendue": False,
            "company": "Centris",
            "version": "1.0.0"
        }
        
        test_data.append(property_data)
    
    return test_data

def test_mongodb_analysis():
    """Test complet du système avec des données MongoDB"""
    print("🚀 === TEST DU SYSTÈME MODULAIRE MONGODB ===")
    
    # Créer les données de test
    test_data = create_mongodb_test_data(100)
    print(f"✅ Données de test créées: {len(test_data)} propriétés")
    
    # Convertir en DataFrame
    df_test = pd.DataFrame(test_data)
    print(f"📊 DataFrame créé: {df_test.shape}")
    
    # Afficher quelques statistiques initiales
    print(f"\n📈 Statistiques initiales:")
    print(f"   💰 Prix moyen: ${df_test['price'].mean():,.0f}")
    print(f"   📐 Surface habitable moyenne: {df_test['living_area'].mean():.0f} pi²")
    print(f"   🏠 Nombre de chambres moyen: {df_test['bedrooms'].mean():.1f}")
    print(f"   🚿 Nombre de salles de bain moyen: {df_test['bathrooms'].mean():.1f}")
    
    # Tester le pipeline complet
    try:
        print(f"\n🔧 Lancement de l'analyse complète...")
        analyzer = PropertyAnalyzer()
        results = analyzer.analyze_properties(df_test, target_column='price')
        
        print(f"\n🎉 === TEST RÉUSSI! ===")
        print(f"📊 Variables sélectionnées ({len(results['selected_features'])}):")
        for i, feature in enumerate(results['selected_features'], 1):
            print(f"   {i:2d}. {feature}")
        
        # Afficher les statistiques de classification
        if 'classification_stats' in results:
            stats = results['classification_stats']
            print(f"\n🏠 Classification des propriétés:")
            for category, count in stats.get('counts', {}).items():
                pct = stats.get('percentages', {}).get(category, 0)
                print(f"   🏷️ {category}: {count} propriétés ({pct:.1f}%)")
        
        # Afficher un résumé
        summary = analyzer.get_summary()
        print(f"\n📋 Résumé de l'analyse:")
        print(f"   📊 Total propriétés: {summary['total_properties']}")
        print(f"   📈 Variables totales: {summary['total_features']}")
        print(f"   ✅ Variables sélectionnées: {summary['selected_features_count']}")
        print(f"   📉 Réduction: {summary['reduction_percentage']:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur pendant le test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_modules():
    """Test des modules individuels"""
    print(f"\n🔧 === TEST DES MODULES INDIVIDUELS ===")
    
    # Créer des données de test
    test_data = create_mongodb_test_data(50)
    df_test = pd.DataFrame(test_data)
    
    # Test du processeur de données
    print(f"\n🧹 Test du processeur de données...")
    from lib.data_processors import PropertyDataProcessor
    processor = PropertyDataProcessor()
    df_processed = processor.clean_data(df_test)
    print(f"   ✅ Nettoyage terminé: {df_test.shape[1]} → {df_processed.shape[1]} colonnes")
    
    # Test du classificateur
    print(f"\n🏠 Test du classificateur...")
    from lib.classifiers import PropertyClassifier
    classifier = PropertyClassifier()
    df_classified = classifier.classify_properties(df_processed)
    print(f"   ✅ Classification terminée")
    
    # Test du sélecteur de variables
    print(f"\n🎯 Test du sélecteur de variables...")
    from lib.feature_selectors import FeatureSelector
    selector = FeatureSelector()
    
    if 'price' in df_classified.columns:
        X = df_classified.drop(columns=['price'])
        y = df_classified['price']
        selected_features = selector.select_features(X, y)
        print(f"   ✅ Sélection terminée: {len(selected_features)} variables sélectionnées")
    
    print(f"✅ Tous les modules fonctionnent correctement!")

if __name__ == "__main__":
    # Test complet
    success = test_mongodb_analysis()
    
    if success:
        # Test des modules individuels
        test_individual_modules()
        
        print(f"\n🏆 === TOUS LES TESTS RÉUSSIS! ===")
        print(f"✅ Le système modulaire est prêt pour les données MongoDB")
    else:
        print(f"\n❌ === TESTS ÉCHOUÉS ===")
        print(f"⚠️ Des problèmes ont été détectés") 