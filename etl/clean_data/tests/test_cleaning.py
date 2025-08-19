#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 TEST DU SYSTÈME DE NETTOYAGE IMMOBILIER
===========================================

Script de test avec des données d'exemple pour valider le pipeline de nettoyage
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import sys

# Ajouter le répertoire courant au path
sys.path.append('.')

try:
    from real_estate_data_cleaning import RealEstateDataCleaner
    print("✅ Script de nettoyage importé avec succès!")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("Assurez-vous que le fichier real_estate_data_cleaning.py est dans le même répertoire")
    sys.exit(1)


def create_sample_dataset(n_properties=100):
    """
    Crée un dataset d'exemple avec des données réalistes mais problématiques
    pour tester le système de nettoyage
    """
    print("🔧 Création du dataset d'exemple...")
    
    # Données de base
    cities = ['Montréal', 'Québec', 'Laval', 'Gatineau', 'Longueuil', 'Sherbrooke']
    regions = ['Montérégie', 'Capitale-Nationale', 'Laval', 'Outaouais', 'Estrie']
    property_types = ['Maison unifamiliale', 'Condo', 'Duplex', 'Triplex', 'Appartement']
    
    # Génération des données
    data = []
    
    for i in range(n_properties):
        # Identifiants
        property_id = f"PROP_{i:06d}"
        link = f"https://example.com/property/{i}"
        company = random.choice(['Centris', 'DuProprio', 'RE/MAX', 'Royal LePage'])
        version = random.choice(['v1', 'v2', 'v3'])
        
        # Dates (avec incohérences)
        base_date = datetime.now() - timedelta(days=random.randint(1, 365))
        created_at = base_date
        updated_at = base_date + timedelta(days=random.randint(0, 30))
        update_at = base_date + timedelta(days=random.randint(0, 30))
        add_date = base_date + timedelta(days=random.randint(-5, 5))
        
        # Localisation
        city = random.choice(cities)
        region = random.choice(regions)
        address = f"{random.randint(100, 9999)} {random.choice(['Rue', 'Avenue', 'Boulevard'])} {city}"
        full_address = f"{address}, QC"
        
        # Coordonnées (avec quelques erreurs)
        if random.random() < 0.95:  # 95% de coordonnées valides
            longitude = random.uniform(-79.0, -56.0)  # Québec
            latitude = random.uniform(45.0, 62.0)
        else:  # 5% de coordonnées invalides
            longitude = random.uniform(-180, 180)
            latitude = random.uniform(-90, 90)
        
        # Prix et évaluations
        base_price = random.randint(200000, 2000000)
        price = base_price + random.randint(-50000, 50000)
        
        # Revenus (avec variations de noms de colonnes)
        revenu = random.randint(1500, 8000) * 12 if random.random() < 0.7 else None
        plex_revenue = random.randint(2000, 10000) * 12 if random.random() < 0.6 else None
        plex_revenu = random.randint(1800, 9000) * 12 if random.random() < 0.5 else None
        
        # Évaluations municipales
        municipal_evaluation_building = base_price * random.uniform(0.7, 1.3)
        municipal_evaluation_land = base_price * random.uniform(0.2, 0.5)
        municipal_evaluation_total = municipal_evaluation_building + municipal_evaluation_land
        
        # Taxes
        municipal_taxes = random.randint(2000, 8000)
        school_taxes = random.randint(1000, 4000)
        municipal_tax = municipal_taxes + random.randint(-500, 500)  # Doublon avec variation
        school_tax = school_taxes + random.randint(-200, 200)  # Doublon avec variation
        
        # Caractéristiques physiques
        surface = random.randint(800, 5000)
        living_area = surface + random.randint(-200, 200)  # Doublon avec variation
        construction_year = random.randint(1950, 2024)
        year_built = construction_year + random.randint(-2, 2)  # Doublon avec variation
        lot_size = surface * random.uniform(1.5, 3.0)
        
        # Propriété
        property_type = random.choice(property_types)
        bedrooms = random.randint(1, 6)
        nb_bedroom = bedrooms + random.randint(-1, 1)  # Doublon avec variation
        bathrooms = random.randint(1, 4)
        nb_bathroom = bathrooms + random.randint(-1, 1)  # Doublon avec variation
        units = random.randint(1, 8) if 'plex' in property_type.lower() else 1
        residential_units = units if 'plex' in property_type.lower() else 1
        commercial_units = random.randint(0, 2) if random.random() < 0.3 else 0
        
        # Autres
        parking = random.randint(0, 4)
        basement = random.choice(['Oui', 'Non', 'Partiel'])
        building_style = random.choice(['Moderne', 'Traditionnel', 'Contemporain', 'Victorian'])
        
        # Dépenses
        depenses = random.randint(500, 3000) * 12 if random.random() < 0.6 else None
        
        # Statut
        vendue = random.choice([True, False])
        
        # Description
        description = f"Belle propriété {property_type.lower()} à {city} avec {bedrooms} chambres et {bathrooms} salles de bain."
        
        # Images
        img_src = f"https://example.com/images/property_{i}.jpg"
        image = img_src
        images = [img_src]
        
        # Métadonnées
        extraction_metadata = {
            "source": company,
            "extraction_date": base_date.isoformat(),
            "confidence": random.uniform(0.8, 1.0)
        }
        municipal_evaluation_year = random.randint(2018, 2024)
        
        # Créer l'enregistrement
        property_record = {
            '_id': property_id,
            'link': link,
            'company': company,
            'version': version,
            'created_at': created_at,
            'updated_at': updated_at,
            'update_at': update_at,
            'add_date': add_date,
            'address': address,
            'full_address': full_address,
            'city': city,
            'region': region,
            'longitude': longitude,
            'latitude': latitude,
            'price': price,
            'revenu': revenu,
            'plex-revenue': plex_revenue,
            'plex-revenu': plex_revenu,
            'municipal_evaluation_building': municipal_evaluation_building,
            'municipal_evaluation_land': municipal_evaluation_land,
            'municipal_evaluation_total': municipal_evaluation_total,
            'municipal_taxes': municipal_taxes,
            'school_taxes': school_taxes,
            'municipal_tax': municipal_tax,
            'school_tax': school_tax,
            'surface': surface,
            'living_area': living_area,
            'construction_year': construction_year,
            'year_built': year_built,
            'lot_size': lot_size,
            'type': property_type,
            'bedrooms': bedrooms,
            'nb_bedroom': nb_bedroom,
            'bathrooms': bathrooms,
            'nb_bathroom': nb_bathroom,
            'unites': units,
            'residential_units': residential_units,
            'commercial_units': commercial_units,
            'parking': parking,
            'basement': basement,
            'building_style': building_style,
            'depenses': depenses,
            'vendue': vendue,
            'description': description,
            'img_src': img_src,
            'image': image,
            'images': images,
            'extraction_metadata': extraction_metadata,
            'municipal_evaluation_year': municipal_evaluation_year
        }
        
        data.append(property_record)
    
    # Créer le DataFrame
    df = pd.DataFrame(data)
    
    # Ajouter quelques doublons pour tester la déduplication
    if n_properties > 10:
        duplicates = df.head(5).copy()
        duplicates['_id'] = [f"DUPL_{i:06d}" for i in range(5)]
        df = pd.concat([df, duplicates], ignore_index=True)
    
    print(f"✅ Dataset d'exemple créé: {df.shape}")
    return df


def test_cleaning_pipeline():
    """Teste le pipeline complet de nettoyage"""
    print("\n🧪 TEST DU PIPELINE COMPLET DE NETTOYAGE")
    print("=" * 50)
    
    # 1. Créer le dataset d'exemple
    sample_df = create_sample_dataset(150)
    
    # 2. Sauvegarder temporairement
    temp_file = "sample_real_estate_data.csv"
    sample_df.to_csv(temp_file, index=False)
    print(f"💾 Dataset d'exemple sauvegardé: {temp_file}")
    
    # 3. Créer le nettoyeur
    cleaner = RealEstateDataCleaner(input_file=temp_file)
    
    # 4. Exécuter le pipeline complet
    print("\n🚀 EXÉCUTION DU PIPELINE COMPLET...")
    success = cleaner.run_complete_cleaning_pipeline()
    
    if success:
        print("\n🎉 TEST RÉUSSI! Pipeline de nettoyage fonctionne correctement.")
        
        # Afficher les résultats
        cleaned_df = cleaner.get_cleaned_data()
        print(f"\n📊 RÉSULTATS DU TEST:")
        print(f"  - Données originales: {len(sample_df)} propriétés")
        print(f"  - Données nettoyées: {len(cleaned_df)} propriétés")
        print(f"  - Colonnes originales: {len(sample_df.columns)}")
        print(f"  - Colonnes finales: {len(cleaned_df.columns)}")
        
        # Afficher quelques métriques
        if 'roi_brut' in cleaned_df.columns:
            roi_stats = cleaned_df['roi_brut'].describe()
            print(f"  - ROI brut moyen: {roi_stats['mean']:.2f}%")
        
        if 'completeness_score' in cleaned_df.columns:
            completeness_mean = cleaned_df['completeness_score'].mean()
            print(f"  - Score de complétude moyen: {completeness_mean:.1f}%")
        
        # Afficher le rapport de qualité
        quality_report = cleaner.get_quality_report()
        if quality_report:
            print(f"\n📋 RAPPORT DE QUALITÉ:")
            print(f"  - Timestamp: {quality_report.get('timestamp', 'N/A')}")
            if 'dataset_info' in quality_report:
                info = quality_report['dataset_info']
                print(f"  - Mémoire utilisée: {info.get('memory_usage_mb', 0):.2f} MB")
        
        # Nettoyer les fichiers temporaires
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"\n🧹 Fichier temporaire supprimé: {temp_file}")
        
        return True
    else:
        print("\n❌ TEST ÉCHOUÉ! Le pipeline de nettoyage a rencontré des erreurs.")
        return False


def test_individual_phases():
    """Teste chaque phase individuellement"""
    print("\n🔬 TEST DES PHASES INDIVIDUELLES")
    print("=" * 40)
    
    # Créer un petit dataset de test
    sample_df = create_sample_dataset(50)
    temp_file = "test_sample.csv"
    sample_df.to_csv(temp_file, index=False)
    
    # Créer le nettoyeur
    cleaner = RealEstateDataCleaner(input_file=temp_file)
    
    # Test Phase 1: Audit
    print("\n🔍 Test Phase 1: Audit et Diagnostic")
    if cleaner.load_data():
        audit_results = cleaner.phase1_audit_diagnostic()
        print(f"  ✅ Audit réussi: {len(audit_results)} analyses effectuées")
        
        # Test Phase 2: Nettoyage
        print("\n🛠️ Test Phase 2: Nettoyage Intelligent")
        if cleaner.phase2_cleaning_intelligent():
            print(f"  ✅ Nettoyage réussi: {cleaner.df_cleaned.shape}")
            
            # Test Phase 3: Enrichissement
            print("\n⚡ Test Phase 3: Enrichissement Intelligent")
            if cleaner.phase3_enrichment_intelligent():
                print(f"  ✅ Enrichissement réussi: {len(cleaner.df_cleaned.columns)} colonnes")
                
                # Test Phase 4: Validation
                print("\n🚨 Test Phase 4: Validation et Contrôle Qualité")
                validation_results = cleaner.phase4_validation_quality_control()
                if validation_results:
                    print(f"  ✅ Validation réussie: {len(validation_results)} tests effectués")
                    
                    # Test Phase 5: Préparation
                    print("\n🎯 Test Phase 5: Préparation pour l'Analyse")
                    if cleaner.phase5_preparation_analysis():
                        print("  ✅ Préparation réussie")
                        print("  🎉 Toutes les phases testées avec succès!")
                    else:
                        print("  ❌ Phase 5 échouée")
                else:
                    print("  ❌ Phase 4 échouée")
            else:
                print("  ❌ Phase 3 échouée")
        else:
            print("  ❌ Phase 2 échouée")
    else:
        print("  ❌ Phase 1 échouée")
    
    # Nettoyer
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    return True


if __name__ == "__main__":
    print("🧪 DÉMARRAGE DES TESTS DU SYSTÈME DE NETTOYAGE")
    print("=" * 60)
    
    # Test des phases individuelles
    test_individual_phases()
    
    # Test du pipeline complet
    test_cleaning_pipeline()
    
    print("\n🎯 TESTS TERMINÉS!")
    print("Le système de nettoyage est prêt à être utilisé avec vos vraies données immobilières.")

